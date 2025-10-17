# Slot Car Racing — 60-Minute Win

## What You'll Create

The final, polished game. You'll add **vehicle presets** (different cars with different handling), **menus** (professional launch and pause screens), and **advanced audio**. This is where your game becomes something you'd actually want to share.

**Time:** 30 minutes (60 minutes total from start)  
**Outcome:** Professional-quality, feature-complete game  
**Skill:** Managing multiple features with the RJW-IDD cycle

---

## Why This Stage Is Different

### The Real-World Problem: Scope Creep

By now, you might be thinking: *"I have a working game with physics. Now I want menus, different cars, better audio... but that's a lot of work."*

Here's the trap:

1. **Unclear Scope** — No spec says what "a menu" looks like. So the AI adds one thing, you want another, rework happens.
2. **Hidden Dependencies** — Vehicle presets need to change physics. Audio needs to match vehicles. If these aren't coordinated, things break.
3. **Scope Explosion** — Each feature becomes 10 features. You're still coding 2 hours later.
4. **No Rollback** — If menus get too complex, you can't easily remove them without breaking the game.

### The Solution: Prioritize & Iterate

Instead of "add all the features," you'll:

1. **Prioritize** — Decide: Which 2–3 features matter most in 30 minutes?
2. **Decide + Spec** for each feature.
3. **Code one feature at a time** — fully, then move to the next.
4. **Keep it modular** — Remove a feature later without breaking others.

---

## Step 1: Prioritize Your Features (2 minutes)

### Your Choices

In 30 minutes, pick **2–3 of these**:

| Feature | Time | Impact | Customization |
|---------|------|--------|----------------|
| **Vehicle Presets** | 10 min | High — makes game feel alive | 3 cars or 5? Different names? |
| **Launch Menu** | 8 min | High — first impression | Minimal or full settings? |
| **Pause Menu** | 5 min | Medium — quality-of-life | Simple or animated? |
| **Advanced Audio** | 8 min | Medium — polish | Engine variety or just pitch? |
| **Track Editor** | 12 min | Low — complex, less visible | Skip this; focus on other features |

### Our Recommendation

**For 60-minute win, pick:**
1. Vehicle Presets (high impact, reasonable time)
2. Launch Menu (sets tone)
3. Advanced Audio (feels professional)

**Skip:** Track editor (too complex for 30 min; can be added later).

---

## Feature #1: Vehicle Presets (10 minutes)

### Your Decision

**Question:** How many cars, and what should they feel like?

**Options:**
- **Option A (Recommended):** 3 cars — Light (fast, twitchy), Balanced (medium), Heavy (slow, stable).
- **Option B:** 5 cars — More variety, more personality.
- **Option C:** Custom — Design your own car archetypes.

**Pick one. Make it yours.**

### Write It Down

Create `docs/decisions/DEC-60min-vehicles.md`:

```markdown
# DEC-60min: Vehicle Presets

**Date:** Today  
**Decision:** Three vehicle presets with distinct handling.

**Why:** Three cars offer clear choice without overwhelming. Each has a different play style.

**Customization:** Light car is fast and fun, Balanced is default, Heavy is for precision players.
```

Commit:
```bash
git add docs/decisions/DEC-60min-vehicles.md
git commit -m "decision: three vehicle presets with distinct physics"
```

### Your Spec

Create `docs/specs/SPEC-60min-vehicles.md`:

```markdown
# SPEC-60min: Vehicle Presets

## Vehicles

| Name | Mass | Max Speed | Acceleration | Turning | Feel |
|------|------|-----------|--------------|---------|------|
| Light Cruiser | 0.6 | 6.0 | Fast (0.8s to max) | Twitchy | Arcade fun |
| Balanced Racer | 1.0 | 5.0 | Normal (1.0s to max) | Responsive | Goldilocks |
| Heavy Tank | 1.5 | 3.5 | Slow (1.5s to max) | Smooth | Precision play |

## UI Requirements

1. **Vehicle Selection Screen:**
   - Show 3 buttons, one for each vehicle.
   - Display vehicle name, icon, and brief description.
   - Highlight the currently selected vehicle.

2. **In-Game Display:**
   - Show currently selected vehicle name in HUD.
   - Vehicle switches immediately when selected (no restart needed for testing).

3. **Persistence:**
   - Remember the player's choice when they restart.
```

