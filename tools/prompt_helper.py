"""Prompt helper: generates copy-paste prompts for the starter kit and validates user deviations.

This module provides a small programmatic API that an assistant or local tooling can use to produce
the dynamic, novice-friendly prompts described in `prompts/DYNAMIC_PROMPTS.md`.

It intentionally does NOT execute shell commands. It prepares the prompt text, validates required
placeholders, and enforces method deviation rules (returns a refusal message when the requested
action would violate policy).
"""
from typing import Dict, Optional
import datetime
from pathlib import Path, PurePosixPath

DEFAULTS = {
    "project_root": "./",
    "python_bin": "python3",
}


def _kit_cmd_root(project_root_hint: str) -> str:
    """Return path prefix for kit-aware commands supporting standalone installs."""
    hint = project_root_hint or "./"
    hint_path = Path(hint)
    candidate = hint_path / "rjw-idd-starter-kit"
    if candidate.exists():
        return str(PurePosixPath(hint) / "rjw-idd-starter-kit")
    return str(PurePosixPath(hint))


class GateBlocked(Exception):
    """Raised when a requested action would violate a gate or protected rule."""
    def __init__(self, gate_id: str, message: str):
        self.gate_id = gate_id
        self.message = message
        super().__init__(f"{gate_id}: {message}")


def _now_date():
    return datetime.date.today().isoformat()


