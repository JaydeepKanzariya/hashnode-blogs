---
title: "map Returns a New Array, push Changes the Old One: Array Methods for Beginners"
slug: javascript-array-methods
subtitle: push, pop, shift, unshift, forEach, map, filter and reduce explained with before-and-after arrays and real output
tags: javascript, web-development, beginners, arrays, tutorial
cover: ./cover.png
seoTitle: "JavaScript Array Methods: push, map, filter, reduce"
seoDescription: "JavaScript array methods (push, pop, shift, unshift, forEach, map, filter, reduce) with before/after arrays, for-loop comparisons, and real output."
enableToc: true
---

Run two array methods on the same list and they behave in opposite ways:

```js
const prices = [10, 20, 30];
const doubled = prices.map(p => p * 2);
console.log("after map:", prices, "returned:", doubled);

const newLength = prices.push(40);
console.log("after push:", prices, "returned:", newLength);
```

```text
after map: [ 10, 20, 30 ] returned: [ 20, 40, 60 ]
after push: [ 10, 20, 30, 40 ] returned: 4
```

`map` left `prices` untouched and handed back a new array. `push` mutated `prices` in place and handed back the number `4`, not the array. That split — **mutating vs returning a new array** — is the main thing to track across every array method in JavaScript.

All outputs below come from real runs on Node.js 24.22.1. If you haven't covered indexing and array basics yet, start with [JavaScript arrays 101](https://jaydeepkanzariya.hashnode.dev/javascript-arrays-101).

## One question for every method

Before using any array method, ask two things: does it change the original array, and what does it return?

| Method | Changes original? | Returns |
|---|---|---|
| `push()` | Yes (adds to end) | New length |
| `pop()` | Yes (removes from end) | Removed item |
| `unshift()` | Yes (adds to front) | New length |
| `shift()` | Yes (removes from front) | Removed item |
| `forEach()` | No (unless your callback mutates it) | `undefined` |
| `map()` | No | New array (same length) |
| `filter()` | No | New array (matching items only) |
| `reduce()` | No | One accumulated value |

Keep that table in mind as you try the examples in your browser console or Node REPL.

## push() and pop(): work at the end

`push` appends an item to the end of an array and returns the new length. `pop` removes the last item and returns the item it took off:

```js
const cart = ["pen", "book"];
console.log("before:", cart);

const len = cart.push("bag");
console.log("after push:", cart, "returned:", len);

const removed = cart.pop();
console.log("after pop:", cart, "returned:", removed);
```

```text
before: [ 'pen', 'book' ]
after push: [ 'pen', 'book', 'bag' ] returned: 3
after pop: [ 'pen', 'book' ] returned: bag
```

Both change `cart` in place. A common mistake is writing `const updated = cart.push("bag")` expecting `updated` to be the array. It will be `3`.

> **Try it in the console** — call `pop()` on an empty array `[]` and check what it returns.

## shift() and unshift(): work at the front

`unshift` adds an item to index `0` and returns the new length. `shift` removes index `0` and returns the removed item:

```js
const queue = ["Asha", "Ravi"];
console.log("before:", queue);

const len = queue.unshift("Meera");
console.log("after unshift:", queue, "returned:", len);

const first = queue.shift();
console.log("after shift:", queue, "returned:", first);
```

```text
before: [ 'Asha', 'Ravi' ]
after unshift: [ 'Meera', 'Asha', 'Ravi' ] returned: 3
after shift: [ 'Asha', 'Ravi' ] returned: Meera
```

Notice the hidden cost. Adding or removing at the end touches one slot. Adding or removing at index `0` shifts every remaining item along by one. For a small list of five names you won't notice. I timed emptying a 50,000-item array in a loop on this machine (Node.js 24.22.1, two runs): `shift` took about 1.5 to 2.4 seconds and `pop` took under a millisecond. Treat that as one machine's result, not a benchmark, but the gap is large.

> **Try it in the console** — pass two arguments to `queue.unshift("Kiran", "Dev")` and check their order in the resulting array.

## forEach(): run a callback, return nothing

`forEach` runs a function once for every item. It is for side effects such as logging, updating the DOM, or saving records. It does not build a new array:

```js
// ❌ expecting forEach to return a new array
const nums = [1, 2, 3];
const doubled = nums.forEach(n => n * 2);
console.log(doubled);
```

```text
undefined
```

Because `forEach` always returns `undefined`, assigning its result to a variable is a bug. Use it when you want an action per item, not a transformed list:

```js
// ✅ side effect only
const nums = [1, 2, 3];
const result = nums.forEach(n => {
  console.log("item:", n);
});
console.log("returned:", result);
console.log("original:", nums);
```

```text
item: 1
item: 2
item: 3
returned: undefined
original: [ 1, 2, 3 ]
```

> **Try it in the console** — add a second parameter `(n, index)` to the `forEach` callback and print both.

## map(): transform every item into a new array

`map` runs your callback on every item and collects the return values into a new array of the same length. Compare a traditional `for` loop against `map` when taking 50 off every price:

```js
const prices = [100, 250, 400];

// for loop
const discountedLoop = [];
for (let i = 0; i < prices.length; i++) {
  discountedLoop.push(prices[i] - 50);
}

// map
const discountedMap = prices.map(p => p - 50);

console.log("before:", prices);
console.log("loop:", discountedLoop);
console.log("map:", discountedMap);
```

```text
before: [ 100, 250, 400 ]
loop: [ 50, 200, 350 ]
map: [ 50, 200, 350 ]
```

Both produce the exact same array, and `prices` stays `[ 100, 250, 400 ]`. The `for` loop spends four lines on plumbing (an empty array, an index counter, a `push`). `map` states the transformation in one line.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    In["[100, 250, 400]"] --&gt; Fn["p => p - 50<br/>runs on each item"]
    Fn --&gt; Out["[50, 200, 350]<br/>new array"]