Commit:
```bash
git add docs/specs/SPEC-60min-vehicles.md
git commit -m "spec: three vehicle presets with distinct physics parameters"
```

### The AI Prompt

```
I have a slot car game with physics and audio (tutorials/slot-car-30-minute-win/).
I want to add vehicle presets: Light, Balanced, Heavy — each with different mass, max speed, acceleration.

Here's my spec (SPEC-60min-vehicles.md):
- Light: mass 0.6, max_speed 6.0, accelerates in 0.8s
- Balanced: mass 1.0, max_speed 5.0, accelerates in 1.0s
- Heavy: mass 1.5, max_speed 3.5, accelerates in 1.5s

Your task:
1. Create a tutorials/slot-car-60-minute-win/ by copying the 30-minute version.
2. Add a vehicle selection UI (3 buttons, each showing vehicle name + description).
3. Modify the physics engine to use selected vehicle's parameters.
4. Store the selected vehicle in browser localStorage so it persists.
5. Update the HUD to show the current vehicle name.
6. Test: switching vehicles should change how the car handles immediately.

Keep code clean and modular. Document vehicle parameters as comments.
```

### Customize It

- **More vehicles?** Ask for 5 instead of 3.
- **Different names?** Change "Light Cruiser" to "Spaceship" or "Cat" or anything you want.
- **Different parameters?** Adjust mass, acceleration, max speed to match your vision.

---

## Feature #2: Launch Menu (8 minutes)

### Your Decision

**Question:** How polished should the launch menu be?

**Options:**
- **Option A (Recommended):** Clean and simple. Title, vehicle selector, Play button, settings toggle.
- **Option B:** Minimal. Just a Play button.
- **Option C:** Elaborate. Animations, intro video, tutorial overlay.

**Pick one.**

### Write It Down

Create `docs/decisions/DEC-60min-launch-menu.md`:

```markdown
# DEC-60min: Launch Menu Design

**Date:** Today  
**Decision:** Clean, professional launch menu.

**Why:** Sets tone for the game. Shows quality without being overwhelming.

**Future:** If we want more polish later, add animations and backgrounds.
```

Commit:
```bash
git add docs/decisions/DEC-60min-launch-menu.md
git commit -m "decision: professional launch menu with vehicle selection"
```

### Your Spec

Create `docs/specs/SPEC-60min-launch-menu.md`:

```markdown
# SPEC-60min: Launch Menu

## Layout

1. **Title Section:**
   - Game title centered at top.
   - Simple, readable font.

2. **Vehicle Selection:**
   - Show 3 vehicle buttons (reuse from Feature #1).
   - Highlight currently selected.

3. **Settings:**
   - Mute button (audio on/off).
   - Volume slider (0–100%).

4. **Play Button:**
   - Prominent, clickable.
   - Takes user into game.

## UX Requirements

- Menu is responsive (works at any window size).
- All buttons are keyboard-navigable (Tab to move, Enter to click).
- Play button always visible and accessible.

## Visual

- Background: solid color or subtle gradient.
- Text: high contrast, readable.
- Buttons: clear affordance (looks clickable).
```

Commit:
```bash
git add docs/specs/SPEC-60min-launch-menu.md
git commit -m "spec: professional launch menu with vehicle selection and settings"
```

### The AI Prompt

