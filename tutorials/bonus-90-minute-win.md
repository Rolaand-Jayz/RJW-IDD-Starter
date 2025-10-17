# Slot Car Racing — BONUS: 90-Minute Win (The Mastery Level)

## Welcome to the Advanced Round

You've built a professional 60-minute game. Now you're going beyond. This bonus section shows you how the RJW-IDD framework scales to **real, enterprise-level complexity**—the kind of work that justifies paying developers.

**Time:** 30 minutes (90 minutes total from start, or standalone)  
**Outcome:** AAA-quality game with advanced features  
**Skill:** Enterprise-grade software design, performance optimization, scalability  
**Audience:** You've mastered 60-minute; ready for the deep end.

---

## What Real Software Looks Like

### The Problem: Feature Complexity Explosion

You have a polished game. Now stakeholders (or yourself) want:
- Track editor (users design custom tracks)
- Leaderboard (competitive ranking)
- Multiplayer (local 2-player split-screen)
- Advanced graphics (particles, shadows, effects)
- Performance monitoring (FPS counter, memory tracking)
- Accessibility (colorblind modes, keyboard alternatives)

**Single prompt approach:** "Add all of this."  
**Result:** Monolithic 5,000-line file, crashes, incomprehensible code, you'd fire yourself if you were a tech lead.

**RJW-IDD approach:** Prioritize, modularize, verify each feature independently, then integrate carefully.  
**Result:** Production-ready code, traceable decisions, maintainable by a team.

### Why This Matters: The Real World

This is how Spotify, Netflix, and every serious company build software:
- Every feature is a **decision** (why are we building this?).
- Every feature is a **spec** (what exactly does "done" mean?).
- Every feature is **tested independently** before integration.
- Every feature is **documented** (so the next person understands it).
- **Integration** happens carefully, with integration tests.

**You're about to learn this.** Not theoretically—by actually doing it.

---

## Overview: The Three Advanced Features

### Feature 1: Track Editor (12 minutes)
**Why it matters:** Players want to create their own tracks. This requires a **new subsystem** (editor mode, serialization, asset management). Teaching point: **subsystems integrate without breaking main game**.

**Specs to write:**
- DEC-bonus-track-editor-design.md (decision: modular vs monolithic)
- SPEC-bonus-track-editor.md (track pieces, grid system, save/load)

### Feature 2: Competitive Leaderboard (10 minutes)
**Why it matters:** Leaderboards require **data persistence, timing, UI integration**. Teaching point: **complex features decompose into manageable parts (timing → storage → UI)**.

**Specs to write:**
- DEC-bonus-leaderboard-strategy.md (decision: local vs cloud storage)
- SPEC-bonus-leaderboard.md (lap timing, ranking, persistence)

### Feature 3: Accessibility & Performance (8 minutes)
**Why it matters:** Real software isn't complete without accessibility and performance. Teaching point: **non-functional requirements are as important as functional ones**.

**Specs to write:**
- DEC-bonus-accessibility.md (decision: colorblind mode, control remapping)
- SPEC-bonus-performance.md (60 FPS guarantee, memory limits, monitoring)

---

## Part 1: Advanced Decision-Making (5 minutes)

### The Constraint Matrix

In 30 minutes, you can't build everything. Real teams make hard choices. Here's the matrix:

| Feature | Impact | Complexity | User Visibility | Time | Recommendation |
|---------|--------|-----------|-----------------|------|-----------------|
| Track Editor | High | High | Very High | 12 min | **BUILD** — Players want this |
| Leaderboard | Medium | Medium | High | 10 min | **BUILD** — Competitive edge |
| Colorblind Mode | Medium | Low | Medium | 3 min | **BUILD** — Easy win, inclusivity |
| Performance Monitor | Low | Low | Low | 2 min | **BUILD** — Dev tools matter |
| Multiplayer | Very High | Very High | Very High | 15+ min | **DEFER** — Save for next iteration |
| Advanced Graphics | Medium | High | High | 10+ min | **DEFER** — Premature optimization |
| Cloud Sync | Medium | High | Low | 10+ min | **DEFER** — Too risky |

### Your Call

