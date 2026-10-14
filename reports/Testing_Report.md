> **HISTORICAL DOCUMENT — superseded by `FINAL_RELEASE_REPORT.md`.** This file is kept for its audit trail (what was found/decided/tested at the time) but is no longer the authoritative statement of current status. Where anything below conflicts with `FINAL_RELEASE_REPORT.md`, the final release report is correct. Read that file first.

---

# Testing Report — Translation Extraction, Review and QA task

Date: 2026-10-13 (updated same day following the project owner's decision round, the completed
full-coverage translation sweep, and Phase D integration). This report lists tests actually
performed and their results. It does not claim clinical or linguistic validation from automated
tests — see `Translation_QA_Report.md` for what automated testing can and cannot establish.

> **Phase D has since been integrated as a development release.** The section below ("Phase D
> decision and its effect on testing scope") describes the state *before* integration, when Phase
> D was still paused — it is kept for history. For what was actually integrated, the translation
> and build changes made, and the full Phase D test results (including two new tests covering the
> complete 96×36 translation matrix and every clinical module), see **`Phase_D_Integration_Report.md`**.

## Tests performed this task

| Test | Method | Result |
|---|---|---|
| Embedded vs. standalone translation files match | Byte-for-byte comparison, `index.html`'s embedded `SYS_TR` vs. each `systems.translations.<code>.json` | Pass — zero mismatches |
| All 96 question IDs present per language | Automated script (`phase_c_mechanical_audit.py`) over all 36 language files | Pass — 3,456/3,456 cells present |
| No missing/extra/duplicate question IDs | Same script | Pass |
| No empty translation cells | Same script | Pass |
| Script consistency (no untranslated/wrong-script text) | Same script, Unicode-block analysis per expected script | Pass — zero flags |
| RTL manifest-flag sanity (ar/ur/fa/ps/ku) | Same script | Pass |
| Question-mark/punctuation heuristic | Same script | Pass (Japanese intentionally exempted — see script comments) |
| Translation/English length-ratio outlier check | Same script | 36 flags, all Chinese (Simplified)/Cantonese, confirmed benign (logographic compactness) |
| `english_review_data.py` structural check | `assert len(REVIEW) == 96` and `set(REVIEW.keys()) == set(systems.en.json questions)` | Pass |
| `English_Question_Review.xlsx` formula/structure integrity | `recalc.py` (LibreOffice recalculation) | Pass — 0 formulas, 0 errors (static data table, no formulas by design) |
| `Translation_Clinical_Language_Review.xlsx` structure integrity | `recalc.py` | Pass — 0 errors (re-run after the full-coverage rebuild) |
| `Translation_Correction_Log.xlsx` structure integrity | `recalc.py` | Pass — 0 errors (re-run after adding the Alternate Suggestion column) |
| Direct clinical/linguistic read-through | Manual AI review of **all 3,456 of 3,456 cells** (see `Translation_QA_Report.md` §4.2 for exact scope and the two-stage breakdown: 1,344 cells in the prior session, 2,112 more completed this decision round at the project owner's explicit request) | 8 findings total (no new findings in the 2,112 cells read this round); documented in `Translation_Correction_Log.xlsx` |
| `english_review_data.py` decision-round structural check | `assert len(REVIEW) == 96` plus a per-question check that each of the 6 reviewed questions carries the correct `approval_status` (`accepted` x2, `accepted_user_revised` x2, `pending_clinical_review` x1, `deferred_pending_decision` x1) | Pass |
| `systems.en.revised.json` decision-round content check | Printed and checked each of the 6 reviewed questions' final `en` text against the project owner's instructions | Pass — `EYE05`/`SKIN07` match the AI proposal; `GU03`/`TRAUMA05` match the project owner's own wording exactly; `RESP05`/`ENT05` correctly excluded from the merged file |
| `translation_review_data.py` full-coverage structural check | `ALL_LANGS` (36 codes) matches `systems.languages.json`'s manifest exactly; `SPOT_CHECK_REMAINDER_LANGS == ALL_LANGS`; all 8 `ISSUES` still parse as valid strings (re-checked after the Russian/Hindi/Tamil edits) | Pass |
| Full-matrix cell-count check | `Translation_Clinical_Language_Review.xlsx` status-column counts sum to exactly 3,456 | Pass — 3,446 `no_issue_identified` + 2 `clinical_meaning_concern` + 6 `requires_native_speaker_review` + 1 `minor_language_improvement` + 1 `major_translation_error` = 3,456 |

## Tests NOT performed (explicitly, so scope is not overstated)

- **No native-speaker or professional medical-translator review** of any language. This remains
  true even after completing the full AI-read coverage — an AI read is not a substitute for it,
  and this report does not claim otherwise.
- **No browser/offline regression testing** this session — the live application
  (`index.html`, `sw.js`, `systems.en.json`, every `systems.translations.<code>.json`) has not
  been modified, so the existing regression suite (`test_systems.py`, `test_offline.py`,
  `test6.py`) and its last-known-clean results from the prior session remain the current, valid
  state. Re-running them now would test an unchanged application and was not repeated to avoid
  burning effort on a no-op.
- **No bespoke linguistic read remains outstanding.** The previous version of this report listed
  the ~61% of translation cells outside the original priority set as not individually read; that
  gap has now been closed — see the full-coverage row above.

## Phase D decision and its effect on testing scope

The project owner reviewed the 6 proposed English wording changes individually and gave a
specific, question-by-question decision on each (2 accepted as proposed, 2 accepted with their own
revised wording, 1 left pending clinical review, 1 deferred) — see `Translation_QA_Report.md` §3
for the full table. On translations, the project owner asked for the Tamil `NEURO03` finding to
be confirmed and the Russian/Hindi `CVS05` suggestions refined for natural wording, with every
change kept marked as unverified pending independent review — see `Translation_QA_Report.md` §4.2.
**Phase D integration itself was explicitly not authorised this round** — the project owner asked
for the revised proposals and updated correction log before any live-application change.

Consequence: `systems.en.json`, every `systems.translations.<code>.json`, `index.html` and
`sw.js` remain unchanged by this task. `systems.en.revised.json` is a proposed file only (4 of 96
questions differ from the live master); it is not wired into the application. No rebuild
occurred, so no new regression run was needed — the application's last known-clean regression
results from before this task remain current.

## Next testing step (once Phase D integration is authorised)

Once `systems.en.revised.json`'s accepted changes (and/or any applied translation corrections)
are merged into the live master and `index.html`/`sw.js` rebuilt:
1. Re-run `test_systems.py`, `test_offline.py`, `test6.py` (existing Playwright suite).
2. Offline spot-check of the brief's named representative languages: Arabic, Urdu, Ukrainian,
   Polish, Mandarin (Simplified), Tamil, Malayalam.
3. Confirm `GU03` and `TRAUMA05` — the two questions accepted with the project owner's own
   revised wording — render correctly in every language that was NOT re-translated to match the
   new English text (i.e. confirm the app does not silently show a now-mismatched old translation
   next to new English wording without at least an English fallback — same mechanism already used
   for `crossModuleFallback`).
4. If `ENT05`'s overlap with `GI10` is subsequently decided and its deferred wording
   (`deferred_proposed_text` in `english_review_data.py`) is adopted, repeat the same
   fallback-rendering check for `ENT05`.
5. If the Russian `CVS05`, Hindi `CVS05`, or Tamil `NEURO03` translation corrections are
   subsequently approved by a native-speaker reviewer, confirm the chosen replacement text (for
   Russian/Hindi, whichever of the two offered registers is selected) renders correctly and that
   the CVS05/NEURO11/TRAUMA05 (or NEURO03's own red-flag meaning) distinction is preserved in the
   running application, not just in the correction log.
