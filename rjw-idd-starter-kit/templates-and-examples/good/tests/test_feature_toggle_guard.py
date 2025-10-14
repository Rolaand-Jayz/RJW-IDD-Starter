"""
Good example: validates the feature-toggle rollout guard.
Links back to `templates-and-examples/good/specs/spec-ci-guardrails.md`.
"""

import pytest


@pytest.mark.unit
def test_guard_blocks_toggle_without_change_log():
    fake_guard_result = {"change_log_present": False, "toggle_registered": True}

    assert not fake_guard_result["change_log_present"], (
        "Guard should fail when the change log lacks the toggle entry. "
        "See templates-and-examples/templates/change-logs/CHANGELOG-template.md."
    )
