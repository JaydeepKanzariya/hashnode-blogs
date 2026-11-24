---
title: "From node -v to Your First HTTP Server: Zero Frameworks"
slug: first-nodejs-app-step-by-step
subtitle: "Installing Node.js, checking your terminal, using the REPL, running hello.js, and writing a Hello World server with zero packages"
tags: nodejs, javascript, web-development, beginners, tutorial
cover: ./cover.png
seoTitle: "Your First Node.js App: Install, REPL & Hello World Server"
seoDescription: "Set up your first Node.js app step by step: install Node.js, verify with node -v, use the REPL, run hello.js, and build a Hello World HTTP server."
enableToc: true
---

Run `node hello.js` and your terminal prompt comes back in a fraction of a second. Run `node server.js` and the cursor sits there blinking — it does not exit.

Nothing is frozen. Your first script ran top to bottom and finished; your HTTP server opened a network port and stayed alive waiting for incoming requests. By the end of this walkthrough, you will have installed Node.js, used the REPL, run your first script, and started a working Hello World web server with **zero frameworks or third-party packages**.

Every command and output below comes from a real run on **Node.js v24.22.1** and **npm 11.19.1**.

## 1. Installing Node.js (OS-neutral)

Download the **LTS (Long-Term Support)** installer from [nodejs.org](https://nodejs.org/). Node.js publishes two release lines:
- **LTS** — recommended for almost everyone; stable and supported for years.
- **Current** — includes the newest experimental features, though it changes more frequently.

Run the official installer for your operating system (Windows, macOS, or Linux) with default options — make sure "Add to PATH" stays checked if prompted. If you work across multiple projects that need different Node versions, developers also use version managers like `nvm` or `fnm`, though the official LTS installer is the cleanest starting point.

## 2. Checking your installation in the terminal

Open a **new** terminal window (an existing terminal may not see the updated `PATH`) and run:

```bash
node -v
npm -v
```

```text
v24.22.1
11.19.1
```

`node` is the JavaScript runtime itself. `npm` (Node Package Manager) ships alongside it and is what you will use later to install packages. Your exact version numbers will differ if you install a newer release. I only ran the examples in this post on Node.js v24.22.1.

If your terminal prints `command not found` or `is not recognized`, close and reopen the terminal first; if it still fails, re-run the installer and verify the PATH option.

## 3. Understanding and using the Node REPL

Before creating any files, try the **REPL** — short for **Read–Eval–Print Loop**:
- **Read:** waits for one line (or block) of JavaScript you type.
- **Eval:** evaluates it inside Node's V8 engine.
- **Print:** displays the result immediately.
- **Loop:** prompts you for the next line.

It is the terminal equivalent of the browser DevTools console, ideal for testing a quick expression without creating a file. Start it by typing `node` with no filename:

```bash
node
```

```text
Welcome to Node.js v24.22.1.
Type ".help" for more information.
> 2 + 3
5
> "hello".toUpperCase()
'HELLO'
> .exit
```

Type `.exit` (or press `Ctrl + C` twice) to leave the REPL and return to your normal shell prompt. Two other handy REPL shortcuts: `_` holds the result of the previous expression (so typing `_ + 10` after `5` gives `15`), and `.help` lists every built-in REPL command such as `.clear` and `.save`. Because nothing typed in the REPL is saved to disk by default, move to a `.js` file as soon as your code grows past a few lines.

## 4. Creating and running your first JavaScript file

Create a new folder for your project, move into it, and create a file named `hello.js`:

```js
// hello.js
const name = "Asha";
console.log(`Hello, ${name}!`);
console.log("Running on Node.js", process.version);
```

Run it from the same folder using the `node` command:

```bash
node hello.js
```

```text
Hello, Asha!
Running on Node.js v24.22.1
```

Here is what happened behind the scenes: the `node` CLI read `hello.js` from disk, handed the code to the V8 engine inside the Node.js runtime, read `process.version` from Node's built-in `process` global, wrote both `console.log` lines to standard output, saw no pending timers or open servers, and exited cleanly. (You can also drop the `.js` extension and run `node hello` — Node resolves `hello.js` automatically.)

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    T["Terminal<br/>node hello.js"] --&gt; F["hello.js<br/>JS source file"]
    F --&gt; R["Node.js Runtime<br/>V8 Engine"]
    R --&gt; O["Terminal Output<br/>Hello, Asha!"]
-->
![Script to runtime to output flow: running node hello.js in the terminal passes hello.js into the Node.js runtime and V8 engine, which executes console.log and prints Hello, Asha! to the terminal before exiting](https://mermaid.ink/img/pako:eNpNzkuLAjEQBOC_0ltnH9dlEGEPKyKLwihepueQnfQ4kTwkk-BB_O_LRkSvzVdVfUMXtKBCb8O1G1RM9FOzJyI6NIyDRGe8sovfOF_6oIUGsTbMziOjpel0SauG8bwVtdnTGHLshHpjhdE-2lZF1w1jG7TMziPV2SfjpISOn_TtT8a_fF387u0H2uV0yan49f_ihL7GQX0wWkzgJDplNCrcGGkQJ4yKoaVX2SbGHfc_9uZLfA==?type=png)

## 5. Writing a Hello World HTTP server (no frameworks)

Node.js includes a built-in `http` module, so you can build a real web server without installing anything. Create `server.js` in the same folder:

```js
// server.js
const http = require("http");

const server = http.createServer((req, res) => {
  res.writeHead(200, { "Content-Type": "text/plain" });
  res.end("Hello, World!\n");
});

server.listen(3000, "127.0.0.1", () => {
  console.log("Server running at http://127.0.0.1:3000/");
});
```

Start it:

```bash
node server.js
```

Open `http://127.0.0.1:3000/` in your browser — or run `curl -i http://127.0.0.1:3000/` from a second terminal to see the status, headers, and body together. To print the same summary yourself, save this as `client.js` and run it from a second terminal while the server is running:

```js
// client.js
fetch("http://127.0.0.1:3000/").then(async (res) => {
  console.log("GET / ->", res.status, res.headers.get("content-type"), JSON.stringify(await res.text()));
});
```

Here is the response summary from Node.js 24.22.1:

```text
GET / -> 200 text/plain "Hello, World!\n"
```

Line by line:
- `require("http")` loads Node's built-in HTTP module.
- `http.createServer((req, res) => { ... })` registers a callback that runs every time a browser or client connects.
- `res.writeHead(200, { "Content-Type": "text/plain" })` sets the HTTP status (`200 OK`) and tells the client the response is plain text.
- `res.end("Hello, World!\n")` sends the response body and finishes that request.
- `server.listen(3000, "127.0.0.1", ...)` binds the server to port `3000` on your local machine (`127.0.0.1`, also reachable as `localhost`).

Because `server.listen` keeps an open network handle on the event loop, `node server.js` stays alive until you press `Ctrl + C`. Binding to `127.0.0.1` keeps the server local to your own computer — nobody else on your Wi-Fi network can reach it while you experiment. If you edit `server.js` (for example, changing `"Hello, World!\n"` to your own name), restart it — or run `node --watch server.js` so Node restarts automatically whenever you save.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart TD
    Start["Run node file.js"] --&gt; Top["Execute top-level code"]
    Top --&gt; Check{"Open handles?<br/>(server, timer)"}
    Check -- "No (hello.js)" --&gt; Exit(["Process exits"])
    Check -- "Yes (server.js)" --&gt; Loop["Wait for requests<br/>on port 3000"]
    Loop --&gt;|"HTTP request"| Handle["Run callback<br/>send Hello, World!"]
    Handle --&gt; Loop
-->
![Node execution flow comparing a one-off script and a long-running HTTP server: both start with the node command and run top-level code; hello.js has no open handles so it exits immediately, while server.js binds port 3000 and loops waiting for incoming HTTP requests until Ctrl+C](https://mermaid.ink/img/pako:eNplkMFqAjEQQH9lOicF1wq9SbGHVvBQWmkXpDgeYjLLrmYz2yRrBfXfy0YrQu_z3ryZA2oxjGMsrPzoUvkI-Qs5AIDPqHxcEn60DpwYhqKyPNwEwhVk2QRyaZaE0z3rNjJEaTLLO7bQCQlXZ0kuTRp-LllvD4TvDTsolTOWw9Pj2t9PeoH9jv0AYlWz7xOezmQiIMuA8E2gV7K1MtyEPmESTvdV7C0J5140hwC8r2KX1v9Hf3GAy5Ib_lVS_kJVEQrx4Pm75RBDahIHjfgID6PR6HpKR3TokXCW5_M_gvAIs3TQ5VdaWbtWeptMgZ2BWdc-gIV4a-6uvjN0jcEB1uxrVRkc44Ewllwz4ZjQcKFaGwlPePoFDauKSg==?type=png)

## 6. Two errors you will hit on day one

**Wrong folder or typo in filename (`MODULE_NOT_FOUND`):**

```bash
node missing.js
```

```text
Error: Cannot find module '.../missing.js'
  code: 'MODULE_NOT_FOUND',
```

Check your current directory (`pwd` on macOS/Linux, `cd` or `Get-Location` on Windows) and list the files (`ls` / `dir`) to make sure the filename matches exactly.

**Starting the server twice on the same port (`EADDRINUSE`):**

```text
Error: listen EADDRINUSE: address already in use 127.0.0.1:3000
```

Another terminal still has `node server.js` running on port `3000`. Switch to that terminal and press `Ctrl + C`, or change the port number in `server.listen(...)` to `3001`.

## When NOT to stick with raw `http`

Node's built-in `http` module is great for learning how servers work and for tiny single-endpoint utilities. Once your app needs multiple routes (`/users`, `/orders/:id`), JSON body parsing, authentication middleware, or static file serving, writing `if (req.url === ...)` blocks by hand turns into repetitive boilerplate. At that point, move up to a framework like Express or Fastify.

## Where this leaves you

You now have the full beginner loop in place: verify Node with `node -v`, test quick ideas in the REPL, run scripts with `node file.js`, and keep a zero-framework HTTP server running with `http.createServer` and `server.listen`.

One honest limit: this post intentionally stopped before `package.json`, installing third-party packages with `npm`, and keeping a server running in production (where you use a process manager or container runtime instead of an open terminal). Did you hit `MODULE_NOT_FOUND`, `EADDRINUSE`, or a `PATH` issue on your very first Node.js run?
