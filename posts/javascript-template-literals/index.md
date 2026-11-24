---
title: "Why \"Total: \" + 5 + 3 Prints 53, and What Template Literals Fix"
slug: javascript-template-literals
subtitle: String concatenation problems, backtick syntax, ${} interpolation, multi-line strings and real use cases in modern JavaScript, with real output
tags: javascript, web-development, beginners, programming, tutorial
cover: ./cover.png
seoTitle: "JavaScript Template Literals Explained for Beginners"
seoDescription: "JavaScript template literals: why + concatenation breaks, backtick syntax, ${} interpolation, multi-line strings and real use cases, with real output."
enableToc: true
---

Here is a greeting built the old way, with `+`:

```js
const name = "Asha";
const age = 21;
const city = "Pune";
const old = "Hi, I am " + name + "," + age + " years old from" + city + ".";
console.log(old);
```

```text
Hi, I am Asha,21 years old fromPune.
```

Two missing spaces, and nothing warned me. JavaScript glued together exactly the characters I typed, and I typed them wrong. **Template literals** are the fix: strings written with backticks that let you drop variables straight into the text. All outputs below are real runs on Node.js 24.22.1.

## What goes wrong with string concatenation

Joining strings with `+` works. It also breaks in four small, repeatable ways.

**1. Missing spaces.** You can see it above. Every gap between a variable and a word is a space you must remember to type inside the quotes.

**2. Numbers join in unexpectedly.** `+` adds numbers and joins strings, and once a string is involved it joins everything after it:

```js
const price = 5;
const tax = 3;
console.log("Total: " + price + tax);
console.log("Total: " + (price + tax));
```

```text
Total: 53
Total: 8
```