**For this bonus, we'll build:**
1. ✅ Track Editor (draw your own tracks)
2. ✅ Leaderboard (local storage, rankings)
3. ✅ Colorblind Mode (accessibility)
4. ✅ Performance Monitor (dev tools)

**We'll defer:**
5. ❌ Multiplayer (too complex for 30 min, needs network layer)
6. ❌ Advanced Graphics (premature; current graphics are fine)
7. ❌ Cloud Sync (risk of data loss, skip for MVP)

### Document Your Decisions

Create `docs/decisions/DEC-bonus-prioritization.md`:

```markdown
# DEC-bonus: Feature Prioritization for 90-Minute Win

**Date:** Today  
**Decision:** Build Track Editor + Leaderboard + Accessibility. Defer Multiplayer.

## Trade-offs

### What We're Building
1. **Track Editor** — Players design custom tracks. Builds on existing game. High ROI.
2. **Leaderboard** — Competitive layer. Local storage only (fast, safe).
3. **Accessibility** — Colorblind mode. Small effort, big inclusion.

### What We're Not Building (Yet)
- **Multiplayer** — Requires networking, state sync, latency handling. Too much for 30 min.
- **Advanced Graphics** — Current graphics are fine. Optimization over polish.
- **Cloud Backend** — Storage/sync complexity introduces risk.

## Reasoning

The goal is to demonstrate **how real software grows** without introducing **unnecessary complexity**. 
Track Editor shows modular subsystem design. Leaderboard shows data persistence. Accessibility shows 
professional thinking. Each teaches a different lesson.

Multiplayer would teach networking, but that's a separate skillset (beyond scope of this 90-min bonus).

## Reversibility

If priorities change:
- Can add Multiplayer later using messaging layer.
- Can add Cloud backend with migration guide.
- Graphics are decoupled; can enhance anytime.
```

Commit:
```bash
git add docs/decisions/DEC-bonus-prioritization.md
git commit -m "decision: prioritize track editor, leaderboard, accessibility over multiplayer/graphics"
```

---

## Part 2: Feature 1 — Track Editor (12 minutes)

### Why This Teaches Enterprise Design

The track editor is a **subsystem**. It has its own:
- **UI** (palette of track pieces, canvas)
- **Logic** (grid snapping, piece placement)
- **Data Model** (pieces, positions, orientations)
- **Serialization** (save to JSON, load from JSON)
- **Integration** (main game loads editor-created tracks)

This is how real systems are built: independent subsystems that compose.

### Your Spec

Create `docs/specs/SPEC-bonus-track-editor.md`:

```markdown
# SPEC-bonus: Track Editor Subsystem

## Overview

In-game track editor. Players create custom oval-based tracks from modular pieces.

## Track Pieces (Minimal Set)

| Piece | Description | Length |
|-------|-------------|--------|
| Straight | Horizontal or vertical line | 50px |
| Gentle Curve | 45-degree arc | 50px radius |
| Sharp Curve | 90-degree arc | 30px radius |

## Editor UI

1. **Left Sidebar (Palette):**
   - 3 buttons: Straight, Gentle Curve, Sharp Curve
   - Each shows piece preview
   - Click to select piece

2. **Canvas (Center):**
   - 600x600 pixel grid
   - Grid lines visible (10px increments)
   - Selected piece follows mouse
   - Click to place piece
   - Right-click to delete piece

3. **Top Toolbar:**
   - **Save Layout** button → downloads JSON
   - **Load Layout** button → loads JSON
   - **Clear** button → reset canvas
   - **Play** button → test track in game

4. **Bottom Status Bar:**
   - Shows selected piece
   - Shows piece count
   - Shows "Valid loop? Yes/No"

## Data Format (JSON)

```json
{
  "version": "1.0",
  "pieces": [
    {
      "id": 1,
      "type": "straight",
      "x": 100,
      "y": 100,
      "rotation": 0,
      "width": 50,
      "height": 10
    },
    {
      "id": 2,
      "type": "gentle_curve",
      "x": 150,
      "y": 100,
      "rotation": 90,
      "radius": 50
    }
  ],
  "metadata": {
    "created": "2025-10-16",
    "name": "My Track"
  }
}
```

## Integration with Main Game

1. Editor runs in separate mode (toggle with "E" key or menu)
2. Game loads custom track layout if JSON provided
3. Custom tracks render same as default oval
4. Fallback: if track invalid, use default oval

## Success Criteria

- Editor is separate from main game (modular)
- Player can place, move, delete pieces
- Layout saves to JSON and loads correctly
- Game renders custom track
- No crashes or memory leaks

## Performance

- Editor remains responsive at 60 FPS
- Undo/redo (optional, future work)
- No lag when placing pieces
```

