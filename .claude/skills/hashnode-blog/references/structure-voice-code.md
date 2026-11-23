# Structure, voice, code, SEO (read before drafting)

Source of truth for how the post itself is written.

## PART 4 — Structure of the post

**Title.** Concrete noun + concrete consequence. Aim for 45–65 characters, since that's roughly what survives Google's truncation and a feed card — but treat it as a target, not a rule. Never pad a title with filler words or strip a specific detail just to hit the count; a precise 72-character title beats a vague 58-character one. It has to survive being read out of context in a feed.

- Weak: "Understanding React useEffect" · "A Complete Guide to Docker"
- Strong: "Your useEffect runs twice — here's what that's protecting you from" · "Our Docker image went from 1.2 GB to 180 MB. Three lines did most of it."
- Banned: "Ultimate Guide", "Everything you need to know", "in 2026", emoji, listicles with a fake count.
- Test: could this be the title of a documentation page? If yes, it's a topic, not an angle. Rewrite it.

Formulas that hold up: **consequence** ("Your `useEffect` runs twice — here's what that protects you from") · **real number** ("Our Docker image went from 1.2 GB to 180 MB") · **correction** ("`useMemo` is not a performance tool") · **cost** ("What a Storybook 9 upgrade actually costs on a 200-component library") · **decision** ("Rollup or Webpack for a component library, after shipping both") · **confession** ("I shipped a memory leak to production. Here's the code review that missed it.")

**Opening.** The first 40 words decide whether they scroll. Open on the concrete moment — the error, the failing build, the number, the question you couldn't answer in review.

> The build was green locally and red in CI, and the only difference in the log was a line about heap allocation. That's how Node's default old-space limit became my problem.

Patterns that work: the error text (paste it, then say what it was assumed to mean) · the number ("The bundle grew 340 KB in one PR. Nobody added a dependency.") · the failed expectation ("The index existed. Postgres ignored it anyway.") · the review comment · the constraint ("Four days, no budget for a migration.").

In RESEARCH mode, open on the **misconception** or the **observable weirdness** instead: "Adding an index made the query slower. That's not a paradox — it's how the planner works."

Delete on sight: "In today's fast-paced world of software development…" · "X has revolutionised the way we build…" · "Before we dive in, let's understand what X is." · "In this article, we will explore…" · any definition of a term the target reader already knows.

**Body.**
- Sections answer a question the reader is now asking. Headings state the answer, not the label: "Why the index was ignored" beats "Analysis".
- One idea per section. 2–5 sentences per paragraph.
- **Show the wrong version first** when there is one. Wrong → why it's wrong → right is the most effective structure in technical writing. Include what was assumed and why the assumption was reasonable.

  ```js
  // ❌ Looks correct, scans the whole table on every keystroke
  ```
  ...then the problem, then:
  ```js
  // ✅ What actually holds up in production
  ```
- Every behavioural claim gets code, real output, or a link behind it.
- First person about what was done, second person about what the reader should do. Skip "we" unless a team really did it.

**Ending.** No "Conclusion" heading, no summary of what they just read, **no CTA block** ("follow me, read my other articles, leave a clap"). End on the takeaway plus one honest limitation of the approach, then one specific question that invites a reply: "Has anyone hit this with pnpm workspaces? I couldn't reproduce it there." Generic "Let me know your thoughts!" gets nothing.

**Optional FAQ.** Only for evergreen how-to and explainer posts, and only if the questions are ones people actually search. 4–6 questions, two to four sentences each, no filler entries. Skip it entirely on debug stories, migrations, and opinion posts — it reads as SEO padding there.

## PART 5 — Voice and craft (never cut this section)

**Banned phrases.** Cut without replacement; the sentence is almost always stronger.

- Openers: "In today's fast-paced world", "In the ever-evolving landscape", "In this article, we will explore", "Before we dive in", "Let's dive in", "Buckle up".
- Connectives: "It's worth noting that", "It's important to remember", "As we've seen", "Needless to say", "At the end of the day", "That being said" (use "but").
- Empty intensifiers: "seamlessly", "effortlessly", "robust", "powerful", "cutting-edge", "game-changer", "revolutionary", "leverage" (use "use"), "utilize" (use "use"), "delve into", "unlock the power of", "supercharge", "in the realm of".
- Closers: "In conclusion", "To sum up", "Happy coding!", "Let me know your thoughts in the comments!", "I hope you found this helpful."
- Also cut: "simply", "just", "obviously", "of course", "as you can see" — they shame the reader who found it hard.

