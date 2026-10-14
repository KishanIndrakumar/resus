# Resus.ie — Final Release Report

**This is the single authoritative status document for this release.** Where any other report in this project (`SYSTEMS_QA_REPORT.md`, `ACCEPTANCE_TEST_CHECKLIST.md`, `SETUP_AND_REMAINING_ISSUES.md`, `Translation_QA_Report.md`, `Testing_Report.md`, `Phase_D_Integration_Report.md`) conflicts with this one, **this document is correct** — those are kept as historical audit trail and are now marked as such.

---

## 1. Version and release date

| | |
|---|---|
| Release | **Resus.ie — ED Translate, development release** |
| Date | 2026-10-13 |
| English content version (`systems.en.json` → `contentVersion`) | `1.2-draft` |
| Service worker cache version (`sw.js` → `CACHE_NAME`) | `edrt-v14` |
| Release type | **Development / pilot-testing build. Not clinically validated.** |

**This document now also covers the Time/Onset module redesign (Change #8 in `CHANGELOG.md`)**, applied after the Phase D translation/English changes described in §4–5 below. That work replaced the shared date/time-picker tool with a structured elapsed-time onset/duration capture widget — see the new §4b.

---

## 2. Clinical validation status — read this first

**Resus.ie is a communication aid for Emergency Department use. It is not a diagnostic tool and it is not a replacement for a qualified interpreter.**

- **0% of the translation content in this application has been reviewed by a native speaker or qualified medical translator**, across all 36 languages and all 96 questions (3,456 cells), including the handful of cells changed in this release.
- The 4 English wording changes in this release were reviewed and approved by the project owner, who is a qualified clinician — but that is an English-content review, not a translation-linguistic one.
- The Tamil `NEURO03` correction applied in this release is grammatically well-supported (a documented morphological analysis) but has **not** been confirmed by an independent Tamil speaker.
- This release is designated a **development/pilot-testing version** and must remain so designated until native-speaker/professional-medical-translator review has actually taken place. Nothing in this report, or in the application itself, claims otherwise.
- The in-app disclaimer, the "AI translated" tag on every drafted-language question, and the Neuro/Stroke module's "not a validated stroke assessment" wording are all preserved unchanged in this release (verified in §6).

---

## 3. Files included in this release

### Application (deployable)
- `index.html` — the built, deployable application (rebuilt in this release; see §5)
- `sw.js` — service worker, `CACHE_NAME` bumped to `edrt-v13`
- `manifest.json` — PWA manifest
- `icons/` — `icon-192.png`, `icon-512.png`, `icon-192-maskable.png`, `icon-512-maskable.png`, `apple-touch-icon.png`, `favicon-64.png`

### Build sources (needed to rebuild `index.html` — see §5)
- `render_index.py` — the build script (fixed in this release to use a portable, self-relative path instead of a machine-specific absolute path — see §5)
- `template.html` — the page template `render_index.py` fills in
- `systems.en.json` — the 96-question English master (`contentVersion` `1.2-draft`)
- `systems.languages.json` — the 36-language manifest
- `systems.translations.<code>.json` × 36 — one file per language, the editable source of truth for that language's translations
- `DATA_PHRASES.r6.json`, `DATA_LANGS.json`, `DATA_META.r6.json` — the legacy 62-phrase/35-language phrasebook's current data files (unchanged by this entire project; included because `render_index.py` needs them to build a complete `index.html`)
- `time_onset_translations.json` **(new in this release)** — English baseline + all 36 languages' AI-draft translations of the redesigned Time/Onset module's patient-facing strings (16 strings × 36 languages = 576 translated strings); `build_time_onset_translations.py` is the script that generated it, kept for maintainability/re-generation

### Tests
- `test_systems.py`, `test_offline.py`, `test6.py` — the pre-existing Playwright regression suite
- `test_phaseD_full_matrix.py`, `test_phaseD_modules.py` — added during Phase D integration
- `test_release_pwa_matrix.py` — added for this final release (PWA install/reload/offline-language-switch/response-workflow/layout/cache-version checks)
- `test_time_onset_module.py` **(new in this release)** — 19 checks covering the redesigned Time/Onset widget (see §4b and §6)
- `test.py`, `test2.py`, `test3.py`, `test4.py`, `test5.py` — older scripts, kept for history; `test.py`/`test2.py`/`test3.py` reference a `[data-shortcut="symptoms"]` element removed from the UI before this QA project began and will not pass as-is (see §7)

### Reports and logs
- `FINAL_RELEASE_REPORT.md` — this document
- `DEPLOYMENT_GUIDE.md` — deployment and rollback instructions
- `TRANSLATION_REVIEW_PENDING.xlsx` — outstanding translations requiring human review
- `Translation_Correction_Log.xlsx`, `Translation_Clinical_Language_Review.xlsx` — full translation QA data (3,456-cell matrix + 8 findings)
- `English_Question_Review.xlsx`, `systems.en.revised.json` — the English-question decision record
- `CHANGELOG.md` — full chronological history of every change made to the application
- `SYSTEMS_QA_REPORT.md`, `ACCEPTANCE_TEST_CHECKLIST.md`, `SETUP_AND_REMAINING_ISSUES.md`, `Translation_QA_Report.md`, `Testing_Report.md`, `Phase_D_Integration_Report.md` — historical reports, each now marked as superseded by this document

### Deliberately excluded (not missing — see §7)
A number of files in the original project folder are superseded intermediate build iterations or working screenshots, not part of the deployable application or its current build inputs: `DATA_PHRASES.json`/`.final`/`.step1`/`.step1b`/`.r4`/`.r5`, `DATA_META.json`/`.final`/`.step1`/`.r4`/`.r5`, `NEW_IDS.json`, `NEW_META.json`, `NEW_PHRASES.json`, `OPTIONS.json`, `batch_a.py`–`batch_d.py`, `build_data.py`–`build_data_r6.py`, `build_language_system.py`, `build_systems_translations.py`, `new_lang_pl_zhhans.py`, `new_lang_remaining8.py`, `phase_c_mechanical_audit.py`, `phase_c_mechanical_findings.pkl`, `orig_index.html`, `split_source_dump.txt`, `systems.translations.draft.json` (an older combined-language working file from before the current one-file-per-language split — superseded by the 36 individual `systems.translations.<code>.json` files, which are the only ones `render_index.py` actually reads), and roughly 60 development screenshot PNGs. None of these are required to rebuild or run the application; see §7 for the full accounting.

---

## 4. Approved English changes (live in `systems.en.json`, `contentVersion` `1.2-draft`)

| Question | Previous text | Current (approved) text |
|---|---|---|
| `SKIN07` | Have you had pain in your skin? | Has your skin been painful? |
| `EYE05` | Has bright light hurt your eyes? | Does bright light hurt your eyes? |
| `GU03` | Have you suddenly needed to pass urine urgently? | Have you had a sudden urge to pass urine that was difficult to hold? |
| `TRAUMA05` | Did you lose consciousness? | Did you black out after the injury? |

`RESP05` and `ENT05` are **confirmed unchanged** (verified byte-for-byte against the pre-release snapshot). `RESP05` awaits further clinical review; `ENT05` is deferred pending a decision on its overlap with `GI10`.

---

## 4b. Time/Onset module redesign (scope: only this module)

Per explicit instruction, this change touched **only** the Time/Onset module — the legacy phrasebook's "Time of Onset" shortcut (phrases 7 & 9) and the shared timing-capture tool reused by the Systems module's per-question recording button, its summary's "record for selected" button, and the Neuro/Stroke rapid-access banner. No other module, category, or approved clinical wording was touched.

**Replaced:** the old plain date-input + time-input "calendar/clock reference tool" is now a structured widget asking:
1. "How long ago did your symptoms start?" — numeric input + unit dropdown (seconds/minutes/hours/days/weeks/months/years), with a "Not sure" option.
2. "How long did your symptoms last?" — the same numeric+unit pattern, plus "Still ongoing" and a separate "Not sure" option.

**Added:** an optional Sudden/Gradual onset-character selector.

**Retained**, specifically for time-critical presentations (especially stroke): the original optional exact date + time inputs and a last-known-well date + time pair, now in a collapsible section underneath the two elapsed-time questions — expanded by default on the Neuro/Stroke "Record onset / last-known-well now" path.

**Nothing new is persisted** — captured values live only in an in-memory `state.timeOnset` object for the session, same as every other piece of state in this app.

**Clinical summary:** the Systems summary screen now shows onset, duration/ongoing status, and onset character as separate tags under each positive (Yes) item (e.g. "Onset: 2 hours ago", "Gradual onset", "Duration: still ongoing") rather than one merged line.

**Translation:** all 16 new patient-facing strings translated into all 36 languages (`time_onset_translations.json`), embedded at build time exactly like the Systems module's own translations. **Every one of these 576 strings is an unreviewed AI draft** (`status: "draft"`, `provenance.needs_human_review: true`) — none have been reviewed by a native speaker or qualified medical translator. This is an addition to, not a reduction of, the translation-review backlog already described in §5 below.

See `CHANGELOG.md` Change #8 for full detail, and §6 for the dedicated test results.

---

## 5. Translation corrections applied, and what remains unresolved

### 5.1 Applied to live translation files in this release

- **`GU03` and `TRAUMA05` retranslated in all 36 languages**, to match the new English meaning above. These are new AI drafts — unverified, same as every other translation in the project.
- **Tamil `NEURO03`** — a confirmed negation-inversion error corrected (previous text read as "the worst headache you have **never** experienced" instead of "**ever** had"). Flagged in the file's own `provenance.priority_native_speaker_review` and in `Translation_Correction_Log.xlsx` as the single highest-priority item awaiting independent Tamil-speaker confirmation.

### 5.2 Confirmed NOT applied — proposals only

- **Russian `CVS05`** and **Hindi `CVS05`** — both remain exactly as before this entire QA project began. Two candidate natural-register replacement phrasings exist for each in `Translation_Correction_Log.xlsx`, pending native-speaker confirmation of which (if either) to use.
- **Urdu, Malayalam, Gujarati `CVS05`** and **Tigrinya `GI03`/`GI04`/`TRAUMA06`** and **Latvian `CVS06`** — the remaining 5 of the 8 total correction-log findings, all unchanged, all flagged `requires_native_speaker_review` or similar in the log, none applied.

### 5.3 Full translation review coverage

All 3,456 Systems-module cells (36 languages × 96 questions) have had a direct AI linguistic read (100% coverage, completed across this project's QA phases). The 8 findings above are everything that read turned up. **None of the 3,456 cells — including the ones just changed — have been reviewed by a native speaker.** See `TRANSLATION_REVIEW_PENDING.xlsx` for the consolidated outstanding-review list.

**Separately, the Time/Onset module redesign (§4b) added 576 more AI-draft strings** (16 strings × 36 languages, in `time_onset_translations.json`) that are not yet part of the 3,456-cell matrix or `TRANSLATION_REVIEW_PENDING.xlsx` — they are a new, distinct set of patient-facing text with the same unreviewed-AI-draft status as everything else, not yet run through the same spreadsheet-based review workflow. This is flagged here so it is not overlooked: any future native-speaker review pass should cover these 576 strings in addition to the existing 3,456-cell matrix.

---

## 6. Automated tests performed, and actual results

All of the following were actually executed against the rebuilt `index.html` on a local static server (`python3 -m http.server`), via Playwright (Chromium), in this session. No result below is a projection or an assumption.

| Test | What it checks | Result |
|---|---|---|
| `test_systems.py` | Systems module smoke test: home screen, legacy Pain smoke test, Neuro rapid-access banner, full English walkthrough of General symptoms, edit-from-summary | **PASS** — 0 console errors |
| `test_offline.py` | Embedded-translation offline architecture: 7 drafted languages plus Tamil/Georgian shown fully offline from first load, unknown-code gate still shows offline | **PASS** — 0 console errors |
| `test6.py` | (see file for scope — part of the existing suite) | **PASS** — 0 console errors |
| `test_phaseD_full_matrix.py` | All 96×36 = 3,456 cells via the app's own `sysGetTranslation()`, online AND fully offline (6,912 lookups total); confirms the exact new text for all 4 English changes + Tamil fix + unchanged `RESP05`/`ENT05`/Russian `CVS05`/Hindi `CVS05` | **PASS** — 0 missing, 0 blank, 0 unexpected English-fallback cells in either pass; 0 console errors |
| `test_phaseD_modules.py` | Patient Details, Pain, Time/Onset, Allergies, Medications, Medical History, Pregnancy, Neuro (incl. Stroke disclaimer wording), Examination, Interpreter, Other, Systems home | **PASS** — 0 console errors, disclaimer wording intact |
| `test_release_pwa_matrix.py` | See item-by-item breakdown below | **18 of 19 checks PASS** (see below) |
| `test_time_onset_module.py` **(new, this release)** | The redesigned Time/Onset widget end-to-end: old date/time picker gone; elapsed-time value+unit capture for onset and duration; Not-sure/Still-ongoing disabling behaviour; Sudden/Gradual selector; retained exact-date/last-known-well section (expanded by default on the Neuro/Stroke path); the Systems runner button, Systems summary button, and Neuro urgent banner all open the same widget; summary shows onset/duration/character as separate tags; fully offline, including a Tamil translation check | **PASS — 19/19 checks**, 0 console errors |
| `test.py`, `test2.py`, `test3.py` | Pre-redesign scripts hardcoding a removed `[data-shortcut="symptoms"]` element | **FAIL, by design, not a regression** — this element was intentionally removed before this QA project began (`test_systems.py` itself asserts it has count 0); these three scripts predate the current suite and are not part of it |
| `test4.py`, `test5.py` | Older smoke scripts | **PASS** — run clean, no assertions failed |

### 6.1 `test_release_pwa_matrix.py` — item-by-item (addressing the specific checklist requested)

| # | Item | Result |
|---|---|---|
| 1 | First online installation: service worker registers, manifest + all icon files fetchable, zero console errors | **PASS** |
| 2 | Reload after installation | **PASS** — zero console errors |
| 3 | Language switching while fully offline | **PASS** — switched to Tamil fully offline, a Tamil-script question rendered |
| 4 | Yes / No / Don't know / Don't understand response workflow | **PASS** — all four buttons present; Yes/No/Don't-know clicks recorded and advanced the question runner, fully offline |
| 5 | Positive symptom summary + edit-from-summary | **PASS** — summary screen reached offline, showed the "POSITIVE (YES)" section, edit control worked |
| 5b | Copy / clipboard-export functionality | **NOT APPLICABLE — this feature does not exist anywhere in the application.** Confirmed by source inspection (`template.html` contains no "copy", "clipboard", "share", or `execCommand` reference of any kind). This was not removed or broken by this release; it was never built. If a copy/export feature is wanted, it needs to be scoped and built as new work — not assumed to already exist. |
| 6 | Pain and Time/Onset modules | **PASS** (smoke-tested via `test_phaseD_modules.py`; the redesigned Time/Onset widget itself has dedicated, detailed coverage in `test_time_onset_module.py` — 19/19 checks, see above) |
| 7 | Allergies, Medications, Medical History, Pregnancy/LMP, Neuro/Stroke | **PASS** (via `test_phaseD_modules.py`) |
| 8 | Mobile layout (390×780) | **PASS** — zero console errors, no horizontal overflow |
| 9 | Desktop layout (1440×900) | **PASS** — zero console errors, no horizontal overflow |
| 10 | PWA manifest, icons, service-worker registration | **PASS** — all present and fetchable |
| 11 | Cache behaviour on a version bump | **PASS** — current cache correctly named `edrt-v14`; `sw.js`'s `activate` handler verified (by source inspection) to delete any cache key that isn't the current `CACHE_NAME` |

**Net: every test that was actually run either passed or (for the 3 obsolete pre-redesign scripts) failed for a documented, pre-existing, out-of-scope reason. The one "not applicable" item (copy/export) is an honest absence, not a failure or an invented pass.**

---

## 7. Known limitations

1. **No translation in any of the 36 languages has been reviewed by a native speaker or qualified medical translator.** This is the single most important limitation of this release.
2. **8 specific translation issues remain open** (§5.2), including two (Russian/Hindi `CVS05`) that fully collapse a clinically important fainting/loss-of-consciousness distinction.
3. **`RESP05` and `ENT05`** have open clinical-content questions (pending review; deferred pending the `GI10` overlap decision, respectively).
4. **No copy/export/share feature exists** in the application at all (§6.1, item 5b) — not a defect in this release, simply something that has never been built.
5. **`render_index.py` previously hard-coded a machine-specific absolute path** (`/tmp/claude-0/.../scratchpad/build`), which would have broken a rebuild on any other machine. **Fixed in this release** to resolve its own directory at runtime; verified by rebuilding `index.html` from a completely separate, freshly-populated directory and confirming a byte-for-byte-identical result (§8).
6. **7 language codes exist in the project with translated content but are outside the current 36-language manifest** (`bs, cs, sk, mk, ln, ko`, and an old Traditional-script `zh` — see `Translation_QA_Report.md` §2/Phase A); not included in this release's scope, no decision made on them.
7. **A number of intermediate/superseded data files and ~60 development screenshots exist in the original project folder** (listed in full in §3) and were deliberately excluded from the release package as clutter, not because they are missing or lost — they remain available in the original working folder if ever needed for history.
8. **This release has not been tested on a real mobile device or in Safari/Firefox** — all testing was performed with Playwright's Chromium at emulated viewport sizes on a local static server, not a true cross-browser or physical-device pass.

---

## 8. Build reproducibility

`render_index.py` was verified to rebuild `index.html` correctly and deterministically:
1. Ran in place: produced a byte-identical `index.html` to the one already built (md5 match).
2. Ran from a **completely separate, freshly-populated directory** containing only `render_index.py`, `template.html`, `DATA_PHRASES.r6.json`, `DATA_LANGS.json`, `DATA_META.r6.json`, `systems.en.json`, `systems.languages.json`, `time_onset_translations.json`, and the 36 `systems.translations.<code>.json` files: produced a byte-identical `index.html` to the in-place build (md5 match).
3. Re-verified again after the Time/Onset module redesign (§4b) added `time_onset_translations.json` as a new build input: same byte-for-byte result, from a fresh directory and from the packaged release's own `src/` folder.

This confirms the build is reproducible with exactly the file set listed in §3's "Build sources" section, and does not depend on any other file in the project or any machine-specific path.

**To rebuild:** `cd` into the folder containing those files and run `python3 render_index.py`. It writes `index.html` in that same folder. No other setup is required (no dependencies beyond Python's standard library).

---

## 9. Deployment and rollback instructions

See **`DEPLOYMENT_GUIDE.md`** for full step-by-step instructions (GitHub Pages or existing static hosting) and rollback steps. Summary:
- **Deploy:** upload `index.html`, `sw.js`, `manifest.json`, and `icons/` to the web root of any static host. No server-side component, no build step required at deploy time (the build already happened; `index.html` is self-contained).
- **Rollback:** keep the previous `index.html`/`sw.js` pair; redeploying the previous pair and letting the service worker's own version-cleanup logic take over on next load is sufficient — no database or server state to roll back, since the app stores nothing server-side and only session-level (non-persistent) state client-side.

---

## 10. What was deliberately NOT done (per instruction)

- No redesign of the application.
- No new modules added.
- No change to approved clinical wording beyond the 4 items in §4, all previously approved by the project owner.
- No modification to any live/already-deployed website — this entire release exists only in this development package until the project owner deploys it.
- No runtime translation downloads or new external dependencies introduced — the embedded-translations, offline-first architecture is unchanged.