Commit:
```bash
git add docs/specs/SPEC-bonus-track-editor.md
git commit -m "spec: track editor subsystem with modular pieces and serialization"
```

### The AI Prompt

```
I have a slot car game (tutorials/slot-car-60-minute-win/). 
I want to add a track editor where players can design custom tracks from modular pieces.

Spec (SPEC-bonus-track-editor.md):
- Editor mode (toggle with "E" key)
- 3 track piece types: Straight, Gentle Curve, Sharp Curve
- Canvas with grid (600x600, 10px increments)
- Palette to select pieces
- Click to place, right-click to delete
- Save/Load buttons export/import JSON
- Game renders custom tracks same as default oval

Your task:
1. Create tutorials/slot-car-bonus-90-minute-win/ by copying the 60-minute version.
2. Add an EditorMode class that manages editor state separately from game state.
3. Implement piece placement with grid snapping.
4. Add save/load JSON functionality (use browser localStorage or download JSON).
5. Ensure game can load and render custom tracks.
6. Keep editor decoupled from main game (toggle mode, don't mix code).

Code requirements:
- Document piece types (Straight, Curve) as constants.
- Use clear separation: EditorMode.js, MainGame.js stay separate.
- Error handling: warn if track is invalid (no closed loop).
- Test: Place pieces, save, load, play custom track without crashing.

Remember: Modularity is key. Editor should be removable without breaking game.
```

### Testing Checklist

- [ ] Toggle to editor mode with "E" key
- [ ] Palette shows 3 piece types
- [ ] Click palette button → mouse shows piece
- [ ] Click canvas → piece placed at grid-snapped position
- [ ] Right-click piece → deletes it
- [ ] Save button → downloads JSON file
- [ ] Load button → loads JSON, recreates track
- [ ] Toggle to game mode → custom track renders
- [ ] Play custom track → car moves smoothly

---

## Part 3: Feature 2 — Leaderboard (10 minutes)

### Why This Teaches Data & Persistence

Leaderboards require:
- **Timing System** (how do we measure lap time?)
- **Data Storage** (where do we save scores?)
- **UI** (how do we display rankings?)
- **Integration** (how does leaderboard talk to game?)

Each is independent. We can build and test each separately, then integrate.

### Your Spec

Create `docs/specs/SPEC-bonus-leaderboard.md`:

```markdown
# SPEC-bonus: Leaderboard System

## Overview

Local leaderboard. Players race, their lap times are recorded, rankings displayed.

## Timing System

1. **Start Condition:** Player crosses start line for first time
2. **Lap Time:** Time when player crosses start line again
3. **Metrics:**
   - Best lap (fastest single lap)
   - Total time (combined time for all laps)
   - Lap count (number of laps completed)

## Data Model

```json
{
  "leaderboard": [
    {
      "rank": 1,
      "vehicle": "Light Cruiser",
      "bestLap": 12.34,
      "totalTime": 45.67,
      "lapCount": 4,
      "timestamp": "2025-10-16T21:30:00Z"
    }
  ]
}
```

## UI

1. **Leaderboard Screen** (accessible from menu)
   - Shows top 10 entries
   - Columns: Rank, Vehicle, Best Lap, Total Time, Laps
   - Highlight player's best entry
   - Show current session stats

2. **In-Game HUD (During Race)**
   - Current lap time (updates every frame)
   - Best lap so far (this session)
   - Lap count
   - Personal best (from leaderboard)

3. **Post-Race Summary**
   - Final lap time
   - Session total
   - Comparison to personal best
   - "New personal best!" celebration if applicable

## Storage

- Use browser localStorage (key: "slotcarLeaderboard")
- Max 10 entries (auto-delete oldest if exceeds 10)
- Persist across page refreshes
- Clear button available in settings

## Success Criteria

- Lap timing is accurate (within 100ms)
- Leaderboard persists across sessions
- Top 10 displayed correctly
- UI is clean and readable
- No crashes on data corruption
```

