# Slot Car Racing — BONUS: 90-Minute Win

## Overview

This bonus section implements the RJW-IDD framework through actual feature development. You will:

1. Execute `bootstrap-bonus-90min.sh` to set development mode
2. Engage with the agent to drive feature prioritization and implementation
3. Execute the full RJW-IDD cycle: Discover → Decide → Spec → Implement → Verify → Commit
4. Build production-ready features that extend the 60-minute game
5. Generate all relevant decision documentation, specifications, and change logs in version control

**Nothing is templated.** The agent will perform research, propose trade-offs, spec requirements, implement code, perform verification testing, and maintain git history—entirely driven by your decisions and chosen mode.**

---

## The RJW-IDD Development Cycle (The Real Version)

### Phase 1: RESEARCH & DISCOVERY
Agent analyzes project state, technical constraints, time budget. Produces feasibility assessment and option matrix.

### Phase 2: DECISION (DEC)
Agent proposes prioritized features with impact/complexity trade-offs. You select approved features. Documented: `docs/decisions/DEC-*.md`

### Phase 3: SPECIFICATION (SPEC)
Agent writes formal specifications with acceptance criteria, data models, API contracts, and integration points. Documented: `docs/specs/SPEC-*.md`

### Phase 4: IMPLEMENTATION
Agent generates code via AI assistance. Code review for quality, correctness, and adherence to spec. Integrated into project.

### Phase 5: VERIFICATION
Agent executes integration testing. Validates feature functionality, performance characteristics, and absence of regressions.

### Phase 6: COMMIT & DOCUMENTATION
All changes committed with descriptive messages. Change logs created in `logs/` with technical rationale.

### Phase 7: ANALYSIS
Agent documents architectural patterns, design decisions, and lessons applicable to future development.

---

## How to Begin

### Step 1: Run the canonical bootstrap

The starter repository includes a canonical bootstrap installer that prepares the project and prompts for initial configuration. Use that script to initialize your environment and select add-ons or modes where applicable.

Run the repository's installer/bootstrap script (example path):

```bash
chmod +x scripts/bootstrap/install.sh
bash scripts/bootstrap/install.sh
```

What this does depends on the installer and your chosen options. It typically prepares dependencies, configuration, and any optional add-ons. After running it, the agent-driven tutorial flow can begin.

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
**Cadence:** Fast. Agent conducts research, proposes decisions, specs, and implements with minimal friction.  
**Decision Points:** You approve at feature-level checkpoints and verification gates.  
**Output:** High-velocity feature delivery with documentation at key transitions.  
**Use Case:** Experienced developers seeking expedited feedback loops.

### YOLO Mode
**Cadence:** Maximum velocity. Agent conducts full research-to-commit cycle uninterrupted.  
**Decision Points:** Post-implementation review of specifications, code, and change logs.  
**Output:** Complete feature set with full git history and documentation.  
**Use Case:** Learning-oriented; understand compositional patterns and architectural decisions retroactively.

### STRICT Mode
**Cadence:** Deliberate. Agent presents research findings and options; you approve before each phase transition.  
**Decision Points:** Research → Decision → Spec → Implementation → Verification gates.  
**Output:** Deep engagement with rationale behind each decision.  
**Use Case:** Educational focus; understand the framework mechanics in detail.

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

1. **Run the canonical bootstrap (example):**
   ```bash
   bash scripts/bootstrap/install.sh
   ```

2. **Chat with the agent:**
   - "Ready to start. What features can I build?"
   - "Research what's feasible in my time budget"
   - "Show me your recommendations"

3. **The agent will take it from there**, researching, proposing, implementing, and documenting everything.

---

## A Note on This Tutorial

This is **not a templated walkthrough.** It's a **framework specification and execution environment.**

The real learning occurs through:
- **Decision ownership** — You prioritize features based on impact/complexity analysis
- **Specification review** — Understand how requirements translate to acceptance criteria
- **Code integration** — See how features compose without breaking existing functionality
- **Git archaeology** — Review commit history and change logs to understand architectural evolution
- **Pattern recognition** — Extract generalizable software engineering principles

**This development is real.** Decisions are versioned. Code is committed. Specifications are documented. The patterns you learn generalize to any software project at scale.

Execute `./bootstrap-bonus-90min.sh` to begin.
