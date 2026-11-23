# Conditional sections and self-check

Read before finishing.

## PART 10 — Conditional sections

Include these **only when the topic actually touches them**. Forcing all of them into every post is what produces the bloated everything-article.

- **Security** — include when the topic touches a trust boundary: authentication, authorization, user input, SQL/command construction, secrets and env vars, file uploads, deserialization, CORS, dependencies, or anything reachable from the internet. Cover the concrete failure mode and the fix, not a generic checklist. Skip it entirely for CSS, tooling, or local-dev topics.
- **Performance & scalability** — include when the post makes or implies a performance claim: query patterns, caching, memory, network round trips, bundle size, N+1s, bottlenecks. Every claim needs a measurement or a `<!-- TODO: measure -->`.
- **Production readiness** — for tutorials that stop at "it works on my machine": what's missing before this ships (error handling, timeouts, retries, observability, config).
- **Migration path** — when recommending a replacement for something readers already run.

## PART 11 — Self-check before handing over

Run this and fix what fails. Don't print the checklist.

- [ ] Correct evidence mode applied; zero fabricated personal experience
- [ ] No invented numbers, benchmarks, APIs, or quotes — markers left where data is missing
- [ ] Fact / inference / recommendation are worded distinguishably
- [ ] Versions pinned on every behavioural claim
- [ ] Title makes sense with no context and promises one specific thing
- [ ] First 40 words contain a concrete detail, not a definition
- [ ] Every code block is language-tagged and would run
- [ ] Wrong-way/right-way contrast appears at least once where relevant
- [ ] "When not to use it" is answered
- [ ] Conditional sections included only where they apply
- [ ] Zero banned phrases from `structure-voice-code.md`; sentence lengths vary
- [ ] No hand-written TOC, no "Conclusion" heading, no CTA block
- [ ] Frontmatter: stable hyphenated slug, 4–5 real tags, cover path, seoTitle under 60 chars, seoDescription 150 chars or fewer — both counted, not estimated
- [ ] Ends with takeaway + honest limitation + one specific question
- [ ] Cover title is 4–7 words with exactly one `*highlighted*` phrase
