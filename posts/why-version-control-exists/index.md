---
title: "final_v2_latest_FINAL.zip: Why Version Control Exists"
slug: why-version-control-exists
subtitle: The pendrive problem, the folders named final_v2, and what version control records that a copied file never can
tags: git, version-control, beginners, web-development, programming
cover: ./cover.png
seoTitle: "Why Version Control Exists: The Pendrive Problem"
seoDescription: "Pendrives, email attachments and final_v2 folders lost code by design. See why version control exists, with a real Git demo of the overwrite problem."
enableToc: true
---

Here's a folder listing most developers have seen some version of:

```text
project/
project_final/
project_final_v2/
project_latest_final/
project_final_USE_THIS/
project_final_USE_THIS (1).zip
```

Which one is current? Which one has the bug fix from last week? Nothing inside these folders can tell you. Only the person who made them can, and only if they remember.

The usual reading is that someone was careless. Better naming, a stricter rule about who copies what, and it would be fine. It wouldn't. A copied file doesn't carry any record of **what changed, who changed it, or which version it started from**. That missing record is the pendrive problem, and it's why version control exists.

## How code moved before version control

Before version control was standard, code moved between people the way any other file did:

- **Pendrives**: copy the project on, carry it to the next machine, copy it off.
- **Email attachments**: zip the folder, send it, reply with a newer zip.
- **Shared folders**: one copy on a network drive that everyone opens and saves.
- **Dated folders**: `project_2024-03-12`, kept "just in case".

Each one is reasonable on its own. The pendrive is fast. Email is already there. A dated folder is a crude backup. The trouble starts when two people work on the same files at the same time, which is the normal state of any team.

## The pendrive problem, step by step

Here's a constructed example, small enough to follow line by line. Two developers, Asha and Ravi, share a project through a pendrive. It has one file:

```js
// app.js
const title = "Shop";
const currency = "INR";
const price = 100;
```

1. Both copy the project from the pendrive to their own laptops.
2. Asha renames the shop: `"Shop"` becomes `"Corner Shop"`.
3. Ravi raises the price: `100` becomes `120`.
4. Asha copies her `app.js` back to the pendrive.
5. Later, Ravi copies his `app.js` back. The computer asks "Replace the file?", and he says yes, because his copy is newer.

The pendrive now holds Ravi's version, which still says `"Shop"`. Asha's change is gone. Nobody deleted it on purpose, and nothing warned anyone. Ravi's copy was "newer", but it was newer than the *original*, not newer than Asha's.

