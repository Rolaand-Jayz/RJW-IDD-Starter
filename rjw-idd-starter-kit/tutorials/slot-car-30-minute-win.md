# Slot Car Racing — 30-Minute Win

Purpose
- Migrate the browser prototype to a desktop wrapper (Electron, Tauri, or equivalent chosen by the author), add basic physics (friction, simple gravity baseline for grounded vehicle sense, and inertia/momentum), include basic sound (engine hum and simple UI clicks), and apply a focused layer of polish to visuals and interactions established at 15 minutes.

Prerequisites
- Completed 15-Minute Win deliverables: project structure, assets (car and oval track), input mapping, camera framing.
- Familiarity with the chosen desktop wrapper (Electron/Tauri) basic packaging concepts and simple build commands.

What this stage delivers (strict scope)
- Platform: Desktop via chosen wrapper (Electron/Tauri). The same codebase should be runnable in the browser (from the 15-minute stage) and packaged for desktop.
- Physics: Add simple friction, a basic gravity constant applied as a grounding force (for visual realism; the car remains on track), and inertia/momentum so acceleration and braking feel weighted.
- Sound: Basic engine loop tied to throttle input (volume/pitch modulation based on speed) and UI click for Start/Pause.
- Polish: Improve sprite scaling, add subtle particle or exhaust effect when accelerating (design description only), smoothing of rotation and movement for visual quality.

Step sequence (design-only, time-boxed)
1. Decision & migration plan (3 minutes)
	- Decide which desktop wrapper to use (author choice). Document the reason (e.g., Electron for broad compatibility; Tauri for smaller binary).
	- Success criteria: Able to launch the existing web build inside the desktop wrapper and confirm rendering and inputs work.

2. Physics design (8 minutes)
	- Core parameters to add:
	  - Mass: lightweight value influencing acceleration rate.
	  - Throttle force: how input translates to forward acceleration.
	  - Friction coefficient: slows the car when throttle releases (simple linear drag is acceptable).
	  - Inertia/momentum: apply velocity vector and dampening instead of immediate position snaps.
	- Gravity (visual grounding): a constant that helps keep the car visually glued to the 2D plane—no jumping or flight behavior required.
	- Decide update loop frequency and how physics integrates with rendering (fixed time-step recommended for stability).

3. Sound design (5 minutes)
	- Audio assets: engine loop (short sample), UI click sound (short SFX). Use simple, short-length files (e.g., ~1 second engine loop, 50–100ms click).
	- Mapping: engine pitch/volume scales with current speed. UI click plays on Play/Pause interactions.
	- Accessibility: allow global mute toggle in the UI.

4. Visual polish & UX (6 minutes)
	- Smooth interpolation for position/rotation to hide frame jitter.
	- Add subtle particle/exhaust effect while throttle > threshold (design spec only: small fade-out sprites or canvas particles).
	- UI: Add Play/Pause button, a small speedometer readout, and a desktop-native window title (in wrapper). Keep layout minimal and readable.

5. Packaging & verification (8 minutes)
	- Migration verification: run the project inside the chosen wrapper and validate inputs and rendered scene match the browser behavior.
	- Performance check: the scene runs at stable frame rate on a modest laptop; physics updates are stable and movement feels weighted.

What is carried forward
- All assets, input mapping, and camera framing from the 15-minute stage.
- The single-scene layout and project structure.

Success criteria (explicit)
- The project runs inside the chosen desktop wrapper and the following behaviors are present:
  - Velocity/inertia: accelerating increases speed over time; releasing throttle causes car to slow due to friction.
  - Steering combined with inertia produces smooth turns (no instant snaps).
  - Engine audio plays and scales with speed; Play/Pause clicks produce SFX.
  - Desktop wrapper launch succeeds and the UI shows Play/Pause and a speed readout.

Time budget guidance
- Keep level of physics minimal and deterministic — target completing the migration, physics integration, and basic audio in ~30 minutes by a novice following precise steps.

Next step pointer
- The 60-minute Win will deepen physics, add vehicle selection, richer audio, and a small track editor while delivering AAA polish to the pause and launch menus.
