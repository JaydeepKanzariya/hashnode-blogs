---
title: "Borrow a Method, Lock a this: call(), apply() and bind() Explained"
slug: javascript-call-apply-bind
subtitle: What this means, then how call, apply and bind let you choose it yourself, with a comparison table and real output
tags: javascript, web-development, beginners, programming, frontend
cover: ./cover.png
seoTitle: "call, apply and bind in JavaScript, Explained"
seoDescription: "Learn this, call(), apply() and bind() in JavaScript: borrow methods, pass arguments one by one or as an array, and lock this for later. With a table."
enableToc: true
---

Here's an object with a useful method:

```js
const laptop = {
  name: "ThinkPad",
  price: 72000,
  describe(currency, note) {
    return `${this.name} costs ${currency}${this.price} ${note}`;
  },
};

const phone = { name: "Pixel", price: 45000 };
```

`phone` needs a `describe()` too. You could copy the method into it. Or you could **borrow** `laptop`'s method and run it with `phone` as its `this`. That's what `call()`, `apply()` and `bind()` are for. Each one lets you choose `this` yourself, instead of leaving it to however the function happens to be called.

All outputs below are real, from Node.js 24.22 with `"use strict"` on, which is how modules and classes behave by default.

## this in one minute

`this` is **whoever is calling the function**. At the call, look at what's to the left of the dot:

```js
laptop.describe("₹", "(in stock)");
```

```text
ThinkPad costs ₹72000 (in stock)
```

`laptop` is left of the dot, so `this` is `laptop`. Take the function away from its object and call it on its own, and there's no caller:

```js
const plain = laptop.describe;
plain("₹", "(?)");
```

```text
TypeError: Cannot read properties of undefined (reading 'name')
```

