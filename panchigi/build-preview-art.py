"""Compose existing approved PanChigi art. Requires Pillow; run with client root.
python panchigi/build-preview-art.py C:/home/Panchigi/.utmp/worktrees/friend-invite-link
No network, new illustration, interface copy or code-drawn art is used.
"""
from pathlib import Path
import sys, hashlib, json
from PIL import Image, ImageOps
root=Path(sys.argv[1]); assets=Path(__file__).parent/'join/assets'
provenance=json.loads((Path(__file__).parent/'art-provenance.json').read_text(encoding='utf-8'))
images={}
for record in provenance['inputs']:
    source=root/record['clientPath']
    assert hashlib.sha256(source.read_bytes()).hexdigest()==record['sha256'],source
    images[record['role']]=Image.open(source).convert('RGBA')
def panel(size):
    # Nine slices preserve the imported paper edge/corner artwork.
    source=images['paper']; w,h=source.size; out=Image.new('RGBA',size); d=48; s=72
    sx=[0,s,w-s,w]; sy=[0,s,h-s,h]; dx=[0,d,size[0]-d,size[0]]; dy=[0,d,size[1]-d,size[1]]
    for y in range(3):
        for x in range(3):
            patch=source.crop((sx[x],sy[y],sx[x+1],sy[y+1])).resize((dx[x+1]-dx[x],dy[y+1]-dy[y]),Image.Resampling.LANCZOS)
            out.alpha_composite(patch,(dx[x],dy[y]))
    return out
def paste(out,role,box,crop=None):
    source=images[role]
    if crop:source=source.crop(crop)
    source=ImageOps.contain(source,box[2:],Image.Resampling.LANCZOS)
    out.alpha_composite(source,(box[0],box[1]))
def save(out,name):
    # Bounded palette keeps the public PNG below 300KB without an external optimizer.
    out.convert('RGB').quantize(colors=192,method=Image.Quantize.MEDIANCUT).save(assets/name,optimize=True)
    if name.startswith('invite-'): assert (assets/name).stat().st_size<300000,name
for size,name in [((1200,630),'invite-1200x630.png'),((600,600),'invite-600x600.png')]:
    out=ImageOps.fit(images['background'],size,Image.Resampling.LANCZOS)
    inset=20 if size[0]==600 else 26
    out.alpha_composite(panel((size[0]-inset*2,size[1]-inset*2)),(inset,inset))
    if size[0]==1200:
        paste(out,'mongi',(190,100,375,480),(0,0,1024,1370))
        paste(out,'logo',(510,76,510,288))
        paste(out,'heads',(650,360,180,180));paste(out,'tails',(840,398,140,140))
    else:
        paste(out,'logo',(90,35,420,237));paste(out,'mongi',(110,230,290,350),(0,0,1024,1250))
        paste(out,'heads',(364,343,142,142));paste(out,'tails',(431,455,98,98))
    save(out,name)
# Page background/paper and brand mark are derivatives of the same declared inputs.
save(ImageOps.fit(images['background'],(720,1280),Image.Resampling.LANCZOS),'background.png')
save(panel((720,960)),'paper.png')
images['logo'].resize((440,248),Image.Resampling.LANCZOS).save(assets/'logo.png',optimize=True)
icon=ImageOps.fit(images['mongi'].crop((220,0,870,650)),(180,180),Image.Resampling.LANCZOS)
icon.save(assets/'apple-touch-icon.png',optimize=True)
icon.resize((32,32),Image.Resampling.LANCZOS).save(assets/'favicon.png',optimize=True)
