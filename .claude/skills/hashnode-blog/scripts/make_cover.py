#!/usr/bin/env python3
"""
make_cover.py — generate a Hashnode cover image (1600x840 PNG by default).

Three visual directions, all grounded in the developer's own world
(source files, terminals, engineering drawings) rather than generic gradients:

  codeframe  (default)  a source-file card: filename tab, line-number gutter,
                        title set as the file's content, accent underline
  terminal              a shell session: prompt line, title as output, tag chips
  blueprint             light engineering-paper look: hairline grid,
                        registration marks, highlighter swipe on key words

Usage
  python3 make_cover.py \
    --title "Why your *useEffect* runs twice" \
    --subtitle "StrictMode, double invocation, and the bugs it exposes" \
    --kicker "react · deep dive" \
    --tech react \
    --author "Jaydeep Kanzariya" \
    --handle "@jaydeep" \
    --file "use-effect-twice.md" \
    --out cover.png

Wrap any word(s) of the title in *asterisks* to highlight them in the accent
colour. Keep it to one phrase — the highlight is the one loud thing on the card.

Everything else has a sane default. --tech picks the accent colour; pass
--accent "#RRGGBB" to override it. Output is PNG (Hashnode does not accept SVG
covers) and stays well under the 8 MB upload limit.
"""

import argparse
import math
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    sys.exit("Pillow is required: pip install pillow")

# --------------------------------------------------------------------------
# fonts
# --------------------------------------------------------------------------

# Windows: system fonts dir, plus the per-user dir that "Install" (not
# "Install for all users") writes to.
_WIN_SYS = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
_WIN_USER = os.path.join(os.environ.get("LOCALAPPDATA", ""),
                         "Microsoft", "Windows", "Fonts")

DISPLAY_CANDIDATES = [
    "/usr/share/fonts/truetype/google-fonts/Poppins-{w}.ttf",
    "/usr/share/fonts/truetype/Inter-{w}.ttf",
    os.path.join(_WIN_USER, "Poppins-{w}.ttf"),
    os.path.join(_WIN_SYS, "Poppins-{w}.ttf"),
    os.path.join(_WIN_USER, "Inter-{w}.ttf"),
    os.path.join(_WIN_SYS, "Inter-{w}.ttf"),
    "/usr/share/fonts/truetype/dejavu/DejaVuSans{dj}.ttf",
    os.path.join(_WIN_SYS, "{segoe}.ttf"),  # Segoe UI ships with Windows
]
MONO_CANDIDATES = [
    "/usr/share/fonts/truetype/jetbrains/JetBrainsMono-{w}.ttf",
    os.path.join(_WIN_USER, "JetBrainsMono-{w}.ttf"),
    os.path.join(_WIN_SYS, "JetBrainsMono-{w}.ttf"),
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono{dj}.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationMono-{w}.ttf",
    os.path.join(_WIN_SYS, "{consolas}.ttf"),  # Consolas ships with Windows
]

_DJ = {"Bold": "-Bold", "Medium": "", "Regular": "", "Light": "-ExtraLight"}
_DJM = {"Bold": "-Bold", "Medium": "", "Regular": "", "Light": ""}
_SEGOE = {"Bold": "segoeuib", "Medium": "seguisb", "Regular": "segoeui",
          "Light": "segoeuil"}
_CONSOLAS = {"Bold": "consolab", "Regular": "consola"}


def _resolve(candidates, weight, dj_map, override=None):
    if override and os.path.exists(override):
        return override
    for pattern in candidates:
        path = pattern.format(w=weight, dj=dj_map.get(weight, ""),
                              segoe=_SEGOE.get(weight, "segoeui"),
                              consolas=_CONSOLAS.get(weight, "consola"))
        if os.path.exists(path):
            return path
    raise SystemExit("No usable font found. Pass --font-display / --font-mono.")


