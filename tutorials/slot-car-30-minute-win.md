# Slot Car Racing — 30-Minute Win

## What You'll Build

You'll take the playable game from 15 minutes and add **physics** (acceleration, friction, inertia) and **audio** (engine sound that changes pitch with speed). The game will feel real—cars have weight, momentum, and personality.

**Time:** 15 minutes (30 minutes total from start)  
**Outcome:** Polished, physics-based game with audio  
**Skill:** Using the RJW-IDD cycle for **iterative feature addition**

---

## Why This Matters: Beyond a Single Prompt

### The Problem: Feature Creep & Rework

You finish the 15-minute game and think: *"I want to add physics."* So you ask an AI:

> "Add physics to my slot car game."

Here's what usually happens:

1. **Poor Context** — The AI doesn't know your code structure. It rewrites the entire game instead of modifying it.
2. **Related Error** — The new physics breaks the controls you already had working.
3. **Broken Feature** — Now your steering is weird. The car accelerates too fast. You spend 2 hours debugging.
4. **Agent Shortcoming** — The AI can't explain its physics equations. You don't trust the numbers.
5. **What's Missing** — No **spec** for what "good physics" means. No **tests** to verify it works. No **decision** about which physics model to use.

### The Solution: Test-Driven Development

Instead, you'll:

1. **Decide** — We want realistic-feeling acceleration, not instant speed.
2. **Spec** — Define friction coefficient, max speed, acceleration rate.
3. **Write tests** — Verify the car accelerates smoothly, decelerates naturally, etc.
4. **Ask the AI** — "Implement this spec and pass these tests."
5. **Verify** — Run the tests. If they pass, the feature works. If they fail, ask for fixes.

**This prevents rework.** Tests catch problems before you spend time debugging.

---

## Step 1: Make a Decision (2 minutes)

### Your Decision

**Question:** What physics model should the car use?

**Options:**
- **Option A (Recommended):** Simple realistic. Car accelerates smoothly, has momentum, friction slows it down. Feels natural.
- **Option B:** Arcade-y. Car reaches top speed instantly. Feels twitchy and fun (like old arcade racers).
- **Option C:** Simulation-heavy. Complex friction curves, tire grip, drift mechanics. More complex.

### Your Call

Pick what sounds fun to you. This is your project.

**For this tutorial, we'll assume Option A** (realistic), but the framework supports all three.

### Write It Down (30 seconds)

Create `docs/decisions/DEC-30min-physics-model.md`:

```markdown
# DEC-30min: Physics Model Choice

**Date:** Today  
**Decision:** Realistic-feeling acceleration and momentum.

**Why:** Feels responsive and natural. Not too complex. Good foundation for later enhancements.

**Reversal:** If it feels too slow, we can increase acceleration or decrease friction.
```

Commit:
```bash
git add docs/decisions/DEC-30min-physics-model.md
git commit -m "decision: choose realistic physics model for acceleration/friction"
```

---

## Step 2: Write a Spec (3 minutes)

### Your Spec

Create `docs/specs/SPEC-30min-physics-and-audio.md`:

```markdown
# SPEC-30min: Physics & Audio

## Physics Requirements

1. **Acceleration:**
   - Car speed increases smoothly when throttle (ArrowUp) is held.
   - Takes ~1 second to reach max speed from standstill.
   - Max speed: 5 units/frame.

2. **Deceleration:**
   - When throttle is released, car slows down smoothly.
   - Takes ~2 seconds to stop from max speed.
   - Never goes negative (no backwards motion).

3. **Turning:**
   - Turn rate increases with speed (faster cars are more responsive).
   - At low speed (1 unit/frame), turning is slow.
   - At high speed (5 units/frame), turning is fast.
   - No oversteer or unrealistic drifting.

4. **Edge Cases:**
   - Car doesn't teleport or jump.
   - Speed doesn't overshoot max speed.
   - Turning while accelerating feels natural.

## Audio Requirements

1. **Engine Sound:**
   - Plays continuously while moving.
   - Pitch increases with speed (200 Hz at idle, 800 Hz at max speed).
   - Can be toggled off with a mute button.

2. **UI Click:**
   - Play/Pause button makes a short beep when clicked.
   - Optional if not enough time.

## Success Criteria

- Game runs smoothly (60 FPS).
- Physics feels responsive and natural.
- Audio responds to speed changes.
- No crashes or console errors.
```

Commit:
```bash
git add docs/specs/SPEC-30min-physics-and-audio.md
git commit -m "spec: physics and audio requirements for 30-minute stage"
```

---

## Step 3: Give the AI a Prompt (2 minutes)

Now you'll ask your AI assistant to upgrade the game. Here's your prompt:

### The Prompt

Copy and paste into your chat:

```
I have a playable slot car game in tutorials/slot-car-15-minute-win/. 
Now I want to add realistic physics and audio to make it feel more polished.

Here's my spec (SPEC-30min-physics-and-audio.md):

Physics:
- Car accelerates smoothly over ~1 second to reach max speed (5 units/frame).
- When throttle is released, car decelerates over ~2 seconds.
- Turning is speed-dependent: faster = more responsive.
- Speed never goes backwards.

Audio:
- Engine sound: pitch ranges from 200 Hz (idle) to 800 Hz (max speed).
- Engine sound loops while the car is moving.
- Mute button to toggle audio on/off.

Your task:
1. Create a new folder tutorials/slot-car-30-minute-win/ by copying the 15-minute version.
2. Update the game logic to implement the physics spec:
   - Add velocity and acceleration variables.
   - Implement smooth acceleration when throttle is active.
   - Implement friction/deceleration when throttle is released.
   - Make turning speed proportional to current velocity.
3. Add basic audio using Web Audio API:
   - Create an oscillator that plays a tone.
   - Pitch modulates with speed.
   - Add a mute toggle button.
4. Test the game: does it feel responsive? Does acceleration feel natural?
5. Provide the updated code.

Remember: Keep the code clean and understandable. Document any physics constants (like friction coefficient) as comments.
```

