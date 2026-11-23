---
title: "One Domain, Six Records: How DNS Record Types Work Together"
slug: dns-record-types-explained
subtitle: NS, A, AAAA, CNAME, MX and TXT explained one at a time, with real lookups, and how they combine for a single website
tags: dns, networking, web-development, beginners, devops
cover: ./cover.png
seoTitle: "DNS Record Types Explained: NS, A, AAAA, CNAME, MX, TXT"
seoDescription: "DNS record types explained simply: NS, A, AAAA, CNAME, MX and TXT, what problem each solves, A vs CNAME, NS vs MX, and how they work together."
enableToc: true
---

How does a browser know where a website lives? You type `example.com`, but computers don't connect to names. They connect to numbers. Somewhere between your keyboard and the page, the name has to turn into an address. Here's that step on its own, run from my laptop on 23 November 2026:

```powershell
Resolve-DnsName example.com -Type A -Server 1.1.1.1
```

```text
Name        Type TTL IPAddress
----        ---- --- ---------
example.com    A 191 104.20.23.154
example.com    A 191 172.66.147.243
```

That lookup is **DNS**, and the line it returned is one **DNS record**. A domain usually has several kinds of record, each answering a different question. This post goes through the six you'll meet first, one at a time, and then puts them together for one small website. Every lookup below is real and ran on the same day. (`Resolve-DnsName` is built into Windows PowerShell; on macOS or Linux, `dig example.com A` gives the same answers.)

## DNS is the internet's phonebook

Your phone's contacts list lets you tap "Mum" instead of remembering a ten-digit number. DNS (Domain Name System) does the same for the internet: you use the name, and DNS looks up the number.

Why not type the numbers? Because they're hard to remember, and they change. A site can move to a new server with a new address, and as long as DNS is updated, everyone typing the name ends up in the right place. The name stays put; the number behind it can move.

