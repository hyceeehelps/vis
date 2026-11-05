from __future__ import annotations
from pathlib import Path
import math, os, subprocess
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

PROJECT=Path(os.environ.get('SURVIVAL_PROJECT', Path(__file__).resolve().parent))
ASSET=Path(os.environ.get('SURVIVAL_ASSETS', PROJECT/'assets'))
SCENES=PROJECT/'scenes'
SCENES.mkdir(parents=True,exist_ok=True) if os.environ.get('SURVIVAL_WRITE_SCENES') else None
W,H=720,1280   # 9:16 delivery (house spec is 1080x1920 — builder upscales)
FPS=24
INK=(52,39,36,255); RED=(191,37,48,255); RED2=(222,61,53,255)
TAN=(197,151,101,255); TAN2=(226,194,150,255)
GRASS=(105,151,92,255); GRASS2=(139,176,104,255)
BLUE=(80,151,187,255); CREAM=(255,248,235,255); WHITE=(255,255,255,255)
FONT_REG='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def font(sz,bold=False): return ImageFont.truetype(FONT_BOLD if bold else FONT_REG,sz)

def line(d,pts,fill=INK,width=4): d.line(pts,fill=fill,width=width,joint='curve')

def center_text(d,xy,text,fnt,fill,anchor='mm'): d.text(xy,text,font=fnt,fill=fill,anchor=anchor)

# Build a clean face-free pepper body from the selected reference. Use the outer contour
# of the red body itself so old arms/legs are not baked into this moving body layer.
def make_body_base():
    src=np.array(Image.open(ASSET/'E_reference.png').convert('RGBA'))
    h,w=src.shape[:2]; rgb=src[:,:,:3].astype(np.int16); r,g=rgb[:,:,0],rgb[:,:,1]
    body_poly=[(573,199),(608,193),(715,194),(751,206),(760,222),(765,274),(763,346),(761,400),(751,470),(739,516),(722,566),(698,592),(675,615),(640,630),(575,638),(553,604),(542,570),(540,520),(540,460),(530,394),(511,270),(520,241),(538,216)]
    roi=np.zeros((h,w),np.uint8); cv2.fillPoly(roi,[np.array(body_poly,np.int32)],255)
    redmask=cv2.bitwise_and(roi,((r-g)>60).astype(np.uint8)*255)
    n,labels,stats,_=cv2.connectedComponentsWithStats(redmask,8)
    idx=1+int(np.argmax(stats[1:,cv2.CC_STAT_AREA]))
    comp=(labels==idx).astype(np.uint8)*255
    contours,_=cv2.findContours(comp,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contour=max(contours,key=cv2.contourArea)
    fill=np.zeros((h,w),np.uint8); cv2.drawContours(fill,[contour],-1,255,-1)
    outline=np.zeros((h,w),np.uint8); cv2.drawContours(outline,[contour],-1,255,4)
    alpha=np.maximum(fill,outline)
    yy,xx=np.indices((h,w))
    face=(rgb.max(axis=2)<105)&(yy>=260)&(yy<355)&(xx>=548)&(xx<730)
    face=cv2.dilate(face.astype(np.uint8),cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(13,13)))
    inpaint=cv2.inpaint(src[:,:,:3],face,12,cv2.INPAINT_TELEA)
    body=src.copy(); body[:,:,:3]=inpaint; body[:,:,3]=alpha
    return Image.fromarray(body,'RGBA')

BODY=make_body_base()
STEM=Image.open(ASSET/'E_stem.png').convert('RGBA')
ARMS={k:Image.open(ASSET/f'E_arm_{k}.png').convert('RGBA') for k in ('left','right')}
LEGS={k:Image.open(ASSET/f'E_leg_{k}.png').convert('RGBA') for k in ('left','right')}
FACES={k:Image.open(ASSET/f'E_face_{k}.png').convert('RGBA') for k in ('sad','surprised','neutral','happy')}
MOUTHS={k:Image.open(ASSET/f'E_mouth_{k}.png').convert('RGBA') for k in ('closed','frown')}

def rotate_part(layer,pivot,angle):
    arr=np.array(layer)
    M=cv2.getRotationMatrix2D(pivot,angle,1.0)
    result=cv2.warpAffine(arr,M,(arr.shape[1],arr.shape[0]),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=(0,0,0,0))
    return Image.fromarray(result,'RGBA')

