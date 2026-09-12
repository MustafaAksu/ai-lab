"""Relational state organization cell (PREREG-RS-0001 v0.3.1, PLAN-20260912-0001).

A governed visitor experiment. INTEGRATION_EFFECT is "none": nothing in this
package changes AI-Lab runtime behaviour, defaults, prompt paths, context
selection, graph-neighbourhood behaviour, provider routing or the self-model.

Import membrane (WARR-20260912-0001 condition 6): every module here except
runner.py is standard-library-only; runner.py alone may import
ai_lab.providers.*. Enforced by tests/experiments/relational_state/test_membrane.py.
"""

INTEGRATION_EFFECT = "none"
PREREG_ID = "PREREG-RS-0001"
PREREG_VERSION = "v0.3.1"
PLAN_ID = "PLAN-20260912-0001"
WARRANT_ID = "WARR-20260912-0001"
