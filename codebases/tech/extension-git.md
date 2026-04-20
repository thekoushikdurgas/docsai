# Extension repository mirror

The extension source lives in the monorepo at `contact360.extension/`.

## Option A: Dedicated clone

Copy or clone only the extension folder into a new repo and push:

```bash
cd contact360.extension
git init
git remote add origin https://github.com/thekoushikdurgas/contact360_extension.git
git branch -M main
git add .
git commit -m "Initial Contact360 extension"
git push -u origin main
```

## Option B: Subtree from monorepo root

From the repository root that contains `contact360.extension/`:

```bash
git subtree split --prefix=contact360.extension -b extension-main
git push https://github.com/thekoushikdurgas/contact360_extension.git extension-main:main
```

Adjust branch names if your default branch differs.

## Option C: Filter-repo (advanced)

From a full monorepo clone, extract only `contact360.extension/` history into a new remote (use when subtree is too heavy):

```bash
git filter-repo --path contact360.extension/ --path-rename contact360.extension/:
git remote add origin https://github.com/thekoushikdurgas/contact360_extension.git
git branch -M main
git push -u origin main
```

Protect **`main`** on GitHub: require PR reviews, status checks from **`.github/workflows/extension-ci.yml`** (Vitest + build), and disallow force-push.

## CI artifact

The workflow zips `contact360.extension/dist` for manual Chrome Web Store upload.
