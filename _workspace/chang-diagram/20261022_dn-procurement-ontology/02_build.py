import json,sys
R=sys.argv[1]; S=json.load(open(f"{R}/01_spec.json"))
F="Pretendard, 'Malgun Gothic', sans-serif"
N={n['id']:n for n in S['nodes']}; A={a['id']:a for a in S['annotations']}
W,G,X0=248,50,80
ZT=248; HDR=ZT+36; CY=ZT+56; CH=168; AY=CY+CH+24
order=['q','onto','opt','whatif','decide']
xs={k:X0+i*(W+G) for i,k in enumerate(order)}
o=[]
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900" font-family="{F}">')
o.append('<defs><marker id="arrow" viewBox="0 0 12 12" refX="12" refY="6" markerWidth="12" markerHeight="12" markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0 L12 6 L0 12 Z" fill="#1B2A4A"/></marker></defs>')
o.append('<rect width="1600" height="900" fill="#FFFFFF"/>')
o.append(f'<g data-role="title"><text x="64" y="112" font-size="42" font-weight="700" fill="#1B2A4A">{S["headline"]}</text><text x="64" y="152" font-size="22" fill="#2C3E5A">{S["subtitle"]}</text></g>')
ZB=AY+76+24
zones=[('problem','문제 정의',64,xs['q']+W+16),('solution','솔루션',xs['onto']-16,xs['decide']+W+16)]
for gid,lab,x1,x2 in zones:
    o.append(f'<g data-group="{gid}" data-container="true"><rect data-box="true" x="{x1}" y="{ZT}" width="{x2-x1}" height="{ZB-ZT}" fill="#F5F5F7"/><text x="{x1+16}" y="{HDR}" font-size="22" font-weight="700" fill="#1B2A4A">{lab}</text></g>')
for k in order:
    n=N[k]; x=xs[k]; f=n['role']=='focal'
    fill,st,sw=('#FFF4E8','#B45309',3) if f else ('#FFFFFF','#7F8FA9',1.5)
    lines=n['sub'].split('\n')
    ts=''.join(f'<tspan x="{x+16}" y="{CY+76+i*28}">{l}</tspan>' for i,l in enumerate(lines))
    o.append(f'<g data-node="{k}"><rect data-box="true" x="{x}" y="{CY}" width="{W}" height="{CH}" rx="8" fill="{fill}" stroke="{st}" stroke-width="{sw}"/><text x="{x+16}" y="{CY+36}" font-size="20" font-weight="700" fill="#1B2A4A">{n["label"]}</text><text font-size="17" fill="#2C3E5A">{ts}</text></g>')
ym=CY+CH//2
for e in S['edges']:
    a,b=e['from'],e['to']
    o.append(f'<g data-edge="{a}->{b}"><path d="M{xs[a]+W} {ym} H{xs[b]-2}" fill="none" stroke="#1B2A4A" stroke-width="3" marker-end="url(#arrow)"/></g>')
for aid,a in A.items():
    if 'near' not in a: continue
    x=xs[a['near']]; lines=a['text'].split('\n'); h=len(lines)*24+4
    ts=''.join(f'<tspan x="{x+16}" y="{AY+24+i*24}">{l}</tspan>' for i,l in enumerate(lines))
    o.append(f'<g data-annotation="{aid}"><rect x="{x}" y="{AY}" width="3" height="{h}" fill="#7F8FA9"/><text font-size="16" fill="#2C3E5A">{ts}</text></g>')
BT=ZB+80; BH=80
o.append(f'<g data-annotation="src"><text x="64" y="{BT-20}" font-size="14" fill="#2C3E5A">{A["src"]["text"]}</text></g>')
o.append(f'<g data-role="takeaway"><rect data-box="true" x="64" y="{BT}" width="1472" height="{BH}" fill="#F5F5F7"/><rect x="64" y="{BT}" width="8" height="{BH}" fill="#1B2A4A"/><text x="800" y="{BT+48}" text-anchor="middle" font-size="22" font-weight="700" fill="#1B2A4A">{S["takeaway"]}</text></g>')
o.append('</svg>')
open(f"{R}/02_diagram_v2.svg","w").write('\n'.join(o))
print(ZB,BT)
