---
title: "Why x => { x * 2 } Returns undefined: Arrow Function Basics"
slug: javascript-arrow-functions
subtitle: Arrow function syntax, one and many parameters, implicit vs explicit return, and how they differ from normal functions, with real output
tags: javascript, web-development, beginners, programming, tutorial
cover: ./cover.png
seoTitle: "JavaScript Arrow Functions Explained for Beginners"
seoDescription: "JavaScript arrow functions: syntax, one or many parameters, implicit vs explicit return, the curly-brace trap, and map(), with real output."
enableToc: true
---

This arrow function looks correct, and `double(4)` returns `undefined`:

```js
const double = x => { x * 2 };
console.log(double(4));
```

```text
undefined
```

Nothing is broken. The braces changed what the function does, and that one detail is the heart of **arrow functions**: a shorter way to write a function, with a few rules about `return` that you need to know. All outputs below are real runs on Node.js 24.22.1.

## What arrow functions are

An arrow function is a function written with `=>` instead of the `function` keyword. It does the same job with less to type. Here's a normal function that squares a number, next to two arrow versions:

```js
function square(n) {
  return n * n;
}
const squareArrow = (n) => {
  return n * n;
};
const squareShort = n => n * n;
console.log(square(5), squareArrow(5), squareShort(5));
```

```text
25 25 25
```

Three functions, one result. The last one dropped the `function` keyword, the braces and the word `return`. Less boilerplate means less to read, which is why modern JavaScript leans on them, especially for short functions passed to other functions.

## Converting a normal function, step by step

Take the `square` function and change it one piece at a time:

1. Remove the keyword `function` and the name. Store the function in a `const` instead.
2. Put `=>` between the parameters and the body.
3. If the body is a single expression, drop the braces and `return`.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    A["function square(n) { return n * n; }"] --&gt; B["const square = (n) => { return n * n; }"]
    B --&gt; C["const square = n => n * n"]
