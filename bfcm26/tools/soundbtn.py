# python3 soundbtn.py file.dc.html ... : adds a SOUND ON/OFF button (bottom right) to a video artboard.
# The board also needs "is_interactive": true in canvas.json; the viewer presses Play, then the button.
import re, sys
BTN = ('<button type="button" data-tag="sound" onClick="{{ toggleSound }}" aria-label="{{ soundLabel }}" '
       'style="position: absolute; right: 48px; bottom: 200px; z-index: 60; height: 120px; padding: 0 44px; '
       'border: 0; background: #FFFFFF; color: #141414; font-family: Figtree, sans-serif; font-size: 40px; '
       'font-weight: 600; letter-spacing: 0.1em; cursor: pointer; box-shadow: 0 8px 24px rgba(20,20,20,0.25)">{{ soundLabel }}</button>\n')
LOGIC = '''class Component extends DCLogic {
  renderVals() {
    const on = !!(this.state && this.state.soundOn);
    return {
      soundLabel: on ? 'SOUND ON' : 'SOUND OFF',
      toggleSound: (e) => {
        const root = e.currentTarget.parentElement;
        const v = root && root.querySelector('video');
        const next = !on;
        if (v) { v.muted = !next; if (next) { v.currentTime = 0; v.play(); } }
        this.setState({ soundOn: next });
      }
    };
  }
}'''
for f in sys.argv[1:]:
    h = open(f).read()
    if 'data-tag="sound"' not in h:
        h = re.sub(r'(<video [^>]*></video>\n)', r'\1' + BTN.replace('\\', '\\\\'), h, count=1)
    h = re.sub(r'class Component extends DCLogic \{.*?\n\}', LOGIC, h, count=1, flags=re.S)
    open(f, 'w').write(h)
    print(f, 'ok' if 'data-tag="sound"' in h else 'NO VIDEO')
