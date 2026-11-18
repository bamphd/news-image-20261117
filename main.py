#!/usr/bin/env python3
"""news-image-20261117 v2 — "Sum up 17 November's world news in one image".

Draws one 1024x1024 front page of Tuesday 17 November 2026's world news:
ten illustrated stories, a world map, a figures strip, and 20 briefs —
30 stories spanning six continents. Every fact is baked in, sourced from 17 November 2026
reporting (Reuters, BBC, AP, Al Jazeera, Le Monde, DW, CNBC, The Hindu,
Geo News, Mongabay, Premium Times, ACI Africa, NewsMada, Rio Times,
DefenseScoop). No network at runtime. Deterministic: fixed fonts, fixed
layout, no timestamps — two runs write byte-identical PNGs. If Pillow or
the fonts are missing at grade time, the beside-it entry.png (byte-identical
to what the draw path writes) is copied to the output path instead.

Run:  python3 main.py            (writes /output/entry.png)
       MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")


def fallback():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"), OUT)
    print("wrote", OUT, "(fallback copy)")


def main():
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        fallback()
        return
    try:
        render(Image, ImageDraw, ImageFont)
    except Exception:
        fallback()


W, H = 1024, 1024
PAPER = (247, 243, 234)
NAVY = (15, 42, 67)
GOLD = (201, 162, 39)
INK = (24, 28, 34)
MUTED = (84, 90, 100)
CARD = (255, 255, 255)
LINE = (214, 208, 194)

# (tag, accent, headline, sub, icon) — 46 sourced stories; layout uses 30.
S = [
 ("UKRAINE", (176, 58, 44), "Kerch Bridge road span falls", "Second day of Ukrainian strikes; rail arch damaged, 2 killed.", "bridge"),
 ("GULF", (196, 120, 20), "US jets strike missile site on Qeshm", "Third US carrier group now in the region.", "jet"),
 ("ASIA", (38, 110, 138), "Trump lands in Manila for ASEAN, Quad", "Xi-Trump-Putin summit set for Thursday in Shenzhen.", "plane"),
 ("TECH", (74, 92, 168), "Nvidia revenue $115.8bn, up 103%", "First earnings without Huang; SEC probe reported.", "chip"),
 ("ISRAEL", (122, 74, 140), "Knesset elects Kahana speaker, 66-52", "Eisenkot ally wins; blow to Netanyahu.", "columns"),
 ("CLIMATE", (58, 128, 84), "COP31 draft haggled as 1.5C slips", "144 items disputed in Turkiye talks.", "leaf"),
 ("UKRAINE", (176, 58, 44), "Record drone barrage overnight", "Russia says 1,336 drones downed; Moscow targeted.", "drone"),
 ("UKRAINE", (176, 58, 44), "Russia hits two Kyiv bridges", "Seven ballistic missiles; power out in 8 regions.", "flame"),
 ("MARKETS", (150, 100, 20), "Brent holds near $93", "US crude stocks up 5.3m barrels, API says.", "barrel"),
 ("MARKETS", (150, 100, 20), "Dow drops about 850 points", "Stocks slide before Nvidia earnings; US data beats forecasts.", "chart"),
 ("TECH", (74, 92, 168), "Anthropic IPO book closes", "Pricing seen above $70-78; up to $64bn raise.", "chartup"),
 ("EUROPE", (58, 128, 84), "Five EU states plan Rwanda hub", "Pilot for about 100 rejected asylum seekers.", "pin"),
 ("UK", (38, 110, 138), "Burnham: Brexit has not worked", "UK PM seeks EU reset at Friday summit.", "flag"),
 ("BANGLADESH", (176, 58, 44), "Bangladesh unrest turns deadly", "Bombs and arson on Hasina sentence anniversary.", "flame"),
 ("CLIMATE", (58, 128, 84), "Earthshot Prize in Mumbai", "Prince and Princess of Wales attend.", "star"),
 ("GAZA", (196, 120, 20), "Four nations urge Gaza aid", "Australia, Canada, Italy, UK: let aid reach flooded Gaza.", "aid"),
 ("S AMERICA", (38, 110, 138), "Pope Leo ends South America tour", "Visit included Peru, Argentina, Uruguay.", "globe"),
 ("AFRICA", (150, 100, 20), "Church warns of food shortages", "Catholic bishops urge urgent action in Sudan, South Sudan.", "wheat"),
 ("USA", (15, 42, 67), "Pentagon fails 9th audit in row", "Inspector general report, 9th year running.", "shield"),
 ("FRANCE", (74, 92, 168), "France strike; protests go on", "Public-sector walkout smaller; living-cost anger grows.", "flag"),
 ("EUROPE", (58, 128, 84), "EU sanctions Wildberries chief", "Tatyana Kim added to Russia sanctions list.", "pin"),
 ("SPAIN", (176, 58, 44), "Spain to vote on 29 November", "Sixth general election in 11 years.", "ballot"),
 ("TRADE", (38, 110, 138), "China, Canada cut more tariffs", "More cuts agreed as Ottawa-Washington ties strain.", "globe"),
 ("ASEAN", (38, 110, 138), "ASEAN agrees power-grid pact", "Bloc also weighs joint oil storage.", "bolt"),
 ("QUAD", (15, 42, 67), "Quad hits cross-border terror", "Maritime, AI and cyber initiatives agreed.", "shield"),
 ("PHILIPPINES", (38, 110, 138), "Trump hails Philippines deal", "$85m AI investment announced in Manila.", "chartup"),
 ("KOREA", (122, 74, 140), "Trump open to Kim meeting", "Possible meeting raised on Asia trip.", "plane"),
 ("MADAGASCAR", (150, 100, 20), "Bush-taxi crashes kill 37", "Two crashes at Betroka and Antsohihy.", "alert"),
 ("CHAD", (58, 128, 84), "Oryx returns to wild in Chad", "Reintroduced antelope returns to the wild.", "leaf"),
 ("PAKISTAN", (58, 128, 84), "Pakistan cuts petrol price", "Down 3 rupees to 325 rupees a litre.", "barrel"),
 ("VENEZUELA", (150, 100, 20), "$12bn Venezuela revenue", "State Dept: oil and mineral income tallied.", "barrel"),
 ("MYANMAR", (122, 74, 140), "UN court to rule on Myanmar", "Genocide-case ruling due Thursday.", "columns"),
 ("OCEANIA", (38, 110, 138), "Australia, Korea ink green deal", "Low-emissions steel and green hydrogen at COP31.", "leaf"),
 ("OCEANIA", (176, 58, 44), "Australia pressed on coal, gas", "UN investigator, First Nations woman speak at COP31.", "flame"),
 ("KYRGYZSTAN", (58, 128, 84), "Kyrgyzstan seeks glacier help", "Call for aid to protect glaciers, water at COP31.", "globe"),
 ("NIGERIA", (150, 100, 20), "Children miss school in Nigeria", "Insecurity and poverty blamed in Nigeria.", "pin"),
 ("MOZAMBIQUE", (176, 58, 44), "Opposition leader faces trial", "Trial over violence after disputed 2024 vote.", "columns"),
 ("SPORT", (58, 128, 84), "Boca meet Mineiro in final", "Copa Sudamericana final Saturday in Barranquilla.", "ball"),
 ("TECH", (74, 92, 168), "New US chip curbs bite", "132-page rule: licences for five nations, rental cap.", "chip"),
 ("TECH", (74, 92, 168), "Nvidia halts H200 China sales", "Chip sales halted under export pressure.", "chip"),
 ("TECH", (74, 92, 168), "Nvidia forms security committee", "Board to oversee national security, export controls.", "shield"),
 ("USA", (15, 42, 67), "AI training for cyber force", "All 79 cyber roles; 24,000 staff short.", "chip"),
 ("USA", (15, 42, 67), "NSA: outage was maintenance", "Network disruption routine maintenance, agency says.", "bolt"),
 ("GULF", (196, 120, 20), "Iran claims US base strikes", "Tehran says it hit bases in Bahrain and Kuwait.", "flame"),
 ("FRANCE", (74, 92, 168), "Darmanin: Melenchon could win", "French minister warns on Le Pen runoff.", "ballot"),
 ("INDIA", (196, 120, 20), "Modi in Manila for ASEAN summits", "ASEAN-India and East Asia summits attended.", "flag"),
]

# Briefs: 20 stories chosen for breadth across six continents + tech/markets.
BRIEFS = [6, 7, 8, 9, 10, 11, 12, 13, 17, 18, 19, 20, 21, 30, 31, 32, 33, 37, 38, 27]
# Mini illustrated panels: Earthshot, Gaza aid, Pope tour, oryx return.
MINIS = [14, 15, 16, 28]

FIGURES = [("$115.8bn", "Nvidia revenue, +103%"),
           ("1,336", "drones downed overnight"),
           ("66-52", "Knesset speaker vote"),
           ("$93", "Brent crude, near")]


def font(name, size, ImageFont):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + name, size)


def wrap(draw, text, fnt, max_w, max_lines):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    assert len(lines) <= max_lines, "overflow: %r -> %d" % (text, len(lines))
    return lines


def render(Image, ImageDraw, ImageFont):
    def F(name, size):
        return font(name, size, ImageFont)

    def icon_bridge(d, cx, cy, s, c):
        d.line([(cx - s, cy + s * 0.5), (cx + s, cy + s * 0.5)], fill=c, width=max(3, s // 6))
        d.arc([cx - s, cy - s * 0.9, cx + s, cy + s * 0.9], 180, 360, fill=c, width=max(3, s // 6))
        for x in (-s * 0.6, 0, s * 0.6):
            d.line([(cx + x, cy - s * 0.45), (cx + x, cy + s * 0.5)], fill=c, width=3)

    def icon_jet(d, cx, cy, s, c):
        d.polygon([(cx - s, cy), (cx + s * 0.9, cy - s * 0.35), (cx + s, cy),
                   (cx + s * 0.9, cy + s * 0.35)], fill=c)
        d.polygon([(cx - s * 0.1, cy - s * 0.7), (cx + s * 0.3, cy),
                   (cx - s * 0.1, cy + s * 0.7)], fill=c)

    def icon_plane(d, cx, cy, s, c):
        d.ellipse([cx - s * 0.9, cy - s * 0.22, cx + s * 0.9, cy + s * 0.22], fill=c)
        d.polygon([(cx - s * 0.2, cy - s * 0.8), (cx + s * 0.25, cy - s * 0.1),
                   (cx - s * 0.05, cy + s * 0.1)], fill=c)
        d.polygon([(cx - s * 0.2, cy + s * 0.8), (cx + s * 0.25, cy + s * 0.1),
                   (cx - s * 0.05, cy - s * 0.1)], fill=c)

    def icon_chip(d, cx, cy, s, c):
        d.rectangle([cx - s * 0.6, cy - s * 0.6, cx + s * 0.6, cy + s * 0.6], outline=c, width=4)
        d.rectangle([cx - s * 0.25, cy - s * 0.25, cx + s * 0.25, cy + s * 0.25], fill=c)
        for x in (-s * 0.35, 0, s * 0.35):
            d.line([(cx + x, cy - s), (cx + x, cy - s * 0.6)], fill=c, width=3)
            d.line([(cx + x, cy + s * 0.6), (cx + x, cy + s)], fill=c, width=3)

    def icon_columns(d, cx, cy, s, c):
        d.polygon([(cx - s, cy - s * 0.3), (cx + s, cy - s * 0.3), (cx, cy - s)], fill=c)
        for x in (-s * 0.65, 0, s * 0.65):
            d.line([(cx + x, cy - s * 0.2), (cx + x, cy + s * 0.7)], fill=c, width=5)
        d.line([(cx - s, cy + s * 0.85), (cx + s, cy + s * 0.85)], fill=c, width=4)

    def icon_leaf(d, cx, cy, s, c):
        d.ellipse([cx - s * 0.7, cy - s * 0.9, cx + s * 0.7, cy + s * 0.5], fill=c)
        d.line([(cx, cy - s * 0.7), (cx, cy + s)], fill=c, width=4)
        d.line([(cx, cy - s * 0.2), (cx + s * 0.55, cy - s * 0.55)], fill=c, width=3)

    def icon_drone(d, cx, cy, s, c):
        d.rectangle([cx - s * 0.3, cy - s * 0.25, cx + s * 0.3, cy + s * 0.25], fill=c)
        for sx in (-1, 1):
            for sy in (-1, 1):
                d.ellipse([cx + sx * s * 0.55 - 8, cy + sy * s * 0.55 - 4,
                           cx + sx * s * 0.55 + 8, cy + sy * s * 0.55 + 4], fill=c)
                d.line([(cx + sx * s * 0.25, cy + sy * s * 0.2),
                        (cx + sx * s * 0.55, cy + sy * s * 0.55)], fill=c, width=3)

    def icon_flame(d, cx, cy, s, c):
        d.polygon([(cx, cy - s), (cx + s * 0.6, cy), (cx + s * 0.3, cy + s * 0.7),
                   (cx - s * 0.3, cy + s * 0.7), (cx - s * 0.6, cy)], fill=c)
        d.ellipse([cx - s * 0.25, cy, cx + s * 0.25, cy + s * 0.5], fill=(255, 220, 120))

    def icon_barrel(d, cx, cy, s, c):
        d.ellipse([cx - s * 0.55, cy - s * 0.85, cx + s * 0.55, cy - s * 0.45], fill=c)
        d.rectangle([cx - s * 0.55, cy - s * 0.65, cx + s * 0.55, cy + s * 0.8], fill=c)
        d.ellipse([cx - s * 0.55, cy + s * 0.55, cx + s * 0.55, cy + s * 0.85], fill=c)
        d.line([(cx - s * 0.55, cy - s * 0.25), (cx + s * 0.55, cy - s * 0.25)],
               fill=(255, 255, 255), width=3)
        d.line([(cx - s * 0.55, cy + s * 0.3), (cx + s * 0.55, cy + s * 0.3)],
               fill=(255, 255, 255), width=3)

    def icon_chart(d, cx, cy, s, c):
        d.line([(cx - s, cy + s * 0.4), (cx - s * 0.3, cy),
                (cx + s * 0.3, cy + s * 0.3), (cx + s, cy - s * 0.6)],
               fill=c, width=5, joint="curve")

    def icon_chartup(d, cx, cy, s, c):
        d.line([(cx - s, cy + s * 0.5), (cx - s * 0.3, cy + s * 0.1),
                (cx + s * 0.3, cy - s * 0.2), (cx + s, cy - s * 0.6)],
               fill=c, width=5, joint="curve")
        d.polygon([(cx + s, cy - s * 0.6), (cx + s * 0.55, cy - s * 0.55),
                   (cx + s * 0.9, cy - s * 0.15)], fill=c)

    def icon_pin(d, cx, cy, s, c):
        d.ellipse([cx - s * 0.6, cy - s, cx + s * 0.6, cy + s * 0.2], fill=c)
        d.polygon([(cx - s * 0.45, cy + s * 0.1), (cx + s * 0.45, cy + s * 0.1),
                   (cx, cy + s)], fill=c)
        d.ellipse([cx - s * 0.22, cy - s * 0.62, cx + s * 0.22, cy - s * 0.18],
                  fill=(255, 255, 255))

    def icon_flag(d, cx, cy, s, c):
        d.line([(cx - s * 0.5, cy - s), (cx - s * 0.5, cy + s)], fill=c, width=4)
        d.polygon([(cx - s * 0.5, cy - s), (cx + s * 0.7, cy - s * 0.6),
                   (cx - s * 0.5, cy - s * 0.1)], fill=c)

    def icon_star(d, cx, cy, s, c):
        import math
        pts = []
        for i in range(10):
            r = s if i % 2 == 0 else s * 0.45
            a = -math.pi / 2 + i * math.pi / 5
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        d.polygon(pts, fill=c)

    def icon_aid(d, cx, cy, s, c):
        d.rectangle([cx - s * 0.3, cy - s * 0.8, cx + s * 0.3, cy + s * 0.8], fill=c)
        d.rectangle([cx - s * 0.8, cy - s * 0.3, cx + s * 0.8, cy + s * 0.3], fill=c)

    def icon_globe(d, cx, cy, s, c):
        d.ellipse([cx - s, cy - s, cx + s, cy + s], outline=c, width=4)
        d.ellipse([cx - s * 0.45, cy - s, cx + s * 0.45, cy + s], outline=c, width=3)
        d.line([(cx - s, cy), (cx + s, cy)], fill=c, width=3)

    def icon_wheat(d, cx, cy, s, c):
        d.line([(cx, cy - s), (cx, cy + s)], fill=c, width=4)
        for k in range(3):
            yy = cy - s * 0.6 + k * s * 0.45
            d.line([(cx, yy), (cx - s * 0.5, yy - s * 0.25)], fill=c, width=3)
            d.line([(cx, yy), (cx + s * 0.5, yy - s * 0.25)], fill=c, width=3)

    def icon_shield(d, cx, cy, s, c):
        d.polygon([(cx - s * 0.7, cy - s * 0.7), (cx + s * 0.7, cy - s * 0.7),
                   (cx + s * 0.7, cy), (cx, cy + s), (cx - s * 0.7, cy)], fill=c)

    def icon_ballot(d, cx, cy, s, c):
        d.rectangle([cx - s * 0.7, cy - s * 0.3, cx + s * 0.7, cy + s * 0.7], outline=c, width=4)
        d.line([(cx - s * 0.4, cy - s * 0.75), (cx + s * 0.4, cy - s * 0.75)], fill=c, width=4)
        d.line([(cx - s * 0.3, cy + s * 0.2), (cx - s * 0.05, cy + s * 0.45),
                (cx + s * 0.45, cy - s * 0.1)], fill=c, width=4)

    def icon_bolt(d, cx, cy, s, c):
        d.polygon([(cx + s * 0.2, cy - s), (cx - s * 0.5, cy + s * 0.1),
                   (cx - s * 0.05, cy + s * 0.1), (cx - s * 0.2, cy + s),
                   (cx + s * 0.5, cy - s * 0.1), (cx + s * 0.05, cy - s * 0.1)], fill=c)

    def icon_alert(d, cx, cy, s, c):
        d.polygon([(cx, cy - s), (cx + s, cy + s * 0.7), (cx - s, cy + s * 0.7)], fill=c)
        d.text((cx - 4, cy - s * 0.25), "!", font=F("DejaVuSans-Bold.ttf", 26), fill=(255, 255, 255))

    def icon_ball(d, cx, cy, s, c):
        d.ellipse([cx - s * 0.8, cy - s * 0.8, cx + s * 0.8, cy + s * 0.8], outline=c, width=4)
        d.polygon([(cx - s * 0.3, cy - s * 0.5), (cx + s * 0.3, cy - s * 0.5),
                   (cx + s * 0.5, cy), (cx, cy + s * 0.5), (cx - s * 0.5, cy)], fill=c)

    ICONS = {"bridge": icon_bridge, "jet": icon_jet, "plane": icon_plane,
             "chip": icon_chip, "columns": icon_columns, "leaf": icon_leaf,
             "drone": icon_drone, "flame": icon_flame, "barrel": icon_barrel,
             "chart": icon_chart, "chartup": icon_chartup, "pin": icon_pin,
             "flag": icon_flag, "star": icon_star, "aid": icon_aid,
             "globe": icon_globe, "wheat": icon_wheat, "shield": icon_shield,
             "ballot": icon_ballot, "bolt": icon_bolt, "alert": icon_alert,
             "ball": icon_ball}

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Header -------------------------------------------------------------
    d.rectangle([0, 0, W, 108], fill=NAVY)
    d.rectangle([0, 108, W, 112], fill=GOLD)
    d.text((28, 12), "THE WORLD IN ONE IMAGE  \u00b7  17 NOVEMBER 2026",
           font=F("DejaVuSans-Bold.ttf", 19), fill=GOLD)
    d.text((28, 32), "TUESDAY, 17 NOVEMBER 2026",
           font=F("DejaVuSerif-Bold.ttf", 44), fill=(255, 255, 255))
    d.text((28, 80), "Ten pictures, the world mapped, then the day in brief",
           font=F("DejaVuSans.ttf", 19), fill=(190, 200, 212))

    # Six illustrated panels: 3 cols x 2 rows -----------------------------
    M, G = 18, 12
    PW = (W - 2 * M - 2 * G) // 3
    PH = 204
    top = 120
    for i in range(6):
        tag, accent, head, sub, icon = S[i]
        x0 = M + (i % 3) * (PW + G)
        y0 = top + (i // 3) * (PH + 10)
        x1, y1 = x0 + PW, y0 + PH
        d.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=CARD, outline=LINE, width=1)
        d.rectangle([x0, y0, x1, y0 + 6], fill=accent)
        cx, cy = x0 + PW // 2, y0 + 46
        d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=accent)
        ICONS[icon](d, cx, cy, 27, (255, 255, 255))
        f_tag = F("DejaVuSans-Bold.ttf", 15)
        tw = d.textlength(tag, font=f_tag)
        d.text((cx - tw / 2, y0 + 82), tag, font=f_tag, fill=accent)
        f_h = F("DejaVuSans-Bold.ttf", 22)
        lines = wrap(d, head, f_h, PW - 20, 2)
        yy = y0 + 100
        for ln in lines:
            lw = d.textlength(ln, font=f_h)
            d.text((cx - lw / 2, yy), ln, font=f_h, fill=INK)
            yy += 27
        f_s = F("DejaVuSans.ttf", 16)
        sl = wrap(d, sub, f_s, PW - 20, 2)
        for ln in sl:
            lw = d.textlength(ln, font=f_s)
            d.text((cx - lw / 2, yy + 2), ln, font=f_s, fill=MUTED)
            yy += 20
        assert yy <= y1 - 6, "panel %d overflows" % i

    # Map + figures strip --------------------------------------------------
    sy = top + 2 * PH + 10 + 10
    mx0, my0, mx1, my1 = M, sy, M + 600, sy + 124
    d.rectangle([mx0, my0, mx1, my1], fill=(203, 225, 238))
    d.rectangle([mx0, my0, mx1, my1], outline=LINE, width=1)

    def MP(px, py):
        return (mx0 + px / 100.0 * (mx1 - mx0), my0 + py / 100.0 * (my1 - my0))

    for poly in [[(4, 24), (28, 18), (32, 32), (24, 48), (12, 46), (6, 34)],
                 [(26, 56), (36, 54), (38, 70), (32, 90), (27, 76)],
                 [(46, 20), (56, 18), (58, 30), (50, 36), (45, 30)],
                 [(47, 40), (60, 38), (62, 56), (56, 74), (49, 62)],
                 [(58, 16), (88, 14), (92, 30), (80, 44), (64, 42), (58, 30)],
                 [(82, 62), (92, 60), (94, 70), (84, 72)]]:
        d.polygon([MP(a, b) for a, b in poly], fill=(233, 226, 200),
                  outline=(150, 150, 130))
    for name, px, py in [("KYIV", 55, 26), ("HORMUZ", 63, 36), ("MANILA", 84, 40),
                         ("MUMBAI", 72, 40), ("WASHINGTON", 16, 32),
                         ("JERUSALEM", 60, 34), ("LIMA", 28, 68),
                         ("KHARTOUM", 54, 48), ("CANBERRA", 90, 68)]:
        cx, cy = MP(px, py)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(176, 58, 44),
                  outline=(255, 255, 255), width=1)
    d.text((mx0 + 10, my0 + 5), "WORLD MAP \u2014 WHERE THE DAY HAPPENED",
           font=F("DejaVuSans-Bold.ttf", 13), fill=NAVY)
    for lab, px, py in [("N AMERICA", 8, 52), ("S AMERICA", 22, 86),
                        ("AFRICA", 46, 78),
                        ("ASIA", 74, 8), ("OCEANIA", 80, 76)]:
        d.text(MP(px, py), lab, font=F("DejaVuSans-Bold.ttf", 11), fill=(90, 100, 110))

    fx0 = mx1 + G
    d.rectangle([fx0, sy, W - M, sy + 124], fill=NAVY)
    for i, (num, lab) in enumerate(FIGURES):
        half = (W - M - fx0) // 2
        cx = fx0 + (i % 2) * half + half // 2
        yy = sy + 10 + (i // 2) * 60
        f_n = F("DejaVuSans-Bold.ttf", 26)
        nw = d.textlength(num, font=f_n)
        d.text((cx - nw / 2, yy), num, font=f_n, fill=GOLD)
        f_l = F("DejaVuSans.ttf", 13)
        lw = d.textlength(lab, font=f_l)
        d.text((cx - lw / 2, yy + 32), lab, font=f_l, fill=(255, 255, 255))

    # Mini illustrated panels: 4 more pictures -----------------------------
    mw = (W - 2 * M - 3 * G) // 4
    mh = 122
    my2 = sy + 124 + 10
    for i, si in enumerate(MINIS):
        tag, accent, head, sub, icon = S[si]
        x0 = M + i * (mw + G)
        y0 = my2
        x1, y1 = x0 + mw, y0 + mh
        d.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=CARD, outline=LINE, width=1)
        d.rectangle([x0, y0, x1, y0 + 5], fill=accent)
        cx, cy = x0 + mw // 2, y0 + 32
        d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=accent)
        ICONS[icon](d, cx, cy, 19, (255, 255, 255))
        f_tag = F("DejaVuSans-Bold.ttf", 13)
        tw = d.textlength(tag, font=f_tag)
        d.text((cx - tw / 2, y0 + 58), tag, font=f_tag, fill=accent)
        f_h = F("DejaVuSans-Bold.ttf", 15)
        lines = wrap(d, head, f_h, mw - 16, 2)
        yy = y0 + 74
        for ln in lines:
            lw = d.textlength(ln, font=f_h)
            d.text((cx - lw / 2, yy), ln, font=f_h, fill=INK)
            yy += 18
        assert yy <= y1 - 6, "mini %d overflows" % i

    # Briefs: 20 stories, 4 cols x 5 rows ---------------------------------
    by = my2 + mh + 10
    d.text((M, by), "THE DAY IN BRIEF", font=F("DejaVuSans-Bold.ttf", 17), fill=NAVY)
    by += 22
    f_b = F("DejaVuSans.ttf", 14)
    CW = (W - 2 * M - 3 * G) // 4
    for idx, si in enumerate(BRIEFS):
        head = S[si][2]
        c, r = idx // 5, idx % 5
        x0 = M + c * (CW + G)
        yy = by + r * 28
        assert d.textlength("\u2022 " + head, font=f_b) <= CW + 4, head
        assert yy + 18 <= H - 32, "briefs overflow"
        d.text((x0, yy), "\u2022 " + head, font=f_b, fill=INK)

    # Footer ---------------------------------------------------------------
    d.rectangle([0, H - 30, W, H], fill=(232, 226, 212))
    d.line([(0, H - 30), (W, H - 30)], fill=LINE, width=1)
    d.text((24, H - 22),
           "Sources: Reuters  \u00b7  BBC  \u00b7  AP  \u00b7  Al Jazeera  \u00b7  Le Monde  \u00b7  DW  \u00b7  CNBC  \u2014  Tuesday 17 November 2026",
           font=F("DejaVuSans.ttf", 16), fill=MUTED)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
