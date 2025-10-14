# Video AI Enhancer Add-on

**Status:** Included (opt-in)  
**Registry Toggle:** `addons.video_ai_enhancer.enabled` in `method/config/features.yml`

The Video AI Enhancer add-on equips RJW-IDD with latency/quality/storage governance, specs, and tooling for real-time video enhancement and upscaling pipelines.

---

## Enabling / Disabling
### Using helper scripts (recommended)
```bash
# Enable with the default baseline profile
python rjw-idd-starter-kit/scripts/addons/enable_video_ai_enhancer.py

# Switch profiles (baseline, live_stream, broadcast_mastering, mobile_edge, remote_collab)
python rjw-idd-starter-kit/scripts/addons/set_video_ai_profile.py --profile live_stream

# Disable when you no longer need the add-on
python rjw-idd-starter-kit/scripts/addons/disable_video_ai_enhancer.py
```

### Manual toggle
```yaml
addons:
  video_ai_enhancer:
    enabled: true
    profile: baseline
```
Edit the block in `method/config/features.yml`, then run `python rjw-idd-starter-kit/scripts/config_enforce.py` to confirm the registry and filesystem are aligned.

### Governance reminders
- Record a change entry in `templates-and-examples/templates/change-logs/CHANGELOG-template.md`
- Capture the decision in `docs/decisions/`
- Update the audit log (`logs/LOG-0001-stage-audits.md`)

---

## What You Get
| Area | Location | Highlights |
| --- | --- | --- |
| Specs & Runbooks | `specs/`, `docs/` | Quality, latency, storage controls; operational guidance |
| Tooling | `tools/` | Latency guard, storage validator, quality gate, ID validators |
| Tests | `tests/` | Coverage for each guard and validator |
| Prompts | `prompts/` | Research packs, change navigator, reconciliation helpers |
| Scripts | `../../scripts/addons/` | Enable/disable/profile scripts integrated with the feature registry |

Consult `docs/` for acceptance criteria and implementation notes.

---

## Profiles
Profiles tailor budgets and guard thresholds for different delivery scenarios (`baseline`, `live_stream`, `broadcast_mastering`, `mobile_edge`, `remote_collab`). Adjust them with `set_video_ai_profile.py` and re-run the configuration guard afterwards.

---

## Validation
After toggling or reconfiguring the add-on:
1. Run `python rjw-idd-starter-kit/scripts/config_enforce.py`
2. Execute `pytest && bash scripts/ci/test_gate.sh` before committing the change

Keeping the feature registry, docs, and tooling in sync preserves the integrity of the RJW-IDD gate.