**Rhythm.** Uniform sentence length is the loudest tell of machine writing. Vary it. A four-word sentence after a long one lands.

> The query planner has statistics. It uses them to estimate how many rows a filter will return, and when that estimate is off by two orders of magnitude it picks a sequential scan over your perfectly good index. Which is exactly what happens here.

Paragraphs: two to five sentences, then break. A one-sentence paragraph is an emphasis tool — spend it rarely.

**Habits that read as human.** Name real things (not "a large dataset" but "1.4M rows"; not "a build tool" but "Rollup 4.9") · admit the wrong turn · timestamp knowledge · link the issue, RFC, or answer that unblocked you · end with a question you actually want answered.

**Weak → strong.**

| Weak | Strong |
|---|---|
| "This can significantly improve performance." | "This cut TTI from 4.1s to 2.3s on a mid-range Android." |
| "You should always memoize expensive computations." | "Memoize when the computation shows up in a profile. Before that, you're paying comparison cost for nothing." |
| "Docker makes deployment easy." | "Docker makes the deploy reproducible. It does not make it fast — the image build still dominates the pipeline." |
| "There are several ways to handle state." | "Three options survive contact with a real app: local state, a store, and the URL. Most bugs come from picking the wrong one." |

## PART 6 — Code, formatting, SEO, length

**Code blocks** are the part people actually read.
- Language tag always: ` ```tsx `, ` ```python `, ` ```sql `, ` ```bash `, ` ```yaml `, ` ```json `, ` ```diff `. Hashnode highlights from that tag.
- Complete enough to paste and run. Elisions are fine in setup code, never in the code the post is about.
- Under ~25 lines. Longer goes in a repo, with the key 10 lines inlined.
- Use a ` ```diff ` block with `+`/`-` when the story is a change.
- Comments carry the *why*: `// keep the ref stable — this list is re-created on every keystroke`.
- Show real output in its own labelled block: the error, the timing, the query plan. Trim noise, never fabricate it.
- Filename above the block when location matters: `// src/hooks/use-debounced-value.ts`.
- Include error handling where a reader would actually need it — but don't wrap every example in try/catch as ceremony.

**Formatting.** `##` for sections, `###` for sub-steps; never `#` in the body. Bold sparingly, for the one clause a skimmer must catch. Bullets for parallel items, prose for reasoning — a post that's all bullets reads as notes. Tables for facts with 3+ comparable columns. Callouts `> **Note** —` / `> **Warning** —`, two or three per post maximum. Images get descriptive alt text and a caption saying what to look at. Hashnode renders bare YouTube, CodeSandbox, gist, and CodePen URLs on their own line; prefer a code block under 25 lines — embeds break, code doesn't.

**SEO.** One primary keyword phrase, appearing naturally in the title, the first 100 words, one `##` heading, and the `seoDescription`. That's enough. Also give, at the end: primary keyword, 3–5 secondary keywords, seoTitle (under 60 chars), seoDescription (150 chars or fewer), slug, and tags — with the character count shown next to the title and description so the user can see they fit. Suggest two or three internal-link spots with descriptive anchor text ("how we bundle the toolkit", not "click here"), written as `[anchor text](TODO: link to your post on X)`. Never invent a URL. No keyword stuffing — it reads badly and no longer helps.

**Length.**

| Post type | Words | Read time |
|---|---|---|
| Quick win / TIL | 400–700 | 3–4 min |
| Debug story | 900–1,400 | 6–9 min |
| Tutorial | 1,200–2,000 | 8–13 min |
| Deep dive | 1,500–2,500 | 10–16 min |
| Comparison | 1,000–1,600 | 7–10 min |

Default 900–1,400 unless the user says otherwise. A tight 900-word post beats a padded 2,500-word one. If a draft runs long, cut setup and background first — the reader arrived with context. Never cut the code or the wrong-turn section.
