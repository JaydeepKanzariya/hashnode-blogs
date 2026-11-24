---
title: "One Thing at a Time: Synchronous vs Asynchronous JavaScript"
slug: synchronous-vs-asynchronous-javascript
subtitle: What synchronous and asynchronous code mean, why blocking code freezes everything, and how JavaScript waits for timers and API calls without stopping
tags: javascript, web-development, beginners, programming, frontend
cover: ./cover.png
seoTitle: "Synchronous vs Asynchronous JavaScript, Explained"
seoDescription: "Synchronous vs asynchronous JavaScript explained: step-by-step code, why blocking code freezes the page, timers and API calls, and the task queue."
enableToc: true
---

Guess the order these three lines print in:

```js
console.log("1. order placed");
setTimeout(() => console.log("2. timer callback (0 ms)"), 0);
console.log("3. order confirmed");
```

```text
1. order placed
3. order confirmed
2. timer callback (0 ms)
```

The timer was set to **zero** milliseconds, and it still printed last. That one result is the difference between synchronous and asynchronous JavaScript in a nutshell. This post explains it with small examples, a real measurement of what blocking code does, and the queue that makes waiting work. Every output is real, from Node.js 24.22 and Chrome 157.

## What synchronous code means

**Synchronous** code runs one line at a time, in order. Each line finishes completely before the next one starts:

```js
console.log("Step 1: boil water");
console.log("Step 2: add tea leaves");
console.log("Step 3: pour into cup");
```

```text
Step 1: boil water
Step 2: add tea leaves
Step 3: pour into cup
```

That's how most of your code runs, and it's what makes code easy to follow: read it top to bottom, and that's the order it happens in.

The everyday version is a queue at a ticket counter with one clerk. Each customer is served completely before the next one steps up. Fine when every customer is quick.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    S1["Step 1<br/>runs to completion"] --&gt; S2["Step 2<br/>waits, then runs"]
    S2 --&gt; S3["Step 3<br/>waits, then runs"]
    S3 --&gt; D["Done"]
