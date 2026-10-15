// Render transparent 1080x1920 overlay PNGs (captions, lockups, end cards) for imitation video ads.
// Usage: PW=<playwright> node ovl.js <assets dir> <out dir> <spec.json>
// spec.json: { "css": "<extra css>", "items": { "<name>": "<html>" , ... } }
// Fonts: Figtree 300/400 as F; logo available as {{LOGO}} (white) — use class .logo-dark to make it black.
const { chromium } = require(process.env.PW);
const fs = require('fs');
const [A, OUT, specFile] = process.argv.slice(2);
const spec = JSON.parse(fs.readFileSync(specFile));
const b64 = f => fs.readFileSync(`${A}/${f}`).toString('base64');
const font = w => `@font-face{font-family:F;font-weight:${w};src:url(data:font/ttf;base64,${b64(`Figtree-${w}.ttf`)})}`;
const LOGO = `data:image/png;base64,${b64('logo_white.png')}`;
const css = `${font(300)}${font(400)}
html,body{margin:0;width:1080px;height:1920px;background:transparent;font-family:F;color:#fff;position:relative;overflow:hidden}
.logo-dark{filter:invert(1)}
${spec.css || ''}`;
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const [k, h] of Object.entries(spec.items)) {
    await p.setContent(`<style>${css}</style>${h.replaceAll('{{LOGO}}', LOGO)}`, { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(150);
    await p.screenshot({ path: `${OUT}/${k}.png`, omitBackground: true });
  }
  await b.close();
})();
