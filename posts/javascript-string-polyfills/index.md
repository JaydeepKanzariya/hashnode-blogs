---
title: "JavaScript String Methods From Scratch, Tested Against the Real Thing"
slug: javascript-string-polyfills
subtitle: How string methods work, why polyfills exist, rebuilding includes, repeat and trim with tests against the built-ins, and common interview problems
tags: javascript, web-development, beginners, programming, interview
cover: ./cover.png
seoTitle: "String Polyfills and Interview Methods in JavaScript"
seoDescription: "Build JavaScript string polyfills for includes, repeat and trim, test them against the built-ins, and solve common interview string problems."
enableToc: true
---

Here's a homemade version of `includes`, the method that checks whether one string contains another:

```js
function includesV1(str, search) {
  for (let i = 0; i < str.length; i++) {
    if (str.slice(i, i + search.length) === search) return true;
  }
  return false;
}

console.log(includesV1("hello world", "world")); // true
console.log(includesV1("hello", "xyz"));         // false
```

It looks right, and it works on the obvious inputs. So I ran it against the real `"...".includes()` on nine inputs, including a few less obvious ones. It matched on **five**. The other four are exactly the cases an interviewer asks about next.

That gap is what this post is about. Writing a string method that handles the easy case takes a minute. Matching the built-in on the edge cases is the actual skill, and it's the clearest way to understand how the built-ins really behave. Below: what string methods are, why polyfills exist, three methods rebuilt and **tested against the real thing**, then the string problems interviews keep asking. Every output is real, from Node.js 24.22.

## What string methods are

Every string in JavaScript can call methods like `includes`, `slice`, `toUpperCase` and `trim`. They live on `String.prototype`, a shared object every string looks up methods on, which is why `"hello".toUpperCase()` works without you defining anything.

One rule shapes all of them: **strings can't be changed**.

```js
let s = "hello";
s[0] = "J";
console.log(s);               // hello
console.log(s.toUpperCase()); // HELLO
console.log(s);               // hello
```

Assigning to `s[0]` silently did nothing, and `toUpperCase()` returned a *new* string while `s` stayed `"hello"`. Every string method works this way: it returns a new string and leaves the original alone. Keep that in mind for the interview problems below, because "modify the string in place" isn't possible. You always build a new one.

## Why developers write polyfills

A **polyfill** is code that adds a built-in feature to an environment that doesn't have it yet. Newer methods like `replaceAll` or `at` don't exist in older browsers. A polyfill checks whether the method is there and, only if it's missing, installs a version written in plain JavaScript.

How you install it matters. Here's the naive way, adding a method by plain assignment (I used the name `myIncludes`, so the real `includes` is left alone):

```js
// ❌ Plain assignment: the new method shows up in for...in loops
String.prototype.myIncludes = function (search, position) {
  return includes(this, search, position);
};
const keysA = [];
for (const k in "hi") keysA.push(k);
console.log("after plain assignment:", keysA);
delete String.prototype.myIncludes;

// ✅ How real polyfills install: only if missing, and not enumerable
if (!String.prototype.myIncludes) {
  Object.defineProperty(String.prototype, "myIncludes", {
    value: function (search, position) {
      return includes(this, search, position);
    },
    writable: true,
    configurable: true,
    enumerable: false,
  });
}
const keysB = [];
for (const k in "hi") keysB.push(k);
console.log("after defineProperty:  ", keysB);
console.log("hello world".myIncludes("world"));
```

```text
after plain assignment: [ '0', '1', 'myIncludes' ]
after defineProperty:   [ '0', '1' ]
true
```

Plain assignment made `myIncludes` show up when looping over a string with `for...in`, next to the real indexes `0` and `1`. That can break other code that loops over properties. Real polyfills install with `Object.defineProperty` and `enumerable: false`, and only when the method is missing, which is the `if` guard.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart TB
    S["Page or script loads"] --&gt; Q{"Does String.prototype.method exist?"}
    Q --&gt;|"yes (modern engine)"| N["Use the built-in<br/>the polyfill does nothing"]
    Q --&gt;|"no (older engine)"| P["Install the polyfill<br/>defineProperty, not enumerable"]
    N --&gt; C["Your code calls str.method()"]
    P --&gt; C
