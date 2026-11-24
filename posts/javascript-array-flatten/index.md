---
title: "flat(1) Isn't Flat: Array Flattening in JavaScript, Step by Step"
slug: javascript-array-flatten
subtitle: Nested arrays, flat(), flatMap, reduce, recursion and a stack, plus how to think through the flatten interview question, with real output
tags: javascript, web-development, beginners, arrays, interview
cover: ./cover.png
seoTitle: "Flatten Arrays in JavaScript: flat, reduce, Recursion"
seoDescription: "Flatten nested arrays in JavaScript with flat(), flatMap, reduce, recursion and a stack, plus the interview version of the question, with real output."
enableToc: true
---

You call `.flat()` on a nested array and some of the nesting is still there:

```js
const nested = [1, [2, [3, [4]]]];
console.log(nested.flat());
```

```text
[ 1, 2, [ 3, [ 4 ] ] ]
```

The method did what it's documented to do: it flattened **one level**. Understanding why, and how to flatten to any depth yourself, is the whole topic, and it's a staple interview question. All outputs below are real runs on Node.js 24.22.1.

## What nested arrays are

A nested array is an array that contains other arrays as items. Each extra layer of brackets is one level of **depth**:

```js
const nested = [1, [2, [3, [4]]]];
```

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart TD
    A["[ 1, [...] ]  depth 0"] --&gt; B["1"]
    A --&gt; C["[ 2, [...] ]  depth 1"]
    C --&gt; D["2"]
    C --&gt; E["[ 3, [...] ]  depth 2"]
    E --&gt; F["3"]
    E --&gt; G["[ 4 ]  depth 3"]
    G --&gt; H["4"]
