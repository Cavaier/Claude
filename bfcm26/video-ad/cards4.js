// Video ad lockups: one headline size + one sub-line size in every scene, white only, wordmark on the closing scene only.
// Usage: node cards4.js <assets dir> <out dir> <spec.json>
// spec.json: { "<name>": { "top": <px>, "head": "...", "sub": "...", "logo": true (closing scene only) } }
const { chromium } = require(process.env.PW);
const fs = require('fs');
const [A, OUT, specFile] = process.argv.slice(2);
const spec = JSON.parse(fs.readFileSync(specFile));
const b64 = f => fs.readFileSync(`${A}/${f}`).toString('base64');
const font = w => `@font-face{font-family:F;font-weight:${w};src:url(data:font/ttf;base64,${b64(`Figtree-${w}.ttf`)})}`;
// House rules (Eli): white text only, logo once (closing scene), one consistent type size set.
const LOGO_H = 28;   // wordmark letters = headline cap height (38px Figtree caps are ~27px)
const HEAD = 38;     // headline size, identical in every scene
const SUB = 17;      // sub-line size, identical in every scene
const ink = '#ffffff';
const logo = `data:image/png;base64,${b64('logo_white.png')}`;
const glow = 'drop-shadow(0 2px 14px rgba(0,0,0,.28))';
const css = `${font(300)}${font(400)}
html,body{margin:0;width:1080px;height:1920px;background:transparent;font-family:F;color:${ink}}
.lock{position:absolute;left:0;right:0;display:flex;flex-direction:column;align-items:center;text-align:center;filter:${glow}}
.logo{display:block;height:${LOGO_H}px;margin-bottom:26px}
.head{font-weight:300;font-size:${HEAD}px;line-height:1.15;letter-spacing:.18em;padding-left:.18em;text-transform:uppercase}
.sub{font-weight:400;font-size:${SUB}px;letter-spacing:.32em;padding-left:.32em;text-transform:uppercase;margin-top:14px;opacity:.92}
`;
// Every scene uses the same two sizes: a headline + a sub-line (always both). The logo appears only on the closing scene.
const html = s => `${s.logo ? `<img class="logo" src="${logo}">` : ''}<div class="head">${s.head}</div>${s.sub ? `<div class="sub">${s.sub}</div>` : ''}`;
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
