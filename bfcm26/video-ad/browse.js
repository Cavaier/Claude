// Usage: node browse.js <url> <outdir> [folder names to click, in order...]
const { chromium } = require(process.env.PW);
(async () => {
  const [url, out, ...path] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1600, height: 1200 } });
  await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await p.waitForTimeout(3000);
  for (const name of path) {
    await p.getByText(name, { exact: true }).last().dblclick();
    await p.waitForLoadState('networkidle');
    await p.waitForTimeout(3000);
  }
  // scroll to load everything
  for (let i = 0; i < 15; i++) { await p.mouse.wheel(0, 3000); await p.waitForTimeout(600); }
  const tag = path.join('_') || 'root';
  await p.screenshot({ path: `${out}/${tag}.png`, fullPage: true });
  require('fs').writeFileSync(`${out}/${tag}.txt`, p.url() + '\n' + await p.innerText('body'));
  await b.close();
})();
