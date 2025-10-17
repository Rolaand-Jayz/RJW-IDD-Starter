# Slot Car Racing: 5-Minute Overview (Optional Read)

## What You're About to Build

Over the next 60 minutes, you will create a **fully playable, polished slot car racing game** that runs in your browser and on your desktop. Here's what the final result looks like:

### The 15-Minute Win
A **simple, playable** slot car game: top-down view, oval track, car moves with arrow keys. It works. It's fun. You built it without fighting the AI.

### The 30-Minute Win
The game now feels **real**: the car accelerates smoothly, has weight (inertia), slows down when you release the throttle. Physics matter. The engine makes a sound that matches the speed. You added complexity without breaking what already worked.

### The 60-Minute Win
A **professional-quality game**: you can pick different cars (each handles differently), design custom tracks from pieces, menus look polished, audio is immersive. You could show this to someone and they'd say "you made this?"

---

## Why This Matters: The Problem It Solves

### The Common AI Coding Trap

When you give an AI agent a single prompt like "make a slot car game," here's what usually happens:

1. **Poor Context** — The agent doesn't understand your project structure, your framework, or your constraints. It hallucinates folder paths that don't exist.

2. **Related Error** — The agent generates a 500-line monolithic file with no separation of concerns, no tests, no documentation.

3. **Broken Feature** — You copy-paste the code, it breaks on line 47 because the agent didn't test it. You spend 2 hours debugging instead of coding.

4. **Agent Shortcoming** — The agent has no concept of *why* you're making these choices. It can't explain the architecture. If something breaks, you're on your own.

5. **What's Missing** — No **structured context** (specs, decisions, tests). No **guardrails** (gates that prevent regressions). No **verified documentation** (living docs that stay in sync with code). No **traceability** (why was this line written? what was the decision behind it?).

**The Result:** You stop trusting the AI. You write everything yourself. You missed the entire point of having an AI partner.

---

## How This Tutorial Works Differently

Instead of one giant prompt, you'll use **the RJW-IDD framework**—a proven method for pairing humans and AI safely. Here's the cycle that repeats:

### The RJW-IDD Cycle (7 Steps)
1. **Start** — You have a goal and a question.
2. **Explore** — You research the problem, document options.
3. **Decide** — You make a choice and explain why (in a `Decision` document).
4. **Create Spec** — You write what success looks like (in a `Spec`).
5. **Test First** — You write tests *before* implementation (TDD).
6. **Implement** — The AI writes code that passes your tests.
7. **Verify & Log** — Tests pass, documentation updates, change log records it.

Each cycle is **traceable**: why did you choose this? what was the test? does it still work? where's the code? All linked together.

### Why This Prevents the Trap

- **Context is structured** — Decisions, specs, and tests give the AI real guardrails, not vague wishes.
- **No surprises** — Tests fail fast. The agent can't hide broken assumptions.
- **You own it** — You made the decisions. You wrote the tests. The AI is the implementation partner, not the designer.
- **It scales** — This works for 15-minute features AND enterprise systems.
- **Creativity stays yours** — The framework doesn't dictate your design; it ensures you can defend it.

---

## What You'll Learn

### About the Framework
- Why **decisions matter** (reversibility, team alignment).
- Why **specs are contracts** (prevent rework, enable parallelism).
- Why **tests come first** (catch bugs, clarify intent).
- Why **change logs are not boring** (traceability is power).
- Why **guards are guardrails** (catch mistakes early).

### About Building with AI
- How to give the AI **enough context** so it writes good code.
- How to verify **the AI's work** (tests, not vibes).
- How to **customize and iterate** without rewriting everything.
- How to **keep control** even when you're using an AI partner.
- How to build **with creativity**, not despite it.

---

## The Flexibility: You Customize At Each Step

This is **not a rigid tutorial**. At several points, you'll see options like:

> **Standard Option:** Make the car red.  
> **Your Idea:** What if the car changes color based on speed? Or matches your favorite car? Or is a cat?

The framework supports this. You'll write a different spec, update your test, and the AI will implement *your* vision—not the template's.

---

## What's Not Here

- **Copy-paste code snippets** — Every line of code is written during the tutorial, not pasted from a template.
- **Magic** — Nothing happens without you understanding why.
- **One big prompt** — If it were one prompt, you wouldn't need this tutorial.
- **Taking over** — The AI doesn't replace you; it amplifies you.

---

## Ready?

This is about **empowering you to build software with clarity, safety, and creativity**. The AI is a tool that gets better when you tell it *exactly* what you want and *verify* that it delivered.

### Next Steps

1. **Read** `tutorials/slot-car-15-minute-win.md` — Start the 15-Minute Win.
2. **Build** — You'll create a playable game.
3. **Loop** — Every 15 minutes, you'll add more features using the same process.
4. **Customize** — At each step, you'll have opportunities to make it *yours*.

At the end of 60 minutes, you'll have a polished game **and** you'll understand how to apply this framework to any project—whether it's a game, an API, a UI, or a system.

---

**Let's go.** Open `tutorials/slot-car-15-minute-win.md` and start building.