def make_character(pose):
    canvas=Image.new('RGBA',(1280,832),(0,0,0,0))
    # Limbs sit behind the pepper body; their hidden overlaps make each connection clean.
    for side,pivot in [('left',(594,632)),('right',(686,583))]:
        canvas.alpha_composite(rotate_part(LEGS[side],pivot,pose.get('leg_'+side,0)))
    for side,pivot in [('left',(527,396)),('right',(758,397))]:
        canvas.alpha_composite(rotate_part(ARMS[side],pivot,pose.get('arm_'+side,0)))
    canvas.alpha_composite(BODY)
    canvas.alpha_composite(STEM)
    canvas.alpha_composite(FACES[pose.get('face','neutral')])
    # Mouth stays visible but closed; narration is voiceover only, with no lip-sync or direct-to-camera talking.
    canvas.alpha_composite(MOUTHS[pose.get('mouth','closed')])
    return canvas

# Farm scene in the style of the user's flat, outlined barn doodle. Layout remains fixed:
# barn on screen-left, well on screen-right, dirt path through the middle.
def gradient_sky(weather):
    colors={
      'dawn':((159,190,207),(250,217,167)),
      'morning':((165,202,220),(245,232,196)),
      'cloudy':((153,174,188),(224,218,192)),
      'storm':((102,123,142),(180,187,173)),
      'dusk':((92,100,126),(222,155,111)),
    }
    top,bottom=colors[weather]
    a=np.zeros((H,W,4),dtype=np.uint8)
    for y in range(H):
        t=y/(H-1)
        c=tuple(round(top[i]*(1-t)+bottom[i]*t) for i in range(3))
        a[y,:,:3]=c; a[y,:,3]=255
    return Image.fromarray(a,'RGBA')

def doodle_cloud(d,x,y,s=1,fill=(246,244,231,255)):
    width=max(2,round(3*s))
    d.ellipse((x,y+12*s,x+43*s,y+42*s),fill=fill,outline=INK,width=width)
    d.ellipse((x+17*s,y,x+56*s,y+39*s),fill=fill,outline=INK,width=width)
    d.ellipse((x+39*s,y+10*s,x+80*s,y+42*s),fill=fill,outline=INK,width=width)
    d.rectangle((x+13*s,y+23*s,x+60*s,y+41*s),fill=fill)
    line(d,[(x+6*s,y+39*s),(x+72*s,y+39*s)],INK,width)

def doodle_sun(d,cx,cy,r=30):
    d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=(255,211,111,255),outline=INK,width=3)
    for i in range(8):
        a=i*math.pi/4
        p1=(cx+int((r+7)*math.cos(a)),cy+int((r+7)*math.sin(a)))
        p2=(cx+int((r+17)*math.cos(a)),cy+int((r+17)*math.sin(a)))
        line(d,[p1,p2],INK,3)

def draw_well(d,x,y,s=1.0,cloudy=False):
    w=lambda v:max(2,round(v*s))
    # A small timber-roofed well and hanging pail.
    roof=(x+4*s,y+27*s,x+90*s,y+27*s)
    d.polygon([(x+3*s,y+28*s),(x+46*s,y+2*s),(x+91*s,y+28*s)],fill=TAN2,outline=INK)
    line(d,[(x+3*s,y+28*s),(x+46*s,y+2*s),(x+91*s,y+28*s)],INK,w(4))
    line(d,[(x+15*s,y+27*s),(x+15*s,y+90*s)],INK,w(5))
    line(d,[(x+78*s,y+27*s),(x+78*s,y+90*s)],INK,w(5))
    line(d,[(x+15*s,y+34*s),(x+78*s,y+34*s)],INK,w(4))
    line(d,[(x+47*s,y+34*s),(x+47*s,y+68*s)],INK,w(3))
    # Bucket with clear/dirty water.
    bucketfill=(139,151,151,255) if cloudy else (102,171,199,255)
    d.polygon([(x+37*s,y+62*s),(x+58*s,y+62*s),(x+55*s,y+88*s),(x+40*s,y+88*s)],fill=TAN,outline=INK)
    d.ellipse((x+39*s,y+60*s,x+57*s,y+66*s),fill=bucketfill,outline=INK,width=w(2))
    if cloudy:
        line(d,[(x+41*s,y+62*s),(x+47*s,y+64*s),(x+54*s,y+61*s)],(211,216,205,255),w(2))
        d.ellipse((x+45*s,y+70*s,x+52*s,y+77*s),fill=(170,153,124,255))
    # Stone rim / opening.
    d.ellipse((x+4*s,y+84*s,x+91*s,y+111*s),fill=(168,166,154,255),outline=INK,width=w(4))
    d.ellipse((x+15*s,y+90*s,x+80*s,y+104*s),fill=(67,126,150,255),outline=INK,width=w(2))
    line(d,[(x+25*s,y+96*s),(x+41*s,y+93*s),(x+54*s,y+97*s),(x+70*s,y+94*s)],(218,241,239,255),w(2))
    return (x+46*s,y+65*s)

