# Hashnode Blog System — Project Context

> How the posts in this repo are written. For the posts themselves, see the [main README](../README.md).

## Goal
A reusable system for writing Hashnode technical blogs on any topic (languages, databases, AI, DevOps), with a matching cover image for each post.

## Files in this system
- **`.claude/skills/hashnode-blog/`** — the skill. Claude Code reads it from this folder only (no account-level install). It runs the cover script and loads reference files only when needed.
- **`CLAUDE.md`** — project defaults (author, publication URL, voice, length, workflow). Claude Code reads it automatically.
- **`system/hashnode-blog-prompt.md`** — the portable master prompt (~5,200 words), for use in ChatGPT, Gemini or other tools that can't load the skill.
- **`.claude/skills/hashnode-blog/scripts/make_cover.py`** — generates a 1600×840 PNG cover (styles `codeframe`, `terminal`, `blueprint`). Needs Python 3 and `pip install pillow`. Lives inside the skill folder (single copy).

The prompt and the skill carry the same rules. Where they differ, it is on purpose: the prompt defaults to an HTML cover (it can't assume Python), the skill defaults to running the script.

## How it works
- **Evidence mode:** `EVIDENCE` when the user supplies real code, errors or numbers. `RESEARCH` when there is no personal incident: never fabricate experience, cite real sources, label inference and constructed examples.
- **Workflow mode:** `FULL` (titles → outline → wait for approval → draft) or `DIRECT` (straight to the draft).
- **Archetypes:** debug story, build-along, deep dive, comparison, migration, pattern, quick win, concept/fundamentals.
- **Global rules:** never invent numbers, quotes or APIs (leave `<!-- TODO: measure -->`). Pin versions on version-sensitive claims. Always say when NOT to use something. No hand-written table of contents, no "Conclusion" heading, no call-to-action block.
- **Conditional sections:** security, performance and production-readiness only when the topic touches them.
- **Diagrams:** Mermaid, only where one beats prose.
- **SEO:** `seoTitle` under 60 characters, `seoDescription` 150 characters or fewer, with the counts shown. Internal links are placeholders, never invented URLs.
- **Cover:** 1600×840 PNG, cover title 4–7 words with exactly one `*highlighted*` phrase. Hashnode does not accept SVG covers.

## Decisions made
- Kept 1600×840: same 1.9:1 ratio as 1200×630, and Hashnode's guidance names it as a good size.
- Kept "title is the only required field" for the Markdown/GitHub workflow (checked against Hashnode's official template). For the web editor, the model gives the same values as a list instead.
- Rejected a fixed 17-section output (manual table of contents, FAQ in every post, "Conclusion", call-to-action).
- Adopted from earlier reviews: research mode, FULL/DIRECT, conditional security, Mermaid, source-verification rules, concept archetype.
- The prompt writes to a principal-engineer standard and never claims the author lived experiences they didn't.

## Author
- **Jaydeep Kanzariya** — https://jaydeepkanzariya.hashnode.dev/
- Publishing: GitHub repo as `posts/<slug>/index.md` plus `cover.png`, or the Hashnode web editor.

## Status and next step
Everything is built and reviewed. The one thing not yet tested is how the posts read. Test on three posts and change only the rules that fail in practice:
1. A React debug story in `EVIDENCE` mode, such as the Storybook 9 / Node 20 CI failure.
2. A PostgreSQL concept post in `RESEARCH` mode.
3. An AI/LLM comparison post, such as chunking strategies.

## Folder layout
- `CLAUDE.md` — project defaults, read automatically by Claude Code
- `.claude/skills/hashnode-blog/` — the skill; edit rules and the cover script here only
- `system/` — the portable prompt for non-Claude tools
- `posts/<slug>/` — one folder per post: `index.md` + `cover.png`
  - Cover: `python .claude/skills/hashnode-blog/scripts/make_cover.py --title "..." --handle "jaydeepkanzariya.hashnode.dev" --out posts/<slug>/cover.png`

