# RJW-IDD Methodology Pack

This pack houses the source-of-truth guidance for Rolaand Jayz Wayz – Coding with Natural Language: Intelligence Driven Development (RJW-IDD).

## Directory Layout
- `core/` — enduring principles and lifecycle design (`METHOD-0001`).
- `governance/` — phase control, checklists, and role handbooks (`METHOD-0002`, `METHOD-0003`).
- `operations/` — execution playbooks for specialised use cases such as AI coding agents (`METHOD-0004`).
- `templates/` — boilerplates that downstream projects clone; prefixed with the artefact namespace they generate (e.g., `PROJECT-DEC-template.md`).

## How to Use
1. Treat every file as method-level doctrine. Only modify after capturing a new `DEC-####` in your project evidence stream.
2. Copy templates into a project workspace before editing; do **not** customise the originals.
3. Keep project artefacts (decisions, specs, ledgers, prompts) under a project-specific prefix to avoid collisions with the `METHOD-####` namespace.
4. Reference these documents from the starter kit (`rjw-idd-starter-kit/`) using relative paths so the bundle remains portable.

RJW-IDD deliberately keeps method guidance separate from project execution assets. The pack here describes *how* to operate; the starter kit provides reusable scaffolding that each project instantiates with its own IDs and evidence.

## Add-ins
- [3D Game Core](addons/3d-game-core/README.md) — governance, tooling, and prompts for deterministic 3D projects (enabled by default; toggle via `method/config/features.yml`).
- [Video AI Enhancer](addons/video-ai-enhancer/README.md) — real-time video enhancement governance (disabled by default; enable via the feature registry).

Edit `method/config/features.yml` (or run the helper scripts under `rjw-idd-starter-kit/scripts/addons/`) to adjust add-in state and then run `python rjw-idd-starter-kit/scripts/config_enforce.py` to confirm the declaration matches the on-disk assets.
