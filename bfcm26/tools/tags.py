# tags.py file.dc.html "TEXT|color" ... : replaces the status tag stack (top-left) on an artboard.
# colors: yellow (draft), blue (working), green (done). The stack carries data-tag="status" so exports skip it.
import sys,re
C={'yellow':'#F4D58A','blue':'#9DBBE3','green':'#8FCBA2','grey':'#DCDCDA'}
f=sys.argv[1]; s=open(f).read()
s=re.sub(r'<div data-tag="status".*?</div>\n?','',s,flags=re.S)
s=re.sub(r'<span data-status="[a-z]+"[^>]*>[^<]*</span>\n?','',s)
items=[]
for a in sys.argv[2:]:
    t,c=a.rsplit('|',1)
    items.append(f'<span style="padding: 12px 20px; background: {C[c]}; color: #141414; font-family: Figtree, sans-serif; font-size: 28px; font-weight: 600; letter-spacing: 0.1em">{t}</span>')
stack='<div data-tag="status" style="position: absolute; top: 28px; left: 28px; z-index: 50; display: flex; flex-direction: column; align-items: flex-start; gap: 10px; pointer-events: none">'+''.join(items)+'</div>\n'
i=s.index('</helmet>'); j=s.index('>', s.index('<div', i))+1
s=s[:j]+'\n'+stack+s[j:]
if 'family=Figtree' in s and 'wght@600' not in s and '600' not in s[:s.index('</helmet>')]: pass
open(f,'w').write(s)