def generate_prompt(step: str, params: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """Return a dict with 'prompt' and 'notes' for a named step.

    step: one of 'bootstrap', 'activate_venv', 'guard_ok', 'guard_bad', 'pytest', 'build_inspect'
    params: optional overrides for placeholders like project_root, python_bin
    """
    p = {**DEFAULTS}
    if params:
        p.update(params)

    proj_raw = p.get('project_root')
    proj = (proj_raw if proj_raw is not None else DEFAULTS['project_root']).rstrip('/')
    python_bin = p.get('python_bin') or DEFAULTS['python_bin']

    kit_root_for_cmd = _kit_cmd_root(proj)

    if step == "bootstrap":
        cmd = f"PYTHON_BIN={python_bin} bash {kit_root_for_cmd}/scripts/setup/bootstrap_project.sh"
        prompt = (
            "Run the bootstrap script for this starter repository. "
            f"Use `{python_bin}` if available. Command: `{cmd}`. "
            "Report stdout/stderr, any non-zero exit, and whether `.venv` was created. "
            "If the script is missing, list the expected path and stop."
        )
        return {"prompt": prompt, "notes": "Bootstraps the repo: creates .venv, installs deps, runs smoke tests."}

    if step == "activate_venv":
        prompt = (
            "Activate the project's virtual environment created under `.venv` and confirm which python executable is active by running `which python` and `python --version`. "
            "If `.venv` is missing, explain that bootstrap must run first."
        )
        return {"prompt": prompt, "notes": "Interactive: the user may need to source .venv/bin/activate."}

    if step == "guard_ok":
        command = f"{kit_root_for_cmd}/bin/rjw guard {kit_root_for_cmd}/examples/ok.json"
        prompt = (
            "Run the governance guard using the packaged CLI on the 'ok' demo fixture: "
            f"`{command}`. Print the output and exit code. If the command is not executable, run `chmod +x {kit_root_for_cmd}/bin/rjw` and retry."
        )
        return {"prompt": prompt, "notes": "Expected: exit 0 and a validation passed message."}

    if step == "guard_bad":
        command = f"{kit_root_for_cmd}/bin/rjw guard {kit_root_for_cmd}/examples/bad.json"
        prompt = (
            "Run the governance guard on the 'bad' demo fixture: "
            f"`{command}`. Print the output and exit code. Explain the rule IDs and JSON paths of violations shown."
        )
        return {"prompt": prompt, "notes": "Expected: non-zero exit; explain violations."}

    if step == "pytest":
        prompt = (
            "Run the test suite with `pytest -q`. If tests fail, print failing test names and traceback. Do not modify code."
        )
        return {"prompt": prompt, "notes": "Runs unit tests. Useful to guard CI correctness."}

    if step == "build_inspect":
        cmd = f"python -m build {kit_root_for_cmd}"
        prompt = (
            f"Build a source and wheel for the starter kit package using: `{cmd}`. "
            "Then list the wheel contents and check for `examples/ok.json` and `examples/bad.json` (e.g., `unzip -l dist/*.whl | grep examples`). Print results."
        )
        return {"prompt": prompt, "notes": "Builds distributions and inspects included package data."}

    if step == "tutorial_step":
        # params may include: title, body, files (list), next_action_hint
        title = p.get('title') or 'Tutorial step'
        body = p.get('body') or 'Perform the requested tutorial action and report the result.'
        next_hint = p.get('next_action_hint') or 'When complete, suggest the next small action and one-line command to execute.'
        prompt = (
            f"Implement the tutorial step titled: '{title}'.\n\n"
            f"Instructions: {body}\n\n"
            "Requirements: keep changes minimal and local to the project; do NOT modify governance guard logic; run tests after making code changes.\n"
            "Outputs required: 1) short summary of actions taken, 2) files created/modified with brief content outline, 3) exact shell commands a novice can copy to run verification (one-line each), 4) suggested next step.\n\n"
            f"{next_hint}"
        )
        return {"prompt": prompt, "notes": "Use this to instruct the assistant to perform a small tutorial step and produce copyable verification commands."}

    raise ValueError(f"Unknown step: {step}")


def validate_user_prompt(user_prompt: str, expected_step: str) -> None:
    """Check whether the user prompt deviates from the expected template in a way that violates gates.

    This performs simple heuristics: if the user asks to remove guard rules, to write to system paths, or to skip tests,
    raise GateBlocked with appropriate message. Otherwise, return None (allowed).
    """
    lower = user_prompt.lower()
    # Protected actions that must be refused
    if "remove guard" in lower or "disable guard" in lower or "bypass guard" in lower:
        raise GateBlocked("GATE_GUARD_MODIFICATION", "Modifying or disabling governance guard rules is forbidden by the method.")

    if "write /etc" in lower or "/etc/passwd" in lower or "format /dev" in lower:
        raise GateBlocked("GATE_PRIVILEGED_WRITE", "Requests to write to system paths or perform privileged writes are forbidden.")

    if "skip tests" in lower or "dont run tests" in lower:
        raise GateBlocked("GATE_SKIP_TESTS", "Skipping tests is not allowed; tests are a required gate before release operations.")

    # if user requests publish to pypi and has not indicated approval, warn — but we'll allow if user explicitly names 'publish'
    if "publish to pypi" in lower and "publish" not in lower:
        raise GateBlocked("GATE_PUBLISH_APPROVAL", "Publishing requires explicit instruction and verification; please confirm 'publish' if you intend to proceed.")

    # otherwise allow
    return None


def chat_response(step: str, params: Optional[Dict[str, str]] = None, user_override: Optional[str] = None) -> Dict[str, str]:
    """Compose a chat-friendly response that includes an assistant message and a copy-paste prompt.

    - Generates the dynamic prompt for `step` using `generate_prompt`.
    - If `user_override` is provided, validate it; if it violates gates, return a refusal message and gate_id.
    - Otherwise return a dict with keys:
      - 'assistant_message': human-friendly guidance
      - 'copy_prompt': the prompt text the user can paste to an agent or use as input
      - optional 'gate_id' if a gate blocked the request
    """
    params = params or {}
    # If user override appears, validate it against gates
    if user_override:
        try:
            validate_user_prompt(user_override, step)
        except GateBlocked as g:
            return {
                'assistant_message': (
                    f"Request refused: attempting to perform a prohibited action would violate a gate. "
                    f"Gate id: {g.gate_id}. Reason: {g.message}"
                ),
                'gate_id': g.gate_id,
                'copy_prompt': ''
            }

    # generate the standard prompt
    try:
        out = generate_prompt(step, params)
    except Exception as e:
        return {'assistant_message': f'Error generating prompt: {e}', 'copy_prompt': ''}

    assistant_message = (
        f"I prepared a guided prompt for the step '{step}'. Copy and paste the prompt below into the assistant input (or run the verification commands it contains).\n\n"
        f"If you want me to run checks locally, say so and I will describe the exact commands to run."
    )

    return {'assistant_message': assistant_message, 'copy_prompt': out['prompt']}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Prompt helper CLI: generate copy-paste prompts for common steps")
    parser.add_argument("step", help="Step name (bootstrap, activate_venv, guard_ok, guard_bad, pytest, build_inspect)")
    parser.add_argument("--project-root", help="Project root path to embed in prompts", default=None)
    parser.add_argument("--python-bin", help="Python binary hint", default=None)
    # tutorial_step optional extras
    parser.add_argument("--title", help="Tutorial step title (for tutorial_step)", default=None)
    parser.add_argument("--body", help="Tutorial step body/instructions (for tutorial_step)", default=None)
    parser.add_argument("--next-action-hint", help="Next action hint (for tutorial_step)", default=None)
    args = parser.parse_args()
    params = {}
    if args.project_root:
        params['project_root'] = args.project_root
    if args.python_bin:
        params['python_bin'] = args.python_bin
    if args.title:
        params['title'] = args.title
    if args.body:
        params['body'] = args.body
    if args.next_action_hint:
        params['next_action_hint'] = args.next_action_hint
    out = generate_prompt(args.step, params)
    print("PROMPT:\n")
    print(out['prompt'])
    print("\nNOTES:\n")
    print(out['notes'])
