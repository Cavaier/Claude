"""Q4 emails -> email-safe Klaviyo HTML (tables, inline styles).
render(e, flow, acct, ctx=None): ctx=None emits Klaviyo template logic (date phase + Gender);
ctx=dict(phase=, day=, g='W'|'M') resolves it locally for previews."""
import re, html as H, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from q4_specs import DAYS, KEYS

ORDER = ['pre', 'ea', 'bf', 'cw', 'xmas', 'late', 'post']
CUT = '2026-12-18'  # first "last minute" day = day after the Christmas cut-off [placeholder until the CEO confirms]
PR = {'pre': (None, '2026-11-23'), 'ea': ('2026-11-23', '2026-11-27'), 'bf': ('2026-11-27', '2026-12-01'), 'cw': ('2026-12-01', '2026-12-07'),
      'xmas': ('2026-12-07', CUT), 'late': (CUT, '2026-12-25'), 'post': ('2026-12-25', None)}
DAYRANGE = {'x1': ('2026-12-07', '2026-12-14'), 'x2': ('2026-12-14', '2026-12-17'), 'x3': ('2026-12-17', CUT), 'l1': (CUT, '2026-12-24')}
FONT = "'Figtree','Helvetica Neue',Helvetica,Arial,sans-serif"
SERIF = "'Bodoni Moda',Didot,'Bodoni 72',Georgia,serif"
BLACK, WHITE, FOG, FOG2, GREY, LINE, INK2, RED = '#0B0B0B', '#FFFFFF', '#F2F2F1', '#E8E8E6', '#8B8B88', '#DCDCDA', '#3A3A38', '#A82C24'
GEN_IF = "{% if person|lookup:'Gender' == 'Men' %}"

