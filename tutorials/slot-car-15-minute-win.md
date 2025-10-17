# Slot Car Racing — 15-Minute Win

## What You'll Create

A **simple, playable slot car racing game** that runs in your browser. You can drive a car around an oval track using arrow keys. It's the foundation for everything you'll build in the next 45 minutes.

**Time:** 15 minutes  
**Outcome:** Playable game, working controls, basic rendering  
**Skill:** Using the RJW-IDD framework's **Decide → Spec → Create → Verify** cycle

---

## Why This Matters: The Methodology at Work

### The Problem: AI Without Structure

Imagine you ask an AI: *"Make me a slot car game."* Here's what could go wrong:

- **Poor Context:** The AI doesn't know your project structure or your goals. It generates random folder names.
- **Related Error:** The AI writes a huge file with game logic, rendering, and physics all mixed together.
- **Broken Feature:** You copy-paste the code. It breaks because the AI never tested it.
- **Agent Shortcoming:** The AI can't explain *why* it built it that way. If something breaks, you're lost.
- **What's Missing:** No **spec** (what success looks like), no **tests** (did it work?), no **decision log** (why this approach?).

### The Solution: Structured Steps

This 15-minute win follows a **cycle that repeats** through all 60 minutes:

1. **Decide** — What are we building? Why?
2. **Spec** — What does success look like?
3. **Create** — The AI writes code that passes your spec.
4. **Verify** — Does it work? Is it documented?

This cycle prevents rework. It keeps *you* in control. It makes the AI **predictable and reliable**.

---

## Step 1: Make a Decision (2 minutes)

### Why This Step?

Before writing a single line of code, you decide: *What game are we making?* This sounds simple, but it's powerful. It forces clarity. It's a contract you can point back to later.

### Your Decision

**Question:** What is the core mechanic of our slot car game?

**Options:**
- **Option A (Recommended):** Simple top-down arcade racing. Car steers left/right, accelerates forward. No complex physics. Pure fun.
- **Option B:** Realistic racing sim with drifting, traction loss, tire wear.
- **Option C:** Abstract and artistic (maybe the "track" is a procedural spiral, or the car is a different creature).

### Make Your Choice

Pick the option that excites you. This is your project. If Option A sounds boring, go with B or C. The framework supports any choice.

**For this tutorial, we'll assume Option A** (simple arcade), but you can absolutely customize.

### Write It Down (30 seconds)

Create a file `docs/decisions/DEC-15min-game-core-mechanic.md`:

```markdown
# DEC-15min: Core Mechanic

**Date:** Today  
**Decision:** Simple top-down arcade racing.

**Why:** Fast to implement, fun to play, foundation for complexity later.

**Reversal:** If it feels boring after testing, we can pivot to drifting or abstract mechanics.
```

Commit it:
```bash
git add docs/decisions/DEC-15min-game-core-mechanic.md
git commit -m "decision: core game mechanic is simple arcade racing"
```

---

## Step 2: Write a Spec (3 minutes)

### Why This Step?

A spec answers: *What does success look like?* It's specific. Testable. Clear. When the AI writes code, it knows what "done" means.

### Your Spec

Create `docs/specs/SPEC-15min-basic-game.md`:

```markdown
# SPEC-15min: Basic Playable Slot Car Game

## Success Criteria (Must Have)

1. **Rendering:** 
   - Canvas displays a track (oval shape) and a car sprite.
   - Car is centered in the canvas initially.

2. **Input Handling:**
   - ArrowUp accelerates the car (speed increases on-screen).
   - ArrowLeft / ArrowRight steer the car.
   - Inputs feel responsive (no delay).

3. **Game Loop:**
   - Car moves around the track when accelerating.
   - Car stops when throttle is released.
   - Speed is displayed on-screen (HUD).

4. **Visual Polish:**
   - Game runs smoothly (60 FPS or close).
   - Track and car are clearly visible.
   - No visual glitches or flickering.

## Nice-to-Have (Skip if Time-Constrained)

- Play/Pause button to freeze the action.
- Car loops cleanly around the track (no teleporting).

## Out of Scope (For Later Wins)

- Physics (friction, acceleration curves, drifting).
- Multiple vehicles or customization.
- Audio.
- Menus or pause screens.
```

Commit it:
```bash
git add docs/specs/SPEC-15min-basic-game.md
git commit -m "spec: basic playable slot car game requirements"
```

---

## Step 3: Give the AI Context (Prompt for Your Agent) (1 minute)

Now you'll ask your AI assistant (Copilot, Claude, etc.) to write the code. But instead of a vague request, you give it *structure*.

### The Prompt

Copy and paste this into your chat with your AI assistant:

```
I'm building a slot car racing game using the RJW-IDD framework. 
I want you to help me create the first playable version.

Here's my spec:
- Top-down canvas-based game (600x600 pixels).
- Car sprite that moves around an oval track.
- ArrowUp = accelerate, ArrowLeft/Right = steer.
- Car speed displayed as text (HUD).
- Simple placeholder graphics (can be drawn using canvas, no external images needed initially).
- Play/Pause button to control simulation.

Constraints:
- Use vanilla JavaScript (no frameworks).
- Single HTML file with embedded CSS and JS, or separate files in a folder.
- Must run locally in a browser without a build step.
- The car should move around the oval track smoothly when accelerating.
- When throttle is released, the car slows down.

Your task:
1. Create the folder structure for tutorials/slot-car-15-minute-win/.
2. Write the HTML, CSS, and JavaScript to meet the spec above.
3. Include placeholder graphics (drawn via canvas API, not external files).
4. Test your code in your head: does it satisfy all the spec requirements?
5. Provide clear instructions for running the game.

Remember: This is the foundation for later features (physics, audio, desktop packaging). Keep it clean, understandable, and modular.
```

