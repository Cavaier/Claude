// Run with use_figma on file e0aqnfx3SvHowbEDDyMNMW.
// Removes the annotations Claude added: yellow "vN note" frames, in-email "stand" notes
// (content below moves up, frame shrinks), and the "TL · note" lines in the timeline headers.
// Leaves dates, phase tags, dots, timeline line, pills, subjects and previews in place.
const out = { notes: 0, stand: 0, tlnotes: 0, pages: [] };
for (const page of figma.root.children) {
  await page.loadAsync();
  let touched = 0;
  for (const n of page.findAll(n => n.type === 'FRAME' && /^v\d+ note/.test(n.name))) { n.remove(); out.notes++; touched++; }
  for (const n of page.findAll(n => n.type === 'TEXT' && n.name.startsWith('TL · note'))) { n.remove(); out.tlnotes++; touched++; }
  for (const s of page.findAll(n => n.type === 'FRAME' && n.name === 'stand' && n.parent && n.parent.type === 'FRAME')) {
    const em = s.parent, h = s.height, y0 = s.y;
    s.remove();
    for (const c of em.children) if (c.y > y0) c.y -= h;
    em.resize(em.width, em.height - h);
    out.stand++; touched++;
  }
  if (touched) out.pages.push(page.name + ': ' + touched);
}
return out;
