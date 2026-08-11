# ABS-0004 v9.1 Version/History Update Record

Base repository HEAD: `8957457e250ca7674040603ca2941daf86f4f230`

This update is bookkeeping only. It makes no substantive correction beyond the eight A1-A8 corrections already present in the base ontology.

Changes:

1. Metadata version changes from `v9` to `v9.1`.
2. Reconstruction-baseline prose names v9.1 as the proposed document requiring admission review.
3. The version admission table records the reviewed v9 as reviewed but not admitted and superseded by the corrected v9.1 candidate.
4. The table records the reviewed-v9 SHA-256 `8f61c283a5d716f6816798a4946824b2d0d633a8be0d154da33cc1ebbe7ab1fa`.
5. The table records the corrected pre-version-bump SHA-256 `c2dadf897441bf842b34e2b71a347a264401bb228168c4b4214d5964c8d218b0` and states that the difference is the eight accepted findings A1-A8 under `DECISION-20260811-0001`.
6. The v9.1 row explicitly states that this version/history update is not a ninth substantive correction.

Final v9.1 candidate SHA-256:

`ce1ddb25488175ed87d7c30d904c5ee334a51527bb5bfef3c45facf063bece51`

Validation:

- `git diff --check`: passed
- `python3 -m pytest -q tests/test_abstraction.py`: 7 passed