Commit:
```bash
git add docs/specs/SPEC-bonus-leaderboard.md
git commit -m "spec: leaderboard system with timing, storage, and UI"
```

### The AI Prompt

```
I want to add a competitive leaderboard to my slot car game.

Spec (SPEC-bonus-leaderboard.md):
- Track lap times (start line crossing to next crossing)
- Store best lap + total time for each session
- Display top 10 in leaderboard screen
- Show current lap time in HUD during race
- Use localStorage for persistence

Your task:
1. Implement LapTimer class that tracks lap times accurately.
2. Create Leaderboard class that manages entries (add, sort, get top 10).
3. Modify HUD to show current lap, best lap, personal record.
4. Add leaderboard screen (accessible from menu) showing top 10.
5. Use localStorage to persist scores.
6. Test: Complete laps, verify timing is accurate, check leaderboard updates.

Code requirements:
- Lap timer must be accurate (detect start line crossing).
- Leaderboard must sort correctly (best lap ascending, total time ascending).
- localStorage must handle corruption gracefully.
- UI must show current session stats + leaderboard.

Remember: Leaderboard is independent subsystem. Can be removed without affecting main game.
```

### Testing Checklist

- [ ] Start racing, lap timer starts
- [ ] Complete lap, time is recorded
- [ ] Lap time displayed in HUD
- [ ] Leaderboard menu shows top 10 entries
- [ ] Best lap highlighted as personal best
- [ ] Reload page, leaderboard persists
- [ ] "New personal best!" message appears
- [ ] Multiple vehicles' lap times tracked separately
- [ ] No crashes or timing errors

---

## Part 4: Feature 3 — Accessibility & Performance (8 minutes)

### Why This Teaches Professional Thinking

Real software considers:
- **Accessibility** (who might use this? colorblind players? keyboard-only users?)
- **Performance** (does this run at 60 FPS on a modest machine?)

These aren't afterthoughts. They're part of the spec from day one.

### Your Spec

Create `docs/specs/SPEC-bonus-accessibility-performance.md`:

```markdown
# SPEC-bonus: Accessibility & Performance

## Accessibility

### Colorblind Mode

1. **Deuteranopia (Red-Green):**
   - Track: Blue/Yellow instead of green/tan
   - HUD text: High contrast (black on white)
   - Car: Different shape indicators, not just color

2. **Protanopia (Red-Green Alternative):**
   - Track: Blue/Orange instead of green/tan
   - Consistent with color-universal design

3. **UI:**
   - Settings menu: "Colorblind Mode" toggle
   - Options: Off, Deuteranopia, Protanopia
   - Applies immediately (no restart needed)

### Keyboard Accessibility

- All UI elements navigable with Tab
- Enter/Space to activate buttons
- Escape to close menus
- Escape while racing = pause menu

### Control Remapping (Future)

- Customizable key bindings
- Menu option to remap keys
- Save to localStorage

## Performance

### Target Metrics

- Render at 60 FPS consistently (target: no frame drops below 50 FPS)
- Memory usage < 100 MB
- Input latency < 50 ms

### Monitoring

1. **Performance Monitor (Dev Tool):**
   - Toggle with "P" key
   - Shows: FPS, frame time, memory usage, draw calls
   - Appears in corner of screen
   - No impact on performance when disabled

2. **Logging:**
   - Log frame time every 30 frames
   - Alert if FPS drops below 50
   - Log memory usage every 5 seconds

### Optimization Targets

- Limit particles to < 100 active
- Canvas rendering: batch draws
- Physics updates: fixed time step
- Audio: limit simultaneous oscillators to 2

## Success Criteria

- Colorblind mode renders correctly
- All UI is keyboard-navigable
- Game maintains 60 FPS on 2018+ hardware
- Performance monitor shows actual metrics
- No visual glitches in colorblind mode
```

Commit:
```bash
git add docs/specs/SPEC-bonus-accessibility-performance.md
git commit -m "spec: accessibility and performance monitoring"
```

