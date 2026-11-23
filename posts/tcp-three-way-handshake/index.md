---
title: "Why the TCP Handshake Takes Three Steps, Not Two"
slug: tcp-three-way-handshake
subtitle: SYN, SYN-ACK and ACK explained slowly, plus how sequence numbers, acknowledgements and retransmission make TCP reliable
tags: networking, tcp, web-development, beginners, computer-science
cover: ./cover.png
seoTitle: "TCP 3-Way Handshake and Reliable Communication"
seoDescription: "How TCP works: the 3-way handshake step by step, sequence numbers and ACKs, retransmission after packet loss, and how FIN closes a connection."
enableToc: true
---

Before your browser receives a single byte of a web page, it has already spent time setting up a connection. Here's `curl` timing a request to example.com from my laptop (curl 8.22, Windows 11):

```bash
curl -s -o /dev/null -w "dns=%{time_namelookup}s connect=%{time_connect}s tls=%{time_appconnect}s first_byte=%{time_starttransfer}s total=%{time_total}s\n" https://example.com
```

```text
dns=0.033602s connect=0.046649s tls=0.087388s first_byte=0.106738s total=0.106844s
```

These timings are cumulative. The address was known after 33.6 ms; the TCP connection was ready at 46.6 ms. So about 13 ms went to nothing but **connecting**: three short messages called the **3-way handshake**. (Across three runs it was between 13 and 22 ms.) Why three, and not one "hello"? The answer explains almost everything else TCP does, so this post builds up to it slowly.

## What happens if data is sent without rules

The internet moves data in **packets**, and makes no promises about them. A packet can get lost. Two packets can take different routes and arrive in the wrong order. A packet can arrive twice. Bits can get damaged on the way.

Picture sending a three-part message, "Meet / at 5 / at the gate", as three packets. Without rules, the other side might receive "at the gate", then "Meet", and never get "at 5". It has no way to know a part is missing, or which order was intended. And you have no way to know it didn't all arrive.

## The problems TCP is designed to solve

TCP (Transmission Control Protocol) is a set of rules both computers follow so that, on top of that unreliable network, a program can send a stream of bytes and have it arrive:

- **complete**: lost pieces get sent again;
- **in order**: pieces are put back in sequence;
- **intact**: damaged pieces are detected;
- **at a sensible pace**: the sender slows down if the receiver or the network can't keep up.

To do any of that, both sides first need to agree they're talking, and agree on how to number what they send. That's the handshake.

## The 3-way handshake as a conversation

Think of a phone call on a bad line:

> **You:** Can you hear me?
> **Friend:** Yes, I can hear you. Can you hear me?
> **You:** Yes.

After three lines, both of you know two things: *my* voice reaches *you*, and *your* voice reaches *me*. Two lines wouldn't be enough. After "Yes, I can hear you. Can you hear me?", your friend still doesn't know if you heard *them*.

TCP's handshake is that conversation, plus one extra detail that makes it essential.

## SYN, SYN-ACK, ACK, one step at a time

