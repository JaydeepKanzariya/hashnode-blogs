---
title: "Three Files, Three if (err) Checks: Callbacks vs Promises"
slug: nodejs-async-callbacks-promises
subtitle: "Why async code exists in Node.js, error-first callbacks, nested callback problems, fs/promises, and when callbacks still fit"
tags: nodejs, javascript, web-development, beginners, tutorial
cover: ./cover.png
seoTitle: "Async Code in Node.js: Callbacks vs Promises Explained"
seoDescription: "Async code in Node.js: why it exists, error-first callbacks, nested callback problems, fs/promises chains, and Promise.all, with real Node 24 output."
enableToc: true
---

Reading one file in Node.js with a callback takes five lines. Reading three files where each file names the next turns into a staircase of indentation and three separate `if (err)` checks.

That staircase is the exact reason Node.js evolved from **callbacks** to **Promises**. Every output below comes from a real run on **Node.js 24.22.1**. To run the snippets locally, create three files in the same folder: `user.txt` containing `order-101.txt`, `order-101.txt` containing `receipt-101.txt`, and `receipt-101.txt` containing `Paid: 450`.

## Why async code exists in Node.js

Your JavaScript in Node.js runs on **one main thread**. Disk reads, database queries, and HTTP calls are slow compared to CPU instructions. If Node.js paused that single thread every time it read a file, a web server handling dozens of users would freeze for everyone while waiting on one disk read.

**Asynchronous code** lets Node.js start a slow I/O task, keep executing the rest of your script, and run a follow-up handler once the OS finishes the task.

## Callback-based async execution, step by step

A **callback** is a function you pass as an argument to another function so it can be called later when the work finishes. Node.js uses an **error-first callback convention** — the first parameter is always `err` (or `null` if everything succeeded), and the second is the result. Putting `err` first is deliberate: wrapping `fs.readFile(...)` in a synchronous `try/catch` block will **not** catch an error that happens later inside the callback, so Node passes errors through the first argument instead:

```js
const fs = require("fs");

console.log("1. Requesting user.txt");
fs.readFile("user.txt", "utf8", (err, data) => {
  if (err) return console.error("Read failed:", err.code);
  console.log("3. Got file:", data.trim());
});
console.log("2. Main thread keeps running");
```

```text
1. Requesting user.txt
2. Main thread keeps running
3. Got file: order-101.txt
```

Step by step:
1. Line 1 prints `"1. Requesting user.txt"`.
2. `fs.readFile` hands the disk read to libuv's background worker pool and returns immediately.
3. Line 2 prints `"2. Main thread keeps running"` before the disk read has finished.
4. When the read completes, Node.js queues your callback on the event loop, and it prints `"3. Got file: order-101.txt"`.

For a single independent operation, callbacks are short and clear. The pain begins when one async step depends on the previous step's result.

## Problems with nested callbacks

Suppose `user.txt` holds the name of an order file (`order-101.txt`), which holds the name of a receipt file (`receipt-101.txt`). With callbacks, each read must sit *inside* the previous callback:

```js
// ❌ nested callbacks: 3 indentation levels and 3 repeated error checks
const fs = require("fs");

fs.readFile("user.txt", "utf8", (err, orderFile) => {
  if (err) return console.error("Step 1 failed:", err.code);
  fs.readFile(orderFile.trim(), "utf8", (err, receiptFile) => {
    if (err) return console.error("Step 2 failed:", err.code);
    fs.readFile(receiptFile.trim(), "utf8", (err, receipt) => {
      if (err) return console.error("Step 3 failed:", err.code);
      console.log("Receipt:", receipt.trim());
    });
  });
});
```

```text
Receipt: Paid: 450
```

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart TD
    S1["1. readFile('user.txt')"] --&gt;|err| E1["Handle Step 1 err"]
    S1 --&gt;|orderFile| S2["2. readFile(orderFile)"]
    S2 --&gt;|err| E2["Handle Step 2 err"]
    S2 --&gt;|receiptFile| S3["3. readFile(receiptFile)"]
    S3 --&gt;|err| E3["Handle Step 3 err"]
    S3 --&gt;|receipt| Done["Print Receipt"]