-->
![How map works: the input array of 100, 250 and 400 passes each item through p => p - 50 to produce a new array of 50, 200 and 350 with the same length, while the original is unchanged](https://mermaid.ink/img/pako:eNolzMEKgkAURuFX-blrpclyI-VSCIKgrXcWk14xcEaZRiTEd4-x9eF8KzVjK1RQN4xL0xsfcH-yA4Cbq5nqo1IJslwlOCulmTTStEQV24RriQkpcnV5-UPpZ_fB6CCm6fEOYpn0n6rcfj3mEMmIZZE95Urvp5MFxnvzZdKUkBVvzbulglam0IsVpoKplc7MQ2DaaPsBzZo1pA==?type=png)

> **Try it in the console** — use `map` on `["asha", "ravi"]` to return uppercase names.

## filter(): keep only the items that pass a test

`filter` runs a callback that returns `true` or `false`. Items where it returns `true` go into the new array; the rest are dropped. Compare a `for` loop against `filter` for keeping passing scores (40 or above):

```js
const scores = [35, 72, 40, 91, 28];

// for loop
const passedLoop = [];
for (let i = 0; i < scores.length; i++) {
  if (scores[i] >= 40) {
    passedLoop.push(scores[i]);
  }
}

// filter
const passedFilter = scores.filter(s => s >= 40);

console.log("before:", scores);
console.log("loop:", passedLoop);
console.log("filter:", passedFilter);
```

```text
before: [ 35, 72, 40, 91, 28 ]
loop: [ 72, 40, 91 ]
filter: [ 72, 40, 91 ]
```

The original `scores` array is untouched, and the new array is shorter. Unlike `map`, `filter` never modifies the values — it only decides which ones survive.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    In["[35, 72, 40, 91, 28]"] --&gt; Test{"s >= 40?"}
    Test -- "true" --&gt; Keep["[72, 40, 91]<br/>new array"]
    Test -- "false" --&gt; Drop["35, 28<br/>dropped"]
-->
![How filter works: the input array 35, 72, 40, 91, 28 is tested item by item with s >= 40; 72, 40 and 91 pass into the new array, while 35 and 28 are dropped](https://mermaid.ink/img/pako:eNpdzr0KwkAQBOBXWaa-YIwRNWhsbEQrsXOvOL0NEfLH5UQk5N0lERFsh_mG6XCrrSBBVtTPW26cp-OJKyKifXVhXGZzRYtIURwqWk0VRUvN0BQEKZ2l9R2jpXRDcbhl9B845BQExPDuIYyxfBBphr3fll5f3SSt5EnGOfNi6H-emaL9-p2rBz_ciZajtK5uGrEMDYVSXGnuFgk6hs-lFEbCsJKZR-EZPfo3JedDww==?type=png)

> **Try it in the console** — filter `scores` for numbers below 40, then check `scores.length` to confirm the original didn't shrink.

## reduce(): fold an array into a single value

`reduce` walks through the array while carrying a running value called the **accumulator**. On each step, your callback receives the current accumulator and the next item, and whatever you return becomes the accumulator for the next step.

The second argument to `reduce` is the starting value (here, `0`):

```js
const expenses = [120, 45, 80, 55];
const total = expenses.reduce((sum, amount) => {
  console.log(`sum=${sum}, amount=${amount} -> ${sum + amount}`);
  return sum + amount;
}, 0);
console.log("total:", total);
console.log("original:", expenses);
```

```text
sum=0, amount=120 -> 120
sum=120, amount=45 -> 165
sum=165, amount=80 -> 245
sum=245, amount=55 -> 300
total: 300
original: [ 120, 45, 80, 55 ]
```

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    S0["start: 0"] --&gt;|"+ 120"| S1["120"]
    S1 --&gt;|"+ 45"| S2["165"]
    S2 --&gt;|"+ 80"| S3["245"]
    S3 --&gt;|"+ 55"| S4["300"]
-->
![How reduce accumulates the array 120, 45, 80, 55 starting from 0: 0 + 120 = 120, 120 + 45 = 165, 165 + 80 = 245, 245 + 55 = 300](https://mermaid.ink/img/pako:eNpNzbEOgjAYBOBX-XOrkpS2GNPBJ3CSsT9DQ0swAUlqjQPw7gYw6HbDd3cj6sEHGDTd8K5bFxNdb_wgIiqFZTyTi8mQYFSUZZeJcaBcCsZEZW4Za66-hXwnuliFXMSp-Am5i_O2oSxD6j-hdlFsG9oylFhecEQfYu_uHgYjI7WhDwzD8KFxry4xZswfRzQ44A==?type=png)

Always pass the initial value (`0` for a sum). Without it, calling `reduce` on an empty array throws:

```js
try {
  [].reduce((sum, n) => sum + n);
} catch (e) {
  console.log(e.name + ": " + e.message);
}
console.log([].reduce((sum, n) => sum + n, 0));
```

```text
TypeError: Reduce of empty array with no initial value
0
```

> **Try it in the console** — change the initial value from `0` to `100` in the `expenses` example and trace the first step.

## When not to use each method

Every method here has a misuse that trips people up:

- **Don't use `map` when you ignore its return value.** If you aren't storing or returning the new array, you built an array for nothing. Use `forEach` or a `for...of` loop.
- **Don't use `forEach` when you need to stop early.** `break` is a syntax error inside a callback, and `return` only skips the current item. Use a plain `for` or `for...of` loop if you need to exit mid-way.
- **Don't use `reduce` when `map` or `filter` says it better.** You can rebuild `map` and `filter` with `reduce`, and it almost always reads worse. Keep `reduce` for folding into one result (a sum, a count, a grouped object).
- **Don't use `shift` in a tight loop on large arrays.** Re-indexing on every iteration adds up.

## The assignment, solved step by step

Start with an array of numbers, double each one with `map`, keep those greater than 10 with `filter`, and sum the survivors with `reduce`. Each step sits in its own variable so you can inspect the intermediate arrays before learning to chain them:

```js
const numbers = [3, 6, 8, 2, 12];

const doubled = numbers.map(n => n * 2);
console.log("doubled:", doubled);

const aboveTen = doubled.filter(n => n > 10);
console.log("above 10:", aboveTen);

const total = aboveTen.reduce((sum, n) => sum + n, 0);
console.log("sum:", total);
console.log("original:", numbers);
```

```text
doubled: [ 6, 12, 16, 4, 24 ]
above 10: [ 12, 16, 24 ]
sum: 52
original: [ 3, 6, 8, 2, 12 ]
```

Step by step: `[3, 6, 8, 2, 12]` doubles to `[6, 12, 16, 4, 24]`. Filtering for `n > 10` drops `6` and `4`, leaving `[12, 16, 24]`. Summing from `0` gives `52`, and `numbers` is still intact at the end.

## Where this leaves you

Track two things for every array method: whether it mutates the original array (`push`, `pop`, `shift`, `unshift` do; `map`, `filter`, `reduce` don't) and what it returns. That single habit prevents most beginner array bugs.

One limit: this post leaves out method chaining (`numbers.map(...).filter(...).reduce(...)`) and search methods like `find`, `some` and `every`, and I haven't benchmarked `for` loops against `map` or `filter`. Which of these methods tripped you up first — `forEach` returning `undefined`, or `push` returning the new length?
