"""
Minimal internationalisation (i18n) layer.

Usage:
    from i18n import t, set_language
    set_language("sv")
    t("onboarding_title")            # -> "Vad jobbar vi med?"
    t("welcome", name="Zebra")       # -> "Välkommen till Zebra!"

Design:
- One flat dict of string keys per language.
- t(key, **kwargs) returns the string for the current language, formatting
  any placeholders. Falls back to English, then to the key itself.
- Language is a module-level setting; set it once at startup.

This is deliberately simple. No gettext, no .po files. Add languages by
adding a new dict to TRANSLATIONS.
"""

DEFAULT_LANGUAGE = "sv"
_current_language = DEFAULT_LANGUAGE


TRANSLATIONS = {
    "en": {
        # onboarding
        "onboarding_title": "What are we working on?",
        "onboarding_help": "Describe what you want to improve, change, or explore.<br>One sentence is enough.",
        "onboarding_placeholder": "I want to...",
        "onboarding_go": "Let's go",
        # directions
        "directions_fallback_title": "Choose a direction",
        "directions_title": "Choose a direction",
        "directions_intro": "Based on what you said, here are some paths we could explore:",
        # name case
        "name_title": "Name your journey",
        "name_help": "A creative name makes it yours. Pick one or write your own.",
        "name_own": "Or write your own:",
        "name_own_placeholder": "My own name...",
        "name_go": "Let's go!",
        # tree
        "tree_fallback_title": "Overview",
        "nav_overview": "Overview",
        "progress_goals": "{n} goals",
        "progress_missions_done": "{n} missions done",
        "progress_observations": "{n} observations",
        "tree_missions_count": "{done}/{total} missions",
        "tree_active_suffix": "{n} active",
        "tree_no_missions": "No missions yet",
        "add_goal_title": "Add Goal",
        "add_goal_placeholder": "What direction or desired change?",
        "add_goal_button": "Add Goal",
        "all_done_title": "All goals done!",
        "all_done_help": "Is everything finished — or shall we find new goals based on where you are now?",
        "all_done_new": "Suggest new goals",
        "flash_new_goals": "{n} new goals added.",
        # goal detail
        "back_all_goals": "All goals",
        "status_label": "Status",
        "progress_goal_set": "Goal set",
        "progress_missions": "{done}/{total} missions",
        "progress_active_mission": "Active mission",
        "missions_title": "Missions",
        "mission_result_placeholder": "What happened? What did you learn?",
        "mark_done": "Mark done",
        "observations_title": "Observations",
        "get_suggestions": "Get new suggestions",
        "mark_goal_done": "Mark goal done",
        "give_up": "Give up",
        # observer
        "observer_says": "{name} says:",
        "observer_meta": "A perspective, not a decision. You decide what matters.",
        # proposal
        "proposal_title": "Proposal",
        "proposal_fallback": "Proposal",
        "proposal_suggestion": "Suggestion",
        "proposal_reason": "Reason",
        "proposal_mission": "Mission",
        "proposal_done_when": "Done when:",
        "accept": "Accept",
        "reject": "Reject",
        "explore_further": "Explore Further",
        "modify_placeholder": "Or modify: write your version here...",
        "modify_accept": "Modify & Accept",
        # suggestions
        "choose_next": "Choose next step",
        "possible_directions": "{n} possible directions:",
        "choose_this": "Choose this",
        # flash messages
        "flash_goal_not_found": "Goal not found.",
        "flash_describe": "Please describe what you're working on.",
        "flash_directions": "Here are some directions we could take:",
        "flash_welcome": "Welcome to {name}!",
        "flash_choose_direction": "Choose a direction:",
        "flash_proposal_for": "Proposal for: {title}",
        "flash_mission_accepted": "Mission accepted.",
        "flash_mission_modified": "Modified mission created.",
        "flash_rejected": "Rejected. Goal remains.",
        "flash_exploring": "Exploring further:",
        "flash_goal_abandoned": "Goal abandoned.",
        "flash_mission_not_found": "Mission not found.",
        "flash_mission_done": "Mission done!",
        "flash_no_observation": "No observation.",
        "flash_observation_recorded": "Observation recorded.",
        "flash_no_direction": "No direction provided.",
        "flash_goal_added": "Goal added.",
        "flash_goal_completed": "Goal completed!",
    },
    "sv": {
        # onboarding
        "onboarding_title": "Vad jobbar vi med?",
        "onboarding_help": "Beskriv vad du vill förbättra, förändra eller utforska.<br>En mening räcker.",
        "onboarding_placeholder": "Jag vill...",
        "onboarding_go": "Nu kör vi",
        # directions
        "directions_fallback_title": "Välj en riktning",
        "directions_title": "Välj en riktning",
        "directions_intro": "Utifrån det du sa, här är några vägar vi skulle kunna utforska:",
        # name case
        "name_title": "Ge din resa ett namn",
        "name_help": "Ett kreativt namn gör det till ditt. Välj ett eller skriv eget.",
        "name_own": "Eller skriv eget:",
        "name_own_placeholder": "Mitt eget namn...",
        "name_go": "Nu kör vi!",
        # tree
        "tree_fallback_title": "Översikt",
        "nav_overview": "Översikt",
        "progress_goals": "{n} mål",
        "progress_missions_done": "{n} uppdrag klara",
        "progress_observations": "{n} observationer",
        "tree_missions_count": "{done}/{total} uppdrag",
        "tree_active_suffix": "{n} aktiva",
        "tree_no_missions": "Inga uppdrag än",
        "add_goal_title": "Lägg till mål",
        "add_goal_placeholder": "Vilken riktning eller önskad förändring?",
        "add_goal_button": "Lägg till mål",
        "all_done_title": "Alla mål klara!",
        "all_done_help": "Är allt klart nu — eller ska vi ta fram nya mål baserat på var du är nu?",
        "all_done_new": "Föreslå nya mål",
        "flash_new_goals": "{n} nya mål tillagda.",
        # goal detail
        "back_all_goals": "Alla mål",
        "status_label": "Status",
        "progress_goal_set": "Mål satt",
        "progress_missions": "{done}/{total} uppdrag",
        "progress_active_mission": "Aktivt uppdrag",
        "missions_title": "Uppdrag",
        "mission_result_placeholder": "Vad hände? Vad lärde du dig?",
        "mark_done": "Markera klar",
        "observations_title": "Observationer",
        "get_suggestions": "Hämta nya förslag",
        "mark_goal_done": "Markera mål klart",
        "give_up": "Ge upp",
        # observer
        "observer_says": "{name} säger:",
        "observer_meta": "Ett perspektiv, inte ett beslut. Du avgör vad som spelar roll.",
        # proposal
        "proposal_title": "Förslag",
        "proposal_fallback": "Förslag",
        "proposal_suggestion": "Förslag",
        "proposal_reason": "Varför",
        "proposal_mission": "Uppdrag",
        "proposal_done_when": "Klart när:",
        "accept": "Acceptera",
        "reject": "Avvisa",
        "explore_further": "Utforska vidare",
        "modify_placeholder": "Eller ändra: skriv din version här...",
        "modify_accept": "Ändra & acceptera",
        # suggestions
        "choose_next": "Välj nästa steg",
        "possible_directions": "{n} möjliga riktningar:",
        "choose_this": "Välj denna",
        # flash messages
        "flash_goal_not_found": "Målet hittades inte.",
        "flash_describe": "Beskriv vad du jobbar med.",
        "flash_directions": "Här är några riktningar vi skulle kunna ta:",
        "flash_welcome": "Välkommen till {name}!",
        "flash_choose_direction": "Välj en riktning:",
        "flash_proposal_for": "Förslag för: {title}",
        "flash_mission_accepted": "Uppdrag accepterat.",
        "flash_mission_modified": "Ändrat uppdrag skapat.",
        "flash_rejected": "Avvisat. Målet finns kvar.",
        "flash_exploring": "Utforskar vidare:",
        "flash_goal_abandoned": "Målet övergavs.",
        "flash_mission_not_found": "Uppdraget hittades inte.",
        "flash_mission_done": "Uppdrag klart!",
        "flash_no_observation": "Ingen observation.",
        "flash_observation_recorded": "Observation sparad.",
        "flash_no_direction": "Ingen riktning angiven.",
        "flash_goal_added": "Mål tillagt.",
        "flash_goal_completed": "Målet slutfört!",
    },
}


def set_language(lang: str):
    """Set the active language. Falls back to default if unknown."""
    global _current_language
    if lang in TRANSLATIONS:
        _current_language = lang
    else:
        _current_language = DEFAULT_LANGUAGE


def get_language() -> str:
    return _current_language


def t(key: str, **kwargs) -> str:
    """
    Translate a key into the current language.
    Falls back to English, then to the key itself.
    Formats {placeholders} using kwargs.
    """
    lang_dict = TRANSLATIONS.get(_current_language, {})
    text = lang_dict.get(key)
    if text is None:
        text = TRANSLATIONS.get("en", {}).get(key, key)
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass
    return text
