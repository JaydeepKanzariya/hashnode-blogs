---
title: "Why \"5\" + 3 Is \"53\": JavaScript Operators for Beginners"
slug: javascript-operators-basics
subtitle: Arithmetic, comparison, logical and assignment operators, what each one returns, and the few that don't behave like maths
tags: javascript, web-development, beginners, programming, frontend
cover: ./cover.png
seoTitle: "JavaScript Operators: The Basics You Need to Know"
seoDescription: "JavaScript operators for beginners: arithmetic, comparison, logical and assignment, == vs === explained, and real console output for every example."
enableToc: true
---

Open your browser's console and type this:

```js
console.log("5" + 3);
```

```text
53
```

Not `8`. The string `"53"`. Most JavaScript operators behave exactly like the maths you already know, and a few don't. This post covers the everyday operators (arithmetic, comparison, logical and assignment) and gives the surprising ones the attention they need. Every output below is real, from Node.js 24.22. Your browser console prints the same values.

## What an operator is

An **operator** is a symbol that does something with values. The values it works on are its **operands**.

```js
2 + 3; // operator: +   operands: 2 and 3   result: 5
```

Every operator produces a result. That's the key thing to watch: *what* it returns, and what *type* that is.

| Category | Operators | Example | Returns |
|---|---|---|---|
| Arithmetic | `+` `-` `*` `/` `%` | `17 % 5` | a number (usually) |
| Comparison | `==` `===` `!=` `!==` `>` `<` | `5 === "5"` | `true` or `false` |
| Logical | `&&` `\|\|` `!` | `age >= 18 && hasTicket` | one of its values |
| Assignment | `=` `+=` `-=` | `score += 5` | stores a new value |

## Arithmetic operators: + - * / %

With two numbers, these do what you'd expect:

```js
const a = 17, b = 5;
a + b; // 22
a - b; // 12
a * b; // 85
a / b; // 3.4
a % b; // 2
```

`/` gives decimals. There's no separate "whole number division". And `%` is the **remainder**: 17 divided by 5 is 3, with 2 left over. Its everyday job is checking even and odd numbers:

```js
8 % 2; // 0  → even
7 % 2; // 1  → odd
```

### The + surprise

`+` has two jobs: adding numbers and joining strings. If either side is a string, it joins:

```text
"5" + 3        "53"
3 + 4 + "px"   "7px"
"px" + 3 + 4   "px34"
```

It works left to right. `3 + 4` is added first (both numbers), then joined with `"px"`. In the last line, `"px" + 3` is already a string, so `4` gets joined too.

The other arithmetic operators only do maths, so they convert strings to numbers instead:

```text
"5" - 3        2
"5" * "2"      10
"abc" * 2      NaN
```

`NaN` means "Not a Number": the result of maths that couldn't produce one. This is why values from a form input, which are always strings, need `Number(value)` before you add them.

Two more you'll meet early:

```text
10 / 0         Infinity
0.1 + 0.2      0.30000000000000004
```

Dividing by zero doesn't crash; it gives `Infinity`. And decimals are stored in binary, so some can't be represented exactly. That's true in most programming languages, not just JavaScript. For money, work in whole paise or cents.

## Comparison operators: == === != > <

Comparisons always return `true` or `false`. `>` and `<` behave as expected with numbers. The ones to get right are the equality checks.

### == vs ===

`===` (strict equality) checks that the value **and** the type are the same. `==` (loose equality) first **converts** the two sides to a common type, then compares. Side by side:

| Comparison | `==` | `===` |
|---|---|---|
| `5` and `"5"` | `true` | `false` |
| `0` and `false` | `true` | `false` |
| `""` and `0` | `true` | `false` |
| `null` and `undefined` | `true` | `false` |

`==` says an empty string equals zero. That's the conversion at work, and it's almost never what you meant. The not-equal versions follow the same pattern: `5 != "5"` is `false`, `5 !== "5"` is `true`.

**The rule: use `===` and `!==`.** If the types might differ, convert on purpose first, `Number(input) === 17`, so anyone reading the code can see it. (One oddity to know: `NaN === NaN` is `false`. To check for it, use `Number.isNaN(value)`.)