![High-level DNS flow: the browser asks DNS where example.com is, DNS answers 104.20.23.154, and the browser connects to the web server at that address](https://mermaid.ink/img/pako:eNpVkU1PwkAURf_Ky1uXsTP9mk4MJNilupCFiQyL0j5ok7ZDplNBKf_dUEXj8ibnnru4ZyxMSahw15hjUeXWweOLtroDAFiuNS6tOfZk77f2bk6nvD00xArTLjRuYDabj5zBsSJLUPdQu8UI2Vpj9rzSuLlpsgkUDLgfMuEzETAehSMsf3cmIGBQmK6jwo2wWmt8pS30ZN9_xv-VNW7Qw72tS1TODuRhS7bNrxHPV6lGV1FLGhVotFQOp1lhGmM16u6CHh7y7s2Y9ta2ZthXqHZ505OHw6HMHWV1vrf5H0JdSfbBDJ1DlU4GVGc8oQq5ZEKmccp9niaBH3j4gYoLwUIRiUDKxJdJmiYXDz-nTZ-JmEex5JGUcZgmkYdU1s7Yp-8vpksuX34oepw?type=png)
*Name in, address out. Then the browser connects to the address.*

## Why one domain needs several records

A phonebook entry for a business might list a street address, a phone number and a postal address. They're all about the same business, but they answer different questions.

DNS records work the same way. Each record has a **type**, and the type says which question it answers:

| Question | Record type |
|---|---|
| Who's in charge of this domain's records? | NS |
| What's the website's IPv4 address? | A |
| What's its IPv6 address? | AAAA |
| Is this name really another name? | CNAME |
| Where should email for this domain go? | MX |
| Any extra notes, or proof of ownership? | TXT |

Let's take them in that order.

## NS: who is responsible for this domain

Before anyone can look up a domain's address, they need to know who holds its records. That's the **NS (name server)** record. Think of it as the post office that keeps the address book for one neighbourhood.

```text
Name        Type   TTL NameHost
----        ----   --- --------
example.com   NS 70818 hera.ns.cloudflare.com
example.com   NS 70818 elliott.ns.cloudflare.com
```

So `example.com`'s records live on two Cloudflare name servers. Two, so one can be down without the domain disappearing.

How does anyone find *those*? DNS is a hierarchy. The root servers know who runs `.com`. The `.com` servers know who runs `example.com`: that's the NS record. And `example.com`'s name servers know everything else about it.

![Simple DNS hierarchy: root servers know who runs .com, the .com servers hold the NS records pointing to hera and elliott.ns.cloudflare.com, and those name servers hold example.com's A, AAAA, MX and TXT records](https://mermaid.ink/img/pako:eNp9kTtPw0AQhP_KahuayxE7Dz-EkExoSQEpEDmKw7eJI87eaH0mgZD_jmKIoKIcaeabkeaAJTvCHFeed2VlJcDixohpAADulwbvmQO0JG8k7dWLXF6_NryDXcUgXdOCLrk2-AyDwTXMlgZP-h877W299fSTOvfMTvHP-QMIlSyu_YT50mBFYuESyPsNh6CbVpeeO7fyVnpAj6_Yu7_Ui_YM-cOf9_OKpcFCQVEUhYK7RwWLxwVorQ0-o8K1bBzmQTpSWJPU9iTxcAIYDBXVZDAHg0Ku2w9K9iwGTXNEhVvbPDHX57Rwt64wX1nfksJu62yg241di_21UONIZtw1AfNo3CMwP-Ae83GU6jjNplk0jLJkNBwpfMc8imM9jifxKE2TYZpkWXJU-NGXDnU8jSbTNJqk6XScJROF5DaB5e772P7f4xdzc5mF?type=png)
*Each level only knows who to ask next. The NS records are the hand-off to the domain's own name servers.*

## A: the domain's IPv4 address

The **A (address)** record is the one from the top of the post: the house address. It maps a name to an IPv4 address, the familiar four numbers separated by dots.

`example.com` has two A records, `104.20.23.154` and `172.66.147.243`. More than one is normal: it gives clients a second address to use.

## AAAA: the same, for IPv6

IPv4 has about 4.3 billion addresses, and the internet ran short of them. IPv6 is the newer, much larger address system, and the **AAAA** record (four As, because an IPv6 address is four times as long) maps a name to one:

```text
Name        Type TTL IPAddress
----        ---- --- ---------
example.com AAAA   6 2606:4700:9ad5:72db:f2ca:0:ef6b:ff98
```

A domain usually has both. Your device uses whichever its network supports. You don't choose; it happens automatically.

## CNAME: one name pointing to another name

Sometimes you don't want to give an address at all. You want to say "this name is really that other name". That's a **CNAME (canonical name)**. Think of a receptionist who says "for sales, ask for Priya" instead of giving a room number. If Priya changes rooms, the instruction is still right.

```text
Name            Type  TTL NameHost   IPAddress
----            ----  --- --------   ---------
www.github.com CNAME 3295 github.com
github.com         A   17            4.186.157.192
```

Asking for `www.github.com` returned a CNAME to `github.com`, and the resolver followed it to `github.com`'s A record. GitHub only has to keep one A record up to date.

CNAMEs are also how you connect a name to a hosting service: point `blog.yoursite.com` at the host's name, and when the host changes its servers, your record stays correct.

![CNAME chain: www.github.com is a CNAME pointing to github.com, which has an A record pointing to 4.186.157.192](https://mermaid.ink/img/pako:eNpVkF1LwzAUhv9KeK-z0GT9SHIhjClDcCLeCC67iG3WFtZmxJROt_13WWWCl-c973MOPCeUvnLQ2O39WDY2RPL0aoLpCSHkbWMwjiOr29gMH6z0ncGWzGZ35-XzYv1wJquNwb_ljVxNrcWZPL5sDFLGZc54VjCuhMEWFHVoK-gYBkfRudDZ64jTlTaIjeucgSYGwVXDcVb6vQ8Gpr-A4mD7d--7Gx38UDfQO7v_dBTDobLR3be2Drb7S4PrKxeWfugjNJfTDegTjtApl0xIlSuecFXMkznFFzQXgqUiE3Mpi0QWShUXiu_pa8JEzrNc8kzKPFVFRuGqNvqw_hU5-bz8ABlRZ80?type=png)
*A CNAME points to a name. The A record at the end of the chain holds the address.*

## A vs CNAME, cleared up

This is the mix-up nearly everyone hits, so slowly:

- An **A record** points a name to an **address**. It's the end of the line.
- A **CNAME** points a name to **another name**. DNS then has to look that name up too.

The rule that catches people: a name with a CNAME can't have any other records. That comes from the original DNS spec, [RFC 1034, section 3.6.2](https://www.rfc-editor.org/rfc/rfc1034#section-3.6.2). Your root domain (`yoursite.com` itself) always has NS records, so it can't be a CNAME. Use a CNAME for `www` or `blog`, and an A record for the root. Some DNS providers offer workarounds with names like "ALIAS" or "CNAME flattening", but those are provider features, not standard record types.

## MX: where email for this domain goes

When someone emails `you@gmail.com`, their mail server needs to know where Gmail accepts mail. That's the **MX (mail exchange)** record. It's the post office for letters, not for visitors.

```text
Name      Type  TTL Preference NameExchange
----      ----  --- ---------- ------------
gmail.com   MX 1623          5 gmail-smtp-in.l.google.com
gmail.com   MX 1623         10 alt1.gmail-smtp-in.l.google.com
gmail.com   MX 1623         20 alt2.gmail-smtp-in.l.google.com
gmail.com   MX 1623         30 alt3.gmail-smtp-in.l.google.com
gmail.com   MX 1623         40 alt4.gmail-smtp-in.l.google.com
```

(Sorted by preference; the lookup returned them in a different order.) The **preference** number sets the order: the lowest is tried first, and the others are backups. Notice that MX records point to names, not addresses; each of those names has its own A record.

And `example.com`? Its MX record is a single dot, `0 .`. That's a "null MX" ([RFC 7505](https://www.rfc-editor.org/rfc/rfc7505)): the domain's way of saying it accepts no email at all.

![Email routing with MX records: the sender's mail server looks up gmail.com's MX records in DNS, gets gmail-smtp-in.l.google.com at preference 5 first with alt1 to alt4 as backups, and delivers the message to the preference 5 server](https://mermaid.ink/img/pako:eNpNkU9vozAQxb_KaC69gIudEMBaRSttjk0PzWXVuAcXJgTVYDSY_tmQ717Bblc9vpl5vyfNu2DpK0KNJ-ffyrPlAHcPhk0HAHA4GjxQVxHfDNDaxsFA_Er845lvt8Fr-PDjz3peiNK3Bp8gjrfT_jc471_GfoLd0eDu_mDw6Qu5W056phMxdSVBCqeGhzDBXh4NLrB4aEMfN51wova-dvSP_o0h4u30bMuXsdcgkwhUAkKICfbqaNC6IGcJ1oX1N99hya7INa_EcyBGWHNToQ48UoQtcWtniZfZYDCcqSWDGgwyVeN7XHrn2aDprhhhb7tH79svN_uxPqM-WTdQhGNf2UC7xtZs2_9TXp75y49dQK3UwkB9wXfUa5kLlRebQiayyFbJKsIP1FIpsVapWuV5luRZUWTXCP8sqYlQG5lucpnm-WZdZGmEVDXB8_5voUuv10_kfZRU?type=png)
*The lowest preference number is tried first; the rest are backups.*

## NS vs MX, cleared up

Both point to servers, and both sound like "the domain's server", which is why they get mixed up.

- **NS** answers "who holds this domain's DNS records?" It's about the address book itself.
- **MX** answers "where should email for this domain be delivered?" It's one entry *in* that address book.

Changing your NS records moves your whole DNS to a different provider. Changing your MX records only moves your email.

## TXT: notes and proof of ownership

A **TXT** record holds plain text. DNS doesn't interpret it; other services read it. The two common uses are proving you own a domain (a service gives you a code, you add it as a TXT record, the service checks) and email rules.

```text
Name        Type TTL Strings
----        ---- --- -------
example.com  TXT 300 {v=spf1 -all}
example.com  TXT 300 {_k2n1y4vw3qtb4skdx9e7dxt97qrmmq9}
```

The first is an **SPF** rule: `-all` means no server is allowed to send email as `example.com`. That fits its null MX: it neither receives nor sends mail. The second looks like a verification code of the kind services ask you to add, though the record itself doesn't say which service it's for.

## One small website, all records together

Here's a constructed example: a made-up shop at `myshop.example`, with its site on one host and its email with a mail provider. (`.example` is reserved for examples, and the IP addresses below are from the ranges set aside for documentation.)

```text
myshop.example.        NS     ns1.dns-host.example.
myshop.example.        NS     ns2.dns-host.example.
myshop.example.        A      203.0.113.10
myshop.example.        AAAA   2001:db8::10
www.myshop.example.    CNAME  myshop.example.
myshop.example.        MX     10 mail.mailhost.example.
myshop.example.        TXT    "v=spf1 include:mailhost.example -all"
```

Read it as answers: the DNS host runs the address book (NS). The site lives at these addresses (A, AAAA). `www` is the same site (CNAME). Email goes to the mail provider (MX). And only that provider may send mail as the shop (TXT).

![Complete DNS setup for the example site myshop.example: NS records point to ns1 and ns2 at dns-host.example, A and AAAA records point to the web server at 203.0.113.10 and 2001:db8::10, www.myshop.example is a CNAME to myshop.example, the MX record points to mail.mailhost.example, and a TXT SPF record says only mailhost may send](https://mermaid.ink/img/pako:eNp9kkFr4zAQhf_KMGdHkeTElkUJuM3uLWEhgZa1clAiNQ7YUpDtTbJx_vsSl5YulF4GZpj3zRt4V9x5Y1Hia-VPu1KHFtaPKigHADAvFNaXpvRHYs-6PlZW4QZGo1m_XPWwLBS6hsEYXMOJcc2o9E37afMDM0hyGEOe53kPq0Lhs91CY8MfGx62YTzjNCaUMBYTRmEMnFImzVZIyegn0HOh8HQ6ka89PS3zxY8e5v-fXbz0sLj_oQ8VuZdvTa5f1j2sC4WrXz8leFdd4F0z-Kz1BRrrjMINRrgPB4OyDZ2NsLah1vcWr3egwra0tVUoQWGwpjuPdr7yQaFyN4zwqN1v7-t3dfDdvkT5qqvGRtgdjW7t_KD3Qdcf02CdseHJd65FyZOBgfKKZ5QTJggXWZIxyrI0pnGEF5SMczLhUx4LkVKRZll6i_DvcJUSnrBpIthUiGSSpdMIrTm0Pize0jCE4vYPPUWmAA?type=png)
*Every record answers a different question about the same domain.*

## Where the simple model leaks

**Answers are cached.** That `TTL` column is "time to live", in seconds: how long a resolver may reuse an answer before asking again. I asked for `gmail.com`'s MX twice, five seconds apart, and the TTL went from 3335 to 3330. It's counting down in the resolver's cache. This is why a DNS change "takes time to spread": old answers stay in caches until their TTL runs out.

**Your browser doesn't walk the hierarchy itself.** It asks a **resolver** (your ISP's, your company's, or a public one like the `1.1.1.1` I used), and the resolver does the root → `.com` → name server walk, then caches the result. Most lookups never reach the root at all.

The one-line version: **every DNS record answers one question about a domain, and a working site is just those answers agreeing with each other.** This post stayed with the six common types; SOA, SRV and CAA exist too, and follow the same pattern. DNS queries mostly travel over UDP, which I covered in [TCP vs UDP and where HTTP fits](https://jaydeepkanzariya.hashnode.dev/tcp-vs-udp-and-http).

Try `Resolve-DnsName yourdomain.com -Type MX` (or `dig yourdomain.com MX`) on a domain you use. Where does its email actually go?
