"""
Concept mode.

Turns one sentence (a Goal's desired_direction), the participant's own
description of the situation and the desired state into four points. A point
can be split further, varied, or run through "deep mode" (several runs, each
through a different lens).

Design decisions (see CURRENT.md / LAST_SESSION.md):
- A point is a name and plain, editable text. No fixed fields are stored.
  The prompt still asks the model to cover what the point means, what it comes
  from, how it meets the desired state, which function of the current way of
  doing things it replaces or keeps, and its biggest risk. That is what gave
  depth in the experiments, but the answer is kept as prose.
- The Engine proposes, the owner decides. Nothing here changes a Goal or
  Mission. It only returns proposals.
- Lenses are hypotheses. Their effect on the output is not yet tested.
- Everything the model says is design assumptions, not evidence.
"""

import json
import math
import random
import re
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from case_file import (
    CaseFile, Goal, ConceptNode,
    CONCEPT_ACTIVE, CONCEPT_MODE_SPLIT, CONCEPT_MODE_VARY,
)
from app_log import get_logger, log_ai
from i18n import t
from engine_ai import AIEngine, MODEL

log = get_logger("concepts")

POINTS_PER_RUN = 4
MAX_COMPLETION_TOKENS = 5000
# Grouping is a small answer, but the model spends 500-1500 hidden reasoning tokens on it
# (measured), and those count against this limit. 2000 left too little margin.
GROUP_MAX_COMPLETION_TOKENS = 6000
GROUP_ATTEMPTS = 2
MAX_LENSES = 5
# Deep mode: each lens gives only a few points, which are then collected into themes.
DEEP_POINTS_PER_LENS = 2
MAX_THEMES = 4


# --- Lenses -----------------------------------------------------------------
# A lens changes HOW the input is read. A mode (split / vary) changes what KIND
# of output is wanted. Keep these short and fixed so runs are comparable.

LENSES = {
    "concept": {
        "name": "Koncept",
        "instruction": "Fråga vilket helt system eller vilken helhet som skulle kunna finnas, inte bara delar av dagens.",
    },
    "outcome": {
        "name": "Mål och resultat",
        "instruction": "Fråga vad som ska vara sant när det är klart, och hur man skulle se det.",
    },
    "philosophical": {
        "name": "Filosofisk",
        "instruction": "Fråga vad orden egentligen betyder och vilka antaganden som ligger i dem.",
    },
    "builder": {
        "name": "Byggare",
        "instruction": "Fråga vad det minsta är som går att pröva, vem som skulle göra det och vad det kräver.",
    },
    "affected": {
        "name": "Den berörde",
        "instruction": "Läs allt ur den berördes egna ögon. Hur skulle hen själv beskriva det och vad skulle hen märka?",
    },
    "systems": {
        "name": "Systemtänkare",
        "instruction": "Titta på återkopplingar, hävstänger, dolda funktioner och hur lösningar kan skapa nya problem.",
    },
    "constraints": {
        "name": "Regelverk och resurser",
        "instruction": "Fråga vad som hindrar, vad det kostar och vilka regler eller beroenden som gäller.",
    },
    "critic": {
        "name": "Kritiker och provokatör",
        "instruction": "Utmana förgivettaganden. Föreslå minst en punkt som känns obekväm eller som ifrågasätter själva ramen.",
    },
}

DEFAULT_DEEP_LENSES = ["concept", "philosophical", "builder", "affected"]


SYSTEM_PROMPT = """\
Du är resonemangsdelen i en Adaptive Navigation Engine. Detta är ett tankeexperiment
om att utforma något nytt. Det är inte en plan för nästa steg och inte råd om verkliga människor.

Regler:
- Föreslå punkter (sätt att förstå eller utforma något), inte uppgifter att utföra.
- Du får lämna nuvarande former. Ange då vilken FUNKTION de fyllde och om punkten ersätter eller bevarar den.
- Bedöm mot det önskade läget. Om underlaget anger ett minimikrav, bedöm också mot det.
- Var ärlig med spänningar och största risk.
- Hitta inte på belägg, forskning eller siffror. Markera antaganden som antaganden.
- Aldrig order, skuldbeläggning eller uppmaning till deltagaren att ändra sig.
- Svara på samma språk som deltagarens text.
"""

ACTIONS_SYSTEM_PROMPT = """\
Du är resonemangsdelen i en Adaptive Navigation Engine. Uppgiften är att hitta konkreta handlingar att börja med.

Regler:
- En handling är ett steg som en person kan börja på och bli klar med på högst en dag, med ett resultat som går att se. Skriv den som verb + föremål.
- Hitta inte på vad deltagaren redan har, kan eller har tillgång till. Om något är oklart, skriv det som ett antagande.
- Hitta inte på belägg, siffror eller namn.
- Aldrig order, skuldbeläggning eller uppmaning till deltagaren att ändra sig.
- Svara på samma språk som deltagarens text.
"""