class R:
    def __init__(self, acct, flow, imgurl, ctx=None):
        self.acct, self.flow, self.IMG, self.ctx = acct, flow, imgurl, ctx
        self.base = 'https://cavaier.com' if acct == 'EU' else 'https://us.cavaier.com'

    # ---------------- logic helpers
    def cond(self, phases):
        ps = [p for p in ORDER if p in phases]
        if len(ps) == len(ORDER): return None
        runs, cur = [], []
        for p in ORDER:
            if p in ps: cur.append(p)
            elif cur: runs.append(cur); cur = []
        if cur: runs.append(cur)
        parts = []
        for r in runs:
            a, b = PR[r[0]][0], PR[r[-1]][1]
            c = ' and '.join(x for x in [f"d >= '{a}'" if a else '', f"d < '{b}'" if b else ''] if x)
            parts.append(c)
        return ' or '.join(parts)
    def when(self, phases, body):
        if not body: return ''
        if self.ctx: return body if self.ctx['phase'] in phases else ''
        c = self.cond(phases)
        return body if not c else '{% if ' + c + ' %}' + body + '{% endif %}'
    def gender(self, w, m):
        if self.ctx: return m if self.ctx['g'] == 'M' else w
        if w == m: return w
        return GEN_IF + m + '{% else %}' + w + '{% endif %}'
    def tok(self, name):
        if self.ctx:
            d = self.ctx['day']; return d.get(name, '') if d else ''
        out, first = '', True
        for d in DAYS:
            v = d.get(name, '')
            if not v or d['phase'] in ('pre', 'post'): continue
            if re.fullmatch(r'\d{4}-\d\d-\d\d', d['id']): c = f"d == '{d['id']}'"
            elif d['id'] in DAYRANGE: a, b = DAYRANGE[d['id']]; c = f"d >= '{a}' and d < '{b}'"
            else: continue
            out += ('{% if ' if first else '{% elif ') + c + ' %}' + H.escape(v, quote=False); first = False
        return out + '{% endif %}' if out else ''
    def t(self, v):
        if v is None: return ''
        if isinstance(v, str):
            if getattr(self, '_plain', False): v = re.sub(r'<[^>]+>', '', v).replace('&nbsp;', ' ')
            s = re.sub(r'«(\w+)»', lambda m: self.tok(m.group(1)), v)
            return s.replace('class="red"', f'style="color:{RED}"')
        if set(v) <= {'W', 'M'}: return self.gender(self.t(v.get('W', '')), self.t(v.get('M', '')))
        if self.ctx:
            for k, val in v.items():
                if self.ctx['phase'] in k.split(): return self.t(val)
            return ''
        out, first = '', True
        for k, val in v.items():
            c = self.cond(k.split()) or 'True'
            out += ('{% if ' if first else '{% elif ') + c + ' %}' + self.t(val); first = False
        return out + '{% endif %}'
    def plain(self, v):  # subject / preview text: strip markup from the copy, keep the logic
        self._plain = True
        try: return self.t(v)
        finally: self._plain = False

    # ---------------- links and images
    def shop(self): return self.gender(f'{self.base}/collections/for-her', f'{self.base}/collections/for-him')
    def link(self, label=''):
        f, L = self.flow, re.sub(r'<[^>]+>', '', str(label)).lower()
        if 'gift card' in L or 'send the link' in L or 'send a gift' in L: return f'{self.base}/products/cavaier-gift-card'
        if f == 'F5': return '{{ event.extra.checkout_url|default:"' + self.base + '/cart" }}'
        if f == 'F4' and ('cart' in L or 'yours' in L or 'finish' in L or 'it now' in L): return self.base + '/cart'
        if f in ('F2', 'F4') and ('it' in L.split() or 'shop it' in L or 'back to' in L): return '{{ event.URL|default:"' + self.base + '" }}'
        if f == 'F9': return '{{ event.URL|default:"' + self.base + '" }}'
        if 'set' in L: return self.gender(f'{self.base}/collections/womens-sets', f'{self.base}/collections/mens-sets')
        return self.shop()
    def img(self, k, w=600, style=''):
        if isinstance(k, dict): return self.gender(self.img(k['W'], w, style), self.img(k['M'], w, style))
        return f'<img src="{self.IMG[k]}" width="{w}" alt="" style="display:block;width:100%;max-width:{w}px;height:auto;border:0;{style}">'

    # ---------------- building blocks
    def row(self, inner, pad='0 24px', bg=None):
        return f'<tr><td style="padding:{pad};{("background:" + bg + ";") if bg else ""}">{inner}</td></tr>'
    def lab(self, v, red=True, size=10):
        return f'<div style="font:500 {size}px/1.5 {FONT};letter-spacing:2px;text-transform:uppercase;color:{RED if red else GREY}">{self.t(v)}</div>'
    def btn(self, label, href=None):
        href = href or self.link(label)
        return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center"><tr><td style="background:{BLACK}">'
                f'<a href="{href}" style="display:inline-block;padding:18px 34px;font:500 11px/1 {FONT};letter-spacing:2.2px;text-transform:uppercase;color:{WHITE};text-decoration:none">{self.t(label)}</a></td></tr></table>')
    def proof(self):
        return f'<div style="margin-top:12px;font:400 11px/1.5 {FONT};letter-spacing:.6px;color:{INK2}">&#9733;&#9733;&#9733;&#9733;&#9733;&nbsp; Rated 4.5 on Trustpilot &middot; 3,000+ reviews</div>'
    def cols(self, cells, gap=12):
        n = len(cells); w = f'{100 / n:.2f}%'
        tds = ''.join(f'<td width="{w}" valign="top" style="padding:0 {gap // 2}px">{c}</td>' for c in cells)
        return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>{tds}</tr></table>'

    # ---------------- modules
    def m_headline(self, m):
        al = 'left' if m.get('align') == 'left' else 'center'
        fs = {'xl': '56px/0.98', 'm': '28px/1.12'}.get(m.get('size'), '38px/1.06')
        fw = 200 if m.get('size') == 'xl' else 300
        o = (self.lab(m['kicker']) + '<div style="height:14px"></div>') if m.get('kicker') else ''
        o += f'<h1 style="margin:0;font:{fw} {fs} {FONT};letter-spacing:-1px;color:{BLACK}">{self.t(m["title"])}</h1>'
        if m.get('sub'): o += f'<p style="margin:14px 0 0;font:300 15px/1.6 {FONT};color:{INK2}">{self.t(m["sub"])}</p>'
        if m.get('cta'): o += '<div style="height:22px"></div>' + self.btn(m['cta'])
        return self.row(f'<div style="text-align:{al}">{o}</div>', '44px 32px 0')
    def m_big_type(self, m):
        o = self.lab(m['kicker']) if m.get('kicker') else ''
        o += f'<div style="font:200 120px/0.9 {FONT};letter-spacing:-6px;color:{BLACK};margin:8px 0 6px">{self.t(m["big"])}</div>'
        if m.get('title'): o += f'<h2 style="margin:0;font:300 28px/1.12 {FONT};letter-spacing:-.5px;color:{BLACK}">{self.t(m["title"])}</h2>'
        if m.get('sub'): o += f'<p style="margin:10px 0 0;font:300 14.5px/1.6 {FONT};color:{INK2}">{self.t(m["sub"])}</p>'
        return self.row(f'<div style="text-align:center">{o}</div>', '48px 24px 0')
    def m_hero_photo(self, m):
        full = m.get('shape', 'inset') != 'inset'
        o = self.img(m['img'], 600 if full else 552)
        if m.get('caption'): o += f'<p style="margin:8px 0 0;text-align:right;font:italic 300 11px/1.4 {FONT};color:{GREY}">{self.t(m["caption"])}</p>'
        return self.row(o, '32px 0 0' if full else '32px 24px 0')
    def m_split(self, m):
        txt = (self.lab(m['kicker']) if m.get('kicker') else '') + \
              f'<h3 style="margin:8px 0 10px;font:300 24px/1.12 {FONT};color:{BLACK}">{self.t(m["title"])}</h3><p style="margin:0;font:300 13.5px/1.55 {FONT};color:{INK2}">{self.t(m["body"])}</p>'
        if m.get('cta'): txt += f'<p style="margin:14px 0 0"><a href="{self.link(m["cta"])}" style="font:500 10.5px/1 {FONT};letter-spacing:1.8px;text-transform:uppercase;color:{BLACK};text-decoration:none;border-bottom:1px solid {BLACK};padding-bottom:5px">{self.t(m["cta"])} &rarr;</a></p>'
        im = f'<td width="50%" valign="middle">{self.img(m["img"], 276)}</td>'
        tx = f'<td width="50%" valign="middle" style="padding:24px">{txt}</td>'
        cells = tx + im if m.get('reverse') else im + tx
        return self.row(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border:1px solid {LINE};background:{WHITE}"><tr>{cells}</tr></table>', '36px 24px 0')
    def m_cta(self, m):
        o = self.btn(m['label'])
        if m.get('note'): o += f'<p style="margin:12px 0 0;font:300 12.5px/1.55 {FONT};color:{GREY}">{self.t(m["note"])}</p>'
        if m.get('proof'): o += self.proof()
        return self.row(f'<div style="text-align:center">{o}</div>', '30px 24px 0')
    def m_text(self, m):
        fs = {'s': '13px/1.65', 'l': '18px/1.5'}.get(m.get('size'), '15px/1.65')
        al = 'left' if m.get('align') == 'left' else 'center'
        return self.row(f'<p style="margin:0;text-align:{al};font:300 {fs} {FONT};color:{INK2}">{self.t(m["body"])}</p>', '24px 36px 0')
    def m_promise(self, m):
        return self.row(f'<p style="margin:0;padding:22px 0;border-top:1px solid {LINE};border-bottom:1px solid {LINE};text-align:center;font:300 20px/1.4 {FONT};color:{BLACK}">{self.t(m["text"])}</p>', '30px 36px 0')
    def m_timeline(self, m):
        cells = []
        for p in m['points']:
            col = RED if p.get('state') == 'end' else (GREY if p.get('state') != 'now' else BLACK)
            cells.append(f'<div style="text-align:center;font:500 9.5px/1.3 {FONT};letter-spacing:1.5px;text-transform:uppercase;color:{col}"><span style="font-size:9px">&#9679;</span><br>{self.t(p["label"])}</div>')
        return self.row(self.cols(cells, 6), '30px 24px 0')
    def m_ticket(self, m):
        cells = []
        for c in m['cells']:
            cells.append(f'<div style="text-align:center;padding:16px 4px">{self.lab(c["label"], False)}<div style="font:300 26px/1.1 {FONT};color:{RED if c.get("red") else BLACK};margin:6px 0">{self.t(c["value"])}</div>'
                         + (f'<div style="font:300 11.5px/1.3 {FONT};color:{INK2}">{self.t(c["sub"])}</div>' if c.get('sub') else '') + '</div>')
        tds = ''.join(f'<td width="{100 / len(cells):.1f}%" valign="top" style="{"border-left:1px dashed #9A9A97;" if i else ""}">{c}</td>' for i, c in enumerate(cells))
        return self.row(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border:1px solid {BLACK};background:{WHITE}"><tr>{tds}</tr></table>', '30px 24px 0')
    def m_offer_list(self, m):
        trs = ''.join(f'<tr><td style="padding:13px 0;border-bottom:1px solid {LINE};font:{"400" if i == 0 and m.get("first_red", True) else "300"} 13px/1.4 {FONT};color:{RED if i == 0 and m.get("first_red", True) else GREY}">{self.t(a)}</td>'
                      f'<td align="right" style="padding:13px 0;border-bottom:1px solid {LINE};font:300 13px/1.4 {FONT};color:{BLACK}">{self.t(b)}</td></tr>' for i, (a, b) in enumerate(m['rows']))
        return self.row(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-top:1px solid {LINE}">{trs}</table>', '30px 24px 0')
    def _bar(self, items, first_red):
        tds = ''.join(f'<td align="center" style="padding:13px 6px;{"border-left:1px solid " + LINE + ";" if i else ""}font:500 9.5px/1.35 {FONT};letter-spacing:1.4px;text-transform:uppercase;color:{RED if first_red and i == 0 else BLACK}">{self.t(x)}</td>' for i, x in enumerate(items))
        return self.row(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-top:1px solid {LINE};border-bottom:1px solid {LINE}"><tr>{tds}</tr></table>', '30px 24px 0')
    def m_offer_bar(self, m): return self._bar(m['items'], True)
    def m_usp_bar(self, m): return self._bar(m['items'], False)
    def m_section_header(self, m):
        lab = f'<td align="right" style="font:500 10px/1.5 {FONT};letter-spacing:2px;text-transform:uppercase;color:{GREY}">{self.t(m["label"])}</td>' if m.get('label') else ''
        return self.row(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-bottom:1px solid {BLACK}"><tr><td style="padding-bottom:10px;font:400 12px/1.3 {FONT};letter-spacing:1.8px;text-transform:uppercase;color:{BLACK}">{self.t(m["title"])}</td>{lab}</tr></table>', '44px 24px 0')
    def pcard(self, k, name, tag=None, href=None, fin=None):
        o = f'<a href="{href or self.shop()}" style="text-decoration:none;color:{BLACK}">{self.img(k, 270)}</a>'
        o += f'<div style="margin-top:10px;font:400 10.5px/1.35 {FONT};letter-spacing:1.6px;text-transform:uppercase;color:{BLACK}">{self.t(name)}</div>'
        if fin: o += f'<div style="margin-top:6px;font:300 11px/1.3 {FONT};color:{INK2}">{" · ".join({"k": "Black", "s": "Silver", "g": "Gold"}[f] for f in fin)}</div>'
        if tag: o += f'<div style="margin-top:6px;font:400 12px/1.3 {FONT};color:{RED}">{self.t(tag)}</div>'
        return o
    def m_product_grid(self, m):
        n = m.get('cols', 2)
        def grid(items):
            rows, cur = '', []
            for it in items:
                cur.append(self.pcard(it['img'], it['name'], it.get('tag'), fin=it.get('finish')))
                if len(cur) == n: rows += self.cols(cur) + '<div style="height:22px"></div>'; cur = []
            if cur: rows += self.cols(cur + [''] * (n - len(cur)))
            return rows
        its = m['items']
        if any(i.get('gender') for i in its):
            w = grid([i for i in its if i.get('gender') in (None, 'W')]); mm = grid([i for i in its if i.get('gender') in (None, 'M')])
            body = self.gender(w, mm)
        else: body = grid(its)
        return self.row(body, '18px 18px 0')
    def m_gift_guide(self, m):
        cells = [f'<a href="{self.shop()}" style="text-decoration:none;color:{BLACK}">{self.img(tl["img"], 270)}'
                 f'<div style="margin-top:10px;padding-bottom:8px;border-bottom:1px solid {BLACK};font:300 18px/1.1 {FONT}">{self.t(tl["label"])} <span style="float:right;font:400 11px/1.6 {FONT};color:{GREY}">{self.t(tl.get("sub")) or "&rarr;"}</span></div></a>'
                 for tl in m['tiles']]
        rows = ''.join(self.cols(cells[i:i + 2] + [''] * (2 - len(cells[i:i + 2]))) + '<div style="height:12px"></div>' for i in range(0, len(cells), 2))
        return self.row(rows, '18px 18px 0')
    DYN = {'viewed': ("{{ event.ImageURL }}", "{{ event.Name|find_replace:'Stack Set|Set' }}", None, "{{ event.Price }}"),
           'cart': ("{{ event.ImageURL }}", "{{ event|lookup:'Product Name'|find_replace:'Stack Set|Set' }}", "{{ event|lookup:'Variant Name' }}", "{{ event.Price }} {{ event|lookup:'$currency' }}"),
           'bis': ("{{ event.ImageURL }}", "{{ event.ProductName|find_replace:'Stack Set|Set' }}", None, None)}
    def m_dynamic_product(self, m):
        im, nm, var, pr = self.DYN[m['source']]
        under = {'ea': 'Members save 30%', 'bf cw': '30% off at checkout', 'xmas': 'Order by [cut-off] for Christmas', 'late': 'Or send a gift card'}
        href = '{{ event.URL }}'
        if self.ctx:  # preview stand-ins
            im = self.IMG.get('p_set_w' if self.ctx['g'] == 'W' else 'p_set_m'); nm = '3x Minimal Set'; var = var and 'Black / Medium'; pr = pr and '€94.90'
        pic = f'<a href="{href}"><img src="{im}" width="{200 if m.get("size") == "side" else 552}" alt="" style="display:block;width:100%;height:auto;border:0;background:#fff"></a>'
        txt = f'<div style="font:400 12px/1.3 {FONT};letter-spacing:1.6px;text-transform:uppercase;color:{BLACK}">{nm}</div>'
        if var: txt += f'<div style="margin-top:6px;font:300 12.5px/1.5 {FONT};color:{GREY}">{var}</div>'
        if pr: txt += f'<div style="margin-top:6px;font:400 13px/1.3 {FONT};color:{BLACK}">{pr}</div>'
        txt += f'<div style="margin-top:6px;font:400 13px/1.3 {FONT};color:{RED}">{self.t(under)}</div>'
        if m.get('size') == 'side':
            return self.row(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td width="200" valign="middle">{pic}</td><td valign="middle" style="padding-left:20px">{txt}</td></tr></table>', '30px 24px 0')
        return self.row(pic + f'<div style="padding:14px 0;border-bottom:1px solid {LINE}">{txt}</div>', '30px 24px 0')
    FEED = {'W': [('p_crystal_br', 'Crystal Bracelet'), ('p_braid_silver', 'Braid Bracelet'), ('p_crystal_neck_silver', 'Crystal Necklace')],
            'M': [('p_braid_black', 'Braid Bracelet'), ('p_cuban_neck', 'Cuban Necklace'), ('p_cube_pend', 'Cube Pendant Necklace')]}
    def m_product_feed(self, m):
        tag = {'pre post': 'Best seller', 'ea': 'Members 30% off', 'bf cw': '30% off', 'xmas': 'Gift pick', 'late': 'Gift pick'}
        n = m.get('count', 3)
        side = lambda g: self.cols([self.pcard(k, nm, tag) for k, nm in self.FEED[g][:n]], 10)
        return self.row(self.gender(side('W'), side('M')), '18px 19px 0')
    def m_order_table(self, m):
        if self.ctx:
            rows = f'<tr><td style="padding:12px 0;font:300 13px {FONT};color:{GREY}" colspan="3">[Checkout line items]</td></tr>'
        else:
            rows = ('{% for item in event.extra.line_items %}'
                    f'<tr><td width="70" style="padding:12px 0;border-bottom:1px solid {LINE}"><img src="{{{{ item.product.images.0.src }}}}" width="60" alt="" style="display:block;width:60px;height:auto;border:0"></td>'
                    f'<td style="padding:12px 12px;border-bottom:1px solid {LINE}"><div style="font:400 11.5px/1.3 {FONT};letter-spacing:1.4px;text-transform:uppercase;color:{BLACK}">{{{{ item.title|find_replace:\'Stack Set|Set\' }}}}</div>'
                    f'<div style="margin-top:4px;font:300 12.5px/1.5 {FONT};color:{GREY}">{{{{ item.variant_title }}}} &middot; Qty {{{{ item.quantity }}}}</div></td>'
                    f'<td align="right" style="padding:12px 0;border-bottom:1px solid {LINE};font:400 13px/1.3 {FONT};color:{BLACK}">{{% if item.title == "Jewelry Case" or item.title == "Schmuckkasten" %}}Included{{% else %}}{{{{ item.line_price }}}} {{{{ event.extra.presentment_currency }}}}{{% endif %}}</td></tr>'
                    '{% endfor %}'
                    f'<tr><td colspan="2" style="padding:10px 0;font:300 13px {FONT};color:{GREY}">Discount</td><td align="right" style="padding:10px 0;font:300 13px {FONT};color:{RED}">&minus;{{{{ event|lookup:\'Total Discounts\' }}}} {{{{ event.extra.presentment_currency }}}}</td></tr>'
                    f'<tr><td colspan="2" style="padding:14px 0 0;font:500 10px/1 {FONT};letter-spacing:1.6px;text-transform:uppercase;color:{BLACK}">Total</td><td align="right" style="padding:14px 0 0;font:300 30px/1 {FONT};color:{RED}">{{{{ event|lookup:\'$value\' }}}} {{{{ event.extra.presentment_currency }}}}</td></tr>')
        head = f'<tr><td colspan="2" style="padding-bottom:10px;border-bottom:1px solid {BLACK};font:400 12px {FONT};letter-spacing:1.8px;text-transform:uppercase">Your order</td><td align="right" style="padding-bottom:10px;border-bottom:1px solid {BLACK};font:500 10px {FONT};letter-spacing:2px;text-transform:uppercase;color:{GREY}">Saved</td></tr>'
        return self.row(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0">{head}{rows}</table>', '30px 24px 0')
    def m_deadline(self, m):
        return self.row(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-top:1px solid {LINE};border-bottom:1px solid {LINE}"><tr>'
                        f'<td style="padding:15px 0;font:500 9.5px/1.3 {FONT};letter-spacing:1.6px;text-transform:uppercase;color:{GREY}">{self.t(m["label"])}</td>'
                        f'<td align="right" style="padding:15px 0;font:300 22px/1 {FONT};color:{RED}">{self.t(m["value"])}</td></tr></table>', '30px 24px 0')
    def m_shipping_calendar(self, m):
        rows = m.get('rows') or [['Netherlands &amp; EU', '[cut-off date]'], ['United Kingdom', '[cut-off date]'], ['US, Canada, Australia', '[cut-off date]'], ['Rest of world', '[cut-off date]']]
        if self.acct == 'US': rows = m.get('rows') or [['United States', '[cut-off date]'], ['Canada', '[cut-off date]']]
        trs = ''.join(f'<tr><td style="padding:12px 18px;border-top:1px solid {LINE};font:300 13px/1.4 {FONT}">{self.t(a)}</td><td align="right" style="padding:12px 18px;border-top:1px solid {LINE};font:300 13px/1.4 {FONT};color:{RED}">{self.t(b)}</td></tr>' for a, b in rows)
        return self.row(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border:1px solid {LINE};background:{WHITE}"><tr><td style="padding:14px 18px;font:400 11px {FONT};letter-spacing:1.8px;text-transform:uppercase">{self.t(m.get("title", "Order by, for Christmas"))}</td><td align="right" style="padding:14px 18px;font:500 10px {FONT};letter-spacing:2px;text-transform:uppercase;color:{GREY}">Standard delivery</td></tr>{trs}</table>', '30px 24px 0')
    def m_gift_box(self, m):
        return self.row(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border:1px solid {LINE};background:{WHITE}"><tr><td width="128" style="padding:16px">{self.img(m.get("img", "p_case"), 128)}</td>'
                        f'<td valign="middle" style="padding:16px 16px 16px 2px">{self.lab(m["kicker"])}<div style="margin:6px 0;font:400 12px/1.3 {FONT};letter-spacing:1.4px;text-transform:uppercase">{self.t(m["title"])}</div><div style="font:300 13px/1.5 {FONT};color:{INK2}">{self.t(m["text"])}</div></td></tr></table>', '36px 24px 0')
    def m_gift_card(self, m):
        card = (f'<table role="presentation" width="280" cellpadding="0" cellspacing="0" align="center" style="background:{WHITE};border:1px solid {LINE}"><tr><td style="padding:18px;height:139px" valign="top">'
                f'<img src="{self.IMG["logo"]}" width="84" alt="Cavaier" style="display:block;border:0"><div style="height:80px"></div><div style="font:300 13px/1 {FONT};color:{GREY}">Gift card &middot; any amount</div></td></tr></table>')
        o = card + f'<h3 style="margin:18px 0 0;font:300 24px/1.1 {FONT};color:{BLACK}">{self.t(m["title"])}</h3><p style="margin:12px 0 18px;font:300 13.5px/1.55 {FONT};color:{INK2}">{self.t(m["text"])}</p>' + self.btn(m['cta'], f'{self.base}/products/cavaier-gift-card')
        return self.row(f'<div style="background:{FOG};padding:26px 24px 28px;text-align:center">{o}</div>', '36px 24px 0')
    def m_steps(self, m):
        cells = [f'<div style="padding:18px 6px"><div style="font:300 22px/1 {FONT};color:{GREY}">0{i + 1}</div><p style="margin:6px 0 0;font:300 12.5px/1.45 {FONT}">{self.t(x)}</p></div>' for i, x in enumerate(m['items'])]
        return self.row(f'<div style="border-top:1px solid {LINE};border-bottom:1px solid {LINE}">{self.cols(cells, 6)}</div>', '36px 24px 0')
    def m_checklist(self, m):
        trs = ''.join(f'<tr><td width="24" style="padding:11px 0;border-bottom:1px solid {LINE};color:{RED};font:500 14px {FONT}">&#10003;</td><td style="padding:11px 0;border-bottom:1px solid {LINE};font:300 14px/1.45 {FONT}">{self.t(x)}</td></tr>' for x in m['items'])
        return self.row(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-top:1px solid {LINE}">{trs}</table>', '30px 40px 0')
    def m_quote(self, m):
        who = m.get('who') or 'Name · Trustpilot'
        q = (f'<div style="border:1px dashed #BDBDBA;background:{WHITE};padding:22px 24px;text-align:center;margin-bottom:10px"><div style="font:12px {FONT};letter-spacing:2.4px">&#9733;&#9733;&#9733;&#9733;&#9733;</div>'
             f'<p style="margin:8px 0;font:300 16px/1.45 {FONT};color:{INK2}">[Verified Trustpilot review &mdash; to pull]</p><div style="font:400 11px/1.3 {FONT};color:{GREY}">{self.t(who)}</div></div>')
        return self.row(q * m.get('count', 1), '30px 24px 0')
    def m_score(self, m):
        return self.row(f'<div style="text-align:center"><div style="font:12px {FONT};letter-spacing:2.4px">&#9733;&#9733;&#9733;&#9733;&#9733;</div><div style="font:200 96px/0.9 {FONT};letter-spacing:-5px;margin:6px 0">4.5</div>{self.lab("Trustpilot · 3,000+ reviews", False)}</div>', '44px 24px 0')
    def m_faq(self, m):
        trs = ''.join(f'<tr><td style="padding:14px 0;border-bottom:1px solid {LINE}"><div style="font:400 13.5px/1.4 {FONT}">{self.t(q)}</div><div style="margin-top:6px;font:300 13px/1.55 {FONT};color:{INK2}">{self.t(a)}</div></td></tr>' for q, a in m['items'])
        return self.row(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-top:1px solid {LINE}">{trs}</table>', '30px 24px 0')
    def m_note(self, m): return ''  # mock-up notes are for the review page only
    def m_spacer(self, m): return f'<tr><td style="height:{m.get("h", 32)}px"></td></tr>'

    # ---------------- frame
    def strip(self, banner):
        def one(s):
            if ' · ' in s:
                a, b = s.split(' · ', 1); return f'<span style="color:{RED};font-weight:600">{a}</span> &middot; {b}'
            return f'<span style="color:{RED};font-weight:600">{s}</span>'
        v = one(banner) if isinstance(banner, str) else {k: one(x) for k, x in banner.items()}
        return self.row(f'<div style="text-align:center;font:500 10px/1.4 {FONT};letter-spacing:2.2px;text-transform:uppercase;color:{BLACK}">{self.t(v)}</div>', '10px 16px', WHITE) + \
            f'<tr><td style="border-bottom:1px solid {LINE};font-size:0;line-height:0">&nbsp;</td></tr>'
    def footer(self):
        ic = lambda k, url, sz: f'<a href="{url}" style="display:inline-block;padding:0 21px"><img src="{self.IMG[k]}" width="{sz}" height="{sz}" alt="" style="display:block;border:0"></a>'
        btn = lambda lab, url, on: (f'<tr><td style="padding:0 0 10px"><a href="{url}" style="display:block;padding:13px 20px;border:1px solid {"#1B1B1B" if on else "#DDDDDD"};background:{"#1B1B1B" if on else WHITE};'
                                    f'color:{WHITE if on else "#1B1B1B"};font:400 10.5px/1 {FONT};letter-spacing:.3px;text-transform:uppercase;text-decoration:none">{lab}</a></td></tr>')
        b = self.base
        return (f'<tr><td style="padding:48px 0 0"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#F1F1F1"><tr><td style="padding:31px 30px">'
                f'<div style="text-align:center;margin-bottom:19px">{ic("ic_ig", "https://www.instagram.com/cavaier/", 28)}{ic("ic_tt", "https://www.tiktok.com/@cavaier", 28)}{ic("ic_fb", "https://www.facebook.com/cavaier", 30)}</div>'
                f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0">{btn("Shop all", b + "/collections/all", True)}{btn("Bracelets", self.shop(), False)}{btn("Necklaces", self.shop(), False)}</table>'
                f'<img src="{self.IMG["logo"]}" width="80" alt="Cavaier" style="display:block;border:0;margin:28px 0 0">'
                f'<p style="margin:36px 0 0;font:400 10px/1.4 {FONT};text-transform:uppercase;color:#666">&copy; Copyright 2026 Cavaier &middot; {{{{ organization.full_address }}}}</p>'
                f'<p style="margin:10px 0 0;font:400 9px/1 {FONT};text-transform:uppercase"><a href="{{% manage_preferences_link %}}" style="color:#333;text-decoration:none">Manage preferences</a> &nbsp;|&nbsp; <a href="{{% unsubscribe_link %}}" style="color:#333;text-decoration:none">Unsubscribe</a></p>'
                '</td></tr></table></td></tr>')

    def email(self, e):
        bg = FOG if e.get('bg') == 'fog' else WHITE
        rows = self.strip(e['banner']) + self.row(f'<div style="text-align:center"><img src="{self.IMG["logo"]}" width="84" alt="Cavaier" style="display:inline-block;border:0"></div>', '24px 24px 20px') + \
            f'<tr><td style="border-bottom:1px solid {LINE};font-size:0;line-height:0">&nbsp;</td></tr>'
        for m in e['modules']:
            h = getattr(self, 'm_' + m['type'])(m)
            if m.get('gender'): h = self.gender(h if m['gender'] == 'W' else '', h if m['gender'] == 'M' else '')
            if m.get('phases'): h = self.when(m['phases'], h)
            rows += h
        rows += self.footer()
        pre = self.plain(e['preview'])
        head = ('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                '<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@200;300;400;500;600&display=swap" rel="stylesheet">'
                '<style>body{margin:0;padding:0}img{-ms-interpolation-mode:bicubic}@media (max-width:620px){.wrap{width:100%!important}}</style></head>')
        top = '' if self.ctx else "{% today '%Y-%m-%d' as d %}"
        return (head + f'<body style="margin:0;padding:0;background:{FOG2}">{top}'
                f'<div style="display:none;max-height:0;overflow:hidden">{pre}</div>'
                f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{FOG2}"><tr><td align="center" style="padding:0">'
                f'<table role="presentation" class="wrap" width="600" cellpadding="0" cellspacing="0" style="width:600px;max-width:600px;background:{bg}">{rows}</table>'
                '</td></tr></table></body></html>')
    def subject(self, e): return ("" if self.ctx else "{% today '%Y-%m-%d' as d %}") + self.plain(e['subject'])
    def preview(self, e): return ("" if self.ctx else "{% today '%Y-%m-%d' as d %}") + self.plain(e['preview'])
