---
title: "What new Really Does: Four Steps Behind Every JavaScript Constructor"
slug: javascript-new-keyword
subtitle: Constructor functions, the four steps new performs, how it links objects to prototypes, and the gotchas, with a hand-built new and real output
tags: javascript, web-development, beginners, programming, oop
cover: ./cover.png
seoTitle: "The new Keyword in JavaScript: Constructors and Prototypes"
seoDescription: "The new keyword in JavaScript explained: constructor functions, its four steps, prototype linking, instances and gotchas, with real output."
enableToc: true
---

Here's a constructor function, called **without** `new`:

```js
function Person(name) {
  this.name = name;
}

const result = Person("Oops");   // no new!
console.log(result);
console.log(globalThis.name);
```

```text
undefined
Oops
```

The function returned `undefined`, and `name` ended up on **`globalThis`**, the global object. No new object was created. The function ran like any ordinary function, with `this` pointing at the global scope (in a normal, non-strict file), so `this.name = name` quietly set a global variable.

Without `new`, nothing gives the function a fresh object to fill in. That silent leak only happens in a plain script; run the same code as an ES module and it throws instead, as the strict-mode example below shows. This post covers what `new` does, how constructor functions use it, and how it connects each object to a prototype, including a hand-built version of `new` tested against the real one. Every output is real, from Node.js 24.22.

## What the new keyword does

`new Person("Asha")` performs four steps, in order:

1. It creates a new, empty object.
2. It links that object to `Person.prototype`, so the object can use methods stored there.
3. It calls `Person` with `this` set to the new object.
4. It returns that object (unless the constructor returns a different object, covered below).

Steps 2 and 3 are where the interesting parts are, and the sections below take them one at a time.

## Constructor functions

A **constructor function** is an ordinary function written to be called with `new`. By convention its name starts with a capital letter, so readers know to use `new`:

```js
function Person(name, age) {
  this.name = name;
  this.age = age;
}

const asha = new Person("Asha", 24);
const ravi = new Person("Ravi", 22);
console.log(asha);
console.log(ravi);
```

```text
Person { name: 'Asha', age: 24 }
Person { name: 'Ravi', age: 22 }
```

Each `new Person(...)` call ran the function once, with `this` as a fresh object, and handed that object back. Two calls gave two separate objects. The `Person` at the front of the printout is the name of the constructor that made each one.

Inside the constructor, `this` is the same "who is calling" idea from [Look Left of the Dot](https://jaydeepkanzariya.hashnode.dev/javascript-this-keyword). `new` is one more way JavaScript decides what `this` is.

Forgetting `new` doesn't always leak onto the global object. In **strict mode**, which modules and classes use automatically, it fails loudly instead:

```js
"use strict";
function Person(name) {
  this.name = name;
}
Person("Oops");   // no new!
```

```text
TypeError: Cannot set properties of undefined (setting 'name')
```

In a plain strict-mode call, `this` is `undefined`, so `this.name = name` has nothing to write to.

## Creating an object, step by step

The best way to see what `new` does is to rebuild it. Here's `myNew`: `Object.create` covers steps 1 and 2, `apply` covers step 3, and the last line is step 4. It's tested against the real `new`:

```js
function Person(name) {
  this.name = name;
}
Person.prototype.greet = function () {
  return `Hi, I'm ${this.name}`;
};

function myNew(Constructor, ...args) {
  const obj = Object.create(Constructor.prototype);   // 1 + 2: empty object, linked to the prototype
  const result = Constructor.apply(obj, args);        // 3: run the constructor with this = obj
  const returnedAnObject = typeof result === "object" && result !== null;
  return returnedAnObject || typeof result === "function" ? result : obj;   // 4: hand back the object
}

