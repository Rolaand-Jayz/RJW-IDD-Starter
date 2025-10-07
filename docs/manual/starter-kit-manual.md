# RJW-IDD Starter Kit Manual

This manual is the field guide for deploying the RJW-IDD starter kit. Pair it with the top-level README: the README gives the elevator pitch and quickstart checklist, while this manual dives into responsibilities, cadence, and troubleshooting.

> Brand-new developers should start with `docs/manual/novice-quickstart.md` plus the prompts in `docs/prompts/`. Come back here once the core flow feels comfortable.

## 1. Orientation

- **Target audience:** Engineering leads, governance sentinels, doc stewards, product tech leads.
- **Goal:** Stand up RJW-IDD governance from day zero—every requirement, spec, test, evidence link, and decision is traceable.
- **Included assets:**
  - Governance docs (`docs/`)
  - SPEC templates (`specs/`)
  - Traceability ledgers (`artifacts/ledgers/`)
  - Research configuration (`research/`)
  - Guard automation (`scripts/`, `tools/testing/`)
  - Dependency manifest (`requirements-dev.txt`) and bootstrap script (`scripts/setup/bootstrap_project.sh`)
  - Prompt suite for non-developers (`docs/prompts/`)

## 2. Prompt Suite Map

| ID | When to Use | Outcome |
|----|-------------|---------|
| `PROMPT-0001-starter-briefing.md` | You have a raw idea and need a simple plan. | Repository tour, RJW-IDD checklist, next-step questions. |
| `PROMPT-0002-implementation-coach.md` | You are ready to edit files but need a guided, test-first sequence. | Ordered to-do list with references to specs, tests, and docs. |
| `PROMPT-0003-spec-translator.md` | A plain requirement must become a formal spec update. | Drafted spec sections and ledger linkage tips. |
| `PROMPT-0004-test-navigator.md` | You need to plan tests before coding. | Structured test cases with simple assertions to implement. |
| `PROMPT-0005-doc-sync.md` | Code changes are done and documentation must catch up. | Change-log guidance, doc updates, reconciliation notes. |
| `PROMPT-0006-governance-audit.md` | Final governance sweep before opening a pull request. | Guard checklist, failure recovery tips, PR template text. |
| `PROMPT-0007-change-log-author.md` | You must write the change-log entry and notify stakeholders. | Ready-to-paste table row, communication snippet, artefact checklist. |
| `PROMPT-0008-merge-ready-checklist.md` | Everything looks done and you want a last safety review. | Merge/no-merge verdict with any remaining blockers. |

Start every change with PROMPT-0001, then follow the suggested next prompt at the end of each interaction.

## 3. Bring-Up Checklist

1. **Create repo & import kit**
   - `git init`
   - Copy kit contents to repo root, commit as `change-YYYYMMDD-01`.
2. **Bootstrap tooling**
   - From the repo root run `scripts/setup/bootstrap_project.sh`.
   - Script creates `.venv/`, installs `requirements-dev.txt`, runs `pytest`, then executes the governance gate.
3. **Assign roles** (see §3) and record them in team docs.
4. **Seed traceability**
   - Add first entries to `artifacts/ledgers/requirement-ledger.csv` and `test-ledger.csv`.
   - Duplicate relevant SPEC templates.
5. **Connect CI**
   - Push to remote; `.github/workflows/test-gate.yml` runs automatically on pull requests.
6. **Start logging**
   - Add initial change entry in `docs/change-log.md` and ensure living-doc gaps are tracked.

## 4. Role Matrix

| Role | Accountabilities | Primary Artefacts |
|------|------------------|-------------------|
| Agent Conductor | Enforces guard compliance, plans lifecycle cadence. | `scripts/ci/test_gate.sh`, `.github/workflows/test-gate.yml` |
| Spec Curator | Owns SPEC-#### documents, keeps spec ↔ ledger ↔ decision links current. | `specs/`, `artifacts/ledgers/requirement-ledger.csv` |
| Doc Steward | Maintains change log & living docs reconciliation. | `docs/change-log.md`, `docs/living-docs-reconciliation.md` |
| Governance Sentinel | Oversees decisions, evidence freshness, audits. | `docs/decisions/`, `research/`, guard suite |

## 5. Directory Reference

- `docs/` – change log, living-doc reconciliation, runbooks, standards, decisions.
- `specs/` – modular SPEC templates covering all governance pillars.
- `artifacts/` – requirement/test ledgers, integration transcript scaffold, evidence indices.
- `research/` – evidence task configuration, allowlists, raw/curated JSON files.
- `scripts/` – validation utilities, CI orchestration, setup bootstrapper.
- `tools/testing/` – guard implementations.
- `tests/` – pytest coverage for guards; extend when adding custom checks.

## 6. Quickstart Script

```bash
# Optional: export PYTHON_BIN=python3.11
scripts/setup/bootstrap_project.sh
```

**Script behaviour:**
1. Create `.venv/` if missing.
2. Install dependencies from `requirements-dev.txt` (and editable project if `pyproject.toml` exists).
3. Run `pytest`.
4. Execute `scripts/ci/test_gate.sh` using `origin/main` or the repository’s first commit as `RJW_BASE_REF`.

