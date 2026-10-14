// Usage: node walk.js <url> <out.json> <folder path joined by '/'> <first filename>
// Opens the first asset, then steps through the folder with ']' and records each asset's preview src.
const { chromium } = require(process.env.PW);
const fs = require('fs');
(async () => {
  const [url, out, folder, first] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1600, height: 1200 } });
  await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await p.waitForTimeout(3000);
  for (const f of (folder ? folder.split('/') : [])) {
    await p.getByText(f, { exact: true }).last().dblclick();
    await p.waitForLoadState('networkidle');
    await p.waitForTimeout(2500);
  }
  await p.waitForTimeout(4000);
  await p.mouse.move(800, 700); await p.mouse.wheel(0, 400); await p.waitForTimeout(1500);
  const t0 = p.getByText(first, { exact: true }).first();
  await t0.scrollIntoViewIfNeeded(); await p.waitForTimeout(800);
  const bb = await t0.boundingBox();
  await p.mouse.dblclick(bb.x + 80, bb.y - 320);
  const res = [];
  for (let i = 0; i < 400; i++) {
    let src = null, name = null, pos = null;
    const prev = res.length ? res[res.length - 1] : {};
    for (let k = 0; k < 40 && (!src || src === prev.src || pos === prev.pos); k++) {
      await p.waitForTimeout(400);
      ({ src, name, pos } = await p.evaluate(() => {
        const v = document.querySelector('video');
        const crumbs = [...document.querySelectorAll('nav a, nav span, nav div')].map(e => e.textContent.trim()).filter(t => /\.\w{3,4}$/.test(t));
        const m = document.body.innerText.match(/(\d+) of (\d+)/);
        return { src: v && (v.currentSrc || v.src), name: crumbs.pop() || null, pos: m && m[0] };
      }));
    }
    if (src === prev.src) { console.log('stuck at', pos); break; }
    res.push({ name, pos, src });
    console.log(pos, name);
    fs.writeFileSync(out, JSON.stringify(res, null, 1));
    const m = pos && pos.match(/(\d+) of (\d+)/);
    if (m && m[1] === m[2]) break;
    await p.keyboard.press(']');
  }
  await b.close();
})();
