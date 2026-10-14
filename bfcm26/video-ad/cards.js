// Renders transparent 1080x1920 text overlays for the ad.
// Safe zone: key text kept between y=270 and y=1536.
const { chromium } = require(process.env.PW);
const A = process.argv[2]; // assets dir
const fs = require('fs');
const b64 = f => fs.readFileSync(`${A}/${f}`).toString('base64');
const font = w => `@font-face{font-family:F;font-weight:${w};src:url(data:font/ttf;base64,${b64(`Figtree-${w}.ttf`)})}`;
const base = `${font(300)}${font(400)}${font(500)}
html,body{margin:0;width:1080px;height:1920px;background:transparent;font-family:F;color:#fff}
.wrap{position:absolute;left:80px;right:80px;display:flex;flex-direction:column;align-items:center;text-align:center}
.label{font-weight:500;font-size:34px;letter-spacing:.1em;text-transform:uppercase}
.pill{background:#A82C24;padding:16px 28px 14px}
h1{margin:0;font-weight:400;text-transform:uppercase;line-height:.95;text-shadow:0 4px 30px rgba(0,0,0,.35)}
.sub{font-weight:400;font-size:38px;margin-top:26px;text-shadow:0 2px 16px rgba(0,0,0,.45)}
.shade{position:absolute;left:0;right:0;height:900px;background:linear-gradient(rgba(0,0,0,.38),rgba(0,0,0,0))}
`;
const cards = {
  hook: `<div class="shade" style="top:0"></div>
    <div class="wrap" style="top:330px"><div class="label pill">Black Friday</div>
    <h1 style="font-size:190px;margin-top:40px">30% off<br>sitewide</h1></div>`,
  pool: `<div class="shade" style="top:0"></div>
    <div class="wrap" style="top:360px"><h1 style="font-size:92px;white-space:nowrap">Gold that goes<br>in the pool</h1>
    <div class="sub">Waterproof. Sweat and heat resistant.</div></div>`,
  steel: `<div class="shade" style="top:0"></div>
    <div class="wrap" style="top:360px"><div class="label">Recycled 316L</div>
    <h1 style="font-size:112px;margin-top:22px">Stainless<br>steel</h1></div>`,
  fit: `<div class="shade" style="top:0"></div>
    <div class="wrap" style="top:360px"><div class="label">Adjustable S / M / L</div>
    <h1 style="font-size:100px;margin-top:22px">Black, silver<br>or gold</h1></div>`,
  reviews: `<div class="shade" style="top:0"></div>
    <div class="wrap" style="top:360px"><div class="label">Trustpilot 4.5 &#9733;</div>
    <h1 style="font-size:112px;margin-top:22px">3,000+<br>reviews</h1></div>`,
  end: `<div style="position:absolute;inset:0;background:rgba(0,0,0,.45)"></div>
    <div class="wrap" style="top:560px">
    <img src="data:image/png;base64,${b64('logo_white.png')}" style="width:560px">
    <div class="label pill" style="margin-top:90px">Black Friday</div>
    <h1 style="font-size:150px;margin-top:36px">30% off<br>sitewide</h1>
    <div class="sub" style="margin-top:40px">No code needed. Taken off at checkout.</div>
    <div class="label" style="margin-top:70px;font-size:30px;border:2px solid #fff;padding:18px 34px 16px">Shop now</div></div>`,
};
(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox', '--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const [k, html] of Object.entries(cards)) {
    await p.setContent(`<style>${base}</style>${html}`, { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(300);
    await p.screenshot({ path: `${process.argv[3]}/${k}.png`, omitBackground: true });
  }
  await b.close();
})();
