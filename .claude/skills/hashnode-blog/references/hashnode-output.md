# Output format and Hashnode frontmatter

Read when packaging the post.

## PART 3 — Output format

Deliver in this order:

1. Five title candidates → your pick + why.
2. Outline (headings only) → in FULL mode, wait for approval.
3. The full post as a single Markdown file with YAML frontmatter:

```yaml
---
title: Your useEffect runs twice — here's what that protects you from
slug: useeffect-runs-twice-strictmode
subtitle: StrictMode's double invocation, and the cleanup bugs it exposes early
tags: react, javascript, web-development, frontend, debugging
cover: ./cover.png
seoTitle: Why useEffect runs twice in React StrictMode
seoDescription: React StrictMode double-invokes effects in development. What it catches, why it exists, and how to write effects that survive it.
enableToc: true
---
```

**Scope:** the frontmatter in this section applies to the Markdown workflow — publishing Markdown from a GitHub repo through Hashnode's GitHub publishing workflow, or importing `.md` files. If the user is pasting into Hashnode's web editor instead, skip the frontmatter block and give the same values as a labelled list (title, subtitle, slug, tags, SEO title, SEO description, canonical URL) so they can fill the editor's settings panel by hand. Hashnode's bulk importer accepts a different, smaller field set — don't assume these fields carry across to it.

These fields were verified against Hashnode's official GitHub-publishing template in August 2026. If it's been a while, spot-check them against Hashnode's current GitHub publishing docs before trusting a field you haven't used before — the schema can change.

Frontmatter fields for the GitHub/Markdown workflow:
- `title` is the only required field. `slug` is the **update key** — pick it once and never change it, or you create a duplicate post. 3–6 words, lowercase, hyphenated, no dates.
- `tags`: slugs, max 15, use 4–5. Mix broad reach (`javascript`, `python`, `web-development`, `devops`, `ai`), specific tech (`react`, `postgresql`, `docker`, `typescript`), and intent (`performance`, `debugging`, `tutorial`, `beginners`, `system-design`). At most one vanity tag (`programming`, `coding`, `developer`).
- `cover`: repo-relative path or absolute URL. **SVG is not supported** — PNG, JPG, WebP, GIF, AVIF, under 8 MB.
- `seoTitle`: **under 60 characters** — that's what search results display before truncating. It can differ from the post title: drop the personality, keep the keyword phrase and the specific noun. Count the characters and state the count when you hand it over.
- `seoDescription`: **150 characters or fewer**, written as a promise rather than a summary — it's the copy people decide on in search results. Lead with the concrete detail, not "In this article". Count the characters and state the count.
- `enableToc: true` above ~1,200 words. **Never hand-write a table of contents in the body** — that's what this field is for.
- `canonical: <url>` if published elsewhere first. `seriesSlug: <slug>` only if the series already exists; an invalid slug is silently ignored.

4. SEO block: primary keyword, 3–5 secondary keywords, `seoTitle`, `seoDescription`, slug and tags, with the character counts shown next to the title and description.
5. Cover spec (see `cover-and-diagrams.md`).
6. Diagram suggestions (see `cover-and-diagrams.md`), if any earn their place.
7. Three lines for the user to post on X/LinkedIn — no hashtag spam, no "excited to share".
