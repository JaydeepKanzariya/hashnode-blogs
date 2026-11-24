---
title: "Pass the Function, Don't Call It: Callbacks in JavaScript Explained"
slug: javascript-callbacks
subtitle: Functions as values, what a callback is, why callbacks aren't always async, and how nesting turns into callback hell, with real output
tags: javascript, web-development, beginners, programming, callbacks
cover: ./cover.png
seoTitle: "Callbacks in JavaScript Explained: Functions as Arguments"
seoDescription: "Callbacks in JavaScript explained: functions as values, sync vs async callbacks, error-first callbacks, callback hell, and why promises replaced them."
enableToc: true
---

Here's a line beginners write all the time, and what it actually does:

```js
function greet() {
  console.log("Hello!");
}

console.log("1. before");
setTimeout(greet(), 1000);   // oops: the parentheses call greet right now
console.log("2. after");
```

```text
1. before
Hello!
TypeError [ERR_INVALID_ARG_TYPE]: The "callback" argument must be of type function. Received undefined
```

`"Hello!"` printed **immediately**, and then JavaScript crashed. The parentheses in `greet()` don't pass the function to `setTimeout`. They **call** `greet` on the spot and pass along what it returned, which is `undefined`. One pair of parentheses is the difference between handing a function over and running it.

Here's the fixed version:

```js
function greet() {
  console.log("Hello!");
}

console.log("1. before");
setTimeout(greet, 1000);     // pass the function itself
console.log("2. after");
```

```text
1. before
2. after
Hello!
```

Without the parentheses, `greet` itself goes to `setTimeout`, which calls it a second later. That handed-over function is a **callback**. This post covers what callbacks are, why they exist, where you meet them, and the problem that made people look for something better. Every output is real, from Node.js 24.22, plus Chrome 157 for the event example.

## Functions are values

In JavaScript, a function is a **value**, just like a number or a string. You can store it in a variable, put it in an array, pass it to another function, and return it from one:

```js
function shout(text) {
  return text.toUpperCase() + "!";
}

const same = shout;                       // stored in another variable
console.log(same("hello"));

const tools = [shout, (t) => t.length];   // stored in an array
console.log(tools[1]("hello"));

function makeGreeter(greeting) {          // returned from a function
  return (name) => `${greeting}, ${name}`;
}
console.log(makeGreeter("Namaste")("Asha"));
```

```text
HELLO!
5
Namaste, Asha
```