The first line reads left to right: `"Total: " + 5` becomes the string `"Total: 5"`, then `+ 3` appends `"3"`. You need extra parentheses to get 8. I covered the rules behind this in [why "5" + 3 is "53"](https://jaydeepkanzariya.hashnode.dev/javascript-operators-basics).

**3. Quotes clash.** A string in single quotes can't contain a single quote without an escape:

```js
console.log('It\'s Asha\'s "best" day');
```

```text
It's Asha's "best" day
```

It works, but every single quote inside needs a backslash. Inside backticks, neither kind of quote needs escaping.

**4. Line breaks need `\n`.** Covered in the multi-line section below.

None of these are hard in isolation. They add up to code you have to read slowly, because the quotes, the plus signs and the spaces are all competing with the actual message.

## Template literal syntax

A template literal uses **backticks** (the key above Tab on most keyboards) instead of quotes. Inside it, `${...}` marks a spot where a value goes:

```js
const name = "Asha", age = 21, city = "Pune";

// ❌ concatenation
const old = "Hi, I am " + name + "," + age + " years old from" + city + ".";

// ✅ template literal
const fixed = `Hi, I am ${name}, ${age} years old from ${city}.`;
console.log(fixed);
```

```text
Hi, I am Asha, 21 years old from Pune.
```

Read the second version aloud and you hear the sentence. That's the readability gain: the string looks like its output.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    A["Hi, I am ${name}"] --&gt; B{"JavaScript replaces<br/>each placeholder"}
    N["name = Asha"] --&gt; B
    B --&gt; C["Hi, I am Asha"]
-->
![Interpolation: the template "Hi, I am" followed by a name placeholder, and the value name = Asha go into JavaScript's placeholder replacement, which produces Hi, I am Asha](https://mermaid.ink/img/pako:eNpNkUFPg0AQhf_KZOJxW4EWWDbapK0HNepBb3Y9rOy0kLAsmYJWCf_dFG3j8c3M-17ypsfcW0KF28p_5oXhFh6eNesaAGC50XhbCrgD4-Cir42jQeMbTCYLWPUa782Hecm5bFpgaiqT0_7qnS8XZPICRl34yhJrHE7Ip43GIweuYbkvzJl22q9Guf4f_HeHAndcWlQtdyTQETtzlNgfnRrbghxpVKCRyXaHSe4rzxp1PaDAxtSv3ruTm323K1BtTbUngV1jTUs3pdmxcecpU22J176rW1RxMDJQ9XhANQ_lNJJZkoVBmKWzYCbwC1UYRdN5FEczKdNAplmWDgK_x9RgGiVhnMgwljKZZ2kskGzZen78bX98wvADhL14vQ?type=png)
*Each placeholder is replaced with its value to produce the final string.*


Below is the before/after of the same message.

| Concatenation | Template literal |
|---|---|
| `"Hi, " + name + "!"` | `` `Hi, ${name}!` `` |
| Quotes, plus signs and spaces to manage | One pair of backticks |
| Hard to see the final text | Reads like the final text |

## Embedding variables, and any expression

`${}` isn't limited to variable names. Anything that produces a value works: math, method calls, a ternary:

```js
const items = 3;
const msg = `You have ${items} ${items === 1 ? "item" : "items"} in your cart.`;
console.log(msg);
console.log(`Name: ${"asha".toUpperCase()}`);
console.log(`2 + 3 = ${2 + 3}`);
```

```text
You have 3 items in your cart.
Name: ASHA
2 + 3 = 5
```

The expression runs first, and its result is converted to a string. That also fixes the `53` problem from earlier, because the sum happens inside `${}`:

```js
const price = 5, tax = 3;
console.log(`Total: ${price + tax}`);
```

```text
Total: 8
```

A caution on that conversion. The value is converted the way `String()` converts it, which isn't always useful:

```js
console.log(`Price: ${{ a: 1 }}`);
console.log(`Value: ${undefined} and ${null}`);
```

```text
Price: [object Object]
Value: undefined and null
```

Objects print as `[object Object]`, and `undefined` prints as the word "undefined". Template literals won't stop you from shipping those into a message. Check the value first.

## Multi-line strings

With quotes, a line break needs `\n` and a `+` to join the pieces. With backticks, you press Enter:

```js
const a = "Line one\n" +
  "Line two\n" +
  "Line three";

const b = `Line one
Line two
Line three`;

console.log(a === b);
```

```text
true
```

The two strings are identical. The second one is just easier to write and to read.

The gotcha is that **every character between the backticks is part of the string**, including indentation:

```js
function show() {
  const text = `Hello
    indented line`;
  console.log(JSON.stringify(text));
}
show();
```

```text
"Hello\n    indented line"
```

Those four spaces are in the string. If you indent a template literal to match your code, the indentation ends up in the output. Start continuation lines at the left edge, or trim the result if it matters.

## Where you'll use them in modern JavaScript

**Messages and logs.** The most common use, as above.

**HTML snippets.** Multi-line plus interpolation fits well:

```js
const user = { name: "Asha", role: "admin" };
const html = `
<div class="card">
  <h2>${user.name}</h2>
  <p>${user.role}</p>
</div>`;
console.log(html);
```

```text

<div class="card">
  <h2>Asha</h2>
  <p>admin</p>
</div>
```

**URLs.** Values slot into a path or query string without `+`:

```js
const id = 42;
const limit = 10;
console.log(`https://api.example.com/users/${id}/posts?limit=${limit}`);
```

```text
https://api.example.com/users/42/posts?limit=10
```

**Receipts and reports.** Building lines in a loop reads cleanly:

```js
const items = [
  { name: "Pen", qty: 2, price: 10 },
  { name: "Notebook", qty: 1, price: 45 },
];
let total = 0;
for (const i of items) {
  const line = i.qty * i.price;
  total += line;
  console.log(`${i.name} x${i.qty} = ${line}`);
}
console.log(`Total: ${total}`);
```

```text
Pen x2 = 20
Notebook x1 = 45
Total: 65
```

There's also a more advanced feature called **tagged templates**, where a function processes the pieces of a template literal. Libraries use it for things like styled components and SQL helpers. I'm leaving it out here.

## When not to use a template literal

For a plain string with no variables, quotes are fine and backticks add nothing. Some teams enforce this with a lint rule.

The more important case is building **HTML or SQL from user input**. A template literal doesn't escape anything. If `user.name` contains markup or SQL, it goes straight into your string. For HTML, escape the value or set text content instead of building markup. For SQL, use parameterised queries from your database library, not interpolation. The HTML example above is safe only because I wrote the values myself.

## Where this leaves you

Use backticks whenever a string contains a variable or spans lines, and keep quotes for plain text. The gain is readability; the behaviour is the same string either way.

One limit: this post doesn't cover tagged templates or `String.raw`. Do you use template literals for everything, or do you keep quotes for strings without variables?
