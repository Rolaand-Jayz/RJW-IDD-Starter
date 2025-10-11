# 3D Game Core Add-on

**Status:** Included (opt-in)  
**Registry Toggle:** `addons.3d_game_core.enabled` in `method/config/features.yml`

The 3D Game Core add-on extends RJW-IDD with determinism harnesses, tolerant replay tooling, performance/asset gates, and documentation tailored to 3D projects.

---

## Enabling / Disabling
### Using helper scripts (recommended)
```bash
# Enable and accept the default profile
python rjw-idd-starter-kit/scripts/addons/enable_3d_game_core.py

# Switch profiles (examples: generic, third_person, driving, networked)
python rjw-idd-starter-kit/scripts/addons/set_3d_profile.py --profile third_person

# Disable when not needed
python rjw-idd-starter-kit/scripts/addons/disable_3d_game_core.py
```

### Manual toggle
Edit `method/config/features.yml`:
```yaml
addons:
  3d_game_core:
    enabled: true
    profile: generic
```
Then run `python rjw-idd-starter-kit/scripts/config_enforce.py` to ensure the declared state matches the repository artefacts.

### Governance reminders
- Log the change in `docs/change-log.md`
- Capture the rationale in `docs/decisions/DEC-####.md`
- Update `logs/LOG-0001-stage-audits.md`

---

## What You Get
| Area | Location | Highlights |
| --- | --- | --- |
| Specs & Config | `config/`, `specs/`, `docs/` | Determinism, rollback, perf and asset governance templates |
| Tooling | `tools/` | Determinism harness, tolerant replay runner, asset linter, perf budget gate |
| Tests | `tests/` | Pytest suites covering the tooling for quick regression checks |
| Prompts | `prompts/` | Research packs, GDD helpers, pact generators, test navigator flows for 3D |
| Scripts | `../../scripts/addons/` | Enable/disable/profile helpers wired into the feature registry |

See the directory READMEs and acceptance docs (`ACCEPTANCE.md`, `docs/`) for deeper walkthroughs.

---

## Profiles
The add-on ships multiple profiles (`generic`, `third_person`, `driving`, `platformer`, etc.) that tailor budgets and tolerances in `config/3d-game-core.yml`. Use `set_3d_profile.py` to switch profiles and rerun the config guard afterwards.

---

## Validation
After any change to the add-on state:
1. Run `python rjw-idd-starter-kit/scripts/config_enforce.py`
2. Execute the guard suite (`pytest && bash scripts/ci/test_gate.sh`) before merging

Keeping the registry, docs, and tooling aligned ensures the RJW-IDD gate remains authoritative.