def draw_hen(d,x,y,s=1.0):
    w=lambda v:max(2,round(v*s))
    d.ellipse((x+4*s,y+20*s,x+70*s,y+66*s),fill=(255,250,237,255),outline=INK,width=w(3))
    d.ellipse((x+47*s,y+8*s,x+78*s,y+39*s),fill=(255,250,237,255),outline=INK,width=w(3))
    d.polygon([(x+76*s,y+21*s),(x+91*s,y+27*s),(x+76*s,y+32*s)],fill=(243,174,57,255),outline=INK)
    for ox,oy in [(54,3),(63,0),(72,5)]: d.ellipse((x+ox*s,y+oy*s,x+(ox+9)*s,y+(oy+14)*s),fill=RED,outline=INK,width=w(2))
    d.ellipse((x+62*s,y+18*s,x+68*s,y+24*s),fill=INK)
    line(d,[(x+30*s,y+65*s),(x+28*s,y+75*s),(x+22*s,y+76*s)],INK,w(3))
    line(d,[(x+56*s,y+65*s),(x+59*s,y+75*s),(x+65*s,y+76*s)],INK,w(3))

def draw_nest(d,x,y,s=1.0,shine=False):
    w=lambda v:max(2,round(v*s))
    # Three warm eggs inside a straw nest.
    for dx in [7,31,55]:
        d.ellipse((x+dx*s,y+4*s,x+(dx+20)*s,y+37*s),fill=(255,248,220,255),outline=INK,width=w(2))
    d.arc((x,y+18*s,x+82*s,y+60*s),180,355,fill=INK,width=w(4))
    d.arc((x+4*s,y+23*s,x+78*s,y+63*s),5,175,fill=(145,104,70,255),width=w(3))
    for i in range(6):
        xx=x+(5+i*13)*s
        line(d,[(xx,y+48*s),(xx+10*s,y+39*s)],(163,118,72,255),w(2))
    if shine:
        for cx in [x+17*s,x+42*s,x+66*s]:
            line(d,[(cx,y-4*s),(cx,y-11*s)],(244,181,54,255),w(2))

def draw_bucket(d,x,y,s=1.0,cloudy=False):
    w=lambda v:max(2,round(v*s))
    fill=(143,153,152,255) if cloudy else (106,174,201,255)
    d.arc((x+5*s,y,x+45*s,y+40*s),180,360,fill=INK,width=w(3))
    d.polygon([(x+4*s,y+18*s),(x+47*s,y+18*s),(x+41*s,y+61*s),(x+11*s,y+61*s)],fill=TAN,outline=INK)
    d.ellipse((x+4*s,y+10*s,x+47*s,y+25*s),fill=fill,outline=INK,width=w(3))
    if cloudy:
        line(d,[(x+12*s,y+18*s),(x+23*s,y+21*s),(x+35*s,y+17*s)],(221,224,211,255),w(2))
        d.ellipse((x+21*s,y+35*s,x+28*s,y+42*s),fill=(162,140,110,255))
    else:
        line(d,[(x+12*s,y+18*s),(x+22*s,y+15*s),(x+34*s,y+19*s)],(222,245,247,255),w(2))

def draw_fence(d,x1,y,x2,step=55):
    line(d,[(x1,y+18),(x2,y+18)],(113,79,52,255),4)
    line(d,[(x1,y+47),(x2,y+47)],(113,79,52,255),4)
    for x in range(x1,x2+1,step):
        d.polygon([(x-8,y+52),(x-8,y-5),(x,y-19),(x+8,y-5),(x+8,y+52)],fill=TAN,outline=INK)

def draw_grass(d,x,y,color=GRASS):
    for i in range(3):
        dx=i*9
        line(d,[(x+dx,y),(x+dx-4,y-12-i%2*4)],color,3)
        line(d,[(x+dx,y),(x+dx+5,y-10-i%2*4)],color,3)

