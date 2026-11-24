---
title: "Kafka Explained: Events, Partitions, and Consumer Groups"
seoTitle: "Kafka Explained: Events, Partitions, and Consumer Groups"
seoDescription: "Learn how Apache Kafka processes millions of events using topics, partitions, append-only logs, and consumer groups — and how it differs from queues."
subtitle: "How large applications stream millions of events without drowning in tightly coupled services"
slug: kafka-events-partitions-consumer-groups
tags: kafka, system-design, backend, event-driven, web-development
cover: ./cover.png
enableToc: true
saveAsDraft: false
ignorePost: false
---

How does a large application process millions of events every day?

Think about what happens the moment you tap **Place Order** on a food delivery app. Your payment gets charged, the restaurant's tablet chimes, a nearby driver is matched, an SMS confirmation fires, your order history updates, and an analytics pipeline records what cuisine is trending in your neighborhood — all within seconds.

If the checkout service tried to call every one of those services directly over HTTP, one slow notification provider or a crashed analytics server would stall checkout for every hungry customer. Modern high-scale systems avoid that trap by switching from direct calls to **event streaming** — and **Apache Kafka** is the backbone many of them run on.

## Why systems need event streaming

In a small app, traditional **request-response** communication (REST or RPC calls between services) works fine. Service A calls Service B, waits for `200 OK`, and moves on. (If you want a refresher on how those APIs are structured, see [REST API design in Express.js](https://jaydeepkanzariya.hashnode.dev/rest-api-design-express-js).)

As the product grows, direct service-to-service calls create **tight coupling**:

- **Availability chains:** if Checkout calls Payments, Inventory, Email, Fraud, and Analytics synchronously, a slowdown in Email can make Checkout time out.
- **Brittle fan-out:** every time the business adds a new downstream feature (like a loyalty-points service), someone has to modify Checkout's code to call yet another endpoint.
- **Traffic spikes overwhelm slow receivers:** during a dinner-hour surge or an e-commerce flash sale, Checkout might generate 10,000 orders per second while the email sender can only process 1,000. Without a buffer between them, requests pile up and crash the slower service.

**Event-driven systems** break that coupling. Instead of commanding five downstream services directly, Checkout emits one fact — *"Order 101 was placed"* — into a shared event log. Every interested service reads that fact at its own pace, without Checkout ever knowing who is listening.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    subgraph Direct["Direct calls (tight coupling)"]
        direction TB
        C1["Checkout"] --&gt;|"HTTP"| P1["Payments"]
        C1 --&gt;|"HTTP"| I1["Inventory"]
        C1 --&gt;|"HTTP"| E1["Email"]
        C1 --&gt;|"HTTP"| A1["Analytics"]
    end
    subgraph Events["Event-driven (loose coupling)"]
        direction TB
        C2["Checkout"] --&gt;|"publish order_created"| K["Kafka topic: orders"]
        K --&gt; P2["Payments"]
        K --&gt; I2["Inventory"]
        K --&gt; E2["Email"]
        K --&gt; A2["Analytics"]
    end
    Direct ~~~ Events
-->
![Tight coupling versus event-driven: on the left, Checkout calls Payments, Inventory, Email and Analytics directly over HTTP; on the right, Checkout publishes one order_created event to the Kafka topic orders and Payments, Inventory, Email and Analytics each read it independently](https://mermaid.ink/img/pako:eNqVk1tr2zAUgP-KOE8dOCFWLr48DLI0sJANwsjTolJU6cQWlSUjy12zNPntRXE7SrouTE_S0XcufEh7EFYi5LDV9pcoufPk2w_mmCGEkKa9KxyvS3KtHAq_YdBtiOBaN-TKq6L0RNi21soUnxjcvGaGJU-ssoasv7yNz-INg1mJ4t62nsEN6fU-PzH4ul6vGDyRVbhe8V2FxjdnJWfxGbwI8MI8oPHW7S7R80DPK670JXIayKnheueVeDsFGvnOzjy0b0LpsOlJpx7QkCttbYP_b4f-1U7d3mnVlMQ6ie5WOOQeZZh0uWGw5Nt7Trytlcg74lzcMpQhK_qx2o5Y0H_47JA5_UBidz2ll829vKLj8fjiDiIonJKQe9diBBW6iocj7EMCA19ihQxywsChbB97wmrrGDBzgAhqbn5aW71mO9sWJeRbrhuMoK0l93iteOF49Sfq0Eh0M9saD_lwdKoB-R4eIR_FaZ-m2SSLB3GWDAfDCHaQx5T2R3RMh2maDNIky5JDBL9PXQd9OonHkzQep-lklCXjCFAqb9337medPtjhGcCWCRc?type=png)

## What is Kafka?

**Apache Kafka** is a distributed **event streaming platform** originally built at LinkedIn to move massive volumes of activity data (page views, clicks, logs, and service events) reliably between systems.

The easiest mental model for Kafka is a **shared, append-only notebook** (a commit log) stored on disk across a cluster of servers:

- Services write new entries to the end of the notebook.
- Other services read entries from wherever they left off.
- Unlike a traditional to-do queue that erases an item the instant someone grabs it, Kafka **keeps entries around** for a configured retention window (for example, 7 days) so multiple teams can read the same stream independently — or rewind and replay history when needed.

Teams reach for Kafka for high-throughput activity tracking, real-time analytics, microservice communication, payment audit trails, and recommendation pipelines.

## Understanding events

Everything in Kafka starts with an **event** (also called a record or message). An event is an immutable record of something that already happened in your system.

Common examples include:
- **User signup:** `user_signed_up`
- **Order creation:** `order_created`
- **Payment completion:** `payment_completed`
- **Notifications:** `delivery_eta_updated`

Each event carries a **key** (used for routing and ordering), a **value** (the payload), and a **timestamp**:

```json
{
  "key": "ord-101",
  "event": "order_created",
  "restaurantId": "rest-44",
  "total": 420,
  "timestamp": "2026-06-14T19:12:04Z"
}
```

An event's lifecycle has two sides:
- **Producers** are services that create and publish events to Kafka (such as the Checkout API or Driver App).
- **Consumers** are services that read and process those events (such as the Notification Service or Fraud Detector).

Producers never wait for consumers to finish processing. Once Kafka confirms the event is safely written, the producer moves on.

## Topics in Kafka

If every service dumped all its events into one giant pile, consumers would spend most of their time throwing away data they do not care about. Kafka organizes events into **topics**.

A **topic** is a named category or feed of related events — like folders in a filing cabinet:
- `orders` for order lifecycle events
- `payments` for charges and refunds
- `user-activity` for clicks, searches, and views
- `delivery-updates` for driver GPS pings

Topics support **multiple producers and multiple consumers** at the same time. Three checkout servers can all write to `orders`, while Billing, Notifications, and Analytics all read from `orders` independently without stepping on each other's toes.

## Partitions explained

Now suppose your food delivery app grows from 1,000 orders a day to 5 million. If the `orders` topic were a single file on a single machine, one disk and one consumer could never keep up.

Kafka solves this by splitting every topic into **partitions** — smaller, independent, ordered logs that can live on different servers in the cluster.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    P["Order Service<br/>(Producer)"]
    subgraph Topic["Topic: orders"]
      P0["Partition 0: offset 0 → 1 → 2"]
      P1["Partition 1: offset 0 → 1 → 2"]
      P2["Partition 2: offset 0 → 1 → 2"]
    end
    P --&gt;|"key: ord-101"| P0
    P --&gt;|"key: ord-204"| P1
    P --&gt;|"key: ord-309"| P2
-->
![Diagram of a Kafka Producer (Order Service) routing events by order key into three separate Partitions (Partition 0, Partition 1, Partition 2) inside the orders topic, each with sequential offsets 0, 1, 2](https://mermaid.ink/img/pako:eNqFkMFqAjEQhl9lmFMFlyaxly7FJygYtLeNh5jMuqHuRmazFVGvPkAfsU9STEupB_Eyc_j-D2b-A7roCUusN3HnGssJXuemAwDQlcEZe2JYEH8ERy8rfpw-aI5-cMQjg8ufYD-s1my3DbzFbXCVwbxLiBe5_4sBaFEZ1JZTSCF2IEqIdd1TAgFf50-Qear_grwS5H1BXQnqjkCd__0VimJ6NPhO-3x3IYU0eAQtbnAlnjKXN_hEPGeucIwtcWuDx_KAqaH20ran2g6bhKfTNxn6eHY?type=png)

Three rules make partitions click:

1. **Every event gets a sequential offset:** inside a partition, events are numbered `0, 1, 2, 3...`. Offsets are immutable — new events only ever append to the end.
2. **Ordering is guaranteed *within* a partition, not across the whole topic:** if a producer attaches a key like `ord-101`, Kafka hashes that key so every event for `ord-101` (`order_created` → `payment_completed` → `order_delivered`) lands in the **same partition** in exact order. Meanwhile, `ord-204` can land in a different partition and be processed in parallel.
3. **Partitions are the unit of parallelism:** a topic with 1 partition can only be read by 1 consumer in a group at a time; a topic with 12 partitions lets up to 12 consumers chew through the backlog simultaneously.

## Why Kafka is fast

People often assume anything that writes to disk must be slow. Kafka achieves very high throughput by leaning into how modern disks and operating systems actually work (this post does not benchmark it, so it gives no throughput figure):

- **Append-only sequential writes:** random disk seeks are slow, but appending bytes sequentially to the end of a file is extraordinarily fast on both SSDs and spinning disks. Kafka never edits or deletes individual rows in the middle of a log.
- **OS page cache:** Kafka writes to and reads from the operating system's memory-backed page cache instead of maintaining a bloated in-process object cache. Freshly written events are often served to consumers straight out of RAM without touching the physical disk again.
- **Batching and compression:** producers group many small events into compressed batches before sending them over the network, amortizing network round-trips.
- **Zero-copy transfers:** when serving unencrypted traffic, Kafka lets the OS kernel stream bytes directly from the page cache to the network socket without copying payloads back and forth through application memory.

## Consumer groups

**Consumer groups** are the most misunderstood concept in Kafka — and the reason Kafka can act like *both* a work queue and a publish-subscribe broadcast system at the same time.

A **consumer group** is a team of consumer instances that share the same group ID and cooperate to process a topic.

Two rules govern how consumer groups work:

1. **Within one consumer group, each partition is read by at most one consumer.** If `orders` has 3 partitions and Group A (Notifications) runs 2 consumer instances, Kafka assigns Partitions 0 and 1 to Consumer 1 and Partition 2 to Consumer 2. In steady state, no two consumers in the same group read from the same partition at the same time.
2. **Different consumer groups read the same topic completely independently.** Group B (Analytics) tracks its own offsets and receives *all* 3 partitions, regardless of what Group A has already read.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    subgraph Topic["Topic: orders (3 Partitions)"]
      P0["Partition 0"]
      P1["Partition 1"]
      P2["Partition 2"]
    end
    subgraph G1["Group A: Notifications"]
      C1["Consumer 1"]
      C2["Consumer 2"]
    end
    subgraph G2["Group B: Analytics"]
      C3["Consumer 3"]
    end
    P0 --&gt; C1
    P1 --&gt; C1
    P2 --&gt; C2
    P0 -.-&gt; C3
    P1 -.-&gt; C3
    P2 -.-&gt; C3
-->
![Diagram showing Topic orders with 3 Partitions feeding two independent Consumer Groups: inside Group A (Notifications), Consumer 1 reads Partitions 0 and 1 while Consumer 2 reads Partition 2; independently, Group B (Analytics) has Consumer 3 reading all 3 partitions](https://mermaid.ink/img/pako:eNp9kbFqwzAURX_l8qYWkmLLm4ZC6iFLKaZkizOokhwLbMnIMqWE_Htw0jpSC53E4Tzd--CdSDqliVPTuU_ZCh_w-l5bABinj6MXQ4udG4zc13R9OZxX2o94KFAJH0wwzo6PNR1uv4Aq29e0KGSxyhOVx4olii1KW_Vrn-2csvVuGrDheHPBNEaK6x5RYDlPlc6OU699UlWy2PzbxJamF46NFd1XMDJpKeKs4m9WlWG9fkaZf2OeIrshuw8_zVzcpxNmP0wr6rXvhVHETxRa3c9HVLoRUxfofL4AqzCI0g?type=png)

That design gives you three huge properties out of the box:

- **Horizontal scaling:** if Notifications falls behind during a dinner rush, spin up a 3rd consumer instance in Group A. Now each of the 3 consumers owns 1 partition. (Note the ceiling: adding a 4th consumer to a 3-partition topic leaves that 4th consumer **idle**, because a partition cannot be split across two consumers in the same group.)
- **Fault tolerance:** if Consumer 2 crashes, Kafka detects the missed heartbeats and automatically hands Partition 2 over to Consumer 1, which resumes from Consumer 2's last committed offset.
- **Rebalancing:** that automatic redistribution of partitions whenever a consumer joins, leaves, or crashes is called a **rebalance**. Rebalances keep the group resilient, though frequent restarts can briefly pause processing on reassigned partitions.

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    subgraph Before["Before: 2 consumers, 3 partitions"]
        direction TB
        BP0["Partition 0"] --&gt; BC1["Consumer 1"]
        BP1["Partition 1"] --&gt; BC1
        BP2["Partition 2"] --&gt; BC2["Consumer 2"]
    end
    subgraph After["After: Consumer 3 joins, group rebalances"]
        direction TB
        AP0["Partition 0"] --&gt; AC1["Consumer 1"]
        AP1["Partition 1"] --&gt; AC2["Consumer 2"]
        AP2["Partition 2"] --&gt; AC3["Consumer 3"]
    end
    subgraph Idle["A 4th consumer has no partition left"]
        direction TB
        IC4["Consumer 4<br/>idle"]
    end
    Before ~~~ After
    After ~~~ Idle
-->
![Scaling consumers in a group: with 2 consumers and 3 partitions, Consumer 1 reads Partitions 0 and 1 and Consumer 2 reads Partition 2; after Consumer 3 joins and the group rebalances, each consumer owns one partition; a 4th consumer would have no partition left and sit idle](https://mermaid.ink/img/pako:eNqNU1GPmzAM_iuWn2kHgbaAppMoezlpk6ppT2vuIQVTmCBBJmi3Ve1vn6DXHt3W7fKS2PH3xZ9jHzAzOWGMRW2-Z6ViCx8_S5YaAKDrd3tWbQlrKgzTVuL5EIOAzOiub4g7B3xoFdvKVkZ3Ep8u6GHlFVM2XMCX9dS_3rhbiZsLDFyJTzCbPcA69bYS0xdy8H7jW2-8G5w3wd3GiZs48Ronpvxiwk86_0N4UljircRxj-GK8-GbqXTnwJ5N3wLTTtVKZ_RW_ck9_cm_9Sf39Cf3dZ1xd-qRpP4U5_-nHo95PbRBAoEtry0ApepAm9cugJoK-8ZKPKbBNIHg_Y7fPVR5TX_P5NyAcDqdzn9z8Y_G6B5SRAf3XOUYW-7JwYa4UYOJhyFaoi2pIYkxSGTK--dZZmrDEqU-ooOt0l-NaS5oNv2-xLhQdUcO9m2uLH2o1J5Vc_Uy6Zw4Nb22GPvhyIHxAZ8xDrxwLsJoGXmuF61813fwB8aeEPNALIQfhis3XEXR6ujgz_FVdy6W3mIZeoswXAbRauEg5ZU1_Ok8qePAHn8BjVwj3g?type=png)

## Kafka architecture at a glance

Putting every building block together into one picture shows how a real food-delivery or e-commerce platform streams events across teams:

<!-- mermaid source: arrows are written as --&gt; so this comment stays hidden; replace &gt; with > before reusing
flowchart LR
    subgraph Producers["Producers"]
      Pr1["Checkout API"]
      Pr2["Delivery App"]
    end
    subgraph Cluster["Kafka Cluster (Brokers)"]
      T1["Topic: orders<br/>(P0, P1, P2)"]
      T2["Topic: delivery-updates<br/>(P0, P1, P2)"]
    end
    subgraph Groups["Consumer Groups"]
      CG1["Payments Group"]
      CG2["Notifications Group"]
      CG3["Analytics Group"]
    end
    Pr1 --&gt; T1
    Pr2 --&gt; T2
    T1 --&gt; CG1
    T1 --&gt; CG2
    T1 --&gt; CG3
    T2 --&gt; CG3
-->
![End-to-end Kafka architecture: Producers (Checkout API, Delivery App) publish to Topics (orders, delivery-updates) hosted across Kafka Brokers; independent Consumer Groups (Payments, Notifications, Analytics) subscribe to the topics they need](https://mermaid.ink/img/pako:eNp9ktFKwzAUhl_lcK4mbGi7uyGDWWGIIkF613iRJac2rG3KSaKMsXeX0m1uVbzLl-9Pzk_IHrUzhAssa_elK8UBXt5kCwDg4-aDVVeBYGeiJvaFxPNa4vsQAxCcFBKzivTWxQAr8XQl00LiI9X2k3gHq647S2rNaFJWRx-IC4nPqtyqE8Pkgd2W2N9cXJz3Q3PXWb0Ax4bY32_4djkRd1MQyRREepVOf9LmWGYWO6MC_XPud8M1u9j1D5G51seG-LhzMSpb982E2jXUBj_4K91XeXXBllarYF37V2ZeSFy1qt4Fq8f-3EpwArPZEvLkxOnA6cD5oLN1MuKxnx85PTFOsSFulDW42GOoqOn_iKFSxTrg4fAN-TuptA?type=png)

- **Producers** write events to named topics.
- **Brokers** are the Kafka servers that store partitions on disk and replicate each partition across multiple brokers so a single broker failure does not lose committed data.
- **Topics & Partitions** organize and shard the stream for parallel throughput.
- **Consumers & Consumer Groups** pull events at their own speed and commit their offsets as they go.

## Kafka vs. traditional message queues

Engineers often compare Kafka with traditional message queues like RabbitMQ or Amazon SQS. Both decouple producers from consumers, but they follow different models:

| Dimension | Traditional Message Queue (e.g., RabbitMQ / SQS) | Apache Kafka (Event Streaming Log) |
|---|---|---|
| **Core model** | Queue: broker pushes or hands out tasks to workers | Append-only distributed log: consumers pull by offset |
| **After reading** | Message is deleted once acknowledged | Message stays for retention window (hours, days, or forever) |
| **Replayability** | Not in a classic queue: once acknowledged, it is gone (RabbitMQ Streams are a log-style exception) | Yes — reset a consumer group's offset to replay past events |
| **Multiple readers** | Needs separate queues or fan-out exchanges per service | Native — each consumer group reads the same topic independently |
| **Ordering** | Often lost when competing workers process in parallel | Strict ordering per partition (using event keys) |
| **Best fit** | Background job queues (send email, resize image, retry tasks) | High-volume event streams, analytics, audit logs, microservice fan-out |

If you want to hand out independent background jobs (like generating PDF invoices) and forget them once done, a traditional queue is simpler. If multiple downstream systems need the same stream of facts — or you ever want to replay yesterday's events into a brand-new analytics service — Kafka shines.

## Real-world applications and building systems with Kafka

Because Kafka decouples producers from consumers and retains history, it shows up across almost every large consumer platform:

- **Analytics systems:** streaming clicks, impressions, and orders into real-time dashboards and data warehouses.
- **Notification systems:** triggering email, SMS, and push alerts when order or account events fire, without slowing down checkout.
- **Payment processing:** recording immutable payment state transitions (`initiated` → `authorized` → `settled`) for reconciliation and fraud checks.
- **User activity tracking & recommendation engines:** feeding social-media likes, watch time, and search events continuously into ranking and feed models.
- **Microservices communication:** letting independent teams subscribe to business events (like `orders`) and ship new features without asking the checkout team for code changes.

Building with Kafka shifts how you design systems: instead of asking *"Which five APIs do I need to call right now?"*, you ask *"What business event happened, and what should react to it?"* That shift gives you **buffer absorption** during traffic spikes, **isolation** when one downstream service goes down, and **replayability** when a bug in a consumer requires reprocessing the last two hours of data.

The core takeaway: Kafka's speed and scale come from a deceptively clean design — **events** organized into **topics**, split across **partitions** for parallelism, and read by **consumer groups** that scale horizontally while letting multiple teams share the same durable stream.

One honest limitation: Kafka is not free to operate. Running a distributed cluster, designing partition keys carefully (a hot key can still overload one partition), and dealing with **eventual consistency** and **at-least-once delivery** by default (meaning consumers must handle occasional duplicate events idempotently) adds real complexity. If your app processes a few dozen background jobs a minute, a managed queue or your existing database is a better starting point.

If you were designing a food delivery app today, which events would you put in your first Kafka topic — and what key would you use to partition them?
