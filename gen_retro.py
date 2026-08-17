#!/usr/bin/env python3
"""Retro arcade SVG assets v2 — heavily animated.
Pixel bitmap font (no font deps). CSS animations run live on GitHub.
Set QA=1 env to force animated elements visible for static QA renders.
"""
import os, random, xml.etree.ElementTree as ET

random.seed(7)
OUT = os.environ.get("OUT", "assets")
QA = bool(os.environ.get("QA"))
os.makedirs(OUT, exist_ok=True)

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
'[':["01110","01000","01000","01000","01000","01000","01110"],
']':["01110","00010","00010","00010","00010","00010","01110"],
'=':["00000","00000","11111","00000","11111","00000","00000"],
}

GREEN="#00ff41"; DIMGREEN="#00902a"; YELLOW="#ffe600"; CYAN="#00e5ff"
RED="#ff3355"; WHITE="#ffffff"; GRAY="#8b949e"; BLACK="#000000"
ORANGE="#ffb000"; PINK="#ff7ad9"; BLUE="#2233ff"

def text(x, y, s, txt, color=None, cls=None, anchor="start", inherit=False):
    """Pixel text. inherit=True -> rects carry no fill (group fill animatable)."""
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
                        fill = '' if inherit else f' fill="{color}"'
                        parts.append(f'<rect x="{cx+c*s:g}" y="{y+r*s:g}" width="{run*s:g}" height="{s:g}"{fill}/>')
                        c += run
                    else:
                        c += 1
        cx += 6*s
    attrs = ''
    if cls: attrs += f' class="{cls}"'
    if inherit: attrs += f' fill="{color}"'
    return f'<g{attrs}>' + ''.join(parts) + '</g>', w

def scan(w, h):
    return ('<g opacity="0.16">' +
            ''.join(f'<rect x="0" y="{y}" width="{w}" height="1.5" fill="#000"/>' for y in range(0, h, 4)) +
            '</g>')

def bezel(w, h, color=GREEN, cls=None):
    a = f' class="{cls}"' if cls else ''
    return (f'<g{a}><rect x="3" y="3" width="{w-6}" height="{h-6}" fill="none" stroke="{color}" stroke-width="2"/>'
            f'<rect x="9" y="9" width="{w-18}" height="{h-18}" fill="none" stroke="{color}" stroke-width="1" opacity="0.35"/></g>')

def svg(w, h, body, style=""):
    if QA:
        style = ""  # strip all CSS so initially-hidden animated elements render visible
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<style>{style}</style>'
            f'<rect width="{w}" height="{h}" fill="{BLACK}"/>' + body + scan(w, h) + '</svg>')

BLINK = ".blink{animation:bl 1.1s steps(2,jump-none) infinite}@keyframes bl{0%,49%{opacity:1}50%,100%{opacity:0}}"
FASTBLINK = ".fblink{animation:fbl .5s steps(2,jump-none) infinite}@keyframes fbl{0%,49%{opacity:1}50%,100%{opacity:0}}"

def sprite(bitmap, palette, ox, oy, s, cls=None):
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
    a=f' class="{cls}"' if cls else ''
    return f'<g{a}>'+''.join(out)+'</g>'

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
PLAYER_PAL={'H':'#3a2b1e','S':'#e6b98f','K':'#101418','G':GREEN,'L':'#9aa0a6'}

def pacman(cx, cy, r, color=YELLOW, cls=""):
    """Chomping pacman: two mouth states alternating."""
    open_m  = f'<path d="M {cx} {cy} L {cx+r*0.95} {cy-r*0.55} A {r} {r} 0 1 0 {cx+r*0.95} {cy+r*0.55} Z" fill="{color}" class="mo"/>'
    closed  = f'<path d="M {cx} {cy} L {cx+r} {cy-r*0.12} A {r} {r} 0 1 0 {cx+r} {cy+r*0.12} Z" fill="{color}" class="mc"/>'
    return f'<g class="{cls}">{open_m}{closed}</g>'

CHOMP = (".mo{animation:cho .36s steps(1) infinite}.mc{animation:chc .36s steps(1) infinite}"
         "@keyframes cho{0%{opacity:1}50%{opacity:0}100%{opacity:1}}"
         "@keyframes chc{0%{opacity:0}50%{opacity:1}100%{opacity:0}}")