-->
![Conversion flow: function square(n) { return n * n; } becomes const square = (n) => { return n * n; }, which becomes const square = n => n * n](https://mermaid.ink/img/pako:eNptkUFPwkAUhP_Ky5zUFNKWlm7XQCJ41ItHWQ6bdoEmdBcfuxFt-t9Nq3jR47zMN5PM61C52kBid3Tv1UGzp6cXxcoSET1sFHbBVr5xls5vQbO5sbfUERsf2JKlO7L31CtsaTJZ0mqjUDl79j9mWtDgXyz_Ra4tq5Fd_2XtQI6AwhYR9tzUkJ6DidAabvUg0Q0pCv5gWqMgSYFNHS6Tyh0dKyjbI8JJ21fn2ivNLuwPkDt9PJsI4VRrbx4bvWfd_l7Z2Nrw2gXrIbN0zIDscIHMEjFNRTkvkzgpi1k8i_ABmaTpNEvzdCZEEYuiLIs-wufYGk_TeZLPRZILMc_KIo9g6sY7fv4ef_xB_wXPR3gx?type=png)
*Each step removes one piece: the keyword and name first, then the braces and return.*

Each step gives you a working function. You can stop at step 2 and still be writing a normal, valid arrow function.

## Syntax breakdown

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    P["(a, b)<br/>parameters"] --&gt; Arrow["=><br/>the arrow"] --&gt; Body["a + b<br/>body / result"]
-->
![Arrow function parts: the parameters (a, b) on the left, the arrow =>, and the body a + b, which is the result](https://mermaid.ink/img/pako:eNo9kEtvwjAQhP-KNadWNZCEPByrRerj2EpVj405OHghSEmMFkdAEf-9IhU97rczu6M5Y-UdQWPd-sOqsRzE-5dh0wshxGdlcGelqO8fa54tdpZtR4F4b7AUk8lCPDP7Q2XwtBgFoSFhr-i2f_HuVBlY8SDqUVF7dxIzwbQf2mCwhMSGtw468EASHXFnryPO1wQGoaGODLQwYHLDcbLyrWcD018gsbP9t_fdzc1-2DTQa9vuSWLYORvobWs3bLt_ytQ74lc_9AE6zccb0GccodNYTRNV5mUcxWUxj-YSJ-g4SaZpkiVzpYpIFWVZXCR-xq_RNMnjLFdxplSelkUmQW4bPH_8VTo2e_kFmw1sfw?type=png)
*Parameters on the left, the arrow in the middle, the result on the right.*

An arrow function has three parts: the parameters on the left, the arrow `=>`, and the body on the right. The arrow reads as "takes these, gives back that".

## One parameter, no parameters, many parameters

The parentheses around the parameters depend on how many you have:

```js
const greet = name => `Hello, ${name}!`;   // one parameter: parentheses optional
const add = (a, b) => a + b;               // two or more: parentheses required
const sayHi = () => "Hi there";            // none: empty parentheses required

console.log(greet("Asha"));
console.log(add(2, 3));
console.log(sayHi());
```

```text
Hello, Asha!
5
Hi there
```

My habit is to always write the parentheses, even for one parameter. It's one rule instead of three, and adding a second parameter later doesn't force an edit to the first. Both styles are valid, so follow whatever your team does.

## Implicit return vs explicit return

This is the part that produced the `undefined` at the top. There are two ways to give a value back.

**Implicit return** has no braces. The expression after `=>` is returned automatically:

```js
const doubleImplicit = x => x * 2;
```

**Explicit return** uses braces and the `return` keyword. Braces open a function body, a block of statements. Nothing leaves a block unless you `return` it:

```js
const double = x => { x * 2 };           // ❌ braces, no return
const doubleOk = x => { return x * 2; }; // ✅ braces and return

console.log(double(4));
console.log(doubleOk(4));
```

```text
undefined
8
```

`x * 2` was calculated and then thrown away, so the function returned `undefined`. The rule: **braces mean you must write `return`; no braces means the value is returned for you.** Use explicit return when the body needs more than one statement.

### The object literal trap

Returning an object is where the two rules collide. JavaScript reads `{` after `=>` as a function body, not an object:

```js
const makeUserBad = name => { name: name };    // ❌ a body containing a label
const makeUser = name => ({ name: name });     // ✅ parentheses make it an object

console.log(makeUserBad("Asha"));
console.log(makeUser("Asha"));
```

```text
undefined
{ name: 'Asha' }
```

Wrap the object in parentheses and JavaScript treats it as a value. It's the same braces problem as before, in a different outfit.

## Arrow function vs normal function: the basics

Arrow functions are not only shorter. Three differences matter early on.

**1. Syntax.** Shorter, with implicit return available, as shown above.

**2. You can't call them before their line has run.** A function declaration can be used before the line that defines it. An arrow function stored in a `const` can't:

```js
console.log(hello("Asha"));            // works: declarations are hoisted
function hello(n) { return "Hello, " + n; }

try {
  console.log(hi("Asha"));             // fails: the const doesn't exist yet
} catch (e) {
  console.log(e.name + ": " + e.message);
}
const hi = n => "Hi, " + n;
```

```text
Hello, Asha
ReferenceError: Cannot access 'hi' before initialization
```

Strictly, this comes from `const`, not from the arrow: a normal function expression stored in a `const` (`const g = function (n) { ... }`) fails with the same `ReferenceError` when called early. I covered this in [function declarations vs expressions](https://jaydeepkanzariya.hashnode.dev/function-declaration-vs-expression).

**3. They don't get their own `this`.** I'm keeping this short on purpose. A normal function gets `this` from how it's called. An arrow function doesn't create one and uses whatever `this` surrounds it:

```js
const user = {
  name: "Asha",
  regular() { return this.name; },
  arrow: () => this.name,
};
console.log(user.regular());
console.log(user.arrow());
```

```text
Asha
undefined
```

This ran as a CommonJS file in Node, where the outer `this` isn't `user`. The takeaway for now: **don't use an arrow function as an object method.** The full story is in [how JavaScript decides what `this` is](https://jaydeepkanzariya.hashnode.dev/javascript-this-keyword).

When not to use an arrow function: as an object method (above), and as a constructor, because `new` on an arrow function throws `TypeError: Person is not a constructor`. For short callbacks, use arrows freely.

## The assignment, solved

**1 and 2. Square: normal, then arrow.** Both are in the first example, so here's the final form:

```js
function square(n) {
  return n * n;
}
const squareArrow = n => n * n;
```

**3. Even or odd.** One parameter, one expression, so an implicit return fits:

```js
const isEvenOrOdd = n => (n % 2 === 0 ? "even" : "odd");
console.log(isEvenOrOdd(4), isEvenOrOdd(7));
```

```text
even odd
```

`n % 2` is the remainder after dividing by 2. Zero means even.

**4. Arrow function inside `map()`.** `map` runs a function on every item and collects the results in a new array. This is where arrows earn their place:

```js
const isEvenOrOdd = n => (n % 2 === 0 ? "even" : "odd");   // from the previous example
const numbers = [1, 2, 3, 4, 5];

const squares = numbers.map(n => n * n);
console.log(squares);

const labels = numbers.map(n => isEvenOrOdd(n));
console.log(labels);

const withFunction = numbers.map(function (n) {
  return n * n;
});
console.log(withFunction);
```

```text
[ 1, 4, 9, 16, 25 ]
[ 'odd', 'even', 'odd', 'even', 'odd' ]
[ 1, 4, 9, 16, 25 ]
```

The first and third give identical results. One is a single short line, the other is four lines of ceremony.

## Where this leaves you

Arrow functions cut the boilerplate for short functions. Remember one rule: braces need `return`, no braces returns for you. Wrap returned objects in parentheses.

This post skipped `this` on purpose, and arrow functions behave very differently there in more cases than the one I showed. I also haven't covered the `arguments` object.

Do you write the parentheses around a single parameter, or drop them? I'm curious whether anyone sticks with the short form.
