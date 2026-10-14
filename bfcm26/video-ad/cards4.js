// Luxury-minimal lockups: Bodoni wordmark, thin large offer numerals, small tracked labels.
// Usage: node cards4.js <assets dir> <out dir> <light|dark> <spec.json>
// spec.json: { "<name>": { "kind": "logo|offer|line|end", "top": <px>, ... } }
const { chromium } = require(process.env.PW);
const fs = require('fs');
const [A, OUT, tone, specFile] = process.argv.slice(2);
const spec = JSON.parse(fs.readFileSync(specFile));
const b64 = f => fs.readFileSync(`${A}/${f}`).toString('base64');
const font = w => `@font-face{font-family:F;font-weight:${w};src:url(data:font/ttf;base64,${b64(`Figtree-${w}.ttf`)})}`;
// House rules (Eli): logo always 17px tall; text sizes are the 30%-reduced set below.
const LOGO_H = 17;
const ink = tone === 'dark' ? '#1d1d1b' : '#ffffff';
const logo = `data:image/png;base64,${b64(tone === 'dark' ? 'logo_dark.png' : 'logo_white.png')}`;
const glow = tone === 'dark' ? 'drop-shadow(0 0 18px rgba(255,255,255,.45))' : 'drop-shadow(0 2px 14px rgba(0,0,0,.28))';
const css = `${font(300)}${font(400)}
html,body{margin:0;width:1080px;height:1920px;background:transparent;font-family:F;color:${ink}}
.lock{position:absolute;left:0;right:0;display:flex;flex-direction:column;align-items:center;text-align:center;filter:${glow}}
.logo{display:block}
.label{font-weight:400;font-size:20px;letter-spacing:.34em;padding-left:.34em;text-transform:uppercase}
.big{font-weight:300;font-size:92px;line-height:1;letter-spacing:.02em;text-transform:uppercase;margin-top:16px}
.mid{font-weight:300;font-size:32px;letter-spacing:.16em;padding-left:.16em;text-transform:uppercase}
.rule{width:40px;height:1px;background:${ink};opacity:.7;margin:21px 0}
`;
const html = s => {
  const L = () => `<img class="logo" src="${logo}" style="height:${LOGO_H}px">`;
  switch (s.kind) {
    case 'logo': return L();
    case 'offer': return `<div class="label">${s.label || 'Black Friday'}</div><div class="big">${s.big || '30% off'}</div>`;
    case 'line': return `<div class="mid">${s.text}</div>${s.sub ? `<div class="label" style="margin-top:13px;font-size:15px">${s.sub}</div>` : ''}`;
    case 'end': return `${L()}<div class="rule"></div><div class="label">${s.label || 'Black Friday'}</div><div class="mid" style="margin-top:11px">${s.text || '30% off sitewide'}</div>${s.sub ? `<div class="label" style="margin-top:14px;font-size:15px;opacity:.85">${s.sub}</div>` : ''}`;
  }
};
(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const [k, s] of Object.entries(spec)) {
    await p.setContent(`<style>${css}</style><div class="lock" style="top:${s.top}px">${html(s)}</div>`, { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(200);
    await p.screenshot({ path: `${OUT}/${k}.png`, omitBackground: true });
  }
  await b.close();
})();
