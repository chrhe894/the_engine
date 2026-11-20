"""
Web Loop — Minimal web interface for the Adaptive Navigation Engine.

Usage:
    python web.py --new                    # fresh empty case
    python web.py engine                   # load existing case by name
    python web.py cases/826868e0.json      # load by path

Opens at http://localhost:5000
"""

import _bootstrap  # noqa: F401  (path + cwd setup)

import os
import json
import sys
import time
from functools import wraps
from pathlib import Path

from dotenv import load_dotenv
from flask import (
    Flask, render_template_string, request, redirect, url_for, session
)

import auth_client
from app_log import get_logger, attach_file_handler

load_dotenv()

from case_file import (
    CaseFile, Goal,
    GOAL_ACTIVE, GOAL_ABANDONED, GOAL_COMPLETED,
    DECISION_ACCEPT, DECISION_MODIFY, DECISION_REJECT,
    DECISION_EXPLORE, DECISION_GIVE_UP,
    MISSION_ACTIVE, MISSION_COMPLETED,
)
from case_file import (
    ConceptNode, SPEC_KEYS,
    ACTION_PROPOSED, ACTION_ACCEPTED, ACTION_DISMISSED, ACTION_LAYER_BASE, ACTION_LAYER_POINTS,
    CONCEPT_ACTIVE, CONCEPT_CANDIDATE, CONCEPT_PARKED, CONCEPT_STATUSES,
    CONCEPT_MODE_SPLIT, CONCEPT_MODE_VARY, CONCEPT_MODE_DEEP, CONCEPT_MODE_OWNER,
)
from engine_ai import AIEngine
from engine_concepts import (
    ConceptEngine, LENSES, DEFAULT_DEEP_LENSES, MAX_LENSES, POINTS_PER_RUN, pick_lens,
)
from observer import Observer
from i18n import t, set_language, get_language

# Default GUI language. Change with: LANG=en python src/web.py ...
set_language(os.environ.get("LANG_UI", "sv"))

log = get_logger("web")
app = Flask(__name__)
attach_file_handler(app.logger)  # unhandled errors (with traceback) go to the log file too
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-insecure-flask-secret")
app.jinja_env.globals["t"] = t          # make t() available in templates
app.jinja_env.filters["lens_name"] = lambda lid: LENSES.get(lid, {}).get("name", lid)
engine = AIEngine()
concept_engine = ConceptEngine(engine)
observer = Observer(client=engine.client, model=engine.model)
case: CaseFile = None
case_filepath: str = None


# --- Case file lookup ---

def find_case_file(query):
    path = Path(query)
    if path.exists():
        return str(path)
    cases_dir = Path("cases")
    if not cases_dir.exists():
        return None
    query_lower = query.lower()
    for f in sorted(cases_dir.glob("*.json")):
        if f.stem.startswith(query_lower):
            return str(f)
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            name = data.get("context", {}).get("description", "").lower()
            if query_lower in name:
                return str(f)
        except (json.JSONDecodeError, OSError):
            continue
    return None


def save_case():
    global case_filepath
    filepath = case.save(directory="cases")
    case_filepath = str(filepath)


# --- Case ownership & listing ---

CASES_DIR = Path("cases")


def _read_case_meta(path):
    """Return metadata for a case file, or None if unreadable."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return {
        "id": data.get("id", path.stem),
        "owner_id": data.get("owner_id"),
        "description": data.get("context", {}).get("description", "") or "(namnlöst)",
        "updated": data.get("updated", ""),
        "path": str(path),
    }


def list_cases_for(user):
    """List case metadata visible to this user. Admin sees all; a user sees
    their own cases plus legacy unowned cases (owner_id is None)."""
    if not CASES_DIR.exists():
        return []
    is_admin = user.get("role") == "admin"
    uid = user.get("id")
    metas = []
    for f in sorted(CASES_DIR.glob("*.json")):
        meta = _read_case_meta(f)
        if not meta:
            continue
        if is_admin or meta["owner_id"] == uid or meta["owner_id"] is None:
            metas.append(meta)
    metas.sort(key=lambda m: m["updated"], reverse=True)
    return metas


def can_access_case(user, meta):
    """True if the user may open/modify the given case."""
    if user.get("role") == "admin":
        return True
    return meta["owner_id"] in (user.get("id"), None)


def load_selected_case():
    """Load the case named in the session into the global `case`.
    Returns True if a case is loaded, False if none selected/found."""
    global case, case_filepath
    case_id = session.get("case_id")
    if not case_id:
        return False
    path = CASES_DIR / f"{case_id}.json"
    if not path.exists():
        return False
    case = CaseFile.load(str(path))
    case_filepath = str(path)
    return True


# --- Auth helpers ---

def get_current_user():
    """Return the logged-in user dict from the session, or None."""
    return session.get("user")


def login_required(f):
    """Decorator: redirects to /login if not authenticated."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not get_current_user():
            return redirect(url_for("login_page"))
        return f(*args, **kwargs)
    return decorated


# Endpoints that don't require a selected case (auth + case management).
_NO_CASE_ENDPOINTS = {
    "login_page", "do_login", "logout", "static",
    "cases_list", "cases_new", "cases_open", "cases_delete",
}


@app.before_request
def _start_timer():
    request.environ["engine.t0"] = time.time()


@app.after_request
def _log_request(response):
    """One line per request: what, outcome, how long, who, which case. No bodies, no query strings."""
    if request.endpoint == "static":
        return response
    t0 = request.environ.get("engine.t0")
    ms = int((time.time() - t0) * 1000) if t0 else -1
    log.info("request method=%s path=%s status=%s ms=%s user=%s case=%s",
             request.method, request.path, response.status_code, ms,
             (session.get("user") or {}).get("id", "-"), session.get("case_id", "-"))
    return response


@app.before_request
def guard():
    endpoint = request.endpoint
    # 1. Public endpoints
    if endpoint in ("login_page", "do_login", "static"):
        return
    # 2. Must be logged in
    if not get_current_user():
        return redirect(url_for("login_page"))
    # 3. Engine routes need a selected, accessible case loaded into the global.
    if endpoint not in _NO_CASE_ENDPOINTS:
        if not load_selected_case():
            return redirect(url_for("cases_list"))


LOGIN_HTML = """
<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Logga in — The Engine</title>
<style>
  body { font-family: system-ui, sans-serif; max-width: 400px; margin: 80px auto; padding: 0 20px; }
  h1 { font-size: 1.3rem; }
  label { display: block; margin-top: 12px; font-weight: 500; }
  input[type=text], input[type=password] {
    width: 100%; padding: 8px; margin-top: 4px; box-sizing: border-box;
    border: 1px solid #ccc; border-radius: 4px; font-size: 1rem;
  }
  button { margin-top: 20px; padding: 10px 24px; font-size: 1rem;
    background: #333; color: #fff; border: none; border-radius: 4px; cursor: pointer; }
  button:hover { background: #555; }
  .error { color: #c33; margin-top: 12px; }
</style>
</head>
<body>
  <h1>The Engine</h1>
  <form method="POST" action="/login">
    <label for="username">Användarnamn</label>
    <input id="username" name="username" type="text" required autofocus
           value="{{ username or '' }}">
    <label for="password">Lösenord</label>
    <input id="password" name="password" type="password" required>
    <button type="submit">Logga in</button>
  </form>
  {% if error %}
    <p class="error">{{ error }}</p>
  {% endif %}
</body>
</html>
"""


@app.route("/login")
def login_page():
    if get_current_user():
        return redirect(url_for("index"))
    return render_template_string(LOGIN_HTML, error=None, username=None)


@app.route("/login", methods=["POST"])
def do_login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    if not username or not password:
        return render_template_string(
            LOGIN_HTML, error="Användarnamn och lösenord krävs", username=username
        )
    try:
        data = auth_client.login(username, password)
    except auth_client.AuthError as exc:
        return render_template_string(LOGIN_HTML, error=str(exc), username=username)

    session["token"] = data["token"]
    session["user"] = data["user"]
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))


# --- Case management (per user) ---

CASES_HTML = """
<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mina cases — The Engine</title>
<style>
  body { font-family: system-ui, sans-serif; max-width: 700px; margin: 40px auto; padding: 0 20px; }
  .topbar { text-align:right; font-size:0.8rem; color:#666; }
  h1 { font-size: 1.3rem; }
  ul { list-style: none; padding: 0; }
  li { border: 1px solid #e0e0e0; border-radius: 6px; padding: 12px; margin-bottom: 8px;
       display: flex; justify-content: space-between; align-items: center; }
  .meta { font-size: 0.8rem; color: #888; }
  a.btn { padding: 6px 14px; background:#333; color:#fff; text-decoration:none; border-radius:4px; }
  a.btn:hover { background:#555; }
  form.new { margin-top: 24px; padding-top: 16px; border-top: 1px solid #eee; }
  input[type=text] { padding:8px; width:70%; border:1px solid #ccc; border-radius:4px; }
  button { padding:8px 16px; background:#2a7; color:#fff; border:none; border-radius:4px; cursor:pointer; }
</style>
</head>
<body>
  <div class="topbar">
    {{ current_user.username }}{% if current_user.role %} ({{ current_user.role }}){% endif %}
    &nbsp;·&nbsp;<a href="/logout">Logga ut</a>
  </div>
  <h1>Mina cases</h1>
  {% if flash %}<p style="color:#2a7;">{{ flash }}</p>{% endif %}
  {% if cases %}
  <ul>
    {% for c in cases %}
    <li>
      <div>
        <strong>{{ c.description }}</strong>
        <div class="meta">
          id {{ c.id }}
          {% if c.owner_id is none %} · <em>legacy/oägt</em>{% endif %}
          {% if is_admin and c.owner_id and c.owner_id != current_user.id %} · annans{% endif %}
          {% if c.updated %} · uppdaterad {{ c.updated[:16] }}{% endif %}
        </div>
      </div>
      <div>
        <a class="btn" href="/cases/open/{{ c.id }}">Öppna</a>
        {% if is_admin %}
        <form method="POST" action="/cases/delete/{{ c.id }}" style="display:inline"
              onsubmit="return confirm('Ta bort detta case?');">
          <button type="submit" style="background:#c33;">Ta bort</button>
        </form>
        {% endif %}
      </div>
    </li>
    {% endfor %}
  </ul>
  {% else %}
  <p>Inga cases än. Skapa ett nytt nedan.</p>
  {% endif %}

  <form class="new" method="POST" action="/cases/new">
    <label>Nytt case</label><br><br>
    <input type="text" name="description" placeholder="Kort beskrivning (valfritt)">
    <button type="submit">Skapa</button>
  </form>
</body>
</html>
"""


@app.route("/cases")
def cases_list():
    user = get_current_user()
    flash = request.args.get("flash", "")
    return render_template_string(
        CASES_HTML,
        cases=list_cases_for(user),
        current_user=user,
        is_admin=(user.get("role") == "admin"),
        flash=flash,
    )


@app.route("/cases/new", methods=["POST"])
def cases_new():
    user = get_current_user()
    description = request.form.get("description", "").strip()
    new_case = CaseFile()
    new_case.owner_id = user.get("id")
    new_case.context["description"] = description
    new_case.save(directory="cases")
    session["case_id"] = new_case.id
    return redirect(url_for("index", flash="Nytt case skapat."))


@app.route("/cases/open/<case_id>")
def cases_open(case_id):
    user = get_current_user()
    path = CASES_DIR / f"{case_id}.json"
    if not path.exists():
        return redirect(url_for("cases_list", flash="Case hittades inte."))
    meta = _read_case_meta(path)
    if not meta or not can_access_case(user, meta):
        return redirect(url_for("cases_list", flash="Du har inte åtkomst till det caset."))
    session["case_id"] = case_id
    return redirect(url_for("index"))


@app.route("/cases/delete/<case_id>", methods=["POST"])
def cases_delete(case_id):
    user = get_current_user()
    if user.get("role") != "admin":
        return redirect(url_for("cases_list", flash="Endast admin kan radera cases."))
    path = CASES_DIR / f"{case_id}.json"
    if path.exists():
        path.unlink()
        if session.get("case_id") == case_id:
            session.pop("case_id", None)
    return redirect(url_for("cases_list", flash="Case raderat."))


