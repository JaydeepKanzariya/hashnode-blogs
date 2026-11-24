---
title: "Call It Before You Define It: Function Declarations vs Expressions"
slug: function-declaration-vs-expression
subtitle: Two ways to write a JavaScript function, the one situation where they behave differently, and hoisting in plain language
tags: javascript, web-development, beginners, programming, frontend
cover: ./cover.png
seoTitle: "Function Declaration vs Expression in JavaScript"
seoDescription: "Function declaration vs function expression in JavaScript: syntax side by side, hoisting in plain language, real errors, and when to use each one."
enableToc: true
---

Here are two functions that add two numbers:

```js
function addDecl(a, b) { return a + b; }
const addExpr = function (a, b) { return a + b; };

console.log(addDecl(2, 3), addExpr(2, 3)); // 5 5
```

Both print `5`. They take the same inputs and return the same result. Now move each call **above** the line that defines the function. The first one still works. The second one crashes:

```text
ReferenceError: Cannot access 'addExpr' before initialization
```

That's the difference between a **function declaration** and a **function expression**, and almost the only one you'll notice day to day. This post covers both, side by side, with hoisting explained just enough to see why. Every output is real, from Node.js 24.22.

## What functions are and why we need them

A **function** is a reusable block of code with a name. You give it inputs (**parameters**), it runs its body, and it hands back a result with `return`.

Without functions, you'd repeat the same logic everywhere you needed it. With one, you write it once and call it as often as you like:

```js
function add(a, b) {
  return a + b;
}

add(2, 3);   // 5
add(10, 20); // 30
add(-1, 1);  // 0
```

Fix a bug in `add`, and every call gets the fix.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    C["add(2, 3)<br/>the call"] --&gt;|a = 2, b = 3| B["Function body runs<br/>return a + b"]
    B --&gt;|returns 5| R["Result used<br/>where it was called"]