ACTION_MAX_TITLE = 200
ACTION_MAX_DONE = 300
ACTIONS_MAX_TOTAL = 10

MODE_INSTRUCTIONS = {
    CONCEPT_MODE_SPLIT: (
        "Dela upp: punkterna ska vara delar som tillsammans utgör det som valts, "
        "olika sätt att förstå och utveckla vad det innebär. Inte en plan med steg."
    ),
    CONCEPT_MODE_VARY: (
        "Variera: punkterna ska vara alternativ som skiljer sig tydligt från varandra "
        "och från det som redan finns. Minst en ska vara ovanlig."
    ),
}

# Variation that actually differs. Measured against the soft instruction above: with
# the same input, independent runs through different lenses mostly rediscovered the
# points that already existed (16 points -> 5 groups, 1 new). Showing what exists and
# demanding a different MECHANISM along named axes gave 12 groups, 8 new.
AXES = ("vem som bestämmer, var och när det sker, hur det organiseras, vilka som är inblandade "
        "och vilken roll de har, hur framsteg eller resultat visas, och vad som bär kostnaden "
        "eller håller det uppe")

VARY_BY_MECHANISM = (
    "Variera: punkterna ska skilja sig i MEKANISM från allt som redan finns på nivån och från varandra. "
    "Det räcker inte att byta ord eller betoning. Låt varje punkt skilja sig längs minst tre av dessa axlar "
    f"jämfört med de befintliga: {AXES}. Minst en ska vara ovanlig."
)

OUTPUT_FORMAT = """\
Svara ENDAST med ett JSON-objekt:
{{
  "points": [
    {{
      "title": "kort namn (2-5 ord)",
      "core": "kärnan i punkten, alltså själva idén och vad den innebär, i 2-4 meningar. Börja med idén, inte med var den kommer ifrån.",
      "reasoning": "ett stycke på 3-5 meningar: vilken del av underlaget punkten kommer ur, hur den möter det önskade läget, vilken funktion den ersätter eller bevarar, och största risk."
    }}
  ]
}}
Exakt {count} {noun}."""


def output_format(count: int) -> str:
    return OUTPUT_FORMAT.format(count=count, noun="punkt" if count == 1 else "punkter")


def _clean_json(raw: str):
    """Parse model output as JSON, tolerating a markdown fence."""
    raw = (raw or "").strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
        if raw.rstrip().endswith("```"):
            raw = raw.rstrip()[:-3]
        raw = raw.strip()
    # strict=False: the model sometimes puts a real line break inside a string
    # (the two-paragraph texts), which strict JSON rejects.
    try:
        return json.loads(raw, strict=False)
    except json.JSONDecodeError:
        # It also occasionally leaves a trailing comma before } or ]. Repair that
        # one known slip and try once more; anything else still fails loudly.
        return json.loads(re.sub(r",\s*([}\]])", r"\1", raw), strict=False)


def stability_threshold(n_lenses: int) -> int:
    """How many different lenses a point must appear in to count as stable.
    Roughly 60% of the runs, and never fewer than 2."""
    return max(2, math.ceil(n_lenses * 3 / 5))


def pick_lens(recent: list = None, rng=random) -> str:
    """Draw a lens at random for a re-run, avoiding the lens used last time so
    consecutive re-runs differ. `recent` is a list of lens ids, newest first."""
    avoid = set((recent or [])[:1])
    choices = [l for l in LENSES if l not in avoid] or list(LENSES)
    return rng.choice(choices)


