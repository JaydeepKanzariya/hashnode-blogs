---
title: "Cookies Aren't Auth: Sessions vs JWT vs Cookies Explained"
slug: sessions-vs-jwt-vs-cookies
subtitle: "What cookies, sessions, and JWTs actually are, stateful vs stateless auth in Express 5.3.0, and how to pick the right one"
tags: nodejs, javascript, web-development, beginners, tutorial
cover: ./cover.png
seoTitle: "Sessions vs JWT vs Cookies: Authentication Explained"
seoDescription: "Sessions vs JWT vs cookies explained: why cookies are transport, stateful vs stateless auth, real Express logout runs, and when to use each."
enableToc: true
---

People compare **sessions vs JWT vs cookies** as if all three were competing authentication systems. They are not.

A **cookie** is not an authentication strategy — it is a **browser storage and transport mechanism**, like an envelope. **Sessions** and **JWTs** are the two authentication strategies you can put *inside* that envelope. You can carry a session ID in a cookie, and you can carry a JWT in a cookie too (or in an `Authorization: Bearer` header).

Once you separate the envelope from the letter, the real architectural choice becomes clear: **stateful sessions vs stateless JWTs**. Every output below comes from a real run on **Node.js 24.22.1**, **Express 5.3.0**, and **jsonwebtoken 9.0.3**.

## What cookies are (the envelope)

A **cookie** is a small key-value string that a server asks the browser to save using the `Set-Cookie` HTTP response header:

```text
Set-Cookie: sid=9f3a...; HttpOnly; Secure; SameSite=Lax; Path=/
```

On every later request to the same domain, the browser attaches that cookie automatically in the `Cookie` request header — no frontend JavaScript required.

Three cookie flags matter in practice:
- **`HttpOnly`** — hides the cookie from `document.cookie`, so JavaScript (including injected XSS scripts) cannot read it.
- **`Secure`** — sends the cookie only over HTTPS connections.
- **`SameSite=Lax` (or `Strict`)** — limits sending the cookie on cross-site requests, reducing CSRF risk.

Because a cookie is only a carrier, it does not decide *how* the server verifies the user. That job belongs to either a session or a JWT.

## What sessions are (stateful authentication)

In **session-based authentication**, the **server stores the user's login state** (in Redis, a database, or memory during local dev) under a random, unguessable **session ID**.

1. User logs in with email and password.
2. Server creates a session record (`sid → { user: "Asha", role: "member" }`) in its session store.
3. Server sends **only the opaque session ID** to the browser in an `HttpOnly` cookie.
4. On every later request, the browser sends the cookie, and the server looks up the session ID in its store.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
sequenceDiagram
    participant B as Browser
    participant S as Express Server
    participant DB as Session Store (Redis/DB)
    B->>S: 1. POST /login (credentials)
    S->>DB: 2. Save sid -> { user, role }
    S--&gt;&gt;B: 3. Set-Cookie: sid=... (HttpOnly)
    B->>S: 4. GET /me (Cookie: sid=...)
    S->>DB: 5. Lookup sid
    DB--&gt;&gt;S: 6. User record
    S--&gt;&gt;B: 7. 200 OK
