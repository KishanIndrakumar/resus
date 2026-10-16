# Resus.ie V2

The existing offline-first bedside communication PWA, updated to version 2.1.0 with compact mobile navigation, session summaries and symptom-specific timing. **This delivery is a development/review application. No supplied translation has documented independent clinical approval.** The restricted build therefore displays no translated clinical content.

## Run locally

Requires Node.js 22+; Python 3.10+ is needed only to re-import DOCX source material. There are no application dependencies, accounts, analytics, remote fonts, external AI calls or backend services.

```sh
cd resus-v2
npm run build
npm run build:clinical
npm test
npm run preview
```

Open http://127.0.0.1:4173. Both `npm run preview` and `npm run dev` start the local server. The delivered `dist/` and `dist-clinical/` are already built. To preview the restricted version: `node scripts/serve.mjs dist-clinical` (stop the other server first). Do not open index.html via file://; module loading and service workers require HTTP localhost or HTTPS.

The small native ES-module architecture deliberately avoids a framework and dependency installation. `src/app.js` owns the UI; `src/core.js` retains the translation approval, search and voice rules; `src/workflow.js` handles transient session and symptom associations, while `src/patient.js` and `src/summary.js` render their respective views. `src/data.d.ts` documents the data contract. No legacy application code is used.

## Using the app

The app defaults to **English source display**, which is explicitly labelled as clinician/test content rather than a validated translation. Use the globe button in the compact header to search English/native language names and switch immediately while preserving the question. The home screen has compact clinical cards, search, Rapid Stroke, Favourites and Recent. Directions / Instructions references existing Master IDs; the Master itself still has 12 original categories and remains unchanged.

The sticky bottom bar provides Home, Search, **Summary (count)** and Favourites. The count includes explicitly recorded answers and timing responses; reopening/editing a response does not add another count. Opened but unanswered questions do not increase it. Unknown and not-understood responses remain distinct, and non-understanding is marked as a communication issue rather than a clinical answer.

Open a question, show the translated question and register an answer. Instructions do not receive Yes/No controls; responses never automatically advance. Show to patient hides clinician controls, retains Play/Stop and RTL, and has an obvious exit. Technical source metadata is collapsed into Review details. The numeric pain scale accepts 0–10 and offers a clinician action for inability to use the scale.

Use **Review [system] answers** at any stage or the compact recap at the end of a system to see positive/unknown answers and add optional symptom-specific timing. Explicit phrase-ID eligibility in `src/workflow.js` limits contextual timing; it is never offered automatically for identity, allergies, regular medicines or instructions. Started, Duration and Sudden/gradual use existing supplied timing phrases and choices. Each symptom has its own timing slots, language and answers; Done restores the prior question, system or summary. Clinicians can explicitly mark numeric/exact timing approximate without inventing patient-facing wording. The generic translated timing question remains unchanged; confirm which symptom is being discussed, using an interpreter if context is unclear. The eligibility list remains subject to clinical governance review.

The summary groups opened questions and recorded answers by section/system and allows editing or clearing answers and timing separately. If an answer changes, existing timing stays attached to that exact symptom and is visibly flagged for review; it is never reassigned. A system review does not assert that clinical assessment is complete. Copy summary requires a separate privacy confirmation and copies only the displayed system/full-session scope to the OS clipboard; the OS may retain or sync it.

Favourites persist **phrase IDs only**. Recent questions, opened state, responses and symptom timing stay in memory. Clear session resets all of these except favourites; refresh closes the session too. No response is placed in a URL, localStorage, IndexedDB or a network request. Browsers/OS keyboard and clipboard services may have their own retention behavior; inputs disable autocomplete. See `CHANGELOG.md` and `review/UI-WORKFLOW.md` for this UI-only update.

Audio is manual. Replay uses the same Play audio button; Stop cancels speech. A language-matched installed device/browser voice is required; the app never substitutes an English voice for another language. Some device voices use network services. Only supplied phrase text is spoken; typed patient responses are never sent to speech synthesis. Offline voice availability must be checked on the intended device.

## Data and review status

`public/data/master.json` is the sole runtime English Master: **287 IDs**, source/contract version `5f17fd4f4b952892`. There is no 313-entry Master in the supplied workspace, and no merge was performed. Each of the 38 language documents contains 287 matching IDs. Each bundle currently exposes **261 entries for review**, with **26 entries quarantined** because the Master marks their ID mappings as provisional or requiring mapping. No ID was renamed. These 26 translations remain preserved in the source archive.

`review/translation-report.json` records per-language missing/quarantined IDs and validation issues. `review/TRANSLATION-STATUS.md` is the readable summary. The original extracted rows, translator notes, document declarations and text are retained in immutable content-hashed files under `review/<master-version>/`; these archives are excluded from the web build. Earlier import snapshots remain as revision history. Source metadata claiming qualifications or approval is preserved as source content, never converted into human verification.

The importer conservatively marks all translations AI draft. Exact English text and speaker/context must match; response contracts are assigned by the importer from the authoritative English wording. Clinical semantic equivalence, medical accuracy, register, mixed scripts and RTL linguistic correctness require independent human review. Automated validation cannot establish these properties. Legitimate markup stays in the archive and is displayed as text rather than executed HTML.

