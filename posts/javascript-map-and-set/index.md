---
title: "Why obj[1] and obj[\"1\"] Are the Same Key: Map and Set Explained"
slug: javascript-map-and-set
subtitle: The quiet problems with plain objects and arrays, how Map and Set fix them, and when to use each, with real output
tags: javascript, web-development, beginners, programming, frontend
cover: ./cover.png
seoTitle: "Map and Set in JavaScript: When to Use Each"
seoDescription: "Learn Map and Set in JavaScript: why object keys become strings, how Set removes duplicates, Map vs Object, Set vs Array, and when to use each one."
enableToc: true
---

Try this in your console:

```js
const obj = {};
obj[1] = "one";
obj["1"] = "uno";
console.log(obj);
```

```text
{ '1': 'uno' }
```

Two assignments, one key. The second overwrote the first, because a plain object turned the number `1` into the string `"1"`. It gets worse with object keys. Here are two different people, tracked by visit count:

```js
const asha = { name: "Asha" }, ravi = { name: "Ravi" };
const visits = {};
visits[asha] = 3;
visits[ravi] = 7;
console.log(visits);
```

```text
{ '[object Object]': 7 }
```

Both people became the same string key, `"[object Object]"`, and Asha's count is gone. No error, no warning.

`Map` and `Set` exist to fix problems like these. This post covers what each one is, how they compare with objects and arrays, and when to reach for them. Every output is real, from Node.js 24.22.

## The problems with plain objects and arrays

Objects make good records (`{ name, age }`), but as general key-value storage they have quirks:

- **Keys become strings.** Numbers, booleans and objects are all converted, as shown above.
- **They come with inherited keys.** `"toString" in {}` is `true`, even though `Object.keys({})` has length `0`. A lookup for a user-supplied key can hit something you never put there.
- **There's no size.** You have to count `Object.keys(obj).length`.
- **Order can surprise you.** `Object.keys({ b: 1, 10: 1, a: 1, 2: 1 })` gives `[ '2', '10', 'b', 'a' ]`: number-like keys jump to the front, sorted.

Arrays have the opposite problem. They store **anything, including duplicates**. If you want "each tag once", you have to check before every insert, and `includes` searches the whole array each time.

## What Map is

A **Map** is a collection of key-value pairs where the key can be **any value**: a number, a string, an object, even a function. Keys keep their type, and they aren't converted.

```js
const m = new Map();
m.set(1, "number one")
 .set("1", "string one")
 .set(asha, 3)
 .set(ravi, 7);

m.size;       // 4
m.get(1);     // "number one"
m.get("1");   // "string one"
m.get(asha);  // 3
m.has(ravi);  // true
```

Four entries, all kept. `1` and `"1"` are different keys, and so are the two person objects. The main methods are `set`, `get`, `has`, `delete` and `clear`, plus a real `size` property. A new Map is empty: `new Map().has("toString")` is `false`.

Maps also **iterate in insertion order**, and they're easy to loop over. Counting words is a classic use:

```js
const words = ["red", "blue", "red", "green", "blue", "red"];
const counts = new Map();
for (const w of words) counts.set(w, (counts.get(w) ?? 0) + 1);
console.log(counts);
```

```text
Map(3) { 'red' => 3, 'blue' => 2, 'green' => 1 }
```

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    subgraph M["Map"]
        K1["1 (number)"] --&gt; V1["'number one'"]
        K2["'1' (string)"] --&gt; V2["'string one'"]
        K3["{ name: 'Asha' } (object)"] --&gt; V3["3"]
        K4["{ name: 'Ravi' } (object)"] --&gt; V4["7"]
    end