-->
![Session authentication flow: client posts credentials to /login, server saves user data in the session store (Redis/DB) and returns Set-Cookie with an opaque session ID; on later requests the browser sends the cookie automatically and the server looks up the session ID in the store](https://mermaid.ink/img/pako:eNptjs1KAzEYRV_lktUInbTWPwiYRZyioFAxdTebMPmsoTPJmGSqUvruUquLVtfn3MvZsCZYYoIlehvIN1Q5s4ymqz0A9CZm17je-AwFk6BieE8U_1K9o7OPPlJK0BTX_0nV94emlFzw0DlEQvFE1qVxpU72viql1AKnHI9zvcC4DUvnUTSRLPnsTJt-RF1KWSmBKYc2a0JyFqXEBkOiOEIMLWH7q5ZSKoEzDk25vAlh5UjsFteccxR3Ofdz334eJpxz3M4WGHeE4mhylHDB8RDCauh3fI8qVe5fLjmeE0VEakK0hz1XHNPJBPN7NmIdxc44ywTb1Cy_Ukc1EzWz9GKGNtdsy7ZftQqA-w==?type=png)

Notice why this is called **stateful**: the server remembers who is currently logged in. Delete that row from the session store, and the user is logged out immediately everywhere.

## What JWT tokens are (stateless authentication)

In **JWT (JSON Web Token) authentication**, the **server stores no session record**. Instead, it packs user claims (`sub`, `user`, `role`, `exp`) into a signed token (`header.payload.signature`) and hands the whole token to the client.

1. User logs in with email and password.
2. Server signs a JWT with its secret key and returns it (in JSON or an `HttpOnly` cookie).
3. Client sends the token on later requests (commonly via `Authorization: Bearer <token>`).
4. Server verifies the signature and expiry mathematically — no database or Redis session lookup needed.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
sequenceDiagram
    participant C as Client
    participant S as Express Server
    C->>S: 1. POST /login (credentials)
    Note over S: 2. Sign claims + exp (no DB write)
    S--&gt;&gt;C: 3. Return signed JWT
    C->>S: 4. GET /me (Authorization: Bearer JWT)
    Note over S: 5. jwt.verify(secret) in memory
    S--&gt;&gt;C: 6. 200 OK / 401
-->
![JWT authentication flow: client posts credentials to /login, server signs user claims with its secret key and returns the JWT without writing to a session store; on later requests the client sends Authorization Bearer token and the server verifies the signature and expiry locally](https://mermaid.ink/img/pako:eNptjk1PwkAURf_KzaxKlBYQXXTRRAox0USMJXHTzaR9lGc6M_XNlA8J_90Q3BBdn3Ny71FVriaVKk9fPdmK5qwb0aa0ANBpCVxxp21ADu2Rt0w2_IXFGS72nZD3KEi2JBcpH2ZZkWIc421ZrJC0rmGLqBKqyQbWrR9cxFcXCG5LgiLFJEbBjUXVajYeN6B9h8g6zGfYCQf6jYrhMMvyFHcx3in0YuG5sVTj-WN1tT-N8bRYITGE6LEPGyf8rQM7m2JGWkjOxX9P7mN87kK8JeH1IfJUCYUB2MKQcXK4vvEQYzIaYfmCBNPRWN0qQ2I01ypVx1KFDRkqVVqqmta6b0OpTur0A44Jd5M=?type=png)

Notice why this is called **stateless**: the server keeps no list of active tokens. Any valid, unexpired signature is trusted until its `exp` timestamp passes.

## Stateful vs stateless in action (real Express 5.3.0 run)

To see the sharpest real-world difference, I built both flows in one Express 5.3.0 app (`Map` session store vs `jsonwebtoken` 9.0.3 `HS256` with `expiresIn: "15m"`), logged in, called `/me`, logged out, and replayed the exact same credential. This is the full server:

```js
// server.js (Node.js 24.22.1, Express 5.3.0, jsonwebtoken 9.0.3)
const crypto = require("crypto");
const express = require("express");
const jwt = require("jsonwebtoken");

const app = express();
const SECRET = crypto.randomBytes(32).toString("hex"); // new random secret on every start (demo only)
const sessions = new Map(); // in-memory session store: local demo only, use Redis or a database in production

function getSid(req) {
  const match = /(?:^|;\s*)sid=([^;]*)/.exec(req.headers.cookie || "");
  return match ? match[1] : null;
}

// Both logins skip the password check to keep the focus on state (see the JWT post for a real login)
app.post("/session/login", (req, res) => {
  const sid = crypto.randomBytes(16).toString("hex");
  sessions.set(sid, { user: "Asha", role: "member" });
  res.setHeader("Set-Cookie", `sid=${sid}; HttpOnly; SameSite=Lax; Path=/`);
  res.status(200).json({ loggedIn: true, sidLength: sid.length });
});

app.get("/session/me", (req, res) => {
  const session = sessions.get(getSid(req));
  if (!session) return res.status(401).json({ error: "Session expired or logged out" });
  res.status(200).json({ user: session.user, via: "session" });
});

// Session logout deletes the server record:
app.post("/session/logout", (req, res) => {
  const sid = getSid(req);
  if (sid) sessions.delete(sid);
  // Add Secure over HTTPS in production
  res.setHeader("Set-Cookie", "sid=; Max-Age=0; HttpOnly; SameSite=Lax; Path=/");
  res.status(204).send();
});

app.post("/jwt/login", (req, res) => {
  const token = jwt.sign({ sub: "1", user: "Asha", role: "member" }, SECRET, {
    algorithm: "HS256",
    expiresIn: "15m",
  });
  res.status(200).json({ token });
});

// JWT route verifies signature + expiry with no server store:
app.get("/jwt/me", (req, res) => {
  const header = req.headers.authorization || "";
  if (!header.startsWith("Bearer ")) return res.status(401).json({ error: "Missing token" });
  try {
    const claims = jwt.verify(header.slice(7), SECRET, { algorithms: ["HS256"] });
    res.status(200).json({ user: claims.user, via: "jwt" });
  } catch {
    res.status(401).json({ error: "Invalid or expired token" });
  }
});

app.listen(3000, () => console.log("Listening on http://127.0.0.1:3000"));
```

Run it with `node server.js`, then run this client in a second terminal. Every line below comes from it:

```js
// client.js: run while server.js is listening
const base = "http://127.0.0.1:3000";

(async () => {
  let res = await fetch(base + "/session/login", { method: "POST" });
  console.log("SESSION login  ->", res.status, await res.text());
  const cookie = res.headers.get("set-cookie").split(";")[0]; // sid=...

  res = await fetch(base + "/session/me", { headers: { cookie } });
  console.log("SESSION /me    ->", res.status, await res.text());

  res = await fetch(base + "/session/logout", { method: "POST", headers: { cookie } });
  console.log("SESSION logout ->", res.status);

  res = await fetch(base + "/session/me", { headers: { cookie } }); // replay the old cookie
  console.log("SESSION replay ->", res.status, await res.text());

  res = await fetch(base + "/jwt/login", { method: "POST" });
  const { token } = await res.json();
  console.log("JWT login      ->", res.status, "tokenLength:", token.length);

  const headers = { Authorization: `Bearer ${token}` };
  res = await fetch(base + "/jwt/me", { headers });
  console.log("JWT /me        ->", res.status, await res.text());

  // There is no JWT logout endpoint: the server keeps no record, so the same token still works
  res = await fetch(base + "/jwt/me", { headers });
  console.log("JWT replay     ->", res.status, await res.text());
})();
```

Real output from both flows:

```text
SESSION login  -> 200 {"loggedIn":true,"sidLength":32}
SESSION /me    -> 200 {"user":"Asha","via":"session"}
SESSION logout -> 204
SESSION replay -> 401 {"error":"Session expired or logged out"}
JWT login      -> 200 tokenLength: 181
JWT /me        -> 200 {"user":"Asha","via":"jwt"}
JWT replay     -> 200 {"user":"Asha","via":"jwt"}
```

Two real numbers jump out of that run:
1. **Instant revocation vs waiting for expiry.** Replaying the session cookie after `POST /session/logout` failed immediately with `401`. Replaying the same JWT still returned `200` — there is no server-side logout to call, because a stateless server keeps no record that the user ever logged in.
2. **Credential size.** The random session ID was **32 characters**; the minimal JWT was **181 characters** (nearly 6× larger on every request, and larger still as you add more claims).

## Session vs JWT comparison table

| Dimension | Session-based Auth | JWT-based Auth |
|---|---|---|
| Where state lives | Server (Redis / database) | Client (inside the signed token) |
| Server lookup per request | Yes (read session store) | No (verify signature in memory) |
| Instant logout / ban | Built-in (delete session row) | Hard (valid until `exp`, or add a blocklist) |
| Credential size | Small (e.g., 32-char ID) | Larger (e.g., 181+ chars with claims) |
| Typical transport | `HttpOnly` Cookie | `Authorization: Bearer` header or Cookie |
| Multi-service / mobile APIs | Needs shared session store | Any service with key can verify |
| Scaling trade-off | Must share Redis/DB across instances | Must manage short expiry + refresh tokens |

## When to use each (and when NOT to)

Base the choice on your **clients** and your **revocation requirements**, not hype:

- **Pick Sessions + `HttpOnly` Cookies** for traditional browser web apps, SaaS dashboards, and e-commerce sites served from one backend (or backends sharing Redis). You get instant logout, instant permission changes, small headers, and automatic browser handling. **Do not** use in-memory `Map` sessions in production — they wipe on every server restart and break across multiple instances; use Redis or your database.
- **Pick Short-Lived JWTs** for mobile apps, third-party APIs, and multi-service architectures where downstream services need to verify identity without calling a central session store on every hop. **Do not** give JWTs multi-day lifetimes without a revocation strategy, and **do not** store sensitive secrets in the payload (it is Base64URL-encoded, not encrypted).
- **The common hybrid:** many production teams issue a short-lived JWT access token (5–15 minutes) paired with a stateful refresh token stored in the database and delivered in an `HttpOnly` cookie — giving fast stateless verification on normal API calls while still letting the server revoke refreshes on logout.

## Where this leaves you

Cookies are the transport envelope; sessions (stateful) and JWTs (stateless) are the two authentication models. Sessions win on simplicity and instant revocation for browser apps, while short-lived JWTs win when multiple services or mobile clients need self-contained verification.

One honest limit: the demo above used an in-memory `Map` instead of Redis and skipped OAuth 2.0 / OpenID Connect, CSRF tokens, and refresh-token rotation to stay focused on the core trade-off. For a brand-new full-stack web app today, do you default to cookie sessions or JWTs?
