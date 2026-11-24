---
title: "JavaScript Arrays 101: Why the First Item Is at Index 0"
slug: javascript-arrays-101
subtitle: Creating arrays, reading and updating by index, the length property and looping, with the off-by-one mistakes to avoid
tags: javascript, web-development, beginners, programming, frontend
cover: ./cover.png
seoTitle: "JavaScript Arrays for Beginners: Index, Length, Loops"
seoDescription: "JavaScript arrays for beginners: create an array, access and update items by index, use length, loop over it, and avoid the classic off-by-one bugs."
enableToc: true
---

Say you're storing five exam marks:

```js
const mark1 = 72;
const mark2 = 85;
const mark3 = 64;
const mark4 = 90;
const mark5 = 78;
```

Now work out the average. You'd type all five names. Add a sixth mark and you'd have to find every place that lists them and add `mark6`. With fifty students, this stops working entirely.

An **array** stores all of them under one name, in order:

```js
const marks = [72, 85, 64, 90, 78];

let total = 0;
for (let i = 0; i < marks.length; i++) {
  total += marks[i];
}
console.log("average:", total / marks.length); // average: 77.8
```

That loop works the same for five marks or five hundred. This post covers the basics: creating arrays, reading and changing items, `length`, and looping. It gives the most attention to the one rule behind most beginner array bugs: **counting starts at 0**. Every output is real, from Node.js 24.22.

## What arrays are and why we need them

An array is an **ordered collection of values**. Each value sits at a numbered position called its **index**, and the first index is `0`, not `1`.

```js
const fruits = ["apple", "banana", "mango", "grapes", "orange"];
```

| Index | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Value | `"apple"` | `"banana"` | `"mango"` | `"grapes"` | `"orange"` |

Compared with separate variables, an array gives you one name for the whole group, a fixed order, a count of how many items there are, and a way to loop over all of them without naming each one.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    N["fruits"] --&gt; B0["0<br/>'apple'"]
    B0 --- B1["1<br/>'banana'"]
    B1 --- B2["2<br/>'mango'"]
    B2 --- B3["3<br/>'grapes'"]
    B3 --- B4["4<br/>'orange'"]
