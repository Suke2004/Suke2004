#!/usr/bin/env python3
"""Generate retro arcade SVG assets for the Suke2004 profile README.
Every letter is drawn as pixel rects from a 5x7 bitmap font -> no font
dependencies, renders identically everywhere (GitHub camo included).
"""
import os, random, xml.etree.ElementTree as ET

random.seed(42)
OUT = "assets"
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- 5x7 font
F = {
'A':["01110","10001","10001","11111","10001","10001","10001"],
'B':["11110","10001","10001","11110","10001","10001","11110"],
'C':["01110","10001","10000","10000","10000","10001","01110"],
'D':["11110","10001","10001","10001","10001","10001","11110"],
'E':["11111","10000","10000","11110","10000","10000","11111"],
'F':["11111","10000","10000","11110","10000","10000","10000"],
'G':["01110","10001","10000","10111","10001","10001","01110"],
'H':["10001","10001","10001","11111","10001","10001","10001"],
'I':["11111","00100","00100","00100","00100","00100","11111"],
'J':["00111","00010","00010","00010","00010","10010","01100"],
'K':["10001","10010","10100","11000","10100","10010","10001"],
'L':["10000","10000","10000","10000","10000","10000","11111"],
'M':["10001","11011","10101","10101","10001","10001","10001"],
'N':["10001","11001","10101","10011","10001","10001","10001"],
'O':["01110","10001","10001","10001","10001","10001","01110"],
'P':["11110","10001","10001","11110","10000","10000","10000"],
'Q':["01110","10001","10001","10001","10101","10010","01101"],
'R':["11110","10001","10001","11110","10100","10010","10001"],
'S':["01111","10000","10000","01110","00001","00001","11110"],
'T':["11111","00100","00100","00100","00100","00100","00100"],
'U':["10001","10001","10001","10001","10001","10001","01110"],
'V':["10001","10001","10001","10001","10001","01010","00100"],
'W':["10001","10001","10001","10101","10101","11011","10001"],
'X':["10001","10001","01010","00100","01010","10001","10001"],
'Y':["10001","10001","01010","00100","00100","00100","00100"],
'Z':["11111","00001","00010","00100","01000","10000","11111"],
'0':["01110","10001","10011","10101","11001","10001","01110"],
'1':["00100","01100","00100","00100","00100","00100","11111"],
'2':["01110","10001","00001","00010","00100","01000","11111"],
'3':["11111","00001","00010","00110","00001","10001","01110"],
'4':["00010","00110","01010","10010","11111","00010","00010"],
'5':["11111","10000","11110","00001","00001","10001","01110"],
'6':["00110","01000","10000","11110","10001","10001","01110"],
'7':["11111","00001","00010","00100","01000","01000","01000"],
'8':["01110","10001","10001","01110","10001","10001","01110"],
'9':["01110","10001","10001","01111","00001","00010","01100"],
'-':["00000","00000","00000","11111","00000","00000","00000"],
':':["00000","00100","00000","00000","00100","00000","00000"],
'.':["00000","00000","00000","00000","00000","00000","00100"],
',':["00000","00000","00000","00000","00000","00100","01000"],
'!':["00100","00100","00100","00100","00100","00000","00100"],
'?':["01110","10001","00001","00010","00100","00000","00100"],
'>':["10000","01000","00100","00010","00100","01000","10000"],
'<':["00001","00010","00100","01000","00100","00010","00001"],
'*':["00000","10101","01110","11111","01110","10101","00000"],
'/':["00001","00001","00010","00100","01000","10000","10000"],
'(':["00010","00100","01000","01000","01000","00100","00010"],
')':["01000","00100","00010","00010","00010","00100","01000"],
'+':["00000","00100","00100","11111","00100","00100","00000"],
"'":["00100","00100","00000","00000","00000","00000","00000"],
'_':["00000","00000","00000","00000","00000","00000","11111"],
'&':["01100","10010","10100","01000","10101","10010","01101"],
'%':["11001","11010","00010","00100","01000","01011","10011"],
'@':["01110","10001","10111","10101","10111","10000","01110"],
'[':["01110","01000","01000","01000","01000","01000","01110"],
']':["01110","00010","00010","00010","00010","00010","01110"],
'=':["00000","00000","11111","00000","11111","00000","00000"],
}

