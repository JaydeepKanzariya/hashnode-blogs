---
title: "Stop Writing user.name Five Times: JavaScript Destructuring Explained"
slug: javascript-destructuring
subtitle: Array and object destructuring, renaming, default values and the errors to recognise, with before-and-after examples and real output
tags: javascript, web-development, beginners, programming, frontend
cover: ./cover.png
seoTitle: "Destructuring in JavaScript: Arrays, Objects, Defaults"
seoDescription: "Learn destructuring in JavaScript: unpack arrays and objects, rename variables, set default values, and avoid errors. Before and after examples."
enableToc: true
---

Here's a function that describes a user:

```js
function describe(user) {
  return `${user.name} (${user.age}) lives in ${user.city}. ${user.name} is ${user.age >= 18 ? "an adult" : "a minor"}.`;
}
```

`user.` appears five times. Here's the same function with destructuring:

```js
function describe({ name, age, city }) {
  return `${name} (${age}) lives in ${city}. ${name} is ${age >= 18 ? "an adult" : "a minor"}.`;
}
```

Both print exactly the same thing:

```text
Asha (24) lives in Pune. Asha is an adult.
```

The second version says up front which three properties it uses, and drops the repetition. That's destructuring. This post covers arrays, objects and default values, plus the few spots where it surprises people. Every output is real, from Node.js 24.22.

## What destructuring means

**Destructuring** unpacks values from an array or an object into separate variables, in one statement. It's shorthand for reading values one by one:

```js
// Without destructuring
const name = user.name;
const city = user.city;

// With destructuring: the same two lines
const { name, city } = user;
```

It only **reads**. The original array or object isn't changed.

## Destructuring arrays

Array destructuring works **by position**. Square brackets on the left, and each variable takes the value at its spot:

```js
const colors = ["red", "green", "blue", "yellow"];

const [first, second] = colors;   // "red", "green"
const [, , third] = colors;       // "blue": commas skip positions
const [head, ...others] = colors; // "red", ["green", "blue", "yellow"]
```

`...others` (the **rest** element) collects everything that's left into a new array.

One neat trick: swapping two variables without a temporary one.

```js
let a = 1, b = 2;
[a, b] = [b, a];
console.log(a, b); // 2 1
```

You've probably already used array destructuring without noticing. In React, `const [count, setCount] = useState(0)` is exactly this: `useState` returns a two-item array, and you name both items.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    subgraph A["colors array"]
        I0["[0] 'red'"]
        I1["[1] 'green'"]
        I2["[2] 'blue'"]
        I3["[3] 'yellow'"]
    end
    I0 --&gt; F["first"]
    I1 --&gt; S["second"]
    I2 --&gt; O["others"]
    I3 --&gt; O