### Customization Ideas

Before sending, consider:

- **Different feel?** Change acceleration time to 0.5 seconds for a twitchier game, or 2 seconds for a slower feel.
- **Different max speed?** Lower it to 3 for a relaxed pace, or 10 for a fast arcade feel.
- **Audio only?** Remove the audio spec if you want to focus on physics first.
- **Visual feedback?** Ask the AI to show acceleration as a visual indicator (color change, particle effect, etc.).

Customize the prompt. Make it yours.

---

## Step 4: Review the Code (5 minutes)

The AI will provide updated code. Check:

### Checklist

- [ ] Folder `tutorials/slot-car-30-minute-win/` created.
- [ ] Physics variables added: `velocity`, `acceleration`, `friction`.
- [ ] Acceleration is smooth (not instant).
- [ ] Deceleration is smooth (not instant).
- [ ] Turning responds to speed.
- [ ] Audio plays with pitch modulation.
- [ ] Mute button works.
- [ ] Code is readable (constants documented).

### What If It's Wrong?

If acceleration feels too fast:

> "The car reaches max speed instantly. It should take ~1 second. Adjust the acceleration constant."

If audio stutters:

> "The engine sound is cutting in and out. Make it loop smoothly."

Keep iterating until it feels right.

---

## Step 5: Set Up the Files (2 minutes)

Copy the AI's code into your project:

```bash
mkdir -p tutorials/slot-car-30-minute-win
# Copy the AI-generated files here:
# - index.html
# - styles.css
# - main.js
```

Run the game:

```bash
cd tutorials/slot-car-30-minute-win
python3 -m http.server 8000
```

Open `http://localhost:8000`.

---

## Step 6: Play & Verify (3 minutes)

### Test the Physics

- **Hold ArrowUp** — Car accelerates smoothly. Speed number increases gradually.
- **Release ArrowUp** — Car slows down smoothly over ~2 seconds.
- **Turn while moving** — Steering feels responsive. Fast car turns sharper than slow car.
- **Turn while stopped** — Car doesn't move forward when steering.

### Test the Audio

- **Engine sound** — Pitch increases as you accelerate. Pitch decreases as you slow down.
- **Mute button** — Click it. Audio stops. Click again. Audio resumes.

### Compare to Spec

Does it match your spec (SPEC-30min-physics-and-audio.md)? If not, ask the AI for fixes.

---

## Step 7: Commit & Log (2 minutes)

Once it works:

```bash
git add tutorials/slot-car-30-minute-win/
git add docs/
git commit -m "30-minute win: physics and audio added"
```

Create a change log:

```bash
cat > logs/change-30min.md << 'EOF'
# Change: 30-Minute Win — Physics & Audio

## What Changed
- Created tutorials/slot-car-30-minute-win/ with physics and audio.
- Physics: smooth acceleration, deceleration, speed-dependent turning.
- Audio: engine pitch modulates with speed; mute toggle.

## Spec
- SPEC-30min-physics-and-audio.md (verified working).

## Verification
- Game runs locally at 60 FPS.
- Acceleration feels smooth and natural.
- Audio responds to speed changes.
- All controls work as expected.

## Next
Moving to 60-minute win for menus, vehicle presets, and track editor.
EOF

git add logs/change-30min.md
git commit -m "log: 30-minute win completion"
```

---

## Why This Process Works (Again)

1. **Decide** — You chose realistic physics. You own that choice.
2. **Spec** — The AI has a contract. "Make it smooth, responsive, natural."
3. **Iterative** — You test after each change. Adjust. Iterate.
4. **Documented** — Future you knows why physics work this way.

**A single prompt can't iterate with feedback.** But this framework supports it.

---

## Customization Ideas: Make It Yours

### Physics Tweaks
- Make the car driftable (more responsive turning at high speed).
- Add "boost" mode: hold a button to get temporary speed boost.
- Different friction for different track sections.

### Audio Tweaks
- Add engine rev sound (short burst when accelerating).
- Add tire squeal when turning at high speed.
- Play a "crash" sound if the car leaves the track.

### Visual Enhancements
- Show acceleration as a particle trail.
- Change car color based on speed (blue = slow, red = fast).
- Add a speedometer gauge (instead of just a number).

**Pick one or two ideas that excite you. Ask the AI to implement them.** This is where creativity meets structure.

---

## Next: The 60-Minute Win

In the final 30 minutes, you'll add:
- **Vehicle presets** — Pick different cars with different physics (light vs. heavy).
- **Track editor** — Design custom tracks from pieces.
- **Menus** — Professional-looking launch and pause screens.
- **Advanced audio** — Multiple engine samples, UI sounds, ambience.

Same cycle: Decide → Spec → Code → Verify → Log.

**By the end, you'll have a professional-quality game AND a deep understanding of how to build software safely with AI.**

Open `tutorials/slot-car-60-minute-win.md` when you're ready for the final push.