def eat_row(x0, x1, y, T, prefix, pac_r=10, ghost=False, ghost_pal=None):
    """Pacman crosses x0->x1 in T seconds eating dots; dots respawn each loop."""
    body=[]; css=[]
    dots=list(range(int(x0)+30, int(x1)-10, 22))
    for i,dx in enumerate(dots):
        p = (dx - x0) / (x1 - x0) * 100
        css.append(f".{prefix}d{i}{{animation:{prefix}k{i} {T}s linear infinite}}"
                   f"@keyframes {prefix}k{i}{{0%{{opacity:1}}{p:.1f}%{{opacity:1}}{min(p+0.4,99.8):.1f}%{{opacity:0}}99.9%{{opacity:0}}100%{{opacity:1}}}}")
        body.append(f'<rect x="{dx}" y="{y-2}" width="5" height="5" fill="{YELLOW}" class="{prefix}d{i}"/>')
    body.append(pacman(0, y, pac_r, YELLOW, cls=f"{prefix}pac"))
    css.append(f".{prefix}pac{{animation:{prefix}mv {T}s linear infinite}}"
               f"@keyframes {prefix}mv{{from{{transform:translate({x0}px,0)}}to{{transform:translate({x1}px,0)}}}}")
    if ghost:
        body.append(f'<g class="{prefix}gh">{sprite(GHOST, ghost_pal or {"R":RED,"W":WHITE,"B":BLUE}, -60, y-13, 2)}</g>')
        css.append(f".{prefix}gh{{animation:{prefix}gm {T}s linear infinite}}"
                   f"@keyframes {prefix}gm{{from{{transform:translate({x0}px,0)}}to{{transform:translate({x1}px,0)}}}}")
    return ''.join(body), ''.join(css)

# ============================================================ TITLE
def make_title():
    W,H=900,330
    b=[bezel(W,H)]
    css=[BLINK,CHOMP]
    # drifting parallax starfield
    for layer,(n,spd,op) in enumerate([(30,60,0.9),(25,110,0.5)]):
        stars=''.join(f'<rect x="{random.randint(0,W)}" y="{random.randint(16,H-40)}" width="{random.choice([2,3])}" height="{random.choice([2,3])}" fill="{WHITE}"/>' for _ in range(n))
        b.append(f'<g class="sf{layer}" opacity="{op}">{stars}<g transform="translate({W},0)">{stars}</g></g>')
        css.append(f".sf{layer}{{animation:sf{layer}m {spd}s linear infinite}}@keyframes sf{layer}m{{from{{transform:translateX(0)}}to{{transform:translateX(-{W}px)}}}}")
    # marquee strip top
    m1="* * * WELCOME TO THE SUKE2004 ARCADE * * * BACKEND DEV * SELF-HOSTER * DATA SCIENTIST * * * INSERT COIN * * * "
    t,mw=text(0,20,2,m1+m1,YELLOW,cls="mq"); b.append(f'<g>{t}</g>')
    css.append(f".mq{{animation:mqm 24s linear infinite}}@keyframes mqm{{from{{transform:translateX(0)}}to{{transform:translateX(-{mw/2:g}px)}}}}")
    # color-cycling title
    t,tw=text(W/2,64,9,"SUKE2004",GREEN,anchor="middle",cls="cyc",inherit=True); b.append(t)
    css.append(".cyc{animation:cyc 6s linear infinite}@keyframes cyc{0%{fill:#00ff41}25%{fill:#00e5ff}50%{fill:#ffe600}75%{fill:#ff7ad9}100%{fill:#00ff41}}")
    # bobbing ghosts
    b.append(f'<g class="gbob1">{sprite(GHOST,{"R":RED,"W":WHITE,"B":BLUE},W/2-tw/2-112,58,5)}</g>')
    b.append(f'<g class="gbob2">{sprite(GHOST,{"R":CYAN,"W":WHITE,"B":BLUE},W/2+tw/2+42,58,5)}</g>')
    css.append(".gbob1{animation:gb 1.6s ease-in-out infinite}.gbob2{animation:gb 1.6s ease-in-out .8s infinite}"
               "@keyframes gb{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}")
    t,_=text(W/2,152,3,"USTELA SUKESH REDDY",WHITE,anchor="middle"); b.append(t)
    t,_=text(W/2,190,2.6,"BACKEND DEV (GO) * SELF-HOSTING * DATA SCIENCE",CYAN,anchor="middle"); b.append(t)
    t,_=text(W/2,228,3,"PRESS START",WHITE,cls="blink",anchor="middle"); b.append(t)
    t,_=text(W/2,268,2,"(C) 2026 SUKE2004 - INSERT COIN TO CONNECT",GRAY,anchor="middle"); b.append(t)
    # chase scene: pacman eats dots, chased by ghost
    er,ec=eat_row(26,W-40,H-26,9,"tt",pac_r=10,ghost=True); b.append(er); css.append(ec)
    # power-on flicker
    css.append(".pwr{animation:pwr 1.2s steps(8) 1}@keyframes pwr{0%{opacity:0}40%{opacity:.4}60%{opacity:.9}70%{opacity:.5}100%{opacity:1}}")
    body=f'<g class="pwr">{"".join(b)}</g>'
    open(f"{OUT}/title.svg","w").write(svg(W,H,body,''.join(css)))