-->
![Array destructuring mapping: in the colors array, position 0 'red' goes to first, position 1 'green' goes to second, and positions 2 'blue' and 3 'yellow' are collected into others](https://mermaid.ink/img/pako:eNpl0VFrgzAQB_CvEu7FF1tMrBrzMBgbg8LGYHub8SE1VxXUlFNpu9LvPnSUyZqnhN__7iB3gcJZBAX7xh2LytDAXj806Y4xxvpxV5I5VOwx01C4xlHPDJE5a8hvmelsg0xDFuTMI7Tef-QT8px5JSF2dywmFjnzds2IdxpOGubMO2PTuOPSsbO36zZgq9UDe8k07Gvqh0Vqy2f6zDT0WLjOLk3M9p5pcEOF1C8t_DXwoaTaghpoRB9apNZMT7hMOQ1DhS1qUEwDoR1Pq_mfNOjuCj4cTPflXHurJjeWFai9aXr0YTxYM-BzbUoyfxHsLNKTG7sBlIznFqAucAK14XItZBqnPOBpEgahD2dQXIj1RkQilDIJZJKmydWH73losBYxj2LJIynjTZpEPqCtB0dvvzufV3_9AUhmllY?type=png)
*Arrays unpack by position. `...others` collects whatever is left.*

## Destructuring objects

Object destructuring works **by name**. Curly braces on the left, and each variable takes the property with the same name. Order doesn't matter:

```js
const user = { name: "Asha", city: "Pune", age: 24 };
const { city, name } = user; // "Pune", "Asha"
```

### Renaming

To use a different variable name, write `property: newName`:

```js
const { name: userName } = user;
console.log(userName); // Asha
console.log(name);     // ReferenceError: name is not defined
```

This reads backwards from what most people expect. `{ name: userName }` **doesn't** create a variable called `name`. It takes the `name` property and stores it in a variable called `userName`. Read the colon as "into": *name into userName*.

### Nested objects and rest

You can reach into nested objects by repeating the pattern:

```js
const user = { name: "Asha", address: { pin: "411001", area: "Kothrud" } };
const { address: { pin } } = user;
console.log(pin); // 411001
```

Only `pin` becomes a variable here; `address` is just the path to it (using `address` afterwards is a `ReferenceError`). And `...rest` works for objects too, collecting the remaining properties into a new object:

```js
const { age, ...rest } = { name: "Asha", city: "Pune", age: 24 };
// age = 24, rest = { name: "Asha", city: "Pune" }
```

### In function parameters

This is where you'll see object destructuring most: unpacking an object right in the parameter list, as in the opening example. It's especially common for "options" objects, and for props in React components.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    subgraph U["user object"]
        P1["name: 'Asha'"]
        P2["city: 'Pune'"]
        P3["age: 24"]
    end
    P1 --&gt;|"{ name }"| V1["const name = 'Asha'"]
    P2 --&gt;|"{ city }"| V2["const city = 'Pune'"]
    P3 --&gt;|"{ age: years }"| V3["const years = 24"]
-->
![Object to variable extraction: from the user object, { name } creates const name equal to 'Asha', { city } creates const city equal to 'Pune', and { age: years } renames age into const years equal to 24](https://mermaid.ink/img/pako:eNplks1OwzAQhF_F2ksvaRU7_5aKhOAIUoQEB2IObrJNghq7chzRkubdUdI2IOrTema_nT1sD7kuEDhsd_orr6Sx5OlFGKEIIaTtNqWR-4q8ZgK6Fg3Rm0_MrYCPa8v4UpoJULJBThb3bSUX_32WCchre-RkkXYKb3wvEyBL5IT5fyxUxbVMKVku704CejLmkEHAibyNsblWrT2L69v0lM3cmH_h2MxN4vp2q9SbuWmvI0rTXmhvps_q-rw1OFCaugBuTYcONGgaOX6hH0cKsBU2KIATAQaL7rDM9U4bAUIN4MBeqnetmyttdFdWwLdy16ID3b6QFh9rWRr524KqQPOgO2WBJ3QaAbyHA3CfxisWJ2FCXZpEnus5cAROGVv5LGBeHEduHCVJNDjwPYW6KxbSIIxpEMehn0SBA1jUVpvn821MJzL8AM5Npjc?type=png)
*Objects unpack by name. The colon renames: `age` goes into `years`.*

## Default values

You can give any destructured variable a fallback with `=`:

```js
const settings = { fontSize: 16, theme: undefined, lang: null };
const { theme = "light", lang = "en", fontSize = 14, mode = "auto" } = settings;
```

```text
{ theme: 'light', lang: null, fontSize: 16, mode: 'auto' }
```

Look at each one:

- `mode` is missing, so the default `"auto"` is used.
- `theme` is `undefined`, so the default `"light"` is used.
- `fontSize` is `16`, so the real value wins over the default.
- `lang` is **`null`**, and it stays `null`. The default `"en"` is **not** used.

**Defaults only apply when the value is `undefined` or missing.** `null` counts as a real value. If an API sends `null` for "no value", a destructuring default won't catch it; use `??` for that instead.

### The error to recognise

Destructuring needs something to read from. Destructure `undefined` or `null` and it throws:

```js
function greet({ name, city = "somewhere" }) {
  return `${name} from ${city}`;
}
greet();
```

```text
TypeError: Cannot destructure property 'name' of 'undefined' as it is undefined.
```

`greet()` passed nothing, so the parameter is `undefined`, and there's no `name` to read. The fix is a default for the **whole** object, `= {}`:

```js
function greetSafe({ name = "Guest", city = "somewhere" } = {}) {
  return `${name} from ${city}`;
}
greetSafe(); // "Guest from somewhere"
```

You'll see the same `TypeError` with "of 'null'" (`const { x } = null` gave `Cannot destructure property 'x' of 'null' as it is null.`). It typically shows up when data you expected hasn't arrived yet.

## Before vs after

**Reading an API response:**

```js
// Before
const title = response.data.title;
const author = response.data.author;
const views = response.data.views;

// After
const { title, author, views } = response.data;
```

**Function options:**

```js
// Before
function createButton(options) {
  const label = options.label || "OK";
  const size = options.size || "medium";
}

// After
function createButton({ label = "OK", size = "medium" } = {}) {}
```

The "after" version also states the function's options right in its signature, so anyone calling it can see what it takes. One difference to be aware of: `||` also replaces `""` and `null`, while the destructuring defaults only replace missing or `undefined` values, as covered above.

**Functions that return two values:**

```js
// Before
const result = getMinMax(scores);
const min = result[0];
const max = result[1];

// After
const [min, max] = getMinMax(scores);
```

## Benefits, and when not to

- **Less repetition.** `user.` written once instead of five times.
- **Clearer signatures.** `function describe({ name, age, city })` documents what it needs.
- **Defaults in one place**, next to the values they protect.
- **Better names.** Rename awkward property names (`{ usr_nm: userName }`) at the point you read them.

Don't overdo it, though. A pattern three levels deep, like `const { a: { b: { c } } } = data`, is harder to read than `data.a.b.c`, and it throws if any level is missing. And if you use a value exactly once, `user.name` right where you need it is perfectly clear.

The takeaway: **destructuring unpacks arrays by position and objects by name into variables, in one line. Defaults cover `undefined`, not `null`, and a `= {}` default stops the "cannot destructure" error.** This post skipped destructuring in loops (`for (const [key, value] of map)`), which uses exactly the same patterns.

Find a function in your code that writes `props.` or `options.` more than three times. What would its signature look like destructured?