const real = new Person("Asha");
const mine = myNew(Person, "Asha");
console.log("real:", real, "| mine:", mine);
console.log("same prototype:", Object.getPrototypeOf(real) === Object.getPrototypeOf(mine));
console.log("mine instanceof Person:", mine instanceof Person);
console.log("mine.greet():", mine.greet());
```

```text
real: Person { name: 'Asha' } | mine: Person { name: 'Asha' }
same prototype: true
mine instanceof Person: true
mine.greet(): Hi, I'm Asha
```

The result has the same shape, the same prototype, passes `instanceof`, and can use the prototype method `greet`. The last line of `myNew` handles one edge case: if the constructor itself returns an object, that object wins. I show that in the gotchas below.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    C["new Person('Asha')"] --&gt; S1["1. Create an empty object"]
    S1 --&gt; S2["2. Link it to Person.prototype"]
    S2 --&gt; S3["3. Run Person with this = the new object"]
    S3 --&gt; S4["4. Return the object"]
    S4 --&gt; R["asha: Person { name: 'Asha' }"]
-->
![Constructor to instance creation flow: new Person('Asha') performs four steps in order, creating an empty object, linking it to Person.prototype, running Person with this set to the new object, and returning the object, which becomes asha, Person { name: 'Asha' }](https://mermaid.ink/img/pako:eNplkkFLw0AQhf_KMJcqpKG7SZtkQUHqUUHam9ke1mRsos1u2EyotfS_S5NWBI8zfO-9GXhHLFxJqPB95_ZFZTzD00p7bQEAlrlGS3t4Id85ezN56CozudW4gen0HtYi1yhCWHoyTGAsUNPyAdzbBxWscXO1WYuRl7lGGcJTbT-hZmB3MQ5b79jxoaW_IjmKolxjFMKqtxca9jVXwFXdwR1wRXC-8H9mNMrjXGMcwoq493bA_6PxgK5yjaarjLrmHMGahhSMb8NJ4wYD3Pq6RMW-pwAb8o05j3g8W2nkihrSqECjp7L_mhZu57xGbU8YYGvsq3PNVe1dv61QvZtdRwH2bWmYHmuz9ab53XqyJfml6y2jkmLwQHXEL1SxSEOZZotMzESWRLMowAMqIWUYy7mM0jSZpUmWJacAv4fUWSgXYr5IxTxNF3GWzAOksmbnn8cGDEU4_QBOmqEM?type=png)
*Four steps, always in this order. The last one hands you the object.*

One honest limit: `myNew` is a teaching version, not a replacement. It can't build instances of a `class`, because calling a class without `new` throws, and it ignores details like `new.target`.

## How new links prototypes

Step 2 is the one that surprises people. Every ordinary function declared with `function` has a `prototype` property (arrow functions, `async` functions and method shorthand don't get one): an object that `new` uses as the **prototype** of everything it creates. Put a method on it, and every instance can use it:

```js
function Person(name) {
  this.name = name;
}
Person.prototype.greet = function () {
  return `Hi, I'm ${this.name}`;
};

const asha = new Person("Asha");
const ravi = new Person("Ravi");

console.log(Object.getPrototypeOf(asha) === Person.prototype);
console.log(Object.hasOwn(asha, "name"), Object.hasOwn(asha, "greet"));
console.log(asha.greet === ravi.greet);
console.log(asha.greet(), "/", ravi.greet());
```

```text
true
true false
true
Hi, I'm Asha / Hi, I'm Ravi
```

Four lines, four facts:

- The instance's prototype **is** `Person.prototype` (`true`).
- `name` is the instance's own property, but `greet` isn't (`true false`). `greet` lives on the prototype.
- Still, `asha.greet === ravi.greet` is `true`: both objects found the **same** function.
- Each call used its own `this`, so each greeted with its own name.

When you write `asha.greet()`, JavaScript looks on `asha` first. It doesn't find `greet` there, so it follows the link to `Person.prototype` and finds it. That trail of links is the **prototype chain**.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    A["asha<br/>name: 'Asha'"] --&gt;|"prototype link"| P["Person.prototype<br/>greet()"]
    R["ravi<br/>name: 'Ravi'"] --&gt;|"prototype link"| P
    F["Person function"] --&gt;|".prototype"| P
    P --&gt;|".constructor"| F
-->
![Prototype linking visual: the objects asha and ravi each hold their own name and both link to Person.prototype, which holds the shared greet() method; the Person function points to Person.prototype through its prototype property, and Person.prototype points back to Person through its constructor property](https://mermaid.ink/img/pako:eNp9kUFvgkAQhf_KZi62CVJAhWXTmJg2ntrEeKzrYQsjkMIuGRarVf97Aw3aXnqcvPd97zAnSEyKIGBXms8kV2TZy1qS1IwxtthIUE2uHt_pYa5VhYKNFk2uRhK2bDyenyXUZKyxxxpZWegPCWe22khYITVGu9ewF2SEaO_uJWwH_3ojgdS--O1fq33xv3-gl9chtmt1Ygujb9xt-w-zGuLE6MZSm1hDXWEJDmRUpCAstehAhVSp7oRTB0qwOVYoQTAJhGl7GCem7FCpL-BArfSbMdVAk2mzHMROlQ060NapsvhcqIzUrYI6RXoyrbYggrBXgDjBAcTU527A4zD2PT-OJt7EgSMIPwjcaTALJpxHHo_iOLo48NWPem4Q-rOQ-zPOw2kczRzAtLCGXn9e23_48g2265sv?type=png)
*Both objects link to one prototype, so there's one greet() shared by all.*

Compare that with defining the method inside the constructor:

```js
function Dog(name) {
  this.name = name;
  this.bark = function () {      // a new function for every dog
    return "Woof";
  };
}