class ConceptEngine:
    """Generates and groups concept points. Needs an AIEngine with a client."""

    def __init__(self, ai: AIEngine):
        self._ai = ai

    @property
    def available(self) -> bool:
        return self._ai.available

    # --- Input -----------------------------------------------------------

    @staticmethod
    def identity_text(case: CaseFile) -> str:
        """The participant's description of the situation. Falls back to
        current_situation when no separate text has been written."""
        return (case.context.get("identity_text") or case.current_situation or "").strip()

    @staticmethod
    def ideal_text(case: CaseFile) -> str:
        return (case.context.get("ideal_text") or "").strip()

    @staticmethod
    def product_block(case: CaseFile) -> str:
        """The Engine's reading of what is being aimed for (possibly edited by the owner),
        as a block for the prompts. Empty when none has been made."""
        prod = case.context.get("product") or {}
        if not prod.get("end_state"):
            return ""
        lines = ["SLUTPRODUKT (tolkning, ägaren kan ha ändrat den):",
                 f"Siktar mot: {prod['end_state']}"]
        if prod.get("deliverable"):
            lines.append(f"Kan framställas härifrån: {prod['deliverable']}")
        if prod.get("answer"):
            lines.append(f"Ägarens svar på motorns fråga: {prod['answer']}")
        return "\n".join(lines)

    def _input_block(self, case: CaseFile, goal: Goal,
                     parent: Optional[ConceptNode], existing: list) -> str:
        parts = []
        identity = self.identity_text(case)
        ideal = self.ideal_text(case)
        is_root = case.context.get("root_goal_id") == goal.id
        if is_root and case.context.get("description"):
            parts.append(f"RUBRIK:\n{case.context['description']}")
        if identity:
            parts.append(f"LÄGESUPPFATTNING (deltagarens egen beskrivning):\n{identity}")
        if ideal:
            parts.append(f"ÖNSKAT LÄGE (idealtillstånd):\n{ideal}")
        product = self.product_block(case)
        if product:
            parts.append(product)
        if not is_root:
            # A hidden root goal only carries the case title; there is no chosen sentence yet.
            parts.append(f"VALT SPÅR (en mening):\n{goal.desired_direction}")
        if parent is not None:
            parts.append(f"VALD PUNKT UR SPÅRET:\n{parent.title}\n{parent.text}")
        if existing:
            parts.append(self._existing_block(existing))
        return "\n\n".join(parts)

    @staticmethod
    def _existing_block(existing: list, limit: int = 12, snippet: int = 260) -> str:
        """What is already on the level: title and the start of each text, so the
        model can tell WHAT it is and not only what it is called. Kept points
        first, then the newest, capped so the prompt stays bounded."""
        ranked = sorted(existing, key=lambda n: n.timestamp, reverse=True)
        ranked = sorted(ranked, key=lambda n: n.status != CONCEPT_ACTIVE)[:limit]
        lines = []
        for n in ranked:
            text = " ".join(n.text.split())
            text = text[:snippet] + ("..." if len(text) > snippet else "")
            lines.append(f"- {n.title}: {text}" if text else f"- {n.title}")
        return "DET SOM REDAN FINNS PÅ DEN HÄR NIVÅN (upprepa inte):\n" + "\n".join(lines)

    # --- One run -----------------------------------------------------------

    def _ask(self, user: str, count: int, label: str) -> list:
        """One model call that returns points as [{"title", "text"}]; [] on failure."""
        started = time.time()
        try:
            response = self._ai.client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "system", "content": SYSTEM_PROMPT},
                          {"role": "user", "content": user}],
                max_completion_tokens=MAX_COMPLETION_TOKENS,
            )
            log_ai(log, label, started, response)
            data = _clean_json(response.choices[0].message.content)
            points = []
            for p in data.get("points", []):
                title = str(p.get("title", "")).strip()
                # Two fields are asked for so the core idea cannot be skipped; they are
                # stored as one plain text with a blank line between (decision: ren text).
                core = str(p.get("core", "")).strip()
                reasoning = str(p.get("reasoning", "")).strip()
                text = (f"{core}\n\n{reasoning}" if core and reasoning
                        else core or reasoning or str(p.get("text", "")).strip())
                if title and text:
                    points.append({"title": title, "text": text})
            return points[:count]
        except Exception as e:
            log_ai(log, label, started, error=e)
            return []

    @staticmethod
    def _angle_line(angle: str) -> str:
        angle = (angle or "").strip()
        return f"\n\nÄGARENS VINKEL (låt den väga tungt): {angle}" if angle else ""

    def generate(self, case: CaseFile, goal: Goal, parent: Optional[ConceptNode],
                 mode: str, lens_id: str = "", exclude_existing: bool = True,
                 count: int = POINTS_PER_RUN, angle: str = "") -> list:
        """One run. Returns a list of {"title", "text"}; [] on failure.
        `count` is how many points to ask for. Existing points on the level
        (including set-aside ones) are shown to the model, with the start of
        their text, so it does not repeat them. When something exists, variation
        is asked for in terms of a different mechanism, not different wording."""
        count = max(1, min(count, POINTS_PER_RUN))
        if not self._ai.client:
            return []
        if mode not in MODE_INSTRUCTIONS:
            mode = CONCEPT_MODE_SPLIT

        existing = []
        if exclude_existing:
            parent_id = parent.id if parent else None
            existing = case.concepts_under(goal.id, parent_id)

        instruction = MODE_INSTRUCTIONS[mode]
        if mode == CONCEPT_MODE_VARY and existing:
            instruction = VARY_BY_MECHANISM

        lens_line = ""
        lens = LENSES.get(lens_id)
        if lens:
            lens_line = (f"\n\nLäs underlaget genom denna lins: {lens['name']}. "
                         f"{lens['instruction']}")

        user = (
            self._input_block(case, goal, parent, existing)
            + "\n\n" + instruction + lens_line + self._angle_line(angle)
            + "\n\n" + output_format(count)
        )
        return self._ask(user, count, f"generate (lens={lens_id or '-'})")

    def vary_from(self, case: CaseFile, goal: Goal, parent: Optional[ConceptNode],
                  node: ConceptNode, angle: str = "", count: int = POINTS_PER_RUN) -> list:
        """Variations of one proposal: the same intent, a different mechanism.
        The other points on the level are shown so the variants avoid them too."""
        count = max(1, min(count, POINTS_PER_RUN))
        if not self._ai.client:
            return []
        others = [n for n in case.concepts_under(goal.id, node.parent_id) if n.id != node.id]
        user = (
            self._input_block(case, goal, parent, others)
            + f"\n\nFÖRSLAG ATT VARIERA:\n{node.title}\n{node.text}"
            + "\n\nGe varianter av förslaget ovan. De ska behålla avsikten bakom det, men skilja sig i MEKANISM "
              "från förslaget, från de övriga befintliga och från varandra. Det räcker inte att byta ord eller "
              f"betoning. Låt varje variant skilja sig längs minst tre av dessa axlar: {AXES}."
            + self._angle_line(angle)
            + "\n\n" + output_format(count)
        )
        return self._ask(user, count, "vary_from")

    def strengthen(self, case: CaseFile, goal: Goal, parent: Optional[ConceptNode],
                   node: ConceptNode, direction: str = "") -> Optional[dict]:
        """
        Förstärk: make one proposal more concrete, one step closer to something
        that can be carried out or measured, without changing its intent. Returns
        a draft the owner decides on:
          {"text", "spec": {goal, done, actor, first_step}, "missing"}
        or None on failure. Spec parts are only filled in when they can be derived
        from the text and the owner's description; an empty part is better than a guess.
        """
        if not self._ai.client:
            return None
        direction = (direction or "").strip()
        user = (
            self._input_block(case, goal, parent, [])
            + f"\n\nFÖRSLAG ATT FÖRSTÄRKA:\n{node.title}\n{node.text}"
            + (f"\n\nÄGARENS RIKTNING (låt den väga tungt): {direction}" if direction else "")
            + """

Förstärk förslaget: gör det konkretare och tydligare, ett steg närmare något som går att utföra eller mäta. \
Behåll avsikten och lägg inte till nya idéer. Skriv om "core" och "reasoning" i samma form som förut \
(kärnan först, sedan motiveringen), men mer konkret: vem gör vad, i vilken form och vad som faktiskt skulle ändras. \
Hitta inte på siffror, namn eller belägg.

Om förslaget är för övergripande för att ha ett riktigt första steg eller ett mätbart mål \
(det beskriver ett helt system eller en hel idé), lämna då spec-delarna tomma och skriv i "missing" \
att det behöver delas upp först. Låtsas inte att något är konkret.

Fyll i "spec" bara de delar som går att härleda. Lämna en del tom hellre än att gissa:
- goal: målet i en mening
- done: hur man ser att det är nått (något observerbart)
- actor: vem som gör det
- first_step: en första aktivitet som går att starta
"missing": en mening om vad som fortfarande är otydligt.

Svara ENDAST med ett JSON-objekt:
{
  "core": "...",
  "reasoning": "...",
  "spec": {"goal": "", "done": "", "actor": "", "first_step": ""},
  "missing": "..."
}"""
        )
        started = time.time()
        try:
            response = self._ai.client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "system", "content": SYSTEM_PROMPT},
                          {"role": "user", "content": user}],
                max_completion_tokens=MAX_COMPLETION_TOKENS,
            )
            log_ai(log, "strengthen", started, response)
            data = _clean_json(response.choices[0].message.content)
            core = str(data.get("core", "")).strip()
            reasoning = str(data.get("reasoning", "")).strip()
            text = f"{core}\n\n{reasoning}" if core and reasoning else core or reasoning
            if not text:
                return None
            spec = data.get("spec") if isinstance(data.get("spec"), dict) else {}
            return {
                "text": text,
                "spec": {k: str(spec.get(k, "")).strip() for k in ("goal", "done", "actor", "first_step")},
                "missing": str(data.get("missing", "")).strip(),
            }
        except Exception as e:
            log_ai(log, "strengthen", started, error=e)
            return None

    # --- End product -------------------------------------------------------

    def infer_product(self, case: CaseFile, answer: str = "") -> Optional[dict]:
        """
        Work out what the owner is really aiming for from the two texts: what exists when
        the desired state is reached (end_state) and what can be produced from here to get
        closer (deliverable: code, documents, a plan ...). It also says how sure it is, how
        big the thing is, other plausible readings and, when it matters, one question.
        Returns a dict (see _read_product) or None on failure. Nothing here is trusted
        blindly: the result is shown to the owner, who can change it.
        """
        if not self._ai.client:
            return None
        identity, ideal = self.identity_text(case)[:3500], self.ideal_text(case)[:3500]
        if not identity and not ideal:
            return None
        parts = []
        if case.context.get("description"):
            parts.append(f"RUBRIK:\n{case.context['description']}")
        parts.append(f"LÄGESUPPFATTNING:\n{identity or '(ingen)'}")
        parts.append(f"ÖNSKAT LÄGE:\n{ideal or '(inget)'}")
        if answer.strip():
            parts.append(f"ÄGARENS SVAR PÅ MOTORNS FRÅGA:\n{answer.strip()[:1000]}")
        parts.append("""Vad är den konkreta slutprodukten som deltagaren siktar mot? Vad finns i världen när det önskade läget är nått, \
och vad kan man faktiskt framställa härifrån för att komma närmare (till exempel kod, dokument, material, en plan)? \
Hitta inte på: texten kan vara kort, och då ska säkerheten vara låg.
"question": tom om du är säker och de andra tolkningarna liknar varandra. Annars en enda fråga som skulle avgöra saken. \
Frågan är obligatorisk om säkerheten är låg eller om tolkningarna skiljer sig i art och inte bara i detaljer.

Svara ENDAST med JSON:
{"end_state": "en mening: vad som finns när det är nått",
 "deliverable": "en mening: vad som kan framställas härifrån",
 "kind": "fri text, 1-3 ord",
 "scale": "liten | medel | stor",
 "confidence": "hög | medel | låg",
 "evidence": "kort: vad i texten stödjer det (högst 8 ord)",
 "alternatives": ["andra rimliga tolkningar, högst 3"],
 "question": ""}""")
        system = ("Du hjälper en motor att förstå vad en deltagare egentligen siktar mot. "
                  "Svara endast med JSON. Svara på samma språk som deltagarens text.")
        for attempt in (1, 2):
            started = time.time()
            try:
                response = self._ai.client.chat.completions.create(
                    model=MODEL,
                    messages=[{"role": "system", "content": system},
                              {"role": "user", "content": "\n\n".join(parts)}],
                    max_completion_tokens=GROUP_MAX_COMPLETION_TOKENS,
                )
                log_ai(log, "product", started, response, attempt=attempt)
                prod = self._read_product(_clean_json(response.choices[0].message.content))
                if answer.strip():
                    prod["answer"] = answer.strip()[:1000]
                return prod
            except Exception as e:
                log_ai(log, "product", started, error=e, attempt=attempt)
        return None

    @staticmethod
    def _read_product(data: dict) -> dict:
        """Validate and normalise the model's answer."""
        def text(key, limit):
            return str(data.get(key, "") or "").strip()[:limit]
        end_state, deliverable = text("end_state", 400), text("deliverable", 400)
        if not end_state or not deliverable:
            raise ValueError("end_state/deliverable missing")
        scale = {"small": "liten", "medium": "medel", "large": "stor", "big": "stor"}.get(
            text("scale", 20).lower(), text("scale", 20).lower())
        if scale not in ("liten", "medel", "stor"):
            scale = "medel"
        conf = {"high": "hög", "medium": "medel", "low": "låg"}.get(
            text("confidence", 20).lower(), text("confidence", 20).lower())
        if conf not in ("hög", "medel", "låg"):
            conf = "medel"
        alts = [str(a).strip()[:200] for a in (data.get("alternatives") or []) if str(a).strip()][:3]
        question = text("question", 300)
        if conf == "låg" and not question:
            question = t("product_default_question")
        return {"end_state": end_state, "deliverable": deliverable, "kind": text("kind", 40),
                "scale": scale, "confidence": conf, "evidence": text("evidence", 200),
                "alternatives": alts, "question": question, "source": "ai", "answer": ""}

    # --- Start list --------------------------------------------------------

    def collect_actions(self, case: CaseFile, goal: Goal, nodes: list, decided: list) -> Optional[dict]:
        """
        Look at the whole picture, the owner's description of the situation and of the
        desired state plus every kept point in the tree, and propose concrete things to
        start with, in two layers:
          base   what must be done before anyone can start at all. This comes from the
                 situation and the desired state, not from the points, which is why it
                 has to be asked for explicitly (measured: without it the model only
                 returned design artefacts).
          points shared prerequisites for several points, in dependency order.

        `nodes` are the kept points; `decided` are titles of actions the owner already
        accepted, so they are not proposed again. Returns
          {"actions": [{"title","done_when","layer","serves": [node ids],"needs": [indexes],"first"}],
           "assumptions": [str]}
        or None on failure. Which points have no concrete action is worked out by the
        caller from `serves`, not taken from the model's word.
        """
        if not self._ai.client:
            return None
        by_label = {f"N{i + 1}": n for i, n in enumerate(nodes)}
        ids = {n.id: label for label, n in by_label.items()}

        def depth(n):
            d, seen = 1, {n.id}
            while n.parent_id and n.parent_id not in seen:
                parent = case.get_concept(n.parent_id)
                if parent is None:
                    break
                seen.add(parent.id)
                n, d = parent, d + 1
            return d

        tree_lines = []
        for label, n in by_label.items():
            parent = f", under {ids[n.parent_id]}" if n.parent_id in ids else ""
            tree_lines.append(f"{label} {n.title} (nivå {depth(n)}{parent})")
            for key in ("goal", "first_step"):
                if (n.spec.get(key) or "").strip():
                    tree_lines.append(f"    {key}: {n.spec[key][:240]}")
        parts = []
        if case.context.get("description"):
            parts.append(f"RUBRIK:\n{case.context['description']}")
        parts.append(f"LÄGESUPPFATTNING:\n{self.identity_text(case)[:4000]}")
        parts.append(f"ÖNSKAT LÄGE:\n{self.ideal_text(case)[:4000]}")
        product = self.product_block(case)
        if product:
            parts.append(product)
        parts.append("BEHÅLLNA PUNKTER I TRÄDET:\n" + ("\n".join(tree_lines) if tree_lines else
                     "(inga. Det här är en liten sak som går direkt till handlingar; skriv bara grundlagret.)"))
        if decided:
            parts.append("REDAN BESLUTADE HANDLINGAR (föreslå dem inte igen):\n" + "\n".join(f"- {t}" for t in decided))
        parts.append("""Samla en startlista i två lager.
GRUND: 1-3 handlingar som måste vara gjorda för att någon över huvud taget ska kunna börja arbeta mot det önskade läget, \
utifrån lägesuppfattningen och det önskade läget. Ta med dem även om ingen punkt nämner dem. De ska passa det som beskrivs; \
hitta inte på vad ärendet handlar om. Skriv dem som en kort handling, utan "kontrollera ... annars".
FRÅN PUNKTERNA: högst 6 handlingar som är gemensamma förutsättningar för flera punkter, ordnade efter beroenden. \
Hellre en handling som tjänar flera punkter än en per punkt.
Peka ut EN första handling. För varje handling: vilka punkter den tjänar (N-id, tom lista för en grundhandling) och vilka \
andra handlingar som ska vara gjorda först (A-id).
Om en punkt är för övergripande för att ha någon görbar handling, låt den vara utan.
Lista dina antaganden.

Svara ENDAST med JSON:
{"first": "A1", "actions": [{"id": "A1", "layer": "base|points", "title": "...", "done_when": "...", "serves": ["N1"], "needs": []}], "assumptions": ["..."]}""")
        user = "\n\n".join(parts)

        for attempt in (1, 2):
            started = time.time()
            try:
                response = self._ai.client.chat.completions.create(
                    model=MODEL,
                    messages=[{"role": "system", "content": ACTIONS_SYSTEM_PROMPT},
                              {"role": "user", "content": user}],
                    max_completion_tokens=GROUP_MAX_COMPLETION_TOKENS,
                )
                log_ai(log, "actions", started, response, attempt=attempt, points=len(nodes))
                data = _clean_json(response.choices[0].message.content)
                return self._read_actions(data, by_label)
            except Exception as e:
                log_ai(log, "actions", started, error=e, attempt=attempt)
        return None

    @staticmethod
    def _read_actions(data: dict, by_label: dict) -> dict:
        """Validate the model's answer. Unknown ids are dropped, order is kept, and at
        most ACTIONS_MAX_TOTAL actions are used."""
        raw = [a for a in data.get("actions", []) if isinstance(a, dict)]
        items, index = [], {}
        for a in raw:
            title = str(a.get("title", "")).strip()[:ACTION_MAX_TITLE]
            if not title or len(items) >= ACTIONS_MAX_TOTAL:
                continue
            layer = "base" if str(a.get("layer", "")).strip().lower() == "base" else "points"
            serves = []
            for label in a.get("serves", []) or []:
                node = by_label.get(str(label).strip().upper())
                if node and node.id not in serves:
                    serves.append(node.id)
            if layer == "base":
                serves = []  # a base action is for the whole case, not for single points
            index[str(a.get("id", "")).strip().upper()] = len(items)
            items.append({"title": title, "done_when": str(a.get("done_when", "")).strip()[:ACTION_MAX_DONE],
                          "layer": layer, "serves": serves, "needs_raw": a.get("needs", []) or [], "first": False})
        if not items:
            raise ValueError("no actions in the answer")
        for it in items:
            it["needs"] = sorted({index[str(n).strip().upper()] for n in it.pop("needs_raw")
                                  if str(n).strip().upper() in index})
        # no self-reference, and no cycles: a need must point to an earlier action
        for i, it in enumerate(items):
            it["needs"] = [j for j in it["needs"] if j < i]
        first = index.get(str(data.get("first", "")).strip().upper(), 0)
        items[first]["first"] = True
        assumptions = [str(x).strip() for x in (data.get("assumptions") or []) if str(x).strip()][:6]
        return {"actions": items, "assumptions": assumptions}

    # --- Deep mode ---------------------------------------------------------

    def deep(self, case: CaseFile, goal: Goal, parent: Optional[ConceptNode],
             lens_ids: list, mode: str, angle: str = "") -> dict:
        """
        Several runs, each through its own lens, run in parallel. Every run sees
        what already exists on the level and is asked to differ from it in
        mechanism, and asks for DEEP_POINTS_PER_LENS points only. The points are then
        collected into at most MAX_THEMES themes by the model (it only decides what
        belongs together and picks one representative per theme). How many lenses a
        theme appears in is counted in code and gives "stable" or "variant".

        Returns:
          {
            "themes": [{"name","title","text","lens","seen_in","stability",
                        "others": [{"title","text","lens"}]}],  # at most MAX_THEMES
            "overflow": [{"title","text","lens"}],  # points from themes beyond the limit
            "points": int,  # raw points produced by all runs
            "runs_ok": int, "runs_total": int, "clustered": bool, "group_error": str,
          }
        """
        lens_ids = [l for l in dict.fromkeys(lens_ids) if l in LENSES][:MAX_LENSES]
        result = {"themes": [], "overflow": [], "points": 0, "runs_ok": 0,
                  "runs_total": len(lens_ids), "clustered": False, "group_error": ""}
        if not lens_ids or not self._ai.client:
            return result

        # Runs are independent, so they can go in parallel.
        with ThreadPoolExecutor(max_workers=len(lens_ids)) as pool:
            futures = [(l, pool.submit(self.generate, case, goal, parent, mode, l, True,
                                       DEEP_POINTS_PER_LENS, angle))
                       for l in lens_ids]
            runs = [(l, f.result()) for l, f in futures]

        points = []  # flat list: {"lens","title","text","pos"}
        ok_lenses = []
        for lens_id, pts in runs:
            if pts:
                ok_lenses.append(lens_id)
                for pos, p in enumerate(pts):
                    points.append({"lens": lens_id, "pos": pos, **p})
        result["runs_ok"] = len(ok_lenses)
        result["points"] = len(points)
        if not points:
            return result

        themes, clustered, group_error = self._themes(points, MAX_THEMES)
        result["clustered"] = clustered
        result["group_error"] = group_error
        threshold = stability_threshold(len(ok_lenses))

        built = []
        for th in themes:
            members = [points[i] for i in th["points"]]
            if not members:
                continue
            rep = points[th["rep"]] if th["rep"] is not None else members[0]
            seen = [l for l in ok_lenses if any(m["lens"] == l for m in members)]
            # Without grouping, "seen in one lens" says nothing, so no stability is claimed.
            stability = ("" if not clustered
                         else "stable" if len(seen) >= threshold else "variant")
            built.append({
                "name": th["name"], "title": rep["title"], "text": rep["text"], "lens": rep["lens"],
                "seen_in": seen, "stability": stability,
                "others": [{"title": m["title"], "text": m["text"], "lens": m["lens"]}
                           for m in members if m is not rep],
            })

        # Themes seen in the most lenses first; then by size. The rest are kept but not shown.
        built.sort(key=lambda t: (-len(t["seen_in"]), -len(t["others"])))
        result["themes"] = built[:MAX_THEMES]
        for t in built[MAX_THEMES:]:
            result["overflow"] += [{"title": t["title"], "text": t["text"], "lens": t["lens"]}] + t["others"]
        return result

    def themes_of(self, nodes: list, max_themes: int):
        """Collect points that already exist (open proposals) into at most `max_themes`
        themes. Returns (themes, clustered, error); each theme is
        {"name", "points": [indexes into nodes], "rep": index into nodes}."""
        points = [{"lens": n.lens, "title": n.title, "text": n.text, "pos": i}
                  for i, n in enumerate(nodes)]
        return self._themes(points, max_themes)

    def _themes(self, points: list, max_themes: int):
        """
        Collect points into at most `max_themes` themes (a theme = a shared direction or
        mechanism). Returns (themes, clustered, error); each theme is
        {"name": str, "points": [indexes], "rep": index}.
        The call is tried GROUP_ATTEMPTS times. If it still fails, every point becomes its
        own theme (taken in turns across lenses so each lens is represented), clustered is
        False and error says why. The error is shown to the owner and written to the case
        history, so the cause can be found.
        """
        def singles():
            order = sorted(range(len(points)), key=lambda i: (points[i]["pos"], i))
            return [{"name": "", "points": [i], "rep": i} for i in order]

        if len(points) < 2:
            return singles(), True, ""  # nothing to group
        if not self._ai.client:
            return singles(), False, "no AI client"

        lines = []
        for i, p in enumerate(points):
            lens_name = LENSES.get(p["lens"], {}).get("name", p["lens"] or "ingen")
            lines.append(f"P{i + 1} (lins: {lens_name}) {p['title']} - {p['text'][:350]}")

        prompt = (
            f"Nedan finns punkter från flera körningar. Samla dem i exakt {max_themes} teman "
            f"(färre bara om det finns färre än {max_themes} punkter). "
            "Ett tema är en gemensam riktning eller mekanism: punkter i samma tema liknar varandra mer än "
            "de liknar punkter i andra teman. Försök få teman av ungefär samma storlek. Bilda inte teman "
            "av punkter som inte hör ihop. Om punkterna naturligt bildar färre riktningar, dela det största "
            "temat efter den mest meningsfulla skillnaden mellan dess punkter. Varje punkt ska ligga i "
            "exakt ett tema. Ge varje tema ett kort namn (2-4 ord) och peka ut 'rep', den punkt som bäst "
            "representerar temat.\n\n"
            + "\n".join(lines)
            + '\n\nSvara ENDAST med JSON: {"themes": [{"name": "...", "items": ["P1","P4"], "rep": "P1"}]}'
        )
        data, error = None, ""
        for attempt in range(1, GROUP_ATTEMPTS + 1):
            finish = "?"
            started = time.time()
            try:
                response = self._ai.client.chat.completions.create(
                    model=MODEL,
                    messages=[{"role": "system",
                               "content": "Du sorterar texter i teman. Svara endast med JSON."},
                              {"role": "user", "content": prompt}],
                    max_completion_tokens=GROUP_MAX_COMPLETION_TOKENS,
                )
                finish = getattr(response.choices[0], "finish_reason", "?")
                log_ai(log, "themes", started, response, attempt=attempt, points=len(points))
                data = _clean_json(response.choices[0].message.content)
                if not isinstance(data, dict):
                    raise ValueError("answer is not a JSON object")
                break
            except Exception as e:
                data = None
                error = f"{type(e).__name__}: {str(e)[:160]} (finish_reason={finish}, attempt {attempt}/{GROUP_ATTEMPTS})"
                log.warning("themes failed: %s", error)
        if data is None:
            return singles(), False, error

        themes, used = [], set()
        for raw in data.get("themes", []):
            th = {"name": str(raw.get("name", "")).strip()[:60], "points": [], "rep": None}
            for item in raw.get("items", []):
                item = str(item).strip().upper()
                if item[:1] == "P" and item[1:].isdigit():
                    i = int(item[1:]) - 1
                    if 0 <= i < len(points) and i not in used:
                        used.add(i)
                        th["points"].append(i)
            rep = str(raw.get("rep", "")).strip().upper()
            if rep[:1] == "P" and rep[1:].isdigit() and int(rep[1:]) - 1 in th["points"]:
                th["rep"] = int(rep[1:]) - 1
            if th["rep"] is None and th["points"]:
                th["rep"] = th["points"][0]
            if th["points"]:
                themes.append(th)

        # Anything the model left out becomes its own theme (and may end up over the limit).
        for i in range(len(points)):
            if i not in used:
                themes.append({"name": "", "points": [i], "rep": i})
        return themes, True, ""
