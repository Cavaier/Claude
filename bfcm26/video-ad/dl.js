// Usage: node dl.js <url> <outdir> <folder path joined by '/'> <filename> [<filename>...]
// Opens each asset in the share player and saves it via the player's Download button.
const { chromium } = require(process.env.PW);
const fs = require('fs');
(async () => {
  const [url, out, folder, ...names] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const ctx = await b.newContext({ acceptDownloads: true, viewport: { width: 1600, height: 1200 } });
  const p = await ctx.newPage();
  await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await p.waitForTimeout(3000);
  for (const f of folder.split('/')) {
    await p.getByText(f, { exact: true }).last().dblclick();
    await p.waitForLoadState('networkidle');
    await p.waitForTimeout(2500);
  }
  const folderUrl = p.url();
  for (const n of names) {
    if (fs.existsSync(`${out}/${n}`)) { console.log('have', n); continue; }
    try {
      await p.goto(folderUrl, { waitUntil: 'networkidle' });
      await p.waitForTimeout(2500);
      const t = p.getByText(n, { exact: true }).first();
      await t.scrollIntoViewIfNeeded();
      const bb = await t.boundingBox();
      await p.mouse.dblclick(bb.x + 80, bb.y - 320);
      await p.waitForTimeout(4000);
      const [d] = await Promise.all([
        p.waitForEvent('download', { timeout: 60000 }),
        (async () => {
          await p.getByText('Download', { exact: true }).first().click();
          await p.waitForTimeout(1500);
          await p.getByText(/^MP4 H264 (1080x|1920x1080)/).first().click();
        })(),
      ]);
      // some versions show a menu (Original / Proxy); pick Original if it appears
      await d.saveAs(`${out}/${n}`);
      console.log('ok', n, fs.statSync(`${out}/${n}`).size);
    } catch (e) {
      console.log('ERR', n, e.message.split('\n')[0]);
      await p.screenshot({ path: `${out}/_err_${n}.png` });
    }
  }
  await b.close();
})();
