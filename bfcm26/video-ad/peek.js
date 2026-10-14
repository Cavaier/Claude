// Usage: node peek.js <url> <out.png> — loads a page and screenshots it with its visible text.
const { chromium } = require(process.env.PW);
(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1600, height: 1200 } });
  await p.goto(process.argv[2], { waitUntil: 'networkidle', timeout: 60000 });
  await p.waitForTimeout(5000);
  await p.screenshot({ path: process.argv[3] });
  console.log(p.url()); console.log((await p.innerText('body')).slice(0, 600));
  await b.close();
})();
