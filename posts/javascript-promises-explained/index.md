---
title: "A Value That Isn't Here Yet: JavaScript Promises for Beginners"
slug: javascript-promises-explained
subtitle: What problem promises solve, their three states, handling success and failure, and how chaining replaces nested callbacks
tags: javascript, web-development, beginners, programming, frontend
cover: ./cover.png
seoTitle: "JavaScript Promises Explained for Beginners"
seoDescription: "JavaScript promises explained: the callback problem they solve, pending, fulfilled and rejected states, then, catch and finally, and promise chaining."
enableToc: true
---

Order a pizza online and you don't get the pizza. You get an **order confirmation**: a promise that a pizza will arrive, or a message saying it can't. JavaScript has the same idea built in. Here's a promise that "delivers" after 100 milliseconds, logged right away and again after 200:

```js
const order = new Promise((resolve) => setTimeout(() => resolve("pizza"), 100));
console.log("right away:", order);
setTimeout(() => console.log("after 200 ms:", order), 200);
```

```text
right away: Promise { <pending> }
after 200 ms: Promise { 'pizza' }
```

Same object, two different states. First it's **pending**, then it holds its value. A **promise** is a placeholder for a value that isn't here yet. This post covers why that's useful, the three states, how to handle success and failure, and how chaining makes async code readable. Every output is real, from Node.js 24.22.

## What problem promises solve

Some work finishes **later**: a timer, a network request, reading a file. JavaScript doesn't wait. It carries on and needs a way to run your code when the result arrives.

The older way was a **callback**: pass in a function to be called with the result. That's fine for one step. Here are three steps that depend on each other (get a user, then their orders, then the first order's details), each simulated with a short delay:

```js
getUser(1, (err, user) => {
  if (err) return console.error(err);
  getOrders(user, (err, orders) => {
    if (err) return console.error(err);
    getDetails(orders[0], (err, details) => {
      if (err) return console.error(err);
      console.log(`${user.name}'s first order:`, details);
    });
  });
});
```

```text
Asha's first order: { orderId: 'order-101', total: 499 }
```

It works, but look at the shape. Every step nests one level deeper, and every level repeats its own error check. Add two more steps and the code drifts off the right of the screen. People call this the "pyramid of doom". Promises let you write the same steps top to bottom instead.

## Promise states: pending, fulfilled, rejected

A promise is always in one of three states:

- **Pending**: still waiting. No result yet.
- **Fulfilled**: finished successfully, with a value.
- **Rejected**: failed, with a reason (usually an `Error`).

Once a promise is fulfilled or rejected, it's **settled**, and that's final. You saw pending and fulfilled above. A rejected one logs like this (stack trace trimmed):

```text
rejected: Promise {
  <rejected> Error: out of stock
      at ...
}
```

The "final" part is literal. A promise settles **once**, and later attempts are ignored:

```js
const once = new Promise((resolve, reject) => {
  resolve("first");
  resolve("second");             // ignored
  reject(new Error("too late")); // ignored
});
once.then((v) => console.log("settled once with:", v));
```

```text
settled once with: first
```

That's a guarantee callbacks never gave you. A buggy callback-based function could call your callback twice; a promise can't fulfil twice.

## The basic promise lifecycle

You create a promise with `new Promise`, passing a function that receives two tools: `resolve` (call it with the value on success) and `reject` (call it with an error on failure):

```js
const wait = (ms, value) =>
  new Promise((resolve) => setTimeout(() => resolve(value), ms));
