---
title: "CSS Selectors 101: Targeting Elements with Precision"
slug: css-selectors-101
subtitle: Element, class, ID, group and descendant selectors, and which rule wins when they clash
tags: css, web-development, beginners, frontend, css3
cover: ./cover.png
seoTitle: "CSS Selectors 101: Element, Class, ID and More"
seoDescription: "Learn CSS selectors from scratch: element, class, ID, group and descendant selectors, plus how the browser decides which rule wins when two clash."
enableToc: true
---

These two CSS rules differ by one character:

```css
.card, p { color: crimson; }
```

```css
.card p { color: crimson; }
```

The first turns every card **and every paragraph on the page** red. The second turns red only the paragraphs that sit **inside** a card. Same words, one comma versus one space, completely different result.

That's what CSS selectors are about: pointing at exactly the elements you mean, and no others. This post covers the five you'll use every day, in the order that makes sense to learn them, and ends with how the browser decides which rule wins when two of them disagree.

## Why CSS needs selectors

A CSS rule has two halves: **which** elements to style, and **how** to style them.

```css
h1 {
  color: navy;
}
```

`h1` is the selector: the "which". `color: navy;` is the declaration: the "how". Without a selector, the browser would have a style and nowhere to put it.

Think of a selector as the way you address people in a crowded room:

- "**Everyone**, please sit down" → every element of one type
- "**Everyone wearing a blue badge**, come here" → every element with a class
- "**Riya, seat 14**, you've won" → exactly one element with an ID

The more specific the address, the fewer people it reaches. Hold on to that idea; it comes back at the end.

## Element selector: "everyone named p"

The simplest selector is a tag name. It matches every element of that type on the page.

```html
<h1>Our menu</h1>
<p>Fresh coffee every morning.</p>
<p>Open until 9 pm.</p>
```

```css
p {
  color: gray;
  font-size: 18px;
}
```

**Before:** both paragraphs use the browser's default black text. **After:** both turn gray and slightly larger. The `h1` is untouched, because it isn't a `p`.

Element selectors are good for setting defaults across a whole site. They're too blunt when you want *one* paragraph to look different from the rest. That's what classes are for.

## Class selector: "everyone wearing this badge"

A class is a label you add to elements yourself, with the `class` attribute. In CSS you select it with a dot.

```html
<p>Fresh coffee every morning.</p>
<p class="highlight">Today only: free refills.</p>
<p>Open until 9 pm.</p>
```

```css
.highlight {
  background-color: lightyellow;
  font-weight: bold;
}
```

**Before:** three identical paragraphs. **After:** only the middle one gets a yellow background and bold text.

Two things make classes the workhorse of CSS:

- **Reusable.** Put `class="highlight"` on ten elements, of any type, and all ten get the style.
- **Combinable.** An element can wear several badges at once: `class="highlight large"`. Each class brings its own styles.

## ID selector: "one specific person"

An ID names exactly one element on the page. In CSS you select it with a `#`.

```html
<header id="site-header">Corner Café</header>
```

```css
#site-header {
  background-color: black;
  color: white;
  padding: 16px;
}
```

**Before:** plain text at the top of the page. **After:** a black bar with white text.

The rule that matters: **an ID must be unique on the page.** Two elements with `id="site-header"` is invalid HTML, even though the browser will usually style both without complaining.

How to choose between them:

