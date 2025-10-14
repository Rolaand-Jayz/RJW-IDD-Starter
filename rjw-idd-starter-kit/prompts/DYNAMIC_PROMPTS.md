# Dynamic prompt templates (novice-friendly)

This file contains copy-paste prompts for the starter kit agent. Each block is crafted so a novice can paste it directly into the agent prompt input. The prompts are dynamic: the agent will substitute the bracketed values (for example {project_root}) based on the repository state or ask for them if missing.

Guidelines for the agent using these prompts:
- If the user pastes the prompt exactly, the agent should run the described step and report the result.
- If the user deviates from the expected prompt, the agent should detect the deviation. If the deviation is outside the method scope, the agent should politely refuse and explain the gate that would be violated. If the user insists, the agent will attempt a best-effort action until the next gate fails and then stop, reporting the blocking gate.

Common steps and copy-paste prompts

1) Bootstrap project (creates .venv and installs deps)

Copy-paste prompt to give to the agent:

"Run the bootstrap script for this starter repository. Use PYTHON_BIN=python3.11 if available. Command to run: `bash rjw-idd-starter-kit/scripts/setup/bootstrap_project.sh`. Report stdout/stderr, any non-zero exit, and whether `.venv` was created. If the file is missing, list the expected path and stop."

2) Activate virtualenv (interactive guidance)

Copy-paste prompt:

"Activate the project's virtual environment created under `.venv` and confirm which python executable is active by running `which python` and `python --version`. If `.venv` is missing, explain that bootstrap must run first."

3) Run guard demo (pass fixture)

Copy-paste prompt:

"Run the governance guard using the packaged CLI on the 'ok' demo fixture: `rjw-idd-starter-kit/bin/rjw guard rjw-idd-starter-kit/examples/ok.json`. Print the output and exit code. If the command is not executable, run `chmod +x rjw-idd-starter-kit/bin/rjw` and retry."

4) Run guard demo (fail fixture)

Copy-paste prompt:

"Run the governance guard on the 'bad' demo fixture: `rjw-idd-starter-kit/bin/rjw guard rjw-idd-starter-kit/examples/bad.json`. Print the output and exit code. Explain the rule IDs and JSON paths of violations shown."

5) Run tests

Copy-paste prompt:

"Run the test suite with `pytest -q`. If tests fail, print the failing test names and traceback. Do not modify code."

6) Build distribution (inspect examples included)

Copy-paste prompt:

"Build a source and wheel for the starter kit package in `rjw-idd-starter-kit` using `python -m build rjw-idd-starter-kit`. Then list the wheel contents and check for `examples/ok.json` and `examples/bad.json`. Print the `unzip -l` result filtered for examples."

When to decline (deviation rules)

- If the user asks the agent to change protected files that would alter governance or gate logic (for example removing a guard rule), the agent must refuse and explain the gate and risk.
- If the user requests actions that require secrets, network publishing, or elevated privileges (writing to system directories), the agent must refuse and point to safe alternatives.

If the user insists to proceed outside the method, the agent will perform a best-effort attempt but must stop immediately if a gate fails and report which gate blocked progress (example: guard failure, test failure, packaging check). The agent will not silently bypass gates.

-- End of templates --