# ============================================================ HEADERS
def make_header(fname,label,color=GREEN):
    W,H=900,64
    css=[CHOMP]
    b=[f'<rect x="3" y="3" width="{W-6}" height="{H-6}" fill="none" stroke="{color}" stroke-width="2"/>']
    t,tw=text(30,18,4,label,color); b.append(t)
    x0=30+tw+30
    er,ec=eat_row(x0,W-30,H/2,6,"h",pac_r=11); b.append(er); css.append(ec)
    open(f"{OUT}/{fname}","w").write(svg(W,H,''.join(b),''.join(css)))

# ============================================================ PLAYER CARD
def make_player():
    W,H=900,380
    css=[BLINK,FASTBLINK]
    b=[bezel(W,H)]
    t,_=text(30,24,2.5,"1P  START",YELLOW,cls="blink"); b.append(t)
    # spinning score digits: SCORE 00071? last digit cycles
    t,_=text(W-30,24,2.5,"SCORE 00071",GRAY,anchor="end"); b.append(t)
    for n in range(10):
        tg,_=text(W-30+15,24,2.5,str(n),WHITE,cls=f"sc sc{n}")
        b.append(tg)
    css.append(".sc{opacity:0}"+''.join(f".sc{n}{{animation:sck 2s steps(1) infinite;animation-delay:{n*0.2}s}}" for n in range(10))
               +"@keyframes sck{0%{opacity:1}10%{opacity:0}100%{opacity:0}}")
    # avatar box, bobbing sprite
    b.append(f'<rect x="30" y="56" width="190" height="240" fill="none" stroke="{DIMGREEN}" stroke-width="2"/>')
    b.append(f'<g class="bob">{sprite(PLAYER_SPRITE,PLAYER_PAL,61,72,8)}</g>')
    css.append(".bob{animation:bobk 1s steps(2,jump-none) infinite}@keyframes bobk{0%,49%{transform:translateY(0)}50%,100%{transform:translateY(-4px)}}")
    t,_=text(125,216,2.4,"SUKE2004",GREEN,anchor="middle"); b.append(t)
    t,_=text(125,246,2,"LV.21 HUMAN",WHITE,anchor="middle"); b.append(t)
    # HP / coffee bars in avatar box
    t,_=text(44,270,1.6,"HP",RED); b.append(t)
    b.append(f'<rect x="70" y="270" width="130" height="8" fill="none" stroke="{DIMGREEN}"/><rect x="72" y="272" width="126" height="4" fill="{GREEN}"/>')
    t,_=text(44,284,1.6,"CF",ORANGE); b.append(t)
    b.append(f'<rect x="70" y="284" width="130" height="8" fill="none" stroke="{DIMGREEN}"/><rect x="72" y="286" width="126" height="4" fill="{ORANGE}" class="cf"/>')
    css.append(".cf{transform-origin:72px 288px;animation:cfk 8s linear infinite}@keyframes cfk{0%{transform:scaleX(1)}90%{transform:scaleX(.05)}100%{transform:scaleX(1)}}")
    # typed stat lines, staggered reveal
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
    for i,(txt_,col) in enumerate(lines):
        t,_=text(250,y,2.4,txt_,col,cls=f"tl tl{i}"); b.append(t)
        css.append(f".tl{i}{{animation-delay:{0.28*i:.2f}s}}")
        y+=28
    css.append(".tl{opacity:0;animation:tlk .01s steps(1) forwards}@keyframes tlk{to{opacity:1}}")
    b.append(f'<rect x="250" y="{y}" width="14" height="16" fill="{GREEN}" class="fblink"/>')
    open(f"{OUT}/player.svg","w").write(svg(W,H,''.join(b),''.join(css)))