-->
![Synchronous execution timeline: Step 1 runs to completion, then Step 2 waits and runs, then Step 3 waits and runs, then done](https://mermaid.ink/img/pako:eNqF0T9vwjAQBfCvYr3Z0Nj551gVSxnbpWzFDG5ykEiJHRlH0CK-e0UQrB3vdL93w7ug9g1BY9_7U93aENn7pwnGMcbYRmwNNpFGJl6_w8sqTO7Iome1H8aeYuedwY4tFiu2kY9LOV-ebBePnMWWHLspg90zVN5F-hDpvyKdxXprsPaODHbgOISugY5hIo6BwmBvIy43YRBbGshAM4NAzXRe1L73wcC4KzhG6768Hx46-OnQQu9tfySOaWxspHVnD8EOz20g11B485OL0CKbM6AvOENnQi2lqopKJKIq0yTl-IEWUi4zmctUqTJRZVWVV47f-WuylIXICyVypYqsKnMOarrow8e9ibmQ6x8sZn0x?type=png)
*Each step waits for the one before it. One slow step delays everything behind it.*

## The problem with blocking code

JavaScript has **one main thread**: one clerk. It can only do one thing at a time. So what happens when one customer takes forever?

Here's a timer set for 100 ms, followed by a loop that keeps the thread busy for about 2 seconds:

```js
const start = Date.now();
setTimeout(() => {
  console.log(`timer asked for 100 ms, actually ran after ${Date.now() - start} ms`);
}, 100);

// Busy loop: keeps the only thread occupied for about 2 seconds
while (Date.now() - start < 2000) {}
console.log(`busy loop finished at ${Date.now() - start} ms`);
```

```text
busy loop finished at 2000 ms
timer asked for 100 ms, actually ran after 2004 ms
```

The timer was due at 100 ms. It ran at **2,004 ms**, about twenty times late, because the thread was stuck in the loop and couldn't get to it. (Three runs gave 2,002 to 2,004 ms.) A timer's delay is a **minimum**, not a guarantee.

That loop is **blocking code**: code that holds the thread so nothing else can run. In Node, it means a server can't answer any other request meanwhile. In a browser, it means the page **freezes**. I measured that in Chrome 157 by recording when the page drew each frame, with a 1-second busy loop in the middle:

```text
gaps between frames (ms): 16, 17, 16, 17, 1000, 17, 17, 17 ...
```

Normally the page redraws about every 16–17 ms. During the loop, there was a **1,000 ms** gap with no redraw at all. For that whole second, clicks, typing and scrolling get no response.

Real code rarely contains a deliberate busy loop. But anything slow done synchronously, like waiting for a server, reading a big file, or a heavy calculation, has the same effect.

## What asynchronous code means

**Asynchronous** code starts a task, **doesn't wait** for it, and carries on. When the task finishes, a function you provided runs with the result.

The everyday version is ordering at a busy restaurant that gives you a buzzer. You don't stand at the counter blocking the line. You sit down, chat, check your phone. When the food's ready, the buzzer goes off and you collect it.

That explains the opening example. `setTimeout(callback, 0)` doesn't mean "run now". It means "run this **once the current code has finished** and at least 0 ms have passed". The two `console.log` lines are the current code, so they run first. Then the timer's callback gets its turn.

## Why JavaScript needs asynchronous behaviour

Plenty of work in a web app involves **waiting for something outside your code**:

- data from a server (API calls),
- a timer or a delay,
- a file to be read,
- the user to click something.

If JavaScript waited synchronously for each of these, the page would freeze every time it fetched data. Instead, it hands the waiting off and keeps going. Here's a real API call:

```js
console.log("1. requesting data...");
fetch("https://jsonplaceholder.typicode.com/todos/1")
  .then((res) => res.json())
  .then((todo) => console.log("3. data arrived:", todo.title));
console.log("2. this line runs while we wait");
```

```text
1. requesting data...
2. this line runs while we wait
3. data arrived: delectus aut autem
```

Line 2 didn't wait for the network. The data arrived later, and its handler ran then. (The `.then` parts are promises, a way of handling results that arrive later.)

Node shows both styles side by side with files. `readFileSync` is synchronous; `readFile` is asynchronous:

```js
const fs = require("node:fs");
console.log("A. before readFileSync");
console.log("B. sync contents:", fs.readFileSync("note.txt", "utf8").trim());
console.log("C. after readFileSync");
fs.readFile("note.txt", "utf8", (err, text) => console.log("F. async contents:", text.trim()));
console.log("D. after readFile was called");
console.log("E. still running other code");
```

```text
A. before readFileSync
B. sync contents: hello from a file
C. after readFileSync
D. after readFile was called
E. still running other code
F. async contents: hello from a file
```

The synchronous read finished before line C could run. The asynchronous one let D and E run first, and delivered the contents at the end.

## How the waiting works: the task queue

If there's only one thread, who's doing the waiting? Not your JavaScript. The **environment** is: the browser, or Node. Here's the mental model:

1. Your code runs on the main thread, top to bottom.
2. When it starts something slow (a timer, a `fetch`, a file read), the environment takes over the waiting, and your code carries on.
3. When the task finishes, its callback is placed in a **queue**.
4. Whenever the main thread has **nothing left to run**, it takes the next callback from the queue and runs it.

That's why the zero-millisecond timer ran last: its callback sat in the queue until the main code finished. And it's why the 100 ms timer ran at 2,004 ms: it was in the queue on time, but the thread didn't free up until the loop ended. (The full mechanism is called the **event loop**, and it has more detail than this. For writing everyday code, this model is enough.)

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    M["Main thread<br/>runs your code"] --&gt;|starts timer / fetch / file read| E["Browser or Node<br/>does the waiting"]
    E --&gt;|task done| Q["Task queue<br/>callbacks wait in line"]
    Q --&gt;|when the main thread is free| M
-->
![Asynchronous task queue: the main thread runs your code and starts a timer, fetch or file read; the browser or Node does the waiting; when the task is done its callback waits in the task queue; when the main thread is free it takes the callback from the queue](https://mermaid.ink/img/pako:eNpNkctOwzAQRX9lNOv0kfQRJ0JdAN1RJBArahZuPG2sJjaMbZXS9t9RggqsRjPSOVeje8LKacISt407VLXiAA_PkqUFAFitJa6UsRBqJqVvNjxacLQeji4ydKDENxgMFmcfFAcPwbTEMIItharupmkIOvQMy7XEW3YHTwyO4dFp6n3akYdQExyUCcbuJL5d45e9Oii_B-0sneFpLfGlWz8ixR-8Uk2zUdXe9zwYC42x9E_y1EsONdk-pf17B4yHLROdYYUJ7thoLANHSrAlblW34qmTSAw1tSSxBIlMOn4OKtc4lijtBRN8V_bVufZKs4u7GsutajwlGN-1CnRv1I5V-3tlspr4zkUbsExF78DyhJ9YTlMxzEQxL9JxWuST8STBI5Zplg2n2SybCJGPRV4U-SXBrz51PMzm6Wwu0pkQ82mRzxIkbYLj1U-zfcGXb9pZnNg?type=png)
*The waiting happens outside your code. Finished callbacks queue up and run when the main thread is free.*

## Blocking vs non-blocking, side by side

| | Blocking (synchronous) | Non-blocking (asynchronous) |
|---|---|---|
| The next line | Waits until this finishes | Runs straight away |
| The page or server | Frozen meanwhile | Stays responsive |
| The result | Available on the next line | Delivered later, to a callback or promise |
| Examples | A loop, `readFileSync`, a heavy calculation | `setTimeout`, `fetch`, `readFile`, event listeners |

**When synchronous is fine:** most of your code. Adding numbers, building a string or looping over a small array finishes too quickly for anyone to notice, and synchronous code is simpler to read. It only becomes a problem when something takes long enough to be noticed, or when it waits on something outside your code. A small script that runs once and exits, where nothing else needs to happen meanwhile, can use `readFileSync` happily.

The takeaway: **JavaScript runs one thing at a time. Synchronous code waits for each step; asynchronous code hands slow work to the browser or Node and picks up the result from a queue when the thread is free. Blocking that one thread delays everything, even a zero-millisecond timer.** This post kept the event loop at the level of a mental model. The next step is handling async results cleanly: [promises](https://jaydeepkanzariya.hashnode.dev/javascript-promises-explained) and then [`async`/`await`](https://jaydeepkanzariya.hashnode.dev/from-then-chains-to-async-await-same-promises-cleaner-code).

Paste the busy-loop example into your browser's console with a button on the page, and try clicking it during the loop. What happens to the click?
