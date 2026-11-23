---
title: "How Does React Remember Between Renders? A Practical Guide to Hooks"
slug: react-hooks-usestate-useeffect-custom-hooks
subtitle: useState, re-renders, useEffect, dependency arrays and custom hooks, built up in order with real React 19 output
tags: react, javascript, web-development, frontend, beginners
cover: ./cover.png
seoTitle: "React Hooks Guide: useState, useEffect, Custom Hooks"
seoDescription: "Learn React hooks from first principles: how useState remembers, what triggers re-renders, useEffect as sync, dependency arrays and custom hooks."
enableToc: true
---

A React component is a function. When a function returns, its local variables are gone. So how does this counter remember that it's on `3`?

```jsx
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

`count` is a local variable. Every click calls `Counter` again from the top, and `useState(0)` is called again with `0`. Yet the button shows `1`, `2`, `3`. The value isn't stored in the function. It's stored by React, and `useState` is how the function asks for it back.

That's what hooks are: React's way of giving a plain function memory (`useState`) and a way to stay in sync with the world outside it (`useEffect`). This post builds them up in order: state, re-renders, effects, dependency arrays, then custom hooks. Every output below is from React 19.3.1, run in Node with jsdom.

## Why hooks were introduced

Before hooks (React 16.8), a component that needed state had to be a class:

```jsx
class Counter extends React.Component {
  state = { count: 0 };
  componentDidMount() { document.title = `Clicked ${this.state.count} times`; }
  componentDidUpdate() { document.title = `Clicked ${this.state.count} times`; }
  render() {
    return <button onClick={() => this.setState({ count: this.state.count + 1 })}>{this.state.count}</button>;
  }
}
```

Three problems kept coming up. One concern, keeping the title in sync, was split across two lifecycle methods. Unrelated concerns piled up in the same `componentDidMount`. And sharing stateful logic between components meant wrapper patterns (higher-order components, render props) that nested components several levels deep.

Hooks fixed all three. Components became plain functions. Each concern lives in one place. And logic can be shared by extracting a function, a custom hook, with no wrappers. That's why modern React code is written with function components and hooks.

## useState: memory for a component

`useState` takes a starting value and returns two things: the current value, and a function to change it.

```jsx
const [count, setCount] = useState(0);
```

Calling `setCount` does two things: it stores the new value, and it tells React to render the component again. On that next render, `useState(0)` ignores the `0` and returns the stored value instead.

You can have as many as you need:

```jsx
function ThemeSwitcher() {
  const [theme, setTheme] = useState("light");
  const [fontSize, setFontSize] = useState(16);
  // ...
}
```

For objects, replace them rather than changing them. React compares the old and new value, and if you mutate the old object, it looks unchanged:

```jsx
const [user, setUser] = useState({ name: "Asha", city: "Pune" });

// ❌ Mutates the same object; React may not re-render
user.city = "Mumbai"; setUser(user);

// ✅ New object with the changed field
setUser({ ...user, city: "Mumbai" });
```

Here's the surprise most people hit early. A button that calls `setCount(count + 1)` three times in one click, compared with the "updater" form:

```text
setCount(count + 1) x3: 1
setCount(c => c + 1) x3: 3
```

The first version ends at `1`. During that click, `count` is `0` and stays `0`: it's a value captured by *this* render. All three calls say "set it to 0 + 1". The updater form passes a function, and React runs each one on the latest value: 0→1→2→3. **When the new value depends on the old one, use the updater form.**

![State update to re-render flow: a click calls setCount(1), React stores 1, Counter() runs again, useState returns 1, and the button shows 1](https://mermaid.ink/img/pako:eNpVkcFugzAMhl8l8qmVaEWgQMhhh3WXSduFqpeRHiJwAQ2SyiRqt6rvPkHVaTva_v7PsnyFytYIEo69PVetJsfeCkXKMMbYtlSw7bvqU8GBrVZPbFcqGNFtrTduwZcKDg90d5-7UkGBunJsdJZwZPwv42aomKyTAWmxZOTNyHSjO_OHLGZwXyrwI-6cdsgInSfzX7i_Y6-lgmfvnDVsbO35zkAADXU1SEceAxiQBj2VcJ2yClyLAyqQTAFh7S-ryvaWFChzgwBO2nxYOzzSZH3TgjzqfsQA_KnWDl863ZAefruEpkaaDwMZi9kB8goXkBsu1pHI05yHPM_iMA7gCySPovUmSqJYiCwUWZ5ntwC-563hOkp5kgqeCJFu8iwJAOvOWXq_P2v-2e0HUD2G6w?type=png)
*setState stores the value; the next render reads it back.*

## What a re-render really is

A **re-render** is React calling your component function again. Three things trigger it:

1. the component's own state changes;
2. its parent re-renders (children re-render with it by default);
3. a context it reads changes.

Re-rendering means *running the function*, not rebuilding the page. React compares the new output with the old and changes only what's different in the real DOM. I measured that in [the virtual DOM post](https://jaydeepkanzariya.hashnode.dev/virtual-dom-reconciliation-rendering): one click, one text node changed.

That leads to the most useful habit with state: **don't store what you can calculate.**

```jsx
// ❌ Two pieces of state that must be kept in sync by hand
const [items, setItems] = useState([]);
const [count, setCount] = useState(0);