Nothing special happened. `shout` and `same` are two names for one function, `tools[1]` pulled a function out of an array and called it, and `makeGreeter` returned a brand-new function. Everything about callbacks follows from this one fact. (If the arrow syntax is new, see [function declarations vs expressions](https://jaydeepkanzariya.hashnode.dev/function-declaration-vs-expression).)

## What a callback is

A **callback** is a function you pass to another function, so that function can call it. The name says it: you give it something to *call back*. Here's the simplest case, with no waiting involved:

```js
function calculate(a, b, operation) {
  return operation(a, b);        // call back the function we were given
}

const add = (x, y) => x + y;
const multiply = (x, y) => x * y;

console.log(calculate(4, 5, add));
console.log(calculate(4, 5, multiply));
```

```text
9
20
```

`calculate` doesn't know what `operation` does. It calls whatever it was given. Pass `add` and you get 9; pass `multiply` and you get 20. That's the point of callbacks: **the caller decides what happens, and the function decides when.**

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    C["Caller: calculate(4, 5, add)"] --&gt;|"passes add along"| F["calculate runs"]
    F --&gt;|"calls back: add(4, 5)"| A["add runs and returns 9"]
    A --&gt;|"hands 9 back"| F
    F --&gt;|"returns 9"| C
-->
![Function calling another function flow: the caller runs calculate(4, 5, add) and passes add along; calculate runs and calls back add(4, 5); add returns 9 to calculate; calculate returns 9 to the caller](https://mermaid.ink/img/pako:eNpd0T1vwjAQgOG_crqpSAblk9geKqFUTO3SsZjhGpsE1bGRk6i0wH-vkkKFOt5Jz3vDnbDy2qDEnfWfVUOhh-dXFZQDACg3Ckuy1gQJFdlqsNSbh4xBzoC0nincwnz-eFZ4oK4z3bgEst7VCs-w3ij8UxAG1ync3tLrK6zI2g7eqfqQo57is1GvNgrH3OiAnIZg-iG4DsRdZXWtNOR0B2LqTKf_n7nDZyiRYR32GmUfBsOwNaGlccTTqBT2jWmNQgkj1MNxXnnrg0LlLsjwQO7N-_amgx_qBuWObGcYDgdNvXnaUx2o_dsG47QJpR9cjzKNpgbKEx5RZjFfJFwsRRzFokijlOEXyjhJFlmSJynnRcQLIYoLw-_parRIlnG-5HHO-TITRc7Q6H3vw8vvI6d_Xn4A8MuQrQ?type=png)
*The caller passes the function in. The receiving function calls it and returns the answer.*

## Callbacks aren't always async

Most people meet callbacks through timers and assume a callback means waiting. It doesn't. Compare two callbacks:

```js
console.log("A. before forEach");
[1, 2, 3].forEach((n) => console.log("   callback got", n));
console.log("B. after forEach");

setTimeout(() => console.log("   timer callback"), 0);
console.log("C. after setTimeout");
```

```text
A. before forEach
   callback got 1
   callback got 2
   callback got 3
B. after forEach
C. after setTimeout
   timer callback
```

`forEach` ran its callback three times **before** line B: no waiting, the callback was just part of the normal flow. The timer's callback waited until the rest of the code had finished, even with a delay of 0 ms. A callback is neutral. Whether it runs now or later depends on the function that receives it. I explained the "later" case in [synchronous vs asynchronous JavaScript](https://jaydeepkanzariya.hashnode.dev/synchronous-vs-asynchronous-javascript).

## Why callbacks exist in async code

Some work takes time: reading a file, asking a server, waiting for a timer. JavaScript can't stop and wait, because that would freeze everything, so instead you hand over **what to do when it's done** and carry on. The callback is that instruction: "when you finish, call this."

Many of Node's built-in functions follow a convention for this. The callback's first parameter is an error (or `null`), and the result comes second. It's called an **error-first callback**:

```js
const fs = require("node:fs");
fs.writeFileSync("note.txt", "hello from a file");

fs.readFile("note.txt", "utf8", (err, data) => {
  console.log("existing file:", err, "|", data);

  fs.readFile("missing.txt", "utf8", (err, data) => {
    console.log("missing file:", err && err.code, "|", data);
  });
});
```

```text
existing file: null | hello from a file
missing file: ENOENT | undefined
```

When the read worked, `err` was `null` and `data` held the contents. When the file was missing, `err.code` was `ENOENT` and there was no data. You check the error first, every time. I read the second file inside the first callback so the two lines print in a predictable order. That small move is where nesting starts.

## Callbacks in common scenarios

You'll meet callbacks in four places, all shown above or below:

- **Array methods** like `forEach`: the callback runs immediately, once per item.
- **Timers** like `setTimeout`: the callback runs later.
- **File and network work in Node**, like `readFile`: the callback runs when the work finishes, error first.
- **Browser events**: the callback runs each time the event happens.

Here's the last one, run in Chrome's console:

```js
const button = document.createElement("button");
button.textContent = "Add to cart";

button.addEventListener("click", () => {
  console.log("callback ran: button clicked");
});

console.log("before click");
button.click();
console.log("after click");
```

```text
before click
callback ran: button clicked
after click
```

`button.click()` simulates a click, so the callback ran right there. With a real user, it runs whenever they click: once, ten times, or never.

## The problem with nesting

Callbacks work well for one step. The trouble starts when each step needs the result of the one before. Here's ordering a pizza: place the order, then cook it, then deliver it. Each step is asynchronous (simulated with short timers):

```js
function placeOrder(item, callback) {
  setTimeout(() => callback(null, { id: 101, item }), 50);
}
function cook(order, callback) {
  setTimeout(() => callback(null, `${order.item} for order ${order.id}, cooked`), 50);
}
function deliver(food, callback) {
  setTimeout(() => callback(null, `${food}, delivered`), 50);
}

placeOrder("pizza", (err, order) => {
  if (err) return console.error("order failed:", err.message);
  cook(order, (err, food) => {
    if (err) return console.error("cooking failed:", err.message);
    deliver(food, (err, result) => {
      if (err) return console.error("delivery failed:", err.message);
      console.log(result);
    });
  });
});
```

```text
pizza for order 101, cooked, delivered
```

It works. But look at the shape: each step sits **inside** the previous callback, so the code drifts to the right. Every level also repeats its own `if (err)` check. Add a fourth step, like sending a receipt, and everything shifts again. This is **callback hell**, also called the "pyramid of doom".

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart TD
    A["placeOrder('pizza', callback 1)"] --&gt;|"50 ms later"| B["callback 1 runs: cook(order, callback 2)"]
    B --&gt;|"50 ms later"| C["callback 2 runs: deliver(food, callback 3)"]
    C --&gt;|"50 ms later"| D["callback 3 runs: print the result"]
    A -.-> E["an if (err) check at every level"]
    B -.-> E
    C -.-> E
-->
![Nested callback execution flow: placeOrder('pizza', callback 1) runs, and 50 ms later callback 1 runs cook(order, callback 2); 50 ms later callback 2 runs deliver(food, callback 3); 50 ms later callback 3 prints the result; every level has its own if (err) check](https://mermaid.ink/img/pako:eNpt0ktPwzAMAOC_YvnCkNqpj3Vtc0CCjSPiwomFQ0i8tVraVF46YGP_Ha28isTRlv3ZlnxE7QyhwLV1L7pS7OFhKVm2AADXK4mdVZru2RBPLrr6cFAXAWhl7bPSW4gvJT5BGF69S8wiaHZglSeW-A43K4m_dcB9uxOgndtO3BkbIckZ-R5587-2GGvJl2bI1nviydo5M_LSsbf431uOvfTL67huPfiKgGnXWz9iriGchldwu5KoWqjXMCHmS9AV6S0oD7QnfgNLe7J_jxm6RssMMQa44dqg8NxTgA1xo84hHs91En1FDUkUIJHJ9K-hdtaxRNmeMMBOtY_ONd_d7PpNhWKt7I4C7DujPC1rtWHV_GSZWkO8cH3rUaSzwUBxxFcUs7iYJkU5L-MoLvM0SgN8QxEnyXSWZElaFHlU5GWZnwI8DFOjaTKPs3kRZ0Uxn5V5FiCZ2ju--3yk4Z9OHwfst_w?type=png)
*Each step starts inside the previous callback, and every level repeats its own error check.*

Callbacks themselves aren't the problem. The problem is that the order of events is stored in the **indentation**, which makes the code hard to read and hard to change.

## Other callback problems

**Trust.** When you give a function your callback, you trust it to call it exactly once. If it doesn't, your code runs twice:

```js
function buggyCharge(callback) {
  callback(null, "paid");
  callback(null, "paid");   // a bug: calls back twice
}

let charges = 0;
buggyCharge(() => {
  charges++;
  console.log("charging the card, charge #" + charges);
});
```

```text
charging the card, charge #1
charging the card, charge #2
```

The card was charged twice. Your callback can't stop a function from calling it twice, and that bug lives in code you may not control.

**Errors don't travel.** An error thrown inside a callback that runs later can't be caught by a `try`/`catch` around the call that started the work. I showed that with real output in [try/catch/finally in JavaScript](https://jaydeepkanzariya.hashnode.dev/javascript-error-handling).

These two problems, along with the pyramid, are what [promises](https://jaydeepkanzariya.hashnode.dev/javascript-promises-explained) were designed to fix, and [async/await](https://jaydeepkanzariya.hashnode.dev/javascript-async-await) makes them read like ordinary code.

## When callbacks are still the right tool

Callbacks haven't gone away, and they shouldn't. Use them for **event handlers**, **array methods** and **one-step jobs**: a single callback, no dependent steps, no nesting. Reach for promises or async/await when steps start to depend on each other.

The takeaway: **a callback is a function you pass to another function so it can call it. `greet` hands it over; `greet()` runs it. Callbacks can run immediately (`forEach`) or later (`setTimeout`, `readFile`), and nesting them for dependent steps is what turns into callback hell.** This post stayed with the idea and skipped related tools like `setInterval` and `util.promisify`.

Look at a `setTimeout` or `addEventListener` call in your own code. Are you passing the function, or accidentally calling it?
