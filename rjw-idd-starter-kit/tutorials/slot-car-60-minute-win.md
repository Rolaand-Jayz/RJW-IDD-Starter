# Slot Car Racing — 60-Minute Win

Purpose
- Extend the desktop project with enhanced physics, vehicle selection, improved audio, and a simple track editor composed of modular pieces. Deliver AAA-quality polish for the game and for a pause and launch menu at the same level.

Prerequisites
- Completed 30-Minute Win deliverables: desktop-wrapped project with basic physics and sound, polished visuals, and Play/Pause UI.

What this stage delivers (strict scope)
- Physics: Improved handling (tighter velocity integration, better angular response), refined friction model, optional simple suspension visual (no full 3D suspension required), and tunable parameters for mass/inertia per vehicle.
- Vehicle selection: UI to pick from multiple vehicle presets (each with tuned mass, throttle, steering sensitivity).
- Sounds: Multiple enhanced audio assets (engine samples for each vehicle, improved UI sounds, collision/impact SFX if desired — design only). Audio mixing/tuning guidance is included.
- Track editor: A small in-app editor that composes the oval track from modular pieces (straight, gentle curve, sharp curve). Editor exposes a simple grid/snap system so users can assemble tracks and save/load layouts. Editor is design-only (no implementation code here).
- Menus: Deliver a polished pause menu and a launch (main) menu with AAA-level details — clear typography, animations (fade/slide), and focus on input affordances.

Step sequence (design-only, time-boxed)
1. Decide vehicle presets & data model (5 minutes)
	- Create 3 vehicle presets (e.g., "Light Cruiser", "Balanced Racer", "Heavy Tank") with explicit tuning values: mass, max throttle, steering sensitivity, drag coefficient.
	- Success criteria: UI shows three choices and selecting one updates the vehicle parameters for the physics system.

2. Improve physics model (20 minutes)
	- Replace simple linear drag with a more realistic combined model:
	  - Velocity-dependent drag (quadratic term) for higher speeds.
	  - Angular damping to stabilize rotation.
	  - Use a semi-implicit Euler integrator or small fixed time-step for stability.
	- Tuning guidance: provide example parameter ranges and a small table showing how they affect feel (e.g., mass 0.8–1.8, drag 0.1–0.5).
	- Success criteria: Each vehicle preset results in distinct and believable handling characteristics.

3. Audio improvement plan (8 minutes)
	- Provide multi-sample engine layers or pitch-shifting strategies to avoid audible artifacts.
	- Add UI sound polish: menu hover, menu select, and subtle background ambience in launch menu.
	- Success criteria: Audio mixes cleanly, engine pitch/volume responds smoothly to speed, and UI sounds feel responsive and appropriately loud relative to engine.

4. Track editor design (12 minutes)
	- Editor features (minimal, required): modular pieces (straight, curve gentle/curve sharp), grid snapping, rotate/mirror piece, delete, save layout JSON.
	- UX: Provide a simple palette of pieces and a canvas with a visible grid. Provide an explicit "Export layout" button that outputs a simple JSON array of piece types and positions.
	- Editor constraints: Ensure exported layouts can be loaded by the game scene unchanged (design the data schema but do not implement it here).
	- Success criteria: A designer can assemble an oval-like track from pieces and export a layout describing piece sequence and transforms.

5. Menus & AAA polish (10 minutes)
	- Launch menu: polished title, vehicle selection UI, "Play" button, settings (audio mute, volume sliders), and small tutorial text.
	- Pause menu: smooth animated overlay, resume, restart, exit-to-launch, and small snapshot of current stats (speed, current vehicle).
	- Visual polish checklist: consistent typographic scale, high-quality icons, micro-animations (fade/slide), and keyboard/gamepad focus support.
	- Success criteria: Menus feel cohesive and are navigable with keyboard/mouse (and gamepad if present). Animations are subtle and responsive.

6. Integration & verification (5 minutes)
	- Integration checklist: vehicle selection changes physics params immediately, track editor export can be loaded by the scene, audio test for each vehicle.
	- Final verification: confirm the game and menus run smoothly on the target desktop wrapper with the new features, and that the highest-polish visuals and menu animations are present.

What is carried forward
- All code/data from the 30-minute Win: physics baseline, desktop packaging, audio pipeline, and polish patterns.

Success criteria (explicit)
- The desktop application provides:
  - Multiple vehicles selectable in the launch menu with distinct handling and tuned physics parameters.
  - Engine and UI audio that respond smoothly and are clearly improved over the 30-minute stage.
  - A basic track editor that exports a simple composable layout (JSON) describing the modular piece placements.
  - A launch and pause menu with AAA-level polish (coherent visual language, micro-animations, keyboard/gamepad accessibility).

Time budget guidance
- This stage is the heaviest and is intended to be completed in ~60 minutes by a motivated novice following the design precisely; the focus should be on high-impact polish and deterministic, stable features rather than exhaustive content.

Next step pointer
- After this stage learners have a production-quality slot-car tech demo with packaging, physics, audio, vehicle presets, a track editor, and polished menus — a credible foundation for further expansion.