```
I want to add a launch menu to my slot car game.

Here's my spec (SPEC-60min-launch-menu.md):
- Title at top.
- Vehicle selection (3 buttons from Feature #1).
- Mute and volume controls.
- Play button.
- Keyboard navigable.

Your task:
1. Create a "menu" screen that appears before the game starts.
2. Show the game title.
3. Show the 3 vehicle selector buttons.
4. Add mute toggle and volume slider.
5. Add a Play button that starts the game.
6. Hide the menu when Play is clicked; show it again if player presses Escape.
7. Keep it clean and professional (no animations yet, just solid design).

Test: menu should be fully functional. All controls work.
```

### Customize It

- **Different title?** Change "Slot Car Racing" to your game's name.
- **No settings?** Remove the mute/volume controls and keep it minimal.
- **Animations?** Ask the AI to add fade-in/slide animations to menu elements.

---

## Feature #3: Advanced Audio (8 minutes)

### Your Decision

**Question:** What should the audio feel like?

**Options:**
- **Option A (Recommended):** Engine pitch changes with speed + UI sounds (button clicks, menu transitions).
- **Option B:** Simple. Just keep the current engine loop.
- **Option C:** Elaborate. Different engine samples for each vehicle + background music.

**Pick one.**

### Write It Down

Create `docs/decisions/DEC-60min-audio.md`:

```markdown
# DEC-60min: Audio Strategy

**Date:** Today  
**Decision:** Responsive engine pitch + UI feedback sounds.

**Why:** Makes game feel alive and responsive. Minimal complexity.

**Future:** Can add background music, different engines per vehicle later.
```

Commit:
```bash
git add docs/decisions/DEC-60min-audio.md
git commit -m "decision: responsive audio with UI feedback"
```

### Your Spec

Create `docs/specs/SPEC-60min-audio.md`:

```markdown
# SPEC-60min: Advanced Audio

## Engine Sound

1. **Pitch Modulation:**
   - Light car: pitch ranges 250–900 Hz.
   - Balanced car: pitch ranges 200–800 Hz.
   - Heavy car: pitch ranges 180–700 Hz.
   - Pitch smoothly follows speed (no jumps).

2. **Volume:**
   - Engine volume tied to speed (silent at 0, full at max).
   - Doesn't distort or clip.

## UI Sounds

1. **Button Click:**
   - Short beep (200 ms) when any button is clicked.
   - Different pitch than engine (200 Hz for contrast).
   - Volume: 0.4 (moderate, not too loud).

2. **Menu Transitions:**
   - Soft whoosh sound when menu appears/disappears (optional).

## Mute Functionality

- Mute button completely silences all audio.
- Unmute restores all audio.
```

Commit:
```bash
git add docs/specs/SPEC-60min-audio.md
git commit -m "spec: responsive audio with UI feedback sounds"
```

### The AI Prompt

```
I want to enhance audio in my slot car game.

Here's my spec (SPEC-60min-audio.md):
- Engine pitch varies by vehicle (Light: 250–900 Hz, Balanced: 200–800 Hz, Heavy: 180–700 Hz).
- Engine pitch smoothly follows speed.
- UI click sound: 200 Hz beep, 200 ms, volume 0.4.
- Mute button controls all audio.

Your task:
1. Modify the existing Web Audio API code to support different pitch ranges per vehicle.
2. Add a UI click sound that plays whenever a button is pressed.
3. Ensure the mute button silences both engine and UI sounds.
4. Test: each vehicle should have a distinct engine sound pitch range.

Keep code clean. Document pitch ranges as comments.
```

### Customize It

- **Different pitch ranges?** Ask for custom frequencies.
- **Different UI sound?** Replace the beep with a more elaborate sound design.
- **Add music?** Ask for background music in the menu and game.

---

## Step 2: Implement Features (20 minutes)

### The Process

For each feature:

1. **AI writes code** based on your spec.
2. **You review** the code against the spec checklist.
3. **You test** in the browser.
4. **You iterate** if something's wrong.
5. **You commit** when it works.

### Example Flow

**You:** "Here's my spec for vehicle presets. Write the code."

**AI:** [Provides code for vehicle selection, physics updates, localStorage.]

