# Quickstart (≤5 commands)

This quickstart gets a novice developer from checkout to running the basic guard checks.

1. Create and activate a virtualenv

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dev deps

```bash
python -m pip install --upgrade pip
pip install -r rjw-idd-starter-kit/requirements-dev.txt || pip install -r rjw-idd-starter-kit/requirements.txt
```

3. Run the governance checks

```bash
bash scripts/checks/run_checks.sh
```

4. Run the bootstrap script (optional)

```bash
bash rjw-idd-starter-kit/scripts/setup/bootstrap_project.sh
```

5. Open `rjw-idd-starter-kit/README.md` and follow the novice guide prompts in
   `rjw-idd-starter-kit/manual/novice-quickstart.md`.
