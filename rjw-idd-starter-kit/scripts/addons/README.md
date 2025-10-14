# RJW-IDD Add-on Management Scripts

This directory contains scripts for enabling, disabling, and configuring RJW-IDD add-ons.

## Available Add-ons

### 3d-game-core
Augments RJW-IDD for 3D game development with determinism harnesses, replay systems, asset and performance gates, and game design document templates.

**Scripts:**
- `enable_3d_game_core.py` - Enable the 3D game core add-on
- `disable_3d_game_core.py` - Disable the 3D game core add-on
- `set_3d_profile.py` - Set the 3D game profile

**Available Profiles:**
- `generic` - General 3D game (default)
- `first_person` - First-person perspective
- `third_person` - Third-person perspective
- `isometric` - Isometric/2.5D
- `platformer` - Platformer game
- `driving` - Driving/racing game
- `action_rpg` - Action RPG
- `networked` - Networked multiplayer game

### video-ai-enhancer
Augments RJW-IDD for real-time video enhancement and upscaling pipelines with quality, latency, and storage governance.

**Scripts:**
- `enable_video_ai_enhancer.py` - Enable the video AI enhancer add-on
- `disable_video_ai_enhancer.py` - Disable the video AI enhancer add-on
- `set_video_ai_profile.py` - Set the video AI enhancer profile

**Available Profiles:**
- `baseline` - Baseline configuration (default)
- `live_stream` - Live streaming optimization
- `broadcast_mastering` - High-bitrate broadcast mastering
- `mobile_edge` - Mobile edge computing
- `remote_collab` - Remote collaboration

## Usage

### Enabling an Add-on

```bash
# Enable 3D game core
python scripts/addons/enable_3d_game_core.py

# Enable video AI enhancer
python scripts/addons/enable_video_ai_enhancer.py
```

### Setting a Profile

```bash
# Set 3D game profile
python scripts/addons/set_3d_profile.py --profile third_person

# Set video AI profile
python scripts/addons/set_video_ai_profile.py --profile live_stream
```

### Disabling an Add-on

```bash
# Disable 3D game core
python scripts/addons/disable_3d_game_core.py

# Disable video AI enhancer
python scripts/addons/disable_video_ai_enhancer.py
```

## Requirements

These scripts require PyYAML to read and write the feature registry:

```bash
pip install pyyaml
```

This is automatically installed when you run `scripts/setup/bootstrap_project.sh`.

## Feature Registry

Add-on state is tracked in `method/config/features.yml`. Each add-on has:
- `enabled`: Boolean flag
- `version`: Version number
- `profile`: Active profile name
- `description`: Add-on description

## Governance

When enabling, disabling, or changing add-on configuration:

1. **Update the Change Log** - Add an entry to `templates-and-examples/templates/change-logs/CHANGELOG-template.md` with the change ID and impacted add-on
2. **Record the Decision** - Document why the add-on was enabled/disabled in `docs/decisions/`
3. **Update Audit Log** - Note the change in `logs/LOG-0001-stage-audits.md`

## Bootstrap Integration

The `scripts/bootstrap/install.sh` script prompts for add-on selection during initial setup:
- Presents available add-ons
- Enables the selected add-on
- Prompts for profile selection
- Provides reminders about governance requirements
