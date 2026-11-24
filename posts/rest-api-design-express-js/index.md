---
title: "Stop Naming Routes /getUsers: REST API Design in Express.js"
slug: rest-api-design-express-js
subtitle: "Resources, HTTP methods, status codes, and a working users API in Express.js 5.3.0, with real HTTP responses"
tags: nodejs, javascript, web-development, beginners, tutorial
cover: ./cover.png
seoTitle: "REST API Design with Express.js: Routes and Status Codes"
seoDescription: "Design clean REST APIs in Express.js: resource-based routes, GET/POST/PUT/DELETE, HTTP status codes, and a working users API with real responses."
enableToc: true
---

Almost every first Express.js API ends up with routes like these:

```js
// ❌ verbs in URLs: ignores what HTTP methods already do (handlers omitted)
app.get("/getUsers", listUsers);
app.post("/createUser", createUser);
app.post("/updateUser", updateUser);
app.get("/deleteUser", deleteUser);
```

They work until the project grows to twenty resources, and then nobody remembers whether it is `/removeOrder`, `/deleteOrder`, or `/orders/delete`. **REST** solves that by keeping URLs focused on nouns and letting HTTP methods describe the action.

Every response below comes from a real run on **Node.js 24.22.1** and **Express 5.3.0**.

## What a REST API means

An **API** (Application Programming Interface) is the contract between a client (a browser, a mobile app, or another backend) and a server. The client sends an HTTP request asking for data or an action; the server processes it and sends back an HTTP response with a status code and a body (usually JSON).