class Fonts:
    def __init__(self, display_override=None, mono_override=None):
        self.display_paths = {
            w: _resolve(DISPLAY_CANDIDATES, w, _DJ, display_override)
            for w in ("Bold", "Medium", "Regular", "Light")
        }
        self.mono_paths = {
            w: _resolve(MONO_CANDIDATES, w, _DJM, mono_override)
            for w in ("Bold", "Regular")
        }
        self._cache = {}

    def display(self, size, weight="Bold"):
        return self._get(self.display_paths[weight], size)

    def mono(self, size, weight="Regular"):
        return self._get(self.mono_paths[weight], size)

    def _get(self, path, size):
        key = (path, int(size))
        if key not in self._cache:
            self._cache[key] = ImageFont.truetype(path, int(size))
        return self._cache[key]


# --------------------------------------------------------------------------
# palette
# --------------------------------------------------------------------------

TECH_ACCENTS = {
    # languages
    "javascript": "#F2C14E", "typescript": "#4C8DFF", "python": "#4FA3D1",
    "go": "#4FD1D9", "rust": "#F0803C", "java": "#E76F51", "kotlin": "#A97BFF",
    "swift": "#FF7A59", "php": "#8B7BE8", "ruby": "#E05C6E", "csharp": "#8E6FE0",
    "dotnet": "#8E6FE0", "cpp": "#5C9DFF", "c": "#5C9DFF", "dart": "#37B5C9",
    # frontend
    "react": "#5CD3EE", "nextjs": "#E6E9EF", "vue": "#54C58C", "angular": "#E8546B",
    "svelte": "#FF6A3D", "tailwind": "#4FC3D9", "css": "#5C9DFF", "html": "#F08A4B",
    "storybook": "#FF67B6", "vite": "#B76BFF", "webpack": "#63C0E8",
    # backend / data
    "node": "#7FC96A", "express": "#9AA7BD", "nestjs": "#E8546B",
    "postgres": "#5C9DD8", "postgresql": "#5C9DD8", "mysql": "#4FA0B8",
    "mongodb": "#5FC97E", "redis": "#E8574A", "sqlite": "#68A5D8",
    "graphql": "#E858A6", "prisma": "#5CC9C0", "kafka": "#9AA0FF",
    # platform
    "docker": "#4FA8F0", "kubernetes": "#5B7CF0", "aws": "#F0973C",
    "azure": "#41A5F5", "gcp": "#5B9BF0", "terraform": "#8C6BF0",
    "devops": "#59C2B0", "linux": "#F2C14E", "git": "#F0703C", "github": "#C9D1E0",
    "cicd": "#59C2B0", "security": "#F05C6E", "testing": "#6FD98F",
    # ai
    "ai": "#B98CFF", "ml": "#B98CFF", "llm": "#B98CFF", "openai": "#5FD4B0",
    "rag": "#B98CFF", "pytorch": "#F0703C", "tensorflow": "#F0973C",
}
DEFAULT_ACCENT = "#6FA8FF"


def accent_for(tech, override):
    if override:
        return override if override.startswith("#") else "#" + override
    if not tech:
        return DEFAULT_ACCENT
    key = tech.lower().replace(".", "").replace("-", "").replace(" ", "")
    return TECH_ACCENTS.get(key, DEFAULT_ACCENT)


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mix(c1, c2, t):
    return tuple(round(a + (b - a) * t) for a, b in zip(c1, c2))


def rgba(c, a):
    return (c[0], c[1], c[2], int(a * 255))


# --------------------------------------------------------------------------
# text helpers
# --------------------------------------------------------------------------

def tokenize(text):
    """'Why *useEffect* runs twice' -> [('Why', False), ('useEffect', True), ...]"""
    tokens, hot = [], False
    for chunk in text.split("*"):
        for word in chunk.split():
            tokens.append((word, hot))
        hot = not hot
    return tokens


def token_width(draw, token, font):
    return draw.textlength(token, font=font)


def wrap_tokens(draw, tokens, font, max_width):
    lines, current, width = [], [], 0.0
    space = draw.textlength(" ", font=font)
    for word, hot in tokens:
        w = token_width(draw, word, font)
        add = w if not current else width + space + w
        if current and add > max_width:
            lines.append(current)
            current, width = [(word, hot)], w
        else:
            current.append((word, hot))
            width = add
    if current:
        lines.append(current)
    return lines


