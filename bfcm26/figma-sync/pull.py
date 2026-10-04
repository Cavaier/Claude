"""Figma -> page: keep edits people made in Figma before a sync overwrites them.
Usage: python3 pull.py <check_result.json> <page.html> <out.html>
Compares each email frame (as dumped by check.js) with what the sync last put there (manifest spec):
  - text whose characters changed  -> written onto the page (out.html), so the next sync keeps it
  - anything else changed (moved/resized layers, colours, fonts, images, layers added/removed)
                                    -> email listed under "flagged": do not sync it, ask the person
Prints a JSON report {applied:[...], flagged:{id:[reasons]}, clean:[...]} and writes it to <out.html>.report.json"""
import json, sys, os, re, html as H
HERE = os.path.dirname(os.path.abspath(__file__))
man = json.load(open(f'{HERE}/manifest.json'))
res = json.load(open(sys.argv[1])); page = open(sys.argv[2]).read()
FM = {'Figtree': {200: 'Light', 300: 'Light', 400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold'},
      'Inter': {200: 'Extra Light', 300: 'Light', 400: 'Regular', 500: 'Medium', 600: 'Semi Bold', 700: 'Bold'}}
def fname(ff, fw, it):
    s = 'Regular' if ff == 'Bodoni Moda' else (FM.get(ff) or FM['Inter']).get(fw, 'Regular')
    if it: s = 'Italic' if s == 'Regular' else s + ' Italic'
    return f'{ff}/{s}'
def far(a, b, t=1.5): return abs(a - b) > t

def diff(spec, got):
    """-> (text_changes [(old,new,occurrence)], reasons [])"""
    S, I = spec['S'], spec['I']; txt, why = [], []
    if got is None: return [], ['frame not found in Figma']
    if len(got['S']) != len(S): return [], ['sections added or removed']
    seen = {}
    for k, s in enumerate(S):
        items = [it for it in I if it[1] == k]; g = got['S'][k]
        if s[0] == 'FOOTER': continue
        if g == 'FOOTER': why.append('sections reordered'); continue
        free = list(g)   # match each built layer to a Figma layer by kind and position (layer order may change)
        for it in items:
            x, y = it[2] - s[1], it[3] - s[2]
            if it[0] == 'x':
                key = it[6].lower(); occ = seen.get(key, 0); seen[key] = occ + 1
                n = next((n for n in free if n[0] == 'x' and not far(n[1], x) and not far(n[2], y)), None)
                if n is None: why.append(f'text moved or removed: "{it[6][:30]}"'); continue
                free.remove(n)
                if n[4] != it[10] or n[5] != fname(it[7], it[8], it[9]) or (n[6] or '')[:7].lower() != it[13][:7].lower():
                    why.append(f'text style changed: "{it[6][:30]}"')
                if n[3] != it[6]: txt.append((it[6], n[3], occ))
            else:
                want = {'r': 'r', 'i': 'r', 'g': 'r', 'v': 'FRAME'}[it[0]]
                fill = 'img:' + it[6] if it[0] == 'i' else ('GRADIENT_LINEAR' if it[0] == 'g' else (it[6][:7].lower() if it[0] == 'r' and it[6] else None))
                cand = [n for n in free if n[0] == want and not far(n[1], x) and not far(n[2], y) and not far(n[3], max(.5, it[4])) and not far(n[4], max(.5, it[5]))]
                n = next((n for n in cand if it[0] == 'v' or (n[5] or None) == fill), None)
                if n is None:
                    why.append(f'{"image" if it[0]=="i" else "shape"} changed, moved or removed in "{s[0]}"'); continue
                free.remove(n)
        if free: why.append(f'layers added in "{s[0]}"')
    return txt, sorted(set(why))

def article_span(h, eid):
    sec = h.find(f'id="e{eid[1:3]}"'); end = h.find('<section', sec + 10); end = len(h) if end < 0 else end
    v = h.find(f'data-ver="{eid[3]}"', sec, end)
    if v < 0 and eid[3] == 'A': v = sec
    a = h.find('<article', v, end); b = h.find('</article>', a)
    return (a, b) if a >= 0 and b > a else None

def text_index(raw):
    """decoded, whitespace-collapsed text of raw html + map from each text char to raw (start,end)"""
    chars, spans = [], []
    for m in re.finditer(r'<[^>]*>|&[#\w]+;|\s+|[^<&\s]+', raw):
        t = m.group()
        if t.startswith('<'):
            if re.match(r'<br\b', t, re.I): chars.append(' '); spans.append((m.start(), m.end()))
            continue
        if t.startswith('&'): t = H.unescape(t).replace('\xa0', ' ')
        if t.isspace():
            if chars and chars[-1] == ' ': continue
            chars.append(' '); spans.append((m.start(), m.end())); continue
        if len(t) == m.end() - m.start():
            for j, c in enumerate(t): chars.append(c); spans.append((m.start() + j, m.start() + j + 1))
        else:
            for c in t: chars.append(c); spans.append((m.start(), m.end()))
    return ''.join(chars), spans

def recase(new, src):
    if new != new.upper() or src == src.upper(): return new
    if src == src.title(): return new.title()
    if src[:1].isupper(): return new[:1].upper() + new[1:].lower()
    return new.lower()

def apply(h, eid, old, new, occ):
    sp = article_span(h, eid)
    if not sp: return h, 'email not found on the page'
    raw = h[sp[0]:sp[1]]; text, spans = text_index(raw)
    norm = lambda s: re.sub(r'\s+', ' ', s.replace('\xa0', ' ')).strip()
    o = norm(old); hits = [m.start() for m in re.finditer(re.escape(o), text, re.I)]
    if len(hits) <= occ: return h, f'could not find "{old[:40]}" on the page'
    i = hits[occ]; a, b = spans[i][0], spans[i + len(o) - 1][1]
    seg = raw[a:b]
    if '<' in seg and not re.fullmatch(r'[^<]*(<br\s*/?>[^<]*)*', seg): return h, f'"{old[:40]}" spans styled text'
    src = text[i:i + len(o)]
    ins = H.escape(recase(new, src), quote=False).replace('\n', '<br>')
    return h[:sp[0]] + raw[:a] + ins + raw[b:] + h[sp[1]:], None

rep = {'applied': [], 'flagged': {}, 'clean': []}
for eid, got in res.items():
    if eid not in man or 'spec' not in man[eid]: continue
    txt, why = diff(man[eid]['spec'], got)
    if why: rep['flagged'][eid] = why; continue          # leave the whole frame alone
    if not txt: rep['clean'].append(eid); continue
    trial, errs = page, []
    for old, new, occ in txt:
        trial, err = apply(trial, eid, old, new, occ)
        if err: errs.append(err)
    if errs: rep['flagged'][eid] = errs; continue
    page = trial; rep['applied'] += [{'email': eid, 'old': o, 'new': n} for o, n, _ in txt]
open(sys.argv[3], 'w').write(page)
json.dump(rep, open(sys.argv[3] + '.report.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps(rep, ensure_ascii=False, indent=1))
