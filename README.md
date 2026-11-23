# hashnode-blogs

Markdown source and cover images for my blog, **[jaydeepkanzariya.hashnode.dev](https://jaydeepkanzariya.hashnode.dev)**.

Beginner-friendly technical posts on web development, JavaScript, React, Git and networking. Every command output and code result in these posts comes from a real run, with the tool version stated. Nothing is made up.

## Posts

### HTML, CSS and the browser

| Post | Source |
|---|---|
| [How a Browser Works: From Pressing Enter to Pixels on Screen](https://jaydeepkanzariya.hashnode.dev/how-a-browser-works-from-pressing-enter-to-pixels-on-screen) | [`how-a-browser-works`](posts/how-a-browser-works/index.md) |
| [HTML Tags vs Elements: What You Type vs What the Browser Builds](https://jaydeepkanzariya.hashnode.dev/html-tags-vs-elements-what-you-type-vs-what-the-browser-builds) | [`html-tags-vs-elements`](posts/html-tags-vs-elements/index.md) |
| [CSS Selectors 101: Targeting Elements with Precision](https://jaydeepkanzariya.hashnode.dev/css-selectors-101-targeting-elements-with-precision) | [`css-selectors-101`](posts/css-selectors-101/index.md) |
| [Emmet for HTML: A Beginner's Guide to Writing Faster Markup](https://jaydeepkanzariya.hashnode.dev/emmet-for-html-a-beginner-s-guide-to-writing-faster-markup) | [`emmet-for-html`](posts/emmet-for-html/index.md) |

### JavaScript

| Post | Source |
|---|---|
| [Why "5" + 3 Is "53": JavaScript Operators for Beginners](https://jaydeepkanzariya.hashnode.dev/javascript-operators-basics) | [`javascript-operators-basics`](posts/javascript-operators-basics/index.md) |
| [Look Left of the Dot: How JavaScript Decides What this Is](https://jaydeepkanzariya.hashnode.dev/javascript-this-keyword) | [`javascript-this-keyword`](posts/javascript-this-keyword/index.md) |

### React

| Post | Source |
|---|---|
| [React Fundamentals: Components, JSX, State, and Re-rendering](https://jaydeepkanzariya.hashnode.dev/a-react-re-render-doesn-t-touch-the-dom-here-s-what-it-does) | not in this repo yet |
| [State Management: Context API, Prop Drilling, React.memo, useMemo, and useCallback](https://jaydeepkanzariya.hashnode.dev/react-memo-context-rerenders) | not in this repo yet |
| [The Virtual DOM isn't faster than the DOM — here's what it buys you](https://jaydeepkanzariya.hashnode.dev/virtual-dom-reconciliation-rendering) | [`virtual-dom-reconciliation-rendering`](posts/virtual-dom-reconciliation-rendering/index.md) |
| [How Does React Remember Between Renders? A Practical Guide to Hooks](https://jaydeepkanzariya.hashnode.dev/react-hooks-usestate-useeffect-custom-hooks) | [`react-hooks-usestate-useeffect-custom-hooks`](posts/react-hooks-usestate-useeffect-custom-hooks/index.md) |

### Git and version control

| Post | Source |
|---|---|
| [final_v2_latest_FINAL.zip: Why Version Control Exists](https://jaydeepkanzariya.hashnode.dev/why-version-control-exists) | [`why-version-control-exists`](posts/why-version-control-exists/index.md) |
| [Git for Beginners: Basics and Essential Commands](https://jaydeepkanzariya.hashnode.dev/git-for-beginners) | [`git-for-beginners`](posts/git-for-beginners/index.md) |
| [Git Doesn't Store Diffs: A Look Inside the .git Folder](https://jaydeepkanzariya.hashnode.dev/inside-git-dot-git-folder) | [`inside-git-dot-git-folder`](posts/inside-git-dot-git-folder/index.md) |

### Networking and the web

| Post | Source |
|---|---|
| [Is HTTP the Same as TCP? TCP, UDP and Where HTTP Fits](https://jaydeepkanzariya.hashnode.dev/tcp-vs-udp-and-http) | [`tcp-vs-udp-and-http`](posts/tcp-vs-udp-and-http/index.md) |
| [Why the TCP Handshake Takes Three Steps, Not Two](https://jaydeepkanzariya.hashnode.dev/why-the-tcp-handshake-takes-three-steps-not-two) | [`tcp-three-way-handshake`](posts/tcp-three-way-handshake/index.md) |
| [One Domain, Six Records: How DNS Record Types Work Together](https://jaydeepkanzariya.hashnode.dev/one-domain-six-records-how-dns-record-types-work-together) | [`dns-record-types-explained`](posts/dns-record-types-explained/index.md) |
| [Root, TLD, Authoritative: Tracing a DNS Lookup Step by Step](https://jaydeepkanzariya.hashnode.dev/how-dns-resolution-works) | [`how-dns-resolution-works`](posts/how-dns-resolution-works/index.md) |
| [A Browser Without the Browser: Getting Started with cURL](https://jaydeepkanzariya.hashnode.dev/a-browser-without-the-browser-getting-started-with-curl) | [`getting-started-with-curl`](posts/getting-started-with-curl/index.md) |
| [From Modem to Load Balancer: The Devices Between You and a Server](https://jaydeepkanzariya.hashnode.dev/network-devices-explained) | [`network-devices-explained`](posts/network-devices-explained/index.md) |

## Repository layout

```text
posts/<slug>/
  index.md     the post, with Hashnode frontmatter (title, slug, tags, SEO fields)
  cover.png    1600×840 cover image
system/        how the posts are written: the portable prompt and project notes
.claude/       the blog-writing skill and cover generator used with Claude Code
CLAUDE.md      default settings for new posts
```

Each `index.md` starts with YAML frontmatter that Hashnode's GitHub publishing reads. The `slug` field is the post's update key, so it never changes once a post is published. Some live URLs differ from the folder name because Hashnode built them from the title.

Covers are generated with:

```bash
python .claude/skills/hashnode-blog/scripts/make_cover.py \
  --title "Short cover *title*" --subtitle "One line" \
  --handle "jaydeepkanzariya.hashnode.dev" --out posts/<slug>/cover.png
```

It needs Python 3 and Pillow (`pip install pillow`).

## Author

**Jaydeep Kanzariya** · [jaydeepkanzariya.hashnode.dev](https://jaydeepkanzariya.hashnode.dev)
