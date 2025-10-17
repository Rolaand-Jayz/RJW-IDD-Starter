# Slot Car Racing — BONUS: 90-Minute Win

## What This Is

This bonus section is **an educational tour** of how to build professional features using the RJW-IDD framework. You will:

1. Run the bootstrap script to select your mode
2. Chat with the agent to drive feature development
3. Experience the real RJW-IDD cycle in action
4. Build features that extend your game
5. See how everything gets documented and versioned

**Nothing is premade.** Your agent will research, propose, spec, implement, and verify—all based on your decisions and your chosen mode.

---

## The RJW-IDD Development Cycle (The Real Version)

### Phase 1: RESEARCH & DISCOVERY
Agent researches what's possible and feasible. Gathers context about your current game, technical constraints, time budget.

### Phase 2: DECISION (DEC)
Agent proposes options with trade-offs. **You choose** which features matter most. Decision is documented: `docs/decisions/DEC-*.md`

### Phase 3: SPECIFICATION (SPEC)
Agent writes detailed spec for approved features. Clear acceptance criteria, data models, UI requirements. Documented: `docs/specs/SPEC-*.md`

### Phase 4: IMPLEMENTATION
Agent prompts AI to write code. Code is reviewed for quality, tested for correctness. Applied to your project.

### Phase 5: VERIFICATION
Agent tests the code in your game. Ensures no crashes, performance is good, integrates cleanly with existing features.

### Phase 6: COMMIT & DOCUMENTATION
All changes committed to git with clear messages. Change log created in `logs/` explaining what was built and why.

### Phase 7: LEARNING
Agent guides you through what was built, why those decisions were made, and what patterns you can apply to your own projects.

---

## How to Begin

### Step 1: Run the Bootstrap Script

```bash
chmod +x bootstrap-bonus-90min.sh
./bootstrap-bonus-90min.sh
```

This will:
- Ask you to select your mode (Turbo, YOLO, or Classic)
- Create `.rjw-idd-mode` file to track your choice
- Commit to git
- Ready the development environment

### Step 2: Chat with the Agent

Tell the agent:
- "I want to build advanced features for my game"
- "What's possible in 30 minutes?"
- "What features do you recommend?"

The agent will research and propose options based on your situation.

### Step 3: Make Decisions

For each feature proposal, the agent will create a decision document (`DEC-*.md`). Review it, ask questions, approve or reject.

Your decisions direct the entire project.

### Step 4: Specifications

Once you approve decisions, agent writes specifications (`SPEC-*.md`). These are the contracts—what "done" means. Review them. Suggest changes.

### Step 5: Implementation

Agent prompts AI to write code. Code is tested, verified, integrated. You can watch this happen in the chat, or let the agent handle it (depends on your mode).

### Step 6: Verification

Agent tests features in your game. Ensures they work, don't break existing features, perform well.

### Step 7: Commit & Learn

Everything is committed to git. Agent explains what was built, the patterns used, how it connects to software engineering principles.

---

## The Modes Explained

### TURBO Mode (Default)
**Speed:** Fast. Agent makes research decisions, proposes options quickly.  
**Control:** You approve at checkpoints (features to build, specs, implementation verification).  
**Output:** Lots of changes, documented well, you stay informed at key moments.  
**Best for:** Experienced developers who want to move fast.

### YOLO Mode
**Speed:** Maximum. Agent researches, decides, specs, implements everything.  
**Control:** You review the results after implementation is complete.  
**Output:** Fully built features, everything documented, one big review at the end.  
**Best for:** Hands-off learning; see how it all fits together.

### CLASSIC Mode
**Speed:** Deliberate. Agent presents options, you decide before every major action.  
**Control:** Full. You're involved in every decision.  
**Output:** Deep learning; you understand why each choice was made.  
**Best for:** Learning-focused; you want to understand the framework deeply.

---

## What Gets Documented

Everything worth knowing is documented:

- **`docs/decisions/DEC-*.md`** — Why we built this feature, what trade-offs we made
- **`docs/specs/SPEC-*.md`** — Exactly what was built, acceptance criteria, data models
- **`logs/change-*.md`** — What changed, why, how it was tested
- **Git commits** — Every step is a commit with a clear message
- **Code comments** — Key decisions and patterns explained in the code itself

You can always look back and understand **why something was done**.

---

## Next Steps

1. **Run the bootstrap script:**
   ```bash
   ./bootstrap-bonus-90min.sh
   ```

2. **Chat with the agent:**
   - "Ready to start. What features can I build?"
   - "Research what's feasible in my time budget"
   - "Show me your recommendations"

3. **The agent will take it from there**, researching, proposing, implementing, and documenting everything.

---

## A Note on This Tutorial

This tutorial is **not a step-by-step guide with predetermined answers.**

It's a **framework explanation**. The real learning happens through:
- Deciding which features matter (your choice)
- Seeing how specs are written
- Understanding why modularity matters
- Building features that actually work
- Reviewing git history to understand decisions

**The work is real.** Your decisions matter. The code will be committed. The patterns you learn apply to any software project.

Ready? Run the bootstrap script and chat with the agent.