**You:** "Does this match the spec?"
- [ ] Vehicle buttons show correctly?
- [ ] Physics change when you switch vehicles?
- [ ] Vehicle choice persists after reload?

**You test in browser:**
- Switch vehicles.
- Reload page (vehicle choice persists?).
- Verify physics feel different.

**You:** "Perfect. Committing."

---

## Step 3: Commit & Verify (5 minutes)

For each feature:

```bash
git add tutorials/slot-car-60-minute-win/
git add docs/
git commit -m "feature: [vehicle presets | launch menu | advanced audio]"
```

Create a change log:

```bash
cat > logs/change-60min.md << 'EOF'
# Change: 60-Minute Win — Complete Game

## What Changed
- Vehicle presets: Light, Balanced, Heavy with distinct physics.
- Launch menu: professional UI with vehicle selector and settings.
- Advanced audio: engine pitch varies by vehicle; UI click sounds.

## Specs
- SPEC-60min-vehicles.md
- SPEC-60min-launch-menu.md
- SPEC-60min-audio.md

## Verification
- All 3 vehicles available and selectable.
- Vehicle choice persists across page reloads.
- Launch menu is functional and keyboard-navigable.
- Engine sounds different for each vehicle.
- UI sounds play on button clicks.
- Mute toggle works.

## Next
Game is complete! Time to play, share, and iterate based on feedback.
EOF

git add logs/change-60min.md
git commit -m "log: 60-minute win completion"
```

---

## Customization Ideas: Make It Truly Yours

Now that you have a complete game, here are some ways to personalize it:

### Physics Tweaks
- Add a "drift mode" — hold a key to enable power sliding.
- Tire warmup: car handles better as it accelerates.
- Fuel consumption: car slows down over time (arcade mechanics).

### Visual Enhancements
- Vehicle images: custom art for each car.
- Track theme: change colors based on selected vehicle.
- HUD redesign: add lap counter, best lap time, speed gauge.

### Gameplay Additions
- Obstacles on the track (cones, barriers).
- Checkpoints and lap timing.
- Multiplayer (local two-player split-screen).

### Audio Depth
- Multiple engine samples per vehicle (realistic engines sound different at different RPMs).
- Collision sounds.
- Wind/environment ambience.

**Pick 1–2 ideas. Ask the AI to implement them.** This is where your game becomes unique.

---

## Why This Process Worked

1. **Prioritize** — You chose features that fit in 30 minutes.
2. **Decide** — Each feature has a decision explaining the "why."
3. **Spec** — Clear requirements prevent rework.
4. **Code** — The AI implements based on specs.
5. **Test & Iterate** — You verify before moving on.
6. **Document** — Change logs and decisions are recorded.

**A single prompt cannot do this.** The framework made the complex simple.

---

## You Built This

You didn't copy-paste code. You didn't follow a video tutorial. You **designed** a game using a structured methodology that real teams use to build real software.

You:
- Made decisions and documented them.
- Wrote specs so the AI knew what "done" means.
- Tested and iterated.
- Maintained traceability (why did we do this? check the decision).
- Kept control (it's your game, your vision, your choices).

**This is what it means to build software safely with AI.**

---

## What's Next?

### Option 1: Expand Your Game
- Add features from the "Customization Ideas" section.
- Follow the same cycle: Decide → Spec → Code → Verify → Log.

### Option 2: Try Another Project
- Apply this framework to a different project (web app, tool, service, etc.).
- The cycle works for any software.

### Option 3: Contribute Back
- Share your game with others.
- Share your specs and decisions.
- Show how this methodology works in practice.

---

## Final Thought

**You started with a blank canvas 60 minutes ago. Now you have a playable, polished, professional-quality game.**

More importantly, **you understand how to build software with an AI partner that's trustworthy, traceable, and controllable.**

That's the point of this tutorial.

Go build something amazing.

---

**Congrats on completing the 60-Minute Win.** 🎉