-->
![Execution flow of a function call: the call add(2, 3) passes a = 2 and b = 3 into the function body, which runs return a + b and returns 5 to where it was called](https://mermaid.ink/img/pako:eNo9kctuwjAQRX9lNKtWNZQ4hDxUWEDVVbthWczCiQcSKbHRxBZQ4N8rUtHl3NE5d3EvWDlDWOCudceq1uzhc61YWQCA1UahNuZJCoif30p-XfiaoNJtq3ALo9HiqmEOUkAJc4ivsNwo_Ai28o2zUDpzBg62H0AmH9iChhcoFW4fDcvB8vfsIbnCeqNwTX1oPYSezMAea2KCxsNR90M7GYVbFLjnxmDhOZDAjrjT9xMvd7VCX1NHCgtQyGTCaVS51rFCZW8o8KDtt3Pdg2YX9jUWO932JDAcjPb03ug96-4_ZbKGeOWC9VikcnBgccETFtMoG8ssn-XRJMrTeBILPGMRSTmeykTGWZZOsjTP05vAn6F1MpazKJllUZJls2meJgLJNN7x198awyi3X1JNf3E?type=png)
*Arguments go in, the body runs, and the return value comes back to the call.*

## Function declaration syntax

A **function declaration** starts with the `function` keyword, as its own statement:

```js
function multiply(a, b) {
  return a * b;
}
```

- `function`: the keyword that starts it.
- `multiply`: the name. **Required** in a declaration.
- `(a, b)`: the parameters.
- `{ return a * b; }`: the body.

## Function expression syntax

A **function expression** creates a function as a **value** and stores it in a variable:

```js
const multiply = function (a, b) {
  return a * b;
};
```

The function itself has no name here. The variable `multiply` holds it, and you call it through the variable, exactly like a declaration: `multiply(4, 5)`. Note the semicolon at the end: the whole line is an assignment.

Two variations you'll see:

```js
// Arrow function: a shorter function expression
const multiplyArrow = (a, b) => a * b;

// Named function expression: the name is visible only inside the function
const factorial = function fact(n) {
  return n <= 1 ? 1 : n * fact(n - 1);
};
```

`factorial(5)` returns `120`, and outside the function, `typeof fact` is `undefined`. The inner name is handy for recursion and shows up in error stack traces.

Because a function expression is just a value, you can create one exactly where it's needed, for example as a callback:

```js
[1, 2, 3].map(function (n) { return n * 2; }); // [ 2, 4, 6 ]
```

## Side by side

Once defined, the two are interchangeable. Both are real functions (`typeof` gives `"function"` for each), and calling them works the same way. The differences are about **how they're created**:

| | Function declaration | Function expression |
|---|---|---|
| Syntax | `function add(a, b) { … }` | `const add = function (a, b) { … };` |
| Name | Required | Optional (usually anonymous) |
| Callable before its line | Yes | No |
| Can be used as a value inline | No, it's a statement | Yes: callbacks, arguments, object properties |
| Typical form today | Top-level named helpers | `const` + arrow function, callbacks |

## Hoisting, at a very high level

Here's the experiment: call each style **before** the line that defines it.

```js
console.log(greet("Asha"));
function greet(name) { return `Hello, ${name}`; }
```

```text
Hello, Asha
```

The declaration works before its definition. Now the expression:

```js
console.log(greet("Asha"));
const greet = function (name) { return `Hello, ${name}`; };
```

```text
ReferenceError: Cannot access 'greet' before initialization
```

Same with an arrow function stored in `const`. And with the older `var`, the error changes:

```js
console.log(typeof greet); // undefined
console.log(greet("Asha"));
var greet = function (name) { return `Hello, ${name}`; };
```

```text
TypeError: greet is not a function
```

The plain-language version of why: **before running your code, JavaScript first sets up the names it finds in the current scope.** That's called **hoisting**.

- A **function declaration** is set up completely in that first pass, name *and* function. So it's ready from the first line.
- A **function expression** is only a value assigned to a variable. The variable name is known early, but it only gets its function **when that line runs**. Before then, a `const` or `let` variable can't be touched at all (a `ReferenceError`), and a `var` variable is `undefined`, so calling it is a `TypeError`.

That's all the hoisting you need for this: declarations work early; expressions don't.

## When to use each

There's no wrong choice once you know the hoisting rule. In practice:

**Use a declaration** for a named, standalone helper that other code in the file calls, especially if you like putting the main logic at the top and the helpers below it. Hoisting is what makes that order work.

**Use an expression** (often an arrow function) when the function is a value: a callback passed to `map` or `addEventListener`, a function stored in an object, or one chosen conditionally. Many codebases also prefer `const` expressions everywhere precisely *because* they can't be used before they're defined. Code then reads top to bottom with no surprises.

What matters more than which you pick is picking one style per project. Linters can enforce it: ESLint's `func-style` rule chooses between the two, and `no-use-before-define` flags calls that rely on hoisting.

## Try it: the assignment

The brief's four steps in one script, with the "call before defining" test first:

```js
// 4. Try calling them BEFORE they are defined
console.log("multiply before definition:", multiply(4, 5));
try {
  console.log("multiplyExpr before definition:", multiplyExpr(4, 5));
} catch (err) {
  console.log("multiplyExpr before definition:", `${err.name}: ${err.message}`);
}

// 1. Function declaration
function multiply(a, b) {
  return a * b;
}

// 2. Same logic as a function expression
const multiplyExpr = function (a, b) {
  return a * b;
};

// 3. Call both and print the results
console.log("multiply(4, 5):", multiply(4, 5));
console.log("multiplyExpr(4, 5):", multiplyExpr(4, 5));
```

```text
multiply before definition: 20
multiplyExpr before definition: ReferenceError: Cannot access 'multiplyExpr' before initialization
multiply(4, 5): 20
multiplyExpr(4, 5): 20
```

The first two lines are the whole lesson. The declaration answered `20` before it was even written; the expression refused. After both are defined, they give the same answer.

The takeaway: **a function declaration is ready before your code runs; a function expression is ready only once its line has run. Everything else about them is the same.** This post kept hoisting at a high level and skipped how it works with `let`, `const` and classes in detail, which follows from the same idea.

Do you put your helper functions above or below the code that uses them, and does your style rely on hoisting without you noticing?
