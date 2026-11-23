---
title: "The Virtual DOM isn't faster than the DOM — here's what it buys you"
slug: virtual-dom-reconciliation-rendering
subtitle: What actually happens when you call setState, from re-render to reconciliation, commit and paint, with real React 19 output
tags: react, javascript, web-development, frontend, beginners
cover: ./cover.png
seoTitle: "How React Works: Virtual DOM, Reconciliation, Render"
seoDescription: "How React works internally: the virtual DOM, re-renders, reconciliation, render vs commit, keys and memo, from setState to pixels on screen."
enableToc: true
---

What actually happens when you call `setState`? Here's a small counter: a heading, a paragraph that says how many times you clicked, and a button. I rendered it with React 19.3.1, clicked the button once, and recorded every change React made to the real DOM with a `MutationObserver`:

```text
DOM after click: <div><h1>Score board</h1><p>Clicked 1 times</p><button>Add one</button></div>
mutations: 1
 - characterData #text "0" -> "1"
```

One change. Not "re-render the component", not "replace the paragraph". React found the one text node that said `0` and changed it to `1`. Everything else in the DOM was left alone.

How React got from "the state changed" to "change exactly that text node" is the whole story of the virtual DOM, re-rendering, reconciliation and the commit phase. It's also where the most common myth comes from: that the virtual DOM is *faster* than the DOM. It isn't. React still makes that DOM change at the end, just as hand-written code would. What the virtual DOM buys you is something else, and it's worth more.

All the demos in this post ran on React 19.3.1 with `react-dom` in Node, using jsdom as the DOM. The outputs are real, trimmed where noted.

## Why React needed a different way to render

Before React, the usual way to update a page was by hand: find the element, change it.

```js
// ❌ Fine for one counter. Painful for a whole app.
button.addEventListener("click", () => {
  count++;
  label.textContent = `Clicked ${count} times`;
  if (count > 10) badge.classList.add("hot");
  cartIcon.dataset.count = count;
});
```

Every event handler has to know every piece of the page it affects. Add a feature and you're hunting for every place that should change. Miss one and the UI shows stale data. As apps grew to hundreds of interactive pieces, keeping the DOM in sync with the data became the main source of bugs.

React's answer was to flip the model. You don't write *how* to change the page. You write *what the page should look like* for the current data, and React works out the changes. That makes React less a component library and more a **UI engine**: you describe; it updates.

## The real DOM, and why touching it costs something

The **DOM** is the browser's live tree of your page: one object per element, text node and attribute. JavaScript reads and changes it, and the browser redraws to match.

Changing it isn't free. Changing an element can force the browser to recalculate layout, where every box sits and how big it is (a **reflow**), and to redraw pixels (a **repaint**). One change is cheap. Thousands of uncoordinated changes, or code that alternates between reading layout and writing to the DOM, can make a page stutter. I walked through layout and paint in more detail in [how a browser works](https://jaydeepkanzariya.hashnode.dev/how-a-browser-works-from-pressing-enter-to-pixels-on-screen).

So the goal for any UI approach is the same: touch the DOM as little as possible, in as few batches as possible.

## The virtual DOM is just objects

"Virtual DOM" sounds like a second browser. It's plain JavaScript objects describing what the UI should be. Here's what JSX produces, printed straight from React (dev-only fields trimmed):

```jsx
const el = <p className="note">Clicked {0} times</p>;
```

```text
{
  type: 'p',
  props: { className: 'note', children: [ 'Clicked ', 0, ' times' ] },
  key: null
}
```

That's a **React element**: a type, some props, and children. A tree of these is what people call the virtual DOM. Creating one is creating a few small objects, which is far cheaper than creating real DOM nodes.

| | Real DOM | Virtual DOM (React elements) |
|---|---|---|
| What it is | The browser's live page tree | Plain JavaScript objects |
| Who owns it | The browser | React |
| Changing it | Can trigger layout and paint | Only creates new objects |
| Shown on screen | Yes | Never directly |

