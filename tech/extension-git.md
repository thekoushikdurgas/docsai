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
