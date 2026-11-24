---
title: "From req.on('data') to app.post(): Express Routing Explained"
slug: express-routes-and-requests
subtitle: "Raw Node http vs Express 5.3.0, creating your first server, GET and POST routes, params, queries, and sending responses"
tags: nodejs, javascript, web-development, beginners, tutorial
cover: ./cover.png
seoTitle: "Express.js Routes and Requests: GET, POST & Responses"
seoDescription: "Learn Express.js routing and request handling: raw Node http vs Express 5.3, GET and POST routes, req.params, req.query, req.body, and responses."
enableToc: true
---

Try handling a single JSON `POST` route using only Node's built-in `http` module:

```js
// Raw Node.js http: manual method checks, stream chunks, JSON.parse, and headers
const http = require("http");

const server = http.createServer((req, res) => {
  if (req.method === "POST" && req.url === "/books") {
    let body = "";
    req.on("data", (chunk) => { body += chunk; });
    req.on("end", () => {
      const parsed = JSON.parse(body);
      res.writeHead(201, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ created: parsed.title }));
    });
    return;
  }
  res.writeHead(404, { "Content-Type": "application/json" });
  res.end(JSON.stringify({ error: "Not found" }));
});

server.listen(3000);
```

```text
POST /books -> 201 (application/json) {"created":"JS Basics"}
```

That is 16 lines of code for one route — without error handling for bad JSON, without path parameters like `/books/1`, and without query strings. Add ten more endpoints and that `if/else` block becomes unreadable. **Express.js** replaces that boilerplate with clean route definitions and request/response helpers.

Every output below comes from a real run on **Node.js 24.22.1** and **Express 5.3.0**.

## What Express.js is (and why it simplifies Node.js)

**Express.js** is a minimal web framework built directly on top of Node's built-in `http` module. It does not replace Node.js — it wraps `http` with four things almost every web server needs:
- **Routing by method and path:** `app.get("/books", ...)` and `app.post("/books", ...)` instead of manual `if (req.method === ... && req.url === ...)` checks.
- **Automatic path and query parsing:** `/books/1` lands on `req.params.id`; `/books?author=Asha` lands on `req.query.author`.
- **Body parsing middleware:** one line (`app.use(express.json())`) replaces manual `req.on("data")` stream collection.
- **Response helpers:** `res.status(201).json(data)` sets `Content-Type: application/json`, stringifies the object, and ends the response in one call.

| Task | Raw Node.js `http` | Express.js 5.3.0 |
|---|---|---|
| Match route | Manual `if (req.method && req.url)` | `app.get("/books/:id", handler)` |
| Read JSON body | Collect `data`/`end` chunks + `JSON.parse` | `app.use(express.json())` → `req.body` |
| Send JSON | `res.writeHead(...)` + `JSON.stringify` | `res.status(201).json(obj)` |
| Parse query string | `new URL(req.url, ...).searchParams` | `req.query` |

## Creating your first Express server

Initialize a project and install Express:

```bash
npm init -y
npm install express@5.3.0
```

Start a file named `server.js` with the setup and root route below (we will add the remaining routes and `app.listen(3000)` as we go):

```js
// server.js (Node.js 24.22.1, Express 5.3.0)
const express = require("express");

const app = express();
app.use(express.json()); // parses incoming JSON into req.body

let nextId = 3;
const books = [
  { id: 1, title: "JS Basics", author: "Asha" },
  { id: 2, title: "Node Patterns", author: "Ravi" },
];

app.get("/", (req, res) => {
  res.send("Books API is running");
});
```

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    C["Client<br/>browser / fetch"] --&gt;|"HTTP Request"| P["express.json()<br/>parse body"]
    P --&gt; R["Matching Route<br/>app.get / app.post"]
    R --&gt;|"res.status().json()"| Res["HTTP Response"]
