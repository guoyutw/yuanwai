#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from yuanwai_simulator import AIInference, Case, Fact, Simulator

def base_result(**overrides):
    data = {
        "facts": [],
        "commitment_request": False,
        "conflict": False,
        "reference": False,
        "supplier_ready": False,
        "primary_next_action": "ask",
        "model_requires_human_gate": False,
        "guardrail": "",
        "decision_type": "",
        "decision_request": "",
        "unknowns": [],
        "conflicts": [],
    }
    data.update(overrides)
    return data

def current_case():
    c = Case()
    c.facts = [
        Fact("service_form", "stated", "s", value="歐式自助餐", status="CURRENT"),
        Fact("date", "stated", "d", value="12/18", status="CURRENT"),
        Fact("time", "stated", "t", value="11:30", status="CURRENT"),
        Fact("location", "stated", "l", value="大溪區", status="CURRENT"),
    ]
    return c

def main():
    ai = AIInference(False)

    r = ai.postprocess_obvious_facts(
        "12／19",
        base_result(unknowns=["date", "time", "service_form"]),
        current_case(),
    )
    assert next(f["value"] for f in r["facts"] if f["topic"] == "date") == "12/19"
    assert "date" not in r["unknowns"]
    assert "service_form" not in r["unknowns"]

    c = Case()
    r = ai.postprocess_obvious_facts(
        "11:30要到公司",
        base_result(
            facts=[
                {"topic": "time", "value_class": "stated", "value": "11:30要到公司"},
                {"topic": "location", "value_class": "stated", "value": "公司"},
            ],
            unknowns=["location"],
        ),
        c,
    )
    assert next(f["value"] for f in r["facts"] if f["topic"] == "time") == "11:30"
    assert not any(f["topic"] == "location" for f in r["facts"])
    assert r["unknowns"][0] == "location"

    r = ai.postprocess_obvious_facts(
        "可以給我有龍蝦的菜單，跟沒有龍蝦的菜單嗎？",
        base_result(
            facts=[{"topic": "time", "value_class": "stated", "value": "11:30要到公司"}],
            commitment_request=True,
            model_requires_human_gate=True,
            primary_next_action="human_gate",
            decision_type="fulfillment",
            decision_request="傳送菜單",
            unknowns=["service_form", "date", "time", "location"],
        ),
        current_case(),
    )
    assert next(f["value"] for f in r["facts"] if f["topic"] == "time") == "11:30"
    assert r["reference"] is True
    assert r["commitment_request"] is False
    assert r["model_requires_human_gate"] is False
    assert r["primary_next_action"] == "reference"
    assert r["decision_type"] == ""
    assert r["decision_request"] == ""
    assert r["unknowns"] == []

    s = Simulator(None, True)
    s.case.facts = [Fact("date", "stated", "d", value="12/18", status="CURRENT")]
    changed = ai.postprocess_obvious_facts(
        "改成12/19",
        base_result(
            facts=[{"topic": "date", "value_class": "stated", "value": "12/18"}],
            primary_next_action="recovery",
        ),
        s.case,
    )
    s.ai.interpret = lambda text, case: changed
    s.turn("改成12/19")
    assert any(f.topic == "date" and f.status == "SUPERSEDED" and f.value == "12/18" for f in s.case.facts)
    assert any(f.topic == "date" and f.status == "CURRENT" and f.value == "12/19" for f in s.case.facts)
    assert s.case.lifecycle == "CHANGED/RECOVERY"

    s = Simulator(None, True)
    s.case.facts = [Fact("menu_preferences", "stated", "m", value="無龍蝦", status="CURRENT")]
    s.ai.interpret = lambda text, case: base_result(
        facts=[{"topic": "menu_preferences", "value_class": "stated", "value": "有龍蝦與無龍蝦兩種"}],
        reference=True,
        primary_next_action="reference",
    )
    reply = s.turn("想比較兩種菜單")
    assert s.case.lifecycle == "OPTIONS"
    assert s.case.next_action == "reference"
    assert reply.startswith("可提供")
    assert not any(e.get("invalidation") for e in s.case.events)

    print("replay_understanding_regression: PASS")

if __name__ == "__main__":
    main()