# ============================================================ SKILLS
SKILLS=[
 ("BACKEND & SYSTEMS  [MAIN SPEC]",GREEN,[("GO",14,True),("HTMX + TEMPL",12,False),("SQLITE",11,False),("LINUX / BASH",13,False),("DOCKER",10,False)]),
 ("DATA SCIENCE & ML  [ACADEMY]",CYAN,[("PYTHON",14,False),("PANDAS / SKLEARN",12,False),("TENSORFLOW",10,False),("OPENCV",11,False)]),
 ("WEB & EXTENSIONS  [SIDE SPEC]",ORANGE,[("TYPESCRIPT",11,False),("JAVASCRIPT",11,False),("REACT",9,False),("C / C++",10,False)]),
]
def make_skills():
    rowh,ghdr=32,46
    H=34+sum(ghdr+len(sk)*rowh for _,_,sk in SKILLS)+26
    W=900
    css=[BLINK,FASTBLINK,
         ".cell{opacity:0;animation:cpop .01s steps(1) forwards}@keyframes cpop{to{opacity:1}}"]
    b=[bezel(W,H)]
    y=34; ci=0
    for gname,col,sk in SKILLS:
        t,_=text(30,y,2.6,"-- "+gname+" --",YELLOW); b.append(t)
        y+=ghdr
        for name,lvl,isnew in sk:
            t,_=text(48,y,2.2,name,WHITE); b.append(t)
            if isnew:
                t,_=text(48+len(name)*6*2.2+16,y,1.8,"UP!",RED,cls="fblink"); b.append(t)
            for i in range(16):
                x=330+i*30
                if i<lvl:
                    d=0.35+ci*0.04+i*0.055
                    extra=f';animation-delay:{d:.2f}s'
                    tip=' fblink' if i==lvl-1 else ''
                    b.append(f'<g class="cell{tip}" style="animation-delay:{d:.2f}s{",".join([""])}"><rect x="{x}" y="{y-2}" width="24" height="18" fill="{col}"/></g>')
                else:
                    b.append(f'<rect x="{x}" y="{y-2}" width="24" height="18" fill="none" stroke="{DIMGREEN}" stroke-width="1.5"/>')
            t,_=text(822,y,2,f"LV{lvl:02d}",GRAY); b.append(t)
            y+=rowh; ci+=1
    # fblink cells: after pop-in, blink forever (two anims)
    css.append(".cell.fblink{animation:cpop .01s steps(1) forwards, fbl .6s steps(2,jump-none) infinite 1.8s}")
    open(f"{OUT}/skills.svg","w").write(svg(W,H,''.join(b),''.join(css)))

# ============================================================ MAIN QUEST
def make_quest():
    W,H=900,240
    css=[BLINK,".sweep{animation:sw 4s linear infinite}@keyframes sw{from{transform:translateX(-80px)}to{transform:translateX(980px)}}",
         ".qcell{opacity:0;animation:qp .01s steps(1) forwards}@keyframes qp{to{opacity:1}}"]
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
            b.append(f'<g class="qcell" style="animation-delay:{0.3+i*0.12:.2f}s"><rect x="{x}" y="180" width="24" height="16" fill="{YELLOW}"/></g>')
        else:
            b.append(f'<rect x="{x}" y="180" width="24" height="16" fill="none" stroke="{DIMGREEN}" stroke-width="1.5"/>')
    t,_=text(710,184,2,"V2.0 LOADING",WHITE,cls="blink"); b.append(t)
    # light sweep
    b.append(f'<g class="sweep"><rect x="0" y="10" width="46" height="{H-20}" fill="{WHITE}" opacity="0.05"/></g>')
    open(f"{OUT}/quest-main.svg","w").write(svg(W,H,''.join(b),''.join(css)))