GREEN="#00ff41"; DIMGREEN="#00902a"; YELLOW="#ffe600"; CYAN="#00e5ff"
RED="#ff3355"; WHITE="#ffffff"; GRAY="#8b949e"; BLACK="#000000"
ORANGE="#ffb000"; PINK="#ff7ad9"

def text(x, y, s, txt, color, cls=None, anchor="start"):
    """Render txt as pixel rects. Returns (svg_string, width_px)."""
    w = (len(txt)*6 - 1) * s
    if anchor == "middle": x -= w/2
    elif anchor == "end":  x -= w
    parts = []
    cx = x
    for ch in txt.upper():
        if ch != ' ':
            rows = F.get(ch, F['?'])
            for r, row in enumerate(rows):
                c = 0
                while c < 5:
                    if row[c] == '1':
                        run = 1
                        while c+run < 5 and row[c+run] == '1': run += 1
                        parts.append(f'<rect x="{cx+c*s:g}" y="{y+r*s:g}" width="{run*s:g}" height="{s:g}" fill="{color}"/>')
                        c += run
                    else:
                        c += 1
        cx += 6*s
    attr = f' class="{cls}"' if cls else ''
    return f'<g{attr}>' + ''.join(parts) + '</g>', w

def scan(w, h):
    return (f'<g opacity="0.18">' +
            ''.join(f'<rect x="0" y="{y}" width="{w}" height="1.5" fill="#000000" opacity="0.9"/>' for y in range(0, h, 4)) +
            '</g>')

def bezel(w, h, color=GREEN):
    return (f'<rect x="3" y="3" width="{w-6}" height="{h-6}" fill="none" stroke="{color}" stroke-width="2"/>'
            f'<rect x="9" y="9" width="{w-18}" height="{h-18}" fill="none" stroke="{color}" stroke-width="1" opacity="0.35"/>')

def svg(w, h, body, style=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<style>{style}</style>'
            f'<rect width="{w}" height="{h}" fill="{BLACK}"/>' + body + scan(w, h) + '</svg>')

BLINK = ".blink{animation:bl 1.1s steps(2,jump-none) infinite}@keyframes bl{0%,49%{opacity:1}50%,100%{opacity:0}}"
TWINK = ".tw{animation:tw 2.4s ease-in-out infinite}@keyframes tw{0%,100%{opacity:.12}50%{opacity:1}}"

def sprite(bitmap, palette, ox, oy, s):
    out=[]
    for r,row in enumerate(bitmap):
        c=0
        while c < len(row):
            ch=row[c]
            if ch!='.':
                run=1
                while c+run<len(row) and row[c+run]==ch: run+=1
                out.append(f'<rect x="{ox+c*s:g}" y="{oy+r*s:g}" width="{run*s:g}" height="{s:g}" fill="{palette[ch]}"/>')
                c+=run
            else: c+=1
    return ''.join(out)

GHOST=[
"....RRRRRR....",
"..RRRRRRRRRR..",
".RRRRRRRRRRRR.",
".RRWWRRRRWWRR.",
"RRWWWWRRWWWWRR",
"RRWBBWRRWBBWRR",
"RRWWWWRRWWWWRR",
"RRRRRRRRRRRRRR",
"RRRRRRRRRRRRRR",
"RRRRRRRRRRRRRR",
"RRRRRRRRRRRRRR",
"RRRRRRRRRRRRRR",
"RR.RRR..RRR.RR",
"R...RR..RR...R",
]

PLAYER_SPRITE=[
"....HHHHHHHH....",
"...HHHHHHHHHH...",
"...HHSSSSSSHH...",
"...HSSSSSSSSH...",
"...HSKSSSSKSH...",
"...HSSSSSSSSH...",
"...HSSSKKSSSH...",
"....SSSSSSSS....",
".....SSSSSS.....",
"...GGGGGGGGGG...",
"..GGGGGGGGGGGG..",
".SSGGGGGGGGGGSS.",
".SSGGGGGGGGGGSS.",
"..LLLLLLLLLLLL..",
"..LLLLLLLLLLLL..",
"..KKKKKKKKKKKK..",
]
PLAYER_PAL={'H':'#3a2b1e','S':'#e6b98f','K':'#101418','G':GREEN,'L':'#9aa0a6','W':WHITE}