If you want a refresher on how HTTP rides over TCP before writing routes, see [TCP, UDP and where HTTP fits](https://jaydeepkanzariya.hashnode.dev/tcp-vs-udp-and-http).

**REST** (Representational State Transfer) is a set of conventions built on top of HTTP. Instead of inventing a custom URL for every action, a REST API exposes **resources** at predictable paths and uses standard HTTP methods and status codes so any client knows what to expect.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    C["Client<br/>browser / app / curl"] --&gt;|"HTTP Request<br/>POST /users + JSON"| S["Express.js Server<br/>route + express.json()"]
    S --&gt;|"HTTP Response<br/>201 Created + JSON"| C
-->
![REST request-response lifecycle: the client sends an HTTP request with method, path, headers and optional JSON body (for example POST /users) to the Express.js server; the server matches the route, runs middleware and logic, and sends back an HTTP response with a status code like 201 Created and a JSON body](https://mermaid.ink/img/pako:eNpVjsFqwlAQRX_lMqsWa1O7DMVNEIqUKr7sHBfPZEQlyYsz76mg_ntBobTrey7nXKgKtVBOmyacqq3XiK8FdwBQLJmKZidd_FhrNl5rOJkoMvi-R4YqacO0wnA4vjJ9luUcCzkksQc-n7kSWTJRwwBTN_tmusItmSbnXsXsdW9wokfRO68hRcEA8ruG7umZafWIcf891ofO5H58fxuhUPFR6j-igl6oFW39rqacLkxxK60w5Uy1bHxqItONbj_-zlGW?type=png)

## Resources and clean route naming

A **resource** is a noun your application manages: `users`, `posts`, `orders`, `products`. In this post, we will design everything around one resource: **`users`**.

Four naming rules keep routes predictable:
- **Use plural nouns, not verbs:** `/users`, not `/getUsers` or `/user`.
- **Use path parameters for a single item:** `/users/3` identifies user `3` inside the `users` collection.
- **Stay lowercase and hyphenated** for multi-word resources (`/order-items`, not `/orderItems`).
- **Keep nesting shallow:** `/users/3/orders` is clear; `/users/3/orders/9/items/2/notes` is hard to maintain.

With those rules in place, the entire `users` API only needs **two paths**: `/users` and `/users/:id`.

## HTTP methods: GET, POST, PUT, DELETE

Because the URL names the **thing** (`/users`), the HTTP method names the **action**:

| CRUD Action | HTTP Method | Route | Meaning | Typical Status |
|---|---|---|---|---|
| Create | `POST` | `/users` | Add a new user to the collection | `201 Created` |
| Read (all) | `GET` | `/users` | Fetch the list of users | `200 OK` |
| Read (one) | `GET` | `/users/:id` | Fetch one user by ID | `200 OK` / `404` |
| Update | `PUT` | `/users/:id` | Replace the user's fields | `200 OK` / `400` / `404` |
| Delete | `DELETE` | `/users/:id` | Remove the user | `204 No Content` |

Two details trip beginners up:
- **`GET` should never change data.** Putting a delete action behind `GET /deleteUser` is dangerous because browsers, caches, and crawlers assume `GET` requests are safe to repeat or prefetch.
- **`PUT` replaces the resource.** Send the full updated object (`name` and `role`). For partial updates (changing only `role`), APIs use `PATCH`, which I am leaving out here to keep the core four clear.

## Status codes basics

Status codes tell the client what happened without forcing it to parse an error message string. Six codes cover almost everything you need early on:

- **`200 OK`** — the request succeeded and the response body has the result.
- **`201 Created`** — a `POST` created a new resource (return the created object). Many APIs also set a `Location: /users/3` header on `201` responses so the client knows where the new resource lives.
- **`204 No Content`** — the request succeeded (common for `DELETE`) and there is no response body.
- **`400 Bad Request`** — the client sent invalid or missing input (for example, an empty `name`).
- **`404 Not Found`** — no resource matches that ID or route.
- **`500 Internal Server Error`** — something broke on the server side.

Never return `200 OK` with `{ "error": "User not found" }`. HTTP clients, monitoring tools, and `fetch` checks (`res.ok`) rely on the status code, not your custom JSON keys.

## Building the users REST API in Express.js

In an empty folder, run `npm init -y` and `npm install express@5.3.0`, then save this as `server.js`. We use an in-memory array so you can run and test it immediately without setting up a database:

```js
// server.js (Node.js 24.22.1, Express 5.3.0)
const express = require("express");

const app = express();
app.use(express.json()); // parse incoming JSON request bodies

let nextId = 3;
const users = [
  { id: 1, name: "Asha", role: "admin" },
  { id: 2, name: "Ravi", role: "member" },
];

app.get("/users", (req, res) => {
  res.status(200).json(users);
});

app.get("/users/:id", (req, res) => {
  const id = Number(req.params.id);
  const user = users.find((u) => u.id === id);
  if (!user) return res.status(404).json({ error: "User not found" });
  res.status(200).json(user);
});

app.post("/users", (req, res) => {
  const { name, role = "member" } = req.body || {};
  if (typeof name !== "string" || !name.trim()) {
    return res.status(400).json({ error: "name must be a non-empty string" });
  }
  const created = { id: nextId++, name, role };
  users.push(created);
  res.status(201).json(created);
});
```

And the `PUT` and `DELETE` routes in the same file, followed by `app.listen`:

```js
app.put("/users/:id", (req, res) => {
  const id = Number(req.params.id);
  const index = users.findIndex((u) => u.id === id);
  if (index === -1) return res.status(404).json({ error: "User not found" });

  const { name, role } = req.body || {};
  if (typeof name !== "string" || !name.trim() || typeof role !== "string" || !role.trim()) {
    return res.status(400).json({ error: "name and role must be non-empty strings" });
  }
  users[index] = { id, name, role };
  res.status(200).json(users[index]);
});

app.delete("/users/:id", (req, res) => {
  const id = Number(req.params.id);
  const index = users.findIndex((u) => u.id === id);
  if (index === -1) return res.status(404).json({ error: "User not found" });
  users.splice(index, 1);
  res.status(204).send();
});

app.listen(3000, () => console.log("Listening on http://127.0.0.1:3000"));
```

One line beginners forget: **`app.use(express.json())`**. Without it, `req.body` is `undefined` on `POST` and `PUT` requests, and your validation will reject every valid payload with `400`.

## Real requests and real responses

I ran the server on Node.js 24.22.1 with Express 5.3.0 and sent seven HTTP requests in sequence — listing users, creating a user, sending a bad payload, fetching the new user, updating it, deleting it, and fetching it again after deletion. This is `client.js`; run the server in one terminal (`node server.js`) and the client in another (`node client.js`):

```js
// client.js (uses the fetch built into Node.js 24)
const base = "http://127.0.0.1:3000";

async function call(method, path, body) {
  const res = await fetch(base + path, {
    method,
    headers: body ? { "content-type": "application/json" } : {},
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  console.log(`${method} ${path} -> ${res.status} ${res.statusText}` + (text ? `\n  ${text}` : ""));
}

(async () => {
  await call("GET", "/users");
  await call("POST", "/users", { name: "Meera" });
  await call("POST", "/users", { role: "editor" });
  await call("GET", "/users/3");
  await call("PUT", "/users/3", { name: "Meera", role: "editor" });
  await call("DELETE", "/users/3");
  await call("GET", "/users/3");
})();
```

Here is the real output:

```text
GET /users -> 200 OK
  [{"id":1,"name":"Asha","role":"admin"},{"id":2,"name":"Ravi","role":"member"}]
POST /users -> 201 Created
  {"id":3,"name":"Meera","role":"member"}
POST /users -> 400 Bad Request
  {"error":"name must be a non-empty string"}
GET /users/3 -> 200 OK
  {"id":3,"name":"Meera","role":"member"}
PUT /users/3 -> 200 OK
  {"id":3,"name":"Meera","role":"editor"}
DELETE /users/3 -> 204 No Content
GET /users/3 -> 404 Not Found
  {"error":"User not found"}
```

Every single status code tells the story on its own: `201` when Meera was created, `400` when `name` was omitted, `204` with no body on deletion, and `404` once user `3` was gone.

## When NOT to force strict REST (and what production needs)

REST fits CRUD resources cleanly, but not every endpoint is a noun. Actions like `/auth/login`, `/payments/refund`, or `/search` are awkward to twist into fake resources — an explicit `POST` action route is clearer than forcing a pretend noun. If your frontend needs deeply nested, client-driven queries across many tables in one round trip, GraphQL or tRPC may fit better than dozens of REST endpoints.

Before shipping this `users` API beyond a local demo, four things are missing:
- **Persistence:** the in-memory array wipes on every server restart; swap it for a database.
- **Validation & auth:** validate field types with a schema library (like Zod) and protect write routes with authentication and authorization checks.
- **Error middleware:** by default, Express 5.3.0 answers malformed JSON with a `400` HTML page, and outside `NODE_ENV=production` that page includes the full stack trace. Add an error-handling middleware `(err, req, res, next)` so clients always get JSON, such as `400 {"error":"Invalid JSON body"}`.
- **Pagination:** `GET /users` returning every row breaks once the table grows.

## Where this leaves you

Keep your URLs plural nouns (`/users`, `/users/:id`), let `GET`, `POST`, `PUT`, and `DELETE` express the action, and return honest HTTP status codes (`200`, `201`, `204`, `400`, `404`). That convention alone makes an Express.js API predictable for anyone calling it.

One honest limit: this post skipped `PATCH`, query-string filtering/pagination (`?role=admin&limit=20`), and API versioning (`/api/v1/users`) to stay focused on the core mechanics. Where do you draw the line between pure REST nouns and action routes like `POST /login`?