# ============================================================ CONTINUE
def make_continue():
    W,H=900,230
    css=[BLINK,".bz{animation:bzp 1.4s ease-in-out infinite}@keyframes bzp{0%,100%{opacity:1}50%{opacity:.35}}"]
    b=[bezel(W,H,RED,cls="bz")]
    t,_=text(W/2,30,5,"CONTINUE?",WHITE,anchor="middle"); b.append(t)
    for n in range(10):
        t,_=text(W/2,86,7,str(9-n),RED,anchor="middle",cls=f"cd cd{n}"); b.append(t)
    ty=176
    t,_=text(W/2-160,ty,3,">",GREEN,cls="blink"); b.append(t)
    t,_=text(W/2-130,ty,3,"YES",GREEN); b.append(t)
    t,_=text(W/2+70,ty,3,"NO",GRAY); b.append(t)
    css.append(".cd{opacity:0}"+''.join(f".cd{n}{{animation:cdk 10s steps(1) infinite;animation-delay:{n}s}}" for n in range(10))
               +"@keyframes cdk{0%{opacity:1}10%{opacity:0}100%{opacity:0}}")
    open(f"{OUT}/continue.svg","w").write(svg(W,H,''.join(b),''.join(css)))

# ============================================================ FOOTER
def make_footer():
    W,H=900,180
    css=[CHOMP,
         ".gl{animation:glk 5s steps(1) infinite}@keyframes glk{0%,88%{transform:translate(0,0)}89%{transform:translate(4px,-2px)}90%{transform:translate(-4px,2px)}91%{transform:translate(2px,0)}92%,100%{transform:translate(0,0)}}",
         ".glr{animation:glo 5s steps(1) infinite}@keyframes glo{0%,88%{opacity:0}89%{opacity:.7}91%{opacity:.5}92%,100%{opacity:0}}"]
    b=[bezel(W,H)]
    t,_=text(W/2,28,5,"GAME OVER",RED,anchor="middle",cls="gl"); b.append(t)
    t,_=text(W/2+3,28,5,"GAME OVER",CYAN,anchor="middle",cls="glr"); b.append(t)
    t,_=text(W/2,96,2.4,"THANKS FOR PLAYING - STAR A REPO TO SAVE PROGRESS",WHITE,anchor="middle"); b.append(t)
    t,_=text(W/2,126,2,"(C) 2026 SUKE2004 * NO CONTINUES REQUIRED * GG",GRAY,anchor="middle"); b.append(t)
    er,ec=eat_row(26,W-40,H-26,9,"ft",pac_r=10,ghost=True,ghost_pal={"R":PINK,"W":WHITE,"B":BLUE}); b.append(er); css.append(ec)
    open(f"{OUT}/footer.svg","w").write(svg(W,H,''.join(b),''.join(css)))

# ============================================================ MARQUEE DIVIDER
def make_marquee():
    W,H=900,46
    m="*** 719 CONTRIBUTIONS AND COUNTING *** 52 PUBLIC REPOS *** GUILD: SUPERPLUGS *** MAIN QUEST: ATLAS *** NOW LOADING NEXT STAGE *** "
    t,mw=text(0,14,2.4,m+m,GREEN,cls="mq")
    css=f".mq{{animation:mqm 26s linear infinite}}@keyframes mqm{{from{{transform:translateX(0)}}to{{transform:translateX(-{mw/2:g}px)}}}}"
    b=[f'<rect x="3" y="3" width="{W-6}" height="{H-6}" fill="none" stroke="{DIMGREEN}" stroke-width="2"/>',
       f'<g>{t}</g>']
    open(f"{OUT}/marquee.svg","w").write(svg(W,H,''.join(b),css))

make_title(); make_player(); make_skills(); make_quest(); make_continue(); make_footer(); make_marquee()
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

for f in sorted(os.listdir(OUT)):
    if f.endswith(".svg"):
        ET.parse(os.path.join(OUT,f))
        print(f"OK {f:22} {os.path.getsize(os.path.join(OUT,f))/1024:6.1f} KB")