With nothing left of the dot, `this` is `undefined` in strict mode, and `this.name` crashes. I covered every case (global scope, nested objects, arrow functions, event handlers) in [Look Left of the Dot: how JavaScript decides what this is](https://jaydeepkanzariya.hashnode.dev/javascript-this-keyword). This post is about the next step: **choosing `this` yourself**.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    A["laptop.describe()"] --&gt;|caller: laptop| F["describe"]
    B["describe.call(phone)"] --&gt;|caller you chose: phone| F
    C["plain()"] --&gt;|no caller| F
    F --&gt; R1["this = laptop"]
    F --&gt; R2["this = phone"]
    F --&gt; R3["this = undefined"]
-->
![Function to caller relationship: laptop.describe() makes laptop the caller so this is laptop; describe.call(phone) makes phone the caller you chose so this is phone; plain() has no caller so this is undefined](https://mermaid.ink/img/pako:eNplkk1vgkAQhv_KZE42QcKHwLJJm7Q2ntqLx7IetuwoJLBLFki16n9vQKmmPc7M834c5oi5UYQct5X5ygtpO3hbCys0AMBzJrCSTWcaV1Gb2_KTZg8CNzCfP51yWVVkOVyAE6wygRMlcDN5vNyt3UEzawqj6Y8NHEwPeWFa4jDeT7CaHJaZwKaSpb5lawMX3R22Gi6w9jOBXVG28HhtdtfligQ3ZMz6T4Q3oteKtqUmJXCDDu5sqZB3ticHa7K1HEY8DupBQjUJ5CDQkur389xUxgoU-owONlJ_GFNPamv6XYF8K6uWHOwbJTt6LeXOyvp3a0krskvT6w55zEYP5EfcI1_4zA1YGqe-56dJ6IUOHpD7QeAugigIGUs8lqRpcnbwe0z13CD2o5j5EWPxIk0iB0mVnbHvlwcY_-D8A5qbo-4?type=png)
*Same function, three callers. `call`, `apply` and `bind` let you pick the caller yourself.*

## call(): run it now, with this this

`call()` runs a function **immediately**, with the first argument as `this`. Any further arguments are passed to the function, one by one:

```js
laptop.describe.call(phone, "₹", "(borrowed with call)");
```

```text
Pixel costs ₹45000 (borrowed with call)
```

Same function, but `this` is now `phone`, so it reads `phone.name` and `phone.price`. `phone` never got a copy of the method. It borrowed it for one call.

## apply(): the same, with an array of arguments

`apply()` does exactly what `call()` does, with one difference: the function's arguments come as **one array**.

```js
laptop.describe.apply(phone, ["₹", "(borrowed with apply)"]);
```

```text
Pixel costs ₹45000 (borrowed with apply)
```

That's useful when your arguments are already in an array. The classic example is `Math.max`, which takes separate numbers, not an array:

```js
const scores = [72, 95, 64, 88];
Math.max.apply(null, scores); // 95
Math.max(...scores);          // 95
```

Both print `95`. `Math.max` doesn't use `this`, so `null` is a placeholder. In modern code, the spread operator (`...scores`) does the same job more readably, which is why you'll see `apply` less often than you used to. It still shows up in older code and libraries.

## bind(): a new function for later

`bind()` is the odd one out: **it doesn't run anything**. It returns a new function with `this` permanently set, which you can store and call later:

```js
const describePhone = laptop.describe.bind(phone);
typeof describePhone;          // "function"
describePhone("₹", "(bound)"); // Pixel costs ₹45000 (bound)
```

That's exactly what you need when you hand a method to someone else to call later, like a timer. Without `bind`, the method loses its object:

```js
const counter = {
  count: 0,
  start() {
    setTimeout(this.tick, 0);            // ❌ setTimeout calls it, not counter
    setTimeout(this.tick.bind(this), 0); // ✅ this locked to counter
  },
  tick() { /* logs whether this is counter */ },
};
counter.start();
```

```text
this is not counter
tick, count = 1
```

`bind` can also **pre-fill arguments**. Pass extra values after `this`, and they're fixed at the front of every call:

```js
const describeInRupees = laptop.describe.bind(phone, "₹");
describeInRupees("(currency pre-filled)"); // Pixel costs ₹45000 (currency pre-filled)
```

### Two limits worth knowing

**A bound function stays bound.** Binding it again doesn't change `this`:

```js
const rebound = describePhone.bind(laptop);
rebound("₹", "(bound again?)");
```

```text
Pixel costs ₹45000 (bound again?)
```

Still `Pixel`. The first `bind` wins.

**Arrow functions ignore all three.** An arrow function has no `this` of its own; it uses the `this` from where it was written. `call`, `apply` and `bind` can't change that:

```js
const arrowName = () => this.name;
arrowName.call(phone);   // undefined
arrowName.bind(phone)(); // undefined
```

If you need to choose `this`, use a regular function or method.

## call vs apply vs bind

| | `call()` | `apply()` | `bind()` |
|---|---|---|---|
| Runs the function | Immediately | Immediately | No, returns a new function |
| Sets `this` to | First argument | First argument | First argument, permanently |
| Other arguments | One by one: `fn.call(obj, a, b)` | As an array: `fn.apply(obj, [a, b])` | One by one, pre-filled: `fn.bind(obj, a)` |
| Returns | The function's result | The function's result | A new function |
| Typical use | Borrowing a method once | Arguments already in an array | Callbacks, timers, event handlers |

A memory aid: **call is comma-separated, apply is an array, bind is for later.**

## Try it: the assignment

The brief's four steps in one script:

```js
// 1. An object with a method that uses this
const student = {
  name: "Asha",
  course: "Web Dev Cohort 2026",
  introduce(greeting, city) {
    return `${greeting}! I'm ${this.name} from ${city}, studying ${this.course}.`;
  },
};
console.log(student.introduce("Hi", "Pune"));

// 2. Borrow that method with call()
const mentor = { name: "Ravi", course: "JavaScript" };
console.log(student.introduce.call(mentor, "Hello", "Surat"));

// 3. apply() with array arguments
const args = ["Namaste", "Ahmedabad"];
console.log(student.introduce.apply(mentor, args));

// 4. bind() and store the function
const ravisIntro = student.introduce.bind(mentor, "Hey");
console.log(ravisIntro("Mumbai"));
console.log(ravisIntro("Delhi"));
```

```text
Hi! I'm Asha from Pune, studying Web Dev Cohort 2026.
Hello! I'm Ravi from Surat, studying JavaScript.
Namaste! I'm Ravi from Ahmedabad, studying JavaScript.
Hey! I'm Ravi from Mumbai, studying JavaScript.
Hey! I'm Ravi from Delhi, studying JavaScript.
```

One method, written once on `student`, used by `mentor` three different ways. The bound version, `ravisIntro`, remembers both its `this` and its greeting across calls.

The takeaway: **`this` is normally chosen by whoever calls the function. `call` and `apply` let you choose it for one call, and `bind` lets you choose it for good.** This post stuck to plain objects. Classes and `new` set `this` their own way, and React class components were a common place to see `.bind(this)` in constructors.

Which have you used most in real code: `bind` for callbacks, or the spread operator in place of `apply`?