### Customization Opportunity!

Before you send this prompt, ask yourself:

- **Different theme?** Change *"oval track"* to *"figure-eight track"* or *"street circuit."*
- **Different controls?** Swap *"ArrowUp"* for *"W key"* or *"mouse-based controls."*
- **Aesthetic twist?** Make the car a spaceship, a cat, or a ghost. Make the track a circuit in space.

Edit the prompt to reflect *your* vision. The AI will adapt.

### What You're Not Doing

- You're not copy-pasting code from the internet.
- You're not guessing what the AI will write.
- You're not hoping it works.
- **You're defining the contract, and the AI will fulfill it.**

---

## Step 4: Review the AI's Code (5 minutes)

The AI will generate code. Here's what to check:

### Checklist

- [ ] **Folder structure** makes sense: `tutorials/slot-car-15-minute-win/` with `index.html`, `styles.css`, `main.js`.
- [ ] **HTML** has a canvas element and a Play/Pause button.
- [ ] **CSS** makes the canvas visible and centered.
- [ ] **JavaScript** handles input (ArrowUp, ArrowLeft, ArrowRight).
- [ ] **Game loop** updates car position and renders it.
- [ ] **HUD** displays speed.
- [ ] **No external dependencies** — everything runs locally.

### What If It's Wrong?

If the code doesn't match your spec, ask the AI:

> "This doesn't meet requirement #2 (Input Handling). The car doesn't respond to ArrowLeft. Fix it."

The AI will revise. **Keep iterating until it matches your spec.**

### Customization Check

Did you ask the AI for a customization (different theme, different controls, etc.)? 
- ✅ If yes, verify the AI actually changed it.
- ✅ If the AI ignored your customization, ask again explicitly.

---

## Step 5: Set Up the Files Locally (2 minutes)

Once you have the code from the AI:

1. Create the folder:
   ```bash
   mkdir -p tutorials/slot-car-15-minute-win
   cd tutorials/slot-car-15-minute-win
   ```

2. Copy the HTML, CSS, and JS files into this folder. The structure should look like:
   ```
   tutorials/slot-car-15-minute-win/
   ├── index.html
   ├── styles.css
   └── main.js
   ```

3. Run a local server:
   ```bash
   python3 -m http.server 8000
   ```

4. Open your browser to `http://localhost:8000`.

---

## Step 6: Verify It Works (2 minutes)

### Play the Game

- Click the **Play** button.
- Hold **ArrowUp** — the car should start moving and the speed number should increase.
- Release **ArrowUp** — the car should slow down.
- While moving, press **ArrowLeft/Right** — the car should steer.
- The car should loop smoothly around the oval track.

### Checklist Against Your Spec

- [ ] **Rendering:** Track and car are visible. ✅
- [ ] **Input:** ArrowUp accelerates, ArrowLeft/Right steer. ✅
- [ ] **Game Loop:** Car moves, stops, loops. ✅
- [ ] **Visual Polish:** Smooth, no glitches. ✅
- [ ] **HUD:** Speed is displayed. ✅

### If Something's Wrong

Compare the code to your spec. Ask the AI to fix it:

> "The car isn't decelerating when I release ArrowUp. According to the spec, it should slow down. Fix the decay logic."

Keep iterating.

---

## Step 7: Commit & Document (1 minute)

Once it's working:

```bash
git add tutorials/slot-car-15-minute-win/
git add docs/
git commit -m "15-minute win: basic playable slot car game"
```

Optional: Create a brief change log:

```bash
cat > logs/change-15min.md << 'EOF'
# Change: 15-Minute Win — Basic Slot Car Game

## What Changed
- Created tutorials/slot-car-15-minute-win/ with playable game.
- Spec: SPEC-15min-basic-game.md defines success.
- Decision: DEC-15min-game-core-mechanic.md explains why we chose simple arcade racing.

## Verification
- Game runs locally without build steps.
- Controls respond as expected.
- Car loops around track smoothly.
- Speed HUD works.

## Next
Moving to 30-minute win to add physics, audio, and polish.
EOF

git add logs/change-15min.md
git commit -m "log: 15-minute win completion"
```

---

## Why This Process Works

1. **Decision** — You're clear on what you're building. You own it.
2. **Spec** — The AI has a contract. It knows what "done" means.
3. **AI Writes Code** — The AI fills in the details based on your spec.
4. **You Verify** — You test it against your spec, not vibes.
5. **Documented** — Future you (or a teammate) knows why this exists.

**A single prompt cannot do this.** This is why the framework matters.

---

## Customization Ideas (Make It Yours)

If you want to go beyond the spec, here are some ideas:

### Visual Tweaks
- Change the car color or shape.
- Make the track different colors or patterns.
- Add a background or skyline.

### Gameplay Tweaks
- Make the car faster or slower by default.
- Add a *"drift mode"* where steering has more effect.
- Add visual feedback when steering (wheel turns, car tilts).

### Experimental
- What if the track was a spiral instead of an oval?
- What if the car left a trail behind it?
- What if the car had a name, and it appeared in the HUD?

**The framework supports all of this.** You adjust your spec, and the AI implements it.

---

## Next: The 30-Minute Win

You've built a playable foundation. In the next 15 minutes, you'll add:
- **Physics** — friction, inertia, acceleration curves.
- **Audio** — engine sound that matches speed.
- **Polish** — menus, better visuals, desktop packaging.

Same cycle: Decide → Spec → Code → Verify → Log.

Open `tutorials/slot-car-30-minute-win.md` when you're ready.
