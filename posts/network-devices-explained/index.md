---
title: "From Modem to Load Balancer: The Devices Between You and a Server"
slug: network-devices-explained
subtitle: Modem, router, hub, switch, firewall and load balancer, one job each, and where they show up in a production web app
tags: networking, web-development, beginners, system-design, devops
cover: ./cover.png
seoTitle: "Network Devices Explained: Modem to Load Balancer"
seoDescription: "What a modem, router, switch, hub, firewall and load balancer each do, how they differ, and how they fit together in a real web app."
enableToc: true
---

The box on your shelf that you call "the router" is usually doing four or five different jobs. It translates the signal from your internet provider, hands out addresses, connects your devices to each other, runs the Wi-Fi, and blocks unwanted traffic. Each of those jobs used to be a separate device, and in a data centre they still are.

Pull the jobs apart and every network device makes sense. This post takes them one at a time, in the order your data passes through them, from the modem in your home to the load balancer in front of a website's servers. For each one: what it does, what it doesn't, and the device it gets confused with.

## How the internet reaches a home or office

Your internet provider runs a line to your building: a phone line, a TV cable, or fibre. That line carries a signal your laptop can't use directly. So the path looks like this:

![How the internet reaches a home or office: the ISP network connects to a modem that translates the signal, then a router that directs traffic, then a switch that connects local devices such as a laptop, phone and printer](https://mermaid.ink/img/pako:eNplkcFuwjAMhl8l8mmTCqMt0LSauIwL0pAmuK3hkCWGRmsT5LpjG-LdJzJtmrSj_X-fLctnMMEiVLBvw8k0mlg8bhQpL4QQq1rByjOSR75_obvFzWr7JDzyKdDrrYKdGI0WYl0rWAeLXUSYtO9bzdgLblD07uB1q2D3M3MdnU2tYBMGRoqSdYSGe8Gk93tn_uCbiG9rBduTY9NE3ATvI98Go1th8c0Z7P9Y22gt01rBoz5yOP7PslrBUxM8_o_ya0TueriCHSRwIGehYhowgQ6p09cSzldJATfYoYJKKCC0w_vIhDaQAuUvkMBR--cQuh-bwnBooNrrtscEhqPVjEunD6S73y6ht0gPYfAMlczjDKjO8A7VNJXjTJbzMp2kZZFP8gQ-oEqzbDzNZlkuZTGRRVkWlwQ-49bJOJuns7lMZ1LOp2UxSwCt40Dr76_H51--AKm8oAc?type=png)
*Translate, then direct, then connect. At home, those three are usually one box.*

At home, the modem, router and switch are usually one box. In an office, they're often three.

## Modem: the translator

A **modem** converts the signal on your provider's line into the standard network signal (Ethernet) that your other equipment understands, and back again. The name comes from what it does: **mo**dulate and **dem**odulate.

Which kind you have depends on the line: a DSL modem for phone lines, a cable modem for TV cable, and for fibre, a box usually called an ONT (optical network terminal) that does the same job.

That's all it does. A modem doesn't decide where anything goes, and it doesn't know about your devices. Think of it as an interpreter at a border: it translates, it doesn't route.

## Router: the post office

A **router** moves packets *between* networks: your home network on one side, the internet on the other. Every packet has a destination address, and the router decides where to send it next, like a post office reading the address on an envelope.

A home router does two more jobs that matter:

- **It hands out local addresses** (DHCP). When your phone joins the Wi-Fi, the router gives it an address, typically from the private ranges reserved by [RFC 1918](https://www.rfc-editor.org/rfc/rfc1918), such as `192.168.x.x` or `10.x.x.x`.
- **It shares one public address** (NAT). Your provider gives your home one public IP address. The router lets every device use it by rewriting addresses on the way out and remembering which reply belongs to which device on the way back.

### Modem vs router

- The **modem** connects your network *to* the internet. It translates.
- The **router** directs traffic *between* your network and the internet, and gives your devices addresses. It decides.

Plug a laptop straight into a modem and, with many providers, you can get online, but only that one device, and with nothing between it and the internet. Add a router and the whole house shares the connection.

## Hub vs switch: how a local network actually works

Inside your network, devices need to reach each other: laptop to printer, phone to TV. Two devices have done that job.

A **hub** is a repeater with many ports. Whatever arrives on one port, it copies out of *every* other port. Every device receives everything and ignores what isn't addressed to it. It's like a teacher reading every student's note aloud to the whole class.

A **switch** learns. Every network card has a hardware address, its MAC address. A switch watches which address appears on which port, builds a table, and from then on sends each frame only to the port it's meant for. It's like a mail sorter who knows which desk everyone sits at.

![Hub vs switch: when A sends to C through a hub, the hub copies the frame to B, C and D, and B and D ignore it; through a switch, the switch uses its MAC table and sends the frame only to C](https://mermaid.ink/img/pako:eNp9kk1r40AMhv-K0KkFJxs7Hx4PpZA4h1x6ykJhPT2MPaptsGeMPG6bDfnvS-KmLN1256SRHr3SCzpi4QyhxOfGvRaVZg8_N4qVBQDoh7xk3VWwG_JM4W7IJRSuq6kH74BeiA_QOfYKn64t57dbZwrX0JM1FzBV-ASTyT3sRpHP-FjbZAo3cFOX1jH1t19DaaYwhRumguqXb6ltpnD7pRRZ84-5_WvtiypTOAbyfXFnm8N1-79n7L9zt3_80LjL-cf9wzoFr_OGPgs8jvh_vJA1GGDJtUHpeaAAW-JWn794PCMKfUUtKZSgkMkMb5PCNY4VKnvCADttfznXXrvZDWWF8lk3PQU4dEZ72ta6ZN1-ZJmsIU7dYD1KEV80UB7xDeUiFNNIJKsknIVJPJ_NAzygDKNouoiW0VyIeCbiJIlPAf6-TJ1No1W4XIlwKcRqkcTLAMnU3vHDeGyXmzv9Ab7LvRM?type=png)
*A hub tells everyone; a switch tells only the device the frame is for.*

The difference matters. With a hub, every device shares the same capacity and sees everyone's traffic, which is slow and makes snooping trivial. A switch gives each connection its own path. That's why hubs have mostly disappeared; the "ports on the back of your router" are a small switch.

The confusing pair in the other direction: a **switch** connects devices *within* one network, using MAC addresses. A **router** connects *different* networks, using IP addresses.

## Firewall: the security gate

A **firewall** checks traffic against rules and blocks anything not allowed. Rules usually say things like "allow web traffic on port 443", "block everything arriving from outside unless it's a reply to something we sent", or "only this office's addresses may reach the database".

It sits at the edge, between a network you trust and one you don't, because that's the one place all traffic has to pass. Like a security gate at a building entrance, it doesn't need to check every room if it checks the door.

There's usually more than one. Your home router has a basic firewall built in. Your laptop has its own (Windows and macOS both include one). In a company or data centre, there's a dedicated firewall at the network edge, and often more between internal sections.

![Firewall placement: traffic from the untrusted internet passes through a firewall that allows or blocks it by rules; allowed traffic reaches the trusted internal network and blocked traffic is dropped](https://mermaid.ink/img/pako:eNpNkUFvgkAQhf_KZk5tAggosJDGS42JSdtDT01dDys7KnHZJeMStOp_b8BoPM7kfe87vDOUViEUsNG2K3eSHPv4FiQMY4wtlgIWxiEZdG9rGk1fWuOoPThUrwJWzPenbL4UMK8IO6n1kJFa246N2Frbcs_WJ0atxoOA1b113nOXIYbqwr4eEqmZQddZ2t9kT6onNvCnl6G7h3-WAmZkmwaVgBV4sKVKQeGoRQ9qpFr2J5x7WoDbYY0CCiaAULVHv7TakgBhruBBI82vtfWdJttud1BspD6gB22jpMNZJbck68eX0Cikd9saB0UeDR1QnOEIxSTiQczzNI_CKM_G4diDExRRHAeTOInHnGchz_I8u3rwN1jDIE6jJOVRwnk6ybPEA1SVs_R5G2jY6foP4m6Ilg?type=png)
*The firewall sits at the one point all traffic has to pass.*

## Load balancer: the toll booth with many lanes

Everything so far is about getting your traffic *out*. A **load balancer** sits on the other side, in front of a website's servers.

One server can only handle so many requests. Run several copies of your app, and something has to decide which copy handles each request. That's the load balancer. It's a toll plaza with many booths: cars arrive on one road and get spread across the open lanes, and a closed booth gets no cars.

It's simple enough to build a small one. This Node.js script (v24.22) starts three app servers and a load balancer on port 8080 that takes turns between them ("round-robin"), skipping any server that doesn't answer:

```js
// lb.js
const http = require("node:http");

// Three app servers, each saying who it is
const ports = [3001, 3002, 3003];
const servers = ports.map((port) =>
  http.createServer((req, res) => res.end(`hello from server ${port}\n`)).listen(port)
);

// The load balancer: round-robin, skipping servers that fail
let next = 0;
http.createServer((req, res) => {
  const tryServer = (attempt) => {
    const port = ports[next++ % ports.length];
    const fwd = http.get({ port, path: req.url }, (r) => r.pipe(res));
    fwd.on("error", () => {
      if (attempt < ports.length) tryServer(attempt + 1); // try the next one
      else { res.statusCode = 502; res.end("no healthy servers\n"); }
    });
  };
  tryServer(1);
}).listen(8080);
```

A small test script sent six requests to port 8080, stopped server 3002, then sent six more:

```text
hello from server 3001
hello from server 3002
hello from server 3003
hello from server 3001
hello from server 3002
hello from server 3003
--- stopping server 3002
hello from server 3001
hello from server 3003
hello from server 3001
hello from server 3003
hello from server 3001
hello from server 3003
```

Every request still got an answer. The user never saw server 3002 go down. That's the second job of a load balancer, and arguably the more important one: it hides failures. Real load balancers (NGINX, HAProxy, cloud ones) also check servers' health *before* sending traffic, rather than waiting for a request to fail.

You'll see them described by layer. A **layer 4** balancer spreads TCP connections without reading them. A **layer 7** balancer reads the HTTP request, so it can send `/api` to one group of servers and `/images` to another.

![Load balancer distributing traffic: users send requests to the load balancer, which forwards them to app servers 1 and 2 and skips app server 3 because it is down](https://mermaid.ink/img/pako:eNptkUFvgkAUhP_K5p2BsIvAsgcTbY_00sRLXQ9b9qmksEseUG3V_95IYxNNjzP5ZuYwJ6i8RVCwbfyh2hsaWPmqSTvGGFutNax6pF7DhoXhnJXLtYbSG8veTWNchaRhc6PL5cQs-FrDoutYj_SJxPg_iLhHxAMShfNz_1F3HVrFrD-4M1sk95FEwwYC2FFtQQ00YgAtUmuuEk7XKg3DHlvUoJgGQjsew8o3njRod4EAOuPevG9vafLjbg9qa5oeAxg7awZ8rs2OTPvnEjqL9ORHN4Aq0qkD1AmOoGZcRkIWWcFjXuRJnATwBYoLEc1EKhIp81jmRZFfAvieVuNIZDzNJE-lzGZFngaAth48vfz-Md1y-QG2JH10?type=png)
*Requests get spread across healthy servers. A server that's down gets none.*

## How they work together for a real web app

Put it all together and follow one request, from someone's phone to your app:

1. The phone's request goes through the home **switch** (or Wi-Fi), to the **router**, which rewrites it with the home's public address (NAT) and sends it out through the **modem**.
2. It crosses the internet, router to router, to your data centre or cloud.
3. A **firewall** checks it: is port 443 allowed? It is.
4. The **load balancer** picks a healthy app server.
5. The app server, on an internal network behind the firewall, talks to the **database**, which isn't reachable from the internet at all.

![End-to-end network architecture for a web application: a phone connects through a home router and modem to the internet, then a firewall, then a load balancer that sends requests to two app servers, which both use one database](https://mermaid.ink/img/pako:eNp10ttOwkAQBuBX2fxXGgvScughxgQEggkSgyYkdrxY6Agk7S4ZtoIS3t1YD-FCL3f-b2YvZg5Y2IyR4CW3u8VKi1PjKQkZpZS6Twn3K2uY8KxqtWs1mqaEkS1YiS0dy9VcLq8vVGEzLgjPP32jaaUng8eUcGsci2F3kk8GjxUYzlLCcC2803l-kg9nVTzupYSx1Zma61ybBcuJGfcq033wU0J3s1Fblte_RfCf6D74Fen30jNCXzs911smnJ-I4FvAw1LWGRInJXsoWAr9-cThUxLcigsmJIognJX72sLmVghkjvCw0ebJ2uKnW2y5XCF50fmWPZSbTDvur_VSdPFbFTYZy40tjUMSx9UMJAfskbT8qB5EcSf2G34cNhtND29I_CCot4J20IyisBGFcRwePbxXvzbqQcdvdyK_HUWdVhy2PXC2dlbuvpZf3cDxA9Xbm8E?type=png)
*One request, end to end: home network, internet, then firewall, load balancer, app server and database.*

## Where the simple model leaks

**In the cloud, most of these are software.** On AWS, Azure or Google Cloud you won't rack a firewall or a load balancer. You'll configure a security group (a firewall), a managed load balancer, and a virtual network whose switching and routing you never see. The jobs are exactly the ones above; the boxes are gone.

**Home routers blur every line.** One box is the modem, router, switch, Wi-Fi access point and firewall at once, which is exactly why the words get mixed up. When something breaks, it helps to ask which *job* failed, not which box.

**My load balancer is a teaching toy.** It retries on failure but has no health checks, no timeouts, and no limit on slow servers. Don't put it in front of anything real.

The takeaway: **each device does one job. The modem translates, the router directs, the switch connects, the firewall filters, and the load balancer spreads the work.** Most confusion comes from one box doing several. This post stayed at the "what and why" level; how packets actually move between these devices is in [why the TCP handshake takes three steps](https://jaydeepkanzariya.hashnode.dev/why-the-tcp-handshake-takes-three-steps-not-two), and how a name becomes the address they route to is in [tracing a DNS lookup](https://jaydeepkanzariya.hashnode.dev/how-dns-resolution-works).

Look at the box your internet comes through. How many of these jobs is it doing, and is there a second box you'd never noticed?
