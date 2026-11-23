---
title: "Emmet for HTML: A Beginner's Guide to Writing Faster Markup"
slug: emmet-for-html
subtitle: Five symbols, one line, a whole block of HTML. Emmet explained one concept at a time
tags: html, web-development, beginners, vscode, productivity
cover: ./cover.png
seoTitle: "Emmet for HTML: A Beginner's Guide"
seoDescription: "Learn Emmet in VS Code: write ul>li*5 and get a full list. Classes, IDs, nesting, multiplication and the ! boilerplate, with real expanded output."
enableToc: true
---

Here's a navigation bar with five links, typed by hand:

```html
<nav>
  <ul>
    <li><a href="#">Link 1</a></li>
    <li><a href="#">Link 2</a></li>
    <li><a href="#">Link 3</a></li>
    <li><a href="#">Link 4</a></li>
    <li><a href="#">Link 5</a></li>
  </ul>
</nav>
```

That's 24 tags and 175 characters, not counting spaces and line breaks. Every one of them is a chance for a typo, and half of them are closing tags that only repeat what you already typed.

Here's the same thing in Emmet:

```text
nav>ul>li*5>a[href=#]{Link $}
```

29 characters. Press a key and the editor writes the HTML above for you. This post teaches Emmet for HTML from zero, one symbol at a time, so you can read and write lines like that one.

## What Emmet is

Emmet is a **shortcut language for HTML**. You type a short abbreviation, and your code editor expands it into full HTML.

It doesn't change your HTML or add anything to your website. The browser never sees Emmet; it only sees the HTML it produced. Think of it like autocomplete on your phone: it helps you type faster, and the message you send is still just text.

Why does this help a beginner in particular? Three reasons:

- **Fewer typos.** Emmet always closes tags and always nests them correctly.
- **Faster practice.** You spend your time on structure, not on typing `</div>` for the hundredth time.
- **It reinforces structure.** Writing `ul>li` makes you think "a list item inside a list", which is exactly how HTML is built.

Emmet is optional. Everything it writes, you could write by hand, and you should still understand every tag it produces. It's a typing tool, not a replacement for knowing HTML.

## How Emmet works in your editor

If you use VS Code, there's nothing to install. VS Code's documentation says Emmet support is "built right into Visual Studio Code, no extension required". Most other popular editors support it too, either built in or through a plugin.

The workflow looks like this:

![Emmet workflow in a code editor: open an HTML file, type an abbreviation such as ul>li*3, an Emmet suggestion appears, press Enter or Tab to accept it, and the full HTML is inserted](https://mermaid.ink/img/pako:eNpN0clu2zAQBuBXGcyxkF1LXkQJhYHGdtFDggaBTxV9oKWxRIAihSGZpYbfPZCKtDnO8s1_mCvWriEs8WLcS90pDnD_JFlaAIDvlcRfA1lQFuZd6A1ctCGJJ5jNtnBXSTy-DTRO1fnM9KxV0M5-O_PXbTRbo78sJZ4-jt1NaFdJPPQ9BfCxbcn_A2oYSLEHbSF0BEb78AnvJryvJD4yeQ8HG4jBMRzVeeLBgaprGgLoz24_uUMl8Uc0Bn4eH-5BjyGeOFCTTLaO7B2PTd3QlH7R7AME1Uo8YYIt6wbLwJES7Il7NZZ4HSMkho56kliCRKYmvs5qZxxLlPaGCQ7K_nau_9DsYttheVHGU4JxaFSgvVYtq_8rZBvinYs2YJmK6QSWV3zFcpWKeSaKTZEu0iJfLpYJvmGZZtl8la2zpRD5QuRFkd8S_DOFLubZJl1vRLoWYrMq8nWC1Ojg-OHv06ff394BqEqiFg?type=png)
*The Emmet workflow inside a code editor.*

**The one thing that confuses most beginners:** in VS Code, pressing Tab on its own doesn't expand an abbreviation by default. The expansion shows up as a suggestion in the autocomplete list, and you accept it there. If you'd rather press Tab directly, VS Code's docs give this setting:

```json
{
  "emmet.triggerExpansionOnTab": true
}
```

Add it to your user settings (Ctrl+Shift+P, then "Preferences: Open User Settings (JSON)"). Tab still indents normally when what you typed isn't an Emmet abbreviation.

Also check that the file is saved as `.html`, or that the language in the bottom-right corner says HTML. Emmet only offers HTML expansions in files the editor knows are HTML.

## Your first abbreviation: an element name

Type a tag name, without angle brackets, and expand it.

| You type | You get |
|---|---|
| `p` | `<p></p>` |
| `h1` | `<h1></h1>` |
| `div` | `<div></div>` |

Under the hood, Emmet reads your abbreviation, turns it into a small tree of elements, and prints that tree as HTML:

![Emmet expansion flow: the abbreviation ul>li*3 is read symbol by symbol, turned into a tree of a ul with three li elements, and written out as HTML with closing tags](https://mermaid.ink/img/pako:eNpNkctqw0AMRX9FaFmc1I_4SQnkUegi2ZRCoZ4sxrZiD4w9QR43SUP-vcRtSneSuOdocS9Ymooww702x7KRbGHzKlh0AACLXOCiKJg-lbTKdE8FP84HPdfqIRC4g8lkDstc4HPbkgUmWfWg7Jjqz21hNBRn-JkE7u7W5citcoHLQemqBwmWiX7lcFS2gQC0-oesRmSdC3xnZakH2xC8vG03IzQSpTa96mqwsu4F7tDBmlWFmeWBHGyJW3lb8XIzCrQNtSQwA4FM1XCalEYbFii6Kzp4kN2HMe2dZjPUDWZ7qXtycDhU0tJayZpl-3dl6irilRk6i5kfjQ7MLnjCbOYlUz9Jo9RzvTQO3MDBM2ae709nfugHSRK7SZym8dXBr_GrO_UjL4wSL0ySaJbGoYNUKWt4-9PVWNn1G0ARifA?type=png)
*From abbreviation to HTML.*

Every example in this post was expanded with the Emmet engine itself (the `emmet` npm package, version 2.4.11), so the output is exactly what it produces. The indentation in your editor will follow your own settings.

## Adding classes, IDs and attributes

These use the same symbols as CSS selectors, so if you've learned those, you already know them.

| You type | You get |
|---|---|
| `p.intro` | `<p class="intro"></p>` |
| `div#main.container` | `<div id="main" class="container"></div>` |
| `.card` | `<div class="card"></div>` |
| `#main` | `<div id="main"></div>` |
| `a[href=#]` | `<a href="#"></a>` |
| `img[src=cat.png alt="A cat"]` | `<img src="cat.png" alt="A cat">` |
| `p{Hello, world}` | `<p>Hello, world</p>` |

- `.` adds a class, `#` adds an ID.
- `[ ]` adds any other attributes. Put quotes around a value with a space in it.
- `{ }` adds the text that goes inside the element.

Notice `.card` and `#main`: if you leave out the tag name, Emmet assumes a `div`. Also notice `img` came out with no closing tag. Emmet knows it's a void element.

Try it yourself: type `button.btn{Save}` and expand it.

## Nesting: `>`, `+` and `^`

Three symbols describe where the next element goes.

**`>` means "inside"** (a child):

```text
div>p
```

```html
<div>
  <p></p>
</div>
```

**`+` means "next to"** (a sibling):

```text
h1+p
```

```html
<h1></h1>
<p></p>
```

Combine them and you can build small components in one line:

```text
.card>h2{Title}+p{Text}
```

```html
<div class="card">
  <h2>Title</h2>
  <p>Text</p>
</div>
```

![Tree built by .card>h2{Title}+p{Text}: a div with class card containing an h2 with the text Title and a p with the text Text](https://mermaid.ink/img/pako:eNo9UE1vgjAY_ivNc64MikBpFpNNr7t5mq-HjlYhAWrelc3N-N8XMfP4fCfPBU1wHgaHPnw3reUothtiGoUQ4mVHcN1X0lh2hL1YLFbidUdo1fMHP622Xew9Yf-wz4b1jnC66_4cCXtIHLlzMJEnLzF4HuwN4nKLEWLrB08wgsDeTedFE_rABBqvkDjZ8T2E4T_NYTq2MAfbf3qJ6eRs9JvOHtkOD5b96DyvwzRGmDydO2AuOMMsM50oXZd1lmZ1lae5xA9MplSyVIXKta5SXdV1dZX4nVfTRJVZUeqs0Lpc1lUh4V0XA7_db5vfu_4Bn3hiYg?type=png)
*The tree that `.card>h2{Title}+p{Text}` builds. `>` goes down a level, `+` stays on the same level.*

**`^` means "climb back up"** one level. After going inside with `>`, it lets you continue at the parent's level:

```text
div>ul>li^p
```

```html
<div>
  <ul>
    <li></li>
  </ul>
  <p></p>
</div>
```

The `p` lands next to the `ul`, not inside it. You'll use `^` less often than the other two; once a line needs several `^`, it's usually clearer to write it as two abbreviations.

## Repeating elements: `*` and `$`

`*` followed by a number repeats an element:

```text
ul>li*5
```

```html
<ul>
  <li></li>
  <li></li>
  <li></li>
  <li></li>
  <li></li>
</ul>
```

`$` inserts a counter that goes up by one for each copy:

```text
ul>li.item$*3
```

```html
<ul>
  <li class="item1"></li>
  <li class="item2"></li>
  <li class="item3"></li>
</ul>
```

![Tree built by ul>li.item$*3: one ul containing three li elements with the classes item1, item2 and item3](https://mermaid.ink/img/pako:eNplkD1vgzAYhP-KdbNB2HzZHro0Y7u1S2MGCzuABDhyjZoW8d-rEDUZOr733N0r3YrWWweF0-i_2t6ESN4OOuiZEELejxrLqNGQJHkiL-yoMQ7pEN3ENJq760b5g_L_NH_QXKMBRRcGCxXD4igmFyZzPbFeUxqxd5PTUEQjOLtcktaPPmjoeQPF2cwf3k9_6eCXroc6mfHTUSxna6I7DKYLZrqrwc3WhWe_zBEqL_YOqBUXqIKJlAtZSZYxWedZTvENxThPC17yXIg6E7WU9Ubxs3_NUl6xshKsFKIqZF1SODtEH15vU-6Lbr9kHmdT?type=png)
*Repeating with `*3` makes three copies, and `$` numbers each one.*

Now you can read the line from the start of this post: `nav>ul>li*5>a[href=#]{Link $}` means *a nav, containing a ul, containing five li, each containing a link to # with the text "Link 1", "Link 2" and so on.*

## The whole HTML boilerplate: `!`

Every HTML page starts with the same skeleton. In an empty `.html` file, type `!` and expand it:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>

</body>
</html>
```

One character, the full page structure. Change `Document` to your page title, change `lang` if your page isn't in English, and start writing inside `<body>`.

## Where Emmet breaks

**A space ends the abbreviation.** `ul > li` looks tidier, but Emmet rejects it: the engine stops with an "Unexpected character" error at the first space. Write it with no spaces: `ul>li`. Spaces are only allowed inside `{ }` text and quoted attribute values.

**Long abbreviations are hard to read.** A 60-character line with three `^` symbols saves typing but costs thinking. If you can't read it back in a few seconds, split it into two or three short abbreviations.

**It's not a substitute for knowing HTML.** If you don't know whether a `p` can contain a `div` (it can't), Emmet will happily generate the wrong thing for you, quickly.

## The five symbols to remember

| Symbol | Meaning | Example |
|---|---|---|
| `>` | inside (child) | `div>p` |
| `+` | next to (sibling) | `h1+p` |
| `*` | repeat | `li*3` |
| `.` / `#` | class / ID | `p.intro`, `div#main` |
| `[ ]` / `{ }` | attributes / text | `a[href=#]{Home}` |

Plus `!` for the boilerplate, `$` for numbering and `^` for climbing up, once these feel natural.

You don't need to memorise this. Keep the table open, type one abbreviation per day in your normal work, and within a week the common ones will be in your fingers.

The limit of this post is that it covers only the daily-use HTML side. Emmet also has CSS abbreviations and editor actions like wrapping existing text in a tag, which are worth a look once the basics feel easy.

Your turn: what's the shortest Emmet abbreviation you can write for a `form` with two labelled `input` fields and a submit `button`?