-->
![Map key-value storage: inside one Map, the number 1 maps to 'number one', the string '1' maps to 'string one', the object { name: 'Asha' } maps to 3, and the object { name: 'Ravi' } maps to 7](https://mermaid.ink/img/pako:eNptkUFvgkAQhf_KZC7YBA0LCMsemjTtrfXioYe6HlYYgUZ2yQKtLeG_N2Csxji3ee99M4fXY2oyQoH7g_lOC2VbeFtLKzUAQNPtcqvqAlYbiStVS9yerXFe2UYig5nuqh3ZB4lbmM8f4X2UnZMIRpNzi_mjzxyYNa0tdX4BJ-Mk3gWDjcQetKpIgPPUFMqBAWZm90lpe7kypoJbNLxG1-qrvIuOqfgKJZ2hi7ktMxSt7cjFimylxhX7MSKxLagiiQIkWsq64zw1B2MlSj2gi7XSH8ZUZ9qaLi9Q7NWhIRe7OlMtvZQqt6r6Vy3pjOyz6XSLIo6mGyh6PKIIGV_4PIkS5rEkDrzAxR8UzPcXob_0A85jj8dJEg8u_k5fvYUfsWXE2ZLzKEzipYuUla2xq1PpU_fDH6FLlrA?type=png)
*Four keys of different types, all kept separate. A plain object would have merged them.*

## What Set is

A **Set** is a collection of **unique values**. Add something that's already there, and nothing happens:

```js
const tags = new Set(["js", "react", "js", "css", "react"]);
console.log(tags);   // Set(3) { 'js', 'react', 'css' }
tags.add("js");
tags.size;           // still 3
tags.has("css");     // true
```

Five values in, three kept. That makes the most common Set trick a one-liner, removing duplicates from an array:

```js
[...new Set([3, 1, 3, 2, 1])]; // [ 3, 1, 2 ]
```

Order is kept: each value stays where it first appeared.

One thing to know: Set compares objects by **identity**, not by content.

```text
Set of two {name:'Asha'}:   2
same object added twice:    1
```

Two separate objects that *look* the same are two values. The same object added twice is one. (Set also treats `NaN` as equal to itself, so `new Set([NaN, NaN]).size` is `1`, even though `NaN === NaN` is `false`.)

Newer JavaScript versions add set operations as built-in methods. They worked in Node.js 24.22; older browsers may not have them yet:

```js
const a = new Set(["js", "react", "css"]);
const b = new Set(["react", "node"]);
a.union(b);        // Set(4) { 'js', 'react', 'css', 'node' }
a.intersection(b); // Set(1) { 'react' }
a.difference(b);   // Set(2) { 'js', 'css' }
```

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    I["Values added:<br/>js, react, js, css, react"] --&gt; S["Set"]
    S --&gt; O["Stored once each:<br/>js, react, css"]
    D["Duplicates: js, react"] -.-&gt;|ignored| S
-->
![Set uniqueness: the values js, react, js, css, react go into a Set, which stores js, react and css once each, while the duplicate js and react are ignored](https://mermaid.ink/img/pako:eNplkUFPg0AQhf_KZM4LAi2wbEwv9mKiMZHEg90e1t0p0ADbLEustv3vBkyjxtu8l3nfO7wTamsIBe5a-65r5Tw8PEsnewCA-43EF9WONIAyhoy4fXM3q_3AwJHSnsF06uGqJW4hCFZQbiSWNMkrqJz9p8n31pEB22sCUrr-h9TD8Cu43khcj4e20crTIGD_pysMVuem6ifiGUpkWLnGoPBuJIYduU5NEk8TS6KvqSOJAiQ6MuMx0La1TqLsL8jwoPpXa7tr2tmxqlHsVDsQw_FglKd1oyqnfl6oN-Tu7Nh7FDyeEShOeESxjHmY8CIr4igu8kW0YPiBIk6ScJmkyYLzPOJ5UeQXhp9zaRQmWZxmPE45z5ZFnjIk03jrHr_XmUe6fAFnJoSu?type=png)
*Five values in, three stored. Adding a value that's already there does nothing.*

## Map vs Object

| | Map | Object |
|---|---|---|
| Key types | Any value, kept as-is | Strings (and symbols); others converted |
| Size | `map.size` | `Object.keys(obj).length` |
| Order | Insertion order | Number-like keys first, then insertion order |
| Inherited keys | None | Yes (`toString`, …) unless created with `Object.create(null)` |
| Iterating | `for…of` directly | Via `Object.keys` / `Object.entries` |
| JSON | Not supported directly | `JSON.stringify` works |
| Best for | Lookups by any key, frequent adds and removes | Fixed-shape records, data sent as JSON |

## Set vs Array

| | Set | Array |
|---|---|---|
| Duplicates | Never | Allowed |
| Order | Insertion order | Index order |
| Access by position | No (`set[0]` doesn't work) | Yes, `arr[0]` |
| "Is this in it?" | `set.has(x)` | `arr.includes(x)`, which searches |
| `map`, `filter`, `sort` | Not built in; convert with `[...set]` | Built in |
| Best for | Uniqueness, membership checks | Ordered lists, positions, transformations |

## When to use Map and Set, and when not to

**Use a Map** when keys aren't simple fixed strings: counting things, caching results, attaching data to objects (like the visit counts), or any collection where you add and remove entries often.

**Use a Set** when the question is "is this already here?" or "keep each one once": deduplicating, tracking which items have been seen, or holding tags and selected IDs.

**Stick with objects and arrays** for data that goes over the network or into storage. That's where Map's biggest catch shows up:

```js
JSON.stringify(counts);                     // {}
JSON.stringify(Object.fromEntries(counts)); // {"red":3,"blue":2,"green":1}
```

A Map turns into an empty `{}` in JSON, silently. Convert it first with `Object.fromEntries`, and a Set with `[...set]`. Plain objects also remain the natural choice for records with known fields, like `{ name: "Asha", city: "Pune" }`. That's not a lookup table, it's a thing.

The takeaway: **Map is key-value storage where keys keep their type; Set is a collection where every value appears once.** Reach for them when objects and arrays start needing workarounds, and convert back before sending data as JSON. This post skipped `WeakMap` and `WeakSet`, which hold object keys without keeping them alive in memory, a more specialised tool built on the same idea.

Where in your current code are you using an object as a lookup table, or checking an array with `includes` before every push?
