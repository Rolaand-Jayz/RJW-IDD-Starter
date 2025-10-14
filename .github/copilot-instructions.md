# Copilot Instructions

## Repo map
- Root kit lives in `rjw-idd-starter-kit/`; copy or adapt this tree when shipping a new project.
- `rjw-idd-methodology/` is doctrine: edit only when a new decision (`DEC-####`) justifies changing the method. Reference it from deliverables instead of inlining content.
- Add-ons under `rjw-idd-methodology/addons/` extend the method (e.g., `video-ai-enhancer/` quality gates, `3d-game-core/` determinism harnesses) and ship reusable CI snippets; pull them in deliberately using `scripts/addons/enable_*.py`.
- The top-level `method/` directory holds shared feature toggles (`config/features.yml`) for tooling experiments.

## Add-on activation
- Enable add-ons via `rjw-idd-starter-kit/scripts/addons/enable_{3d_game_core,video_ai_enhancer}.py`.
- Configure profiles using `set_3d_profile.py` or `set_video_ai_profile.py` with `--profile <name>`.
- Disable cleanly with `disable_{3d_game_core,video_ai_enhancer}.py`.
- Bootstrap installer (`scripts/bootstrap/install.sh`) prompts for add-on selection during initial setup.
- Always update `templates-and-examples/templates/change-logs/CHANGELOG-template.md` and `docs/decisions/` when toggling add-ons.

## Template boundaries
- Ship the starter kit pristine: leave placeholder tables such as `templates-and-examples/templates/change-logs/CHANGELOG-template.md`, `artifacts/ledgers/*.csv`, and `specs/*.md` untouched so downstream projects can fill them after copying.
- Use `rjw-idd-starter-kit/docs/manual/starter-kit-manual.md` for the end-to-end bring-up checklist, guard explanations, and role expectations.
- Sample scaffolds (`workspace/`, `ci_samples/`) illustrate expected artefacts; treat them as documentation rather than editable inputs.

## When you change things
- Every material update gets a new `change-YYYYMMDD-##` row in `rjw-idd-starter-kit/templates-and-examples/templates/change-logs/CHANGELOG-template.md`, linked to affected IDs and integration artifacts.
- Specs live in `rjw-idd-starter-kit/specs/`; use the templates and keep IDs aligned with `artifacts/ledgers/requirement-ledger.csv` and `test-ledger.csv`.
- Decisions stay in `rjw-idd-starter-kit/docs/decisions/` using `rjw-idd-methodology/templates/PROJECT-DEC-template.md`; cross-link evidence (`EVD-####`), requirements (`REQ-####`), and tests (`TEST-####`).
- Integration work should create a transcript bundle via `tools/integration/archive_scaffold.py` and log its path in the Change Log.

## Local workflows
- Bootstrap the dev environment from repository root with:
  - `bash rjw-idd-starter-kit/scripts/setup/bootstrap_project.sh` (honors `PYTHON_BIN` if you need a specific interpreter).
- Day-to-day: work inside `rjw-idd-starter-kit/`, activate `.venv`, then run `pytest` followed by `bash scripts/ci/test_gate.sh` to mirror CI.
- Guard scripts assume the Git history includes `origin/main`; set `RJW_BASE_REF`/`RJW_HEAD_REF` when diffing other ranges.

## Governance guards
- `scripts/ci/test_gate.sh` chains the method requirements:
  - `tools/testing/red_green_guard.py` enforces red→green test flow.
  - `scripts/validate_ids.py` ensures ledgers, specs, and Change Log stay consistent.
  - `scripts/validate_evidence.py` (auto-runs when research assets move) rejects evidence older than 14 days.
  - `tools/testing/change_log_guard.py` blocks missing Change Log rows; `living_docs_guard.py` forces documentation updates; `governance_alignment_guard.py` checks decision/spec linkage.
- Keep guard fixtures synchronized with the tests under `rjw-idd-starter-kit/tests/guards/` when behaviour changes.

## Evidence & prompts
- Evidence configuration lives in `research/evidence_tasks.json`; harvest with `tools/rjw_idd_evidence_harvester.py`, curate via `scripts/promote_evidence.py`, and validate freshness through `scripts/validate_evidence.py`.
- Prompt playbooks under `docs/prompts/` drive non-coders: start with `PROMPT-0001-starter-briefing.md`, then `PROMPT-0002-implementation-coach.md` for build tasks.
- `rjw-idd-methodology/operations/METHOD-0004-ai-agent-workflows.md` enumerates role expectations; follow it when coordinating multi-agent work.