def pac(cx, cy, r, color=YELLOW, cls=None):
    attr=f' class="{cls}"' if cls else ''
    return (f'<g{attr}><path d="M {cx} {cy} L {cx+r*0.94} {cy-r*0.44} A {r} {r} 0 1 0 {cx+r*0.94} {cy+r*0.44} Z" fill="{color}"/></g>')

# ============================================================ 1. TITLE
def make_title():
    W,H=900,300
    b=[bezel(W,H)]
    for _ in range(55):
        x=random.randint(18,W-18); y=random.randint(18,H-18); sz=random.choice([2,2,3])
        d=random.uniform(0,2.4)
        b.append(f'<rect x="{x}" y="{y}" width="{sz}" height="{sz}" fill="{WHITE}" class="tw" style="animation-delay:-{d:.2f}s"/>')
    t,_=text(W/2,28,2,"* * *  ARCADE PROFILE  * * *",YELLOW,anchor="middle"); b.append(t)
    t,tw=text(W/2,58,9,"SUKE2004",GREEN,anchor="middle"); b.append(t)
    b.append(sprite(GHOST,{'R':RED,'W':WHITE,'B':'#2233ff'},W/2-tw/2-110,52,5))
    b.append(sprite(GHOST,{'R':CYAN,'W':WHITE,'B':'#2233ff'},W/2+tw/2+40,52,5))
    t,_=text(W/2,146,3,"USTELA SUKESH REDDY",WHITE,anchor="middle"); b.append(t)
    t,_=text(W/2,182,2.6,"BACKEND DEV (GO) * SELF-HOSTING * DATA SCIENCE",CYAN,anchor="middle"); b.append(t)
    t,_=text(W/2,222,3,"PRESS START",WHITE,cls="blink",anchor="middle"); b.append(t)
    t,_=text(W/2,262,2,"(C) 2026 SUKE2004 - INSERT COIN TO CONNECT",GRAY,anchor="middle"); b.append(t)
    dots=''.join(f'<rect x="{x}" y="{H-22}" width="4" height="4" fill="{YELLOW}"/>' for x in range(30,W-40,24))
    b.append(dots)
    b.append(pac(24,H-20,9,YELLOW,cls="pm"))
    style=BLINK+TWINK+f".pm{{animation:mv 9s linear infinite}}@keyframes mv{{from{{transform:translateX(0)}}to{{transform:translateX({W-60}px)}}}}"
    open(f"{OUT}/title.svg","w").write(svg(W,H,''.join(b),style))

# ============================================================ 2. HEADERS
def make_header(fname, label, color=GREEN):
    W,H=900,64
    b=[f'<rect x="3" y="3" width="{W-6}" height="{H-6}" fill="none" stroke="{color}" stroke-width="2"/>']
    b.append(pac(34,H/2,12))
    t,tw=text(62,18,4,label,color); b.append(t)
    x0=int(62+tw+24)
    b.append(''.join(f'<rect x="{x}" y="{H/2-2}" width="4" height="4" fill="{YELLOW}"/>' for x in range(x0,W-24,20)))
    open(f"{OUT}/{fname}","w").write(svg(W,H,''.join(b)))