-->
![Nested callback execution chain: readFile(user.txt) checks if(err) then calls readFile(order-101.txt), which checks if(err) then calls readFile(receipt-101.txt), which checks if(err) before printing the receipt — creating three separate error exits](https://mermaid.ink/img/pako:eNpdzTtrw0AQBOC_skxjG2KD7joVqZyQMljptCoO3QoL9DCbMzZI-u_BUR4ntTuz8w0oey9IUTX9rTw7DfRx5I6IKEtyRnIgFedf60a2m-un6CHcw2bHKGi_fx5FdaSXR_HNdb4RyoJcKCFRZRS_O9_VXr3oY2ekzOQMEy3_Zbv_LxMBZgWYJTBXVUqpL-GHsDnDRkSURoiNELtC7BKxMTLSse8kZ7xr3QU6zVdGgSe0oq2rPVIMjHCWVhgpw0vlrk1gTJi-AFj2dd4=?type=png)

This pattern — nicknamed **callback hell** or the **pyramid of doom** — creates three real maintenance problems:
- **Horizontal drift:** every dependent step pushes code further right, making the control flow hard to scan.
- **Repeated error handling:** every single layer needs its own `if (err) return ...`. Forget one `return` and the next step runs with `undefined` data.
- **Hard to compose:** running three reads concurrently and waiting for all of them requires manual counters and state variables.

## Promise-based async handling (`fs/promises`)

A **Promise** is an object representing a value that is not ready yet. It moves through three states: **`pending`** (work in progress), **`fulfilled`** (succeeded with a value), or **`rejected`** (failed with an error). If you want a dedicated intro to Promises first, see [JavaScript Promises for beginners](https://jaydeepkanzariya.hashnode.dev/javascript-promises-explained).

Node.js ships a Promise-based version of `fs` under `require("fs/promises")`. Here is the exact same three-file chain rewritten with `.then()` and a single `.catch()`:

```js
// ✅ flat Promise chain with one shared error handler
const fs = require("fs/promises");

fs.readFile("user.txt", "utf8")
  .then((orderFile) => fs.readFile(orderFile.trim(), "utf8"))
  .then((receiptFile) => fs.readFile(receiptFile.trim(), "utf8"))
  .then((receipt) => console.log("Receipt:", receipt.trim()))
  .catch((err) => console.error("Chain failed:", err.code, err.path));
```

```text
Receipt: Paid: 450
```

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    P["Promise<br/>(pending)"] --&gt;|"fulfilled"| T1[".then() step 1"]
    T1 --&gt;|"fulfilled"| T2[".then() step 2"]
    T2 --&gt;|"fulfilled"| Done["Print Receipt"]
    P --&gt;|"rejected"| C[".catch(err)<br/>single error handler"]
    T1 --&gt;|"rejected"| C
    T2 --&gt;|"rejected"| C
-->
![Promise lifecycle flow: a Promise starts in pending state; if fulfilled it passes its value down the flat .then() chain to the final result; if any step rejects it skips remaining .then() steps and jumps straight to the single .catch() handler](https://mermaid.ink/img/pako:eNptzzFvwjAQBeC_cropkUqrZIwqlnbsECE2jsG1X7Arx44uRh2A_14VqlZQ5tP33rsD2-zAHQ8xf1pvtNDbShIRUb8R7jWPYcbzuz4tqwnJhbSrhbe0WCyPwsM-DiFGOOEjrZuN8GPxSFVNc8FEjfD2krVu7or2VrR_or0nXnPCeVZIhVawCFP5Jf2PUHzAlgt4-W6wplhfQbU-PzKHtIsgqGYlb5KL0P9Lr1JuNl3d-IFH6GiC444PwsVjhHAn7DCYfSzCJz59AZZXcjA=?type=png)

Notice what happens when step 2 tries to read a missing file. To see it, change `user.txt` to contain `missing.txt`, then run the same chain:

```text
Chain failed: ENOENT .../missing.txt
```

The rejection skips the remaining `.then()` handlers and lands straight in the single `.catch()` at the bottom. You do not repeat `if (err)` three times.

Two small Promise details save hours of debugging:
- **Always return the inner Promise inside `.then()`.** Notice our arrow functions omit curly braces (`(orderFile) => fs.readFile(...)`), which returns the inner Promise implicitly. If you add `{ ... }` braces and forget `return`, the next `.then()` runs immediately with `undefined` instead of waiting for the file read to finish.
- **Use `.finally()` for cleanup.** Code inside `.finally(() => ...)` runs whether the chain fulfilled or rejected — handy for closing a connection or logging that a job ended.

## Benefits of Promises over callbacks

| Aspect | Callbacks (`fs`) | Promises (`fs/promises`) |
|---|---|---|
| Chaining dependent steps | Nests deeper at every step | Stays flat with `.then()` |
| Error handling | Separate `if (err)` at every level | One `.catch()` for the whole chain |
| Running tasks concurrently | Manual counters & result arrays | Built-in `Promise.all([...])` |
| Modern syntax support | Cannot `await` directly | Works directly with `async`/`await` |

Look how clean concurrent reads become when three files do **not** depend on each other:

```js
const fs = require("fs/promises");

Promise.all([
  fs.readFile("user.txt", "utf8"),
  fs.readFile("order-101.txt", "utf8"),
  fs.readFile("receipt-101.txt", "utf8"),
])
  .then((contents) => console.log(contents.map((c) => c.trim())))
  .catch((err) => console.error("Failed:", err.code));
```

```text
[ 'order-101.txt', 'receipt-101.txt', 'Paid: 450' ]
```

`Promise.all` starts all three reads at once and preserves their order in the returned array (if any one read rejects, `Promise.all` rejects immediately; use `Promise.allSettled` when you want results from every file even if one fails). And if you ever need to call an older callback-only Node API, Node's built-in `util.promisify(fn)` wraps an error-first callback function into a Promise-returning one. Once you are comfortable with `.then()` chains, [from .then() chains to async/await](https://jaydeepkanzariya.hashnode.dev/javascript-async-await) shows how `async`/`await` makes Promise code read like synchronous lines.

## When NOT to replace callbacks with Promises

A Promise settles **exactly once** — it resolves or rejects a single time and is done. That makes Promises the wrong abstraction for **repeating events**:
- **Streams and HTTP chunks:** `req.on("data", (chunk) => ...)` fires once per incoming chunk, not once per request.
- **Event emitters and timers:** `server.on("request", ...)` and `setInterval(...)` run over and over.

Use Promises for one-shot async results (reading a file, querying a database, calling an API), and keep callbacks for event listeners and streams that fire multiple times.

## Where this leaves you

Async code keeps Node's single JavaScript thread moving during slow I/O. Error-first callbacks work for one-off calls and repeating event listeners, while `fs/promises` and `.then()`/`.catch()` keep multi-step file and network chains flat, composable, and easy to handle when errors happen.

One honest limit: this post stopped at `.then()` chains rather than covering `async`/`await` syntax (linked above) or Node's unhandled Promise rejection exit behavior when you forget `.catch()`. Do you still run into callback-only libraries in your Node.js projects, or have you moved almost entirely to Promises and `async`/`await`?