![Real DOM vs virtual DOM: on the left, a virtual DOM of plain objects, a div object with h1 and p children; on the right, the matching real browser DOM with div, h1 and p elements; React keeps the two in sync](https://mermaid.ink/img/pako:eNplkj1v2zAQhv_K4Ya4BWRHlD8kMUCXeMjQoIEGDTUz0OJFYiKRAkUlcR3_90L-QG2XG--e9-UzcIuFVYQcX2r7UVTSefiZCScMAEDXr0sn2wrylcBcO9_LGpa_HuGbXb9S4bvvAp9P8HDy5UrgFvymJQ4jpd9HsBP4DOPxD8gfzncVO6wu0wfw6RxsRwEUla6VI8NhdF_r4o0UhOB1Q91lCRn1n3q2EpjRyXvt7EdH7to7G7xvan-n9PtN6e9OztnDcV6x4_gydYCejlA7MFeCw_y2vQqfeeZDxVdGsvDwRtR24CtqQBvoNqb4ggwDLJ1WyL3rKcCGXCOHK26HAoEDTgI5CHSk-s9xYWvrBAqzwwBbaX5b25zSzvZlhfxF1h0F2LdKelpqWTr5DyGjyN3b3njkbLavQL7FT-QzlkyiJF2kLGRpPA2nAW6QsyiazKJ5NE2SOEziNI13Af7ZPxpOogWbLxI2T5LFLI3nAZLS3rrHw5_bf73dX_5CwXg?type=png)
*The virtual DOM is a cheap description. The real DOM is what the browser draws.*

## First render: from JSX to pixels

Take a button component:

```jsx
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>Clicked {count} times</button>;
}
```

Browsers don't understand JSX. A build tool rewrites it first. Here's what esbuild 0.28 actually turned that `return` line into:

```js
return jsxs("button", { onClick: () => setCount(count + 1), children: [
  "Clicked ",
  count,
  " times"
] });
```

A function call that returns an element object. (Older setups produce `React.createElement("button", …)` instead; same idea.) On the first render:

1. React calls your component function.
2. It returns a tree of elements: the virtual DOM.
3. React creates real DOM nodes to match and inserts them into the page.
4. The browser lays out and paints.

![Initial render lifecycle: a build tool turns JSX into jsx() calls; the component runs and returns an element tree, the virtual DOM; React creates real DOM nodes from it; the browser paints](https://mermaid.ink/img/pako:eNpNkU9rwkAQxb_KMCeFaE38k00oHmq8SKXFXkqzHtZk1JTNbphsqq363UuUFo_z-L33Bt4JM5sTxrjV9pDtFTt4XkmWBgBgkUpcvL1LXEOvNz1vmkLn4KzVZ5ilEj_rY6cLmdK6lrj-M82ubGbLyhoyDrgx9RnmqcS5prJVHBM9bvhh2vkq2DVKQ_Ky7N5FzG8RTMoRGJtTfYYklbiiG3uHJi0Kr6nEJ7aHmhgqVRjXPoQe7rjIMXbckIclcanaE0-tVaLbU0kSY5DIlDfHXma1ZYnSXNDDSpkPa8s_N9tmt8d4q3RNHjZVrhwlhdqxKv9VJpMTz2xjHMa-uGZgfMIjxiNf9AMRTSJ_4EfhcDD08BtjPwj6o2AcDIUIByKMovDi4c-1ddAPJv54IvyxEJNRFI49pLxwlpe3ua6rXX4BvuOKuQ?type=png)
*First render: JSX becomes function calls, function calls become objects, objects become DOM nodes.*

## When state changes

Calling `setCount(1)` doesn't change anything on the spot. It tells React "this component's state changed; render it again". React batches updates that happen together, then:

1. **Calls the component function again** with the new state. That's what a **re-render** is: your function running, nothing more.
2. Gets back a **new element tree** describing what the UI should be now.
3. **Compares** it with the previous tree.
4. **Applies** only the differences to the real DOM.

That's the most useful thing to know for interviews and debugging: **a re-render is not a DOM update.** Your component can re-render and produce exactly the same output, in which case React changes nothing in the DOM. It's also why hooks work the way they do. `useState` hands each new call of your function the latest value, because the function is called fresh every time.

## Reconciliation: comparing the old tree with the new

**Reconciliation** is step 3: React comparing the previous element tree with the new one to work out what changed. In the counter, the trees differ in exactly one place:

![Old virtual DOM vs new virtual DOM: both trees have a div containing an h1 Score board, a p and a button Add one; the only difference is the p text, Clicked 0 times in the old tree and Clicked 1 times in the new tree](https://mermaid.ink/img/pako:eNqN0s1O6zAQBeBXGc06qWKnbRIvkPjZkizuXRGzcONpE5HY1dShQOm7X7VVr1ABgXdjnWN_i9lh4y2hwmXvt01rOMDfG83aAQBsxsWKzbqFqre1xqq3EJhI4-M5cTiVqDXa7lnjI8TxFVSy1tgKBX8azwQLb9h-qpySaa1xreC275onspBA6AbafBOe1hoXYwjeKbi2Frz7KCFnP7FL2tYaS9p-xS4v2OXP7PIkKS_Y4kv2OfxrdpVCPImv3r3rX8F2yyUxuYbeoUwxwhV3FlXgkSIciAdzGHF3qGoMLQ2kUYFGJju-xI3vPWvUbo8Rro178H44t9mPqxbV0vQbinBcWxPorjMrNsP_WyZniW_96AIqKY9voNrhC6qpyCcyL-aFSESRpUka4SsqIeVkKmcyzfMsybOiyPYRvh1_TSZyLmbzXMzyfD4tslmEZLvg-f60eccF3P8DKaC_4Q?type=png)
*Two whole trees, one difference. That one difference is all React commits.*

Why compare trees at all, instead of updating the DOM directly? Because the comparison is between cheap objects, and it lets you write the simple version, "here's the whole UI for the current state", without React rebuilding the whole page each time. The result is the single text-node change from the top of this post.

## The diffing rules

A perfect comparison of two arbitrary trees is expensive. React uses a few simple rules instead, described in its [reconciliation docs](https://legacy.reactjs.org/docs/reconciliation.html):

1. **Different type, replace it.** If a `<div>` becomes a `<section>`, or `<Profile>` becomes `<Settings>`, React throws away the old subtree, state included, and builds the new one.
2. **Same element type, update it.** If it's still a `<p>`, React keeps the DOM node and changes only the props or text that differ.
3. **Same component type, keep it.** If it's still `<Counter>`, React keeps the component and its state, and renders it with the new props.
4. **Children are matched in order, or by key.** For lists, `key` tells React which old child is which new child.

Rule 1 has a practical consequence. Conditionally wrapping something in a different element, say `<div>` one moment and `<span>` the next, resets all state inside it. That surprises people.

## Render phase vs commit phase

React splits each update into two phases:

- **Render phase**: call components, build the new tree, reconcile. This is pure calculation. Nothing on screen changes, and React can pause or throw the work away and start again.
- **Commit phase**: apply the changes to the real DOM, all at once. Then the browser paints, and your effects (`useEffect`) run afterwards.

React's own docs describe it as [trigger, render, commit](https://react.dev/learn/render-and-commit). The split exists so the DOM is never left half-updated: you see either the old UI or the new one, never a mix. It's also why component functions must be pure. React may call them in the render phase without ever committing the result.

![Render phase to commit phase: setState triggers the render phase, which calls components and builds and compares trees; the commit phase applies DOM changes; the browser paints; then effects run](https://mermaid.ink/img/pako:eNpVkU9vgkAQxb_KZq5FCyiwkMZD0VtNDfVU1sMKw58EdsmwRK3xuzdu08Ye5-X93kzmXaHQJUICVadPRSPJsLdMkFCMMbbPBeyprWuklyM9r0Y0H0YaFHBgs9mKZbmADFWJxIZGjmhNhew6Vuh-0AqVGa12nNquZE9WloTMEOIo4PC7KLNxaS4g1X3fmoc4OQzdha3ft6xopKr_YanFdrmAV9Kn8X6GbJV5tOysZZML2FQVFmZkNCkBB3CgpraExNCEDvRIvbyPcL1zAkyDPQpImADCcjrPCt1pEiDUDRwYpPrUuv-lSU91A0kluxEdmIZSGly3sibZ_6lk_5TqSRlI_NBmQHKFMyRLj899Hoex53pxtHAXDlwg8Xx_vvQDf8F55PIojqObA192qzv3Qy8IuRdwHi7jKHAAy9Zo2v50aSu9fQOgUZUp?type=png)
*All the work happens in the render phase. The DOM only changes in the commit.*

## Keys and lists

For lists, rule 4 matters most. Here's a list of people, each with a text input. I typed "note for Asha" into Asha's row, then added Meera at the **top** of the list. First with the array index as the key, then with each person's id:

```jsx
{people.map((p, i) => (
  <li key={useIndexKey ? i : p.id}>
    {p.name}: <input />
  </li>
))}
```

```text
key={index}: Meera [note for Asha]  |  Asha []  |  Ravi []
key={p.id}:  Meera []  |  Asha [note for Asha]  |  Ravi []
```

With index keys, the note jumped to **Meera's** row. React matched children by key: key `0` used to be Asha's row and is now Meera's, so React kept that row's DOM input, with its typed text, and just changed the name. With stable ids, React knew `asha` was still Asha, moved her row down, and created a fresh one for Meera.

The rules for keys:

- **Use a stable, unique id** from your data.
- **Index keys are only safe** if the list never reorders, filters or inserts.
- **Never use `Math.random()`.** A new key every render means React rebuilds every item every time.

![List rendering with keys: with key equal to index, key 0 changes from Asha to Meera but keeps the input text note for Asha, key 1 changes from Ravi to Asha, and key 2 is a new row for Ravi; with key equal to id, meera is a new row, asha moves down keeping its input, and ravi moves down](https://mermaid.ink/img/pako:eNptkstOwzAQRX9lNJtuQknSRxILkIBuuugGsQKzcOtpE7Wxo6nTB1W3fACfyJegpA2FCO9sHx_fK80BZ1YTCpyv7HaWKnbw_CBZGgCAdTldsCpSGOvdq8Ql7eEWMqNpJ_Gtgao19s_XvoD7darg6-MTJkSsbqZ8fZeZonSwpMIJ6BjrCOaWa7DTFgVnUSDgSW2yWlSBbS48c6EAQ9saq_hfGBn9T49LDd1SjpoOeZX7pGW7bVNNQLVOlYDcbkh7cCnYxpucrDbZGf-bET1ccKZROC7Jw5w4V9UWDxUi0aWUk0QBEpl0ubua2ZVlidIc0cNCmRdr8-Y123KRopir1Zo8LAutHI0ytWCV_5wyGU38aEvjUPT82oHigDsU_SDuhnEyTAI_SKKe3_NwjyIIw24_HIS9OI78OEqS6Ojhe_2r3w2HwWAYB4M4HvaTaOAh6cxZnpyGqp6t4zfvArxW?type=png)
*React matches rows by key. Index keys tie the typed input to a position; id keys tie it to a person.*

## Avoiding unnecessary re-renders

Re-rendering is cheap, but not free. When a parent re-renders, all its children re-render too, by default. I put two identical children in a parent with a counter: one plain, one wrapped in `React.memo`. After the first render and three clicks:

```text
after 1 render + 3 clicks: { plain: 4, memo: 1 }
```

The plain child ran four times; the memoised one once, because its props never changed. The tools, roughly in the order to reach for them:

- **Move state down.** If only one small component needs the state, keep it there; then only that component re-renders.
- **Split components** so expensive parts don't sit under fast-changing state.
- **`React.memo(Component)`** skips a re-render when props are the same as last time.
- **`useMemo`** remembers an expensive calculated value between renders.
- **`useCallback`** remembers a function, so a memoised child doesn't see a "new" prop every render.

**When not to:** memoisation costs memory and a props comparison on every render. Wrapping everything "just in case" adds complexity for no visible gain. Measure first with the React DevTools Profiler, and memoise what actually shows up as slow. The React Compiler, which can add this memoisation automatically at build time, makes hand-written `useMemo` and `useCallback` less necessary in projects that use it.

## Virtual DOM myths

**"The virtual DOM is faster than the DOM."** No. React does extra work: building trees and comparing them, *and then* updating the DOM. Carefully hand-written DOM code that changes exactly the right node is at least as fast. What React gives you is "fast enough, automatically": good updates without writing the update code yourself.

**"React doesn't touch the real DOM."** It does, in the commit phase. The virtual DOM decides *what* to change; the real DOM still gets changed.

**"Diffing finds the perfect minimal change."** It finds a good one, quickly, using the rules above. Swap an element's type and React rebuilds the subtree even if the contents are identical.

**"Re-renders are bad."** Unnecessary *expensive* re-renders are bad. A re-render that produces the same output changes nothing in the DOM, and the counter at the top re-rendered its whole component to make a single text change. Profile before worrying.

## The full lifecycle, start to finish

Put together, here's everything between a click and new pixels:

1. **Initial render**: components run, an element tree is built, real DOM is created, the browser paints.
2. **State update**: `setState` schedules a re-render.
3. **New virtual DOM**: the component runs again and returns a new tree.
4. **Reconciliation**: React compares old and new, using type and key rules.
5. **Commit**: React applies only the differences to the real DOM.
6. **Browser paint**: the browser lays out and draws the changed pixels. Then effects run.

![Complete React update pipeline: setState, the component runs again, a new virtual DOM, reconciliation of old vs new, commit of DOM changes, the real DOM, then browser paint](https://mermaid.ink/img/pako:eNplkctuwjAQRX_FmnWgeRDyUMWiybIpFUgsGrNwkyGxlNho4hBaxL9XNaJC6nI859xraS5Q6RohhUOnp6oVZNjrhhNXjDG2LTkMaLZGGOSwZ7PZimUlh0z3R61QmedPelrRqAYmGiEVh_1dzSy8Kzm84cROkswoOpaviwdmZ5lNyWGDlVaV7KQwUiubqruanQamcHowNtYobl_o5a0_XxesaoVqcHhAC4vmNvxfc26X7yWHF9LTgMSOQirDYQ8ONCRrSA2N6ECP1IvfES6_JgfTYo8cUsaBsB7Ps0p3mjhwdQUHjkJ9aN3fbdJj00J6EN2ADozHWhjMpWhI9H-vhKpGyvSoDKTBwmZAeoEzpAsvnvtxskw810uiwA0c-ILU8_35wg_9II4jN46SJLo68G1b3bm_9MJl7IVxvFwkUegA1tJoKm43tqe-_gC8kpjV?type=png)
*From setState to pixels, in six steps.*

The interview answer in one line: **calling `setState` re-runs your component to produce a new element tree; React compares it with the old one and commits only the differences to the real DOM, which the browser then paints.** The virtual DOM doesn't make updates faster than careful DOM code. It means you never write the update code at all. This post deliberately stayed above React's internal scheduler and Fiber architecture, which decide *when* that work happens rather than *what* it does.

Open the React DevTools Profiler on an app you've built and click around. Which component re-renders most often, and does it actually need to?
