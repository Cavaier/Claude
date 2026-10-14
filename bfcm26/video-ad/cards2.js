// Minimal text overlays in the Vacier layout: small wordmark at mid-height, one tiny tracked line.
const { chromium } = require(process.env.PW);
const fs = require('fs');
const A = process.argv[2];
const b64 = f => fs.readFileSync(`${A}/${f}`).toString('base64');
const font = w => `@font-face{font-family:F;font-weight:${w};src:url(data:font/ttf;base64,${b64(`Figtree-${w}.ttf`)})}`;
const logo = `data:image/png;base64,${b64('logo_white.png')}`;
const base = `${font(400)}${font(500)}
html,body{margin:0;width:1080px;height:1920px;background:transparent;font-family:F;color:#fff}
.mid{position:absolute;left:0;right:0;top:900px;display:flex;flex-direction:column;align-items:center;text-align:center;
  filter:drop-shadow(0 1px 6px rgba(0,0,0,.35))}
.logo{width:150px}
.line{margin-top:18px;font-weight:500;font-size:21px;letter-spacing:.42em;text-transform:uppercase;padding-left:.42em}
.small{margin-top:10px;font-weight:400;font-size:17px;letter-spacing:.36em;text-transform:uppercase;padding-left:.36em;opacity:.9}
`;
const card = (line, small = '', top = 900) => `<div class="mid" style="top:${top}px"><img class="logo" src="${logo}"><div class="line">${line}</div>${small ? `<div class="small">${small}</div>` : ''}</div>`;
const cards = {
  s1: card('Black Friday', '', 1460),
  s2: card('30% off sitewide'),
  s3: card('No code needed', 'Taken off at checkout', 1360),
  s4: card('Black Friday · 30% off', 'Sitewide', 1440),
};
(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const [k, html] of Object.entries(cards)) {
    await p.setContent(`<style>${base}</style>${html}`, { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(200);
    await p.screenshot({ path: `${process.argv[3]}/${k}.png`, omitBackground: true });
  }
  await b.close();
})();
