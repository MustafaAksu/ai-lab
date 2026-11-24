"""Deliberate failure for PLAN-20261124-0001 S9: live falsification of the CI failure path.

This branch must never be merged. Its CI run must fail and still upload a receipt
whose result is one_or_more_commands_failed.
"""


def test_deliberately_broken_for_s9():
    assert False, "deliberate failure (PLAN-20261124-0001 S9); do not merge"
