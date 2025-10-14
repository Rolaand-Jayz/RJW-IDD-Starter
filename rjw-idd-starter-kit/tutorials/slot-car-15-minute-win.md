# Slot Car Racing — 15-Minute Win

Purpose
- Provide a working, browser-playable minimal slot-car experience where the player can drive a car around a simple oval track. This stage demonstrates the smallest playable loop and establishes the baseline project structure for later stages.

Prerequisites
- Basic familiarity with a text editor and running a local static web server (one command such as `python -m http.server` is sufficient). No prior game-development experience required.
- A directory in the repo for this tutorial (we assume `tutorials/slot-car-15-minute-win` as working area).

What this stage delivers (strict scope)
- Platform: Web browser only.
- Track: Single oval track (visual only).
- Controls: Simple drive control (e.g., accelerate/steer left/right). Keep input mapping minimal and discoverable.
- Physics: None. Movement is deterministic and scripted (no friction, no gravity, no collision resolution).
- UI: Minimal HUD showing a "Play" button and a small indicator for current speed (optional). No menus.

Step sequence (design-only, novice-friendly)
1. Purpose & success criteria (1 minute)
	- Purpose: Confirm the goal — make a car sprite move around an oval when player presses drive input.
	- Success criteria: In the browser the user can press a key (or click a visible control) and the car travels around the oval repeatedly; the scene visually loops.

2. Project scaffolding & assets (2 minutes)
	- Decide file layout: index.html, styles.css, assets/ (images), and a single JS entry file (placeholder). Note: implementation files will be created in code stage, but here you only design their purpose.
	- Asset plan: one car sprite (top-down view) and one simple oval track image or background. Placeholder size guidance: 512x512 PNG for the track, 128x64 PNG for the car.

3. Input & control design (3 minutes)
	- Map controls: "Arrow Up" (accelerate), "Arrow Left/Right" (steer). Alternatively provide on-screen buttons for mobile.
	- Behavior design: When accelerate is pressed, the car moves forward along the current heading. Steering rotates the heading. There is no physics — movement is position/rotation updates applied each frame.
	- Edge behavior: When the car reaches the end of the oval path, continue seamlessly (wrap around). No collision detection required.

4. Visual composition & camera (3 minutes)
	- Decide camera view: Fixed top-down camera centered on the track (no scrolling required). Keep a consistent scale so the car and track are clearly visible in a single browser viewport.
	- Polishing guidance: Use crisp sprites, simple anti-aliased edges, and a subtle drop shadow for the car to make visuals look intentional even at this basic stage.

5. Play loop & verification (4 minutes)
	- Define the play loop: Player starts the scene, presses accelerate to move and steer to follow the oval. No win condition required — this stage is about a working loop.
	- Verification checklist:
	  - Car moves when accelerate is pressed.
	  - Steering changes the car heading and visually rotates the sprite.
	  - The car follows the oval repeatedly without stopping or jittering.
	  - The page runs in a modern browser and the inputs are responsive.

What is carried forward
- Project structure (index, assets, single JS entry) and assets (car and track placeholders) are reused by the 30-minute stage.
- Input mapping decisions and camera framing are preserved and become the baseline for adding physics later.

Success criteria (explicit)
- In a modern browser: pressing the accelerate input causes a car sprite to move forward and continue around an oval track; steering rotates the car and affects its path; the scene loops visually without errors. No physics, no menus, and no packaging required.

Time budget guidance
- Keep code and assets minimal — this design is intended to be implemented by a novice in ~15 minutes.

Next step pointer
- The 30-minute Win will take the same project files and add physics, desktop packaging via Electron/Tauri/equivalent, basic audio, and a layer of polish to the visuals and interactions.

Copy-paste prompts for novices (dynamic)
-------------------------------------

The starter kit includes dynamic, novice-friendly prompt templates that you can copy-paste into the assistant to perform common tasks. These prompts include placeholders which the assistant will fill from the repository state where possible. If a placeholder is missing, the assistant will ask for it.

Use-case: run the bootstrap, verify guard examples, run tests, and optionally build and inspect the package. Copy an entire prompt below and paste it to your agent input.

1) Bootstrap the project (dynamic prompt)

Use the helper to generate a context-aware prompt that you can paste to the assistant. This keeps the prompt accurate for forks or renamed roots.

Generate the prompt locally (copy-paste into your terminal):

```bash
python rjw-idd-starter-kit/tools/prompt_helper.py bootstrap --project-root . --python-bin python3.11
```

The helper prints a copyable prompt; paste the printed prompt into the assistant. The assistant will run or instruct you to run the exact command (for example: `bash rjw-idd-starter-kit/scripts/setup/bootstrap_project.sh`).

2) Activate virtualenv (dynamic prompt)

Generate the activation prompt:

```bash
python rjw-idd-starter-kit/tools/prompt_helper.py activate_venv --project-root .
```

Paste the printed prompt into the assistant; it will describe how to activate `.venv` and which commands to run to verify the python executable.

3) Run governance guard on the pass fixture (dynamic prompt)

Generate the prompt:

```bash
python rjw-idd-starter-kit/tools/prompt_helper.py guard_ok --project-root .
```

Paste the generated prompt to the assistant; it will print exact commands the novice can run and the expected verification steps.

4) Run governance guard on the fail fixture (dynamic prompt)

Generate the prompt:

```bash
python rjw-idd-starter-kit/tools/prompt_helper.py guard_bad --project-root .
```

Paste the generated prompt to the assistant; it will instruct how to run the guard and how to interpret violations.

5) Run tests (dynamic prompt)

Generate the prompt:

```bash
python rjw-idd-starter-kit/tools/prompt_helper.py pytest --project-root .
```

Paste the generated prompt into the assistant; it will instruct the novice on running `pytest` and how to read failures.

6) Build and inspect package (dynamic prompt)

Generate the prompt:

```bash
python rjw-idd-starter-kit/tools/prompt_helper.py build_inspect --project-root .
```

Paste the generated prompt into the assistant; it will provide the exact build and inspection commands and the expected outputs to verify examples were included.

Deviation & Gate behavior (important)
-----------------------------------

- If you paste a prompt that asks the agent to modify governance logic (for example "disable guard rules" or "remove test"), the assistant will refuse and explain which gate would be violated (for example: GATE_GUARD_MODIFICATION). It will not silently change or remove gate logic.
- If you deviate by asking the assistant to perform privileged actions (writing to system directories) the assistant will refuse and explain GATE_PRIVILEGED_WRITE.
- If you insist and the assistant attempts a best-effort, it will stop at the first failing gate and report that gate and why it prevented further progress.
- These refusals are polite and advise the safe path (for example, run bootstrap first, or run tests and fix failures before publishing).

Where these prompts come from
----------------------------
The prompts are derived from `rjw-idd-starter-kit/prompts/DYNAMIC_PROMPTS.md` and can be generated programmatically by the helper `rjw-idd-starter-kit/tools/prompt_helper.py` which produces dynamic prompts that embed repository paths and python binary hints.