## CI hooks
- GitHub Actions workflow `.github/workflows/video-ai-enhancer.yml` can be called directly or reused; it runs add-on quality gates only when `ENABLE_RJW_VIDEO` (or a `force` input) enables them.
- Reusable snippets in `addons/*/ci/` document how to wire additional gates when integrating with downstream repos.
{
        "\"/home/rolaandjayz__/Desktop/Rolaand": true,
        "git add": true,
        "git commit": true,
        "add": true,
        "start": true,
        "green": true,
        "true": true,
        "*": true,
        "ps": true,
        "PYTHONPATH=.": true,
        "(echo": true,
        "/tmp/rve_dev_demo.log": true,
        "sed": true,
        "RVE_TORCH_AVAILABLE=1": true,
        "print(PySide6.__version__)\"": true,
        "env": true,
        "WAYLAND_DISPLAY": true,
        "XDG_SESSION_TYPE'": true,
        "python": true,
        "'PY'": true,
        "printf": true,
        "research/evidence_allowlist.txt": true,
        "printf \"# Promote all first-hand engine/networking records\\n%s\\n\" \"$(python -c \"import json\nwith open('research/evidence_index_raw.json') as f:\n data=json.load(f)\n recs=[r['evid_id'] for r in data['records'] if 'first-hand' in r.get('quality_flags',[]) and any(t in ('engine','networking') for t in r.get('tags',[]))]\n print('\\n'.join(recs))\")\" > research/evidence_allowlist.txt && sed -n '1,120p' research/evidence_allowlist.txt": {
            "approve": true,
            "matchCommandLine": true
        },
        "'id':r['evid_id'],'platform':r['platform'],'date':r['date'],'quote':r['minimal_quote'][:240]})": true,
        "Netcode": true,
        "s['id']}": true,
        "s['platform']}": true,
        "s['date']}):": true,
        "s['quote']}\"": true,
        "pytest": true,
        "bash": true,
        "pip": true,
        "ERROR": true,
        "packages)\"": true,
        "cd /home/rolaandjayz__/Desktop/method/rjw-idd-starter-kit && python -c \"\nimport re\n\n# Read the file\nwith open('docs/troubleshooting.md', 'r') as f:\n    content = f.read()\n\n# Fix all the markdown linting issues\n# Add blank lines around lists\ncontent = re.sub(r'(\\*\\*Symptoms:\\*\\*)\\n(-)', r'\\1\\n\\n\\2', content)\ncontent = re.sub(r'(\\*\\*Solutions:\\*\\*)\\n(```
)', r'\\1\\n\\n\\2', content)\n\n# Add blank lines around headings\ncontent = re.sub(r'(### Environment Check Script)\\n(
```)', r'\\1\\n\\n\\2', content)\ncontent = re.sub(r'(### Performance Benchmark Script)\\n(```
)', r'\\1\\n\\n\\2', content)\n\n# Write back\nwith open('docs/troubleshooting.md', 'w') as f:\n    f.write(content)\n\nprint('Fixed markdown formatting issues')\n\"": {
            "approve": true,
            "matchCommandLine": true
        },
        "cd /home/rolaandjayz__/Desktop/method/rjw-idd-starter-kit && python -c \"\nimport re\n\n# Read the file\nwith open('docs/troubleshooting.md', 'r') as f:\n    content = f.read()\n\n# Fix all markdown issues systematically\n\n# 1. Add blank lines around all lists (Symptoms and Solutions)\ncontent = re.sub(r'(\\*\\*Symptoms:\\*\\*)\\n(-)', r'\\1\\n\\n\\2', content)\ncontent = re.sub(r'(\\*\\*Solutions:\\*\\*)\\n(
```)', r'\\1\\n\\n\\2', content)\n\n# 2. Add blank lines around headings before code blocks\ncontent = re.sub(r'(### Environment Check Script)\\n(```
)', r'\\1\\n\\n\\2', content)\ncontent = re.sub(r'(### Performance Benchmark Script)\\n(
```)', r'\\1\\n\\n\\2', content)\ncontent = re.sub(r'(### Community Resources)\\n(1\\.)', r'\\1\\n\\n\\2', content)\ncontent = re.sub(r'(### Escalation Path)\\n(1\\.)', r'\\1\\n\\n\\2', content)\ncontent = re.sub(r'(### Diagnostic Information to Include)\\n(-)', r'\\1\\n\\n\\2', content)\n\n# 3. Add blank lines around fenced code blocks\ncontent = re.sub(r'(```\\n)(### )', r'\\1\\n\\2', content)\n\n# 4. Ensure file ends with single newline\nif not content.endswith('\\n'):\n    content += '\\n'\n\n# Write back\nwith open('docs/troubleshooting.md', 'w') as f:\n    f.write(content)\n\nprint('Fixed all markdown formatting issues')\n\"": {
            "approve": true,
            "matchCommandLine": true
        },
        "tools/health_check.py": true,
        "tools/performance_benchmark.py": true,
        "cd /home/rolaandjayz__/Desktop/method/rjw-idd-starter-kit && python -c \"\nimport sys\nprint('Python version:', sys.version)\nprint('All imports working correctly!')\ntry:\n    import tools.logging_config\n    import tools.performance_monitor\n    import tools.backup_manager\n    import tools.health_check\n    import tools.performance_benchmark\n    print('✅ All tools imported successfully')\nexcept ImportError as e:\n    print('❌ Import error:', e)\n    sys.exit(1)\n\"": {
            "approve": true,
            "matchCommandLine": true
        },
        "import": true,
        "print('ok',": true,
        "rg": true,
        "change_id": true,
        "description": true,
        "impacted_ids": true,
        "operator": true,
        "verification": true,
        "-----------": true,
        "------------": true,
        "-------------": true,
        "--------------": true,
        "----------": true,
        "change-20251003-03": true,
        "2025-10-03": true,
        "Documented": true,
        "DOC-IDE-SETUP": true,
        "TOOLS-HEALTH-CHECK": true,
        "TOOLS-PERFORMANCE-BENCH": true,
        "Platform": true,
        "validator:pass": true,
        "\"\"\"": true,
        "git checkout": true,
        "python3": true
    }