def background(weather,include_nest=False,cloudy_bucket=False,close_door=False):
    img=gradient_sky(weather); d=ImageDraw.Draw(img,'RGBA')
    # Low sun at dawn, distant hills and a muted green farm field.
    if weather in ('dawn','morning'):
        doodle_sun(d,1080,176,27)
    d.polygon([(0,366),(150,330),(305,359),(480,334),(665,365),(850,336),(1030,362),(1170,333),(1280,350),(1280,720),(0,720)],fill=(111,155,91,255))
    d.polygon([(0,410),(210,384),(394,411),(610,379),(824,407),(1050,378),(1280,405),(1280,720),(0,720)],fill=(135,169,98,255))
    # Central dirt path stays in the same position in every scene.
    d.polygon([(604,359),(668,359),(885,720),(385,720)],fill=(190,151,101,255),outline=(117,84,58,255))
    d.polygon([(620,366),(653,366),(806,720),(468,720)],fill=(209,174,124,255))
    # Gentle path marks and small stones.
    for x,y,rx in [(630,435,7),(608,485,5),(672,520,6),(573,583,5),(713,640,7),(525,686,6)]:
        d.ellipse((x-rx,y-rx/2,x+rx,y+rx/2),fill=(168,132,91,255))
    # Fence lines recede toward the horizon.
    draw_fence(d,0,330,435,62); draw_fence(d,845,333,1280,62)
    # User-supplied barn doodle: same red barn/silo, always screen-left.
    barn=Image.open(ASSET/'barn_doodle_user_reference.png').convert('RGBA')
    barn=barn.resize((292,265),Image.Resampling.LANCZOS)
    img.alpha_composite(barn,(58,211))
    d=ImageDraw.Draw(img,'RGBA')
    # A side door panel on the barn edge is shown closed only in the storm/ending shots.
    if close_door:
        d.rounded_rectangle((319,390,370,470),radius=4,fill=(155,38,45,255),outline=INK,width=4)
        d.line((327,398,361,462),fill=(230,188,137,255),width=3)
        d.line((361,398,327,462),fill=(230,188,137,255),width=3)
        d.ellipse((358,428,364,434),fill=(244,203,84,255),outline=INK,width=1)
    # Well is always screen-right, same location and structure.
    well_head=draw_well(d,960,286,1.45,cloudy=cloudy_bucket)
    d.ellipse((942,443,1090,466),fill=(95,119,76,105))
    # Small farm details, kept secondary to the pepper.
    for x,y in [(35,510),(390,450),(870,500),(1158,494),(1213,558)]: draw_grass(d,x,y)
    # Farm rows behind the path.
    for start in [15,90,1100,1175]:
        for yy in [515,552,590]:
            line(d,[(start,yy),(start+35,yy-7)],(88,131,74,255),2)
    if include_nest:
        draw_hen(d,262,439,0.72)
        draw_nest(d,302,485,0.75,shine=True)
    if weather=='storm':
        # Rolling clouds and slanted rain on the same stable layout.
        doodle_cloud(d,465,75,1.08,(104,119,132,255))
        doodle_cloud(d,745,88,1.18,(106,121,134,255))
        for i in range(8):
            x=470+i*54
            line(d,[(x,145),(x-9,164)],(108,163,189,255),3)
        for i in range(5):
            x=880+i*40
            line(d,[(x,194),(x-10,214)],(108,163,189,255),3)
        line(d,[(365,274),(397,267),(383,281),(415,274)],(235,239,226,255),4)
        line(d,[(838,250),(870,243),(856,257),(889,249)],(235,239,226,255),4)
    elif weather=='dusk':
        doodle_cloud(d,850,92,0.9,(127,133,150,255))
        doodle_sun(d,1086,295,24)
    elif weather=='cloudy':
        doodle_cloud(d,828,79,0.95,(201,208,204,255))
    return img

# Character placement: large, full-body, and centered on the path. E faces camera with a visible static mouth; narration is voiceover only, with no lip-sync.
def place_character(img,pose,center_x=610,target_h=535):
    char=make_character(pose)
    bbox=char.getchannel('A').getbbox()
    char=char.crop(bbox)
    scale=target_h/char.height
    char=char.resize((round(char.width*scale),target_h),Image.Resampling.LANCZOS)
    x=round(center_x-char.width/2); y=92
    img.alpha_composite(char,(x,y))
    return img

def title_badge(img):
    d=ImageDraw.Draw(img,'RGBA')
    d.rounded_rectangle((390,15,890,57),radius=18,fill=(255,248,234,238),outline=(78,54,46,220),width=2)
    center_text(d,(640,36),'FARM SURVIVAL  •  DAY 2',font(23,True),(76,49,42,255))

def subtitle(img,text):
    if not text: return
    d=ImageDraw.Draw(img,'RGBA')
    d.rounded_rectangle((34,646,1246,709),radius=17,fill=(42,34,32,230),outline=(255,249,237,230),width=2)
    fnt=font(18,False); maxw=1148
    words=text.split(); lines=[]; cur=''
    for word in words:
        trial=(cur+' '+word).strip()
        if d.textlength(trial,font=fnt)>maxw and cur: lines.append(cur);cur=word
        else: cur=trial
    if cur: lines.append(cur)
    if len(lines)>2:
        fnt=font(16,False); lines=[];cur=''
        for word in words:
            trial=(cur+' '+word).strip()
            if d.textlength(trial,font=fnt)>maxw and cur: lines.append(cur);cur=word
            else: cur=trial
        if cur: lines.append(cur)
    y=677-(len(lines)-1)*11
    for ln in lines:
        center_text(d,(640,y),ln,fnt,WHITE); y+=22

