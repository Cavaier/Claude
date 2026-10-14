// Usage: node dl2.js <share base url> <walk.json> <outdir> <filename>...
// Opens each asset's view page directly (asset id taken from its preview src) and saves the 1080 proxy.
const { chromium } = require(process.env.PW);
const fs = require('fs');
(async () => {
  const [base, walk, out, ...names] = process.argv.slice(2);
  const ids = Object.fromEntries(JSON.parse(fs.readFileSync(walk)).map(r => [r.name, r.src.match(/encode\/([0-9a-f-]{36})\//)[1]]));
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const ctx = await b.newContext({ acceptDownloads: true, viewport: { width: 1600, height: 1200 } });
  const p = await ctx.newPage();
  for (const n of names) {
    if (fs.existsSync(`${out}/${n}`)) { console.log('have', n); continue; }
    try {
      await p.goto(`${base}/view/${ids[n]}`, { waitUntil: 'networkidle', timeout: 60000 });
      await p.waitForTimeout(2500);
      const [d] = await Promise.all([
        p.waitForEvent('download', { timeout: 60000 }),
        (async () => {
          await p.getByText('Download', { exact: true }).first().click();
          await p.waitForTimeout(1500);
          await p.getByText(/^MP4 H264 (1080x|1920x1080)/).first().click();
        })(),
      ]);
      await d.saveAs(`${out}/${n}`);
      console.log('ok', n, fs.statSync(`${out}/${n}`).size);
    } catch (e) { console.log('ERR', n, e.message.split('\n')[0]); }
  }
  await b.close();
})();