### The AI Prompts

**Prompt 1: Colorblind Mode**

```
Add colorblind mode to my slot car game.

Spec:
- Two modes: Deuteranopia (red-green) and Protanopia (red-green alternative)
- Track colors change (blue/yellow for Deuteranopia, blue/orange for Protanopia)
- HUD text becomes high contrast (black on white)
- Car gets shape indicators (not just color)
- Settings menu toggle (applies immediately, no restart)

Your task:
1. Create ColorblindMode class that defines color palettes.
2. Add settings menu option to switch modes.
3. Update rendering code to use selected color palette.
4. Test: Toggle colorblind mode, verify all colors change correctly.

Code requirements:
- Define color constants as Palette objects.
- Render must respect selected palette.
- UI must be accessible (text readable in all modes).

Remember: Colorblind mode must not break performance or game logic.
```

**Prompt 2: Performance Monitor**

```
Add performance monitoring to my slot car game.

Spec:
- Toggle with "P" key
- Shows: FPS, frame time (ms), memory usage (MB)
- Appears in corner (optional overlay)
- No performance impact when disabled

Your task:
1. Create PerformanceMonitor class that tracks FPS, frame time, memory.
2. Update game loop to collect performance data.
3. Render monitor overlay (if enabled).
4. Log warning if FPS drops below 50.

Code requirements:
- FPS calculation: sample every 30 frames
- Frame time: measure time between frames
- Memory: use performance.memory API if available
- Overlay: simple text display in corner

Remember: Monitor should not affect game performance when enabled.
```

### Testing Checklist

- [ ] Toggle colorblind mode in settings
- [ ] Colors change correctly (blue/yellow or blue/orange)
- [ ] Text remains readable in colorblind mode
- [ ] HUD shows high contrast
- [ ] Car is distinguishable in colorblind mode
- [ ] Press "P" key, performance monitor appears
- [ ] Monitor shows FPS, frame time, memory
- [ ] Game maintains 60 FPS with monitor enabled
- [ ] Tab through UI elements (all accessible)
- [ ] Escape closes menus

---

## Part 5: Integration & Verification (3 minutes)

### Integration Checklist

- [ ] Track editor is separate mode (toggle with "E")
- [ ] Main game works with custom tracks
- [ ] Leaderboard doesn't interfere with gameplay
- [ ] Colorblind mode applies to all UI elements
- [ ] Performance monitor logs metrics
- [ ] No crashes when switching between features
- [ ] Settings persist (vehicle choice, colorblind mode)
- [ ] All features work together smoothly

### Commit Everything

```bash
git add tutorials/slot-car-bonus-90-minute-win/
git add docs/
git commit -m "bonus 90-minute win: track editor, leaderboard, accessibility, performance monitoring"
```

Create a comprehensive change log:

```bash
cat > logs/change-bonus-90min.md << 'EOF'
# Change: BONUS 90-Minute Win — Advanced Features

## What We Built

1. **Track Editor**
   - Modular subsystem design
   - Players create custom tracks from 3 piece types
   - Save/load as JSON
   - Game renders custom tracks seamlessly

2. **Leaderboard**
   - Lap timing system (accurate to 100ms)
   - Persistent storage (localStorage)
   - Top 10 rankings displayed
   - Integration with main game (shows best lap in HUD)

3. **Accessibility**
   - Colorblind mode (Deuteranopia, Protanopia)
   - High contrast UI
   - Keyboard navigation (Tab, Enter, Escape)

4. **Performance Monitoring**
   - Dev tool (toggle with "P")
   - Shows FPS, frame time, memory usage
   - Logging of performance warnings

## Why This Matters

These features demonstrate **enterprise-level design**:
- **Modularity** — Track editor is separate subsystem, removable without breaking game
- **Data Persistence** — Leaderboard persists across sessions, handles corruption
- **Accessibility** — Professional apps consider colorblind, keyboard-only users
- **Performance** — Real software monitors and optimizes performance

Each feature was:
- Designed with a spec (clear requirements)
- Implemented independently
- Tested in isolation
- Integrated carefully

**This is how real teams scale complexity.**

## Verification

- ✅ Track editor places pieces, saves, loads, renders
- ✅ Leaderboard tracks timing accurately, persists, sorts correctly
- ✅ Colorblind mode renders all colors correctly, maintains readability
- ✅ Performance monitor shows realistic metrics
- ✅ All features integrate without crashes
- ✅ Game maintains 60 FPS under all conditions

## Tests

See integration tests in tests/test_bonus_90min.js

## Rollback

If issues arise:
- Track editor: remove EditorMode.js, restore main game
- Leaderboard: remove LapTimer.js, Leaderboard.js, restore HUD
- Accessibility: remove ColorblindMode.js, revert rendering
- Performance: remove PerformanceMonitor.js, remove "P" key handler

Features are modular; can be removed independently.

---
**Author:** [Your name]  
**Date:** Today  
**Status:** Complete
EOF

git add logs/change-bonus-90min.md
git commit -m "log: bonus 90-minute win completion"
```