-->
![Array index and values: the fruits array holds 'apple' at index 0, 'banana' at 1, 'mango' at 2, 'grapes' at 3 and 'orange' at 4](https://mermaid.ink/img/pako:eNpV0T9vwjAQBfCvYr2FJaGx88-xKgbase3QsTGDISZESuzoSFRaxHevwEIV40m_d3fSO2PnGwuFfe-_dwdDE3v71KQdY4x91Bp7mrvpqLFhcbxi66TWSJ639LRamHHs7UJjc-frhMVxzNa81uDBbI0zzjwgHpCoNURAg3GtfzAimLTWSINpyYz2-IDSgLJaIwvIk3Ht7SVEaKlroCaabYTB0mCuI87XsMZ0sIPVUEyDbDOf4p3vPWlod0GE0bgv74d7mvzcHqD2pj_aCPPYmMm-dqYl80-sayy9-NlNUFVxWwF1xgkq43IpZFVUPOFVmSZphB8oLsQyE7lIpSwTWVZVeYnwezuaLEXB80LyXMoiq8o8gm26ydN7aOpW2OUPObiAhQ?type=png)
*Five values, indexes 0 to 4. The last index is always one less than the length.*

## How to create an array

Square brackets with values separated by commas:

```js
const tasks = ["write", "review", "deploy"];
const empty = [];                     // an empty array, length 0
const mixed = ["Asha", 24, true, null]; // allowed, but usually avoided
```

JavaScript allows mixed types in one array. In practice, keep each array to one kind of thing (all names, all marks), so code that loops over it can treat every item the same way.

You may also see `new Array()`. It has a trap:

```js
new Array(3);    // [ <3 empty items> ]
new Array(3, 4); // [ 3, 4 ]
```

With one number, it creates an array of that **length** with nothing in it. With two, it creates an array of those values. Stick to `[]` and you'll never hit this.

## Accessing elements by index

Put the index in square brackets:

```js
fruits[0]; // "apple"   ← first item
fruits[2]; // "mango"   ← third item
```

Because counting starts at 0, **the last item is at `length - 1`**:

```js
fruits.length;                // 5
fruits[fruits.length - 1];    // "orange"
```

Five items means indexes 0 to 4. There's nothing at index 5, and JavaScript doesn't complain if you ask:

```text
fruits[5]:              undefined
fruits[fruits.length]:  undefined
```

No error, just `undefined`. That's what makes off-by-one mistakes hard to spot: the code keeps running with a missing value instead of stopping.

Newer JavaScript also has a shortcut for the last item: `fruits.at(-1)` returns `"orange"`. Negative numbers count from the end.

## Updating elements

Assign a new value to an index:

```js
const tasks = ["write", "review", "deploy"];
tasks[1] = "test";
console.log(tasks); // [ 'write', 'test', 'deploy' ]
```

Notice `tasks` is a `const`, and changing an item still worked. `const` stops you from replacing the **whole array**, not from changing what's inside it:

```js
tasks = [];
```

```text
TypeError: Assignment to constant variable.
```

Be careful assigning past the end, though:

```js
const gap = ["a", "b"];
gap[5] = "f";
console.log(gap, gap.length);
```

```text
[ 'a', 'b', <3 empty items>, 'f' ] 6
```

JavaScript filled the space with **empty slots**, and `length` jumped to 6. Reading one of those slots gives `undefined`. It's almost never what you meant; to add an item at the end, you'll later use `push()`.

## The length property

`length` is the number of items, and it's always **one more than the last index**. It updates on its own as the array changes.

It can also be set, and setting it smaller **cuts the array**:

```js
const nums = [1, 2, 3, 4, 5];
nums.length = 3;
console.log(nums); // [ 1, 2, 3 ]
```

Items 4 and 5 are gone. Good to know, mostly so you don't do it by accident.

## Looping over arrays

The classic `for` loop counts through the indexes:

```js
for (let i = 0; i < fruits.length; i++) {
  console.log(i, fruits[i]);
}
```

The condition is `i < fruits.length`, **less than**. Here's what happens with `<=`, a classic beginner bug:

```text
0 apple
1 banana
2 mango
3 grapes
4 orange
5 undefined
```

One step too far: index 5 doesn't exist, so the last line is `undefined`. The rule: **start at 0, stop before `length`**.

When you don't need the index, `for...of` hands you each value directly, and there's no counting to get wrong:

```js
for (const fruit of fruits) {
  console.log(fruit);
}
```

```text
apple
banana
mango
grapes
orange
```

## How arrays are stored, conceptually

A useful picture: an array is a row of numbered boxes. The array's name points at the row, and each index is a box number. To get `fruits[3]`, go to box 3.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart TB
    V["const fruits"] --&gt; R
    subgraph R["one array: boxes in order"]
        direction LR
        C0["[0]<br/>apple"] --- C1["[1]<br/>banana"] --- C2["[2]<br/>mango"] --- C3["[3]<br/>grapes"] --- C4["[4]<br/>orange"]
    end
    L["length = 5"] -.-&gt; R
-->
![Memory-style block diagram of array storage, as a mental model: the variable fruits points to one array of numbered boxes in order, [0] apple, [1] banana, [2] mango, [3] grapes and [4] orange, with length equal to 5](https://mermaid.ink/img/pako:eNpN0s2OozAMAOBXsXymHcJPgWhmDts9zl6q1R6W9JASF5AgQSZoO1v13UcpajU5Jf7i2JF8xcYZQonnwf1rOs0efv9QrCwAwJ9aYePs7OHMS-9nhUfYbN7h8LgwL6eW9dTBoVboLIFm1p8STu5CM_QWHBtihcdHQlimZ2p87yx8HL7H93GtsI6Pryd-edfTNNBabwN7EUSsctJWW_2kJFCy0qht656SBklXCV3S_KQsULaSY21b-tYjWfPYftQKB7Kt7-AN8nv6NvwfI2y5Nyg9LxThSDzqcMRryFPoOxpJoQSFTGa5bBo3OFao7A0jnLT969z4yGa3tB3Ksx5minCZjPb0s9ct6_EZZbKGeO8W61GKOL4_gvKKF5SZKLdJWe0qEYuqSOM0wk-UIkm2WZInaVkWcVlUVXGL8P-9bLxNdiLflSIvy11WFXmEZHrv-Nc6CveJuH0Bypyh3w?type=png)
*A mental model, not real memory layout: numbered boxes in order, and a length that counts them.*

That's a **mental model**, not a description of memory. JavaScript engines store arrays in different ways depending on what's in them, and the language doesn't promise a particular layout. For writing code, "numbered boxes in order, starting at 0" is all you need.

## Try it: the assignment

The brief's four steps in one script:

```js
// 1. An array of 5 favourite movies
const movies = ["3 Idiots", "Dangal", "Inception", "Interstellar", "Lagaan"];

// 2. Print the first and last element
console.log("First:", movies[0]);
console.log("Last:", movies[movies.length - 1]);

// 3. Change one value and print the updated array
movies[2] = "The Dark Knight";
console.log("Updated:", movies);

// 4. Loop through the array and print every element
for (let i = 0; i < movies.length; i++) {
  console.log(`${i + 1}. ${movies[i]}`);
}
```

```text
First: 3 Idiots
Last: Lagaan
Updated: [ '3 Idiots', 'Dangal', 'The Dark Knight', 'Interstellar', 'Lagaan' ]
1. 3 Idiots
2. Dangal
3. The Dark Knight
4. Interstellar
5. Lagaan
```

Note `${i + 1}` in the loop. The index starts at 0, but people count from 1, so the printed list adds one.

The takeaway: **an array is an ordered list under one name; indexes start at 0, so the last item is at `length - 1`, and loops stop before `length`.** Most early array bugs are that rule broken by one. This post skipped array methods on purpose. `push`, `pop`, `map`, `filter` and friends are the natural next step, and they all build on indexes and `length`.

Without running it: what does `["a", "b", "c"][3]` give you, and why isn't it an error?
