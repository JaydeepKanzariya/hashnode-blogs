---
title: "Why Your switch Runs Three Cases: break Explained"
slug: javascript-control-flow
subtitle: Control flow in JavaScript, from if and else to else if ladders and switch, with step-by-step traces and real output
tags: javascript, web-development, beginners, programming, tutorial
cover: ./cover.png
seoTitle: "JavaScript If, Else and Switch Explained for Beginners"
seoDescription: "Control flow in JavaScript: if, if-else, else if ladders and switch, why break matters, and when to pick switch over if-else, with real output."
enableToc: true
---

Leave `break` out of a `switch` and one match can print three lines instead of one. No error, no warning. It's the best way into **control flow**: the part of a language that decides which line runs next.

This post covers `if`, `if-else`, the `else if` ladder and `switch`, then when to pick which. Every output below is a real run on Node.js 24.22.1. The examples are small on purpose, and they use `const` and `let`; if those are new, start with [let, const or var?](https://jaydeepkanzariya.hashnode.dev/javascript-variables-data-types).

## What control flow means

You make decisions all day. If it's raining, you take an umbrella. If your marks are above 40, you pass. If the shop is closed, you go home.

Code does the same thing. By default JavaScript runs top to bottom, one line after another. **Control flow** is how a program decides what runs next. The most common kind is a decision: check a condition, run one block of code, skip another. (Loops are another kind of control flow; this post sticks to decisions.) Here's the shape every example in this post follows:

1. A condition is evaluated to `true` or `false`.
2. If it's `true`, the matching block runs.
3. If it's `false`, JavaScript skips the block and moves on.

## The if statement: run this only when the condition is true

```js
const age = 20;
console.log("start");
if (age >= 18) {
  console.log("You can vote.");
}
console.log("end");
```

```text
start
You can vote.
end
```

Step by step: `"start"` prints. JavaScript evaluates `age >= 18`, which is `20 >= 18`, so `true`. The block runs. Then execution continues after the closing brace and prints `"end"`.

Change `age` to `15` and the condition becomes `false`:

```text
start
end
```

The block is skipped, and the program carries on. An `if` on its own has nothing to say about the false case. That's what `else` is for.

## if-else: pick one of two paths

```js
const age = 15;
if (age >= 18) {
  console.log("Adult ticket");
} else {
  console.log("Child ticket");
}
```

```text
Child ticket
```

Exactly one block runs, never both and never neither. The condition `15 >= 18` is `false`, so JavaScript jumps to `else`.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart TD
    A([Start]) --&gt; B{"age >= 18?"}
    B -- true --&gt; C["Adult ticket"]
    B -- false --&gt; D["Child ticket"]
    C --&gt; E([Continue])
    D --&gt; E
-->
![Flowchart of if-else decision-making: the program starts, checks the condition age >= 18, prints Adult ticket if it is true or Child ticket if it is false, and both paths then rejoin and continue](https://mermaid.ink/img/pako:eNpl0U9rgzAYBvCvEp5TC1rUVk0C62h1x52204yHYFKVqSlZZN3E7z5qKWPs-PL83j_wTqiM0uA4deazaqR15DUXVgyEEHJYFS9OWleuie_vyXESkLUm-wcS0keB-e6OxPeJs6NeWFYIHNTYOeLa6l07gfIPPMnu4ybzQiBr2k79l9kCnlZFZgbXDqMu1_cov0XwUNtWgV8Xe-i17eW1xHRlAq7RvRbgRMBqNV78ynTGCohhhoezHN6M6e_d1ox1A76c5mE8K-l03srayl-iB6VtZsbBgbNlAviEC_gupJuIsoSFQcjSbbD18AUeRtFmF8XRltI0oClj6ezhe9kZbKIkjBMaxpQmO5bGHrRqnbHPt18sL5l_ACaHefk?type=png)
*One condition, two paths. Exactly one runs, then both rejoin.*

Both paths rejoin afterwards. That's the picture to keep in your head for everything else here: branches split, then merge.

## The else if ladder: more than two outcomes

Marks and grades are the classic case. Two paths aren't enough, so you chain conditions:

```js
const marks = 72;
if (marks >= 90) {
  console.log("Grade A");
} else if (marks >= 75) {
  console.log("Grade B");
} else if (marks >= 60) {
  console.log("Grade C");
} else if (marks >= 40) {
  console.log("Grade D");
} else {
  console.log("Fail");
}
```

```text
Grade C
```

JavaScript works down the ladder. `72 >= 90` is false, so it moves on. `72 >= 75` is false, so it moves on. `72 >= 60` is true, so it prints `Grade C` and **stops checking**. The `>= 40` test never runs, even though 72 satisfies it too.

That "first match wins" rule is where beginners get burned. Here's the same ladder with the broadest test first:

```js
// ❌ wrong order: the broadest test comes first
const marks = 95;
if (marks >= 40) {
  console.log("Grade D");
} else if (marks >= 60) {
  console.log("Grade C");
} else if (marks >= 90) {
  console.log("Grade A");
}
```

```text
Grade D
```

95 marks and a Grade D. Nothing is broken; the code did what it was told. `95 >= 40` is true, so the ladder ended on its first rung. Order ranged conditions from the most specific to the least.

## The switch statement: one value, many exact matches

Some decisions aren't ranges. They compare one value against a list of exact options: a day number, a menu choice, a status code. `switch` is built for that:

```js
const day = 3;
switch (day) {
  case 1:
    console.log("Monday");
    break;
  case 2:
    console.log("Tuesday");
    break;
  case 3:
    console.log("Wednesday");
    break;
  default:
    console.log("Some other day");
}
```

```text
Wednesday
```

JavaScript evaluates `day` once, then compares it against each `case` in order. `3` doesn't match `1` or `2`, matches `3`, and runs that block. `default` is the `else` of a switch: it runs when no case matches.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart TD
    A(["switch (day)"]) --&gt; B{"day value"}
    B -- "1" --&gt; C["Monday"]
    B -- "2" --&gt; D["Tuesday"]
    B -- "3" --&gt; E["Wednesday"]
    B -- "no match" --&gt; F["default"]
    C --&gt; G(["leave the switch<br/>(break, or the end of the switch)"])
    D --&gt; G
    E --&gt; G
    F --&gt; G
-->
![Switch-case branching diagram: switch (day) checks the day value; 1 leads to Monday, 2 to Tuesday, 3 to Wednesday and no match to default; every branch then leaves the switch, by break or at the end of the switch](https://mermaid.ink/img/pako:eNp1ks1u4kAQhF-lVSci2QTbgH8URUog2RM3pJXWncPE02AUeyYaxklYxLuvMLDKrpJjdX9drZJqj8pqQYFVY9-rWjlPyzk7NkREd4OSsX3f-KqmgVa7K8bTFYXhLd3vGVrt6E01nTAOl4t7CkNiRIwem5WMhTVa7RhP_zHxmZmXjGUn2y-h5Aw9lIyfos03mLHUKl_VZ_qxZGhZqa7xn9hZv_txzNSIehPytdAp3c2zu74dPDtRLwFZ12_EaLKrT1Cf_mI2P5ld5MO_8vEkEWDtNhqFd50EaMW16iixP2IMX0srjIIYTnT3EVa2sY7B5oAAr8r8sra9XDvbrWsUK9VsJUD3qpWX-UatnWr_Tp0YLW5mO-NRREnvgWKPDxTjKBvGWT7No1GUp8koCbBDEcXxcBxP4iTL0lGW5nl6CPC7_zoaxtNoMs2iSZZNx3k6CSB6461bnArT9-bwB3s_qBc?type=png)
*A switch jumps straight to the matching case. break, or the end of the switch, is the way out.*

## What break does, and what happens without it

`break` means "leave the switch now". Without it, JavaScript doesn't stop at the matching case. It runs that case and then **every case below it**, ignoring whether they match. This is called fall-through.

```js
// ❌ no break statements
const day = 2;
switch (day) {
  case 1:
    console.log("Monday");
  case 2:
    console.log("Tuesday");
  case 3:
    console.log("Wednesday");
  default:
    console.log("Some other day");
}
```

```text
Tuesday
Wednesday
Some other day
```

`day` is `2`, and three lines print. JavaScript jumped to `case 2`, then kept going down through `case 3` and `default`. The `case` labels only decide where to **enter**. Only `break` (or `return`) decides where to leave.

Fall-through isn't always a bug. Stacking cases with no code between them lets several values share one result:

```js
const day = 6;
switch (day) {
  case 6:
  case 7:
    console.log("Weekend");
    break;
  default:
    console.log("Weekday");
}
```

```text
Weekend
```

If you do this on purpose, leave a comment saying so. The next reader will assume you forgot a `break`.

## switch vs if-else: how to choose

My rule: **use `switch` when you compare one value against fixed, exact options. Use `if-else` for everything else.**

| Situation | Use | Why |
|---|---|---|
| Day number → day name | `switch` | One value, exact matches |
| Menu option 1 to 5 | `switch` | One value, exact matches |
| Marks → grade | `if-else if` | Ranges, not exact values |
| Age ≥ 18 and has ID | `if-else` | Combines several conditions |
| Two outcomes (pass/fail) | `if-else` | `switch` is overkill |

`switch` is awkward for ranges. This looks plausible and quietly fails:

```js
// ❌ switch compares with ===, so a ranged test never matches
const marks = 85;
switch (marks) {
  case marks >= 75:
    console.log("Grade B");
    break;
  default:
    console.log("No match");
}
```

```text
No match
```

`marks >= 75` evaluates to `true`, and `switch` then checks whether `85 === true`. It isn't.

There is a workaround, `switch (true)`. Each `case` becomes a comparison that gives `true` or `false`, so `true === true` can match:

```js
const marks = 85;
switch (true) {
  case marks >= 90:
    console.log("Grade A");
    break;
  case marks >= 75:
    console.log("Grade B");
    break;
  default:
    console.log("Below B");
}
```

```text
Grade B
```

It works, but it reads worse than an `if` ladder, and the first matching case still wins, so the order matters just as much. I'd use the ladder.

Also, `switch` uses strict equality (the same `===` I covered in [Why "5" + 3 Is "53"](https://jaydeepkanzariya.hashnode.dev/javascript-operators-basics)), so the string `"3"` doesn't match `case 3`:

```js
const input = "3";
switch (input) {
  case 3:
    console.log("number three");
    break;
  default:
    console.log("string \"3\" is not the number 3");
}
```

```text
string "3" is not the number 3
```

Values from forms and prompts arrive as strings. Convert them first, or your cases won't match.

## The assignment, solved

**1. Positive, negative or zero.** Three outcomes decided by comparisons, so this is an `if / else if / else`:

```js
function sign(n) {
  if (n > 0) {
    return "positive";
  } else if (n < 0) {
    return "negative";
  } else {
    return "zero";
  }
}
for (const n of [7, -3, 0]) console.log(n, "is", sign(n));
```

```text
7 is positive
-3 is negative
0 is zero
```

I used `if-else` because the checks are comparisons (`> 0`, `< 0`), and `switch` can't express those. The final `else` handles zero without a third test: if it's neither positive nor negative, it has to be zero.

**2. Day of the week.** One number, seven exact values, so `switch`:

```js
function dayName(n) {
  switch (n) {
    case 1: return "Monday";
    case 2: return "Tuesday";
    case 3: return "Wednesday";
    case 4: return "Thursday";
    case 5: return "Friday";
    case 6: return "Saturday";
    case 7: return "Sunday";
    default: return "Invalid day number";
  }
}
for (const n of [1, 5, 7, 9]) console.log(n, "->", dayName(n));
```

```text
1 -> Monday
5 -> Friday
7 -> Sunday
9 -> Invalid day number
```

Here `return` does the job of `break`, since it leaves the function and the switch with it. Seven `else if` rungs would work too, but they'd repeat `day ===` seven times. The `switch` states the comparison once. `default` catches `9`, which is the case you'd forget to handle with a ladder.

## Where this leaves you

`if-else` handles any condition. `switch` handles one value against exact options, and it needs `break` to behave. Both are easy to get wrong in quiet ways: a ladder in the wrong order, a case missing its `break`.

One limit of this post: I kept every example flat. Real code nests `if` inside `if`, and past two levels it gets hard to read. I haven't covered the usual fixes (early returns, lookup objects) here.

What's your rule for nesting: at which depth do you stop and restructure?