TCP numbers every byte it sends, so the receiver can spot gaps and fix the order. Each side picks its own **starting number**, and the spec ([RFC 9293](https://www.rfc-editor.org/rfc/rfc9293)) says it should be hard to guess rather than starting at 0. The handshake is how each side learns the other's starting number, and confirms it was received.

The numbers below are made up to keep them readable; real ones are large and random.

**Step 1: SYN (client → server).** "I'd like to connect. My numbering starts at 1000." SYN is short for *synchronise*.

**Step 2: SYN-ACK (server → client).** Two things in one message. *ACK*: "I got your 1000; next I expect 1001." *SYN*: "My numbering starts at 5000."

**Step 3: ACK (client → server).** "I got your 5000; next I expect 5001."

Now each side's starting number has been sent **and confirmed**. That's why it takes three steps. With only two, the server would announce 5000 but never learn whether the client received it. The second step does double duty, which is why it isn't four.

![TCP 3-way handshake: the client sends SYN with seq 1000, the server replies SYN-ACK with seq 5000 and ack 1001, and the client sends ACK with ack 5001, after which the connection is established](https://mermaid.ink/img/pako:eNpt0lFPgzAQB_CvcrnnbilsQGniEoNvxr3wpOGlwg0aod3aYqbLvruBOTONj-2_9-sldyesbUMo0dNhJFPTg1atU0PlKgMAsFcu6FrvlQlQgPJQ9JpM-C8up7gk907uGheLzaaUUD5vGXg63EWc82u2tYHA6bYLYHdQSqhnGXxQLnhQAW5fl4vNppilxX3xeNESzjkDVb9NbvTL7Wk3s4UEP3d0wyY37HeDMzlByV_ITrUFm9qzxlAdtDVAPqjXXvuOGmTYOt2gDG4khgO5QU1HPE1IhaGjgSqUUKGjZjwuattbV2Flzshwr8yLtcO12tmx7VDuVO-J4bhvVLjO4-fWkWnIFXY0AeU6nQ2UJzyiXEdiGYs8zSMe5dmKrxh-oIzieLmOk3glRMZFlufZmeHn_CtfxmmUpCJKhEjXeZYwpEYH654uOzGvxvkLH42oMQ?type=png)
*Each starting number is sent once and confirmed once. The middle step does both jobs.*

You can watch the result. I ran a small Node.js script that starts a server on port 5050 and connects to it, then printed `netstat` after the handshake:

```text
TCP  127.0.0.1:5050   0.0.0.0:0         LISTENING
TCP  127.0.0.1:5050   127.0.0.1:59741   ESTABLISHED
TCP  127.0.0.1:59741  127.0.0.1:5050    ESTABLISHED
```

One line for the server still listening for new connections, and one `ESTABLISHED` line for each end of the new connection.

## How data moves: sequence numbers and ACKs

Once connected, every piece of data carries a **sequence number**: the number of its first byte. The receiver replies with an **ACK number**: the next byte it expects. That one rule does a lot of work.

Say the client sends 300 bytes in three pieces, starting from 1001:

| Client sends | Bytes | Server replies |
|---|---|---|
| seq=1001, 100 bytes | 1001–1100 | ack=1101 |
| seq=1101, 100 bytes | 1101–1200 | ack=1201 |
| seq=1201, 100 bytes | 1201–1300 | ack=1301 |

`ack=1301` means "I have everything up to 1300. Send 1301 next." It confirms all the earlier bytes at once, so not every piece needs its own reply.

![TCP data transfer with sequence and ACK numbers: the client sends 100 bytes at seq 1001 and the server acks 1101, then 100 bytes at seq 1101 acked with 1201, then 100 bytes at seq 1201 acked with 1301](https://mermaid.ink/img/pako:eNqFkTFvgzAQhf-KdVMrOZHPBDCWwkLXTmwViwvXBDXY5DBV0ij_vUoqOkXqePfedye9d4E2dAQWJjrO5Ft66d2O3dBw44UQYnQc-7YfnY-iEm4S1aEnHx_J9U2uib-IF7lalWVtxUTHLSqF4gmVEu_nSNPzYqlXZVlZ4drPLaLCRyT-T-rHpP6fTBSChB33HdjIM0kYiAd3G-FyszcQ9zRQA1Y0wNTNp1UbDoEbaPwVJIzOv4UwLDSHebcH--EOE0mYx87FJdO_LZPviKsw-wg2VfcbYC9wArtBs9amyApUWOSJSiScwaLW641OdWJMrkxeFPlVwvf9q1rrDNPMYGpMtinyVAJ1fQz8-tvrvd7rDxGjj-U?type=png)
*Each ACK names the next byte expected, which confirms everything before it.*

## When a packet gets lost

Now drop the middle piece. The server receives bytes 1001–1100, then 1201–1300, but not 1101–1200.

- The server can't hand bytes 1201–1300 to the program yet; that would put them out of order. It **holds them** and keeps replying `ack=1101`: "I'm still waiting for 1101."
- The client notices one of two ways. Either a **timer** for that piece runs out with no ACK, or it sees the **same ACK repeated** several times, which strongly suggests a gap. ([RFC 6298](https://www.rfc-editor.org/rfc/rfc6298) covers the timer; [RFC 5681](https://www.rfc-editor.org/rfc/rfc5681) the repeated-ACK signal.)
- The client **resends** 1101–1200. The gap fills, the server passes all 300 bytes to the program in order, and replies `ack=1301`.

The program never knew a packet was lost. It only saw the bytes arrive a little later.

For damaged data, every TCP segment carries a **checksum**. If the bytes don't match it, the receiver discards the segment, which turns "damaged" into "lost", and the resend handles it.

![Packet loss and retransmission: the client sends seq 1001 and gets ack 1101; the segment at seq 1101 is lost; the client sends seq 1201 but the server still replies ack 1101; after a timeout or repeated ACK the client resends seq 1101 and the server replies ack 1301, all received](https://mermaid.ink/img/pako:eNqNkjFv20AMhf8KwSkGZONOtizpgBgo1K1oF2-BlqtE24ec7hSKSp0Y_u-BHChdPGQk3_veG8gLNrElNDjQy0ihoZ_OHtl2NdcBAKC3LK5xvQ0CFdgBKu8oyD15P8l74lfiWa6Wu93ewEAvj1opDQ9aKfj7JjQsZst-udtVBmzz_Ki10v_J5Xkm9UT6OMjiXm76rVx4GMR5D_-sExeOX7Y_UQg8HQTiASoD4jqKo0BkYOrJCrXwo_p1r_iWyjRQkLut60m33gNTQ-6V2gUmeGTXohEeKcGOuLPTiJeJrlFO1FGNBmpkasfzsok-co11uGKCvQ1PMXYzzXE8ntAcrB8owbFvrczH-9oyhZa4imMQNNnmloHmgmc0G12s0qLcllrpMl-rdYJvaHSarjZplq6LIldFXpb5NcH3W6tapVudbQudFcV2U-ZZgtQ6ifz784Fuf3T9AJL9skA?type=png)
*The repeated `ack=1101` is the server pointing at the gap. One resend fills it.*

## Closing the connection: FIN and ACK

A TCP connection carries data in **both directions**, and each direction is closed separately. So closing usually takes four messages:

1. One side sends **FIN** (*finish*): "I have nothing more to send."
2. The other side **ACKs** it. It can still send its own remaining data.
3. When it's done too, it sends its own **FIN**.
4. The first side **ACKs** that.

Then the side that closed first waits a while in a state called `TIME_WAIT`. That's so a late, delayed packet from this connection can't be mistaken for part of a new one, and so the last ACK can be resent if it was lost. In my script the server closed first, and this is what `netstat` showed straight afterwards:

```text
TCP  127.0.0.1:5050   0.0.0.0:0         LISTENING
TCP  127.0.0.1:5050   127.0.0.1:59741   TIME_WAIT
```

The client's line is gone. The server's end lingers in `TIME_WAIT`, exactly because it sent the first FIN.

![TCP connection lifecycle: from Closed, SYN, SYN-ACK and ACK lead to ESTABLISHED; data and ACKs flow with resends if lost; FIN, ACK, FIN, ACK lead to TIME_WAIT on the side that closed first; after a short wait the connection is Closed](https://mermaid.ink/img/pako:eNpVkdFqwkAQRX9lmNeu1kRjNqEIMVoqrT5UoVhXytbdmECSLZMNtTX-ezHFYt9mhnvPzHCPuDNKY4hJbj53qSQLT8-CRAkAEG0ExrmptBK4hU5n1CzXCwbL9aITxY8MovixgfFG4HS5isZPs-XDdCJwe7GPW4uSVsLNWVvdvdPtiHSlSwVZArmpbAPj__L72aIFM7hUDcQbgavZfPr2Es1WLaTKlAabSgu79j5IMqrs1e64hcnEagIJVWrIwqfMbAOT66eQ4Z4yhaGlWjMsNBXy3OLxjBFoU11ogSEIJK3qQ2dnckMCRXlChh-yfDWmuLjJ1PsUw0TmlWZYfyhp9SSTe5LF35R0qTTFpi4thh5vGRge8YDhwOFdlwfDwOk5gd_v9Rl-Yei4bnfgem6fc7_H_SDwTwy_2629rjt0vCF3PM6Hg8D3GGqVWUPz30jbZE8_8K-SEQ?type=png)
*Connect, transfer, close. Only the side that closed first waits in `TIME_WAIT`.*

## Where the simple model leaks

**The handshake costs a round trip, every time.** Those 13–22 ms happen before any data moves, on every new connection. That's why HTTP keeps connections open and reuses them. When I asked curl for example.com twice in one command, the first request reported `num_connects=1` and the second `num_connects=0`: it reused the connection and skipped the handshake entirely. It's also part of why HTTP/3 uses QUIC, which sets up the connection and encryption together.

**Reliable means delivered, not handled.** TCP guarantees the bytes reached the other computer's TCP, in order. It doesn't guarantee the program there read them, saved them, or didn't crash a moment later. That's why APIs still send their own responses, like `200 OK`, on top.

**My numbers are illustrations.** Real sequence numbers are random 32-bit values, and real segments are usually much larger than 100 bytes. The rules are exactly as described; the sizes are not.

The takeaway: **TCP numbers every byte, and the 3-way handshake exists so both sides agree on those numbers before anything else happens.** Ordering, acknowledgements and retransmission are all that numbering put to work. This post skipped flow control and congestion control, which decide how *fast* to send. If you want to see where TCP sits next to UDP and HTTP, I covered it in [TCP vs UDP and where HTTP fits](https://jaydeepkanzariya.hashnode.dev/tcp-vs-udp-and-http), and if curl is new to you, start with [getting started with curl](https://jaydeepkanzariya.hashnode.dev/a-browser-without-the-browser-getting-started-with-curl) before trying the `-w` timing command above.

Run that `curl -w` command against a site far from you, then one close by. How much does the `connect` time change, and why?
