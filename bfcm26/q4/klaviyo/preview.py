"""Local preview: python3 preview.py F1E1 bf W -> /tmp preview png (uses local images)."""
import sys, os, re, json
sys.path.insert(0, '..')
src = open('../gen_q4.py').read(); g = {'__file__': os.path.abspath('../gen_q4.py')}
exec(src[:src.index('# ---------------------------------------------------------------- phases')], g)
import q4_specs as q
from emailer import R
class IMG(dict):
    def __missing__(s, k):
        if k == 'logo': p = '../logo0.png'
        elif k.startswith('ic_'): p = f'../icons/{k[3:]}.png'
        else: return g['load_img'](k)
        import base64; return 'data:image/png;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
def find(eid):
    for f in q.FLOWS:
        for e in f['emails']:
            if e['id'] == eid: return f, e
if __name__ == '__main__':
    out = sys.argv[1]; items = sys.argv[2:]
    html = ''
    for it in items:
        eid, ph, gg = it.split(':')
        f, e = find(eid)
        day = next((d for d in q.DAYS if d['phase'] == ph and d['default']), None)
        r = R('EU', f['id'], IMG(), ctx=dict(phase=ph, day=day, g=gg))
        html += f'<div style="display:inline-block;vertical-align:top;margin:10px"><p style="font:14px sans-serif">{eid} {ph} {gg} · {r.subject(e)} / {r.preview(e)}</p>' + re.sub(r'^.*?<body[^>]*>|</body></html>$', '', r.email(e), flags=re.S) + '</div>'
    open(out, 'w').write('<html><body style="margin:0;background:#ddd;width:2600px">' + html + '</body></html>')