![Sequence of the pendrive overwrite: Asha and Ravi each copy app.js from the pendrive, Asha changes the title and Ravi changes the price, Asha copies hers back, then Ravi copies his back over it, leaving the title as Shop and Asha's change lost](https://mermaid.ink/img/pako:eNptks1u2zAQhF9lsZekgOJIsq0fIjVgpNcWgnMreGGojcVEItkVZSQx_O6B7KjQwUfufDODBfeI2tWEAnv6N5DV9MuoPatOsrQAAF5xMNp4ZQNUoHqoyNZsDnQN2I7Atm_UNXE3ijt1MJNY3W02WwHa-Q9Q3i9e-7myu6psL55gQkvwEyQ-OrbE8NQ4L3Gidhe_Z6NHKknjub_6Tn5W-m3umM_hlsm3StOPifjjAoE7EEM1778UPzzz_WZc_KYH3Si7J2hdHzDCPZsaReCBIuyIOzU-8ThmSgwNdSRRgESmeni_0651LFHaE0bolf3rXDe52Q37BsWLanuKcPC1CtNn_Z8y2Zr40Q02oMiycwaKI76jWCXFIi3KrEzipMyX8TLCDxRJmi5W6TpdFkUeF3lZ5qcIP8-t8SLNknVWJOuiyFZlvo6QahMc_74czPluTl95frM1?type=png)
*Ravi's copy is newer than the original, not newer than Asha's. The pendrive can't tell the difference.*

## What actually goes wrong

That one scenario contains every problem the pendrive workflow has.

**Overwritten code.** The last copy wins. At most, the "Replace the file?" dialog shows you dates. It never compares contents, so "newer" and "complete" get confused.

**Lost changes with no way back.** If the code worked on Tuesday and is broken on Friday, you can only go back if someone happened to save Tuesday's copy. Usually that's the folder called `project_final_v2`, and usually nobody's sure what's in it.

**No history.** Even when nothing is lost, you can't answer basic questions. Who changed this line? When? Why? A file has a "last modified" date and nothing else.

**Names that lie.** `final` is only final until someone edits it. Then you get `final_v2`, then `latest_final`. Each name records someone's hope at one moment, not a fact about the code.

**No collaboration, only taking turns.** The only safe pendrive rule is "one person edits at a time". That turns a team into a queue.

![Timeline of file versions: Monday's project_final becomes Tuesday's project_final_v2 with a bug fix; on Wednesday Asha and Ravi edit separate copies; Thursday's latest_final holds Asha's copy, and on Friday Ravi copies over it and the title change is lost](https://mermaid.ink/img/pako:eNptkk1r20AQhv_KMJdeJFdafS_FUBJyai6huFBvCBtpLG2QdsVqZTt1_N-LpNS4JMd5ed6Pw5ywNBUhx11rDmUjrYMfD8IKDQCwCbcC743-9my_rntrXqh0TzulZSvwEXx_DRu2FfhzpI_E057N4vNYw04dqRL4eMlliznaCvxF1cx9HxrJQdMBnHItfULHV_SD3KuF7q0q_6OjhU6mYc040610NLzvupR9GaA0_eu1NV6s6VbgnVWXoolTNIDZkwXlZn0eCWUjdU3QmsFd5yTgr_z128QfrHKO9BtsUvSwtqpC7uxIHnZkOzmdeJpsAl1DHQnkINBSNR790rTGChT6jB72Uv82pvvntmasG-Q72Q7k4dhX0tGtkrWV3UW1pCuyN2bUDnkWzBnIT3hEHof5iuVFWoRBWGRREHn4ijxkbBWzhEV5ngV5VhTZ2cM_c2uwYmmYpHmY5HkaF1niIVXKGXu_vM_8Ree_q-a4vQ?type=png)
*Each folder name records someone's hope at the time. Friday's copy silently drops Thursday's work.*

## The same edits, this time with Git

I ran the same two edits through Git 2.56: a shared repository, and Asha and Ravi each with their own clone. Asha pushes her change first. Then Ravi tries to push his:

```bash
git push origin main
```

```text
 ! [rejected]        main -> main (fetch first)
hint: Updates were rejected because the remote contains work that you do not
hint: have locally. This is usually caused by another repository pushing to
hint: the same ref. If you want to integrate the remote changes, use
hint: 'git pull' before pushing again.
```

Git refuses. Where the pendrive said "replace the file?", Git says the shared copy has work Ravi hasn't seen. He pulls it in:

```bash
git pull origin main
cat app.js
```

```text
Auto-merging app.js
Merge made by the 'ort' strategy.

const title = "Corner Shop";
const currency = "INR";
const price = 120;
```

Both changes survived. Git knew which version both edits started from, so it could tell that Asha changed one line and Ravi changed another, and it combined them.

When the two of them change the **same** line (Asha sets the price to 150, Ravi to 99), Git doesn't guess:

```text
Auto-merging app.js
CONFLICT (content): Merge conflict in app.js
Automatic merge failed; fix conflicts and then commit the result.
```

```text
const title = "Corner Shop";
const currency = "INR";
const price = 150;
```

It stops and shows both versions, and a person decides. One thing the demo surfaced that I didn't expect: in my first attempt the two edits were on *neighbouring* lines, and Git reported a conflict there too. It treats changes that touch adjacent lines as overlapping, so "different lines" really means lines with at least one unchanged line between them.

## What version control records that a pendrive can't

Strip away the commands and version control is a record of the project's history. Every saved change, a **commit**, records:

- **what** changed, line by line;
- **who** made the change and **when**;
- **why**, in the commit message;
- **which version it was based on**: its parent commit.

That last item is the one the pendrive was missing. Because Git knows Ravi's change started from the same version as Asha's, it can tell "both edited" apart from "one is newer". The rest follows from it:

- Going back to Tuesday is one command, not a hunt through folders.
- Two people can work in parallel, on branches, and merge when they're done.
- Real overlaps become conflicts you resolve, not silent losses.

![Pendrive workflow vs version control workflow: with a pendrive, Asha's and Ravi's copies are both copied back to one file and the last copy wins; with version control, Asha pushes her commit and Ravi pulls, merges and pushes his to a shared repository that keeps the full history](https://mermaid.ink/img/pako:eNqVUk1r20AQ_SvDXHqRXUv-0AclkCbgSwvGLTlUm8NaO5aWSLtidhXHtf3fg9SqxCkUuqfZx7z35g1zwsIqwgz3tT0UlWQP3z8LFgYAwHW7kmVbwYaMYv1MucCxhIPlp54k8HHs75_STIXX1sCX7Vt8c5sLvHWV_OCgsO1R4CNMJjfnvoadLJ7OsLnPBba_9T_t-OONNQR7XVMAtXR-4MFBG_fOc7PNBW7ls_6X9kggo_7K93D3LRf4QOz6wQtrPNv6fxOurxI2jfbjHG3nqjOsew9XSSYFTK112ls-Djn3XV1DpV0PvHNbX2W7Vq3rABrikgIYLd6kxABL1gozzx0F2BA3sv_iqW8R6CtqSGAGAplU9zIpbG1ZoDAXDLCV5oe1zchm25UVZntZOwqwa5X0dK9lybL5gzIZRXxnO-MxixeDBmYnfMFsESbTKElXaTgL03g-mwd4xCyMoukiWkbzJIlnSZym8SXAn4PrbBqtwuUqCZdJslqk8TJAUv3Cvv461-FqL68yyd9y?type=png)
*Same two edits. One workflow keeps a single file; the other keeps the history both edits started from.*

## Why it became mandatory

Version control tools existed long before Git. Pro Git's [overview of version control](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control) runs from local tools like RCS, to centralized systems such as CVS and Subversion, to distributed systems such as Git and Mercurial. Git itself started in 2005, when the Linux kernel project needed a replacement for the tool it had been using; the [history of Git](https://git-scm.com/book/en/v2/Getting-Started-A-Short-History-of-Git) chapter has the details.

What made it mandatory rather than optional is how teams work now. Code review looks at a diff between two commits. CI runs tests on every push. Hosting platforms, deployment pipelines and "revert the release" all assume there's a shared history to point at. A team without version control can't take part in any of that. Being messier is the smaller problem.

## Where the analogy stops

**Version control isn't a backup.** A Git repository that only lives on your laptop dies with your laptop. History protects you from your own and your teammates' mistakes. It doesn't protect you from a dead disk. Pushing to a remote is what puts a second copy somewhere else.

**It's built for text.** Line-by-line merging works on code. Two people editing the same image or design file still end up taking turns. Git can store those files, and extensions like Git LFS exist for large ones, but it can't merge them line by line.

**It doesn't replace talking.** Git will tell you two people changed the same line. It won't tell you which price is right.

The takeaway: the pendrive workflow didn't lose code because people were careless. It lost code because a copied file has no history, and without history "newer" and "complete" look the same. If you want to see what that history looks like on disk, I walked through it in [what's inside the .git folder](https://jaydeepkanzariya.hashnode.dev/inside-git-dot-git-folder). The commands themselves are in [Git for Beginners](https://jaydeepkanzariya.hashnode.dev/git-for-beginners).

What's the strangest `final_v2`-style file name you've found in a real project, and did anyone know which one was current?