## Versioned import and new languages

The supplied Word files are included in `source-documents/` for reproducibility. Initial import: `python scripts/import_docx.py SOURCE_FOLDER` (or `npm run import` for that included collection). It uses Python standard-library ZIP/XML tooling and does not modify the Word documents. Existing source/runtime fingerprints protect canonical data against silent replacement. If source or runtime content changes, import refuses to overwrite it.

For a revised source collection:

```sh
python scripts/import_docx.py SOURCE_FOLDER --stage
```

This writes a complete candidate dataset and report into `review/import-candidates/<timestamp>/`. Review its changes, reconcile conflicts/mappings, archive the current canonical dataset, and explicitly promote the complete Master, matching bundles, language registry, report and input manifest together. Never merge different Masters implicitly.

For a new/revised JSON language bundle:

```sh
node scripts/stage-bundle.mjs candidate.json
node scripts/validate.mjs
```

Staging validates against the canonical Master, saves a content-hashed candidate, records changed/removed IDs and previous version, and leaves the canonical bundle unchanged. After review, explicitly promote the candidate and add/update one metadata object in `public/data/languages.json` (`code`, English `name`, `native`, `dir`, `available`, `total`, `status`, `version`). The core app does not need changes. Language codes use BCP 47. Duplicate JSON keys are rejected by staging and builds; DOCX duplicate IDs are rejected/quarantined by the importer. Keep conflicts in review archives. Add new English questions only through an explicit Master revision and translation review.

## Clinical release boundary

`npm run build` produces review mode. `npm run build:clinical` produces a separate artifact which strips every entry unless it has status `Human verified`, an exact source hash, speaker and response-type match, resolved ID mapping, and nonempty documented approval fields (`reviewer`, `date`, `policyVersion`, `evidence`). Runtime checks repeat these rules for question text **and auxiliary patient labels**. No fallback to another language or draft is allowed. A clinical build cannot be switched into review mode through its UI.

These checks are a technical restriction, not an approval process. Before clinical release, the project owner must establish a clinical governance policy, independently review the English wording, categories and response mappings, verify translations and response labels, record real approval evidence, perform device/accessibility/usability assessment, and authorize a release. The current source corpus has no independently established approval; do not change statuses based on AI declarations. This app provides neither diagnosis nor prescribing, and a Yes response never establishes informed consent.

## PWA deployment and updates

No deployment was performed, as requested. For static hosting, upload **only the contents of the selected build directory** to an HTTPS origin or GitHub Pages subdirectory. All asset paths are relative. Do not publish `review/`, source DOCX files, or the project ZIP alongside the clinical artifact. Keep review and clinical releases on separate origins, and retire any previously hosted review data when changing an origin to clinical use.

The generated manifest includes PNG icons at 192/512px, a relative scope and standalone display. On Android/desktop use the browser install action; on iOS use Share → Add to Home Screen where available. Real Android/iOS installation remains a manual device check, not a claim of completed physical-device testing.

The service worker atomically precaches app assets and all registered language bundles. The cache key hashes the full artifact and includes the registration scope. Navigation and bundle requests use the same active version cache to avoid mixed versions. An update waits; Menu → Update app explicitly activates it and clears session state. Existing controlled windows reload on controller change. Failed precaching leaves the prior active version in use. Initial offline use requires one successful online load and service-worker installation. Browser storage eviction/private browsing may remove caches; verify offline readiness on the intended device.

## Tests

`npm test` uses Node's built-in test runner. Build both artifacts first. The tests cover exact mapping, source contracts, approval filtering, malicious markup, missing translations, response types, search, categories, voice selection, session reset and clinical bundle stripping.

`node tests/browser.cjs` runs the Playwright integration suite and starts/stops its own server on port 4180. Install Playwright for development (`npm install --no-save playwright` and `npx playwright install chromium`) or point `RESUS_PLAYWRIGHT` at an existing package. `RESUS_BROWSER_CHANNEL=chrome` uses installed Chrome. These are optional test dependencies only; the app has no runtime packages. The suite exercises 320/360/390/430px mobile widths, tablet, desktop and landscape patient mode; symptom-linked onset and duration; summary counts and edits; English/Arabic/Tamil switching; RTL; Stroke; explicit clipboard confirmation; session privacy; missing/unverified translations; offline operation and service-worker activation. Use `npm run test:browser` after configuring Playwright if needed. See `review/browser-test-results.json` and `review/test-results.txt` for actual results. Testing uses synthetic inputs only.

Manual checks still required: physical iOS/Android install and eviction, VoiceOver/TalkBack, keyboard-only assistive technology, actual installed language voices, independent translation accuracy, and clinical workflow assessment.

## Project contents

- `src/`: application, styles, pure rules and data types.
- `public/data/`: one authoritative Master, language registry and one bundle per language.
- `scripts/`: DOCX import, validation, staged imports, deterministic PWA build and local HTTP server.
- `tests/`: unit/data and real browser tests.
- `review/`: source provenance, translation reports, proposed English additions and test evidence; excluded from runtime.
- `dist/`, `dist-clinical/`: standalone review/restricted artifacts.

The supplied documents' rights remain with their owners. This delivery does not assert ownership of the translations or include a third-party faces pain instrument.
