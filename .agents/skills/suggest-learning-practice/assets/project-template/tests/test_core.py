from __future__ import annotations

import pytest

from practice_module import learner_function


def test_normal_documented_contract() -> None:
    pytest.fail("Replace with one observable normal contract; do not reveal the method.")


def test_edge_documented_contract() -> None:
    pytest.fail("Replace with one meaningful boundary contract.")


def test_failure_invalid_input_contract() -> None:
    pytest.fail("Replace with one invalid-input or failure contract.")