-->
![Polyfill behaviour: when the page or script loads, it checks whether String.prototype has the method; if yes, in a modern engine, the built-in is used and the polyfill does nothing; if no, in an older engine, the polyfill is installed with defineProperty as non-enumerable; either way your code then calls str.method()](https://mermaid.ink/img/pako:eNpdks1r20AQxf-VYU4OyIolf-iDkkKTSw8NDmkPjTeHtXcsLax2xOyK2nX8vxc5TTE9zmPe7_GGOeGODWGNe8e_dq2WCN-_KFEeAOB5o3CtGwIWCDuxfQTH2gSFrzCd3sHTSeEDU4DnKNY3aS8cOR57SjuKLRuggw3xs8LzB_Fp9L0pPFKASceGxAP5xnq6UfgGjxuFPwJBbAm2g3Vxav2nrdzejULP7ri3zoEZIz3H1vpG4ev_bM8wYWdIrsnrjcKvPkTtHFzDLnRDe-tpLdyTxGMysoH80JHoraOriMdL7fuNwp88CIyng512LkCI8rf05ObKsH43YIKNWIN1lIES7Eg6PY54GtcUxpY6UliDQiEzHKY7diwKlT9jgr32L8zdh1t4aFqs99oFSnDojY70YHUjuvunCnlDcs-Dj1jPZxcG1ic8YL3IyjQvq1WVzbKqmM_mCR6xzvI8XeTLfF6Wxawsqqo4J_j7kjpL81W2XJXZsixXi6pYJkjGRpZv759zeaDzH4FWu8U?type=png)
*A polyfill only steps in when the method is missing. In a modern engine, it does nothing.*

In your own application code, **don't add methods to built-in prototypes**. If a future version of JavaScript adds a method with the same name but different behaviour, your version and the real one collide. This has happened: a popular old library, MooTools, added its own `Array.prototype.flatten`, and the standard method had to be named `flat` instead so existing sites wouldn't break. When you need a polyfill in a real project, use a maintained library such as core-js, which already handles the edge cases.

So why write polyfills at all? Because rebuilding a method is the fastest way to learn exactly what it does, and it's a standard interview question.

## Testing a polyfill against the real thing

To find the edge cases, I used a small helper. It runs the same inputs through the built-in method and through our version, and compares the results, including any error thrown:

```js
// Run the same inputs through the built-in and our version; compare results or errors
function compare(name, builtin, ours, cases) {
  const run = (fn, args) => {
    try { return JSON.stringify(fn(...args)); }
    catch (e) { return `${e.name}: ${e.message}`; }
  };
  const show = (v) => String(v).replace(/\u00A0/g, "\\u00A0");
  let pass = 0;
  for (const args of cases) {
    const want = run(builtin, args);
    const got = run(ours, args);
    if (want === got) pass++;
    else {
      const shown = args.map((a) => show(typeof a === "string" ? JSON.stringify(a) : a)).join(", ");
      console.log(`  ✗ ${name}(${shown}): built-in ${show(want)}, ours ${show(got)}`);
    }
  }
  console.log(`${name}: ${pass}/${cases.length} match the built-in`);
}
```

Now each polyfill gets a score.

## includes: four edge cases the first try missed

Here's how `includesV1` from the top scored on nine inputs:

```js
const includesCases = [
  ["hello world", "world"], ["hello", "xyz"], ["hello", ""], ["", ""], ["hi", "hi there"],
  ["hello", "l", 3], ["hello", "h", 1], ["12345", 3], ["abc", /a/],
];
compare("includesV1", (s, ...a) => s.includes(...a), includesV1, includesCases);
```

```text
  ✗ includesV1("", ""): built-in true, ours false
  ✗ includesV1("hello", "h", 1): built-in false, ours true
  ✗ includesV1("12345", 3): built-in true, ours false
  ✗ includesV1("abc", /a/): built-in TypeError: First argument to String.prototype.includes must not be a regular expression, ours false
includesV1: 5/9 match the built-in
```

Four misses, each one a rule the built-in follows:

- **An empty search string is always found**, even in an empty string. The loop never ran for `""`, so it returned `false`.
- **The second argument is a starting position.** `"hello".includes("h", 1)` starts looking at index 1, so there's no `"h"` to find. `includesV1` ignored it.
- **Non-strings are converted.** `includes(3)` searches for `"3"`. `includesV1` tried to read `.length` of a number.
- **Regular expressions are rejected** with a `TypeError`, rather than silently returning `false`.

The fixed version handles all four:

```js
function includes(str, search, position = 0) {
  if (search instanceof RegExp) {
    throw new TypeError("First argument to String.prototype.includes must not be a regular expression");
  }
  str = String(str);
  search = String(search);
  const start = Math.min(Math.max(Math.trunc(position) || 0, 0), str.length);
  for (let i = start; i <= str.length - search.length; i++) {
    if (str.slice(i, i + search.length) === search) return true;
  }
  return false;
}

compare("includes", (s, ...a) => s.includes(...a), includes, includesCases);
```

```text
includes: 9/9 match the built-in
```

## repeat: when the edge case is a crash

`repeat(n)` joins `n` copies of a string. The obvious version:

```js
function repeatV1(str, count) {
  let out = "";
  for (let i = 0; i < count; i++) out += str;
  return out;
}

const repeatCases = [["ab", 3], ["ab", 0], ["ab", 2.7], ["ab", -1], ["", 5], ["ab", "2"], ["ab", NaN]];
compare("repeatV1", (s, c) => s.repeat(c), repeatV1, repeatCases);
```

```text
  ✗ repeatV1("ab", 2.7): built-in "abab", ours "ababab"
  ✗ repeatV1("ab", -1): built-in RangeError: Invalid count value: -1, ours ""
repeatV1: 5/7 match the built-in
```

Two misses. `2.7` should be **truncated** to 2 (the loop ran 3 times, for i = 0, 1, 2), and a negative count should **throw**, not return an empty string.

The case I left out of that list is worse. `repeatV1("ab", Infinity)` never returns: the loop keeps adding `"ab"` forever, and when I ran it, Node ran out of memory at about 4 GB, roughly a minute in, and the process crashed. The built-in throws `RangeError: Invalid count value: Infinity` straight away. That's the difference between a toy and a method you can ship: **validate first, then do the work.**

```js
function repeat(str, count) {
  str = String(str);
  const n = Math.trunc(Number(count)) || 0;
  if (n < 0 || n === Infinity) throw new RangeError(`Invalid count value: ${count}`);
  if (str === "" || n === 0) return "";
  let out = "";
  for (let i = 0; i < n; i++) out += str;
  return out;
}

compare("repeat", (s, c) => s.repeat(c), repeat, [...repeatCases, ["ab", Infinity]]);
```

```text
repeat: 8/8 match the built-in
```

## trim: whitespace is more than spaces

`trim()` removes whitespace from both ends. A first try that only removes spaces:

```js
const trimV1 = (str) => str.replace(/^ +| +$/g, "");        // spaces only
const trim = (str) => String(str).replace(/^\s+|\s+$/g, ""); // any whitespace

const trimCases = [["  hi  "], ["\t hi \n"], ["\u00A0hi\u00A0"], ["hi"], [""], ["   "], ["a  b"]];
compare("trimV1", (s) => s.trim(), trimV1, trimCases);
compare("trim", (s) => s.trim(), trim, trimCases);
```

```text
  ✗ trimV1("\t hi \n"): built-in "hi", ours "\t hi \n"
  ✗ trimV1("\u00A0hi\u00A0"): built-in "hi", ours "\u00A0hi\u00A0"
trimV1: 5/7 match the built-in
trim: 7/7 match the built-in
```

Tabs, newlines and non-breaking spaces (`\u00A0`, common in text pasted from web pages) are whitespace too. The regex `\s` matches the same whitespace characters `trim` removes, so switching to `/^\s+|\s+$/g` passed all seven cases.

One honest limit: "matches on every case I tested" isn't the same as "matches the specification". Called on `null`, the built-in throws `TypeError: String.prototype.includes called on null or undefined`, while my `includes(null, "nu")` returned `true`, because `String(null)` is `"null"`. The language specification defines dozens of rules like that for each method. That's why production code relies on the built-ins, or on a maintained polyfill library, rather than hand-written versions.

## Common interview string problems

These come up again and again, and each one leans on the ideas above. Strings are immutable, so you build new ones; and characters aren't always what they seem.

### Reverse a string

The classic one-liner splits into characters, reverses, and joins:

```js
const reverseNaive = (str) => str.split("").reverse().join("");
const reverse = (str) => [...str].reverse().join("");
const reverseGraphemes = (str) =>
  [...new Intl.Segmenter().segment(str)].map((part) => part.segment).reverse().join("");

console.log(reverseNaive("hello"));                // olleh
console.log(JSON.stringify(reverseNaive("hi 😀")));
console.log(reverse("hi 😀"));
console.log("😀".length, [..."😀"].length);
console.log(reverse("hi 👨‍👩‍👧"));
console.log(reverseGraphemes("hi 👨‍👩‍👧"));
```

```text
olleh
"\ude00\ud83d ih"
😀 ih
2 1
👧‍👩‍👨 ih
👨‍👩‍👧 ih
```

It reverses `"hello"` fine, and **breaks emoji**. `"😀"` has a `.length` of **2**, because JavaScript stores it as two code units, and `split("")` splits it into two halves. Reversed, they no longer form an emoji: you get `"\ude00\ud83d"`, two broken characters. Spreading with `[...str]` splits by whole code points instead, so the emoji stays in one piece. (More on the spread operator in [Same Three Dots, Opposite Jobs](https://jaydeepkanzariya.hashnode.dev/same-three-dots-opposite-jobs-spread-vs-rest-in-javascript).)

It still isn't the whole story. The family emoji `👨‍👩‍👧` is several emoji glued together, and `[...str]` reversed its parts into a different family. `Intl.Segmenter`, built into modern JavaScript, splits text the way a person reads it, and kept the family intact. Mentioning this in an interview shows you know strings aren't just arrays of letters.

### Palindrome check

A palindrome reads the same backwards. Normalise first, so case, spaces and punctuation don't count. (The `[^a-z0-9]` filter keeps only unaccented English letters and digits, which suits interview questions; real text in other languages needs a Unicode-aware filter.)

```js
function isPalindrome(str) {
  const clean = str.toLowerCase().replace(/[^a-z0-9]/g, "");
  return clean === [...clean].reverse().join("");
}

console.log(isPalindrome("A man, a plan, a canal: Panama")); // true
console.log(isPalindrome("hello"));                          // false
```

### Anagram check

Two strings are anagrams if they use the same letters the same number of times. Counting is the reliable way:

```js
function isAnagram(a, b) {
  const clean = (s) => s.toLowerCase().replace(/[^a-z0-9]/g, "");
  a = clean(a);
  b = clean(b);
  if (a.length !== b.length) return false;
  const counts = {};
  for (const ch of a) counts[ch] = (counts[ch] ?? 0) + 1;
  for (const ch of b) {
    if (!counts[ch]) return false;
    counts[ch]--;
  }
  return true;
}

console.log(isAnagram("listen", "silent"));        // true
console.log(isAnagram("Dormitory", "dirty room")); // true
console.log(isAnagram("rat", "car"));              // false
```

The length check returns early for obvious mismatches. Counting visits each character a fixed number of times, so the work grows in step with the input, while sorting both strings grows a little faster than that. That's a point worth saying out loud in an interview.

### Character count and first non-repeating character

Count every character in one pass, then find the first one that appears once:

```js
function charCount(str) {
  const counts = new Map();
  for (const ch of str) counts.set(ch, (counts.get(ch) ?? 0) + 1);
  return counts;
}

function firstUnique(str) {
  const counts = charCount(str);
  for (const ch of str) if (counts.get(ch) === 1) return ch;
  return null;
}

console.log(charCount("swiss"));   // Map(3) { 's' => 3, 'w' => 1, 'i' => 1 }
console.log(firstUnique("swiss")); // w
console.log(firstUnique("aabb"));  // null
```

`for...of` steps through whole code points, like `[...str]`, so this works with simple emoji like 😀. Joined ones like 👨‍👩‍👧 would still be counted in parts.

### Capitalise each word

```js
const capitalizeWords = (str) =>
  str
    .split(" ")
    .map((word) => (word ? word[0].toUpperCase() + word.slice(1).toLowerCase() : word))
    .join(" ");

console.log(JSON.stringify(capitalizeWords("hello wORLD from  js")));
```

```text
"Hello World From  Js"
```

Splitting on single spaces keeps the double space in `"from  js"` intact, and the `word ?` check skips the empty string between those spaces, so `word[0]` never fails.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    I["Input string"] --&gt; N["Normalise<br/>lowercase, strip spaces and punctuation"]
    N --&gt; C["Split into characters<br/>[...str] or a for...of loop"]
    C --&gt; P["Process<br/>reverse, count, compare"]
    P --&gt; J["Join, or return a result"]
-->
![String processing flow: the input string is normalised (lowercase, spaces and punctuation stripped), split into characters with [...str] or a for...of loop, processed (reversed, counted or compared), then joined or turned into a result](https://mermaid.ink/img/pako:eNpNkUtv4zAMhP8KwbOjxs7DDxS9pJcWbRDs3tbKQSsziQBbNChp222Q_76wiy56Ikhwvhlgrmi5I2zw1PObvRiJ8PJDi_YAAE-txic_pgghivNnjUdYLB5g32rcswymd4Huf8vdQ89vJNYEyubXEcJoLAUwvoMxeRuTiY69xuMXez-Tdq3Gn2PvIjgfGaYAxkaSMFNbpVSIcgQWMHBiUUrxCXrm8RtpN5MOrcaDsKXwqRX6QzLlsZx8nMYwGqFvusOse241PrPz2WQiFJN4MCAUUh81HjHDs7gOmyiJMhxIBjOteJ0gGuOFBtLYgEahLr0vLPcsGrW_YYaj8b-Yhy-1cDpfsDmZPlCGaexMpEdnzmKG_1ch35HsptDYrNYzA5srvmOzzitVVPW2zpd5Xa6Wqwz_YpMXhVoXm2JVVeWyKuu6vGX4MbsuVbHNN9sq31TVdl2Xmwypc5Hl9bPzufrbP2iQo2Y?type=png)
*Most string interview problems follow these four steps.*

## Why understanding built-in behaviour matters

Every polyfill above passed the obvious case on the first try and failed somewhere else: empty strings, positions, numbers passed as strings, `Infinity`, non-breaking spaces, emoji. That's where real bugs come from, and it's exactly what interviewers probe after you write the happy path.

So the useful habit isn't memorising implementations. It's asking, for any method: **what happens with an empty string? A negative or huge number? A non-string argument? Characters outside basic English?** Then test those cases against the real method, the way the `compare` helper does. Your answer is right when it agrees with the built-in, not when it agrees with your first example.

The takeaway: **string methods return new strings and never change the original; a polyfill installs a missing method safely (only if missing, not enumerable); and rebuilding one teaches you its edge cases faster than reading about them.** In real projects, use the built-ins or a maintained polyfill library rather than your own. Write them to learn, test them to be sure.

Pick a string method you use often, like `slice`, `padStart` or `split`, and write your own version. How many edge cases does it miss on its first run against the real one?
