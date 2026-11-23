# Archetypes

Read after the angle is settled, to pick the outline.

## PART 7 — Archetypes

Pick one. Percentages are share of total length. Archetypes 1 and 5 need EVIDENCE mode; 3, 4, and 8 work well in RESEARCH mode.

**1. Debug story** — the highest-engagement format, because documentation can't replace it. EVIDENCE mode only.
1. The symptom (10%) — exact error text, failing screen, the metric that spiked. Open here, no setup.
2. Why the obvious fix didn't work (20%) — what was tried first. This is the section readers came for; do not skip it to look smart.
3. The clue (15%) — the log line, flame graph, or docs sentence that reframed the problem.
4. The mechanism (30%) — what was actually happening underneath, with the code or config that proves it.
5. The fix (15%) — the diff, and how it was verified.
6. What it generalises to (10%).
Trap: narrating hour by hour. Compress everything that didn't teach something.

**2. Build-along (tutorial)**
1. What you'll have at the end (5%) — screenshot, demo link, or final output.
2. Assumptions (5%) — versions, prerequisites, and explicitly what's *not* covered. Version numbers are non-negotiable.
3. Steps (70%) — each: goal in one line, the code, then what you'd see.
4. The part that will break (10%) — the two or three errors readers will actually hit, with fixes. This is why people bookmark tutorials.
5. Where to take it next (10%) + repo link.
Trap: a wrapper around the official quickstart. If it doesn't solve a problem the docs don't, pick a different post.

**3. Deep dive (how X actually works)** — works well in RESEARCH mode.
1. The behaviour that doesn't add up (10%).
2. The mental model most people have (15%) — state it fairly; you're about to amend it.
3. What's actually happening (45%) — layer by layer, each anchored to observable evidence: source excerpts, EXPLAIN plans, DevTools traces, network waterfalls.
4. The consequences (20%) — three or four things that now make sense.
5. Where the model still leaks (10%).
Trap: paraphrasing source code without showing behaviour.

**4. Comparison / decision** — works well in RESEARCH mode.
1. The decision to be made (10%) — real constraints: team size, deadline, existing stack, budget.
2. The criteria (15%) — set *before* the comparison, or it reads as post-hoc justification.
3. Head to head (45%) — the same task implemented in each option, real code both ways. Tables for facts only (licence, bundle size, support matrix), never for opinions.
4. The verdict, scoped (20%) — "for a 4-person team shipping weekly, X; if you need Y, the answer flips."
5. What would change my mind (10%).
Trap: false balance. Readers want a recommendation. Give one, with conditions attached.

**5. Migration / upgrade** — EVIDENCE mode only.
1. Where we were and why it hurt (15%).
2. The plan (10%) — including what was deliberately not migrated.
3. The mechanics (40%) — codemods, adapter layers, feature flags, the shape of the PRs.
4. What broke (20%) — the surprises. The most valuable section; anyone can read a changelog.
5. Was it worth it (15%) — before/after on the metric that mattered, and the cost in engineer-days.
Trap: presenting it as frictionless. A migration post with no scars reads as marketing.

**6. Pattern & architecture**
1. The recurring problem (15%) — two or three places it shows up, so readers recognise their own code.
2. The naive shape and where it collapses (20%), with code.
3. The pattern (35%) — the implementation, plus the constraint that makes it work.
4. Trade-offs (20%) — indirection, testing cost, onboarding cost.
5. When not to use it (10%).
Trap: abstraction with no code. If it can't be shown in 25 lines, show the smallest piece that carries the idea.

**7. Quick win / TIL** — 400–700 words, one screen. Problem, snippet, why it works, one caveat. No introduction about the ecosystem. Pairs with `DIRECT` mode.

**8. Concept / fundamentals** — for "how does X actually work" topics with no incident behind them: closures, event loop, indexes, hashing, consensus, tokenisation. Usually RESEARCH mode.
1. The confusion (10%) — the specific thing people get wrong, or the question that exposes a shaky model. Not a definition.
2. The simplest model that's still true (20%) — the version that fits in one paragraph, stated without hedging.
3. What actually happens (35%) — the mechanism, with a minimal runnable example and its real output.
4. Where the simple model breaks (20%) — the case that forces the refinement. This is what separates it from a docs page.
5. When this knowledge pays off (15%) — the bugs it prevents, the decisions it improves.
Trap: analogies that don't survive contact with the mechanism. If the analogy needs a caveat, drop it and show the code instead.