---

## Part 6: Real-World Lessons

### What You've Learned

This bonus section taught you **how professional software scales**:

1. **Prioritization** — You can't build everything. Choose high-impact, low-complexity features first.

2. **Modularity** — Each subsystem (editor, leaderboard, accessibility) is independent. One can break without killing the others.

3. **Data Persistence** — Real software saves state. Leaderboard uses localStorage; production would use databases.

4. **Accessibility** — Colorblind mode seems small, but it's core to professional design. A1.5 billion people are colorblind.

5. **Performance** — A monitor that shows FPS is a basic dev tool. Real teams instrument everything.

6. **Integration** — Features don't just magically work together. Integration tests verify they compose cleanly.

### Why This Is "Mastery"

You started with:
- Copy-paste tutorials
- Single-prompt AI requests
- Hoping it works

You ended with:
- Decisions documented
- Specs as contracts
- Independent subsystems
- Data persistence
- Accessibility
- Performance monitoring
- Integration verification

**This is production-quality software thinking.**

### Next Steps for Real Projects

Apply this pattern to any project:

1. **Identify subsystems** — What parts can be built independently?
2. **Prioritize ruthlessly** — What has highest impact + lowest complexity?
3. **Spec each subsystem** — What does "done" mean?
4. **Build independently** — Each subsystem is a mini-project
5. **Test in isolation** — Verify before integration
6. **Integrate carefully** — One subsystem at a time
7. **Monitor in production** — Performance, errors, user behavior

---

## The Meta-Lesson: How to Grow Without Breaking

At 15 minutes, you had: simple game.  
At 30 minutes, you added: physics + audio.  
At 60 minutes, you added: vehicles + menus + polish.  
At 90 minutes, you added: track editor + leaderboard + accessibility + performance.

**Each step built on previous without breaking it.**

This is the opposite of "rewrite everything when scope changes."

This is **software that grows**.

---

## Customization Ideas: Push Even Further

If you want to go beyond 90 minutes:

### Level 91+: Multiplayer (15+ min)
- Split-screen 2-player
- Shared leaderboard
- Head-to-head races

### Level 92+: Advanced Graphics (10+ min)
- Particle effects (dust when accelerating)
- Shadows
- Camera interpolation (smooth following)

### Level 93+: Sound Design (8+ min)
- Multiple engine samples per vehicle
- Tire squeal on tight turns
- Collision sounds

### Level 94+: Cloud Backend (15+ min)
- Remote leaderboard
- Profile/accounts
- Replay recording

### Level 95+: Mobile Optimization (10+ min)
- Touch controls
- Responsive UI
- Mobile-first performance

**Each of these is a project unto itself.** Apply the same cycle: Decide → Spec → Code → Verify.

---

## Final Thoughts

You've gone from "AI beginner copying snippets" to "software architect designing subsystems."

The game is just the vehicle. The real learning is the **process**:
- Decide what matters
- Spec the contract
- Build independently
- Verify before combining
- Document everything
- Scale without breaking

This works for games. This works for web apps. This works for backend systems. This works for teams of 1 or 100.

**This is how you build software that lasts.**

---

**Congratulations on completing the 90-Minute Mastery Level.** 🏆

You've earned the right to call yourself a software engineer who understands how to work safely with AI.

Now go build something that matters.
