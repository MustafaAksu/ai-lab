from ai_lab.experiments.relational_state.equivalence import audit, distinct_handles_preserved, query_independent
from ai_lab.experiments.relational_state.generator import generate
from ai_lab.experiments.relational_state.model import ITEM_VOCAB, PERSON_VOCAB, Clue, Puzzle, Trial
from ai_lab.experiments.relational_state.render import decode, inference_derived_facts, prompt, render_flat, render_rm, state_block


def _sample():
    out = []
    for n, d, st, seed in ((3, 1, "unique", 1), (5, 2, "ambiguous", 2), (8, 4, "unique", 3), (9, 4, "ambiguous", 4)):
        inst = generate(n, d, st, seed)
        assert inst is not None
        out.append(inst)
    return out


def test_a1_to_a6_pass_on_generated_instances():
    for inst in _sample():
        assert audit(inst.trial.puzzle) == audit(inst.trial.puzzle)
        assert audit(inst.trial.puzzle).ok, audit(inst.trial.puzzle).failed


def test_rm_contains_clue_table_once_and_id_only_index():
    for inst in _sample():
        pz = inst.trial.puzzle
        flat, rm = render_flat(pz), render_rm(pz)
        assert rm.startswith(flat)
        index = rm[len(flat):]
        for c in pz.clues:
            assert rm.count(c.line()) == 1
            assert c.line() not in index
        assert inference_derived_facts(rm, pz) == []


def test_a4_rejects_semantic_content_in_rm():
    pz = _sample()[0].trial.puzzle
    doctored = render_rm(pz) + "\nAndo: candidates kite lamp"
    assert inference_derived_facts(doctored, pz) == ["Ando: candidates kite lamp"]


def test_a6_rejects_repeated_clue_bodies():
    pz = _sample()[0].trial.puzzle
    clues = pz.clues + (Clue(pz.clues[0].id, pz.clues[0].relation, pz.clues[0].person, pz.clues[0].item),)
    doubled = Puzzle(pz.persons, pz.items, clues)
    res = audit(doubled)
    assert not res.ok and "A6" in res.failed


def test_query_independence_and_prompt_frame_identical_across_arms():
    for inst in _sample():
        pz = inst.trial.puzzle
        assert query_independent(pz)
        p1, p2 = prompt(inst.trial, 1), prompt(inst.trial, 2)
        head1 = p1.split("\n\nCLUES\n")[0]
        head2 = p2.split("\n\nCLUES\n")[0]
        assert head1 == head2
        assert p1.endswith(f"Question: which item belongs to {inst.trial.target}?")
        assert p2.endswith(f"Question: which item belongs to {inst.trial.target}?")
        for t in pz.persons:
            assert state_block(Trial(pz, t), 2) == state_block(inst.trial, 2)


def test_a5_identical_neighbourhoods_remain_distinct_handles():
    # Ando and Brix have byte-identical clue neighbourhoods (same relation to the same item)
    persons, items = PERSON_VOCAB[:3], ITEM_VOCAB[:3]
    pz = Puzzle(persons, items, (Clue("C1", "NOT_EQUAL", "Ando", "kite"), Clue("C2", "NOT_EQUAL", "Brix", "kite")))
    assert distinct_handles_preserved(pz)
    for arm_text in (render_flat(pz), render_rm(pz)):
        clues, _ = decode(arm_text)
        assert {c.person for c in clues} == {"Ando", "Brix"}
    assert "Ando: C1" in render_rm(pz) and "Brix: C2" in render_rm(pz)