# ============================================================ 3. PLAYER CARD
def make_player():
    W,H=900,340
    b=[bezel(W,H)]
    t,_=text(30,24,2.5,"1P  START",YELLOW); b.append(t)
    t,_=text(W-30,24,2.5,"HI-SCORE 999999",GRAY,anchor="end"); b.append(t)
    # avatar box
    b.append(f'<rect x="30" y="56" width="190" height="226" fill="none" stroke="{DIMGREEN}" stroke-width="2"/>')
    b.append(sprite(PLAYER_SPRITE,PLAYER_PAL,30+31,70,8))
    t,_=text(125,212,2.4,"SUKE2004",GREEN,anchor="middle"); b.append(t)
    t,_=text(125,244,2,"LV.21 HUMAN",WHITE,anchor="middle"); b.append(t)
    lines=[
        ("PLAYER  : USTELA SUKESH REDDY",WHITE),
        ("CLASS   : BACKEND DEVELOPER (GO)",GREEN),
        ("SUBCLASS: DATA SCIENCE STUDENT",CYAN),
        ("GUILD   : SUPERPLUGS (OPEN SOURCE)",PINK),
        ("ALIGN   : LAWFUL OPEN-SOURCE",YELLOW),
        ("BASE    : LINUX TERMINAL",GRAY),
        ("SPECIAL : DATA TO INSIGHTS,",WHITE),
        ("          COFFEE TO CODE.",WHITE),
        ("GRIND   : ADVANCED ML + SYSTEM DESIGN",ORANGE),
        ("CO-OP   : GO + PYTHON OSS LIBRARIES",GREEN),
    ]
    y=64
    for txt_,col in lines:
        t,_=text(250,y,2.4,txt_,col); b.append(t)
        y+=26
    b.append(f'<rect x="250" y="{y}" width="14" height="16" fill="{GREEN}" class="blink"/>')
    open(f"{OUT}/player.svg","w").write(svg(W,H,''.join(b),BLINK))

# ============================================================ 4. SKILLS
SKILLS=[
 ("BACKEND & SYSTEMS  [MAIN SPEC]",[("GO",14),("HTMX + TEMPL",12),("SQLITE",11),("LINUX / BASH",13),("DOCKER",10)]),
 ("DATA SCIENCE & ML  [ACADEMY]",[("PYTHON",14),("PANDAS / SKLEARN",12),("TENSORFLOW",10),("OPENCV",11)]),
 ("WEB & EXTENSIONS  [SIDE SPEC]",[("TYPESCRIPT",11),("JAVASCRIPT",11),("REACT",9),("C / C++",10)]),
]
def make_skills():
    rowh, ghdr = 32, 46
    H = 34 + sum(ghdr + len(sk)*rowh for _,sk in SKILLS) + 26
    W=900
    b=[bezel(W,H)]
    y=34
    for gi,(gname,sk) in enumerate(SKILLS):
        col=[GREEN,CYAN,ORANGE][gi]
        t,_=text(30,y,2.6,"-- "+gname+" --",YELLOW); b.append(t)
        y+=ghdr
        for name,lvl in sk:
            t,_=text(48,y,2.2,name,WHITE); b.append(t)
            for i in range(16):
                x=330+i*30
                if i<lvl:
                    tip = ' class="blink"' if i==lvl-1 else ''
                    b.append(f'<g{tip}><rect x="{x}" y="{y-2}" width="24" height="18" fill="{col}"/></g>')
                else:
                    b.append(f'<rect x="{x}" y="{y-2}" width="24" height="18" fill="none" stroke="{DIMGREEN}" stroke-width="1.5"/>')
            t,_=text(822,y,2,f"LV{lvl:02d}",GRAY); b.append(t)
            y+=rowh
        y+=0
    open(f"{OUT}/skills.svg","w").write(svg(W,H,''.join(b),BLINK))

