// Usage: node fps.js <share url> <session names...>
// For each Women session, descends into its video folders and prints the first clip's preview src per leaf folder.
const { chromium } = require(process.env.PW);
(async () => {
  const [url, ...sessions] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1600, height: 1200 } });
  const open = async name => {
    await p.getByText(name, { exact: true }).last().dblclick();
    await p.waitForLoadState('networkidle'); await p.waitForTimeout(2500);
  };
  const folders = async () => p.evaluate(() => {
    const t = document.body.innerText.split('\n').map(s => s.trim()).filter(Boolean);
    const out = [];
    for (let i = 0; i < t.length - 1; i++) if (/^(\d+ Items|No Items)$/.test(t[i + 1])) out.push([t[i], t[i + 1]]);
    return out;
  });
  const firstClip = async () => {
    await p.waitForTimeout(2000);
    const names = await p.evaluate(() => (document.body.innerText.match(/Source Filename\n(\S+\.(?:MP4|MOV|mp4|mov))/g) || []).map(s => s.split('\n')[1]));
    if (!names.length) return null;
    const bb = await p.getByText(names[0], { exact: true }).first().boundingBox();
    await p.mouse.dblclick(bb.x + 80, bb.y - 320);
    let src = null;
    for (let k = 0; k < 30 && !src; k++) { await p.waitForTimeout(400); src = await p.evaluate(() => { const v = document.querySelector('video'); return v && (v.currentSrc || v.src); }); }
    return [names[0], src];
  };
  for (const s of sessions) {
    try {
      await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 }); await p.waitForTimeout(2500);
      await open('Women'); await open(s);
      const top = (await folders()).filter(([n, c]) => /video/i.test(n) && c !== 'No Items');
      for (const [v] of top) {
        await open(v);
        const base = p.url();
        const subs = (await folders()).filter(([, c]) => c !== 'No Items');
        if (!subs.length) { console.log(JSON.stringify([s, v, '', await firstClip()])); continue; }
        for (const [sub, cnt] of subs) {
          await p.goto(base, { waitUntil: 'networkidle' }); await p.waitForTimeout(2500);
          await open(sub);
          console.log(JSON.stringify([s, v, sub + ' (' + cnt + ')', await firstClip()]));
        }
      }
    } catch (e) { console.log(JSON.stringify([s, 'ERR', e.message.split('\n')[0]])); }
  }
  await b.close();
})();
