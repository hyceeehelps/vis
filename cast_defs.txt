"""cast_defs — the channel's PERMANENT CAST, declared once.

Every recurring character lives here: colours, skin, hat, silhouette seed, default
expression. Scenes must call `cast_engine.char(d, 'name', ...)` and may only vary
pose / expression / position / size — never identity.

    python3 cast_sheet.py      # regenerate cast_sheet.png after any edit here

Adding someone new? Append a define() line, run cast_sheet.py, eyeball the sheet,
then use the name in scenes. Names are lowercase, no spaces.
"""
from cast_engine import define

# ── Episode 19/20 — the Bubble era (first cast, seeded from the shipped builds) ──
define('law',    body=(70, 110, 180), skin=(255, 251, 240), hat='wig',
       hatcol=(64, 46, 36), face='cool', seed=4101)
define('regent', body=(28, 40, 78), hat='tricorne', hatcol=(24, 26, 34),
       trim=(240, 196, 60), seed=4102)
define('newton', body=(92, 76, 60), hat='wig', hatcol=(214, 210, 200), seed=4103)
define('director', body=(46, 44, 52), hat='tophat', hatcol=(22, 22, 26),
       trim=(150, 150, 158), seed=4104)
define('clerk',  body=(150, 120, 90), hat='cap', hatcol=(90, 96, 110), seed=4105)
define('duchess', body=(196, 88, 140), hat='bonnet', hatcol=(240, 232, 214), seed=4106)
define('sailor', body=(58, 92, 128), hat='cap', hatcol=(240, 240, 236), seed=4107)
define('soldier', body=(150, 40, 44), hat='shako', hatcol=(30, 32, 40), seed=4108)
define('merchant', body=(146, 114, 80), hat='tricorne', hatcol=(60, 48, 40), seed=4109)
define('emperor', body=(206, 170, 74), hat='tricorne', hatcol=(30, 30, 36),
       trim=(120, 30, 34), seed=4110)
define('admiral', body=(58, 58, 64), hat='tricorne', hatcol=(24, 26, 34),
       trim=(240, 196, 60), seed=4111)
define('merchant2', body=(146, 114, 80), hat='furcap', seed=4112)

# ── generic crowd members — rotate these for background extras ──
define('villager', body=(120, 124, 130), hat='cap', hatcol=(80, 84, 92), seed=4201)
define('villager2', body=(104, 128, 104), hat='bonnet', hatcol=(232, 226, 206), seed=4202)
define('crowd', body=(96, 96, 102), seed=4203)