-->
![Request to route handler to response flow in Express: the client sends an HTTP request, express.json() parses the JSON body if present, Express matches the HTTP method and path to the route handler (req, res), and the handler sends back a status code and JSON response](https://mermaid.ink/img/pako:eNo9jrFug0AQRH9lNZUtxdCjyI2bFImETu5YigMWQwR3l9tDTmT73yMclG6KmffmhtZ3ggL95K_tYGOid8OOiOhUMU7TKC69NjE_NtFfVSLl1EtqB0ZNh8Pxzng7n0sy8rWIJsadyooh3yGKavap3u32z32wUYUa3_0w6j9DuRLIVIwPm9phdBcyfkny7NsQsoskymlNwa_wbWc2cxTNNNm06G6_qdYDRrT6v6XBOxVGjRfMEmc7dihwY6RBZmEUjE56u0yJ8cDjFxnaWGY=?type=png)

`express()` creates an application object (`app`). Calling `app.listen(3000)` at the bottom of the file starts the underlying HTTP server on port 3000. Run `node --watch server.js` during development so Node.js restarts automatically whenever you save an edit.

## How Express routing works

A **route** maps an HTTP method (`GET`, `POST`, `PUT`, `DELETE`) plus a URL path (`/books`, `/books/:id`) to a handler function `(req, res) => { ... }`. When a request arrives, Express checks your registered routes from top to bottom and runs the **first** one whose method and path match.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart TD
    In["Incoming HTTP Request"] --&gt; App{"Express App<br/>match method + path"}
    App --&gt;|"GET /"| R1["res.send('Books API...')"]
    App --&gt;|"GET /books"| R2["Filter by req.query<br/>200 JSON"]
    App --&gt;|"GET /books/:id"| R3["Lookup req.params.id<br/>200 or 404"]
    App --&gt;|"POST /books"| R4["Validate req.body<br/>201 or 400"]
    App --&gt;|"no match"| R5["Catch-all middleware<br/>404 JSON"]
-->
![Express routing structure visualization: incoming requests enter the Express app, which dispatches top to bottom across GET /, GET /books, GET /books/:id, POST /books, and a fallback 404 handler when no route matches](https://mermaid.ink/img/pako:eNp90MFOwkAQBuBXmcxFjVIK1ktjSFBRMUYINF46HLbdwTZ0u8t2GyTAu5uWYGJCPE4y_5d_ZoeplowhLgu9STNhHURPVAIAjMuYcFymWuXlF7xG0RRmvK65coQL6HQGMDRmRzj6NparqpnuE9sdKOHSDBS7TEu4BiNcRng4mkNjmuSe8GUUQZdwD7NeTGi58iou5eXFg9arCobTsed5F1eEi7PBpNlq0_2Y8DkvHFtItmB57a1rttu2Sd_34W0--fhX6Ya5bKXbmPBd61VtWsYIK1Tl5fKX0hYCPziDTSfzP52CmPBTFLkUjlsr0fLUqHdk_DNMqaH9XWvcxYSPzdQRRQEql7LgjbDcMoEfnA7DG1RslcglhrgjdBkrJgwJJS9FXTjCAx5-AN6glrk=?type=png)

Express gives you three clean places to read incoming data:
- **`req.params`** — dynamic segments from the URL path (`/books/:id` → `req.params.id`).
- **`req.query`** — key/value pairs after `?` in the URL (`/books?author=Asha` → `req.query.author`).
- **`req.body`** — the parsed request body on `POST`/`PUT` requests (populated by `express.json()`).

Because Express stops at the **first** matching route, **static paths must come before dynamic parameter paths**. If you add a `GET /books/featured` route *after* `GET /books/:id`, Express matches `/books/:id` first with `req.params.id` set to `"featured"`, `Number("featured")` evaluates to `NaN`, and your `/books/featured` handler never runs. Always register specific paths like `/books/featured` above `/books/:id`.

## Handling GET requests

Add two `GET` routes to `server.js` — one for the full list (with optional `?author=` filtering) and one for a single book by `:id`:

```js
app.get("/books", (req, res) => {
  const { author } = req.query;
  const list = author
    ? books.filter((b) => b.author.toLowerCase() === String(author).toLowerCase())
    : books;
  res.status(200).json(list);
});

app.get("/books/:id", (req, res) => {
  const id = Number(req.params.id);
  const book = books.find((b) => b.id === id);
  if (!book) return res.status(404).json({ error: "Book not found" });
  res.status(200).json(book);
});
```

Notice `Number(req.params.id)`: URL parameters always arrive as strings (`"1"`), so converting to a number is required before comparing with `===` against numeric IDs.

A helpful rule for choosing between `req.params` and `req.query`: use `req.params` to identify **which** resource the client wants (`/books/1`), and use `req.query` for **optional** filtering, searching, or sorting on a collection (`/books?author=Asha`). Notice also how `/books` returns an empty array `[]` with `200 OK` if no books match a filter, while `/books/99` returns `404 Not Found` because that specific resource does not exist.

Every response in this post came from this small test client (Node's built-in `fetch`). Run `node server.js` in one terminal and `node client.js` in another once all the routes are in place; for the raw example at the top, run the raw server instead and use `node client.js raw`:

```js
// client.js: `node client.js` tests the Express routes, `node client.js raw` the raw server
const base = "http://127.0.0.1:3000";

async function show(method, path, body) {
  const res = await fetch(base + path, {
    method,
    headers: body ? { "Content-Type": "application/json" } : {},
    body: body ? JSON.stringify(body) : undefined,
  });
  const type = (res.headers.get("content-type") || "").split(";")[0];
  console.log(`${method} ${path} -> ${res.status} (${type}) ${await res.text()}`);
}

(async () => {
  if (process.argv[2] === "raw") return show("POST", "/books", { title: "JS Basics" });
  await show("GET", "/");
  await show("GET", "/books");
  await show("GET", "/books?author=Asha");
  await show("GET", "/books/1");
  await show("GET", "/books/99");
  await show("POST", "/books", { title: "Express Guide", author: "Meera" });
  await show("POST", "/books", { title: "No author" });
  await show("GET", "/unknown");
})();
```

Real responses for the `GET` routes from Node.js 24.22.1 and Express 5.3.0:

```text
GET / -> 200 (text/html) Books API is running
GET /books -> 200 (application/json) [{"id":1,"title":"JS Basics","author":"Asha"},{"id":2,"title":"Node Patterns","author":"Ravi"}]
GET /books?author=Asha -> 200 (application/json) [{"id":1,"title":"JS Basics","author":"Asha"}]
GET /books/1 -> 200 (application/json) {"id":1,"title":"JS Basics","author":"Asha"}
GET /books/99 -> 404 (application/json) {"error":"Book not found"}
```

## Handling POST requests

`POST` creates a new resource using data in `req.body`. Always validate incoming fields before saving and return `201 Created` on success:

```js
app.post("/books", (req, res) => {
  const { title, author } = req.body || {};
  if (typeof title !== "string" || !title.trim() || typeof author !== "string" || !author.trim()) {
    return res.status(400).json({ error: "title and author must be non-empty strings" });
  }
  const created = { id: nextId++, title: title.trim(), author: author.trim() };
  books.push(created);
  res.status(201).json(created);
});
```

Real responses for a valid `POST` and an invalid one (missing `author`):

```text
POST /books -> 201 (application/json) {"id":3,"title":"Express Guide","author":"Meera"}
POST /books -> 400 (application/json) {"error":"title and author must be non-empty strings"}
```

Without `app.use(express.json())` registered above this route, `req.body` stays `undefined` and every valid `POST` would hit the `400` branch. You can test both `GET` and `POST` straight from your terminal with `curl` (no extra GUI tool needed) by passing `-X POST`, `-H "Content-Type: application/json"`, and `-d '{"title":"Express Guide","author":"Meera"}'`. Remember to include the `Content-Type` header on every JSON `POST`, because `express.json()` skips bodies sent without it. Also check that your validation handles both missing fields and empty whitespace strings (`!title.trim()`), which prevents blank records from slipping into your store.

## Sending responses cleanly (and catching 404s)

Express gives you several ways to finish a request:
- **`res.send(text)`** — sends plain text or HTML (as seen above, `res.send("Books API is running")` automatically sent `Content-Type: text/html`).
- **`res.json(obj)`** — sends JSON with `Content-Type: application/json`.
- **`res.status(code).json(obj)`** — chains an explicit HTTP status code (`201`, `400`, `404`) before sending JSON.
- **`res.sendStatus(204)`** — sends a status code with an empty body (handy for `DELETE` routes).

Remember that every request can only receive **one** response. In our `GET /books/:id` and `POST /books` handlers, notice the `return` keyword before `res.status(404).json(...)` and `res.status(400).json(...)`. Without `return`, JavaScript keeps executing the rest of the function and calls `res.status(...).json(...)` a second time, throwing `ERR_HTTP_HEADERS_SENT`.

Finally, register a catch-all middleware **at the very bottom** of `server.js` (after every route) so unknown URLs return clean JSON instead of Express's default HTML `Cannot GET /unknown` page, then start listening:

```js
app.use((req, res) => {
  res.status(404).json({ error: `Route ${req.method} ${req.url} not found` });
});

app.listen(3000, () => console.log("Listening on http://127.0.0.1:3000"));
```

```text
GET /unknown -> 404 (application/json) {"error":"Route GET /unknown not found"}
```

## When NOT to reach for Express

Express is a solid default for learning and building Node.js APIs, though it is not always the right pick:
- **A single-endpoint utility or health probe:** Node's built-in `http` module handles one route with zero third-party dependencies.
- **Strict schema validation and TypeScript-first APIs out of the box:** Express leaves validation, logging, and project structure entirely to you. Fastify has built-in JSON Schema validation, and Hono is TypeScript-first, so both put more of that in the box.

## Where this leaves you

Express wraps Node's `http` module so you can map `GET` and `POST` paths to clean handlers, read `req.params`, `req.query`, and `req.body`, and reply with `res.status(...).json(...)` instead of wiring streams and headers by hand.

One honest limit: this walkthrough keeps everything in one `server.js` file with an in-memory `books` array and skips splitting routes into separate files with `express.Router()` or connecting a real database. When you start a new Node.js API today, do you still reach for Express first or go straight to Fastify/Hono?
