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
from functools import wraps
from pathlib import Path

from dotenv import load_dotenv
from flask import (
    Flask, render_template_string, request, redirect, url_for, session
)

import auth_client

load_dotenv()

from case_file import (
    CaseFile, Goal,
    GOAL_ACTIVE, GOAL_ABANDONED, GOAL_COMPLETED,
    DECISION_ACCEPT, DECISION_MODIFY, DECISION_REJECT,
    DECISION_EXPLORE, DECISION_GIVE_UP,
    MISSION_ACTIVE, MISSION_COMPLETED,
)
from engine_ai import AIEngine
from observer import Observer
from i18n import t, set_language, get_language

# Default GUI language. Change with: LANG=en python src/web.py ...
set_language(os.environ.get("LANG_UI", "sv"))

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-insecure-flask-secret")
app.jinja_env.globals["t"] = t          # make t() available in templates
engine = AIEngine()
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
              onsubmit="return confirm('Radera detta case?');">
          <button type="submit" style="background:#c33;">Radera</button>
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

{% if view != 'onboarding' and case.goals %}
<div class="topbar"><a href="/">&#8962; {{ t('nav_overview') }}</a></div>
{% endif %}

{% if flash_message %}
<div class="flash">{{ flash_message }}</div>
{% endif %}

<!-- ==================== ONBOARDING ==================== -->
{% if view == 'onboarding' %}
<div class="onboarding">
    <h2>{{ t('onboarding_title') }}</h2>
    <p>{{ t('onboarding_help')|safe }}</p>
    <form method="POST" action="/start">
        <textarea name="input" rows="2" placeholder="{{ t('onboarding_placeholder') }}" style="font-size: 1.1em;"></textarea><br><br>
        <button type="submit" class="btn-primary" style="font-size: 1.1em; padding: 12px 24px;">{{ t('onboarding_go') }}</button>
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

<form method="POST" action="/complete_goal/{{ active_goal.id }}" style="margin-top: 10px; display: inline;">
    <button type="submit" class="btn-small btn-accept">{{ t('mark_goal_done') }}</button>
</form>
<form method="POST" action="/abandon_goal/{{ active_goal.id }}" style="margin-top: 10px; display: inline;">
    <button type="submit" class="btn-small btn-giveup">{{ t('give_up') }}</button>
</form>

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
    }
    defaults.update(kwargs)
    return render_template_string(HTML, **defaults)


# --- Routes ---

@app.route("/")
def index():
    flash = request.args.get("flash", "")
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


# --- Startup ---

def main():
    # Cases are now selected per user via the web UI (login -> /cases).
    # No global case is created at startup.
    print(f"  Open: http://localhost:5000")
    print(f"  Log in, then pick or create a case.")
    print(f"  Ctrl+C to stop.\n")
    app.run(debug=False, port=5000)


if __name__ == "__main__":
    main()
