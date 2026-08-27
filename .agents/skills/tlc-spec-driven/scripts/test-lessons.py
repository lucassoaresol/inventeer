#!/usr/bin/env python3

import json
import pathlib
import subprocess
import sys
import tempfile


def run(*args: str, expect: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(SUBJECT), "--root", str(ROOT), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != expect:
        raise AssertionError(
            f"expected exit {expect}, got {result.returncode}: {result.stdout}{result.stderr}"
        )
    return result


SUBJECT = pathlib.Path(__file__).with_name("lessons.py")

with tempfile.TemporaryDirectory(prefix="test-tlc-lessons.") as temp_dir:
    ROOT = pathlib.Path(temp_dir)
    run("init")
    run(
        "add",
        "--feature",
        "review-lifecycle",
        "--signal",
        "review_finding",
        "--source",
        "validation.md:confirmed-review-R1",
        "--text",
        "Bind validation evidence to the exact reviewed head before promotion.",
        "--scope",
        "delivery",
    )

    data = json.loads((ROOT / ".specs" / "lessons.json").read_text(encoding="utf-8"))
    assert len(data["lessons"]) == 1
    lesson = data["lessons"][0]
    assert lesson["signal"] == "review_finding"
    assert lesson["features"] == ["review-lifecycle"]
    assert lesson["evidence"] == ["validation.md:confirmed-review-R1 (delivery)"]
    print("ok 1 - records an independently confirmed external review finding")

    run(
        "add",
        "--feature",
        "ungrounded-review",
        "--signal",
        "review_finding",
        "--source",
        "",
        "--text",
        "Do not accept an ungrounded external review opinion as a project lesson.",
        expect=2,
    )
    unchanged = json.loads((ROOT / ".specs" / "lessons.json").read_text(encoding="utf-8"))
    assert len(unchanged["lessons"]) == 1
    print("ok 2 - rejects an ungrounded external review opinion")

    # --- Segundo eixo de merge: similaridade de token-set --------------------
    # Exigir texto normalizado idêntico é o motivo de a recorrência quase nunca subir: a mesma
    # lição reescrita em outra feature entrava como uma lição nova.

    run(
        "add",
        "--feature",
        "reworded-feature",
        "--signal",
        "review_finding",
        "--source",
        "validation.md:R7",
        "--text",
        "Bind the validation evidence to the exact reviewed head commit before promotion.",
    )
    data = json.loads((ROOT / ".specs" / "lessons.json").read_text(encoding="utf-8"))
    assert len(data["lessons"]) == 1, f"reworded lesson forked a new id: {data['lessons']}"
    merged = data["lessons"][0]
    assert merged["recurrence"] == 2, merged["recurrence"]
    assert merged["status"] == "confirmed", merged["status"]
    assert merged["features"] == ["review-lifecycle", "reworded-feature"], merged["features"]
    assert merged["text"] == "Bind validation evidence to the exact reviewed head before promotion.", (
        "the stored phrasing must stay authoritative"
    )
    assert "validation.md:R7" in merged["evidence"], merged["evidence"]
    print("ok 3 - a reworded restatement merges, promotes, and keeps the stored text")

    run(
        "add",
        "--feature",
        "unrelated-feature",
        "--signal",
        "review_finding",
        "--source",
        "validation.md:R9",
        "--text",
        "Apply a visually hidden utility to a wrapper element rather than a table.",
    )
    data = json.loads((ROOT / ".specs" / "lessons.json").read_text(encoding="utf-8"))
    assert len(data["lessons"]) == 2, "an unrelated same-signal lesson must stay separate"
    print("ok 4 - an unrelated lesson sharing the signal stays separate")

    # O sinal é o que ancora a lição numa falha de verificação; texto idêntico sob outro sinal
    # descreve outra falha.
    run(
        "add",
        "--feature",
        "other-signal",
        "--signal",
        "gate_fail",
        "--source",
        "validation.md:G1",
        "--text",
        "Bind validation evidence to the exact reviewed head before promotion.",
    )
    data = json.loads((ROOT / ".specs" / "lessons.json").read_text(encoding="utf-8"))
    assert len(data["lessons"]) == 3, "identical text under a different signal must not merge"
    print("ok 5 - different signals never merge, even on identical text")

    # Limiar 1.0 reduz o comportamento ao merge exato anterior.
    store = ROOT / ".specs" / "lessons.json"
    data = json.loads(store.read_text(encoding="utf-8"))
    data["merge_similarity"] = 1.0
    store.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    run(
        "add",
        "--feature",
        "exact-only-feature",
        "--signal",
        "review_finding",
        "--source",
        "validation.md:R11",
        "--text",
        "Bind the validation evidence to the exact reviewed head commit before promotion now.",
    )
    data = json.loads(store.read_text(encoding="utf-8"))
    assert len(data["lessons"]) == 4, "threshold 1.0 must reduce to exact-match-only merging"
    print("ok 6 - threshold 1.0 reduces to exact-match-only merging")

    # Contrato do limiar: falha fechada, sem escrever.
    for bad in (-0.1, 1.5, "0.6", True, None):
        data = json.loads(store.read_text(encoding="utf-8"))
        before = store.read_text(encoding="utf-8")
        data["merge_similarity"] = bad
        store.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        run(
            "add",
            "--feature",
            "guarded",
            "--signal",
            "gate_fail",
            "--source",
            "validation.md:G2",
            "--text",
            "This lesson must never reach the store while the threshold is invalid.",
            expect=2,
        )
        after = json.loads(store.read_text(encoding="utf-8"))
        assert len(after["lessons"]) == 4, f"invalid threshold {bad!r} still wrote a lesson"
        store.write_text(before, encoding="utf-8")
    print("ok 7 - an out-of-range or non-numeric threshold exits 2 and writes nothing")

    # Empate de similaridade resolve pelo menor id, independentemente da ordem no store.
    data = json.loads(store.read_text(encoding="utf-8"))
    data["merge_similarity"] = 0.60
    data["lessons"] = [
        {
            "id": "L-900",
            "key": "ac_gap::alpha beta gamma delta",
            "text": "alpha beta gamma delta",
            "signal": "ac_gap",
            "scope": "",
            "status": "candidate",
            "features": ["f1"],
            "recurrence": 1,
            "harmful": 0,
            "evidence": ["s1"],
            "created": "2026-08-27T00:00:00Z",
            "last_seen": "2026-08-27T00:00:00Z",
        },
        {
            "id": "L-800",
            "key": "ac_gap::alpha beta gamma epsilon",
            "text": "alpha beta gamma epsilon",
            "signal": "ac_gap",
            "scope": "",
            "status": "candidate",
            "features": ["f2"],
            "recurrence": 1,
            "harmful": 0,
            "evidence": ["s2"],
            "created": "2026-08-27T00:00:00Z",
            "last_seen": "2026-08-27T00:00:00Z",
        },
    ]
    data["next_id"] = 901
    store.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    run(
        "add",
        "--feature",
        "tie-breaker",
        "--signal",
        "ac_gap",
        "--source",
        "validation.md:A1",
        "--text",
        "alpha beta gamma zeta",
    )
    data = json.loads(store.read_text(encoding="utf-8"))
    winner = [l for l in data["lessons"] if "tie-breaker" in l["features"]]
    assert len(winner) == 1 and winner[0]["id"] == "L-800", (
        f"tie must break on lowest id, got {[l['id'] for l in winner]}"
    )
    print("ok 8 - an equal-similarity tie breaks on the lowest lesson id")

    # Uma lição em quarentena absorve a recorrência sem ressuscitar.
    data = json.loads(store.read_text(encoding="utf-8"))
    for lesson in data["lessons"]:
        lesson["status"] = "quarantined"
    store.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    run(
        "add",
        "--feature",
        "quarantine-probe",
        "--signal",
        "ac_gap",
        "--source",
        "validation.md:A2",
        "--text",
        "alpha beta gamma epsilon theta",
    )
    data = json.loads(store.read_text(encoding="utf-8"))
    touched = [l for l in data["lessons"] if "quarantine-probe" in l["features"]]
    assert len(touched) == 1, touched
    assert touched[0]["status"] == "quarantined", "a quarantined lesson must not be resurrected"
    print("ok 9 - merging into a quarantined lesson does not resurrect it")

    # Texto só de stopwords não tem conteúdo comparável e não pode fundir por similaridade.
    run(
        "add",
        "--feature",
        "stopwords-only",
        "--signal",
        "spec_deviation",
        "--source",
        "validation.md:S1",
        "--text",
        "it is to be and or of the",
    )
    run(
        "add",
        "--feature",
        "stopwords-again",
        "--signal",
        "spec_deviation",
        "--source",
        "validation.md:S2",
        "--text",
        "the and or of to be is it not",
    )
    data = json.loads(store.read_text(encoding="utf-8"))
    stop = [l for l in data["lessons"] if l["signal"] == "spec_deviation"]
    assert len(stop) == 2, f"empty content-token sets must not merge: {stop}"
    print("ok 10 - lessons with no content tokens never merge by similarity")