```

In practice, you'll more often **receive** promises than create them. `fetch()` returns one, and so do most modern libraries. Either way, the lifecycle is the same: the promise starts pending, settles once, and then the handlers you attached run.

Those handlers always run **later**, even if the promise is already settled:

```js
console.log("1. before .then");
Promise.resolve("done").then((v) => console.log("3. inside .then:", v));
console.log("2. after .then");
```

```text
1. before .then
2. after .then
3. inside .then: done
```

`Promise.resolve("done")` is fulfilled immediately, yet line 3 still printed last. Promise handlers wait until the code currently running has finished. That keeps their timing predictable: a `.then` callback never interrupts the code around it.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    C["new Promise(...)"] --&gt; P["Pending"]
    P --&gt;|"resolve(value)"| F["Fulfilled<br/>has a value"]
    P --&gt;|"reject(error)"| R["Rejected<br/>has a reason"]
    F --&gt; T[".then(onSuccess) runs"]
    R --&gt; X[".catch(onError) runs"]
    T --&gt; Fi[".finally() runs either way"]
    X --&gt; Fi
-->
![Promise lifecycle: new Promise starts as Pending; resolve(value) moves it to Fulfilled with a value and reject(error) moves it to Rejected with a reason; Fulfilled runs .then(onSuccess), Rejected runs .catch(onError), and .finally() runs either way](https://mermaid.ink/img/pako:eNpt0k1P4zAQBuC_Ys0pldKQpE3zIcQF6AmkqnBAxBy8ybQxcmw0sSml9L-jGBDd1R5tP_POWJoDNKZFqGCjzK7pBFl2s-bENWOMXdYcNO7YikwvBwyiKJpweGLT6QVb1RxWqFuptxyefipW49sHB8LBqFcMXoVyOOHwwZY1h6VTG6kUtud_6OyiEwMTzIv_JjxjYwMkMuQD1jWHtb_8q55QDEafBCz9ePc1h8h2qAOj71zT4DBMGDk9nMi1lw-jbIRtusDoa9_uX3jv4VKOciO1UGoffCGG0nZIbCf2J_7h20MIW5ItVJYchtAj9WI8wmF0HGyHPXKo2Pjd1r1NG6MMceD6CCG8CP1oTP9TTcZtO6g2Qg0YgntphcUrKbYkfgnqFunSOG2hSuLMZ0B1gDeo5kkRpUW5KJM4KfNZPAthD1WSptE8zdJZUeRxkZdlfgzh3XeNo3SRZIsiyYpiMS_zLARspTV0-7Uwfm-On9ctsf4?type=png)
*A promise settles once, as fulfilled or rejected. `.finally()` runs whichever way it goes.*

## Handling success and failure

Three methods cover it:

- `.then(fn)` runs when the promise is **fulfilled**, with the value.
- `.catch(fn)` runs when it's **rejected**, with the error.
- `.finally(fn)` runs **either way**, for cleanup like hiding a loading spinner.

```js
getUser(1)
  .then((user) => console.log("got", user.name))
  .catch((err) => console.error("Something failed:", err.message))
  .finally(() => console.log("done loading"));
```

**Always handle the failure.** A rejected promise that nobody catches is an *unhandled rejection*, and in Node.js it stops the whole program:

```js
Promise.reject(new Error("payment failed"));
setTimeout(() => console.log("this line never prints"), 100);
```

```text
Promise.reject(new Error("payment failed"));
               ^

Error: payment failed
    at ...
```

The process exited with code 1, and the timer's message never printed. Browsers don't stop the page, but they log an "Uncaught (in promise)" error in the console. Either way, the failure goes unhandled.

## Promise chaining

Here's what makes promises readable: **every `.then` returns a new promise**. Whatever you return from a `.then` becomes the value for the next one:

```js
Promise.resolve(2)
  .then((n) => n * 10)
  .then((n) => n + 1)
  .then((n) => console.log("2 * 10 + 1 =", n));
```

```text
2 * 10 + 1 = 21
```

And if you return a **promise**, the next `.then` waits for it to settle. That's how dependent async steps line up. Here's the callback pyramid from earlier, rewritten with functions that return promises:

```js
let user;
getUser(1)
  .then((u) => { user = u; return getOrders(u); })
  .then((orders) => getDetails(orders[0]))
  .then((details) => console.log(`${user.name}'s first order:`, details))
  .catch((err) => console.error("Something failed:", err.message))
  .finally(() => console.log("done loading"));
