// node gql.js <out.json> <folderId>...   recursively lists folders via the share GraphQL API, hydrates files (thumbnail + names)
const { chromium } = require(process.env.PW);
const fs = require('fs');
const SHARE = '6eb9d8a6-060e-4b96-a2d8-3f37804d0c13';
const Q = n => JSON.parse(fs.readFileSync(__dirname + '/' + n + '.json'));
(async () => {
  const [out, ...folders] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage();
  let H = null;
  p.on('request', r => { if (!H && r.url().includes('graphql')) { const h = r.headers(); H = {}; for (const [k,v] of Object.entries(h)) if (!k.startsWith('sec-') && !['x-gql-op','x-telemetry-event-name','x-telemetry-event-id'].includes(k)) H[k] = v; } });
  await p.goto(`https://next.frame.io/share/${SHARE}/${folders[0]}`, { waitUntil: 'networkidle', timeout: 60000 });
  await p.waitForTimeout(2000);
  const call = async (tpl, vars) => { const r = await p.request.post('https://api.frame.io/graphql', { headers: H, data: { ...tpl, variables: vars } }); return r.json(); };
  const coll = Q('GetShareCollectionAssets'), hyd = Q('HydrateScrolledShareAssets');
  const result = {};
  async function list(fid, path) {
    for (const t of ['FOLDER', 'FILE']) {
      let after = null;
      do {
        const page = after ? { first: 200, after } : { first: 200 };
        const j = await call(coll, { shareId: SHARE, folderId: fid, assetType: t, page });
        const s = JSON.stringify(j);
        // find connection with edges/nodes
        let conn = null;
        (function f(o) { if (conn || !o || typeof o !== 'object') return; if (o.pageInfo && (o.edges || o.nodes)) { conn = o; return; } for (const v of Object.values(o)) f(v); })(j);
        if (!conn) { console.log('noconn', s.slice(0, 300)); break; }
        const nodes = (conn.nodes || conn.edges.map(e => e.node));
        if (t === 'FOLDER') { for (const n of nodes) { console.log('folder', path + '/' + n.name, n.id); await list(n.id, path + '/' + n.id); } }
        else {
          const ids = nodes.map(n => n.id);
          for (let i = 0; i < ids.length; i += 50) {
            const h = await call(hyd, { ...hyd.variables, shareId: SHARE, ids: ids.slice(i, i + 50), page: { first: 50 } });
            (function f(o) { if (!o || typeof o !== 'object') return; if (o.id && o.name && o.thumbnailImageUrl) result[o.id] = { path, name: o.name, thumb: o.thumbnailImageUrl.url, type: o.__typename, dur: o.duration }; for (const v of Object.values(o)) f(v); })(h);
          }
          console.log(path, nodes.length);
        }
        after = conn.pageInfo.hasNextPage ? conn.pageInfo.endCursor : null;
      } while (after);
    }
  }
  for (const f of folders) await list(f, f);
  fs.writeFileSync(out, JSON.stringify(result, null, 1));
  console.log('total', Object.keys(result).length);
  await b.close();
})();
