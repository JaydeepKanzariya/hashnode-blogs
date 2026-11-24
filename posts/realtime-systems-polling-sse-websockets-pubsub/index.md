---
title: "Polling, SSE, WebSockets & Pub/Sub: How Realtime Systems Scale"
slug: realtime-systems-polling-sse-websockets-pubsub
subtitle: "From HTTP request-response to polling, long polling, Server-Sent Events, WebSockets, and Pub/Sub — tradeoffs, diagrams, and choosing the right fit"
tags: system-design, web-development, nodejs, backend, beginners
cover: ./cover.png
seoTitle: "Realtime Systems: Polling, SSE, WebSockets & Pub/Sub"
seoDescription: "How realtime systems work and scale: short polling, long polling, Server-Sent Events (SSE), WebSockets, and Pub/Sub compared with tradeoffs."
enableToc: true
---

**How does WhatsApp deliver a message instantly?**

You do not tap a Refresh button every two seconds to check if your friend replied. The moment they hit Send, the message appears on your screen. Standard HTTP APIs cannot do that on their own — in normal HTTP, the server never speaks first. WhatsApp's own internal protocol is not something I can verify here, so the rest of this post describes the general web patterns behind that experience, not WhatsApp's implementation.

Building systems that push updates as they happen requires choosing among **polling**, **long polling**, **Server-Sent Events (SSE)**, **WebSockets**, and **Pub/Sub**. Notice one crucial distinction up front: the first four describe *how a client talks to a server*, while **Pub/Sub** is a *backend architecture* that lets multiple servers coordinate at scale.

## What makes a system "realtime"?

In web engineering, **realtime** means users see state changes quickly enough that the interaction feels live — without manually reloading the page.

Engineers separate two tiers:
- **Hard realtime:** strict, guaranteed deadlines measured in milliseconds or microseconds (aircraft flight controls, medical devices, braking systems). Missing a deadline is a system failure.
- **Near realtime (soft realtime):** almost every web app belongs here. A chat message arriving in 200ms or a delivery rider moving on a map every 3 seconds feels instant to a human, even though there is no hard physical guarantee.

Five everyday apps rely on near-realtime updates:
- **Chat applications** (WhatsApp, Slack): messages, typing indicators, and read receipts flowing both ways.
- **Notifications** (GitHub, Instagram): a badge updating the second someone mentions you.
- **Live dashboards** (sports scores, stock tickers, server metrics): numbers ticking continuously without a reload.
- **Ride and delivery tracking** (Uber, Swiggy): GPS coordinates updating on a map as the driver moves.
- **Collaborative editing** (Google Docs, Figma): multiple cursors and edits converging on one document.

## Why traditional HTTP request-response isn't enough