# ============================================================ 5. QUEST PANEL (main quest)
def make_quest():
    W,H=900,240
    b=[bezel(W,H,YELLOW)]
    t,_=text(30,26,3,"MAIN QUEST",YELLOW); b.append(t)
    t,_=text(W-30,26,2.2,"STATUS: ACTIVE",GREEN,anchor="end",cls="blink"); b.append(t)
    t,_=text(30,72,4,"ATLAS",GREEN); b.append(t)
    t,_=text(180,79,2.2,"A SELF-HOSTED PERSONAL OPERATING SYSTEM",WHITE); b.append(t)
    t,_=text(30,116,2,"GO + HTMX + TEMPL + SQLITE. LOCAL-FIRST. ONE TAB TO RULE THEM ALL.",GRAY); b.append(t)
    t,_=text(30,146,2,"FTS5 GLOBAL SEARCH UNDER 100MS. NOTES, TASKS, JOURNAL, KNOWLEDGE.",GRAY); b.append(t)
    t,_=text(30,184,2.2,"V1.0 CLEAR!",YELLOW); b.append(t)
    for i in range(16):
        x=210+i*30
        if i<10:
            b.append(f'<rect x="{x}" y="180" width="24" height="16" fill="{YELLOW}"/>')
        else:
            b.append(f'<rect x="{x}" y="180" width="24" height="16" fill="none" stroke="{DIMGREEN}" stroke-width="1.5"/>')
    t,_=text(710,184,2,"V2.0 LOADING",WHITE,cls="blink"); b.append(t)
    open(f"{OUT}/quest-main.svg","w").write(svg(W,H,''.join(b),BLINK))

# ============================================================ 6. CONTINUE
def make_continue():
    W,H=900,230
    b=[bezel(W,H,RED)]
    t,_=text(W/2,30,5,"CONTINUE?",WHITE,anchor="middle"); b.append(t)
    for n in range(10):
        num=str(9-n)
        t,_=text(W/2,86,7,num,RED,anchor="middle",cls=f"cd cd{n}")
        b.append(t)
    ty=176
    t,_=text(W/2-160,ty,3,">",GREEN,cls="blink"); b.append(t)
    t,_=text(W/2-130,ty,3,"YES",GREEN); b.append(t)
    t,_=text(W/2+70,ty,3,"NO",GRAY); b.append(t)
    style=BLINK+".cd{opacity:0}"+''.join(
        f".cd{n}{{animation:cd 10s steps(1) infinite;animation-delay:{n}s}}" for n in range(10)
    )+"@keyframes cd{0%{opacity:1}10%{opacity:0}100%{opacity:0}}"
    open(f"{OUT}/continue.svg","w").write(svg(W,H,''.join(b),style))

# ============================================================ 7. FOOTER
def make_footer():
    W,H=900,170
    b=[bezel(W,H)]
    t,_=text(W/2,28,5,"GAME OVER",RED,anchor="middle"); b.append(t)
    t,_=text(W/2,92,2.4,"THANKS FOR PLAYING - STAR A REPO TO SAVE PROGRESS",WHITE,anchor="middle"); b.append(t)
    t,_=text(W/2,122,2,"(C) 2026 SUKE2004 * NO CONTINUES REQUIRED * GG",GRAY,anchor="middle"); b.append(t)
    dots=''.join(f'<rect x="{x}" y="{H-24}" width="4" height="4" fill="{YELLOW}"/>' for x in range(30,W-40,24))
    b.append(dots)
    b.append(pac(24,H-22,9,YELLOW,cls="pm"))
    style=f".pm{{animation:mv 9s linear infinite}}@keyframes mv{{from{{transform:translateX(0)}}to{{transform:translateX({W-60}px)}}}}"
    open(f"{OUT}/footer.svg","w").write(svg(W,H,''.join(b),style))

# ============================================================ build all
make_title()
make_player()
make_skills()
make_quest()
make_continue()
make_footer()
for fname,label in [
    ("hdr-player.svg","STAGE 1 * CHARACTER SELECT"),
    ("hdr-skills.svg","STAGE 2 * SKILL TREE"),
    ("hdr-quests.svg","STAGE 3 * QUEST LOG"),
    ("hdr-scores.svg","STAGE 4 * HIGH SCORES"),
    ("hdr-bonus.svg","BONUS STAGE * PAC-MAN"),
    ("hdr-trophy.svg","STAGE 5 * TROPHY ROOM"),
    ("hdr-continue.svg","FINAL STAGE * CONTINUE?"),
]:
    make_header(fname,label)

# validate all
for f in sorted(os.listdir(OUT)):
    if f.endswith(".svg"):
        ET.parse(os.path.join(OUT,f))
        sz=os.path.getsize(os.path.join(OUT,f))
        print(f"OK {f:22} {sz/1024:6.1f} KB")
