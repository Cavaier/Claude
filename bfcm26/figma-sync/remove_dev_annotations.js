// Run with use_figma on file e0aqnfx3SvHowbEDDyMNMW.
// Removes Dev Mode annotations in the "Development" category (the "EU · Instagram button / Link: …" cards)
// from every node on the Email Campaign page (310:2). Other annotation categories and all design layers stay.
const page = await figma.getNodeByIdAsync('310:2');
await page.loadAsync();
const cats = await figma.annotations.getAnnotationCategoriesAsync();
const dev = cats.filter(c => /development/i.test(c.label)).map(c => c.id);
let nodes = 0, removed = 0;
for (const n of page.findAll(n => 'annotations' in n && n.annotations && n.annotations.length)) {
  const keep = n.annotations.filter(a => !(a.categoryId && dev.includes(a.categoryId)));
  if (keep.length !== n.annotations.length) {
    removed += n.annotations.length - keep.length; nodes++;
    n.annotations = keep;
  }
}
return { categories: cats.map(c => c.label), nodes, removed };