// ✅ One piece of state; the count is derived on every render
const [items, setItems] = useState([]);
const count = items.length;
```

Derived values are recalculated on each render for free, so they can never drift out of sync.

## How React remembers: hooks are a list

So where does the stored value live? For each component on screen, React keeps a list of hook "slots". On every render, hooks are matched to slots **by the order they're called**: first `useState` call, slot 1; second, slot 2; and so on.

```jsx
function ThemeSwitcher() {
  const [theme, setTheme] = useState("light"); // slot 1
  const [fontSize, setFontSize] = useState(16); // slot 2
}
```

React doesn't know the names `theme` or `fontSize`. It only knows "the first hook call gets slot 1". That one fact explains why `useState` remembers, why two counters on the same page have separate counts (separate slot lists), and the rules of hooks further down.

![React hooks mental model: ThemeSwitcher() runs on every render; its first hook call reads slot 1, theme equals light, and its second hook call reads slot 2, fontSize equals 16; both values feed the returned UI](https://mermaid.ink/img/pako:eNpVkc1PwkAQxf-VyVzQpGB36XeUC15I9ELlIsthbZe2sd0lw1a-5H83LWLwOJP3fm8y74SZyRUmuK7NLislWXiZCxIaAGBqms1S4FupGpXuKpuViu7uHz_oYUKt3oLRoL4UHYCUzhUJXMFwOPlmWwulMZ-Qybr-hpQtBaa1scB6q-1w8ASDuipKOxC4us3rCVzn_wj8SuA9YW20TatjB2HBjT9lnRsWs6XAubItaZXDYnar4L8KdLCgKsfEUqscbBQ1shvx1AkF9kcKTEAgqbzdDzNTGxIo9Bkd3Ej9bkxzdZNpixKTtay3ysF2k0urnitZkGz-tpcXTU2rLSYe7xmYnHCPiceiEY_iIGYui8OxO3bwgAnjfORxn4-jKHSjMI7Ds4PHPtUd8YD5QcT8KAq8OPQdVHllDb1euuwrPf8AFTmSog?type=png)
*React doesn't know your variable names. It knows the first hook call gets slot 1.*

## useEffect: syncing with the outside world

Rendering should be pure: take state, return UI, touch nothing else. But apps have to touch other things: set the page title, start a timer, subscribe to a chat server, fetch data. Those are **side effects**, and `useEffect` is where they go.

The clearest way to think about it, and the way the [React docs frame it](https://react.dev/learn/synchronizing-with-effects): an effect **keeps something outside React in sync with your state**. Not "run this on mount".

```jsx
function ThemeSwitcher() {
  const [theme, setTheme] = useState("light");

  useEffect(() => {
    document.body.dataset.theme = theme; // keep the page in sync with state
  }, [theme]);

  return <button onClick={() => setTheme(theme === "light" ? "dark" : "light")}>{theme}</button>;
}
```

If the effect starts something, it should also stop it. That's the **cleanup function** you return. Here's a `Profile` component that "subscribes" to a user. I logged every render, effect and cleanup while rendering it with `userId=1`, rendering again with the same id, switching to `userId=2`, then removing it:

```jsx
useEffect(() => {
  log.push(`effect: subscribe to user ${userId}`);
  return () => log.push(`cleanup: unsubscribe from user ${userId}`);
}, [userId]);
```

```text
render userId=1
effect: subscribe to user 1
render userId=1
render userId=2
cleanup: unsubscribe from user 1
effect: subscribe to user 2
cleanup: unsubscribe from user 2
```

Read it slowly. Effects run **after** the render. The second render with the same id ran **no effect**, because nothing it depends on changed. Switching users cleaned up user 1 *before* subscribing to user 2. And removing the component cleaned up the last subscription. Start, stop, restart only when needed: that's synchronisation.

![useEffect execution and cleanup lifecycle: render, commit to DOM, then the effect runs; when dependencies change the old effect is cleaned up and the effect runs again; when the component is removed a final cleanup runs](https://mermaid.ink/img/pako:eNplkU1vwjAMhv-K5XNBbelnDrsUOIEmcRzhEDXuh9QkVUg2NuC_Ty1jmrSj_b5-Xsu-Ym0kIcNmMB91J6yD3YFbrgEADkeOB9KSLMcTLBYvUB05Vkap3oEzsH7dczw93dXs2Bw5bpqGagfW6_MffTPpN0njGepO6JZuUO0m3kBC-xHMIIHmyb_Q3YMaT6t4_WMA0Ype_2PXRo1Gk3ZgSZl3kjeotkeO216LAepHDscTBtjaXiJz1lOAiqwSU4nXicbRdaSIIwOOlqS_LGozGMuR6zsGOAr9Zox6Tlvj2w5ZI4YzBehHKRyte9FaoX67dj5iZbx2yJJsZiC74gVZEhXLuCizMgqjMl-FqwA_kUVxvEziNF4VRR4WeVnm9wC_5tRwGWdRmhVRWhRZUuZpgCR7Z-z-8cj5n_dvVtSR8w?type=png)
*Effects run after the commit. Cleanup always runs before the next effect, and once more on removal.*

## Dependency arrays

The second argument to `useEffect` says *when* to re-sync:

| You write | Effect runs |
|---|---|
| `useEffect(fn)` | after every render |
| `useEffect(fn, [])` | once after the first render (plus cleanup on removal) |
| `useEffect(fn, [userId])` | after the first render, then whenever `userId` changes |

React compares each dependency with its value from the last render using `Object.is`. That's where the classic infinite loop comes from:

```jsx
// ❌ A new object on every render
const options = { page: 1 };
useEffect(() => { setN((x) => x + 1); }, [options]);
```

`{ page: 1 }` creates a **new** object each render, so it's never "the same" as last time. The effect sets state, which re-renders, which creates a new object, which re-runs the effect. My demo capped it at 50 and hit the cap. With `const page = 1` as the dependency, a plain number, the effect ran **once**.

The fixes: depend on primitive values (`page`, not `options`), create the object *inside* the effect, or move it outside the component if it never changes. And don't silence the `react-hooks/exhaustive-deps` lint warning by leaving dependencies out. That gives you an effect that reads stale values.

One more thing you'll see in development. In Strict Mode, React deliberately runs effects twice on mount:

```text
render userId=1
render userId=1
effect: subscribe to user 1
cleanup: unsubscribe from user 1
effect: subscribe to user 1
```

That's a test, not a bug: if your effect breaks when it's set up, cleaned up and set up again, its cleanup is wrong. It only happens in development.

![Dependency array behavior comparison: no array runs the effect every render; an empty array runs it on the first render only; [userId] runs it on the first render and when userId changes; an options object runs it every render because it is a new object each time](https://mermaid.ink/img/pako:eNpl0U1Pg0AQBuC_MpmrtAIt5SOmB21NPFgvnmQ5bGEKGNhthsUWm_53A_2w0eMkz_vOJHPAVGeEEW4qvUsLyQbeHwULBQCwigWuNEhm2QlMYDSaw8qJBS6_iDtgUhmxwOTil7HAGJILXfb0ueTGnCloVXU3ftH7tiF-ya6hxb_Q3cOa7-e7ghScLKSFVDk1N01vfZPemlKrBvT6k1JzbXz7e_HQp2h3hkAyLcCUNQlM0MKcywwjwy1ZWBPXsh_x0C8SaArqXQQCmbJ2P0p1pVmgUEe0cCvVh9b1Jc26zQuMNrJqyMJ2m0lDi1LmLH_JcNGTbpXByHOGCowOuMdo6gRjNwhnoWM7oT-xJxZ2GDmuO566njsJAt8O_DD0jxZ-D0vtsTtzvFngeEEwm4a-ZyFlpdH8enrx8OnjD5PQm4c?type=png)
*Same effect, four dependency arrays. The object one looks like [userId] but behaves like no array.*

## Common effect patterns

**Fetching data.** The trap is a race: the user switches profiles quickly, and the slow first response arrives last and overwrites the second. An `ignore` flag in the cleanup handles it:

```jsx
useEffect(() => {
  let ignore = false;
  fetch(`/api/users/${userId}`)
    .then((r) => r.json())
    .then((data) => { if (!ignore) setUser(data); });
  return () => { ignore = true; }; // a newer request replaced this one
}, [userId]);
```

**Browser events and timers.** Add the listener or start the interval in the effect; remove or clear it in the cleanup. Every `addEventListener` needs its `removeEventListener`, and every `setInterval` its `clearInterval`.

**When not to use an effect.** Calculating values from state (derive them during render) and responding to a click (do it in the event handler) don't need effects. React's guide [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect) lists the cases. If nothing *outside* React is involved, you probably don't need one.

## Custom hooks

A **custom hook** is a function whose name starts with `use` and that calls other hooks. That's all. It's how you reuse stateful logic. Here's window-width tracking, written once:

```jsx
function useWindowWidth() {
  const [width, setWidth] = useState(window.innerWidth);
  useEffect(() => {
    const onResize = () => setWidth(window.innerWidth);
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);
  return width;
}

function Header() { const w = useWindowWidth(); return <h1>{w < 600 ? "Menu ☰" : "Home · Blog · About"}</h1>; }
function Footer() { const w = useWindowWidth(); return <p>Width: {w}px</p>; }
```

I rendered both, then simulated resizing the window to 480 px (spacing added between the two components' text):

```text
at 1024: Home · Blog · About  Width: 1024px
at 480:  Menu ☰  Width: 480px
```

Two components, one piece of logic, both updated. Each call gets **its own** state, because each component has its own slot list. Custom hooks share *logic*, not *state*. Shared state is a job for lifting state up or context.

![Custom hook architecture: useWindowWidth(), built from useState and useEffect, is used by Header and Footer; each keeps its own width state; Header shows the menu or full navigation and Footer shows Width: 480px](https://mermaid.ink/img/pako:eNqFkU1Lw0AQhv_KMCfFtCZpk2wWKbR-0IsnlYLdHtbspA0ku2Wza6ql_12SYvHmcYbnfWbgPWJhFCHHsjZdsZPWwetCWKEBAJZrgb6lVaWV6VaVcrur67sPezvzLb046QhuwLf0WJZUOIEbGI1mMF8LXJJUZAfUdBq6PgptnxC4udgHfLEW-GSM-xefD_hbr38m7cFYKH1dg5aff6jFmeqtw8McpizcHwRuMMCtrRRyZz0F2JBtZD_isU8KdDtqSCAHgZaUP4wKUxsrUOgTBriX-t2Y5jdtjd_ukJeybilAv1fS0UMlt1Y2l60lrcjeG68d8iQZHMiPeEA-jdg4ZnmaR2GUZ5NwEuAX8iiOx9M4iSeMZSHL8jw7Bfg9XA3HcRolKYsSxtJpniUBkqqcsc_n9oYSTz_sf46j?type=png)
*One hook, two components, two separate copies of the state. Custom hooks share logic, not state.*

## When to create one

Good candidates, where the same stateful logic shows up in more than one component:

- **Data fetching**: `useFetch(url)` returning `{ data, error, loading }`, with the `ignore` flag built in.
- **Authentication**: `useAuth()` returning the current user and `login`/`logout`.
- **Forms**: `useForm(initialValues)` handling values, changes and validation.
- **Window and device utilities**: `useWindowWidth`, `useOnlineStatus`, `useLocalStorage`.

**When not to:** logic used in only one place, or a hook that just wraps one `useState` and adds nothing. Extract when the second component needs it, not before.

## Rules of hooks

React's [rules of hooks](https://react.dev/reference/rules/rules-of-hooks) are two lines:

1. Call hooks **at the top level**: not inside conditions, loops, or nested functions.
2. Call hooks **only from React function components or custom hooks**.

The slot model explains rule 1. Here's a component that calls a hook only when `showName` is true:

```jsx
const [a] = useState("a");
if (showName) { const [name] = useState("Asha"); } // ❌
const [b] = useState("b");
```

It rendered fine with `showName={false}`: two hooks, two slots. Re-rendered with `showName={true}`, React threw:

```text
Rendered more hooks than during the previous render.
```

and warned that it had "detected a change in the order of Hooks". The `b` call moved from slot 2 to slot 3, so every hook after the `if` would read the wrong slot. The fix is to always call the hook and put the condition *inside* or after it. The `eslint-plugin-react-hooks` lint rule catches this before you run anything.

## Thinking in hooks

Three questions cover most decisions:

- **Does this value need to survive re-renders and change the UI when it changes?** `useState`. If it can be calculated from other state, calculate it instead.
- **Does something outside React need to match my state?** `useEffect`, with a cleanup if it starts anything, and honest dependencies.
- **Do two components need the same stateful logic?** A custom hook. Each gets its own copy of the state.

The answer to the opening question, in one line: **React remembers between renders by keeping each component's hook values in slots, matched by call order; `useState` reads and writes a slot, and `useEffect` keeps the outside world in sync with it.** This post skipped `useRef`, `useReducer`, `useContext` and the memoisation hooks, which follow the same rules.

Look at the last `useEffect` you wrote. Is it syncing with something outside React, or could it be a calculation or an event handler instead?