-->
![Nested array structure as a tree: the outer array at depth 0 holds 1 and an array at depth 1, which holds 2 and an array at depth 2, which holds 3 and an array at depth 3, which holds 4](https://mermaid.ink/img/pako:eNplkT9vwjAQR7-K9ZtNFDv_HA-VWqB06dapuQxWYggSiZGbqLSI717hqhQp4z29dzfcGY1rLTS2B_fZdMaP7G1FngbGGHusCBUTnFVRFNWsZqy1x7FjMaFmi8UDe6oIglDfgkCXIZOz7N5cBnNVEeSMrkOfzPp7cx3M54qQzOgm9Ol_eK9sgvJSEVJCDY6d37fQo58sR299b64jzlebMHa2twTNCN6202nRuIPzBBou4Dia4d25_q_2btp10Ftz-LAc07E1o13tzc6b_ka9HVrrl24aRugsDTugzzhBp0JFUpV5KWJRFkmccHxBCymjVGYyUaqIVVGWxYXjO1yNI5mLLFciUypPyyLjsO1-dP7196Xhs5cfT5qGUw?type=png)
*Every extra pair of brackets is one more level of depth.*

Think of it as a tree. The numbers are leaves, the arrays are branches, and flattening means collecting the leaves into one list, in their original order. If you're new to arrays, start with [JavaScript arrays 101](https://jaydeepkanzariya.hashnode.dev/javascript-arrays-101).

## Why flattening is useful

Nesting usually appears by accident. You `map` over a list and each step returns a list:

```js
const orders = [
  { id: 1, items: ["pen", "book"] },
  { id: 2, items: ["bag"] },
];
console.log(orders.map(o => o.items));
```

```text
[ [ 'pen', 'book' ], [ 'bag' ] ]
```

You wanted one list of items, and you got a list of lists. Flatten it and you can count, search or render the items directly. Data from APIs, grouped results and tree-like structures produce the same shape.

## The concept, step by step

Flattening one level means: for each item, if it's an array, take its contents out and place them in the result. If it isn't, place the item itself.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    A["[1, [2, [3]]]"] --&gt;|"flatten 1 level"| B["[1, 2, [3]]"]
    B --&gt;|"flatten 1 more"| C["[1, 2, 3]"]
-->
![Flatten transformation: one pass removes one layer of brackets, so the nested list 1, 2, 3 with 3 buried two layers deep first keeps 3 inside one layer, and a second pass gives the flat list 1, 2, 3](https://mermaid.ink/img/pako:eNplkMFuwjAQRH_FmrNBsUMSxwekQo_tpcfGOVhkA0hJjLZOSwv8exUK7aHHHc17K80Jm9AQLNoufGx2nqN4enHsBiGEeKgcKiVFpaWo0rquHWoxmy3PDm3nY6RBKNHRO3UOZ7G6tW9lh_ruWf2D-sA0Mes_Jp0ISGx538BGHkmiJ-79dOI0mRzijnpysMKBqRmPs03oAju44QKJgx9eQ-jvNIdxu4NtffdGEuOh8ZEe937Lvv9NmYaGeB3GIcJm5uqAPeEIu1Bmrk2ZlypRZZEmqcQnrNJ6vtCZTo0pElOUZXGR-Lp-TeY6V1luVGZMviiLTIKafQz8_DPxdenLN_Ajbgg?type=png)
*Each pass removes one layer of brackets.*

Each pass removes one layer of brackets. "Fully flat" just means repeating until no item is an array. The next four approaches differ in how they repeat.

## Approach 1: flat(depth)

`flat` takes a depth, which defaults to 1:

```js
const nested = [1, [2, [3, [4]]]];
console.log(nested.flat(2));
console.log(nested.flat(Infinity));
```

```text
[ 1, 2, 3, [ 4 ] ]
[ 1, 2, 3, 4 ]
```

`flat(2)` removes two layers, and `flat(Infinity)` removes all of them. **When you can use it, use it.** It's built in, it's readable, and it does the job.

## Approach 2: flatMap, when you map first

`flatMap` is `map` followed by a one-level `flat`, in one call:

```js
const orders = [
  { id: 1, items: ["pen", "book"] },
  { id: 2, items: ["bag"] },
];
console.log(orders.flatMap(o => o.items));
```

```text
[ 'pen', 'book', 'bag' ]
```

It's the right tool for the "list of lists from map" case above. It only goes **one level deep**, so it won't fully flatten deeper nesting:

```js
console.log([1, [2, [3]]].flatMap(x => x));
```

```text
[ 1, 2, [ 3 ] ]
```

## Approach 3: reduce and concat (one level)

Interviewers often say "flatten without `flat()`". The first version most people reach for uses `reduce`:

```js
const oneLevel = arr => arr.reduce((acc, x) => acc.concat(x), []);
console.log(oneLevel([1, [2, 3], [4, [5]]]));
```

```text
[ 1, 2, 3, 4, [ 5 ] ]
```

`concat` spreads out an array argument by one level, which is why this works, and also why `[5]` survives. A correct answer to the full question has to go deeper.

## Approach 4: recursion, for any depth

The key insight is that a nested array is made of smaller nested arrays. So the function can call itself on every array it finds:

```js
function flatten(arr) {
  const out = [];
  for (const item of arr) {
    if (Array.isArray(item)) {
      out.push(...flatten(item)); // go deeper, then merge the result
    } else {
      out.push(item);             // a leaf: keep it
    }
  }
  return out;
}
console.log(flatten([1, [2, [3, [4]]], 5]));
```

```text
[ 1, 2, 3, 4, 5 ]
```

Trace `[1, [2, [3]]]`: `1` is a leaf, so it's kept. `[2, [3]]` is an array, so `flatten` runs on it: `2` is kept, `[3]` triggers another call that returns `[3]`. Results merge back up as `[2, 3]`, then `[1, 2, 3]`.

The "flatten to a given depth" variant just adds a counter that stops the recursion:

```js
function flattenDepth(arr, depth = 1) {
  const out = [];
  for (const item of arr) {
    if (Array.isArray(item) && depth > 0) {
      out.push(...flattenDepth(item, depth - 1));
    } else {
      out.push(item);
    }
  }
  return out;
}
console.log(flattenDepth([1, [2, [3, [4]]]], 2));
```

```text
[ 1, 2, 3, [ 4 ] ]
```

That matches `flat(2)` on the same input.

## Approach 5: a stack, with no recursion

Recursion has a limit: every call uses call-stack space. I built an array nested 20,000 levels deep and ran `flat(Infinity)` on it. It threw `RangeError`, and so did my recursive version. A loop with your own stack doesn't have that limit:

```js
function flattenIter(arr) {
  const stack = [...arr];
  const out = [];
  while (stack.length) {
    const item = stack.pop();
    if (Array.isArray(item)) {
      for (const x of item) stack.push(x); // unpack it and keep going
    } else {
      out.push(item);
    }
  }
  return out.reverse(); // items came off the end, so restore the order
}
console.log(flattenIter([1, [2, [3, [4]]], 5]));
```

```text
[ 1, 2, 3, 4, 5 ]
```

The same function handled the 20,000-level array and returned `[ 1 ]`. That's a result from one machine and one Node version, so treat the exact limit as a rough one, not a rule. Real data almost never nests this deep. One detail: I unpack with a loop instead of `stack.push(...item)`, because spreading a very large array into `push` can hit its own `RangeError`.

## The interview version: how to think about it

The question is easy to memorise and hard to explain, so practise the reasoning:

1. **Ask what's inside.** Only numbers, or strings, `null`, objects? `flat` leaves non-array values alone, and so should you.
2. **Ask about depth.** One level, a given depth, or all the way? That decides between `reduce`, a depth counter and full recursion.
3. **Find the repeating shape.** An array of arrays of arrays is the same problem at every layer. That's the signal to use recursion.
4. **State the base case.** An item that isn't an array is kept as-is.
5. **Mention the limit.** Recursion and very deep input. Offer the stack version as the answer.

Two edge cases worth knowing, both from real runs:

```js
console.log([1, , [2, , 3]].flat());
console.log([1, [2], "ab", null, undefined, [[]]].flat(Infinity));
```

```text
[ 1, 2, 3 ]
[ 1, 2, 'ab', null, undefined ]
```

`flat` drops empty slots in sparse arrays, and an empty nested array vanishes. Strings aren't split into characters. My hand-written versions keep `undefined` but behave differently on sparse arrays: `for...of` visits empty slots as `undefined`, so they'd stay in the output. If an interviewer asks, say so.

## When not to write your own

If `flat` is available, don't rewrite it. It's shorter, other people recognise it, and it handles holes the standard way. Write your own when the interviewer asks for it, when you need custom behaviour (flatten only certain keys, say), or when depth could be extreme.

## Where this leaves you

Reach for `flat(Infinity)` first. When asked to build it, use recursion for the clearest answer and a stack when you need to avoid call-stack limits.

I haven't benchmarked these approaches. Any claim about which is faster would be a guess, so I left it out. Which approach do you reach for first in an interview: recursion, or `reduce`?
