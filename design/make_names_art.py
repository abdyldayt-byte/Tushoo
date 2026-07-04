import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT_DIR = "/Users/abdyldamamashev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/afee1dec-7924-416e-8330-96742e2091ff/52aba0a4-cce8-431e-99db-d1b741de34da/skills/canvas-design/canvas-fonts"

NAVY = (47, 65, 86)
TEAL = (86, 124, 141)
BEIGE = (245, 239, 235)
BEIGE_DARK = (237, 229, 222)

W, H = 1440, 1920
SS = 2  # supersample factor for crisp edges
CW, CH = W * SS, H * SS

img = Image.new("RGB", (CW, CH), BEIGE)
draw = ImageDraw.Draw(img)

# ---- paper grain texture ----
random.seed(11)
grain = Image.new("L", (CW, CH), 0)
gdraw = ImageDraw.Draw(grain)
for _ in range(CW * CH // 900):
    x = random.randint(0, CW - 1)
    y = random.randint(0, CH - 1)
    v = random.randint(0, 40)
    gdraw.point((x, y), fill=v)
grain = grain.filter(ImageFilter.GaussianBlur(0.6))
img = Image.composite(Image.new("RGB", (CW, CH), BEIGE_DARK), img, grain)
draw = ImageDraw.Draw(img)

# ---- outer hairline frame ----
margin = int(70 * SS)
frame_w = max(2, int(2.4 * SS))
draw.rectangle(
    [margin, margin, CW - margin, CH - margin],
    outline=NAVY, width=frame_w
)
inner_pad = int(14 * SS)
draw.rectangle(
    [margin + inner_pad, margin + inner_pad, CW - margin - inner_pad, CH - margin - inner_pad],
    outline=TEAL, width=max(1, int(1.1 * SS))
)

cx = CW // 2
cy = CH // 2

# ---- twin-star emblem (Gemini motif) ----
def draw_star(center, r, color, width):
    cx0, cy0 = center
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx0 + rad * math.cos(ang), cy0 + rad * math.sin(ang)))
    draw.polygon(pts, outline=color, width=width)


def draw_twin_emblem(center_y, flip=False):
    star_gap = int(58 * SS)
    star_r = int(15 * SS)
    if not flip:
        arc_box = [cx - star_gap - star_r, center_y - int(46 * SS), cx + star_gap + star_r, center_y + star_r]
        draw.arc(arc_box, start=200, end=340, fill=TEAL, width=max(1, int(1.3 * SS)))
    else:
        arc_box = [cx - star_gap - star_r, center_y - star_r, cx + star_gap + star_r, center_y + int(46 * SS)]
        draw.arc(arc_box, start=20, end=160, fill=TEAL, width=max(1, int(1.3 * SS)))
    draw_star((cx - star_gap, center_y), star_r, NAVY, max(1, int(1.6 * SS)))
    draw_star((cx + star_gap, center_y), star_r, NAVY, max(1, int(1.6 * SS)))
    draw.ellipse(
        [cx - int(2.2 * SS), center_y - int(2.2 * SS), cx + int(2.2 * SS), center_y + int(2.2 * SS)],
        fill=TEAL
    )

# ---- vertical composition block, centered in canvas ----
# content heights (relative offsets from block top)
block = {
    "top_emblem": 0,
    "name_top": int(170 * SS),
    "amp": int(360 * SS),
    "name_bottom": int(480 * SS),
    "rule": int(710 * SS),
    "motto": int(756 * SS),
    "bottom_emblem": int(860 * SS),
}
block_height = block["bottom_emblem"]
start_y = cy - block_height // 2

emblem_y = start_y + block["top_emblem"] + int(46 * SS)
draw_twin_emblem(emblem_y, flip=False)

# ---- typography ----
italiana = ImageFont.truetype(f"{FONT_DIR}/Italiana-Regular.ttf", int(150 * SS))
italiana_med = ImageFont.truetype(f"{FONT_DIR}/Italiana-Regular.ttf", int(58 * SS))
serif_italic = ImageFont.truetype(f"{FONT_DIR}/InstrumentSerif-Italic.ttf", int(96 * SS))
crimson_small = ImageFont.truetype(f"{FONT_DIR}/CrimsonPro-Regular.ttf", int(30 * SS))


def draw_centered_text(y, text, font, fill, tracking=0):
    if tracking == 0:
        w = draw.textlength(text, font=font)
        draw.text((cx - w / 2, y), text, font=font, fill=fill)
        return w
    total_w = 0
    widths = []
    for ch in text:
        cw_ = draw.textlength(ch, font=font)
        widths.append(cw_)
        total_w += cw_ + tracking
    total_w -= tracking
    x = cx - total_w / 2
    for ch, cw_ in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += cw_ + tracking
    return total_w


name_top_y = start_y + block["name_top"]
draw_centered_text(name_top_y, "LEON", italiana, NAVY, tracking=int(10 * SS))

amp_y = start_y + block["amp"]
draw_centered_text(amp_y, "&", serif_italic, TEAL)

name_bottom_y = start_y + block["name_bottom"]
draw_centered_text(name_bottom_y, "MARCEL", italiana, NAVY, tracking=int(10 * SS))

# ---- divider rule with diamond ----
rule_y = start_y + block["rule"]
rule_half = int(120 * SS)
draw.line([(cx - rule_half, rule_y), (cx - int(14 * SS), rule_y)], fill=TEAL, width=max(1, int(1.3 * SS)))
draw.line([(cx + int(14 * SS), rule_y), (cx + rule_half, rule_y)], fill=TEAL, width=max(1, int(1.3 * SS)))
d = int(6 * SS)
draw.polygon(
    [(cx, rule_y - d), (cx + d, rule_y), (cx, rule_y + d), (cx - d, rule_y)],
    outline=NAVY, width=max(1, int(1.2 * SS))
)

# ---- heraldic motto ----
motto_y = start_y + block["motto"]
draw_centered_text(motto_y, "G E M I N I", crimson_small, TEAL, tracking=int(4 * SS))

# ---- mirrored bottom emblem for heraldic symmetry ----
bottom_emblem_y = start_y + block["bottom_emblem"] - int(46 * SS)
draw_twin_emblem(bottom_emblem_y, flip=True)

# ---- downsample for crisp anti-aliasing ----
final = img.resize((W, H), Image.LANCZOS)
out_path = "/Users/abdyldamamashev/TushooTwins/design/output/leon-marcel-names.png"
final.save(out_path, "PNG")
print("saved", out_path, final.size)