Normal HTTP is strictly **client-initiated**. The browser opens a request (`GET /messages`), the server computes a response, sends it back, and the exchange ends. If you want a refresher on how HTTP rides on TCP, see [TCP, UDP and where HTTP fits](https://jaydeepkanzariya.hashnode.dev/tcp-vs-udp-and-http).

The server cannot ring the browser out of the blue when a new chat message arrives. Forcing users to refresh the page breaks the user experience: forms reset, scroll position jumps, and updates stay stale until someone clicks Reload. Every pattern below is a way to work around HTTP's "client must ask first" rule — each with its own cost.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
sequenceDiagram
    participant B as Browser
    participant S as Server
    B->>S: GET /messages
    S--&gt;>B: 200 + current messages
    Note over B,S: Exchange over. A new message reaches the server.
    Note over S: The server cannot contact the browser first
    B->>S: GET /messages (only after the user reloads)
    S--&gt;>B: 200 + the new message
-->
![Traditional request-response: the browser sends GET /messages and the server replies with the current messages; when a new message reaches the server it cannot contact the browser first, so the browser only sees it after the user reloads and sends another GET /messages](https://mermaid.ink/img/pako:eNp9kk1Pg0AQhv_KZE4aKQL9APbQRNR40gs9GS7rMgWSsltnF21t-t8NNKjRxuPMO8_MvJk5oDIloUBLrx1pRXeNrFi2BRcaAGAr2TWq2UrtIANpIWPzbonP6Xmv58Rv33I2WS5zAQ_3K7huyVpZkR21fDJZLjMBURDAFaiOmbSD31VPxhGYN2LIvFzA_U7VUlenlA83oOl9ZIBJqposuJrADnv4f9vkAlZfOiiptXGgjHZSuYF8OTmEdcPW_WcELoze7EGuHfFAdj3GtDGytJfnbfZlP1ZGDytuShSOO_KwJW5lH-Khhwt0NbVUoIACmcpuN1FmY7jAQh_Rw63Uz8a0I82mq2oUa7mx5GG3LaUbz_mVZdIl8a3ptEMRxkMPFAfcoZiFiR8l6SINgzCNp8HUwz2KMIr8WTSPpkkSB0mcpvHRw49hauBHi3C-SMJ5kixmaTz3kMrGGX48vdTwWcdPTDbCqg?type=png)

## Short Polling: ask again every few seconds

**Short polling** is the most direct workaround: the client runs a timer (`setInterval`) and sends a normal HTTP `GET /messages` request every few seconds whether anything changed or not.

**How it works:** Client asks at `t = 0s` → server replies "nothing new." Client asks at `t = 5s` → "nothing new." Client asks at `t = 10s` → server returns the new message.

- **Advantages:** works everywhere with plain HTTP, requires zero special server infrastructure, plays nicely with load balancers and HTTP caches, and is easy to debug.
- **Disadvantages:** wastes bandwidth and server CPU on empty responses; updates are delayed by up to the polling interval; thousands of clients polling every second can overwhelm your API and database.
- **When polling is sufficient:** background status checks (like "is my PDF export finished yet?"), dashboards where a 15–30 second delay is fine, or low-traffic internal admin tools.

## Long Polling: hold the phone until something happens

**Long polling** was introduced to stop the flood of empty responses. The client sends a normal HTTP request, and if no new data exists yet, the server **holds the request open** instead of replying immediately.

The moment new data arrives (or a timeout such as 30 seconds expires), the server sends the response. The client processes it and immediately opens a new long-poll request to wait for the next event.

- **Benefits:** far fewer empty requests than short polling; near-instant delivery once an event occurs; still runs over plain HTTP through corporate proxies and firewalls.
- **Drawbacks:** every open request ties up a connection on the server; high message rates trigger constant reconnects and HTTP header overhead; harder to track message ordering across reconnects.
- **Real-world usage:** historically powered early web chat and notification systems, and still shows up as a fallback when WebSockets are blocked by strict networks (as well as in message queues like AWS SQS long polling).

## Server-Sent Events (SSE): one-way push over HTTP

**Server-Sent Events (SSE)** give you genuine server-to-client push over a single, long-lived standard HTTP connection. The client opens one `GET /events` request (using the browser's built-in `EventSource` API), and the server keeps the response open, writing newline-delimited text events whenever updates happen.

Here is a minimal **Node.js 24.22.1** SSE server. It sends two events 300ms apart and then closes the stream:

```js
// sse-server.js (Node.js 24.22.1, no packages)
const http = require("http");

const scores = [142, 148];

http
  .createServer((req, res) => {
    if (req.url !== "/events") {
      res.writeHead(404);
      return res.end();
    }
    res.writeHead(200, {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
    });

    let id = 0;
    const timer = setInterval(() => {
      id += 1;
      // One event = a few "field: value" lines followed by a blank line
      res.write(`id: ${id}\nevent: score\ndata: ${JSON.stringify({ team: "IND", runs: scores[id - 1] })}\n\n`);
      if (id === scores.length) {
        clearInterval(timer);
        res.end();
      }
    }, 300);
    req.on("close", () => clearInterval(timer));
  })
  .listen(3000, "127.0.0.1");
```

And a client that prints exactly what arrives on the wire (run it in a second terminal while the server is up):

```js
// sse-client.js: run while sse-server.js is listening
(async () => {
  const res = await fetch("http://127.0.0.1:3000/events");
  console.log(`Status: ${res.status} | Content-Type: ${res.headers.get("content-type")}`);

  const decoder = new TextDecoder();
  for await (const chunk of res.body) {
    process.stdout.write(decoder.decode(chunk, { stream: true }));
  }
})();
```

Real output:

```text
Status: 200 | Content-Type: text/event-stream
id: 1
event: score
data: {"team":"IND","runs":142}

id: 2
event: score
data: {"team":"IND","runs":148}
```

- **One-way model:** data flows strictly **server → client**. If the client needs to send something back (like posting a comment), it uses a normal HTTP `POST`.
- **Advantages:** runs over standard HTTP/HTTPS (passes through proxies cleanly), includes automatic browser reconnection with `Last-Event-ID` to resume missed events, and needs no extra client library.
- **Limitations:** unidirectional only; text-based (no raw binary frames); under older HTTP/1.1, browsers cap concurrent connections per origin (typically 6), though HTTP/2 multiplexing removes that pinch.
- **Best fit:** live sports scores, stock price feeds, notification streams, build logs, and streaming LLM responses token by token.

## WebSockets: persistent, bidirectional connections

When both sides need to talk continuously — like two people typing in a chat room or editing a Figma canvas — one-way SSE is not enough. **WebSockets** start with a normal HTTP handshake that asks the server to `Upgrade` the connection. Once upgraded, both sides share a single persistent, **full-duplex** TCP connection where either client or server can push frames at any moment.

**Connection lifecycle:**
1. **Handshake:** client sends an HTTP `Upgrade: websocket` request; server replies `101 Switching Protocols`.
2. **Open:** the persistent socket stays alive; both sides send lightweight text or binary messages with minimal framing overhead (no repeated HTTP headers).
3. **Heartbeat (ping/pong):** periodic checks detect silently dropped connections on flaky mobile networks.
4. **Close:** either side closes the socket; clients typically reconnect with exponential backoff.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
sequenceDiagram
    participant C as Client
    participant S as Server
    Note over C,S: Short Polling (repeated requests)
    C->>S: GET /updates
    S--&gt;>C: 200 (empty)
    C->>S: GET /updates (5s later)
    S--&gt;>C: 200 (new data)
    Note over C,S: Long Polling (server holds the request)
    C->>S: GET /updates
    Note over S: waits until new data exists
    S--&gt;>C: 200 (new data)
    C->>S: GET /updates (reconnects at once)
    Note over C,S: SSE (one-way HTTP stream)
    C->>S: GET /events
    S--&gt;>C: data: event 1
    S--&gt;>C: data: event 2
    Note over C,S: WebSockets (bidirectional)
    C->>S: HTTP Upgrade -> 101 Switching
    C->>S: send message
    S--&gt;>C: push message
-->
![Sequence diagram comparing Short Polling (repeated GET requests with empty replies), Long Polling (the server holds the request until data exists, then the client reconnects at once), SSE (single HTTP request with continuous one-way server push events), and WebSockets (HTTP Upgrade handshake followed by bidirectional messages in both directions)](https://mermaid.ink/img/pako:eNqNk82PmzAQxf-V0ZwSCVIgX-BDLnTVHtpqJVJVqrh4YQpWwab2kI9G-d-rsKUrpclqj_bze_N7suaEhSkJBTr61ZMu6L2SlZVtbnMNANBJy6pQndQMKUgHaaNI8y05u8gZ2R3ZUf5imMDsyELqZQKy2liGR9M0SlcwsdSRZCrBXmY7dtPRl_qbTSbgw8MW3vVdKZncKGW-v9mkAqIggAm1HR9fc8Fk6aCRTHZ6M0DTHkrJcnqH-JPR1QuwG8pBbZrSAdc0gr-F-yU4E7CXih30mlUDIwLQQTl2b8O8WdVSYbSmgh1IBqMLulcryx5gYjT5e3mEj9vtIzi2JNub-bQj_T_XBUfAoEH4mhjdYfhGT5kpfhI7mDypUlkqWBktm2uIge9rV1lZEvgbCIMQsr3iola6unrrSJfQknOyomuornf1qKGHlVUlCrY9ediSbeXliKeLJ0euqaUcBeRoqewPfmEaY3PM9Rk97KT-bkw7uq3pqxrFD9k48vD5O_6u0b9bS7okm5peM4pwPmSgOOEBxSKMZ1GcrJIwCJP1PJh7eEQRRtFsES2jeRyvg3idJOuzh7-HqcEsWoXLVRwu43i1SNZLD6lUbOzn51UeNvr8BxRBMbI?type=png)

- **Why chat apps use WebSockets:** low per-message overhead, instant bidirectional delivery for messages, typing indicators, and presence status, plus native binary support for voice or media chunks.
- **Tradeoffs:** stateful connections complicate load balancing and deploys; proxies and firewalls need WebSocket support; you must build reconnection, heartbeats, and message acknowledgments yourself (or use a library).

## Pub/Sub systems: an architecture, not a protocol

A common mistake is listing **Pub/Sub (Publish–Subscribe)** alongside SSE and WebSockets as if you pick one *instead* of the others. You do not. **SSE and WebSockets are client-server transport protocols. Pub/Sub is a messaging architecture** used on the backend to decouple who produces an event from who consumes it.

In a Pub/Sub system (such as Redis Pub/Sub, Kafka, NATS, or Google Cloud Pub/Sub):
- **Producers (publishers)** emit an event to a named **topic** or **channel** (for example, `chat:room-42` or `orders:created`) without knowing who is listening.
- **The broker** routes that event to every interested **subscriber (consumer)**.
- **Subscribers** react independently — one pushes a WebSocket frame to connected browsers, another sends a mobile push notification, and a third writes an analytics record.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    P1["Chat Service<br/>(Producer)"] --&gt;|"publish<br/>chat:room-42"| B["Pub/Sub Broker<br/>(Topics / Channels)"]
    P2["Order Service<br/>(Producer)"] --&gt;|"publish<br/>orders:new"| B
    B --&gt;|"fan-out"| S1["WebSocket Server<br/>(Subscriber)"]
    B --&gt;|"fan-out"| S2["Mobile Push<br/>(Subscriber)"]
    B --&gt;|"fan-out"| S3["Analytics<br/>(Subscriber)"]
-->
![Publish-Subscribe architecture: producers (Chat Service, Order Service) publish events to topics inside a Pub/Sub Broker without knowing consumers; subscribers (WebSocket Server, Push Notifier, Analytics) subscribe to relevant topics and receive fan-out messages independently](https://mermaid.ink/img/pako:eNqVj01Lw0AQhv_KMCcFQ2j1FKRgelUMRvCQ8bC7mbBLN7tlPyzS9r9LmnhT0PM77_O8c0Tle8YKB-sPSouQ4PGFHABAs-oIt1okaDl8GMX3MpSbqyb4PisO14TvUBSbE-E-S2uivuRKi1QF78fibk14grojbLIs2yyhDn7HYca8-r1REUrYauEc2zjxFvG6I3wOPYd_mf3UiJXjw8U7s-rlcBCu8DlNSTv99cay9WrH83Pfo9osowpGzo7fCdPAJy-NZWjyov9z-bYjfHDCfiaj4k9VvMGRwyhMjxUeCZPmkQkrwp4HkW0iPOP5CxlEj4g=?type=png)

Because producers and subscribers never call each other directly, you can add a new consumer (say, an audit logger) without changing the service that publishes messages.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    A["Order Service"] --&gt;|"publish order.shipped"| B["Pub/Sub Broker"]
    C["Comment Service"] --&gt;|"publish comment.new"| B
    B --&gt;|"fan-out"| N["Notification Service<br/>(subscriber)"]
    N --&gt;|"SSE stream"| W["Open browser tab"]
    N --&gt;|"push provider"| M["Mobile device"]
    N --&gt;|"save unread count"| D[("Notifications DB")]
-->
![Notification delivery system: the Order Service and Comment Service publish events to a Pub/Sub broker, which fans them out to a Notification Service subscriber that pushes to an open browser tab over an SSE stream, to a mobile device through a push provider, and saves the unread count in a notifications database](https://mermaid.ink/img/pako:eNp1kluP2jAQhf-KNU-7UsiScMlF1UoF-lZotTxUasyDEw_EamJHYxu2Bf57lSxUbdU-zuV8c440Z6iMRMhh35hTVQty7OMLJ64ZY-x9weETSSS2RTqqCjns2Gj0fOHQ-bJRtmamH4e2Vl2HksOFLQoOn335tPUlW5D5hsRhdwcuCw5L07ao3f-R1dtCqPE0AO_ixW1vL_TIeNfPNgWHjXFqryrhlNF36LuSnp4frC9tRapEevzNw-aG2W4_MOsIRduTvvRRO9SsJHOySMyJ8h-iztuadWSOSvbBLmxdcFibUjXIJN7y_C2y4ojMa0IhWWW8Hqyvioc_vVu2WnB43EEAB1ISckceA2iRWtGXcO6pHFyNLXLIGQdC6V9HlWkMceD6CgF0Qn81pr2ryfhDDfleNBYD8J0UDldKHEi0v7qEWiIte2OQx9HAgPwMr5BPozSM02yeReMoSybjSQDfIY_iOJzGs3iSpsk4TbIsuQbwY7g6DuN5NJun0SxN59MsmQWAUjlD67cvG57t-hOvysk2?type=png)

## Comparing all approaches

Think of these five patterns in pairs to see where each boundary lies:
- **Short Polling vs Long Polling:** Long polling cuts wasted empty requests and lowers latency, at the cost of holding server connections open.
- **Long Polling vs SSE:** SSE keeps one clean HTTP stream open instead of re-opening a request after every single message, and gives you built-in reconnects.
- **SSE vs WebSockets:** Choose SSE when only the server pushes text updates; choose WebSockets when you need high-frequency two-way traffic or binary frames.
- **WebSockets vs Pub/Sub:** Different layers. WebSockets connect *users to a server*; Pub/Sub connects *servers and services to each other*.

| Approach | Layer | Direction | Connection | Best For | Main Tradeoff |
|---|---|---|---|---|---|
| Short Polling | Client–Server | Client → Server | Repeated HTTP | Low-frequency status checks | Wasted requests & delay |
| Long Polling | Client–Server | Client → Server (held) | Repeated held HTTP | Fallback when push is blocked | Reconnect overhead under load |
| SSE | Client–Server | Server → Client (1-way) | Single HTTP stream | Feeds, scores, logs, AI streams | One-way text only |
| WebSockets | Client–Server | Bidirectional (full-duplex) | Persistent TCP upgrade | Chat, gaming, collab editing | Stateful connections to manage |
| Pub/Sub | Backend Architecture | Many → Many (via topics) | Broker-mediated | Fan-out & horizontal scaling | Extra broker infrastructure |

## Building realtime systems at scale

Running a WebSocket chat server on one laptop is straightforward: keep a `Map` of connected users in memory and forward messages between them. Production breaks that assumption immediately:

1. **Horizontal scaling and connection state:** Once you run two servers behind a load balancer, **User A** might hold a WebSocket on **Server 1** while **User B** holds a WebSocket on **Server 2**. Server 1's memory has no socket for User B. The standard fix is **Pub/Sub**: Server 1 publishes User A's message to a shared broker (such as Redis Pub/Sub), Server 2 is subscribed to that room's topic, and Server 2 pushes the frame down User B's WebSocket.
2. **Handling thousands of open connections:** Each idle socket consumes file descriptors and memory. Non-blocking runtimes (like Node.js or Go) handle many concurrent connections per instance, and you need raised OS file-descriptor limits, load-balancer idle timeout tuning, and sticky sessions if you use multi-request fallback transports (like Socket.IO's HTTP long-polling handshake).
3. **Reliability and message delivery:** Mobile networks drop constantly. A WebSocket disconnect should never silently lose chat messages. Production systems persist messages to a database, assign monotonically increasing IDs or timestamps, and let reconnecting clients fetch anything missed since their last acknowledged ID (SSE's `Last-Event-ID` models this directly).

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    UA["User A"] <--&gt;|"WebSocket"| LB["Load Balancer"]
    UB["User B"] <--&gt;|"WebSocket"| LB
    LB <--&gt; S1["WS Server 1<br/>(holds User A)"]
    LB <--&gt; S2["WS Server 2<br/>(holds User B)"]
    S1 --&gt;|"1. publish msg"| Broker["Shared Pub/Sub Broker<br/>(e.g. Redis / NATS)"]
    Broker --&gt;|"2. deliver to subscriber"| S2
-->
![Realtime system horizontal scaling architecture: User A connects via WebSocket through a Load Balancer to Server 1, and User B connects to Server 2; when User A sends a message, Server 1 publishes it to a shared Pub/Sub Broker (e.g. Redis), which delivers it to Server 2 to push down User B's WebSocket](https://mermaid.ink/img/pako:eNp1kMFqwkAQQH9lmFMLNSE5BhGy5yDFVTxkPOxmRxPcuLKbtAfjv5c0qVJKrzPzHo-5YeUMY4ZH6z6rWvkOig1dAAB2eUm4C-whJzzAcrFYDYR71tJVZ-4IByhESVg4ZUAoqy4Ve8LDTIsfWvxPT6eF-F6DTErCvQTJ_oM9JEvt49VL7awJMHW8PvQPJv3FpH8Y8WRkAlNFEsG117YJNbThNKYI787sS0JZK88G3nsdy17P80nK0SmCDZsmQAzrfCuf5ulstqcRGLbNmNM5CL0OlW_0-JoBZIpv2LJvVWMwwxthV3PLhBmh4aPqbUd4x_sX7fx8nA==?type=png)

## Choosing the right approach (and when NOT to use realtime)

Match the simplest tool to the actual direction and frequency of updates:

| Use Case | Recommended Setup | Why |
|---|---|---|
| Chat applications (web chat, Slack-style) | WebSockets + Pub/Sub | High-frequency bidirectional messages, typing, presence, scaled across servers |
| Notification systems | SSE (or WebSockets if already open) + Pub/Sub | Server-to-client push; Pub/Sub fans out events from multiple services |
| Live sports scores | SSE (or short polling for low budgets) | Strictly one-way updates; easy CDN/HTTP compatibility |
| Stock market dashboards | SSE or WebSockets | High-frequency price ticks; WebSockets if users also place live orders |
| Collaborative editing (Docs, Figma) | WebSockets + Pub/Sub | Continuous low-latency bidirectional edits and cursor positions |
| IoT systems | MQTT (Pub/Sub protocol) or WebSockets | Thousands of constrained devices publishing telemetry to topics |

**When NOT to add realtime complexity:** If your data only changes every few minutes — an analytics report, an e-commerce product page, or a weekly billing summary — do not maintain persistent sockets or a Pub/Sub broker. Normal HTTP caching or a 30-second poll is cheaper, simpler to operate, and far less likely to break during deploys.

## Where this leaves you

Start with the simplest pattern that meets your latency needs: short polling for occasional checks, SSE for one-way live feeds, WebSockets for two-way interactive apps, and Pub/Sub behind your servers once a single instance is no longer enough.

One honest limit: this guide stayed at the architectural level and skipped low-level WebSocket frame internals, backpressure handling for slow consumers, and exactly-once delivery guarantees in distributed brokers like Kafka. Which realtime feature are you planning to build next — notifications, a live dashboard, or a chat app?
