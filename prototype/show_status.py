"""
Show the current status of a Case File and respond to pending missions.

Usage:
    python show_status.py cases/826868e0.json    # show status + prompt for decision
    python show_status.py                        # shows all cases with active missions
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def show_case(filepath, interactive=False):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    name = data.get("context", {}).get("description", "Unnamed")
    case_id = data["id"]
    goals = data.get("goals", [])
    missions = data.get("missions", [])
    observations = data.get("observations", [])

    active_goals = [g for g in goals if g["status"] == "ACTIVE"]
    active_missions = [m for m in missions if m["status"] == "ACTIVE"]

    if not active_missions and not active_goals:
        return False  # nothing pending

    print(f"\n  Case: {name}")
    print(f"  ID:   {case_id}")
    print(f"  File: {filepath}")

    if active_goals:
        print(f"\n  Active goals ({len(active_goals)}):")
        for g in active_goals:
            print(f"    • {g['desired_direction'][:80]}")

    if active_missions:
        print(f"\n  AWAITING DECISION ({len(active_missions)}):")
        for m in active_missions:
            label = m.get("name") or m["id"]
            print(f"\n    Mission: {label} ({m['id']})")
            print(f"    Description: {m['description']}")
            if m.get("purpose"):
                print(f"    Purpose: {m['purpose']}")
            if m.get("definition_of_done"):
                print(f"    Done when:")
                for d in m["definition_of_done"]:
                    print(f"      - {d}")

    print(f"\n  Observations so far: {len(observations)}")
    if observations:
        print(f"  Latest: {observations[-1]['text'][:100]}")

    print()

    # Interactive decision
    if interactive and active_missions:
        for m in active_missions:
            decision = prompt_decision(m)
            if decision:
                record_decision(filepath, data, m, decision)

    return True


def prompt_decision(mission):
    """Prompt the user for a decision on a mission."""
    label = mission.get("name") or mission["id"]
    print("  " + "=" * 50)
    print(f"  What do you decide on mission '{label}'?\n")
    print("    1. ACCEPT")
    print("    2. MODIFY")
    print("    3. REJECT")
    print("    4. EXPLORE FURTHER")
    print("    5. GIVE UP")
    print("    6. Skip (decide later)")
    print()

    try:
        choice = input("  > ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n")
        return None

    decisions = {
        "1": "ACCEPT",
        "2": "MODIFY",
        "3": "REJECT",
        "4": "EXPLORE_FURTHER",
        "5": "GIVE_UP",
        "6": None,
    }

    decision_type = decisions.get(choice)
    if decision_type is None:
        return None

    result = {"decision_type": decision_type, "mission_id": mission["id"]}

    if decision_type == "MODIFY":
        print("\n  How would you modify it?")
        try:
            result["modification"] = input("  > ").strip()
        except (EOFError, KeyboardInterrupt):
            return None

    if decision_type in ("REJECT", "GIVE_UP"):
        print("\n  Reason (optional):")
        try:
            reason = input("  > ").strip()
            if reason:
                result["reason"] = reason
        except (EOFError, KeyboardInterrupt):
            pass

    return result


def record_decision(filepath, data, mission, decision):
    """Record the decision into the case file."""
    decision_type = decision["decision_type"]

    # Add to decisions list
    decision_record = {
        "id": f"d-{datetime.now().strftime('%H%M%S')}",
        "decision_type": decision_type,
        "goal_id": mission.get("goal_id", ""),
        "context": mission["description"][:100],
        "reason": decision.get("reason") or decision.get("modification") or None,
        "timestamp": datetime.now().isoformat(),
    }
    data.setdefault("decisions", []).append(decision_record)

    # Update mission status based on decision
    if decision_type == "ACCEPT":
        mission["status"] = "ACCEPTED"
        print(f"\n  ✓ Mission {mission['id']} ACCEPTED.")
    elif decision_type == "MODIFY":
        mission["status"] = "MODIFIED"
        mission["modification"] = decision.get("modification", "")
        print(f"\n  ✓ Mission {mission['id']} MODIFIED: {decision.get('modification', '')[:60]}")
    elif decision_type == "REJECT":
        mission["status"] = "REJECTED"
        print(f"\n  ✗ Mission {mission['id']} REJECTED.")
    elif decision_type == "GIVE_UP":
        mission["status"] = "ABANDONED"
        # Also mark the goal
        for g in data.get("goals", []):
            if g["id"] == mission.get("goal_id"):
                g["status"] = "ABANDONED"
                g.setdefault("history", []).append({
                    "event": "abandoned",
                    "reason": decision.get("reason", ""),
                    "timestamp": datetime.now().isoformat(),
                })
        print(f"\n  ✗ Mission {mission['id']} — GIVE UP.")
    elif decision_type == "EXPLORE_FURTHER":
        print(f"\n  … Mission {mission['id']} — exploring further.")

    # Add to history
    data.setdefault("history", []).append({
        "event": "decision_recorded",
        "data": decision,
        "timestamp": datetime.now().isoformat(),
    })
    data["updated"] = datetime.now().isoformat()

    # Save
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"  Saved to: {filepath}\n")


def find_case_file(query):
    """Find a case file by name fragment, ID prefix, or full path."""
    path = Path(query)
    if path.exists():
        return str(path)

    # Search in cases/ directory
    cases_dir = Path("cases")
    if not cases_dir.exists():
        return None

    query_lower = query.lower()
    for f in sorted(cases_dir.glob("*.json")):
        # Match by ID prefix
        if f.stem.startswith(query_lower):
            return str(f)
        # Match by name/description
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            name = data.get("context", {}).get("description", "").lower()
            if query_lower in name:
                return str(f)
        except (json.JSONDecodeError, OSError):
            continue

    return None


def main():
    if len(sys.argv) > 1:
        query = sys.argv[1]
        filepath = find_case_file(query)
        if filepath is None:
            print(f"\n  No case file matching '{query}' found.")
            print(f"  Try: a name fragment, an ID prefix, or a full path.\n")
            sys.exit(1)
        show_case(filepath, interactive=True)
        return

    # Show all cases with active missions
    cases_dir = Path("cases")
    if not cases_dir.exists():
        print("  No cases/ directory found.")
        return

    print("\n  === CASES WITH PENDING MISSIONS ===")
    found = False
    for f in sorted(cases_dir.glob("*.json")):
        if show_case(str(f), interactive=False):
            found = True

    if not found:
        print("\n  No cases with active missions.\n")
    else:
        print("  Run with a specific case file to make a decision:")
        print("  python show_status.py cases/<id>.json\n")


if __name__ == "__main__":
    main()