![Decision flow for choosing a class or an ID: if a style could apply to more than one element, use a class, which is reusable and easy to override; use an ID only for exactly one element, knowing it is hard to override](https://mermaid.ink/img/pako:eNpdkk2P0zAQhv_KaLi6pUm_kggtQu2lB5BYsQeoOUzj2diSYxfboQ1t_ztKWNhdbh7Zz_OOR3PB2ivGCh-tP9WaQoIvWxmkAwD4fJG48Z1VkLSJEFNvGeh4tD0k_-4Q3t61PjAkTQ68Y2DLLbv0XuLtnwImk7vrV44CfICW-gODpcThCpu9xIfIQFBbinH0TbVptDWNThK_v3ZI_OQFJM2BwUTgM9XJ9kOuGFFy6umW7In6CCdjLRxY4hV2e4kfHOy2A0nW-hOrEXoTTeKJZlIcXiRuhkS430u85y7SwbKA2rcH48bziDLFYQzgf3IIRvELfDfiD8P_nPnRMXg3tAZHap5gTUH9B6PAJhiFVQodC2w5tDSUeBmkEpPmliVWIDGw6s6T2lsfJEp3Q4FHct-8b__SwXeNxuqRbGSB3VFR4q2hJtDzE3aKw8Z3LmFVjgasLnjGapEV07woV2U2y8r1fDYX2GOV5fl0kS_zeVGsZ8W6LNc3gb_GzNk0X2XLVZEti2K1KNdLgaxM8uHjn90aV-z2G-CbxrY?type=png)
*Class vs ID. When in doubt, use a class.*

My recommendation: style with classes almost always. An ID's real jobs are links to a section of the page (`href="#contact"`), connecting a `<label>` to its input, and JavaScript lookups. The reason to avoid IDs for styling comes up in the priority section.

## Group selector: the comma means "and these too"

When several selectors need the same styles, list them with commas instead of repeating the rule.

```css
/* ❌ The same three lines, three times */
h1 { font-family: Georgia, serif; }
h2 { font-family: Georgia, serif; }
h3 { font-family: Georgia, serif; }
```

```css
/* ✅ One rule, three selectors */
h1, h2, h3 {
  font-family: Georgia, serif;
}
```

The result is identical; the second is easier to change. Read the comma as "and": *h1, and h2, and h3*. Each part of the group is a completely separate selector. That's why `.card, p` from the opening hits every paragraph on the page: the `p` part doesn't care where it is.

## Descendant selector: the space means "inside"

A space between two selectors means "the second, when it's somewhere inside the first".

```html
<div class="card">
  <p>Inside the card.</p>
  <section>
    <p>Deeper inside the card.</p>
  </section>
</div>
<p>Outside the card.</p>
```

```css
.card p {
  font-weight: bold;
}
```

**Result:** both paragraphs in the card turn bold, including the one nested inside `<section>`. The paragraph outside the card stays normal.

"Inside" means at any depth, not only the direct children. Children, grandchildren, further down: all count. If you've read about the DOM tree, this is the selector walking down that tree. (I covered the tree in [HTML tags vs elements](https://jaydeepkanzariya.hashnode.dev/html-tags-vs-elements-what-you-type-vs-what-the-browser-builds).)

Now the opening example makes sense:

| Selector | Read it as | Matches |
|---|---|---|
| `.card, p` | every `.card` **and** every `p` | cards, plus all paragraphs on the page |
| `.card p` | every `p` **inside** a `.card` | only paragraphs within cards |

## When two rules disagree: priority

Sooner or later, two rules will try to style the same element differently:

```html
<p id="intro" class="note">Welcome!</p>
```

```css
#intro { color: red; }
.note  { color: green; }
p      { color: blue; }
```

The text is red. At a very high level, the browser ranks selectors like this:

1. **ID** beats **class**, and **class** beats **element**.
2. If two rules are equally specific, the **later** one in the CSS wins.

In the addressing analogy: "Riya, seat 14" outranks "everyone with a blue badge", which outranks "everyone".

The part that surprises people is that the ranking goes **by category first**, not by counting. I tested this in Chrome 157: an element styled by `#hero` and also by a selector with ten classes chained together (`.a.b.c.d.e.f.g.h.i.j`) still took the `#hero` colour. Ten classes don't add up to one ID.

That's the reason to keep IDs out of your styling. Once an ID sets a colour, the only way to change it later is another ID-level selector (or `!important`, which creates its own mess). Classes keep your styles easy to override.

The real rules (called **specificity**) have more detail than this, and also involve inline styles and `!important`. For a beginner, "ID > class > element, and later wins a tie" explains almost every clash you'll hit.

## How the browser matches a selector

Putting it together, here's what happens to every rule in your stylesheet:

![How the browser applies a CSS rule: it takes the selector, checks each element in the DOM, skips non-matches, and when two rules set the same property the higher priority wins, ID then class then element, with the later rule breaking a tie](https://mermaid.ink/img/pako:eNpNksuS2jAQRX-lq9eGYPOyXalJAc7ALCZZkE2CZiHsBquwLZfULoYY_j1lMUy80-PePrdbajHVGWGMh0Kf01wahl-JMKICAFjsBK62WzBNQV_35svTMJUmgxpaOOiKB2dSx5xj2Osig5vANxgMnmC5E7g0-mzJAMsTWeCcwFJBKWsj8O1Rfunkqw6SU3qyQDLNgQoqqWJQlfMlP197lpWzJK3ARJMFxVBKTvNvAm8PSdJJrj_0Fb7vBG5PqgbFvRL3-99kr_C8E7jIMsfpegTWwLnkR4ae69mB163ARaU5J3M3WGLrJuNalCVBbXRNhi_9SOvPSJuOWNfF5T4TvhTUg6z_R3vZCdyoYweqjdJG8QXOqrKxo70kXleggrSQ1n6sP0J7TlFIfmTcG5InCxJY9WEvrqMNeng0KsOYTUMelmRK2W2x7WQCOaeSBMYg0FDWvA9SXXSvKKobeljL6o_W5cNtdHPMMT7IwpKHTZ1JpkTJo5Hl56mhKiOz0k3FGPtjVwPjFt8xnvjhMAijWeSP_Gg-Ho09vGDsB8FwEkyDcRjOR-E8iuY3D_866mgYzPzpLPSnYTibRPOph5Qp1ub1_qnd3779A19W6Pg?type=png)
*How a selector turns into styles on the page.*

One detail that's useful to know: browser engines generally check a selector like `.card p` from the **right**. They find each `p` first, then look up its ancestors for a `.card`. You don't need to write CSS any differently because of it, but it explains why the rightmost part of a selector is called the "key".

Selectors are the foundation the rest of CSS sits on. Every colour, margin and layout rule you'll ever write starts with one, and if the selector points at the wrong elements, nothing after it can fix that.

The limit of this post is that it stops at the basics. Pseudo-classes like `:hover`, attribute selectors and the child combinator `>` all build on exactly these five, and they're worth learning next.

Try this in DevTools: inspect any element, look at the Styles panel, and find a rule that's crossed out. Which selector beat it, and was it an ID, a class or simply a later rule?