def draw_wet_puddles(d):
    for box in [(454,580,530,595),(690,628,762,642),(885,538,944,551)]:
        d.ellipse(box,fill=(104,160,179,130),outline=(78,127,146,190),width=2)
        x1,y1,x2,y2=box
        line(d,[(x1+12,y1+4),(x1+30,y1+3),(x1+46,y1+5)],(222,239,233,220),2)

def draw_broken_fence(d,x=832,y=465):
    # A damaged foreground fence panel, clearly separate from the stable farm layout.
    d.ellipse((x-6,y+52,x+142,y+72),fill=(82,116,73,100))
    d.polygon([(x+4,y+48),(x+10,y-2),(x+20,y-14),(x+27,y+48)],fill=TAN,outline=INK)
    d.polygon([(x+108,y+49),(x+114,y-3),(x+124,y-13),(x+132,y+49)],fill=TAN,outline=INK)
    # The upper rail is snapped; the lower rail hangs at an angle.
    line(d,[(x+18,y+5),(x+53,y+8),(x+62,y+3)],(113,79,52,255),6)
    line(d,[(x+75,y+2),(x+114,y+6)],(113,79,52,255),6)
    line(d,[(x+20,y+35),(x+63,y+34),(x+74,y+47),(x+116,y+42)],(113,79,52,255),6)
    line(d,[(x+58,y-1),(x+65,y+5),(x+60,y+11)],(240,213,167,255),3)

def draw_dry_wood(d,x=321,y=466):
    # Small dry sticks tucked beneath the barn's roof overhang.
    d.ellipse((x-8,y+27,x+111,y+47),fill=(91,119,75,95))
    for i,(dy,dx) in enumerate([(0,0),(10,8),(20,1),(5,22)]):
        line(d,[(x+dx,y+dy),(x+80+dx,y+dy-5)],(122,79,47,255),7)
        line(d,[(x+2+dx,y+dy-3),(x+10+dx,y+dy+3)],(220,183,132,255),2)