console.log(new Dog("Bruno").bark === new Dog("Rex").bark);
```

```text
false
```

Each `new Dog(...)` created a brand-new `bark` function, so the two dogs hold two different copies (`false`). On the prototype, there's one function shared by all. That's why methods usually go on the prototype.

## Instances made from constructors

An **instance** is an object made by `new` from a given constructor. JavaScript can answer "what made this?" in a few ways:

```js
function Person(name) {
  this.name = name;
}
const asha = new Person("Asha");

console.log(asha instanceof Person);
console.log(asha instanceof Object);
console.log(asha.constructor === Person);
console.log(Object.hasOwn(asha, "constructor"));
console.log(Person.prototype.constructor === Person);
```

```text
true
true
true
false
true
```

- `asha instanceof Person` is `true`: `instanceof` checks whether `Person.prototype` appears in the object's prototype chain.
- `asha instanceof Object` is also `true`. The chain continues up to `Object.prototype`, which nearly every object inherits from.
- `asha.constructor === Person` is `true`, yet `Object.hasOwn(asha, "constructor")` is `false`. `asha` has no `constructor` of its own; it found one on `Person.prototype`, which points back at the function that made it. The last line shows that link directly.

## Gotchas

**A constructor can return something else.** Normally it doesn't return anything, and `new` hands back the object it built. But if the constructor returns an object, `new` uses that instead:

```js
function ReturnsObject() {
  this.a = 1;
  return { b: 2 };       // an object replaces the new one
}
function ReturnsPrimitive() {
  this.a = 1;
  return 42;             // a primitive is ignored
}

console.log(new ReturnsObject());
console.log(new ReturnsPrimitive());
```

```text
{ b: 2 }
ReturnsPrimitive { a: 1 }
```

The first call returned `{ b: 2 }`, and the object with `a: 1` was thrown away. The second returned `42`, a primitive, which `new` ignores. That's why constructors normally don't use `return` at all.

**Arrow functions can't be constructors.**

```js
const Person = (name) => {
  this.name = name;
};
new Person("Asha");
```

```text
TypeError: Person is not a constructor
```

An arrow function has no `this` of its own, and no `prototype` for `new` to link to, so `new` has nothing to work with. Use a regular function, or a class, for constructors.

## new and classes

`class` syntax runs the same machinery, with tidier clothes:

```js
class Person {
  constructor(name) {
    this.name = name;
  }
  greet() {
    return `Hi, I'm ${this.name}`;
  }
}

console.log(typeof Person);
console.log(Person.prototype.constructor === Person);
const asha = new Person("Asha");
console.log(Object.hasOwn(asha, "greet"), Object.getPrototypeOf(asha) === Person.prototype);
Person("Asha");
```

```text
function
true
false true
TypeError: Class constructor Person cannot be invoked without 'new'
```

`typeof Person` is `"function"`, `Person.prototype.constructor` points back at it, and `greet`, written inside the class, ended up on the prototype (`false true`: not an own property, and the prototype link is intact). That's exactly what the hand-written version did. The one difference is the last line: a class refuses to run without `new`, instead of leaking onto `globalThis`.

I covered classes in [One Blueprint, Many Objects](https://jaydeepkanzariya.hashnode.dev/one-blueprint-many-objects-classes-in-javascript-for-beginners). In new code, prefer `class`: it's harder to misuse. Constructor functions are still worth knowing because you'll meet them in older code, and because they show what `class` does underneath. And as in [the string polyfills post](https://jaydeepkanzariya.hashnode.dev/javascript-string-polyfills), don't add methods to built-in prototypes like `Array.prototype` in your own application code.

The takeaway: **`new` creates an empty object, links it to the constructor's `prototype`, runs the constructor with `this` set to that object, and returns it. Methods on the prototype are shared by every instance; methods created inside the constructor are copied for each one.** This post stopped before inheritance between constructors, which builds on exactly these prototype links.

Create two objects with `new` from the same constructor and compare `Object.getPrototypeOf(a) === Object.getPrototypeOf(b)`. What do you expect, and why?
