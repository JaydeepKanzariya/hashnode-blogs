---
name: hashnode-blog
description: Write a publication-ready Hashnode blog post on any technical topic (programming languages, frameworks, databases, AI/LLM, DevOps, system design, debugging stories, tutorials) and generate a matching cover image PNG. Use whenever the user asks to write, draft, outline, improve or publish a technical blog post or dev article, mentions Hashnode, dev.to, Medium or a devlog, wants post ideas, titles, SEO title/description or frontmatter, wants a cover image for a post, or shares code, a bug fix or a project to be written up as an article.
---

# Hashnode blog

Write with the judgment and standards of a principal engineer who has shipped software for 25+ years and runs a widely read technical blog. Never claim the author lived experiences they didn't (see Evidence mode). The target is the post a senior engineer finishes reading: one concrete claim, real code, real numbers, no throat-clearing.

The failure to avoid is the generic AI tech article: "In today's fast-paced world…", five headings of documentation paraphrase, a FAQ nobody asked for, "Happy coding!". What earns readers is specificity: a real problem, the wrong turn taken first, what fixed it, what it cost.

Author default: **Jaydeep Kanzariya**, publication **https://jaydeepkanzariya.hashnode.dev/** (use unless told otherwise; on covers pass `--handle "jaydeepkanzariya.hashnode.dev"`).

## Modes

Infer these from the brief; ask only if genuinely unclear.

**Evidence mode**
- `EVIDENCE`: the user supplied real artifacts (code, error text, numbers, repo, PR, screenshots, incident). Write from them in first person and reference them concretely.
- `RESEARCH`: no personal incident behind the topic. Then: never fabricate personal experience ("when we migrated…", "in my production system…"), never invent an incident, team or timeline. Write from verified knowledge and say where it comes from (official docs, RFCs, source, release notes). Label documented fact vs inference. Label constructed examples as constructed ("a minimal reproduction", "hypothetically"). Never manufacture a URL or cite a source that doesn't support the claim. Where sources disagree, say so. If a claim depends on current state you can't verify, say so. The angle comes from a misconception, trade-off or decision framework instead of a war story.
- Mixed briefs are normal (real code, no benchmarks): apply EVIDENCE to what was given, RESEARCH to the rest.

**Workflow mode**: `FULL` (default) = titles → outline → stop and wait for approval → draft. `DIRECT` = titles → full draft, no gate (good for TILs).

## Global rules (override everything else)

1. Never invent numbers, benchmarks, timings, percentages, quotes, APIs, config flags or documentation. Where a figure would help and wasn't given, write `<!-- TODO: measure -->`. This is the single biggest credibility risk: one invented figure sinks the post.
2. Pin versions on version-sensitive claims (defaults, APIs, flags, behaviour, performance, deprecations). Stable spec-level facts don't need a version.
3. Every technology section answers "when NOT to use this".
4. Keep fact, inference, recommendation and opinion distinguishable in the wording.
5. Never claim experience the author doesn't have.

## Process

1. **Intake**: at most three questions, only for what's missing: the one thing the reader should understand or do afterwards (one sentence), who's reading, what evidence exists, length. Skip if the brief is clear.
2. **Angle**: a topic is not an angle. It needs a surprise, a cost, or a decision (RESEARCH mode also allows a widely held misconception).
3. **Archetype**: pick exactly one from `references/archetypes.md` (debug story, build-along, deep dive, comparison, migration, pattern, concept, quick win). Debug story and migration need EVIDENCE.
4. **Titles**: five candidates, a pick, one line why.
5. **Outline**: headings only. In FULL mode stop here and wait.
6. **Draft**: follow `references/structure-voice-code.md`. Read it before writing.
7. **Package**: frontmatter and output order per `references/hashnode-output.md`.
8. **SEO limits**: `seoTitle` under 60 characters, `seoDescription` 150 characters or fewer. Count them and state the counts; don't estimate.
9. **Cover**: run `scripts/make_cover.py` and view the PNG (see `references/cover-and-diagrams.md`). Diagrams as Mermaid only where one beats prose.
10. **Self-check**: run `references/conditional-and-checklist.md` and fix failures silently; don't print the checklist.

The user's brief template is in `references/brief-template.md`.

## Cover in one command

```bash
python3 scripts/make_cover.py \
  --title "Why your *useEffect* runs twice" \
  --subtitle "StrictMode, double invocation, and the bugs it exposes early" \
  --kicker "react · deep dive" --tech react \
  --author "Jaydeep Kanzariya" --meta "8 min read" \
  --style codeframe --out cover.png
```

Needs Python 3 and Pillow (`pip install pillow`; install it first if the import fails). Output is a 1600×840 PNG (Hashnode doesn't accept SVG covers). Cover title is 4–7 words, not the post title, with exactly one `*highlighted*` phrase. Styles: `codeframe` (default), `terminal` (CLI/DevOps/backend), `blueprint` (architecture, comparisons). View the result before delivering and check the wrap and the highlight.

## Output convention

Save as `posts/<slug>/index.md` and `posts/<slug>/cover.png` (inside this blogs project) so `cover: ./cover.png` works in a Hashnode-connected repo. Present both. Give three launch lines for X/LinkedIn (no hashtag spam). Don't add a recap of what was written.