If the repository is not yet tracked by git, the script skips the gate and prints a reminder.

## 7. Guard Suite Summary

| Guard | Script | Trigger | Resolution |
|-------|--------|---------|------------|
| Red/Green | `tools/testing/red_green_guard.py` | Changed code without tests | Add/update tests before merging |
| ID Validator | `scripts/validate_ids.py` | Broken REQ/SPEC/TEST/EVD refs | Align ledgers, change log, evidence |
| Evidence Freshness | `scripts/validate_evidence.py` | Research artefacts stale | Refresh evidence via harvester |
| Change Log | `tools/testing/change_log_guard.py` | No change-log row | Append row to `docs/change-log.md` |
| Living Docs | `tools/testing/living_docs_guard.py` | Open reconciliation items; doc gaps | Update docs or log gap resolution |
| Governance Alignment | `tools/testing/governance_alignment_guard.py` | Spec without ledger/DEC alignment | Update `artifacts/ledgers` and `docs/decisions/` |

## 8. Lifecycle Adoption

1. **RDD**
   - Customize `research/evidence_tasks.json`.
   - Run `tools/rjw_idd_evidence_harvester.py` and then `scripts/validate_evidence.py`.
2. **SDD**
   - Draft specs under `specs/` following templates. Populate ledgers with IDs and cross-references.
   - Open living-doc gaps for any known shortfalls; resolve them before implementation.
3. **TDD/LDDD/IDD**
   - Write failing tests (`TEST-####`), implement fixes, verify guards pass.
   - Update specs/docs, add change-log entry, and record governance decisions.

## 9. Add-on Management

RJW-IDD supports optional add-ons that extend the methodology for specific domains:

### Available Add-ons

**3d-game-core** - Augments RJW-IDD for 3D game development:
- Determinism and rollback harnesses
- Tolerant replay systems
- Asset and performance gates
- Game design document templates
- Profiles: `generic`, `first_person`, `third_person`, `isometric`, `platformer`, `driving`, `action_rpg`, `networked`

**video-ai-enhancer** - Augments RJW-IDD for real-time video enhancement:
- Quality, latency, and storage governance
- Pipeline architecture templates
- Live streaming optimization
- Profiles: `baseline`, `live_stream`, `broadcast_mastering`, `mobile_edge`, `remote_collab`

### Enabling Add-ons

During bootstrap (`scripts/bootstrap/install.sh`), you'll be prompted to select an add-on. You can also enable manually:

```bash
# Enable 3D game core
python scripts/addons/enable_3d_game_core.py
python scripts/addons/set_3d_profile.py --profile third_person

# Enable video AI enhancer
python scripts/addons/enable_video_ai_enhancer.py
python scripts/addons/set_video_ai_profile.py --profile live_stream
```

### Disabling Add-ons

```bash
python scripts/addons/disable_3d_game_core.py
# or
python scripts/addons/disable_video_ai_enhancer.py
```

### Governance Requirements

When enabling, disabling, or changing add-on configuration:
1. Add an entry to `docs/change-log.md`
2. Document the decision in `docs/decisions/`
3. Update `logs/LOG-0001-stage-audits.md`

Add-on state is tracked in `method/config/features.yml`.

## 10. Troubleshooting & FAQ

**Q: Guards fail locally but the kit just shipped?**
   - Clone the SPEC template, cross-link REQ/SPEC/TEST IDs, and update ledgers.
3. **Implementation & Living Docs**
   - Add tests, run `pytest` locally, capture verification evidence in change log.
   - Ensure living-doc reconciliation is closed before merging.
   - Record decisions using `docs/decisions/DEC-####.md` template.

## 9. Extending the Kit

- **Additional guards:** place in `tools/testing/`, register inside `scripts/ci/test_gate.sh`, add pytest coverage.
- **Dependencies:** update `requirements-dev.txt` and rerun bootstrap script.
- **Standards & runbooks:** add domain-specific docs under `docs/standards/` or `docs/runbooks/`.
- **CI automation:** extend `.github/workflows/` with extra jobs (linting, deploy, etc.).

## 10. Operational Cadence

- **Daily:** `pytest && scripts/ci/test_gate.sh` before pushing.
- **Weekly:** Check `docs/living-docs-reconciliation.md` for lingering gaps.
- **Monthly:** Audit evidence freshness and ledger completeness; record DEC updates.
- **Quarterly:** Review SPEC templates/runbooks to bake in learnings.

## 11. Troubleshooting

- **`origin/main` missing:** Set `RJW_BASE_REF=$(git rev-list --max-parents=0 HEAD)` before running the gate.
- **Guard import errors:** Ensure `tests/conftest.py` remains intact; it prepends repo root to `sys.path`.
- **Decision guard failure:** Replace `DEC-XXXX` placeholders and mention the DEC ID inside the file.
- **Living-doc guard complaining about placeholder row:** Remove or update the template row once real reconciliations exist.

## 12. Next Steps After Bootstrap

1. Log first real change entry in `docs/change-log.md`.
2. Add initial REQ-#### and TEST-#### ledger rows.
3. Capture early assumptions in a DEC-#### decision file.
4. Share this manual and the README with the team to align on process expectations.

By following this manual, a team can convert the starter kit into a living governance system within a single sprint.
