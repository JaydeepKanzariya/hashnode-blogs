---
title: "person.key vs person[key]: JavaScript Objects for Beginners"
slug: javascript-objects-basics
subtitle: What objects are, creating them, dot vs bracket notation, updating, adding and deleting properties, and looping through keys, with real output
tags: javascript, web-development, beginners, programming, frontend
cover: ./cover.png
seoTitle: "JavaScript Objects for Beginners: Keys and Values"
seoDescription: "JavaScript objects for beginners: create objects, dot vs bracket notation, update, add and delete properties, loop through keys, arrays vs objects."
enableToc: true
---

Here's a person stored as an array:

```js
const person = ["Asha", 24, "Pune"];
console.log(person[1]); // 24
```

`person[1]` is `24`. But 24 *what*? Age? House number? Years at the company? The array knows the order, not the meaning. You have to remember that position 1 is the age, and so does everyone who reads your code.

Here's the same person as an **object**:

```js
const person = { name: "Asha", age: 24, city: "Pune" };
console.log(person.age); // 24
```

Every value has a name. `person.age` says what it is. That's the whole idea of objects, and this post covers how to create them, read and change them, add and remove properties, and loop through them. Every output is real, from Node.js 24.22.

## What objects are and why we need them

An object is a collection of **key-value pairs**. Each **key** is a name (a string), and each **value** is the data stored under that name. Together, a key and its value are called a **property**.

```js
const person = { name: "Asha", age: 24, city: "Pune" };
```

`name`, `age` and `city` are the keys; `"Asha"`, `24` and `"Pune"` are the values. Think of a form with labelled fields: the label is the key, and what's written next to it is the value.

You need objects whenever data has **parts with meanings**: a user, a product, a setting, an order. Arrays are for lists of similar things; objects are for one thing described by several named facts.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    subgraph P["person object"]
        K1["name"] --&gt; V1["'Asha'"]
        K2["age"] --&gt; V2["24"]
        K3["city"] --&gt; V3["'Pune'"]
    end
