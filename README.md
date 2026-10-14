# Resus.ie — ED Translate (Development Release)

**Status: development / pilot-testing build. Not clinically validated. Not a replacement for a qualified interpreter.** See `FINAL_RELEASE_REPORT.md` for full detail.

Resus.ie is an offline-first Progressive Web App (PWA) communication aid for Emergency Department staff: a 62-phrase legacy phrasebook (British Red Cross/NHS Emergency Multilingual Phrasebook, 35 languages) plus a 96-question structured "Systems" symptom-screening module (36 languages), all embedded directly in one self-contained `index.html` with no server-side component and no runtime network dependency for translation content.

---

## What's in this folder

```
resus-ie-complete-release/
├── index.html              ← the built, deployable application
├── sw.js                   ← service worker (offline caching)
├── manifest.json           ← PWA manifest
├── icons/                  ← PWA icons (incl. Apple touch icon, maskable icons)
├── README.md                ← this file
├── FINAL_RELEASE_REPORT.md  ← the authoritative status report — READ THIS FIRST
├── DEPLOYMENT_GUIDE.md       ← step-by-step deploy/rollback instructions
├── TRANSLATION_REVIEW_PENDING.xlsx  ← outstanding translation review work
├── src/                     ← build source files (see "Rebuilding" below)
│   ├── render_index.py      ← the build script
│   ├── template.html        ← page template render_index.py fills in
│   ├── systems.en.json      ← 96-question English master (contentVersion 1.2-draft)
│   ├── systems.en.revised.json  ← English-question decision-round record
│   ├── systems.languages.json   ← 36-language manifest
│   ├── systems.translations.<code>.json × 36  ← one editable file per language
│   ├── time_onset_translations.json  ← Time/Onset module strings, English + 36 AI-draft languages
│   ├── build_time_onset_translations.py  ← script that generated time_onset_translations.json
│   └── DATA_PHRASES.r6.json, DATA_LANGS.json, DATA_META.r6.json  ← legacy phrasebook data (unchanged by this project; needed only because the build reads them)
├── tests/                   ← all Playwright test scripts (see "Testing" below)
└── reports/                 ← full QA/decision history (historical — superseded by FINAL_RELEASE_REPORT.md where they conflict)
```

---

## Quick start: run it locally

No build step is required to just view the app — `index.html` is already built and self-contained.

```bash
cd resus-ie-complete-release
python3 -m http.server 8731
```

Then open `http://localhost:8731/index.html` in a browser.

---

## Rebuilding `index.html` from source

If you change an English question (`src/systems.en.json`), a translation (`src/systems.translations.<code>.json`), or the legacy phrasebook data, rebuild with:

```bash
cd resus-ie-complete-release/src
python3 render_index.py
```

This writes a new `index.html` **inside `src/`** — copy it up to the release root (replacing the one there) to deploy it. No dependencies beyond Python's standard library.

**After rebuilding, bump `sw.js`'s `CACHE_NAME`** (e.g. `edrt-v14` → `edrt-v15`) so browsers with the app already cached pick up the change. See `DEPLOYMENT_GUIDE.md` §5 for the full rebuild-and-redeploy procedure.

This exact rebuild process was verified during release preparation: rebuilding from `src/` alone (no other file in this project) reproduces `index.html` byte-for-byte.

---

## Testing

All scripts in `tests/` use [Playwright](https://playwright.dev/python/) against a local server. From the release root:

```bash
python3 -m http.server 8731 &
cd tests
python3 test_systems.py
python3 test_offline.py
python3 test6.py
python3 test_phaseD_full_matrix.py
python3 test_phaseD_modules.py
python3 test_release_pwa_matrix.py
python3 test_time_onset_module.py
```

(`test.py`, `test2.py`, `test3.py`, `test4.py`, `test5.py` are older scripts kept for history; the first three reference a UI element removed before this release — see `FINAL_RELEASE_REPORT.md` §6 for why that's expected, not a regression.)

Actual results from the most recent run of every script are recorded in `FINAL_RELEASE_REPORT.md` §6 — this README does not repeat them so there is only one place results can go stale.

---

## Deployment

See `DEPLOYMENT_GUIDE.md` for full step-by-step instructions (GitHub Pages or any static host) and rollback steps. In short: deploy `index.html`, `sw.js`, `manifest.json`, and `icons/` to any static HTTPS host — no server-side component, no database, no build step at deploy time.

---

## Clinical safety — read before any real-world use

- This is a **communication aid**, not a diagnostic tool and not a replacement for a qualified interpreter.
- **No translation in any of the 36 languages has been reviewed by a native speaker or qualified medical translator.** Every translation is an AI draft (`provenance.needs_human_review: true` in every `systems.translations.<code>.json` file).
- The Neurological/Stroke rapid-access banner is explicitly labelled "not a validated stroke assessment."
- See `FINAL_RELEASE_REPORT.md` §2 and `TRANSLATION_REVIEW_PENDING.xlsx` for the full, current list of what still needs human review before this could be considered for real patient-facing use.

---

## Where to look next

| Question | Where to look |
|---|---|
| "Is this safe to use with real patients yet?" | `FINAL_RELEASE_REPORT.md` §2 — short answer: not yet |
| "What changed in this release?" | `FINAL_RELEASE_REPORT.md` §4–5, or `reports/CHANGELOG.md` for full history |
| "What still needs translation review?" | `TRANSLATION_REVIEW_PENDING.xlsx` |
| "How do I deploy / roll back?" | `DEPLOYMENT_GUIDE.md` |
| "How do I rebuild after editing a translation?" | This file, "Rebuilding" above, or `DEPLOYMENT_GUIDE.md` §5 |
| "What did older QA passes find?" | `reports/` — each file now marked historical where superseded |
