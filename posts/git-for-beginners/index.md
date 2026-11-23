---
title: "Git for Beginners: Basics and Essential Commands"
slug: git-for-beginners
subtitle: What Git is, the three places your work lives, and a first workflow from git init to your first branch
tags: git, beginners, version-control, web-development, github
cover: ./cover.png
seoTitle: "Git for Beginners: Basics and Essential Commands"
seoDescription: "Learn Git from zero: repository, commit, branch and HEAD, the staging area explained, and a first workflow with git init, add, commit, log and switch."
enableToc: true
---

If you've ever had a folder that looks like this, you already understand the problem Git solves:

```text
index.html
index-v2.html
index-final.html
index-final-REALLY-final.html
```

Every copy is a save point. None of them tell you what changed, why, or which one actually works.

Git replaces that folder with one clean project and a full history behind it. This guide covers Git basics for beginners: what Git is, the handful of terms you need, and a first workflow from an empty folder to your first branch. Every terminal output below is real, from Git 2.56.0.

## What Git is

Git is a **version control system**: a tool that records snapshots of your project over time, so you can see what changed, go back, and try things without fear.

It's also **distributed**. Every copy of a Git project carries the complete history on its own. Your laptop doesn't need a server to commit, view history or switch versions. When you work with others, you share history between copies; nobody's copy is the only real one.

One common mix-up: **Git is not GitHub.** Git is the tool on your computer. GitHub is a website that hosts Git repositories so people can share them. You can use Git for years without ever touching GitHub.

## Why developers use Git

- **Undo with confidence.** Every commit is a save point you can return to.
- **See what changed, and why.** Each commit records the exact changes, who made them, when, and a message explaining them.
- **Try ideas safely.** A branch lets you experiment without touching the working version.
- **Work with other people.** Several developers can change the same project and combine their work.

## The core terms

Four words cover most of what you'll read about Git:

- **Repository (repo):** your project folder plus its entire history. The history lives in a hidden `.git` folder inside the project.
- **Commit:** a saved snapshot of your project at one moment, with a message and a unique ID (a hash like `523d7bc`). A commit stores the whole project as it was, not just a list of edits. Git stores it efficiently, but you can think of every commit as a complete save point.
- **Branch:** a named line of commits. The default one is usually called `main`. A new branch lets you work on something without affecting `main`.
- **HEAD:** a pointer to where you are right now, normally the latest commit on the branch you're on. When you see `HEAD -> main`, read it as "you are here, on main".

## The three areas: why `git add` comes before `git commit`

The question nearly every beginner asks: why two steps? Why not save directly?

Because Git has three places your work can be:

![The three areas of Git: files in the working directory move to the staging area with git add, then into the repository with git commit](https://mermaid.ink/img/pako:eNo9kUFvgkAQhf_KZM5oARUW0piYemyTRg8mdXvYsgNslF0yLK1W_e8NNHqcN3nfm8y7YOE0YY7l0f0UtWIPrxvJ0gIA7NZ7iTvHB2Mr0Iap8I7Pz1_8tCzNkTo4ux5IGy_xEyaT5bUyHpTWV9iu9hK3XlWDUzGp0VTUylbUQWuKA2koHY-yrwksnTwUrmlG2P2A7eqB_d9dYfO-l7ih1nXmcUynvklDZ1Xb1c53o2YsTKsRhgFWbDTmnnsKsCFu1DDiZQiR6GtqSGIOEpl0f5oU7uhYorQ3DLBV9sO55u5m11c15qU6dhRg32rlaW1Uxap5qExWE7-43nrMZ2JkYH7BE-bzSExjkSVZFEZZOgtnAZ4xj-J4Oo8X8UyINBRplqW3AH_H1HAaJ9EiEdFCiGSepYsAh4c7fvuvbWzv9gdvt5L9?type=png)
*Changes move from your files, to the staging area, to the repository.*

1. **Working directory:** the actual files you edit in your editor.
2. **Staging area:** a holding area where you choose which changes go into the next commit.
3. **Repository:** the permanent history of commits.

The staging area exists so a commit can be **one meaningful change**, not "everything I touched today". Fixed a typo and started a new feature in the same hour? Stage and commit the typo fix alone, then the feature separately. Your history stays readable, and undoing one doesn't undo the other.

`git add` moves changes into the staging area. `git commit` saves whatever is staged as a new snapshot.

## Your first Git workflow, step by step

Open a terminal. Every command below can be typed exactly as shown.

### 1. Tell Git who you are (once per computer)

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

Git attaches your name and email to every commit. The third line makes new projects start on a branch called `main`. Without it, Git 2.56 still names the first branch `master` and prints a long hint about the default changing in Git 3.0. `main` is what GitHub uses, so it's the less confusing choice.

### 2. Create a repository: `git init`

```bash
mkdir my-website
cd my-website
git init
```

```text
Initialized empty Git repository in .../my-website/.git/
```

That `.git` folder is the repository. It's hidden, and you never edit it by hand. Here's what's inside, at a beginner level:

![A local Git repository: the my-website folder holds your files and a hidden .git folder, which contains objects for saved snapshots, refs for branch names, HEAD for the current branch, and config for settings](https://mermaid.ink/img/pako:eNpl0stu2zAQBdBfGcymG1mx5IceKAIEcZFsihZFVxGzoKWRyNTiGEMqjmr43wvLTjdekrjnkgTniDU3hCW2Oz7URkuA3xslygEA_KwU9uPsQFtvA9193crd_ciDQGt35Es4sPyxroPGCtWBZVT4CrPZPTxVCuPOhgsJhkBoz95eM5_9T1P4R6WQt29UB3_J0zvJCF6_UwPe6b03HG7Ur0qhUHslW9GuNuB0Tz4CirsYem3djXquFD5_e9hM6GBsbeBKRx6-CAHfmsdKYc2utd2kPIVgXeehZYFgrJ_epvAVI-zENlgGGSjCnqTX5yUez20Kg6GeFJZwvngzfMxq3rEoVO6EEe61e2HuP7Xw0BksW73zFOGwb3SgjdWd6P7_rpBrSB55cAHLZTp1YHnEDyyXSR6nebEuknlSZIv5IsIRyyRN42W6Shd5ns3zrCiyU4R_p1PncbpOVus8WeX5ellkqwipOf_X98t4TFNy-gc9TbAy?type=png)
*A local repository. Your files sit next to `.git`, which holds the history.*

Delete `.git` and the history is gone; your current files stay. That's the whole difference between "a folder" and "a Git repository".

### 3. Check what Git sees: `git status`

Create two files, `index.html` and `style.css`, with any content. Then:

```bash
git status
```

```text
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	index.html
	style.css

nothing added to commit but untracked files present (use "git add" to track)
```

**Untracked** means Git sees the files but isn't recording them yet. `git status` is the command you'll run most. When in doubt, run it: it always tells you where things stand, and usually what to do next.

### 4. Stage your changes: `git add`

```bash
git add index.html style.css
```

You can also use `git add .` to stage everything in the current folder. Run `git status` again:

```text
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   index.html
	new file:   style.css
```

Both files are now in the staging area, waiting for a commit.

### 5. Save a snapshot: `git commit`

```bash
git commit -m "Add home page and styles"
```

```text
[main (root-commit) 0793928] Add home page and styles
 2 files changed, 8 insertions(+)
 create mode 100644 index.html
 create mode 100644 style.css
```

That's your first commit. `0793928` is the start of its ID; yours will be different, because the ID depends on the content, author and time. `-m` sets the message. Write messages that say what the change does: "Add home page and styles", not "update" or "stuff".

### 6. Change something, see the difference: `git diff`

Add a paragraph to `index.html`, then run `git status`:

```text
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   index.html

no changes added to commit (use "git add" and/or "git commit -a")
```

To see exactly what changed:

```bash
git diff
```

```diff
diff --git a/index.html b/index.html
index 44e99bb..1a9d657 100644
--- a/index.html
+++ b/index.html
@@ -3,5 +3,6 @@
 <head><title>My Website</title></head>
 <body>
   <h1>Hello, Git</h1>
+  <p>My first tracked change.</p>
 </body>
 </html>
```

Lines starting with `+` were added; lines with `-` were removed. Happy with it? Stage and commit:

```bash
git add index.html
git commit -m "Add intro paragraph"
```

### 7. Read the history: `git log`

```bash
git log --oneline
```

```text
523d7bc (HEAD -> main) Add intro paragraph
0793928 Add home page and styles
```

Newest first. Plain `git log` shows the same commits with full IDs, author and date. `(HEAD -> main)` is the "you are here" marker.

### 8. Try an idea on a branch: `git switch -c`

```bash
git switch -c dark-mode
```

```text
Switched to a new branch 'dark-mode'
```

Add a dark background to `style.css`, then `git add style.css` and `git commit -m "Try a dark theme"`. The log on this branch:

```text
6b85f46 (HEAD -> dark-mode) Try a dark theme
523d7bc (main) Add intro paragraph
0793928 Add home page and styles
```

Now switch back:

```bash
git switch main
git log --oneline
```

```text
523d7bc (HEAD -> main) Add intro paragraph
0793928 Add home page and styles
```

The dark theme commit isn't on `main`, and `style.css` on disk is back to the version without it. The experiment still exists on `dark-mode`; `main` is untouched.

![Commit history: three commits in a row, 0793928 Add home page, 523d7bc Add intro paragraph and 6b85f46 Try a dark theme; the main branch points at 523d7bc, dark-mode points at 6b85f46, and HEAD points at main](https://mermaid.ink/img/pako:eNpNkctqg0AUhl9lOKsW1Op4mQslEJJCFs2mdFUni4kzUWl05FRp0pB3L9rmsjz833cunBMUzliQsNu776LS2JPXN4WqJYSQRZQrCJmIBeXPW3yazY0hlWss6XRpFWyI78_IguYKUhobti2uVN326EinUZeou0rB5tqU_llxriDb8nSXZJP1jkeiidH4SfrKNvZOWT_kChpdtwo2j8QPpqGXcDmGo-Y3ztg7Ir4Qq5FYvcyXt3ANHpRYG5A9DtaDxmKjxxJOo6PgfwVJFKA1w8Ev3N6hAtWewYNOtx_ONRcb3VBWIHd6_2U9GDqje7usx8tviG2NxYUb2h5kwqYWIE9wAJlEPKBcZCIKI8HiMPbgCDKiNEhoSmPOWciZEOzswc80NAxoFqUZj1LOs0Sw1ANr6t7h-u-V00fPvyWiiww?type=png)
*Commit history. Each commit points back to the one before it; branch names point at their latest commit, and HEAD points at the branch you're on.*

## The essential commands

| Command | What it does |
|---|---|
| `git init` | Turn the current folder into a repository |
| `git status` | Show what's changed, staged or untracked |
| `git add <file>` | Stage a file's changes for the next commit |
| `git add .` | Stage all changes in the current folder |
| `git commit -m "msg"` | Save the staged changes as a new commit |
| `git diff` | Show unstaged changes, line by line |
| `git log --oneline` | Show the commit history, one line each |
| `git branch` | List branches; `*` marks the current one |
| `git switch -c <name>` | Create a new branch and move to it |
| `git switch <name>` | Move to an existing branch |

## Where beginners get stuck

**`git add .` without looking.** It stages everything, including files you didn't mean to commit. Run `git status` first, every time, and read the list.

**Committing secrets.** Passwords and API keys in a file like `.env` don't belong in a repository; once committed, they stay in the history even if you delete the file later. Create a file called `.gitignore` and list the files Git should never track:

```text
.env
node_modules/
```

Git then leaves those files out of `git status` and `git add .`.

**Messages like "fix" or "changes".** In three weeks you'll want to know what each commit did. One clear sentence per commit pays for itself the first time you search the history.

The takeaway: Git is three areas and a handful of commands that move changes between them. **Edit, `add`, `commit`, repeat**, with `git status` whenever you're unsure.

The limit of this guide is that everything here happens on your own computer. Sharing work through GitHub (`git push`, `git pull`), and bringing a branch back into `main` (`git merge`), are the next steps, and they build directly on these commands.

Run through the eight steps once in an empty folder. Which Git message confused you first, and did `git status` help you work it out?