def draw_fire_pot(d,x=805,y=425,phase=0,steam=True):
    # A small, controlled cooking flame and a simple metal pot held above it.
    d.ellipse((x-16,y+103,x+118,y+126),fill=(72,91,62,95))
    # kindling/logs
    line(d,[(x+5,y+95),(x+93,y+103)],(99,63,42,255),8)
    line(d,[(x+17,y+106),(x+83,y+91)],(123,79,49,255),7)
    # Flame silhouette varies slightly in the final waiting hold.
    h=32+[0,5,-2,7][phase%4]
    d.polygon([(x+25,y+94),(x+31,y+94-h//2),(x+43,y+94-h),(x+48,y+94-h//2),(x+60,y+94-h+4),(x+68,y+94-h//3),(x+78,y+94)],fill=(239,128,45,255),outline=INK)
    d.polygon([(x+43,y+94),(x+49,y+94-h//2),(x+57,y+94-h+9),(x+64,y+94-h//3)],fill=(255,204,75,255),outline=None)
    # Pot and side handles.
    d.polygon([(x+25,y+25),(x+92,y+25),(x+84,y+66),(x+34,y+66)],fill=(155,167,167,255),outline=INK)
    line(d,[(x+25,y+25),(x+92,y+25),(x+84,y+66),(x+34,y+66),(x+25,y+25)],INK,4)
    d.ellipse((x+20,y+19,x+97,y+31),fill=(193,202,198,255),outline=INK,width=3)
    d.ellipse((x+45,y+14,x+70,y+21),fill=TAN,outline=INK,width=2)
    line(d,[(x+17,y+37),(x+7,y+45),(x+18,y+52)],INK,3)
    line(d,[(x+100,y+37),(x+111,y+45),(x+99,y+52)],INK,3)
    line(d,[(x+36,y+43),(x+51,y+47),(x+68,y+43),(x+83,y+47)],BLUE,2)
    if steam:
        for sx,offset in [(x+43,0),(x+62,8),(x+79,-3)]:
            line(d,[(sx,y+10),(sx-5,y-1+offset),(sx+1,y-12+offset)],(235,241,234,220),3)

def draw_roof_drips(d):
    # Rain has stopped; last drops fall from the barn eave and roof.
    for x,y in [(310,398),(333,405),(356,412)]:
        d.ellipse((x,y,x+7,y+11),fill=BLUE,outline=INK,width=1)
        line(d,[(x+3,y-5),(x+3,y-1)],BLUE,2)

_BG_CACHE={}
def background_portrait(weather,cloudy_bucket=False):
    """Portrait 9:16 re-layout preserving barn-left, well-right, centered path (cached)."""
    key=(weather,cloudy_bucket)
    if key in _BG_CACHE: return _BG_CACHE[key].copy()
    img=_background_portrait_raw(weather,cloudy_bucket)
    _BG_CACHE[key]=img
    return img.copy()

def _background_portrait_raw(weather,cloudy_bucket=False):
    img=gradient_sky(weather); d=ImageDraw.Draw(img,'RGBA')
    if weather in ('dawn','morning'):
        doodle_sun(d,600,215,30)
    # Distant hills and farm field fill the tall frame.
    d.polygon([(0,560),(110,520),(235,553),(355,520),(500,556),(620,523),(720,547),(720,1280),(0,1280)],fill=(111,155,91,255))
    d.polygon([(0,613),(132,583),(275,610),(431,579),(586,609),(720,580),(720,1280),(0,1280)],fill=(135,169,98,255))
    # Center path opens toward the viewer while keeping a clear vertical centerline.
    d.polygon([(303,576),(417,576),(720,1280),(0,1280)],fill=(190,151,101,255),outline=(117,84,58,255))
    d.polygon([(320,584),(400,584),(624,1280),(96,1280)],fill=(209,174,124,255))
    for x,y,rx in [(343,665,6),(378,745,5),(304,825,6),(424,902,5),(268,1000,6)]:
        d.ellipse((x-rx,y-rx/2,x+rx,y+rx/2),fill=(168,132,91,255))
    # Background fence, behind both the barn and well.
    draw_fence(d,0,554,720,72)
    barn=Image.open(ASSET/'barn_doodle_user_reference.png').convert('RGBA')
    barn=barn.resize((260,236),Image.Resampling.LANCZOS)
    img.alpha_composite(barn,(22,357))
    d=ImageDraw.Draw(img,'RGBA')
    draw_well(d,540,412,1.27,cloudy=cloudy_bucket)
    d.ellipse((518,556,694,587),fill=(95,119,76,105))
    for x,y in [(42,740),(188,672),(670,765),(80,930),(625,1020)]:
        draw_grass(d,x,y)
    for start_x in [28,106,610,675]:
        for yy in [790,843,896]:
            line(d,[(start_x,yy),(start_x+32,yy-7)],(88,131,74,255),2)
    if weather=='cloudy':
        doodle_cloud(d,485,93,1.04,(201,208,204,255))
        doodle_cloud(d,110,145,0.68,(210,215,209,255))
    elif weather=='storm':
        doodle_cloud(d,290,105,1.15,(104,119,132,255))
        doodle_cloud(d,500,130,1.10,(106,121,134,255))
        for i in range(7):
            x=260+i*48
            line(d,[(x,205),(x-10,226)],(108,163,189,255),3)
    return img

def place_character_portrait(img,pose,center_x=360,target_h=680,top=310,bob=0):
    """bob = vertical offset in px (idle breathing / weight shift)."""
    top = int(round(top + bob))
    char=make_character(pose)
    bbox=char.getchannel('A').getbbox()
    char=char.crop(bbox)
    scale=target_h/char.height
    char=char.resize((round(char.width*scale),target_h),Image.Resampling.LANCZOS)
    img.alpha_composite(char,(round(center_x-char.width/2),top))
    return img

TITLE_LABEL='FARM SURVIVAL  •  DAY 2'
def title_badge_portrait(img,label=None):
    d=ImageDraw.Draw(img,'RGBA')
    d.rounded_rectangle((70,22,650,70),radius=20,fill=(255,248,234,238),outline=(78,54,46,220),width=2)
    center_text(d,(360,46),label or TITLE_LABEL,font(21,True),(76,49,42,255))

def subtitle_portrait(img,text):
    if not text: return
    d=ImageDraw.Draw(img,'RGBA')
    d.rounded_rectangle((24,1113,696,1247),radius=18,fill=(42,34,32,235),outline=(255,249,237,235),width=2)
    fnt=font(20,False); maxw=626
    words=text.split(); lines=[]; cur=''
    for word in words:
        trial=(cur+' '+word).strip()
        if d.textlength(trial,font=fnt)>maxw and cur:
            lines.append(cur); cur=word
        else: cur=trial
    if cur: lines.append(cur)
    if len(lines)>3:
        fnt=font(18,False); lines=[]; cur=''
        for word in words:
            trial=(cur+' '+word).strip()
            if d.textlength(trial,font=fnt)>maxw and cur:
                lines.append(cur); cur=word
            else: cur=trial
        if cur: lines.append(cur)
    line_h=27 if fnt.size>=20 else 24
    y=1180-(len(lines)-1)*line_h/2
    for ln in lines:
        center_text(d,(360,y),ln,fnt,WHITE); y+=line_h

def draw_wet_puddles_portrait(d):
    for box in [(92,720,166,739),(520,720,596,736),(238,1025,310,1042)]:
        d.ellipse(box,fill=(104,160,179,130),outline=(78,127,146,190),width=2)
        x1,y1,x2,y2=box
        line(d,[(x1+12,y1+4),(x1+30,y1+3),(x1+46,y1+5)],(222,239,233,220),2)

def draw_roof_drips_portrait(d):
    for x,y in [(228,579),(248,584),(268,589)]:
        d.ellipse((x,y,x+7,y+11),fill=BLUE,outline=INK,width=1)
        line(d,[(x+3,y-5),(x+3,y-1)],BLUE,2)

def scene_frame_day2_portrait(pose,caption=None,prop='cold',fire_phase=0,show_title=True,
                              weather='cloudy',look='center',env=None):
    """One rendered panel.

    Adds motion + framing hooks on top of the original Day 2 panel:
    - fire_phase: 0..N drives the flame silhouette height (real movement, not a still)
    - weather: 'dawn' | 'morning' | 'cloudy' | 'storm' | 'dusk' (gradient_sky presets)
    - look: 'center' | 'down' | 'up' | 'left' | 'right' — moves the camera by re-framing
    - env: optional dict of animated rain / wind / embers (see env_overlay)
    """
    img=background_portrait(weather,cloudy_bucket=(prop=='water'))
    d=ImageDraw.Draw(img,'RGBA')
    draw_wet_puddles_portrait(d)
    draw_roof_drips_portrait(d)
    if prop=='broken':
        draw_broken_fence(d,492,690)
    elif prop=='water':
        draw_bucket(d,564,620,1.05,cloudy=True)
        line(d,[(568,612),(607,612)],INK,3)
    elif prop=='wood':
        draw_dry_wood(d,196,562)
    elif prop in ('fire','fire_hold'):
        # Put the pot behind E so the reaching glove can overlap its rim.
        draw_fire_pot(d,548,750,phase=fire_phase,steam=(prop=='fire_hold'))
    place_character_portrait(img,pose,center_x=360,target_h=680,top=310,
                             bob=(env or {}).get('bob',0.0))
    if prop=='cold':
        line(d,[(195,480),(207,470),(199,460)],(230,241,240,255),3)
        line(d,[(516,475),(528,465),(520,455)],(230,241,240,255),3)
    if prop=='broken':
        line(d,[(486,690),(477,681)],(237,237,220,255),3)
        line(d,[(484,701),(472,701)],(237,237,220,255),3)
    if env: env_overlay(img, env)
    if look!='center': img=camera_look(img, look, env)
    if show_title: title_badge_portrait(img)
    subtitle_portrait(img,caption)   # panel's own subtitle (only when the panel asks for one)
    return img

def scene_panel(d=None, f=0, n=1, t=0.0):
    """Factory-style scene hook: rendered per-frame by the part's anim module.

    Set rig.PANEL = dict(pose=..., prop=..., weather=..., look=..., env=...) before a
    scene renders; the anim module's scene function calls this once per frame.
    """
    cfg = PANEL
    env = dict(cfg.get('env') or {})
    env['f'] = f
    env['n'] = n
    if 'bob' not in env:
        env['bob'] = 1.2 * math.sin(f * 0.45)      # idle breathing / weight shift
    img = scene_frame_day2_portrait(cfg['pose'], None, cfg.get('prop', 'cold'),
                                   int(f / 3) % 4, False,
                                   weather=cfg.get('weather', 'cloudy'),
                                   look=cfg.get('look', 'center'), env=env)
    if d is not None:
        d._image.paste(img.convert('RGB')) if hasattr(d, '_image') else None
    return img

PANEL = {'pose': {'face': 'sad', 'mouth': 'frown'}, 'prop': 'cold', 'weather': 'cloudy', 'look': 'center'}

def scene_frame_day2(weather,pose,center_x,caption=None,prop='cold',fire_phase=0,show_title=True):
    img=background(weather,include_nest=False,cloudy_bucket=(prop=='water'),close_door=False)
    d=ImageDraw.Draw(img,'RGBA')
    draw_wet_puddles(d)
    draw_roof_drips(d)
    if prop=='broken':
        draw_broken_fence(d)
    elif prop=='water':
        draw_bucket(d,1016,390,0.95,cloudy=True)
        line(d,[(1010,380),(1066,380)],INK,3)
        line(d,[(1080,405),(1095,405)],(233,236,222,255),2)
    elif prop=='wood':
        draw_dry_wood(d)
    elif prop in ('fire','fire_hold'):
        # background kindling and pot; avatar is composited afterward in front of the prop.
        draw_fire_pot(d,780,425,phase=fire_phase,steam=(prop=='fire_hold'))
    place_character(img,pose,center_x)
    if prop=='cold':
        # Small shiver marks beside the shoulders; the mouth remains closed.
        line(d,[(420,305),(432,297),(423,289)],(230,241,240,255),3)
        line(d,[(791,320),(803,312),(794,304)],(230,241,240,255),3)
    if prop=='broken':
        # subtle inspection rays beside the snapped rail
        line(d,[(818,441),(809,434)],(237,237,220,255),3)
        line(d,[(821,454),(809,454)],(237,237,220,255),3)
    if prop in ('fire','fire_hold'):
        # keep the pot visibly just in front of the hand/body while the flame stays low
        draw_fire_pot(d,780,425,phase=fire_phase,steam=(prop=='fire_hold'))
    if show_title: title_badge(img)
    subtitle(img,caption)
    return img



# ---------------------------------------------------------------- motion -------
# Everything below is the merge layer: the farm panel stays exactly as drawn,
# these add the movement and camera language a 45-50s house-format part needs.

LOOK_SHIFT = {'down': (0.16, 1.02), 'up': (0.16, 0.99), 'right': (0.05, 1.03), 'left': (0.27, 1.03)}

def camera_look(img, look, env=None):
    """Ken-Burns style reframe (mirrors the factory's zoompan rule: +14%/-14% alternating)."""
    dx, zoom = LOOK_SHIFT.get(look, (0.16, 1.0))
    if env and 'zoom' in env:
        zoom = env['zoom']
    w, h = img.size
    nx, ny = int(w * zoom), int(h * zoom)
    big = img.resize((nx, ny), Image.Resampling.LANCZOS)
    cx, cy = int(nx * dx), int(ny * 0.5)
    x0 = max(0, min(nx - w, cx - w // 2)); y0 = max(0, min(ny - h, cy - h // 2))
    return big.crop((x0, y0, x0 + w, y0 + h))

def env_overlay(img, env):
    """rain streaks, wind-blown grass, fire embers — all deterministic from env['f']."""
    d = ImageDraw.Draw(img, 'RGBA')
    f = env.get('f', 0)
    if env.get('rain'):
        span = H + 120
        frames = max(1, env.get('n', 1))
        for i in range(34):
            x = (i * 53 + f * 11) % (W + 120) - 60
            y = (i * 97 + f * 34) % span - 60
            line(d, [(x, y), (x - 9, y + 34)], (198, 219, 232, 150), 2)
        # droplet splashes on the ground, cycling every ~0.4s
        for k, (bx, by) in enumerate([(150, 1120), (300, 1180), (470, 1090), (560, 1210)]):
            ph = (f + k * 5) % 12
            if ph < 5:
                r = 4 + ph * 2
                d.ellipse((bx - r, by - r * 0.45, bx + r, by + r * 0.45),
                          outline=(198, 219, 232, 170), width=2)
    if env.get('embers'):
        for i in range(10):
            x = env.get('ex', 575) + (i * 13 % 60) - 30 + math.sin(f * 0.3 + i) * 6
            y = env.get('ey', 880) - (f * 2 + i * 11) % 90
            d.ellipse((x, y, x + 4, y + 4), fill=(255, 196, 92, 210))
        flicker = 1.0 + 0.10 * math.sin(f * 1.9) + 0.06 * math.sin(f * 3.3)
        d.ellipse((520, 900, 660, 1010), fill=(255, 186, 96, int(46 * flicker)))
    if env.get('wind'):
        for (sx, sy) in [(60, 700), (180, 860), (640, 760), (540, 980)]:
            off = (f * 6) % 40
            line(d, [(sx + off, sy), (sx + off + 26, sy - 6)], (111, 155, 91, 190), 3)
        # drifting cloud shading so the sky is never dead still
        sway = 6 * math.sin(f * 0.12)
        d.ellipse((455 + sway, 88, 525 + sway, 108), fill=(214, 219, 214, 120))
        d.ellipse((120 - sway, 140, 190 - sway, 158), fill=(219, 223, 217, 110))
    return img

def rain_puddles(img, strength=1.0):
    d = ImageDraw.Draw(img, 'RGBA')
    for box in [(120, 1150, 250, 1176), (430, 1120, 600, 1150), (250, 1215, 400, 1238)]:
        d.ellipse(box, fill=(120, 170, 190, int(90 * strength)), outline=(86, 132, 150, 200), width=2)
    return img
