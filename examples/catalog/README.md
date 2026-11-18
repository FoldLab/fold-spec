# Catalog and thumbnail example

`first-fold-catalog.fold.json` is the minimal text lesson plus a `catalog` member and one `thumbnail`-role asset, `assets/gallery.webp` (360×270, 1,458 bytes, a generated placeholder drawing rather than a render of any model).

`first-fold-catalog.foldlab` is the same document packaged. Its `manifest.json` carries a derived `index`, so a gallery can show the title, slug, step count and thumbnail from this one file:

```sh
python tools/foldspec.py pack examples/catalog/first-fold-catalog.fold.json -o /tmp/catalog.foldlab
python tools/foldspec.py index examples/catalog/first-fold-catalog.foldlab
```

Run commands from the repository root. The index is recomputed and compared on every package inspection; editing it by hand makes the package invalid (`E_INDEX`). No assistive-technology review of the alt text is claimed.