-->
![Object key-value structure: the person object has three keys, name, age and city, each pointing to its value: name to 'Asha', age to 24, city to 'Pune'](https://mermaid.ink/img/pako:eNpdkc1qwzAQhF9FzCUXJ9jyn6xDobS3thB66KFWD4q9sV1iycgyTRry7sUpSUv2NsO3swtzRGVrgsR2Z7-qVjvPnl-VU4YxxsZp0zg9tGxdKgzkRmuY3XxS5RU-LtA8T1GpYHRPCh9subxjb7OxuB9bvbhFeamgmz9y1jy5peJSoer84YrNxmI9GfofSKZGgMZ1NaR3EwXoyfV6ljjOiIJvaX5LMgVH9bRfVnZnnYIyJwQYtHm3tr9sOzs1LeRW70YKMA219vTY6cbp_uo6MjW5BzsZD8n5OQPyiD1kEokVF0VWRGFU5HEYBzhARpyvEp7yWIg8FHlR5KcA3-er4YpnUZqJKBUiS4o8DUB15617-S3l3M3pB2aVe_o?type=png)
*Every value in an object sits behind a name.*

## Creating objects

The usual way is an **object literal**: curly braces, with `key: value` pairs separated by commas.

```js
const person = { name: "Asha", age: 24, city: "Pune" };
```

Values can be anything: strings, numbers, booleans, arrays, even other objects:

```js
const user = {
  name: "Asha",
  skills: ["js", "css"],
  address: { city: "Pune", pin: "411001" },
  active: true,
};

user.skills[0];     // "js"
user.address.city;  // "Pune"
```

You can also start with an empty object and add properties as you go:

```js
const student = {};
student.name = "Ravi";
student.course = "JS";
console.log(student); // { name: 'Ravi', course: 'JS' }
```

## Accessing properties: dot vs bracket notation

There are two ways to read a property:

```js
person.age;       // 24      ← dot notation
person["city"];   // "Pune"  ← bracket notation, key as a string
```

Dot notation is shorter, and it's what you'll use most. Bracket notation is needed in two situations.

**1. The key isn't a valid name.** Keys with spaces or dashes can't follow a dot:

```js
const profile = { "favourite color": "teal", "home-town": "Surat" };
profile["favourite color"]; // "teal"
```

**2. The key is stored in a variable.** This is the one that catches beginners:

```js
const key = "city";
console.log(person.key);  // undefined
console.log(person[key]); // Pune
```

`person.key` doesn't read the variable `key`. It looks for a property **literally named "key"**, which doesn't exist, so you get `undefined`. `person[key]` evaluates `key` first, gets `"city"`, and reads `person.city`. Rule of thumb: **dot for names you type, brackets for names you compute.**

### Missing properties

Reading a property that doesn't exist isn't an error. You just get `undefined`:

```js
person.email; // undefined
```

But going one level deeper **is** an error, because you're now asking `undefined` for a property:

```js
person.address.pin;
```

```text
TypeError: Cannot read properties of undefined (reading 'pin')
```

That's one of the most common runtime errors in JavaScript, and I covered handling it in [try/catch/finally in JavaScript](https://jaydeepkanzariya.hashnode.dev/javascript-error-handling).

## Updating properties

Assign a new value to an existing key:

```js
person.age = 25;
console.log(person); // { name: 'Asha', age: 25, city: 'Pune' }
```

`person` was declared with `const`, and the update still worked. `const` stops you from **replacing the whole object**, not from changing what's inside it:

```js
person = {};
```

```text
TypeError: Assignment to constant variable.
```

## Adding and deleting properties

Adding a property uses exactly the same syntax as updating one. If the key doesn't exist yet, it's created:

```js
person.email = "asha@example.com";
// { name: 'Asha', age: 25, city: 'Pune', email: 'asha@example.com' }
```

To remove one, use `delete`:

```js
delete person.email; // true
// { name: 'Asha', age: 25, city: 'Pune' }
```

Deleting a property isn't the same as setting it to `undefined`. Here are two identical objects, one of each:

```js
const a = { name: "Asha", city: "Pune" };
const b = { name: "Asha", city: "Pune" };
a.city = undefined;
delete b.city;
```

```text
a:                      { name: 'Asha', city: undefined }
b:                      { name: 'Asha' }
"city" in a / in b:     true false
Object.keys(a) / (b):   [ 'name', 'city' ] [ 'name' ]
```

`a` still **has** a `city` key, just with no value; `b` doesn't have one at all. The difference shows up when you loop over keys, count them, or send the object as JSON. Use `delete` when the property should really be gone.

## Looping through object keys

`for...in` visits each key of an object:

```js
for (const key in person) {
  console.log(key, "->", person[key]);
}
```

```text
name -> Asha
age -> 25
city -> Pune
```

Note the brackets: `person[key]`, because `key` is a variable. That's the dot-vs-bracket rule in action.

The other common way is to turn the object into an array first, then loop with `for...of`:

```js
Object.keys(person);    // [ 'name', 'age', 'city' ]
Object.values(person);  // [ 'Asha', 25, 'Pune' ]
Object.entries(person); // [ [ 'name', 'Asha' ], [ 'age', 25 ], [ 'city', 'Pune' ] ]

for (const [key, value] of Object.entries(person)) {
  console.log(`${key}: ${value}`);
}
```

```text
name: Asha
age: 25
city: Pune
```

`Object.entries` gives each key with its value, which is usually what you want. Keys come back in the order they were added, with one exception: number-like keys are moved to the front and sorted, which I showed in [Map and Set explained](https://jaydeepkanzariya.hashnode.dev/why-obj-1-and-obj-1-are-the-same-key-map-and-set-explained).

## Arrays vs objects

Both store several values in one variable. The difference is how you find each value:

| | Array | Object |
|---|---|---|
| Values found by | Position (index: 0, 1, 2…) | Name (key: `name`, `age`…) |
| Written as | `["Asha", 24, "Pune"]` | `{ name: "Asha", age: 24, city: "Pune" }` |
| Order | The order is the point | Not what you rely on |
| Size | `arr.length` | `Object.keys(obj).length` |
| Best for | Lists of similar things: marks, tasks, fruits | One thing with named facts: a user, a product, a setting |

One confusing detail: arrays are a special kind of object, so `typeof` can't tell them apart:

```text
typeof []:                   object
typeof {}:                   object
Array.isArray([]) / ({}):    true false
```

Use `Array.isArray` when you need to know which one you have. (Arrays have their own post: [JavaScript Arrays 101](https://jaydeepkanzariya.hashnode.dev/javascript-arrays-101).)

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart TB
    subgraph A["Array: values by position"]
        A0["[0] → 'Asha'"]
        A1["[1] → 24"]
        A2["[2] → 'Pune'"]
    end
    subgraph O["Object: values by name"]
        O1["name → 'Asha'"]
        O2["age → 24"]
        O3["city → 'Pune'"]
    end
-->
![Array vs object: an array stores values by position, [0] 'Asha', [1] 24, [2] 'Pune'; an object stores the same values by name, name 'Asha', age 24, city 'Pune'](https://mermaid.ink/img/pako:eNp1kj1SwzAQha-i2SaNyVjyn6zOQMuYggorhWIrthlb8sgyxGTScgCOyEkYJYTJBLLd7r637yt2B6WuJDDYdPqtbISx6OmWG64QQmic1rURQ4OygkNmjJgZehXdJEe0ntGgx9a2WnFYnQyuMr_gUPgr9PXxiRbZ2IjFpQI7BT4qSHi5JW5LfvyPk5LnfqmqP3R5wSFfv8jSnuMp0cuL07kLdvPrbLlLF7X8ny0PCg5la-ercOBBbdoKmDWT9KCXpheuhZ2TcLCNdFgMcTCymrY3pe604cDVHjwYhHrWuj-5jZ7qBthGdKP0YBoqYeV9K2oj-t-pkaqS5k5PygIj8eEGsB1sgYWYLglN4xT7OE0CP_BgBoYJWYYkIgGliU-TNE32HrwfUv0liXEUUxxRGodpEnkgq9Zq83D8kcOr7L8BZ-isTQ?type=png)
*The same three values, found by position in an array and by name in an object.*

## Try it: the assignment

The brief's four steps in one script:

```js
// 1. An object representing a student
const student = {
  name: "Asha",
  age: 20,
  course: "Web Dev Cohort 2026",
};

// 2. Add a property
student.city = "Pune";

// 3. Update one property
student.age = 21;

// 4. Print all keys and values with a loop
for (const key in student) {
  console.log(`${key}: ${student[key]}`);
}
```

```text
name: Asha
age: 21
course: Web Dev Cohort 2026
city: Pune
```

`age` shows the updated value, and `city` appears last because it was added last.

The takeaway: **an object stores values by name instead of position. Use dot notation for keys you type and brackets for keys in a variable; assign to add or update, `delete` to remove, and `for...in` or `Object.entries` to loop.** This post skipped prototypes and methods on purpose. The natural next step is pulling values out in one line with [destructuring](https://jaydeepkanzariya.hashnode.dev/javascript-destructuring).

Without running it: if `const key = "age"`, what do `person.key` and `person[key]` each return, and why are they different?
