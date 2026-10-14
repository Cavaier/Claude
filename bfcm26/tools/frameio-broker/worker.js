// Frame.io token broker (Cloudflare Worker).
// Holds the Adobe IMS refresh token so nobody has to sign in again:
//   GET  /login     -> Adobe sign-in (one time)
//   GET  /callback  -> swaps the code for tokens, stores them in KV, shows "Connected"
//   POST /token     -> short-lived Frame.io access token for helpers (auth header required)
//   GET  /status    -> health (auth header required), never returns tokens
//   cron (daily)    -> renews the refresh token so it never reaches Adobe's 14-day limit
// Auth for /token and /status: header X-Broker-Auth = hex(HMAC-SHA256(key=client secret, msg=unix minute)),
// accepted for +-2 minutes. Helpers already have the client secret in env, so no extra key is needed.
// Bindings: KV (namespace), ADOBE_CLIENT_ID, ADOBE_CLIENT_SECRET (secrets).

const IMS = 'https://ims-na1.adobelogin.com/ims';
const SCOPE = 'openid,AdobeID,offline_access,email,profile';

const html = (title, body) => new Response(
  `<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>${title}</title>` +
  `<body style="font-family:system-ui,sans-serif;max-width:520px;margin:15vh auto;padding:0 16px;color:#141414"><h1 style="font-weight:400">${title}</h1><p>${body}</p></body>`,
  { headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store' } });
const json = (o, status = 200) => new Response(JSON.stringify(o), { status, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } });

async function hmacHex(key, msg) {
  const k = await crypto.subtle.importKey('raw', new TextEncoder().encode(key), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('HMAC', k, new TextEncoder().encode(msg));
  return [...new Uint8Array(sig)].map(b => b.toString(16).padStart(2, '0')).join('');
}
async function authorized(req, env) {
  const got = req.headers.get('x-broker-auth') || '';
  const m = Math.floor(Date.now() / 60000);
  for (const d of [0, -1, 1, -2, 2]) if (got === await hmacHex(env.ADOBE_CLIENT_SECRET, String(m + d))) return true;
  return false;
}

async function ims(env, params) {
  const body = new URLSearchParams({ client_id: env.ADOBE_CLIENT_ID, client_secret: env.ADOBE_CLIENT_SECRET, ...params });
  const r = await fetch(`${IMS}/token/v3`, { method: 'POST', body, headers: { 'content-type': 'application/x-www-form-urlencoded' } });
  const d = await r.json().catch(() => ({}));
  if (!r.ok || !d.access_token) throw new Error(`IMS ${r.status} ${d.error || ''} ${d.error_description || ''}`.trim());
  return d;
}

async function save(env, d, how) {
  const now = Date.now();
  const st = JSON.parse(await env.KV.get('state') || '{}');
  if (d.refresh_token) {
    st.refresh_token = d.refresh_token;
    st.refresh_set_at = now;
    st.rotations = (st.rotations || 0) + (how === 'refresh' ? 1 : 0);
  }
  st.access_token = d.access_token;
  st.access_expires_at = now + (Number(d.expires_in) || 3600) * (Number(d.expires_in) > 100000 ? 1 : 1000) - 120000;
  st.last_ok = now; st.last_how = how; st.last_error = null;
  st.refresh_returned_on_refresh = how === 'refresh' ? !!d.refresh_token : st.refresh_returned_on_refresh;
  await env.KV.put('state', JSON.stringify(st));
  return st;
}

async function refresh(env) {
  const st = JSON.parse(await env.KV.get('state') || '{}');
  if (!st.refresh_token) throw new Error('not connected: open /login once');
  try {
    return await save(env, await ims(env, { grant_type: 'refresh_token', refresh_token: st.refresh_token }), 'refresh');
  } catch (e) {
    st.last_error = String(e.message || e); st.last_error_at = Date.now();
    await env.KV.put('state', JSON.stringify(st));
    throw e;
  }
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const cb = `${url.origin}/callback`;
    if (url.pathname === '/login') {
      const state = crypto.randomUUID();
      await env.KV.put('oauth_state:' + state, '1', { expirationTtl: 600 });
      const q = new URLSearchParams({ client_id: env.ADOBE_CLIENT_ID, redirect_uri: cb, scope: SCOPE, response_type: 'code', state });
      return Response.redirect(`${IMS}/authorize/v2?${q}`, 302);
    }
    if (url.pathname === '/callback') {
      const code = url.searchParams.get('code'), state = url.searchParams.get('state');
      if (!code || !state || !(await env.KV.get('oauth_state:' + state))) return html('Sign-in failed', 'This link has expired or is invalid. Open <b>/login</b> again.');
      await env.KV.delete('oauth_state:' + state);
      try {
        const st = await save(env, await ims(env, { grant_type: 'authorization_code', code, redirect_uri: cb }), 'login');
        return html('Frame.io connected ✓', st.refresh_token ? 'Claude can now upload to Frame.io without new sign-ins. You can close this tab.' : 'Signed in, but Adobe returned no refresh token (offline_access missing). Tell Claude.');
      } catch (e) { return html('Sign-in failed', String(e.message || e).replace(/[<>]/g, '')); }
    }
    if (url.pathname === '/token' && req.method === 'POST') {
      if (!(await authorized(req, env))) return json({ error: 'unauthorized' }, 401);
      let st = JSON.parse(await env.KV.get('state') || '{}');
      try { if (!st.access_token || Date.now() > st.access_expires_at) st = await refresh(env); }
      catch (e) { return json({ error: String(e.message || e) }, 502); }
      return json({ access_token: st.access_token, expires_at: st.access_expires_at });
    }
    if (url.pathname === '/status') {
      if (!(await authorized(req, env))) return json({ error: 'unauthorized' }, 401);
      const st = JSON.parse(await env.KV.get('state') || '{}');
      return json({ connected: !!st.refresh_token, refresh_set_at: st.refresh_set_at, rotations: st.rotations || 0,
        refresh_returned_on_refresh: st.refresh_returned_on_refresh ?? null, last_ok: st.last_ok, last_how: st.last_how,
        last_error: st.last_error || null, last_error_at: st.last_error_at || null });
    }
    return html('Frame.io broker', 'Private service.');
  },
  async scheduled(event, env, ctx) { ctx.waitUntil(refresh(env).catch(() => {})); },
};