# --- HTML Template ---

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ case.context.description or 'Adaptive Navigation Engine' }}</title>
    <style>
        * { box-sizing: border-box; }
        body { font-family: system-ui, -apple-system, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #fafafa; color: #333; line-height: 1.5; }
        h1 { font-size: 1.3em; border-bottom: 2px solid #333; padding-bottom: 8px; }
        h2 { font-size: 1.1em; margin-top: 24px; color: #555; }
        a { color: #2d46d7; text-decoration: none; }
        a:hover { text-decoration: underline; }

        .tree { background: white; border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin: 16px 0; }
        .tree-item { padding: 10px 14px; margin: 4px 0; border-radius: 4px; display: flex; align-items: center; gap: 10px; cursor: pointer; }
        .tree-item:hover { background: #f0f0f0; }
        .tree-item.active { border-left: 3px solid #2d7d46; }
        .tree-item.completed { border-left: 3px solid #2d46d7; opacity: 0.7; }
        .tree-item.abandoned { border-left: 3px solid #999; opacity: 0.5; }
        .tree-missions { font-size: 0.85em; color: #666; }

        .mission-item { padding: 10px 14px; margin: 6px 0; background: #f8f8f8; border-radius: 4px; border-left: 3px solid #ccc; display: flex; align-items: flex-start; gap: 10px; }
        .mission-item.active { border-left-color: #2d7d46; background: #f0f7f0; }
        .mission-item.completed { border-left-color: #2d46d7; }
        .mission-check { font-size: 1.2em; min-width: 20px; }
        .mission-text { flex: 1; }

        .observation { background: #f7f7f0; border-left: 3px solid #d4c94e; padding: 8px 12px; margin: 6px 0; font-style: italic; font-size: 0.9em; }

        .proposal { background: #eef4ff; border: 1px solid #b3d0ff; border-radius: 6px; padding: 16px; margin: 16px 0; }
        .proposal h3 { margin: 0 0 8px 0; color: #1a5276; }
        .observer { background: #fff4e6; border: 1px dashed #e0a44e; border-radius: 6px; padding: 14px 16px; margin: 16px 0; }
        .observer-character { font-weight: bold; color: #b5651d; margin-bottom: 6px; }
        .observer-content { font-size: 1.05em; }
        .observer-meta { font-size: 0.75em; color: #999; margin-top: 8px; font-style: italic; }
        .dod { margin: 8px 0; padding-left: 20px; }
        .dod li { margin: 4px 0; }

        form { margin: 10px 0; }
        textarea { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; font-family: inherit; font-size: 0.95em; resize: vertical; }
        button { padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; font-size: 0.9em; margin: 4px 4px 4px 0; }
        .btn-accept { background: #2d7d46; color: white; }
        .btn-modify { background: #d4a017; color: white; }
        .btn-reject { background: #999; color: white; }
        .btn-explore { background: #2d46d7; color: white; }
        .btn-giveup { background: #c0392b; color: white; }
        .btn-primary { background: #333; color: white; }
        .btn-secondary { background: #666; color: white; }
        .btn-pill { background: white; border: 2px solid #2d46d7; color: #2d46d7; padding: 12px 20px; border-radius: 8px; font-size: 1em; display: block; width: 100%; text-align: left; margin: 8px 0; cursor: pointer; }
        .btn-pill:hover { background: #eef4ff; }
        .btn-small { padding: 4px 10px; font-size: 0.85em; }
        .flash { background: #d4edda; border: 1px solid #c3e6cb; padding: 10px; border-radius: 4px; margin: 10px 0; }
        .meta { font-size: 0.8em; color: #888; }
        .breadcrumb { font-size: 0.85em; color: #666; margin-bottom: 12px; }
        .progress { display: flex; gap: 8px; flex-wrap: wrap; margin: 12px 0; }
        .progress-step { padding: 4px 10px; border-radius: 12px; font-size: 0.75em; font-weight: bold; }
        .progress-step.done { background: #2d7d46; color: white; }
        .progress-step.current { background: #d4a017; color: white; }
        .onboarding { background: white; border: 1px solid #ddd; border-radius: 8px; padding: 30px; margin: 20px 0; text-align: center; }
        .onboarding h2 { color: #333; margin-top: 0; }
        .topbar { padding: 8px 0 12px 0; border-bottom: 1px solid #eee; margin-bottom: 12px; }
        .topbar a { font-size: 0.95em; color: #555; font-weight: bold; }
    </style>
</head>
<body>

{% if current_user %}
<div style="text-align:right; font-size:0.8rem; color:#666; padding:4px 0;">
    {{ current_user.username }}{% if current_user.role %} ({{ current_user.role }}){% endif %}
    &nbsp;·&nbsp;<a href="/cases">Mina cases</a>
    &nbsp;·&nbsp;<a href="/logout">Logga ut</a>
</div>
{% endif %}

{% if view != 'onboarding' and case.goals and not is_root_goal %}
<div class="topbar"><a href="/">&#8962; {{ t('nav_overview') }}</a></div>
{% endif %}

{% if flash_message %}
<div class="flash">{{ flash_message }}</div>
{% endif %}

{% macro spec_lines(spec) %}
{% for key, label in [('goal', t('concepts_spec_goal')), ('done', t('concepts_spec_done')), ('actor', t('concepts_spec_actor')), ('first_step', t('concepts_spec_first'))] %}
{% if spec.get(key) %}<div><strong>{{ label }}:</strong> {{ spec.get(key) }}</div>{% endif %}
{% endfor %}
{% endmacro %}

{% macro working(label) -%}onsubmit="var b = this.querySelector('button[type=submit]'); b.disabled = true; b.textContent = '{{ label }}';"{%- endmacro %}

{% macro ping_banner() %}
<div class="flash" style="background: #e6f4ff; border-color: #b3d0ff;">
    <strong>{{ t('actions_banner') }}</strong>
    <form method="POST" action="/concepts/{{ active_goal.id }}/collect" style="display: inline;" {{ working(t('concepts_working')) }}>
        <button type="submit" class="btn-small btn-primary">{{ t('actions_collect') }}</button>
    </form>
</div>
{% endmacro %}

{% macro product_box(back) %}
<div class="observation" style="font-style: normal;">
    {% if product %}
    <strong>{{ t('product_title') }}</strong>
    <div>{{ t('product_aim') }}: {{ product.end_state }}</div>
    <div>{{ t('product_deliverable') }}: {{ product.deliverable }}</div>
    <div class="meta">{{ product.kind }}{% if product.kind %} &middot; {% endif %}{{ t('product_scale', scale=product.scale) }} &middot;
        {% if product.source == 'owner' %}{{ t('product_yours') }}{% else %}{{ t('product_confidence', c=product.confidence) }}{% endif %}</div>
    {% if product.alternatives and product.source != 'owner' %}
    <div class="meta">{{ t('product_alternatives') }}: {{ product.alternatives|join(' | ') }}</div>
    {% endif %}
    {% if product.question and product.source != 'owner' %}
    <form method="POST" action="/concepts/{{ active_goal.id }}/product" {{ working(t('concepts_working')) }} style="margin-top: 8px;">
        <input type="hidden" name="back" value="{{ back }}">
        <input type="hidden" name="action" value="answer">
        <label><strong>{{ product.question }}</strong></label>
        <input type="text" name="answer" maxlength="1000" placeholder="{{ t('product_answer_placeholder') }}" style="width:100%; padding:8px; margin:6px 0; border:1px solid #ccc; border-radius:4px;">
        <button type="submit" class="btn-small btn-primary">{{ t('product_answer') }}</button>
    </form>
    {% endif %}
    <details style="margin-top: 6px;">
        <summary>{{ t('concepts_edit') }}</summary>
        <p class="meta">{{ t('product_help') }}</p>
        <form method="POST" action="/concepts/{{ active_goal.id }}/product">
            <input type="hidden" name="back" value="{{ back }}">
            <input type="hidden" name="action" value="edit">
            <label>{{ t('product_aim') }}</label>
            <textarea name="end_state" rows="2" maxlength="400">{{ product.end_state }}</textarea>
            <label>{{ t('product_deliverable') }}</label>
            <textarea name="deliverable" rows="2" maxlength="400">{{ product.deliverable }}</textarea><br>
            <button type="submit" class="btn-small btn-primary">{{ t('concepts_save') }}</button>
        </form>
        <form method="POST" action="/concepts/{{ active_goal.id }}/product" {{ working(t('concepts_working')) }} style="margin-top: 6px;">
            <input type="hidden" name="back" value="{{ back }}">
            <input type="hidden" name="action" value="redo">
            <button type="submit" class="btn-small btn-secondary">{{ t('product_redo') }}</button>
        </form>
    </details>
    {% else %}
    <span class="meta">{{ t('product_none') }}</span>
    <form method="POST" action="/concepts/{{ active_goal.id }}/product" {{ working(t('concepts_working')) }} style="display: inline;">
        <input type="hidden" name="back" value="{{ back }}">
        <input type="hidden" name="action" value="redo">
        <button type="submit" class="btn-small btn-primary">{{ t('product_interpret') }}</button>
    </form>
    {% endif %}
</div>
{% endmacro %}

{% macro small_banner() %}
<div class="flash" style="background: #e6f4ff; border-color: #b3d0ff;">
    <strong>{{ t('product_small_hint') }}</strong>
    <form method="POST" action="/concepts/{{ active_goal.id }}/collect" style="display: inline;" {{ working(t('concepts_working')) }}>
        <button type="submit" class="btn-small btn-primary">{{ t('actions_collect') }}</button>
    </form>
</div>
{% endmacro %}

{% macro action_card(v) %}
{% set a = v.a %}
<div class="proposal" style="border-left: 4px solid {% if a.status == 'DISMISSED' %}#999{% elif a.first and a.status == 'PROPOSED' %}#0e7c86{% else %}#2d46d7{% endif %};{% if a.status == 'DISMISSED' %} opacity: 0.75;{% endif %}">
    <h3>{{ a.title }}
        {% if a.first and a.status == 'PROPOSED' %}<span class="progress-step done" style="font-size: 0.6em; vertical-align: middle; background: #0e7c86;">{{ t('actions_first') }}</span>{% endif %}</h3>
    <div class="meta"><strong>{{ t('actions_done_when') }}:</strong> {{ a.done_when or '-' }}</div>
    <div class="meta">
        {% if v.serves %}{{ t('actions_serves', titles=v.serves|join(', ')) }}{% else %}{{ t('actions_serves_all') }}{% endif %}
        {% if v.needs %}&middot; {{ t('actions_needs', titles=v.needs|join(', ')) }}{% endif %}
        {% if a.edited %}&middot; {{ t('concepts_badge_edited') }}{% endif %}
    </div>
    {% if a.status == 'PROPOSED' %}
    <div style="margin-top: 8px;">
        <form method="POST" action="/concepts/action/{{ a.id }}/accept" style="display: inline;">
            <button type="submit" class="btn-small btn-accept">{{ t('actions_accept') }}</button>
        </form>
        <form method="POST" action="/concepts/action/{{ a.id }}/dismiss" style="display: inline;">
            <button type="submit" class="btn-small btn-reject">{{ t('actions_dismiss') }}</button>
        </form>
    </div>
    <details style="margin-top: 6px;">
        <summary>{{ t('concepts_edit') }}</summary>
        <form method="POST" action="/concepts/action/{{ a.id }}/edit">
            <input type="text" name="title" value="{{ a.title }}" maxlength="200" style="width:100%; padding:8px; margin:6px 0; border:1px solid #ccc; border-radius:4px;">
            <label>{{ t('actions_done_when') }}</label>
            <textarea name="done_when" rows="2" maxlength="300">{{ a.done_when }}</textarea><br>
            <button type="submit" class="btn-small btn-primary">{{ t('concepts_save') }}</button>
        </form>
    </details>
    {% elif a.status == 'DISMISSED' %}
    <form method="POST" action="/concepts/action/{{ a.id }}/restore" style="margin-top: 8px;">
        <button type="submit" class="btn-small btn-accept">{{ t('concepts_take_back') }}</button>
    </form>
    {% elif v.mission and v.mission.status == 'ACTIVE' %}
    <form method="POST" action="/concepts/action/{{ a.id }}/done" style="margin-top: 8px;">
        <textarea name="result" rows="2" maxlength="2000" placeholder="{{ t('actions_result_placeholder') }}"></textarea><br>
        <button type="submit" class="btn-small btn-accept">{{ t('actions_mark_done') }}</button>
    </form>
    {% elif v.mission and v.mission.result %}
    <div class="observation">{{ v.mission.result }}</div>
    {% endif %}
</div>
{% endmacro %}

<!-- ==================== ONBOARDING ==================== -->
{% if view == 'onboarding' %}
<div class="onboarding" style="text-align: left;">
    <h1 style="border: none; margin-top: 0;">{{ case.context.description or t('tree_fallback_title') }}</h1>
    <p>{{ t('begin_intro') }}</p>
    <form method="POST" action="/begin" onsubmit="var b = this.querySelectorAll('button[type=submit]'); for (var i = 0; i &lt; b.length; i++) { b[i].disabled = true; } document.getElementById('begin-wait').style.display = 'block';">
        <p style="margin-bottom: 4px;"><strong>{{ t('begin_now_label') }}</strong> <span class="meta">{{ t('begin_now_tag') }}</span></p>
        <textarea name="identity_text" rows="8" placeholder="{{ t('begin_now_placeholder') }}" style="font-size: 1.05em;">{{ identity_text }}</textarea>
        <p style="margin-bottom: 4px; margin-top: 18px;"><strong>{{ t('begin_wish_label') }}</strong> <span class="meta">{{ t('begin_wish_tag') }}</span></p>
        <textarea name="ideal_text" rows="8" placeholder="{{ t('begin_wish_placeholder') }}" style="font-size: 1.05em;">{{ ideal_text }}</textarea>
        <p class="meta">{{ t('begin_privacy') }}</p>
        <button type="submit" name="action" value="generate" class="btn-primary" style="font-size: 1.1em; padding: 12px 24px;">{{ t('begin_go') }}</button>
        <button type="submit" name="action" value="deep" class="btn-secondary">{{ t('begin_deep') }}</button>
        <p class="meta">{{ t('begin_deep_help') }}</p>
        <p id="begin-wait" class="meta" style="display: none;">{{ t('begin_wait') }}</p>
    </form>
</div>

<!-- ==================== DIRECTION CHOICE ==================== -->
{% elif view == 'directions' %}
<h1>{{ case.context.description or t('directions_fallback_title') }}</h1>
<h2>{{ t('directions_title') }}</h2>
<p>{{ t('directions_intro') }}</p>
{% for d in directions %}
<form method="POST" action="/choose_direction">
    <input type="hidden" name="title" value="{{ d.title }}">
    <input type="hidden" name="description" value="{{ d.description }}">
    <button type="submit" class="btn-pill">
        <strong>{{ d.title }}</strong><br>
        <span style="font-size: 0.85em; color: #555;">{{ d.description }}</span>
    </button>
</form>
{% endfor %}

<!-- ==================== NAME YOUR CASE ==================== -->
{% elif view == 'name_case' %}
<div class="onboarding">
    <h2>{{ t('name_title') }}</h2>
    <p class="meta">{{ t('name_help') }}</p>
    <form method="POST" action="/confirm_name">
        <input type="hidden" name="direction" value="{{ direction }}">
        {% for name in name_options %}
        <label style="display:block; text-align:left; margin:8px 0; cursor:pointer;">
            <input type="radio" name="case_name_choice" value="{{ name }}" {% if loop.first %}checked{% endif %}>
            <strong>{{ name }}</strong>
        </label>
        {% endfor %}
        <p class="meta" style="margin-top:16px;">{{ t('name_own') }}</p>
        <input type="text" name="case_name_custom" placeholder="{{ t('name_own_placeholder') }}"
               style="width: 100%; padding: 10px; font-size: 1.05em; border: 1px solid #ccc; border-radius: 4px;">
        <br><br>
        <button type="submit" class="btn-primary" style="font-size: 1.1em; padding: 12px 24px;">{{ t('name_go') }}</button>
    </form>
</div>

<!-- ==================== TREE VIEW (default) ==================== -->
{% elif view == 'tree' %}
<h1>{{ case.context.description or t('tree_fallback_title') }}</h1>

{% set n_goals = case.goals|length %}
{% set n_missions_done = case.missions|selectattr('status', 'equalto', 'COMPLETED')|list|length %}
{% set n_observations = case.observations|length %}
<div class="progress">
    <span class="progress-step done">{{ t('progress_goals', n=n_goals) }}</span>
    {% if n_missions_done > 0 %}<span class="progress-step done">{{ t('progress_missions_done', n=n_missions_done) }}</span>{% endif %}
    {% if n_observations > 0 %}<span class="progress-step done">{{ t('progress_observations', n=n_observations) }}</span>{% endif %}
</div>

<div class="tree">
{% for goal in case.goals %}
    {% set gm = case.missions|selectattr('goal_id', 'equalto', goal.id)|list %}
    {% set gm_done = gm|selectattr('status', 'equalto', 'COMPLETED')|list %}
    {% set gm_active = gm|selectattr('status', 'equalto', 'ACTIVE')|list %}
    <a href="/goal/{{ goal.id }}" style="text-decoration: none; color: inherit;">
    <div class="tree-item {{ goal.status|lower }}">
        <span style="font-size:1.2em;">{% if goal.status == 'ACTIVE' %}&#9679;{% elif goal.status == 'COMPLETED' %}&#10003;{% else %}&#10007;{% endif %}</span>
        <div style="flex:1;">
            <strong>{{ goal.desired_direction[:70] }}{% if goal.desired_direction|length > 70 %}...{% endif %}</strong>
            {% if gm %}
            <div class="tree-missions">{{ t('tree_missions_count', done=gm_done|length, total=gm|length) }}{% if gm_active %} &middot; {{ t('tree_active_suffix', n=gm_active|length) }}{% endif %}</div>
            {% else %}
            <div class="tree-missions">{{ t('tree_no_missions') }}</div>
            {% endif %}
        </div>
    </div>
    </a>
{% endfor %}
</div>

{% set active_goals = case.goals|selectattr('status', 'equalto', 'ACTIVE')|list %}
{% if case.goals and not active_goals %}
<div class="onboarding">
    <h2>{{ t('all_done_title') }}</h2>
    <p class="meta">{{ t('all_done_help') }}</p>
    <form method="POST" action="/new_goals" style="display:inline;">
        <button type="submit" class="btn-primary">{{ t('all_done_new') }}</button>
    </form>
</div>
{% endif %}

<h2>{{ t('add_goal_title') }}</h2>
<form method="POST" action="/add_goal">
    <textarea name="direction" rows="2" placeholder="{{ t('add_goal_placeholder') }}"></textarea><br>
    <button type="submit" class="btn-secondary">{{ t('add_goal_button') }}</button>
</form>

<!-- ==================== GOAL DETAIL VIEW ==================== -->
{% elif view == 'goal' %}
<div class="breadcrumb"><a href="/">&larr; {{ t('back_all_goals') }}</a></div>
<h1>{{ active_goal.desired_direction }}</h1>
<span class="meta">{{ t('status_label') }}: {{ active_goal.status }}</span>

{% set goal_missions_all = case.missions|selectattr('goal_id', 'equalto', active_goal.id)|list %}
{% set goal_missions_done = goal_missions_all|selectattr('status', 'equalto', 'COMPLETED')|list %}
{% set goal_missions_active = goal_missions_all|selectattr('status', 'equalto', 'ACTIVE')|list %}

<div class="progress">
    <span class="progress-step done">{{ t('progress_goal_set') }}</span>
    {% if goal_missions_all|length > 0 %}<span class="progress-step done">{{ t('progress_missions', done=goal_missions_done|length, total=goal_missions_all|length) }}</span>{% endif %}
    {% if goal_missions_active %}<span class="progress-step current">{{ t('progress_active_mission') }}</span>{% endif %}
</div>

{% if goal_missions_all %}
<h2>{{ t('missions_title') }}</h2>
{% for m in goal_missions_all %}
<div class="mission-item {{ m.status|lower }}">
    <span class="mission-check">{% if m.status == 'COMPLETED' %}&#9745;{% else %}&#9744;{% endif %}</span>
    <div class="mission-text">
        <strong>{{ m.name or m.id }}</strong><br>
        <span style="font-size:0.9em;">{{ m.description[:140] }}{% if m.description|length > 140 %}...{% endif %}</span>
        {% if m.status == 'ACTIVE' %}
        <form method="POST" action="/complete_mission/{{ m.id }}" style="margin-top: 8px;">
            <textarea name="observation" rows="2" placeholder="{{ t('mission_result_placeholder') }}"></textarea><br>
            <button type="submit" class="btn-small btn-accept">{{ t('mark_done') }}</button>
        </form>
        {% endif %}
        {% if m.result %}<br><span class="meta">{{ m.result[:80] }}</span>{% endif %}
    </div>
</div>
{% endfor %}
{% endif %}

{% set goal_obs = case.observations|selectattr('mission_id', 'in', goal_missions_all|map(attribute='id')|list)|list %}
{% if goal_obs %}
<h2>{{ t('observations_title') }}</h2>
{% for o in goal_obs %}
<div class="observation">{{ o.text }}</div>
{% endfor %}
{% endif %}

<form method="POST" action="/propose/{{ active_goal.id }}" style="margin-top: 20px;">
    <button type="submit" class="btn-primary">{{ t('get_suggestions') }}</button>
</form>

<p style="margin-top: 10px;"><a href="/concepts/{{ active_goal.id }}"><button type="button" class="btn-explore">{{ t('concepts_open') }}</button></a></p>

<form method="POST" action="/complete_goal/{{ active_goal.id }}" style="margin-top: 10px; display: inline;">
    <button type="submit" class="btn-small btn-accept">{{ t('mark_goal_done') }}</button>
</form>
<form method="POST" action="/abandon_goal/{{ active_goal.id }}" style="margin-top: 10px; display: inline;">
    <button type="submit" class="btn-small btn-giveup">{{ t('give_up') }}</button>
</form>

<!-- ==================== CONCEPTS (concept tree) ==================== -->
{% elif view == 'concepts' %}
{% macro working(label) -%}onsubmit="var b = this.querySelector('button[type=submit]'); b.disabled = true; b.textContent = '{{ label }}';"{%- endmacro %}
{% macro node_card(n, goal_id, child_count) %}
{% set spec_n = [n.spec.get('goal'), n.spec.get('done'), n.spec.get('actor'), n.spec.get('first_step')]|select|list|length %}
<div class="proposal" style="border-left: 4px solid {% if n.spiked %}#0e7c86{% elif n.status == 'ACTIVE' %}#2d7d46{% elif n.status == 'CANDIDATE' %}#2d46d7{% else %}#999{% endif %};{% if n.status == 'PARKED' %} opacity: 0.75;{% endif %}">
    <h3>{{ n.title }}
        {% if n.spiked %}<span class="progress-step done" style="font-size: 0.6em; vertical-align: middle; background: #0e7c86;">{{ t('concepts_nailed_badge') }}</span>
        {% elif n.status == 'ACTIVE' %}<span class="progress-step done" style="font-size: 0.6em; vertical-align: middle;">{{ t('concepts_kept_badge') }}</span>{% endif %}</h3>
    <div class="meta">
        {% if n.source == 'owner' %}{{ t('concepts_badge_owner') }} &middot; {% endif %}
        {% if n.edited %}{{ t('concepts_badge_edited') }} &middot; {% endif %}
        {% if n.theme %}{{ t('concepts_theme', name=n.theme) }} &middot; {% endif %}
        {% if n.variant_of %}{{ t('concepts_variant_of', title=concept_titles.get(n.variant_of, '?')) }} &middot; {% endif %}
        {% if n.lens and not n.seen_in %}{{ t('concepts_via_lens', lens=(n.lens|lens_name)) }} &middot; {% endif %}
        {% if n.stability == 'stable' %}<strong>{{ t('concepts_badge_stable') }}</strong> &middot; {% elif n.stability == 'variant' %}{{ t('concepts_badge_variant') }} &middot; {% endif %}
        {% if n.seen_in %}{{ t('concepts_seen_in', lenses=(n.seen_in|map('lens_name')|join(', '))) }}{% endif %}
    </div>
    <p style="white-space: pre-wrap;">{{ n.text }}</p>
    {% if spec_n %}
    <div class="observation" style="font-style: normal;">{{ spec_lines(n.spec) }}</div>
    {% endif %}

    {% if n.draft_text %}
    <div class="observer" style="margin: 10px 0;">
        <div class="observer-character">{{ t('concepts_draft_title') }}</div>
        <p style="white-space: pre-wrap;">{{ n.draft_text }}</p>
        {% if n.draft_spec.values()|select|list %}<div class="observation" style="font-style: normal;">{{ spec_lines(n.draft_spec) }}</div>{% endif %}
        {% if n.draft_missing %}<p class="meta">{{ t('concepts_draft_missing') }}: {{ n.draft_missing }}</p>{% endif %}
        <form method="POST" action="/concepts/node/{{ n.id }}/draft" style="display:inline;">
            <button type="submit" name="action" value="use" class="btn-small btn-accept">{{ t('concepts_draft_use') }}</button>
            <button type="submit" name="action" value="drop" class="btn-small btn-reject">{{ t('concepts_draft_drop') }}</button>
        </form>
    </div>
    {% endif %}

    <div style="margin-top: 8px;">
        {% if n.status == 'PARKED' %}
        <form method="POST" action="/concepts/node/{{ n.id }}/status" style="display:inline;">
            <input type="hidden" name="status" value="ACTIVE">
            <button type="submit" class="btn-small btn-accept">{{ t('concepts_take_back') }}</button>
        </form>
        {% else %}
        {% if not n.spiked %}
        <form method="POST" action="/concepts/node/{{ n.id }}/status" style="display:inline;">
            <input type="hidden" name="status" value="{{ 'CANDIDATE' if n.status == 'ACTIVE' else 'ACTIVE' }}">
            <button type="submit" class="btn-small {{ 'btn-secondary' if n.status == 'ACTIVE' else 'btn-accept' }}">{{ t('concepts_release') if n.status == 'ACTIVE' else t('concepts_keep') }}</button>
        </form>
        {% endif %}
        {% if child_count %}
        <a href="/concepts/{{ goal_id }}?parent={{ n.id }}"><button type="button" class="btn-small btn-explore">{{ t('concepts_open_n', n=child_count) }}</button></a>
        {% elif not n.spiked %}
        <form method="POST" action="/concepts/{{ goal_id }}/generate" style="display:inline;" {{ working(t('concepts_working')) }}>
            <input type="hidden" name="parent_id" value="{{ n.id }}">
            <input type="hidden" name="mode" value="split">
            <button type="submit" class="btn-small btn-explore">{{ t('concepts_split_this') }}</button>
        </form>
        {% endif %}
        <form method="POST" action="/concepts/node/{{ n.id }}/status" style="display:inline;">
            <input type="hidden" name="status" value="PARKED">
            <button type="submit" class="btn-small btn-reject">{{ t('concepts_set_aside') }}</button>
        </form>
        {% endif %}
    </div>

    <div style="display: flex; flex-wrap: wrap; gap: 18px; margin-top: 8px;">
        <details>
            <summary>{{ t('concepts_edit') }}</summary>
            <form method="POST" action="/concepts/node/{{ n.id }}/edit">
                <input type="text" name="title" value="{{ n.title }}" style="width:100%; padding:8px; margin:6px 0; border:1px solid #ccc; border-radius:4px;">
                <textarea name="text" rows="10" style="min-width: 320px;">{{ n.text }}</textarea><br>
                <button type="submit" class="btn-small btn-primary">{{ t('concepts_save') }}</button>
            </form>
        </details>
        {% if n.status != 'PARKED' %}
        {% if not n.spiked %}
        <details>
            <summary>{{ t('concepts_vary') }}</summary>
            <form method="POST" action="/concepts/node/{{ n.id }}/vary" {{ working(t('concepts_working')) }}>
                <input type="text" name="angle" maxlength="300" placeholder="{{ t('concepts_angle_placeholder') }}" style="width:100%; min-width: 280px; padding:8px; margin:6px 0; border:1px solid #ccc; border-radius:4px;">
                <button type="submit" class="btn-small btn-explore">{{ t('concepts_vary_go') }}</button>
                <div class="meta">{{ t('concepts_vary_help') }}</div>
            </form>
        </details>
        {% endif %}
        <details>
            <summary>{{ t('concepts_strengthen') }}</summary>
            <form method="POST" action="/concepts/node/{{ n.id }}/strengthen" {{ working(t('concepts_working')) }}>
                <input type="text" name="direction" maxlength="300" placeholder="{{ t('concepts_strengthen_placeholder') }}" style="width:100%; min-width: 280px; padding:8px; margin:6px 0; border:1px solid #ccc; border-radius:4px;">
                <button type="submit" class="btn-small btn-explore">{{ t('concepts_strengthen_go') }}</button>
                <div class="meta">{{ t('concepts_strengthen_help') }}</div>
            </form>
        </details>
        <details {% if n.spiked %}open{% endif %}>
            <summary>{{ t('concepts_spec_title', n=spec_n) }}</summary>
            <form method="POST" action="/concepts/node/{{ n.id }}/spec">
                <div class="meta">{{ t('concepts_spec_help') }}</div>
                <label>{{ t('concepts_spec_goal') }}</label>
                <textarea name="goal" rows="2">{{ n.spec.get('goal', '') }}</textarea>
                <label>{{ t('concepts_spec_done') }}</label>
                <textarea name="done" rows="2">{{ n.spec.get('done', '') }}</textarea>
                <label>{{ t('concepts_spec_actor') }}</label>
                <textarea name="actor" rows="2">{{ n.spec.get('actor', '') }}</textarea>
                <label>{{ t('concepts_spec_first') }}</label>
                <textarea name="first_step" rows="2">{{ n.spec.get('first_step', '') }}</textarea><br>
                <button type="submit" name="action" value="save" class="btn-small btn-primary">{{ t('concepts_save') }}</button>
                {% if n.spiked %}
                <button type="submit" name="action" value="unnail" class="btn-small btn-reject">{{ t('concepts_spec_unnail') }}</button>
                {% else %}
                <button type="submit" name="action" value="nail" class="btn-small btn-accept">{{ t('concepts_spec_nail') }}</button>
                {% endif %}
            </form>
        </details>
        {% endif %}
    </div>
</div>
{% endmacro %}

<div class="breadcrumb">
    {% if is_root_goal %}
    <a href="/concepts/{{ active_goal.id }}">&larr; {{ case.context.description or t('concepts_title') }}</a>
    {% else %}
    <a href="/goal/{{ active_goal.id }}">&larr; {{ active_goal.desired_direction[:60] }}{% if active_goal.desired_direction|length > 60 %}...{% endif %}</a>
    {% endif %}
    {% for p in concept_path %}
    &rsaquo; <a href="/concepts/{{ active_goal.id }}?parent={{ p.id }}">{{ p.title }}</a>
    {% endfor %}
</div>

<h1>{{ concept_parent.title if concept_parent else (case.context.description if is_root_goal and case.context.description else t('concepts_title')) }}</h1>
<p class="meta">{{ t('concepts_assumption_note') }} &middot; <a href="/concepts/{{ active_goal.id }}/tree">{{ t('concepts_tree_link') }}</a></p>
{% if ready_ping %}{{ ping_banner() }}{% endif %}
{% if small_hint and not ready_ping and not concept_parent %}{{ small_banner() }}{% endif %}

{% if concept_parent %}
<div class="observation" style="font-style: normal; white-space: pre-wrap;">{{ concept_parent.text }}</div>
{% else %}
{% if not is_root_goal %}
<div class="observation" style="font-style: normal;"><strong>{{ t('concepts_start') }}:</strong> {{ active_goal.desired_direction }}</div>
{% endif %}

{{ product_box('concepts') }}

<details {% if not identity_text and not ideal_text %}open{% endif %}>
    <summary><strong>{{ t('concepts_context_title') }}</strong></summary>
    <p class="meta">{{ t('concepts_context_help') }}</p>
    <form method="POST" action="/concepts/{{ active_goal.id }}/context">
        <label>{{ t('concepts_identity_label') }}</label>
        <textarea name="identity_text" rows="6">{{ identity_text }}</textarea>
        <label>{{ t('concepts_ideal_label') }}</label>
        <textarea name="ideal_text" rows="6">{{ ideal_text }}</textarea><br>
        <button type="submit" class="btn-primary">{{ t('concepts_save') }}</button>
    </form>
</details>
{% endif %}

<h2>{{ t('concepts_slots') }}</h2>
{% for n in concepts_slots %}{{ node_card(n, active_goal.id, child_counts.get(n.id, 0)) }}{% else %}
<p class="meta">{{ t('concepts_empty') }}</p>
{% endfor %}

{% if concepts_slots %}
<form method="POST" action="/concepts/{{ active_goal.id }}/reroll" {{ working(t('concepts_working')) }}>
    <input type="hidden" name="parent_id" value="{{ concept_parent.id if concept_parent else '' }}">
    <button type="submit" class="btn-primary">{{ t('concepts_reroll') }}</button>
    <p class="meta">{{ t('concepts_reroll_help') }}</p>
</form>
{% if themes_open > themes_target %}
<form method="POST" action="/concepts/{{ active_goal.id }}/themes" {{ working(t('concepts_working')) }}>
    <input type="hidden" name="parent_id" value="{{ concept_parent.id if concept_parent else '' }}">
    <button type="submit" class="btn-secondary">{{ t('concepts_themes_go', n=themes_target) }}</button>
    <p class="meta">{{ t('concepts_themes_help', open=themes_open, n=themes_target) }}</p>
</form>
{% endif %}
{% else %}
<form method="POST" action="/concepts/{{ active_goal.id }}/generate" {{ working(t('concepts_working')) }}>
    <input type="hidden" name="parent_id" value="{{ concept_parent.id if concept_parent else '' }}">
    <input type="hidden" name="mode" value="{{ 'split' if concept_parent else 'vary' }}">
    <button type="submit" class="btn-primary">{{ t('concepts_generate_split') if concept_parent else t('concepts_first_vary') }}</button>
</form>
{% endif %}

<h2>{{ t('concepts_deep_title') }}</h2>
<form method="POST" action="/concepts/{{ active_goal.id }}/deep" {{ working(t('concepts_deep_running')) }}>
    <input type="hidden" name="parent_id" value="{{ concept_parent.id if concept_parent else '' }}">
    <input type="hidden" name="mode" value="vary">
    <p class="meta">{{ t('concepts_deep_help', max=max_lenses) }}</p>
    <input type="text" name="angle" maxlength="300" placeholder="{{ t('concepts_angle_placeholder') }}" style="width:100%; padding:8px; margin:6px 0; border:1px solid #ccc; border-radius:4px;">
    <details>
        <summary>{{ t('concepts_lenses_summary') }}</summary>
        {% for lid, lens in lenses.items() %}
        <label style="display:block;">
            <input type="checkbox" name="lens" value="{{ lid }}" {% if lid in default_lenses %}checked{% endif %}>
            <strong>{{ lens.name }}</strong> <span class="meta">{{ lens.instruction }}</span>
        </label>
        {% endfor %}
    </details>
    <button type="submit" class="btn-explore" style="margin-top: 8px;">{{ t('concepts_deep_go') }}</button>
</form>

<h2>{{ t('concepts_add_title') }}</h2>
<form method="POST" action="/concepts/{{ active_goal.id }}/add">
    <input type="hidden" name="parent_id" value="{{ concept_parent.id if concept_parent else '' }}">
    <input type="text" name="title" placeholder="{{ t('concepts_add_name') }}" required style="width:100%; padding:8px; margin:6px 0; border:1px solid #ccc; border-radius:4px;">
    <textarea name="text" rows="4" placeholder="{{ t('concepts_add_text') }}"></textarea><br>
    <button type="submit" class="btn-secondary">{{ t('concepts_add_button') }}</button>
</form>

{% if concepts_parked %}
<details style="margin-top: 20px;">
    <summary><strong>{{ t('concepts_parked', n=concepts_parked|length) }}</strong></summary>
    {% for n in concepts_parked %}{{ node_card(n, active_goal.id, child_counts.get(n.id, 0)) }}{% endfor %}
</details>
{% endif %}

<!-- ==================== TREE OVERVIEW ==================== -->
{% elif view == 'concepts_tree' %}
<div class="breadcrumb"><a href="/concepts/{{ active_goal.id }}">&larr; {{ case.context.description or t('concepts_title') }}</a></div>
<h1>{{ t('concepts_tree_title') }}</h1>
<p class="meta">{{ t('concepts_tree_summary', total=tree_rows|length, kept=tree_kept, nailed=tree_nailed, depth=tree_depth) }}{% if tree_parked %} &middot; {{ t('concepts_tree_parked', n=tree_parked) }}{% endif %}</p>
{% if ready_ping %}{{ ping_banner() }}{% endif %}
{% if small_hint and not ready_ping %}{{ small_banner() }}{% endif %}
{{ product_box('tree') }}

<h2>{{ t('actions_title') }}</h2>
<form method="POST" action="/concepts/{{ active_goal.id }}/collect" {{ working(t('concepts_working')) }}>
    <button type="submit" class="btn-primary">{{ t('actions_collect') }}</button>
    <p class="meta">{{ t('actions_collect_help') }}</p>
</form>

{% if actions.doing %}
<h3>{{ t('actions_doing') }}</h3>
{% for v in actions.doing %}{{ action_card(v) }}{% endfor %}
{% endif %}

{% if actions.proposed %}
{% set base_list = actions.proposed|selectattr('a.layer', 'equalto', 'base')|list %}
{% set point_list = actions.proposed|selectattr('a.layer', 'equalto', 'points')|list %}
{% if base_list %}
<h3>{{ t('actions_layer_base') }}</h3>
{% for v in base_list %}{{ action_card(v) }}{% endfor %}
{% endif %}
{% if point_list %}
<h3>{{ t('actions_layer_points') }}</h3>
{% for v in point_list %}{{ action_card(v) }}{% endfor %}
{% endif %}
{% elif not actions.any %}
<p class="meta">{{ t('actions_none') }}</p>
{% endif %}

{% if actions.uncovered %}
<div class="observation" style="font-style: normal;">
    <strong>{{ t('actions_uncovered') }}</strong>
    {% for c in actions.uncovered %}<a href="/concepts/{{ active_goal.id }}?parent={{ c.id }}">{{ c.title }}</a>{% if not loop.last %}, {% endif %}{% endfor %}
</div>
{% endif %}

{% if actions.assumptions %}
<details><summary>{{ t('actions_assumptions') }}</summary>
<ul>{% for x in actions.assumptions %}<li>{{ x }}</li>{% endfor %}</ul>
</details>
{% endif %}
{% if actions.done %}
<details><summary>{{ t('actions_done_list', n=actions.done|length) }}</summary>
{% for v in actions.done %}{{ action_card(v) }}{% endfor %}
</details>
{% endif %}
{% if actions.dismissed %}
<details><summary>{{ t('actions_dismissed', n=actions.dismissed|length) }}</summary>
{% for v in actions.dismissed %}{{ action_card(v) }}{% endfor %}
</details>
{% endif %}

<h2>{{ t('actions_tree_heading') }}</h2>
{% for r in tree_rows %}
<div class="tree-item {% if r.node.spiked %}active{% endif %}" style="margin-left: {{ r.depth * 28 }}px; display: block; cursor: default;">
    <a href="/concepts/{{ active_goal.id }}?parent={{ r.node.id }}"><strong>{{ r.node.title }}</strong></a>
    <span class="meta">
        &middot; {% if r.node.spiked %}<strong>{{ t('concepts_nailed_badge') }}</strong>{% elif r.node.status == 'ACTIVE' %}{{ t('concepts_kept_badge') }}{% else %}{{ t('concepts_tree_open_badge') }}{% endif %}
        &middot; {{ r.spec_n }}/4{% if r.children %} &middot; {{ t('concepts_open_n', n=r.children) }}{% endif %}
    </span>
    {% if r.node.spiked %}<div class="meta" style="margin-top: 4px;">{{ spec_lines(r.node.spec) }}</div>{% endif %}
</div>
{% else %}
<p class="meta">{{ t('concepts_empty') }}</p>
{% endfor %}
{% endif %}

<!-- ==================== PROPOSAL (any view) ==================== -->
{% if observer_event %}
<div class="observer">
    <div class="observer-character">{{ t('observer_says', name=observer_event.character_name) }}</div>
    <div class="observer-content">{{ observer_event.content }}</div>
    <div class="observer-meta">{{ t('observer_meta') }}</div>
</div>
{% endif %}

{% if proposal %}
<h2>{{ t('proposal_title') }}</h2>
<div class="proposal">
    <h3>{{ proposal.mission_name or t('proposal_fallback') }}</h3>
    <p><strong>{{ t('proposal_suggestion') }}:</strong> {{ proposal.suggestion }}</p>
    <p><strong>{{ t('proposal_reason') }}:</strong> {{ proposal.reason }}</p>
    <p><strong>{{ t('proposal_mission') }}:</strong> {{ proposal.mission_description }}</p>
    {% if proposal.definition_of_done %}
    <strong>{{ t('proposal_done_when') }}</strong>
    <ul class="dod">
        {% for d in proposal.definition_of_done %}
        <li>{{ d }}</li>
        {% endfor %}
    </ul>
    {% endif %}
    <form method="POST" action="/decide" style="margin-top: 12px;">
        <input type="hidden" name="goal_id" value="{{ proposal.goal_id }}">
        <button type="submit" name="decision" value="ACCEPT" class="btn-accept">{{ t('accept') }}</button>
        <button type="submit" name="decision" value="REJECT" class="btn-reject">{{ t('reject') }}</button>
        <button type="submit" name="decision" value="EXPLORE_FURTHER" class="btn-explore">{{ t('explore_further') }}</button>
        <button type="submit" name="decision" value="GIVE_UP" class="btn-giveup">{{ t('give_up') }}</button>
        <br><br>
        <textarea name="modification" rows="2" placeholder="{{ t('modify_placeholder') }}"></textarea><br>
        <button type="submit" name="decision" value="MODIFY" class="btn-modify">{{ t('modify_accept') }}</button>
    </form>
</div>
{% endif %}

<!-- ==================== SUGGESTIONS (any view) ==================== -->
{% if suggestions %}
<h2>{{ t('choose_next') }}</h2>
<p class="meta">{{ t('possible_directions', n=suggestions|length) }}</p>
{% for s in suggestions %}
<div class="proposal" style="border-left: 4px solid #2d46d7;">
    <h3>{{ s.title }}</h3>
    <p>{{ s.description }}</p>
    <form method="POST" action="/select" style="margin-top: 8px;">
        <input type="hidden" name="goal_id" value="{{ suggestion_goal_id }}">
        <input type="hidden" name="selection_id" value="{{ s.id }}">
        <input type="hidden" name="selection_title" value="{{ s.title }}">
        <input type="hidden" name="selection_description" value="{{ s.description }}">
        <button type="submit" class="btn-accept">{{ t('choose_this') }}</button>
    </form>
</div>
{% endfor %}
{% endif %}

</body>
</html>
"""


# --- Template helper ---

def render(view="tree", **kwargs):
    defaults = {
        "case": case,
        "current_user": get_current_user(),
        "view": view,
        "proposal": None,
        "suggestions": None,
        "suggestion_goal_id": None,
        "directions": None,
        "active_goal": None,
        "name_options": [],
        "direction": "",
        "observer_event": None,
        "flash_message": "",
        # concept view
        "concept_parent": None,
        "concept_path": [],
        "concepts_slots": [],
        "concepts_parked": [],
        "child_counts": {},
        "ready_ping": False,
        "product": None,
        "small_hint": False,
        "actions": {"proposed": [], "doing": [], "done": [], "dismissed": [], "uncovered": [],
                    "any": False, "assumptions": []},
        "themes_target": 4,
        "themes_open": 0,
        "concept_titles": {},
        "tree_rows": [],
        "tree_parked": 0,
        "tree_kept": 0,
        "tree_nailed": 0,
        "tree_depth": 0,
        "identity_text": "",
        "ideal_text": "",
        "is_root_goal": False,
        "lenses": LENSES,
        "default_lenses": DEFAULT_DEEP_LENSES,
        "max_lenses": MAX_LENSES,
    }
    defaults.update(kwargs)
    return render_template_string(HTML, **defaults)


# --- Routes ---

@app.route("/")
def index():
    flash = request.args.get("flash", "")
    root_id = _root_goal_id()
    if root_id:
        # Cases started from the "describe the situation" page live in the concept view.
        return _concept_redirect(root_id, None, flash)
    if not case.goals:
        return render("onboarding", flash_message=flash)
    return render("tree", flash_message=flash)


@app.route("/goal/<goal_id>")
def goal_view(goal_id):
    goal = case.get_goal(goal_id)
    if not goal:
        return redirect(url_for("index", flash=t("flash_goal_not_found")))
    # Check for a saved pending proposal
    pending = case.pending_proposals.get(goal_id)
    proposal = None
    if pending:
        from engine import Proposal
        proposal = Proposal(**pending)
    # Show the most recent observer event for this goal that has no reaction yet
    observer_event = None
    for e in reversed(case.observer_events):
        if e.goal_id == goal_id and not e.participant_reaction:
            observer_event = e
            break
    flash = request.args.get("flash", "")
    return render("goal", active_goal=goal, proposal=proposal,
                  observer_event=observer_event, flash_message=flash)


@app.route("/start", methods=["POST"])
def start():
    user_input = request.form.get("input", "").strip()
    if not user_input:
        return redirect(url_for("index", flash=t("flash_describe")))

    interpretation = engine.interpret_input(case, user_input)
    case.update_situation(interpretation.current_situation)
    case.context["description"] = user_input[:80]

    # Generate directions — ALL of these will become goals.
    temp_goal = Goal(desired_direction=interpretation.possible_direction)
    directions = engine.suggest(case, temp_goal)

    # Stash directions so /confirm_name can turn them all into goals.
    case.context["pending_directions"] = [
        f"{d.get('title','')}: {d.get('description','')}" if d.get('description') else d.get('title', '')
        for d in directions
    ]
    save_case()

    # Go straight to naming the case (the vision), then create the goals.
    name_options = engine.generate_case_name(user_input, interpretation.possible_direction)
    return render("name_case", name_options=name_options,
                  direction="", flash_message="")


@app.route("/choose_direction", methods=["POST"])
def choose_direction():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    direction = f"{title}: {description}" if description else title

    # Generate creative case name suggestions
    user_input = case.context.get("description", "")
    name_options = engine.generate_case_name(user_input, direction)

    # Show name choice page
    return render("name_case",
                  name_options=name_options,
                  direction=direction,
                  flash_message="")


@app.route("/confirm_name", methods=["POST"])
def confirm_name():
    custom = request.form.get("case_name_custom", "").strip()
    choice = request.form.get("case_name_choice", "").strip()
    name = custom or choice

    if name:
        case.context["description"] = name

    # Turn all pending directions into goals.
    pending = case.context.pop("pending_directions", [])
    for direction in pending:
        if direction.strip():
            case.add_goal(desired_direction=direction)
    save_case()
    return redirect(url_for("index", flash=t("flash_welcome", name=name or "")))


@app.route("/propose/<goal_id>", methods=["POST"])
def propose(goal_id):
    goal = case.get_goal(goal_id)
    if not goal:
        return redirect(url_for("index", flash=t("flash_goal_not_found")))
    suggestions = engine.suggest(case, goal)
    return render("goal", active_goal=goal, suggestions=suggestions,
                  suggestion_goal_id=goal_id,
                  flash_message=t("flash_choose_direction"))


@app.route("/select", methods=["POST"])
def select():
    goal_id = request.form.get("goal_id", "")
    selection = {
        "id": request.form.get("selection_id", ""),
        "title": request.form.get("selection_title", ""),
        "description": request.form.get("selection_description", ""),
    }
    goal = case.get_goal(goal_id)
    if not goal:
        return redirect(url_for("index", flash=t("flash_goal_not_found")))
    proposal = engine.propose_for_selection(case, goal, selection)
    # Save proposal so it survives navigation
    case.pending_proposals[goal_id] = {
        "goal_id": proposal.goal_id,
        "current": proposal.current,
        "desired": proposal.desired,
        "suggestion": proposal.suggestion,
        "reason": proposal.reason,
        "mission_name": proposal.mission_name,
        "mission_description": proposal.mission_description,
        "mission_purpose": proposal.mission_purpose,
        "definition_of_done": proposal.definition_of_done,
    }

    # Observer may notice something and offer a perspective.
    # It never changes Case File state — only records an event.
    observer_event = observer.observe(case, goal, proposal)
    event_record = None
    if observer_event:
        event_record = case.record_observer_event(
            goal_id=goal_id,
            character=observer_event.character,
            character_name=observer_event.character_name,
            event_type=observer_event.type,
            reason=observer_event.reason,
            content=observer_event.content,
        )

    save_case()
    return render("goal", active_goal=goal, proposal=proposal,
                  observer_event=event_record,
                  flash_message=t("flash_proposal_for", title=selection['title']))


@app.route("/decide", methods=["POST"])
def decide():
    goal_id = request.form.get("goal_id", "")
    decision = request.form.get("decision", "")
    modification = request.form.get("modification", "").strip()
    goal = case.get_goal(goal_id)
    if not goal:
        return redirect(url_for("index", flash=t("flash_goal_not_found")))

    # Get the saved pending proposal
    from engine import Proposal
    pending = case.pending_proposals.get(goal_id, {})
    proposal = Proposal(**pending) if pending else engine.propose(case, goal)

    # If there's an unreacted observer event for this goal, record the reaction.
    for e in reversed(case.observer_events):
        if e.goal_id == goal_id and not e.participant_reaction:
            case.record_observer_reaction(e.id, decision)
            break

    if decision == "ACCEPT":
        case.record_decision(DECISION_ACCEPT, goal_id=goal_id, context=proposal.suggestion)
        case.add_mission(goal_id=goal_id, purpose=proposal.mission_purpose,
                         description=proposal.mission_description,
                         definition_of_done=proposal.definition_of_done,
                         name=proposal.mission_name)
        case.pending_proposals.pop(goal_id, None)
        save_case()
        return redirect(url_for("goal_view", goal_id=goal_id, flash=t("flash_mission_accepted")))

    elif decision == "MODIFY" and modification:
        case.record_decision(DECISION_MODIFY, goal_id=goal_id, context=modification)
        case.add_mission(goal_id=goal_id, purpose=proposal.mission_purpose,
                         description=modification,
                         definition_of_done=proposal.definition_of_done,
                         name=proposal.mission_name)
        case.pending_proposals.pop(goal_id, None)
        save_case()
        return redirect(url_for("goal_view", goal_id=goal_id, flash=t("flash_mission_modified")))

    elif decision == "REJECT":
        case.record_decision(DECISION_REJECT, goal_id=goal_id, context="Rejected")
        case.pending_proposals.pop(goal_id, None)
        save_case()
        return redirect(url_for("goal_view", goal_id=goal_id, flash=t("flash_rejected")))

    elif decision == "EXPLORE_FURTHER":
        case.record_decision(DECISION_EXPLORE, goal_id=goal_id, context="Exploring")
        case.pending_proposals.pop(goal_id, None)
        save_case()
        suggestions = engine.suggest(case, goal)
        return render("goal", active_goal=goal, suggestions=suggestions,
                      suggestion_goal_id=goal_id,
                      flash_message=t("flash_exploring"))

    elif decision == "GIVE_UP":
        case.record_decision(DECISION_GIVE_UP, goal_id=goal_id, context="Gave up")
        case.abandon_goal(goal_id, reason="Participant chose to give up.")
        case.pending_proposals.pop(goal_id, None)
        save_case()
        return redirect(url_for("index", flash=t("flash_goal_abandoned")))

    return redirect(url_for("index"))


@app.route("/complete_mission/<mission_id>", methods=["POST"])
def complete_mission(mission_id):
    observation_text = request.form.get("observation", "").strip()
    mission = case.get_mission(mission_id)
    if not mission:
        return redirect(url_for("index", flash=t("flash_mission_not_found")))

    case.complete_mission(mission_id, result=observation_text or "Completed")
    if observation_text:
        case.add_observation(observation_text, mission_id=mission_id)
        case.update_situation(observation_text)
    save_case()
    return redirect(url_for("goal_view", goal_id=mission.goal_id, flash=t("flash_mission_done")))


@app.route("/observe", methods=["POST"])
def observe():
    observation_text = request.form.get("observation", "").strip()
    goal_id = request.form.get("goal_id", "").strip()
    if not observation_text:
        return redirect(url_for("index", flash=t("flash_no_observation")))
    # Record the observation into the Case File. It becomes context for the
    # next proposal, but it does NOT overwrite the current situation and does
    # NOT trigger a new goal automatically. The participant stays in control.
    case.add_observation(observation_text, mission_id=None)
    save_case()
    if goal_id:
        return redirect(url_for("goal_view", goal_id=goal_id, flash=t("flash_observation_recorded")))
    return redirect(url_for("index", flash=t("flash_observation_recorded")))


@app.route("/add_goal", methods=["POST"])
def add_goal():
    direction = request.form.get("direction", "").strip()
    if not direction:
        return redirect(url_for("index", flash=t("flash_no_direction")))
    case.add_goal(desired_direction=direction)
    save_case()
    return redirect(url_for("index", flash=t("flash_goal_added")))


@app.route("/new_goals", methods=["POST"])
def new_goals():
    """All goals done — ask the Engine for fresh goals based on where we are."""
    # Use the accumulated case as context via a temp goal describing the vision.
    vision = case.context.get("description", "our situation")
    temp_goal = Goal(desired_direction=f"Build on progress so far in: {vision}")
    directions = engine.suggest(case, temp_goal)
    created = 0
    for d in directions:
        title = d.get("title", "")
        desc = d.get("description", "")
        direction = f"{title}: {desc}" if desc else title
        if direction.strip():
            case.add_goal(desired_direction=direction)
            created += 1
    save_case()
    return redirect(url_for("index", flash=t("flash_new_goals", n=created)))


@app.route("/complete_goal/<goal_id>", methods=["POST"])
def complete_goal(goal_id):
    case.complete_goal(goal_id)
    save_case()
    return redirect(url_for("index", flash=t("flash_goal_completed")))


@app.route("/abandon_goal/<goal_id>", methods=["POST"])
def abandon_goal(goal_id):
    case.abandon_goal(goal_id, reason="Participant marked as given up.")
    save_case()
    return redirect(url_for("index", flash=t("flash_goal_abandoned")))


# --- Concept tree (concept mode) ---
#
# One level of points hangs under a goal (its desired_direction is the sentence)
# or under another point. The owner edits, chooses and parks points. The Engine
# only proposes. Slow AI calls (generate, deep) run on a snapshot of the case and
# the result is applied to a fresh copy from disk, because the module-global
# `case` is replaced by every request (known single-user limit).

MAX_CONCEPT_TITLE = 200
MAX_CONCEPT_TEXT = 8000
MAX_CONTEXT_TEXT = 10000
MAX_ANGLE = 300
MAX_SPEC = 600


def _concept_redirect(goal_id, parent_id=None, flash=""):
    args = {}
    if parent_id:
        args["parent"] = parent_id
    if flash:
        args["flash"] = flash
    return redirect(url_for("concepts_page", goal_id=goal_id, **args))


def _concept_parent(goal_id, raw_id):
    """Resolve a parent id from the request. Returns (ok, parent). An empty id
    means the goal root; an id that is not a point of this goal is not ok."""
    raw_id = (raw_id or "").strip()
    if not raw_id:
        return True, None
    node = case.get_concept(raw_id)
    if node and node.goal_id == goal_id:
        return True, node
    return False, None


def _concept_path(node):
    """Points from the first level down to `node`."""
    path, seen = [], set()
    while node is not None and node.id not in seen:
        seen.add(node.id)
        path.append(node)
        node = case.get_concept(node.parent_id) if node.parent_id else None
    return list(reversed(path))


def _reload_case():
    """A fresh copy of the selected case from disk (used after slow AI calls)."""
    return CaseFile.load(str(CASES_DIR / f"{session['case_id']}.json"))


def _root_goal_id():
    """Id of the hidden root goal of a case started from the 'describe the
    situation' page, or None for older cases."""
    gid = case.context.get("root_goal_id")
    return gid if gid and case.get_goal(gid) else None


def _store_product(product):
    """Write the end-product reading to a fresh copy of the case and to the one in memory."""
    fresh = _reload_case()
    fresh.context["product"] = product
    fresh._log("product_set", {"source": product.get("source"), "confidence": product.get("confidence"),
                               "scale": product.get("scale")})
    fresh.save(directory="cases")
    case.context["product"] = product


def _ensure_product():
    """Older cases have no reading of the end product yet. Make one the first time it is
    needed, so every prompt can use it. Failing to make one never blocks the work."""
    if case.context.get("product") or not concept_engine.available:
        return
    product = concept_engine.infer_product(case)
    if product:
        _store_product(product)


def _small_hint(goal_id):
    """A small thing does not need a tree of proposals; offer the start list straight away."""
    prod = case.context.get("product") or {}
    return prod.get("scale") == "liten" and not any(a.goal_id == goal_id for a in case.actions)


def _apply_generate(goal, parent, mode, with_product=True):
    """One generate run, stored on a fresh copy of the case. Returns a flash text."""
    parent_id = parent.id if parent else None
    if not concept_engine.available:
        return t("flash_concepts_no_ai")
    if with_product:
        _ensure_product()
    points = concept_engine.generate(case, goal, parent, mode)
    if not points:
        return t("flash_concepts_failed")
    fresh = _reload_case()
    # New points are open slots; the owner keeps the ones worth keeping.
    for p in points:
        fresh.add_concept(goal.id, p["title"], p["text"], parent_id=parent_id,
                          status=CONCEPT_CANDIDATE, source="ai", mode=mode)
    # Splitting a point shows interest in it, so it is kept (survives a re-run).
    parent_node = fresh.get_concept(parent_id) if parent_id else None
    if parent_node and parent_node.status == CONCEPT_CANDIDATE:
        fresh.set_concept_status(parent_id, CONCEPT_ACTIVE)
    fresh.save(directory="cases")
    return t("flash_concepts_added", n=len(points))


def _apply_vary(goal, node, angle=""):
    """Variera one proposal: new proposals with the same intent but a different
    mechanism. They become open slots on the same level, marked as variants of
    the proposal, which is kept. Returns a flash text."""
    if not concept_engine.available:
        return t("flash_concepts_no_ai")
    parent = case.get_concept(node.parent_id) if node.parent_id else None
    _ensure_product()
    points = concept_engine.vary_from(case, goal, parent, node, angle)
    if not points:
        return t("flash_concepts_failed")
    fresh = _reload_case()
    for p in points:
        fresh.add_concept(goal.id, p["title"], p["text"], parent_id=node.parent_id,
                          status=CONCEPT_CANDIDATE, source="ai", mode=CONCEPT_MODE_VARY,
                          variant_of=node.id)
    base = fresh.get_concept(node.id)
    if base and base.status == CONCEPT_CANDIDATE:  # varying a proposal shows interest in it
        fresh.set_concept_status(node.id, CONCEPT_ACTIVE)
    fresh.save(directory="cases")
    return t("flash_concepts_varied", n=len(points), title=node.title)


def _apply_strengthen(goal, node, direction=""):
    """Förstärk: ask for a more concrete version of one proposal. The answer is stored
    as a draft on the point; nothing changes until the owner uses it."""
    if not concept_engine.available:
        return t("flash_concepts_no_ai")
    parent = case.get_concept(node.parent_id) if node.parent_id else None
    _ensure_product()
    draft = concept_engine.strengthen(case, goal, parent, node, direction)
    if not draft:
        return t("flash_concepts_failed")
    fresh = _reload_case()
    fresh.set_concept_draft(node.id, draft["text"], draft["spec"], draft["missing"])
    fresh.save(directory="cases")
    return t("flash_concepts_strengthened")


def _tree_rows(goal_id):
    """The concept tree as a flat, depth-first list for the overview. Set-aside
    points are left out (their number is reported separately)."""
    nodes = [c for c in case.concepts if c.goal_id == goal_id]
    kids = {}
    for c in sorted(nodes, key=lambda c: c.timestamp):
        if c.status != CONCEPT_PARKED:
            kids.setdefault(c.parent_id, []).append(c)
    rows = []

    def walk(parent_id, depth, seen):
        for c in kids.get(parent_id, []):
            if c.id in seen:
                continue
            rows.append({"node": c, "depth": depth,
                         "children": len(kids.get(c.id, [])),
                         "spec_n": sum(1 for k in SPEC_KEYS if (c.spec.get(k) or "").strip())})
            walk(c.id, depth + 1, seen | {c.id})

    walk(None, 0, set())
    parked = sum(1 for c in nodes if c.status == CONCEPT_PARKED)
    return rows, parked


def _apply_themes(goal, parent):
    """Collect the open proposals on a level into themes (as many as there are free
    places), keep one proposal per theme open and set the rest aside. Nothing is
    deleted. If the grouping fails nothing is changed."""
    parent_id = parent.id if parent else None
    if not concept_engine.available:
        return t("flash_concepts_no_ai")
    nodes = case.concepts_under(goal.id, parent_id)
    kept = [n for n in nodes if n.status == CONCEPT_ACTIVE]
    open_ = [n for n in nodes if n.status == CONCEPT_CANDIDATE]
    target = max(1, POINTS_PER_RUN - len(kept))
    if len(open_) <= target:
        return t("flash_concepts_few_to_group")
    themes, clustered, error = concept_engine.themes_of(open_, target)
    if not clustered:
        return t("flash_concepts_failed") + f" [{error}]"

    themes = sorted(themes, key=lambda th: -len(th["points"]))
    fresh = _reload_case()
    aside = 0
    for rank, th in enumerate(themes):
        rep_node = open_[th["rep"]]
        shown = rank < target
        for i in th["points"]:
            node = open_[i]
            fresh.set_concept_theme(node.id, th["name"], rep_node.id if shown else None)
            if not (shown and i == th["rep"]):
                fresh.set_concept_status(node.id, CONCEPT_PARKED)
                aside += 1
    fresh.save(directory="cases")
    return t("flash_concepts_themes_done", themes=min(target, len(themes)), aside=aside)


def _node_depth(node):
    d, seen = 1, {node.id}
    while node.parent_id and node.parent_id not in seen:
        parent = case.get_concept(node.parent_id)
        if parent is None:
            break
        seen.add(parent.id)
        node, d = parent, d + 1
    return d


def _ready_to_start(goal_id):
    """The 'ping': true when the tree is concrete enough to try to collect a start list.
    Deliberately a cheap check without any AI call: a kept point on level two or deeper
    has all four nailing-down parts, and no list has been collected yet."""
    if any(a.goal_id == goal_id for a in case.actions):
        return False
    return any(n.goal_id == goal_id and n.status == CONCEPT_ACTIVE and _node_depth(n) >= 2
               and case.spec_complete(n) for n in case.concepts)


def _apply_collect(goal):
    """Collect a start list from the whole tree plus the owner's two texts. Decided
    (accepted) actions stay; proposals that were never decided are replaced and set aside."""
    if not concept_engine.available:
        return t("flash_concepts_no_ai"), False
    nodes = [n for n in case.concepts
             if n.goal_id == goal.id and n.status == CONCEPT_ACTIVE]
    nodes.sort(key=lambda n: (_node_depth(n), n.timestamp))
    _ensure_product()
    if not nodes and (case.context.get("product") or {}).get("scale") != "liten":
        return t("flash_actions_no_nodes"), False
    decided = [a.title for a in case.actions if a.goal_id == goal.id and a.status == ACTION_ACCEPTED]
    result = concept_engine.collect_actions(case, goal, nodes, decided)
    if not result:
        return t("flash_actions_failed"), False
    fresh = _reload_case()
    created = fresh.replace_proposed_actions(goal.id, result["actions"])
    fresh.context["actions_assumptions"] = result["assumptions"]
    fresh.save(directory="cases")
    return t("flash_actions_collected", n=len(created)), True


def _actions_view(goal_id):
    """Everything the tree page needs to show the start list."""
    titles = {c.id: c.title for c in case.concepts if c.goal_id == goal_id}
    atitles = {a.id: a.title for a in case.actions}
    def view(a):
        return {"a": a, "serves": [titles[i] for i in a.serves if i in titles],
                "needs": [atitles[i] for i in a.needs if i in atitles],
                "mission": case.get_mission(a.mission_id) if a.mission_id else None}
    mine = sorted((a for a in case.actions if a.goal_id == goal_id), key=lambda a: (a.layer != ACTION_LAYER_BASE, a.order))
    proposed = [view(a) for a in mine if a.status == ACTION_PROPOSED]
    accepted = [view(a) for a in mine if a.status == ACTION_ACCEPTED]
    doing = [v for v in accepted if v["mission"] and v["mission"].status == MISSION_ACTIVE]
    done = [v for v in accepted if v["mission"] and v["mission"].status != MISSION_ACTIVE]
    dismissed = [view(a) for a in mine if a.status == ACTION_DISMISSED]
    # Points that no live action serves yet. Base actions are for the whole case and do not
    # count: they do not make a single point doable.
    live = [a for a in mine if a.status != ACTION_DISMISSED and a.layer == ACTION_LAYER_POINTS]
    served = {i for a in live for i in a.serves}
    kept = [c for c in case.concepts if c.goal_id == goal_id and c.status == CONCEPT_ACTIVE]
    uncovered = [c for c in kept if c.id not in served] if mine else []
    return {"proposed": proposed, "doing": doing, "done": done, "dismissed": dismissed,
            "uncovered": uncovered, "any": bool(mine),
            "assumptions": case.context.get("actions_assumptions", [])}


def _apply_reroll(goal, parent):
    """Slot-machine re-run. Points the owner has kept stay; every other open slot
    is replaced by new proposals made through a randomly drawn lens. Replaced
    points are set aside (not deleted) and the Engine is told not to repeat them."""
    parent_id = parent.id if parent else None
    if not concept_engine.available:
        return t("flash_concepts_no_ai")
    nodes = case.concepts_under(goal.id, parent_id)
    kept = [n for n in nodes if n.status == CONCEPT_ACTIVE]
    count = POINTS_PER_RUN - len(kept)
    if count <= 0:
        return t("flash_concepts_all_kept")

    recent = [n.lens for n in sorted(nodes, key=lambda n: n.timestamp, reverse=True) if n.lens]
    lens_id = pick_lens(recent)
    mode = CONCEPT_MODE_SPLIT if parent else CONCEPT_MODE_VARY
    _ensure_product()
    points = concept_engine.generate(case, goal, parent, mode, lens_id, count=count)
    if not points:
        return t("flash_concepts_failed")  # nothing is replaced when the run fails

    fresh = _reload_case()
    for n in fresh.concepts_under(goal.id, parent_id):
        if n.status == CONCEPT_CANDIDATE:
            fresh.set_concept_status(n.id, CONCEPT_PARKED)
    for p in points:
        fresh.add_concept(goal.id, p["title"], p["text"], parent_id=parent_id,
                          status=CONCEPT_CANDIDATE, source="ai", mode=mode, lens=lens_id)
    fresh.save(directory="cases")
    return t("flash_concepts_rerolled", n=len(points), lens=LENSES[lens_id]["name"])


def _apply_deep(goal, parent, lens_ids, mode, angle="", with_product=True):
    """A deep-mode run, stored on a fresh copy of the case. At most four themes become
    open proposals (one representative each). The other points of a theme, and points
    from themes over the limit, are set aside, not thrown away. Returns a flash text."""
    parent_id = parent.id if parent else None
    if not concept_engine.available:
        return t("flash_concepts_no_ai")
    if with_product:
        _ensure_product()
    result = concept_engine.deep(case, goal, parent, lens_ids, mode, angle)
    if result["runs_ok"] == 0:
        return t("flash_concepts_failed")
    fresh = _reload_case()
    set_aside = 0
    for th in result["themes"]:
        rep = fresh.add_concept(goal.id, th["title"], th["text"], parent_id=parent_id,
                                status=CONCEPT_CANDIDATE, source="ai", mode=CONCEPT_MODE_DEEP,
                                lens=th["lens"], stability=th["stability"], seen_in=th["seen_in"],
                                theme=th["name"])
        for o in th["others"]:
            fresh.add_concept(goal.id, o["title"], o["text"], parent_id=parent_id,
                              status=CONCEPT_PARKED, source="ai", mode=CONCEPT_MODE_DEEP,
                              lens=o["lens"], variant_of=rep.id, theme=th["name"])
            set_aside += 1
    for o in result["overflow"]:
        fresh.add_concept(goal.id, o["title"], o["text"], parent_id=parent_id,
                          status=CONCEPT_PARKED, source="ai", mode=CONCEPT_MODE_DEEP, lens=o["lens"])
        set_aside += 1
    fresh.save(directory="cases")
    flash = t("flash_concepts_deep", points=result["points"], new=len(result["themes"]),
              aside=set_aside, ok=result["runs_ok"], total=result["runs_total"])
    if not result["clustered"]:
        flash += " " + t("flash_concepts_ungrouped") + (f" [{result['group_error']}]" if result["group_error"] else "")
        # Written to the case history so the cause can be read from the case file later.
        fresh2 = _reload_case()
        fresh2._log("deep_group_failed", {"error": result["group_error"], "points": result["points"]})
        fresh2.save(directory="cases")
    return flash


@app.route("/begin", methods=["POST"])
def begin():
    """First page of a new case: the owner describes the situation and the wish.
    A hidden root goal is created so the concept tree has somewhere to hang."""
    if _root_goal_id():
        return redirect(url_for("index"))
    if case.goals:
        return redirect(url_for("index"))  # an older case with goals keeps its own flow
    identity = request.form.get("identity_text", "").strip()[:MAX_CONTEXT_TEXT]
    ideal = request.form.get("ideal_text", "").strip()[:MAX_CONTEXT_TEXT]
    if not identity and not ideal:
        return render("onboarding", flash_message=t("flash_begin_empty"))

    case.context["identity_text"] = identity
    case.context["ideal_text"] = ideal
    root = case.add_goal(case.context.get("description") or t("concepts_title"))
    case.context["root_goal_id"] = root.id
    save_case()

    # The reading of the end product runs alongside the first proposals so it adds no waiting.
    # The first proposals are therefore made without it; everything after them uses it.
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=1) as pool:
        product_job = pool.submit(concept_engine.infer_product, case) if concept_engine.available else None
        if request.form.get("action") == "deep":
            flash = _apply_deep(root, None, DEFAULT_DEEP_LENSES, CONCEPT_MODE_VARY, with_product=False)
        else:
            flash = _apply_generate(root, None, CONCEPT_MODE_VARY, with_product=False)
        product = product_job.result() if product_job else None
    if product:
        _store_product(product)
    return _concept_redirect(root.id, None, flash)


@app.route("/concepts/<goal_id>")
def concepts_page(goal_id):
    goal = case.get_goal(goal_id)
    if not goal:
        return redirect(url_for("index", flash=t("flash_goal_not_found")))
    ok, parent = _concept_parent(goal_id, request.args.get("parent"))
    if not ok:
        return _concept_redirect(goal_id)
    nodes = case.concepts_under(goal_id, parent.id if parent else None)
    child_counts = {}
    for c in case.concepts:
        if c.goal_id == goal_id and c.parent_id:
            child_counts[c.parent_id] = child_counts.get(c.parent_id, 0) + 1
    return render(
        "concepts",
        active_goal=goal,
        concept_parent=parent,
        concept_path=_concept_path(parent) if parent else [],
        concepts_slots=[n for n in nodes if n.status in (CONCEPT_ACTIVE, CONCEPT_CANDIDATE)],
        ready_ping=_ready_to_start(goal_id),
        product=case.context.get("product"),
        small_hint=_small_hint(goal_id),
        themes_target=max(1, POINTS_PER_RUN - sum(1 for n in nodes if n.status == CONCEPT_ACTIVE)),
        themes_open=sum(1 for n in nodes if n.status == CONCEPT_CANDIDATE),
        concepts_parked=[n for n in nodes if n.status == CONCEPT_PARKED],
        child_counts=child_counts,
        is_root_goal=(goal_id == _root_goal_id()),
        concept_titles={c.id: c.title for c in case.concepts if c.goal_id == goal_id},
        identity_text=concept_engine.identity_text(case),
        ideal_text=concept_engine.ideal_text(case),
        flash_message=request.args.get("flash", ""),
    )


@app.route("/concepts/<goal_id>/context", methods=["POST"])
def concepts_context(goal_id):
    if not case.get_goal(goal_id):
        return redirect(url_for("index", flash=t("flash_goal_not_found")))
    case.context["identity_text"] = request.form.get("identity_text", "").strip()[:MAX_CONTEXT_TEXT]
    case.context["ideal_text"] = request.form.get("ideal_text", "").strip()[:MAX_CONTEXT_TEXT]
    case._log("concept_context_saved", {"goal_id": goal_id})
    save_case()
    return _concept_redirect(goal_id, flash=t("flash_concepts_saved"))


@app.route("/concepts/<goal_id>/generate", methods=["POST"])
def concepts_generate(goal_id):
    goal = case.get_goal(goal_id)
    if not goal:
        return redirect(url_for("index", flash=t("flash_goal_not_found")))
    ok, parent = _concept_parent(goal_id, request.form.get("parent_id"))
    if not ok:
        return _concept_redirect(goal_id)
    mode = request.form.get("mode", CONCEPT_MODE_SPLIT)
    if mode not in (CONCEPT_MODE_SPLIT, CONCEPT_MODE_VARY):
        mode = CONCEPT_MODE_SPLIT
    flash = _apply_generate(goal, parent, mode)
    return _concept_redirect(goal_id, parent.id if parent else None, flash)


@app.route("/concepts/<goal_id>/deep", methods=["POST"])
def concepts_deep(goal_id):
    goal = case.get_goal(goal_id)
    if not goal:
        return redirect(url_for("index", flash=t("flash_goal_not_found")))
    ok, parent = _concept_parent(goal_id, request.form.get("parent_id"))
    if not ok:
        return _concept_redirect(goal_id)
    parent_id = parent.id if parent else None
    mode = request.form.get("mode", CONCEPT_MODE_VARY)
    if mode not in (CONCEPT_MODE_SPLIT, CONCEPT_MODE_VARY):
        mode = CONCEPT_MODE_VARY
    lens_ids = [l for l in request.form.getlist("lens") if l in LENSES]
    if not lens_ids:
        return _concept_redirect(goal_id, parent_id, t("flash_concepts_pick_lens"))
    angle = request.form.get("angle", "").strip()[:MAX_ANGLE]
    flash = _apply_deep(goal, parent, lens_ids, mode, angle)
    return _concept_redirect(goal_id, parent_id, flash)


@app.route("/concepts/<goal_id>/reroll", methods=["POST"])
def concepts_reroll(goal_id):
    goal = case.get_goal(goal_id)
    if not goal:
        return redirect(url_for("index", flash=t("flash_goal_not_found")))
    ok, parent = _concept_parent(goal_id, request.form.get("parent_id"))
    if not ok:
        return _concept_redirect(goal_id)
    flash = _apply_reroll(goal, parent)
    return _concept_redirect(goal_id, parent.id if parent else None, flash)


@app.route("/concepts/<goal_id>/themes", methods=["POST"])
def concepts_themes(goal_id):
    goal = case.get_goal(goal_id)
    if not goal:
        return redirect(url_for("index", flash=t("flash_goal_not_found")))
    ok, parent = _concept_parent(goal_id, request.form.get("parent_id"))
    if not ok:
        return _concept_redirect(goal_id)
    flash = _apply_themes(goal, parent)
    return _concept_redirect(goal_id, parent.id if parent else None, flash)


@app.route("/concepts/<goal_id>/add", methods=["POST"])
def concepts_add(goal_id):
    if not case.get_goal(goal_id):
        return redirect(url_for("index", flash=t("flash_goal_not_found")))
    ok, parent = _concept_parent(goal_id, request.form.get("parent_id"))
    if not ok:
        return _concept_redirect(goal_id)
    parent_id = parent.id if parent else None
    title = request.form.get("title", "").strip()[:MAX_CONCEPT_TITLE]
    text = request.form.get("text", "").strip()[:MAX_CONCEPT_TEXT]
    if not title:
        return _concept_redirect(goal_id, parent_id)
    case.add_concept(goal_id, title, text, parent_id=parent_id, status=CONCEPT_ACTIVE,
                     source="owner", mode=CONCEPT_MODE_OWNER)
    save_case()
    return _concept_redirect(goal_id, parent_id, t("flash_concepts_saved"))


@app.route("/concepts/node/<concept_id>/edit", methods=["POST"])
def concepts_edit(concept_id):
    node = case.get_concept(concept_id)
    if not node:
        return redirect(url_for("index"))
    title = request.form.get("title", "").strip()[:MAX_CONCEPT_TITLE]
    text = request.form.get("text", "").strip()[:MAX_CONCEPT_TEXT]
    if title:
        case.edit_concept(concept_id, title, text)  # editing does not change keep/open status
        save_case()
    return _concept_redirect(node.goal_id, node.parent_id, t("flash_concepts_saved") if title else "")


@app.route("/concepts/node/<concept_id>/vary", methods=["POST"])
def concepts_vary(concept_id):
    node = case.get_concept(concept_id)
    goal = case.get_goal(node.goal_id) if node else None
    if not node or not goal:
        return redirect(url_for("index"))
    angle = request.form.get("angle", "").strip()[:MAX_ANGLE]
    flash = _apply_vary(goal, node, angle)
    return _concept_redirect(node.goal_id, node.parent_id, flash)


@app.route("/concepts/<goal_id>/tree")
def concepts_tree(goal_id):
    goal = case.get_goal(goal_id)
    if not goal:
        return redirect(url_for("index", flash=t("flash_goal_not_found")))
    rows, parked = _tree_rows(goal_id)
    return render(
        "concepts_tree",
        active_goal=goal,
        is_root_goal=(goal_id == _root_goal_id()),
        tree_rows=rows,
        tree_parked=parked,
        tree_kept=sum(1 for r in rows if r["node"].status == CONCEPT_ACTIVE),
        tree_nailed=sum(1 for r in rows if r["node"].spiked),
        tree_depth=(max((r["depth"] for r in rows), default=-1) + 1),
        ready_ping=_ready_to_start(goal_id),
        product=case.context.get("product"),
        small_hint=_small_hint(goal_id),
        actions=_actions_view(goal_id),
        flash_message=request.args.get("flash", ""),
    )


def _tree_redirect(goal_id, flash=""):
    args = {"flash": flash} if flash else {}
    return redirect(url_for("concepts_tree", goal_id=goal_id, **args))


@app.route("/concepts/<goal_id>/product", methods=["POST"])
def concepts_product(goal_id):
    """The owner edits the end-product reading, answers the Engine's question, or asks for a new reading."""
    goal = case.get_goal(goal_id)
    if not goal:
        return redirect(url_for("index", flash=t("flash_goal_not_found")))
    action = request.form.get("action", "")
    back = request.form.get("back", "concepts")
    flash = t("flash_product_saved")
    if action == "edit":
        end_state = request.form.get("end_state", "").strip()[:400]
        if end_state:
            old = dict(case.context.get("product") or {})
            old.update({"end_state": end_state,
                        "deliverable": request.form.get("deliverable", "").strip()[:400],
                        "source": "owner", "question": ""})
            old.setdefault("scale", "medel"); old.setdefault("confidence", "medel")
            old.setdefault("alternatives", []); old.setdefault("kind", "")
            _store_product(old)
    elif action in ("answer", "redo"):
        if not concept_engine.available:
            flash = t("flash_concepts_no_ai")
        else:
            answer = request.form.get("answer", "").strip()[:1000] if action == "answer" else ""
            product = concept_engine.infer_product(case, answer)
            if product:
                _store_product(product)
            else:
                flash = t("flash_product_failed")
    if back == "tree":
        return _tree_redirect(goal_id, flash)
    return _concept_redirect(goal_id, None, flash)


@app.route("/concepts/<goal_id>/collect", methods=["POST"])
def concepts_collect(goal_id):
    goal = case.get_goal(goal_id)
    if not goal:
        return redirect(url_for("index", flash=t("flash_goal_not_found")))
    flash, _ok = _apply_collect(goal)
    return _tree_redirect(goal_id, flash)


@app.route("/concepts/action/<action_id>/<verb>", methods=["POST"])
def concepts_action(action_id, verb):
    a = case.get_action(action_id)
    if not a or verb not in ("accept", "dismiss", "restore", "edit", "done"):
        return redirect(url_for("index"))
    flash = t("flash_concepts_saved")
    if verb == "accept":
        case.accept_action(action_id)
        flash = t("flash_actions_accepted")
    elif verb == "dismiss":
        case.set_action_status(action_id, ACTION_DISMISSED)
    elif verb == "restore":
        case.set_action_status(action_id, ACTION_PROPOSED)
    elif verb == "edit":
        title = request.form.get("title", "").strip()[:200]
        if title:
            case.edit_action(action_id, title, request.form.get("done_when", "").strip()[:300])
    elif verb == "done":
        case.finish_action(action_id, request.form.get("result", "").strip()[:2000])
        flash = t("flash_actions_done")
    save_case()
    return _tree_redirect(a.goal_id, flash)


@app.route("/concepts/node/<concept_id>/strengthen", methods=["POST"])
def concepts_strengthen(concept_id):
    node = case.get_concept(concept_id)
    goal = case.get_goal(node.goal_id) if node else None
    if not node or not goal:
        return redirect(url_for("index"))
    direction = request.form.get("direction", "").strip()[:MAX_ANGLE]
    flash = _apply_strengthen(goal, node, direction)
    return _concept_redirect(node.goal_id, node.parent_id, flash)


@app.route("/concepts/node/<concept_id>/draft", methods=["POST"])
def concepts_draft(concept_id):
    node = case.get_concept(concept_id)
    if not node:
        return redirect(url_for("index"))
    if request.form.get("action") == "use":
        case.use_concept_draft(concept_id)
        flash = t("flash_concepts_draft_used")
    else:
        case.drop_concept_draft(concept_id)
        flash = t("flash_concepts_draft_dropped")
    save_case()
    return _concept_redirect(node.goal_id, node.parent_id, flash)


@app.route("/concepts/node/<concept_id>/spec", methods=["POST"])
def concepts_spec(concept_id):
    node = case.get_concept(concept_id)
    if not node:
        return redirect(url_for("index"))
    action = request.form.get("action", "save")
    flash = t("flash_concepts_saved")
    if action != "unnail":
        case.set_concept_spec(concept_id, {k: request.form.get(k, "").strip()[:MAX_SPEC] for k in SPEC_KEYS})
        if action == "save" and node.spiked and not case.spec_complete(node):
            # A nailed point must stay complete, so emptying a part un-nails it.
            case.set_concept_spiked(concept_id, False)
            flash = t("flash_concepts_unnailed_incomplete")
    if action == "nail":
        if case.set_concept_spiked(concept_id, True):
            flash = t("flash_concepts_nailed")
        else:
            flash = t("flash_concepts_nail_incomplete")
    elif action == "unnail":
        case.set_concept_spiked(concept_id, False)
        flash = t("flash_concepts_unnailed")
    save_case()
    return _concept_redirect(node.goal_id, node.parent_id, flash)


@app.route("/concepts/node/<concept_id>/status", methods=["POST"])
def concepts_status(concept_id):
    node = case.get_concept(concept_id)
    if not node:
        return redirect(url_for("index"))
    status = request.form.get("status", "")
    if status in CONCEPT_STATUSES:
        case.set_concept_status(concept_id, status)
        save_case()
    return _concept_redirect(node.goal_id, node.parent_id)


# --- Startup ---

def main():
    log.info("server starting model=%s ai_available=%s auth=%s", engine.model, engine.available,
             auth_client.AUTH_BASE_URL)
    # Cases are now selected per user via the web UI (login -> /cases).
    # No global case is created at startup.
    print(f"  Open: http://localhost:5000")
    print(f"  Log in, then pick or create a case.")
    print(f"  Ctrl+C to stop.\n")
    app.run(debug=False, port=5000)


if __name__ == "__main__":
    main()
