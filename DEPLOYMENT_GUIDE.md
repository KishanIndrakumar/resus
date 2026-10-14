# Resus.ie — Deployment Guide

Covers: deploying this release, rebuilding it from source, and rolling back. Read `FINAL_RELEASE_REPORT.md` first for what this release actually contains and its clinical-validation status (development/pilot build — not clinically validated).

---

## 1. What gets deployed

Only four things need to be on the web server — everything else in the release package is source, tests, or documentation:

```
index.html
sw.js
manifest.json
icons/
  ├── icon-192.png
  ├── icon-512.png
  ├── icon-192-maskable.png
  ├── icon-512-maskable.png
  ├── apple-touch-icon.png
  └── favicon-64.png
```

`index.html` is fully self-contained (all 36 languages' translations and the English question bank are embedded directly in it at build time) — there is no separate data file to deploy alongside it, and no server-side component or database.

---

## 2. Deploying to GitHub Pages

1. Create (or use an existing) GitHub repository for the site.
2. Copy the 4 items from §1 into the repository, at the path you want served (repository root for a user/org site, or any folder for a project site — just keep `index.html`, `sw.js`, `manifest.json`, and `icons/` together, since `sw.js`'s cache list and `manifest.json`'s icon paths are relative).
3. Commit and push.
4. In the repository's **Settings → Pages**, set the source to the branch/folder you pushed to.
5. GitHub Pages will serve the site at `https://<username>.github.io/<repo>/` (or your custom domain, if configured). Open that URL — the app should load, show the disclaimer, and be installable as a PWA (the browser's install prompt, or "Add to Home Screen" on mobile).
6. **HTTPS is required for the service worker to register** — GitHub Pages serves HTTPS by default, so no extra step is needed there.

## 3. Deploying to existing static hosting (Netlify, S3+CloudFront, nginx, Apache, etc.)

1. Upload the 4 items from §1 to the web root (or the subpath you're serving the app from), preserving the `icons/` folder structure.
2. Confirm the host serves the site over **HTTPS** — service workers refuse to register over plain HTTP (except `localhost`, which only matters for local testing).
3. No server configuration is required beyond serving static files — no redirects, no server-side routing, no environment variables, no build step at deploy time.
4. If you serve the app from a subpath (e.g. `https://example.org/resus-ie/`), no changes are needed: `manifest.json`'s `start_url`/`scope` and `sw.js`'s `CORE_ASSETS` all use relative paths (`./`, `./icons/...`), so they resolve correctly under any subpath.

## 4. Verifying a deployment

After deploying, from a browser:
1. Open the deployed URL. Confirm the disclaimer appears and the home screen loads with no visible errors.
2. Open the browser's DevTools console — confirm no errors.
3. Open DevTools → Application → Service Workers — confirm a service worker is registered and activated for the page's origin.
4. Open DevTools → Application → Cache Storage — confirm a cache named `edrt-v13` (or whatever `CACHE_NAME` the deployed `sw.js` has) exists and contains `index.html`, `manifest.json`, and the 6 icon files.
5. Turn off your network connection (or use DevTools' "Offline" throttling) and reload the page — it should load exactly as before, fully offline.
6. Switch to a non-English language in the Systems module and confirm the question text changes — this should also work fully offline, since every language is embedded in `index.html` already.

These are the same checks `test_release_pwa_matrix.py` runs automatically against a local server (see `FINAL_RELEASE_REPORT.md` §6 for its actual results); repeating them against the real deployed URL is good practice before telling anyone the release is live.

---

## 5. Rebuilding from source (if you need to change anything first)

The deployable `index.html` is generated, not hand-edited. To change English question wording, a translation, or add a language, edit the source files and rebuild — **never hand-edit the deployed `index.html` directly**, since the next rebuild will silently overwrite any such edit.

1. Make your change in the relevant source file:
   - English question wording → `systems.en.json`
   - A translation → the relevant `systems.translations.<code>.json`
   - The legacy phrasebook → `DATA_PHRASES.r6.json` / `DATA_META.r6.json` / `DATA_LANGS.json` (unchanged by this project, included only because the build needs them)
2. From the folder containing `render_index.py`, `template.html`, and all the source JSON files above, run:
   ```
   python3 render_index.py
   ```
3. This overwrites `index.html` in that same folder. No dependencies beyond Python's standard library (`json`, `os`) are required.
4. **Bump `sw.js`'s `CACHE_NAME`** (e.g. `edrt-v13` → `edrt-v14`) any time you redeploy a changed `index.html` — this is what makes a visiting browser discard its old cached copy and fetch the new one. If you forget this step, users who already have the app cached may keep seeing the old version until they manually clear their browser cache.
5. Re-run the test suite (`test_systems.py`, `test_offline.py`, `test6.py`, `test_phaseD_full_matrix.py`, `test_phaseD_modules.py`, `test_release_pwa_matrix.py`) against a local server before redeploying — see each script's own header comment for what it checks. A simple local server for testing: `python3 -m http.server 8731` from the folder containing `index.html`, then point the test scripts' `http://localhost:8731/...` URL at that port (already the default in all of them).
6. Redeploy the new `index.html` + updated `sw.js` using the same steps as §2 or §3.

This exact rebuild process was verified during this release — see `FINAL_RELEASE_REPORT.md` §8 for the reproducibility check (rebuilding from a completely separate, freshly-populated folder produced a byte-identical `index.html`).

---

## 6. Rolling back

There is no database or server-side state to roll back — the entire application is the 4 files in §1, and all user-entered data lives only in the browser's in-memory JavaScript state for the current session (never written to `localStorage` or any persistent store, so there's nothing left behind to migrate or clean up on either a forward or backward move).

To roll back to a previous version:
1. Keep a copy of the previous `index.html` and `sw.js` pair before deploying a new one (standard version control — e.g. a git tag or a dated backup folder — makes this automatic).
2. Redeploy the previous `index.html` and `sw.js` over the current ones, exactly as in §2/§3.
3. Because the rolled-back `sw.js` has a cache name the browser hasn't seen as "current" since the forward deploy (e.g. rolling back from `edrt-v13` to `edrt-v12`), its own `activate` handler will delete the newer cache and create its own — the same version-cleanup mechanism that handles forward upgrades handles rollback identically, with no special-casing needed.
4. A user who has the app open at the moment of rollback will pick up the rolled-back version on their next full reload (the service worker's `skipWaiting()`/`clients.claim()` calls mean this happens promptly, not after a long delay).

No data migration, no downtime, and no coordination with any backend is required in either direction.