def fit_title(draw, tokens, fonts, weight, max_width, max_lines, hi, lo):
    """Largest size where the title wraps into at most max_lines."""
    size = hi
    while size > lo:
        font = fonts.display(size, weight)
        lines = wrap_tokens(draw, tokens, font, max_width)
        if len(lines) <= max_lines and all(
            sum(token_width(draw, w, font) for w, _ in ln)
            + draw.textlength(" ", font=font) * (len(ln) - 1) <= max_width
            for ln in lines
        ):
            return font, lines
        size -= 3
    font = fonts.display(lo, weight)
    return font, wrap_tokens(draw, tokens, font, max_width)[:max_lines]


def token_spans(draw, x, line, font):
    """x-ranges of the highlighted tokens in a wrapped line."""
    space = draw.textlength(" ", font=font)
    spans = []
    for i, (word, hot) in enumerate(line):
        if i:
            x += space
        w = draw.textlength(word, font=font)
        if hot:
            spans.append((x, x + w))
        x += w
    return spans


def draw_tokens(draw, xy, line, font, base_color, hot_color):
    x, y = xy
    space = draw.textlength(" ", font=font)
    spans = []
    for i, (word, hot) in enumerate(line):
        if i:
            x += space
        w = draw.textlength(word, font=font)
        draw.text((x, y), word, font=font, fill=hot_color if hot else base_color)
        if hot:
            spans.append((x, x + w))
        x += w
    return x, spans