### Comparing strings

Strings compare character by character, alphabetically:

```text
"apple" < "banana"   true
"10" < "9"           true
"10" > 9             true
```

`"10" < "9"` is `true` because `"1"` comes before `"9"`. It's comparing text, not numbers. Mix a string with a number (`"10" > 9`) and the string is converted, so you get the numeric answer. Convert first and you never have to remember which is which.

## Logical operators: && || !

Logical operators combine conditions:

- `&&` (AND) is true when **both** sides are true.
- `||` (OR) is true when **at least one** side is true.
- `!` (NOT) flips true to false, and false to true.

| A | B | A && B | A \|\| B | !A |
|---|---|---|---|---|
| true | true | true | true | false |
| true | false | false | true | false |
| false | true | false | true | true |
| false | false | false | false | true |

A real condition:

```js
if (age >= 18 && hasTicket && !isBanned) {
  console.log("Entry allowed");
}
```

### They return values, not just true or false

Here's the part beginners don't expect. `&&` and `||` return **one of their operands**, not necessarily a boolean:

```text
"" || "Guest"          "Guest"
"Asha" || "Guest"      "Asha"
null && "never"        null
"Asha" && "Hi Asha"    "Hi Asha"
```

`||` returns the first "truthy" value, or the last one if none are. `&&` returns the first "falsy" value, or the last one if all are truthy. The falsy values are `false`, `0`, `""`, `null`, `undefined` and `NaN`; everything else is truthy. That's why `const name = input || "Guest"` is a common way to set a default. They also stop early: in `null && "never"`, the right side isn't evaluated at all.

The catch: `0 || 10` gives `10`, because `0` is falsy, even if `0` was a perfectly valid value. The `??` operator only falls back on `null` or `undefined`: `0 ?? 10` gives `0`. Use `??` when `0` or `""` are real answers.

## Assignment operators: = += -=

`=` stores a value in a variable. `+=` and `-=` are shorthand for "update this variable using its current value":

```js
let score = 10;
score += 5; // same as score = score + 5  → 15
score -= 3; // same as score = score - 3  → 12

let greeting = "Hello";
greeting += ", Asha"; // "Hello, Asha" (+= joins strings too)
```

The classic bug is using `=` where you meant `===`:

```js
let x = 1;
if (x = 5) {
  console.log("if (x = 5) ran; x is now", x);
}
```

```text
if (x = 5) ran; x is now 5
```

`x = 5` doesn't compare. It **assigns** 5 to `x`, and the result, `5`, is truthy, so the `if` always runs. One `=` assigns, three `===` compare.

## Try it: the assignment

Here are the three tasks from the cohort brief in one script:

```js
// 1. Arithmetic on two numbers
const a = 17;
const b = 5;
console.log("Sum:", a + b);
console.log("Difference:", a - b);
console.log("Product:", a * b);
console.log("Quotient:", a / b);
console.log("Remainder:", a % b);

// 2. Compare two values with == and ===
const typed = "17"; // what an <input> gives you: always a string
console.log("a == typed:", a == typed);
console.log("a === typed:", a === typed);
console.log("a === Number(typed):", a === Number(typed));

// 3. A small condition with logical operators
const age = 20;
const hasTicket = true;
const isBanned = false;
if (age >= 18 && hasTicket && !isBanned) {
  console.log("Entry allowed");
} else {
  console.log("Entry denied");
}
```

```text
Sum: 22
Difference: 12
Product: 85
Quotient: 3.4
Remainder: 2
a == typed: true
a === typed: false
a === Number(typed): true
Entry allowed
```

Look at the middle three lines. `==` says the number `17` and the string `"17"` are equal; `===` says they aren't. Converting with `Number()` first gives you `true` *and* makes the intent obvious.

The takeaway: **operators behave like maths until types get mixed. `+` joins when it sees a string, `==` converts before comparing, and `&&`/`||` hand back values, not just booleans.** Use `===`, convert input on purpose, and most surprises go away. This post skipped operator precedence and the less common operators (`**`, `++`, `?.`); they follow the same "check what it returns" habit.

Paste `[] + []` and `[] + {}` into your console. Can you explain what `+` did with each?