```

```text
Asha's first order: { orderId: 'order-101', total: 499 }
done loading
```

Same result, but the code reads top to bottom, one step per line, and there's **one** `.catch` for the whole chain. If any step fails, the chain skips straight to it. Asking for an order that doesn't exist (`orders[5]`) made `getDetails` reject:

```text
Something failed: no order id
```

The `.then` after it never ran.

### The forgotten return

A classic chaining bug is a `.then` that starts async work but doesn't **return** it:

```js
getUser(1)
  .then((u) => { getOrders(u); })   // ← no return
  .then((orders) => console.log("orders:", orders));
```

```text
orders: undefined
```

With curly braces, a function returns nothing unless you write `return`, so the next step gets `undefined` and doesn't wait for `getOrders`. Either write `return getOrders(u);` or drop the braces: `(u) => getOrders(u)`.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart TB
    subgraph CB["Callbacks: nested"]
        A1["getUser(cb)"] --&gt; A2["  getOrders(cb)"]
        A2 --&gt; A3["    getDetails(cb)"]
        A3 --&gt; A4["      use result"]
        E1["error check at every level"]
    end
    subgraph PR["Promises: flat chain"]
        B1["getUser()"] --&gt; B2[".then(getOrders)"]
        B2 --&gt; B3[".then(getDetails)"]
        B3 --&gt; B4[".then(use result)"]
        B4 --&gt; B5[".catch(one handler)"]
    end
-->
![Callbacks vs promises: with callbacks, getUser, getOrders and getDetails nest one level deeper each time with an error check at every level; with promises, getUser, .then(getOrders), .then(getDetails) and .then(use result) form a flat chain ending in one .catch handler](https://mermaid.ink/img/pako:eNpt0s9vmzAUwPF_5emdUolE_EyAw6SS7jitmrbL4h4c8wKoxo4epmsX5X-fgDRNk_lm87HNV_IBlS0Jc9xp-0fVkh38LAQLAwDQ9duK5b6GdbERuJZab6V67nIw1DkqBT69y2HcBxuBFblfHfFMbe8EPsF8_gXuw41AgIrcdy6Ju9O3T1vDSUajHO0DOdno_-JowvEJA_QdAVPXa3dFvw6_RMyWQdWknkE6oBfiN9D0QvpCkylvqh9_bAQ-sm2bjrocdlo6ULVszNUtxWX4ObsYsheuJjM7p1-nFFN3EV3SU_mNnbKL-Gw_sm9sPNlksEo6Vc-sIailKTXx3edu9LDipsTccU8etsStHKZ4GIhAV1NLAnMQyFT2r3NltWWBwhzRw700v61t33ez7asa853UHXnY70vp6KGRFcv2vMpkSuK17Y3DPPCz8RDMD_iKeRykizDNllngB9kq8iMP3zAPwnARh0kYpenKT1dZtjp6-He81l-EyyBZpkGSpss4WyUeUtk4y9-mdz0-7-M_2A7b6A?type=png)
*Same three steps. Callbacks nest and repeat the error check; promises stay flat with one `.catch`.*

## Callbacks vs promises, side by side

| | Callbacks | Promises |
|---|---|---|
| Shape with several steps | Nested, drifts right | Flat chain, top to bottom |
| Error handling | Checked at every level | One `.catch` for the chain |
| Called how many times | Up to the function you called | Settles exactly once |
| Result | Only available inside the callback | An object you can store, pass and chain |
| Running tasks together | Manual bookkeeping | Built-in helpers like `Promise.all` |

Callbacks aren't wrong: event listeners like `button.addEventListener("click", fn)` still use them, because a click can happen many times. Promises are for things that happen **once**: one response, one file, one result.

The takeaway: **a promise is a placeholder for a future value. It starts pending, settles once as fulfilled or rejected, and `.then`/`.catch` run when it does. Return from each `.then` and a chain of async steps reads like a list.** This post stopped before `async`/`await`, which is the same promises written to look like ordinary top-to-bottom code. It's the natural next step, and everything here still applies underneath.

Find a place in your code with a callback inside a callback. What would it look like as a chain, and where would the single `.catch` go?