def draw_tracked(draw, xy, text, font, fill, tracking):
    """Letter-spaced text — small caps labels need air to read as labels."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking
    return x


def text_height(draw, font):
    box = draw.textbbox((0, 0), "Hxg", font=font)
    return box[3] - box[1]


# --------------------------------------------------------------------------
# background helpers
# --------------------------------------------------------------------------

def vertical_gradient(size, top, bottom):
    w, h = size
    strip = Image.new("RGB", (1, h))
    px = strip.load()
    for y in range(h):
        px[0, y] = mix(top, bottom, y / max(1, h - 1))
    return strip.resize((w, h), Image.BILINEAR)


def radial_glow(size, color, center, radius, strength):
    """Soft accent bloom — one light source, so the card reads as lit, not painted."""
    w, h = size
    small = (max(2, w // 8), max(2, h // 8))
    layer = Image.new("L", small, 0)
    px = layer.load()
    cx, cy = center[0] / 8, center[1] / 8
    r = radius / 8
    for y in range(small[1]):
        for x in range(small[0]):
            d = math.hypot(x - cx, y - cy) / r
            if d < 1:
                px[x, y] = int(255 * strength * (1 - d) ** 2)
    layer = layer.resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(18))
    glow = Image.new("RGBA", (w, h), color + (0,))
    glow.putalpha(layer)
    return glow


def stamp(base, layer):
    """Paste a translucent RGBA layer onto an RGB base (real alpha blending)."""
    base.paste(layer, (0, 0), layer)
    return base


def dot_grid(size, color, step, alpha, radius=1):
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, "RGBA")
    for y in range(step, size[1], step):
        for x in range(step, size[0], step):
            d.ellipse([x - radius, y - radius, x + radius, y + radius],
                      fill=rgba(color, alpha))
    return layer


def line_grid(size, color, step, alpha, width=1):
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, "RGBA")
    for x in range(step, size[0], step):
        d.line([(x, 0), (x, size[1])], fill=rgba(color, alpha), width=width)
    for y in range(step, size[1], step):
        d.line([(0, y), (size[0], y)], fill=rgba(color, alpha), width=width)
    return layer


# --------------------------------------------------------------------------
# style: codeframe
# --------------------------------------------------------------------------

def render_codeframe(cfg, fonts):
    W, H = cfg["size"]
    s = W / 1600
    accent = hex_rgb(cfg["accent"])
    ink_top, ink_bottom = (11, 16, 28), (17, 24, 42)
    card_fill = (17, 23, 40)
    white = (240, 244, 250)
    muted = (138, 152, 176)

    img = vertical_gradient((W, H), ink_top, ink_bottom)
    stamp(img, radial_glow((W, H), accent, (W * 0.84, H * 0.08), W * 0.62, 0.40))
    stamp(img, dot_grid((W, H), (255, 255, 255), int(34 * s), 0.06))

    d = ImageDraw.Draw(img, "RGBA")
    m = int(46 * s)
    card = [m, m, W - m, H - m]
    d.rounded_rectangle(card, radius=int(26 * s), fill=card_fill + (228,),
                        outline=rgba((255, 255, 255), 0.10), width=max(1, int(1.5 * s)))

    # --- header: filename tab + publication handle
    head_h = int(70 * s)
    hx, hy = card[0], card[1]
    tab_font = fonts.mono(int(21 * s))
    label = cfg["file"]
    tab_w = d.textlength(label, font=tab_font) + int(52 * s)
    d.rounded_rectangle([hx, hy, hx + tab_w, hy + head_h],
                        radius=int(26 * s), fill=(24, 32, 54, 255))
    d.rectangle([hx, hy + head_h - int(28 * s), hx + tab_w, hy + head_h], fill=(24, 32, 54, 255))
    d.rectangle([hx + int(2 * s), hy + head_h - int(3 * s), hx + tab_w, hy + head_h],
                fill=accent + (255,))
    d.text((hx + int(26 * s), hy + head_h / 2), label, font=tab_font,
           fill=(206, 217, 235), anchor="lm")
    d.line([(hx, hy + head_h), (card[2], hy + head_h)], fill=rgba((255, 255, 255), 0.08),
           width=max(1, int(1.5 * s)))
    if cfg["handle"]:
        d.text((card[2] - int(28 * s), hy + head_h / 2), cfg["handle"],
               font=fonts.mono(int(19 * s)), fill=(104, 118, 142), anchor="rm")

    # --- body geometry
    gutter_x = card[0] + int(26 * s)
    text_x = card[0] + int(104 * s)
    text_w = card[2] - text_x - int(60 * s)
    num_font = fonts.mono(int(19 * s))
    rows = []  # (y, font) per rendered line, for the gutter numbers

    kicker_font = fonts.mono(int(20 * s), "Bold")
    sub_font = fonts.display(int(27 * s), "Light")
    title_font, title_lines = fit_title(
        d, cfg["tokens"], fonts, "Bold", text_w,
        cfg["max_lines"], int(96 * s), int(46 * s))
    title_lh = title_font.size * 1.16

    kicker_h = text_height(d, kicker_font) if cfg["kicker"] else 0
    sub_lines = wrap_tokens(d, [(w, False) for w in cfg["subtitle"].split()],
                            sub_font, text_w)[:2] if cfg["subtitle"] else []
    sub_lh = sub_font.size * 1.4

    block_h = (kicker_h + int(34 * s) if cfg["kicker"] else 0) \
        + title_lh * len(title_lines) \
        + (int(26 * s) + sub_lh * len(sub_lines) if sub_lines else 0)
    y = card[1] + head_h + (card[3] - card[1] - head_h - int(74 * s) - block_h) / 2

    if cfg["kicker"]:
        rows.append((y, kicker_font))
        draw_tracked(d, (text_x, y), cfg["kicker"].upper(), kicker_font,
                     mix(accent, (255, 255, 255), 0.15), int(2.4 * s))
        y += kicker_h + int(34 * s)

    for line in title_lines:
        rows.append((y, title_font))
        # highlighted words get an inline-code chip — same idiom as the file motif
        probe_spans = token_spans(d, text_x, line, title_font)
        for x0, x1 in probe_spans:
            pad = int(12 * s)
            d.rounded_rectangle([x0 - pad, y + title_font.size * 0.14,
                                 x1 + pad, y + title_font.size * 1.08],
                                radius=int(10 * s), fill=rgba(accent, 0.16))
        draw_tokens(d, (text_x, y), line, title_font, white,
                    mix(accent, (255, 255, 255), 0.10))
        y += title_lh

    if sub_lines:
        y += int(26 * s)
        for line in sub_lines:
            rows.append((y, sub_font))
            draw_tokens(d, (text_x, y), line, sub_font, muted, muted)
            y += sub_lh

    for i, (ry, rf) in enumerate(rows, start=1):
        d.text((gutter_x, ry + rf.size * 0.42), f"{i:02d}", font=num_font,
               fill=(78, 92, 118), anchor="lm")

    # --- footer
    fy = card[3] - int(40 * s)
    if cfg["author"]:
        d.ellipse([text_x, fy - int(6 * s), text_x + int(12 * s), fy + int(6 * s)],
                  fill=accent + (255,))
        d.text((text_x + int(26 * s), fy), cfg["author"],
               font=fonts.display(int(21 * s), "Medium"), fill=(178, 190, 212), anchor="lm")
    if cfg["meta"]:
        d.text((card[2] - int(28 * s), fy), cfg["meta"], font=fonts.mono(int(19 * s)),
               fill=(104, 118, 142), anchor="rm")
    return img


# --------------------------------------------------------------------------
# style: terminal
# --------------------------------------------------------------------------

def render_terminal(cfg, fonts):
    W, H = cfg["size"]
    s = W / 1600
    accent = hex_rgb(cfg["accent"])
    bg = (7, 10, 16)
    white = (238, 243, 250)

    img = vertical_gradient((W, H), bg, (13, 18, 28))
    stamp(img, radial_glow((W, H), accent, (W * 0.10, H * 0.92), W * 0.62, 0.28))
    d = ImageDraw.Draw(img, "RGBA")

    # scanline texture keeps the flat black from reading as empty
    for ly in range(0, H, max(4, int(5 * s))):
        d.line([(0, ly), (W, ly)], fill=rgba((255, 255, 255), 0.022))

    bar_h = int(64 * s)
    d.rectangle([0, 0, W, bar_h], fill=(16, 22, 32, 255))
    d.line([(0, bar_h), (W, bar_h)], fill=rgba((255, 255, 255), 0.08))
    for i in range(3):
        cx = int(38 * s) + i * int(28 * s)
        d.ellipse([cx - int(7 * s), bar_h / 2 - int(7 * s),
                   cx + int(7 * s), bar_h / 2 + int(7 * s)],
                  fill=(58, 68, 86, 255))
    d.text((W / 2, bar_h / 2), cfg["file"], font=fonts.mono(int(20 * s)),
           fill=(126, 140, 164), anchor="mm")

    x = int(78 * s)
    text_w = W - x * 2

    prompt_font = fonts.mono(int(24 * s))
    title_probe, probe_lines = fit_title(
        d, cfg["tokens"], fonts, "Bold", text_w - int(40 * s),
        cfg["max_lines"], int(88 * s), int(44 * s))
    sub_font = fonts.display(int(26 * s), "Light")
    sub_lines = wrap_tokens(d, [(w, False) for w in cfg["subtitle"].split()],
                            sub_font, text_w - int(60 * s))[:2] if cfg["subtitle"] else []
    block_h = int(64 * s) + title_probe.size * 1.15 * len(probe_lines) \
        + (int(20 * s) + sub_font.size * 1.4 * len(sub_lines) if sub_lines else 0)
    y = bar_h + (H - bar_h - int(110 * s) - block_h) / 2

    d.text((x, y), "~/posts", font=prompt_font, fill=(96, 190, 150))
    px = x + d.textlength("~/posts ", font=prompt_font)
    d.text((px, y), "$", font=prompt_font, fill=accent)
    px += d.textlength("$ ", font=prompt_font)
    d.text((px, y), f"cat {cfg['file']}", font=prompt_font, fill=(150, 164, 190))
    y += int(64 * s)

    title_font, title_lines = title_probe, probe_lines
    lh = title_font.size * 1.15
    for i, line in enumerate(title_lines):
        if i == 0:
            d.text((x, y + title_font.size * 0.18), "›", font=fonts.mono(int(38 * s)),
                   fill=accent)
        draw_tokens(d, (x + int(40 * s), y), line, title_font, white, accent)
        y += lh

    if sub_lines:
        y += int(20 * s)
        for line in sub_lines:
            draw_tokens(d, (x + int(40 * s), y), line, sub_font, (146, 160, 184), accent)
            y += sub_font.size * 1.4

    # tag chips + cursor block
    chip_font = fonts.mono(int(20 * s))
    cy = H - int(74 * s)
    cx = x
    for tag in cfg["tags"][:4]:
        label = f"#{tag}"
        w = d.textlength(label, font=chip_font) + int(34 * s)
        d.rounded_rectangle([cx, cy, cx + w, cy + int(44 * s)], radius=int(22 * s),
                            outline=rgba(accent, 0.42), width=max(1, int(1.5 * s)))
        d.text((cx + w / 2, cy + int(22 * s)), label, font=chip_font,
               fill=mix(accent, (255, 255, 255), 0.25), anchor="mm")
        cx += w + int(14 * s)
    if cfg["author"]:
        d.text((W - int(78 * s), cy + int(22 * s)), cfg["author"],
               font=fonts.mono(int(21 * s)), fill=(120, 134, 158), anchor="rm")
    return img


# --------------------------------------------------------------------------
# style: blueprint
# --------------------------------------------------------------------------

def render_blueprint(cfg, fonts):
    W, H = cfg["size"]
    s = W / 1600
    accent = hex_rgb(cfg["accent"])
    paper = (238, 241, 244)
    ink = (16, 24, 34)
    muted = (104, 118, 134)

    img = Image.new("RGB", (W, H), paper)
    stamp(img, line_grid((W, H), ink, int(48 * s), 0.05))
    stamp(img, line_grid((W, H), ink, int(192 * s), 0.10))
    d = ImageDraw.Draw(img, "RGBA")

    # registration marks — drafting convention, not decoration
    for cx, cy in [(int(44 * s), int(44 * s)), (W - int(44 * s), int(44 * s)),
                   (int(44 * s), H - int(44 * s)), (W - int(44 * s), H - int(44 * s))]:
        d.line([(cx - int(14 * s), cy), (cx + int(14 * s), cy)], fill=rgba(ink, 0.35))
        d.line([(cx, cy - int(14 * s)), (cx, cy + int(14 * s))], fill=rgba(ink, 0.35))

    x = int(104 * s)
    text_w = W - x - int(140 * s)

    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    kf_probe = fonts.mono(int(21 * s), "Bold")
    tf_probe, tl_probe = fit_title(probe, cfg["tokens"], fonts, "Bold", text_w,
                                   cfg["max_lines"], int(92 * s), int(44 * s))
    sf_probe = fonts.display(int(27 * s), "Light")
    sl_probe = wrap_tokens(probe, [(w, False) for w in cfg["subtitle"].split()],
                           sf_probe, text_w)[:2] if cfg["subtitle"] else []
    block_h = (text_height(probe, kf_probe) + int(60 * s) if cfg["kicker"] else 0) \
        + tf_probe.size * 1.14 * len(tl_probe) \
        + (int(24 * s) + sf_probe.size * 1.4 * len(sl_probe) if sl_probe else 0)
    y = int(96 * s) + max(0, (H - int(200 * s) - block_h) * 0.42)

    if cfg["kicker"]:
        kf = fonts.mono(int(21 * s), "Bold")
        draw_tracked(d, (x, y), cfg["kicker"].upper(), kf, muted, int(3 * s))
        y += text_height(d, kf) + int(20 * s)
        d.line([(x, y), (x + int(72 * s), y)], fill=accent + (255,), width=max(2, int(4 * s)))
        y += int(40 * s)

    title_font, title_lines = fit_title(
        d, cfg["tokens"], fonts, "Bold", text_w, cfg["max_lines"],
        int(92 * s), int(44 * s))
    lh = title_font.size * 1.14

    # highlighter swipe goes on its own rotated layer, behind the type
    swipe = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(swipe, "RGBA")
    ty = y
    for line in title_lines:
        cx = x
        space = probe.textlength(" ", font=title_font)
        for i, (word, hot) in enumerate(line):
            if i:
                cx += space
            w = probe.textlength(word, font=title_font)
            if hot:
                pad = int(10 * s)
                sd.rounded_rectangle(
                    [cx - pad, ty + title_font.size * 0.16,
                     cx + w + pad, ty + title_font.size * 1.06],
                    radius=int(6 * s), fill=rgba(accent, 0.34))
            cx += w
        ty += lh
    swipe = swipe.rotate(-0.7, resample=Image.BICUBIC, center=(x, int(H / 2)))
    stamp(img, swipe)
    d = ImageDraw.Draw(img, "RGBA")

    for line in title_lines:
        draw_tokens(d, (x, y), line, title_font, ink, ink)
        y += lh

    if cfg["subtitle"]:
        y += int(24 * s)
        sub_font = fonts.display(int(27 * s), "Light")
        for line in wrap_tokens(d, [(w, False) for w in cfg["subtitle"].split()],
                                sub_font, text_w)[:2]:
            draw_tokens(d, (x, y), line, sub_font, muted, muted)
            y += sub_font.size * 1.4

    ry = H - int(104 * s)
    d.line([(x, ry), (W - int(104 * s), ry)], fill=rgba(ink, 0.16))
    fy = ry + int(36 * s)
    if cfg["author"]:
        d.text((x, fy), cfg["author"], font=fonts.display(int(22 * s), "Medium"),
               fill=(52, 64, 80), anchor="lm")
    right = cfg["meta"] or (" · ".join(cfg["tags"][:3]) if cfg["tags"] else "")
    if right:
        d.text((W - int(104 * s), fy), right, font=fonts.mono(int(19 * s)),
               fill=muted, anchor="rm")
    return img


STYLES = {"codeframe": render_codeframe, "terminal": render_terminal,
          "blueprint": render_blueprint}


# --------------------------------------------------------------------------

def slugify(text):
    out = "".join(c.lower() if c.isalnum() else "-" for c in text)
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-")[:48]


def main():
    p = argparse.ArgumentParser(description="Generate a Hashnode cover image.")
    p.add_argument("--title", required=True,
                   help="Cover title. Wrap words in *asterisks* to accent them.")
    p.add_argument("--subtitle", default="")
    p.add_argument("--kicker", default="", help="Small label above the title.")
    p.add_argument("--tech", default="", help="react, node, postgres, docker, ai ...")
    p.add_argument("--accent", default="", help="Override accent, e.g. #5CD3EE")
    p.add_argument("--style", default="codeframe", choices=sorted(STYLES))
    p.add_argument("--author", default="")
    p.add_argument("--handle", default="", help="e.g. @yourname · yourblog.hashnode.dev")
    p.add_argument("--file", default="", help="Filename shown in the tab / prompt.")
    p.add_argument("--tags", default="", help="Comma-separated, used by terminal/blueprint.")
    p.add_argument("--meta", default="", help="Right-hand footer text, e.g. '8 min read'.")
    p.add_argument("--preset", default="hashnode", choices=["hashnode", "og", "square"])
    p.add_argument("--max-lines", type=int, default=3)
    p.add_argument("--font-display", default="")
    p.add_argument("--font-mono", default="")
    p.add_argument("--out", default="cover.png")
    a = p.parse_args()

    size = {"hashnode": (1600, 840), "og": (1200, 630), "square": (1080, 1080)}[a.preset]
    plain = a.title.replace("*", "")
    cfg = {
        "size": size,
        "tokens": tokenize(a.title),
        "subtitle": a.subtitle,
        "kicker": a.kicker or a.tech,
        "accent": accent_for(a.tech, a.accent),
        "author": a.author,
        "handle": a.handle,
        "file": a.file or f"{slugify(plain)}.md",
        "tags": [t.strip() for t in a.tags.split(",") if t.strip()]
                or ([a.tech] if a.tech else []),
        "meta": a.meta,
        "max_lines": a.max_lines,
    }

    fonts = Fonts(a.font_display or None, a.font_mono or None)
    img = STYLES[a.style](cfg, fonts).convert("RGB")
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    img.save(a.out, "PNG", optimize=True)
    kb = os.path.getsize(a.out) / 1024
    print(f"{a.out}  {size[0]}x{size[1]}  {kb:.0f} KB  style={a.style}  accent={cfg['accent']}")


if __name__ == "__main__":
    sys.exit(main())
