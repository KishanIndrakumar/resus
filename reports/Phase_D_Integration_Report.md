> **HISTORICAL DOCUMENT — superseded by `FINAL_RELEASE_REPORT.md`.** This file is kept for its audit trail (what was found/decided/tested at the time) but is no longer the authoritative statement of current status. Where anything below conflicts with `FINAL_RELEASE_REPORT.md`, the final release report is correct. Read that file first.

---

# Resus.ie — Phase D Integration Report (Development Release)

**Date:** 2026-10-13
**Status: DEVELOPMENT RELEASE ONLY.** Nothing in this release has been clinically validated or reviewed by a native speaker or qualified medical translator. It is **not** suitable to replace a qualified interpreter. This report exists to make exactly that point unambiguous, alongside a complete record of what changed and what remains outstanding.

This report documents Phase D: integrating the decision-round changes from `Translation_QA_Report.md` into the live application, per the project owner's explicit instructions. It supersedes the Phase D section of `Testing_Report.md` (which recorded that Phase D had *not* yet been authorised) for everything that follows.

---

## 1. What was authorised, and what this release does

The project owner's instructions were specific and itemised, not a blanket "integrate everything." This release applies exactly what was authorised:

| Item | Instruction | Action taken |
|---|---|---|
| `SKIN07` (English) | Accept | Applied to `systems.en.json` |
| `EYE05` (English) | Accept | Applied to `systems.en.json` |
| `GU03` (English) | Accept, with the project owner's own wording | Applied to `systems.en.json` |
| `TRAUMA05` (English) | Accept, with the project owner's own wording | Applied to `systems.en.json` |
| `RESP05` (English) | Keep unchanged | **Not** changed — still "Have you noticed unusual sounds when breathing?" |
| `ENT05` (English) | Keep unchanged | **Not** changed — still "Have you had difficulty swallowing?" |
| `GU03`/`TRAUMA05` translations | Update to match revised English meaning, retain unverified status | Retranslated in all 36 languages; still unverified AI drafts |
| Tamil `NEURO03` | Prioritise, correct, flag clearly for independent confirmation | Applied to `systems.translations.ta.json`; flagged in-file and in the correction log |
| Russian/Hindi `CVS05` | Keep as proposed, do not silently mark approved | **Not** applied — both remain exactly as they were; suggestions remain proposals in `Translation_Correction_Log.xlsx` only |
| All 36 language files, backups, correction logs | Preserve | Preserved — see §6 |
| `index.html` | Rebuild via `render_index.py` | Rebuilt |
| `sw.js` cache version | Bump | `edrt-v12` → `edrt-v13` |
| Testing | Full 96×36 matrix + cross-module regression | Done — see §4 |
| No redesign / no runtime language downloads | Preserve architecture | Preserved — same embedded-translations design, same build process, no new runtime fetches |

---

## 2. English master changes (`systems.en.json`, `contentVersion` 1.1-draft → 1.2-draft)

| Question | Old text | New text (now live) |
|---|---|---|
| `SKIN07` | Have you had pain in your skin? | Has your skin been painful? |
| `EYE05` | Has bright light hurt your eyes? | Does bright light hurt your eyes? |
| `GU03` | Have you suddenly needed to pass urine urgently? | Have you had a sudden urge to pass urine that was difficult to hold? |
| `TRAUMA05` | Did you lose consciousness? | Did you black out after the injury? |

`RESP05` and `ENT05` are confirmed byte-for-byte unchanged in the live file.

**Meaning-impact assessment** (why only 2 of the 4 needed translation updates): `SKIN07` and `EYE05` are pure grammar/register smoothing — the clinical meaning is identical, so their existing translations in all 36 languages already express that same meaning and were left untouched. `GU03` and `TRAUMA05` changed meaning: `GU03` adds an explicit "difficult to hold" qualifier (moving the question closer to the urinary-urgency/incipient-urge-incontinence concept); `TRAUMA05` adds an explicit "after the injury" temporal anchor and switches from "lose consciousness" to the more colloquial "black out," which also helps distinguish it from `NEURO11` ("Have you lost consciousness?") in languages where both questions previously used identical wording. Both were therefore retranslated into all 36 languages (§3).

---

## 3. Translation changes

### 3.1 `GU03` and `TRAUMA05` — retranslated in all 36 languages

Every one of the 36 `systems.translations.<code>.json` files has new text for `GU03` and `TRAUMA05`, matching the new English meaning. Where a natural, distinct colloquial equivalent of "black out" was available, it was used for `TRAUMA05` to help separate it from `NEURO11`'s "lost consciousness" phrasing (e.g. French *"avoir un trou noir"*, German *"weggetreten sein"*, Italian *"un mancamento"*, Turkish *"gözünüz karardı"*); where a confidently distinct idiom was not available (several of the lower-confidence-tier languages), the translation stays accurate to the new English and relies on the added "after the injury" context for disambiguation rather than inventing an idiom this reviewer isn't confident in.

**All 36 of these retranslations are unverified AI drafts.** Each file's `provenance.needs_human_review` remains `true`, `status` remains `"draft"`, and a new `provenance.phaseD_update` field records that `GU03`/`TRAUMA05` were updated on 2026-10-13 to match the revised English master.

Affected languages (all 36): uk, ru, ro, pt, pl, ar, es, zh-Hans, ur, so, fr, fa, ps, bn, hi, pa, tr, ka, lt, lv, bg, sq, ku, ti, am, vi, yue-Hant, kmr, ta, ml, it, de, hu, el, ja, gu.

### 3.2 Tamil `NEURO03` — corrected and applied, flagged for priority confirmation

| | |
|---|---|
| Old text (inverted negation) | இது நீங்கள் என்றுமே அனுபவிக்காத மோசமான தலைவலியா? ("...the worst headache you have **never** experienced") |
| New text (now live) | இது இதுவரை நீங்கள் அனுபவித்ததிலேயே மிக மோசமான தலைவலியா? ("...the worst headache you have **ever** experienced, so far") |

This is the **only** one of the 8 translation-correction-log findings applied to a live file in this release, at the project owner's explicit instruction to prioritise it. The grammatical basis is strong — the suffix `-க்காத` is Tamil's standard negative relative-participle marker — but this remains an **AI grammatical analysis, not an independent Tamil-speaker confirmation**. `systems.translations.ta.json` now carries a `provenance.priority_native_speaker_review` entry naming this exact change, the reason, the before/after text, and an explicit instruction not to treat it as clinically verified. `Translation_Correction_Log.xlsx`'s new "Applied to Live Files" column records the same.

### 3.3 Russian and Hindi `CVS05` — confirmed NOT applied

Both remain byte-for-byte unchanged from before this release:
- Russian: "Вы теряли сознание?" (unchanged — still collapses into the same wording as `NEURO11`/`TRAUMA05`'s pre-Phase-D phrasing)
- Hindi: "क्या आप बेहोश हुए हैं?" (unchanged — same collapse)

The refined, more natural-register suggestions for both (with a formal alternate for each) remain in `Translation_Correction_Log.xlsx` as proposals only, explicitly not approved, per the project owner's instruction not to silently mark them approved.

---

## 4. Testing performed

| Test | Method | Result |
|---|---|---|
| `systems.en.json` structural check | 96 questions present; only the 4 approved questions differ from the pre-Phase-D snapshot; `RESP05`/`ENT05` confirmed unchanged | Pass |
| All 36 translation files — ID/structure check | Every file has exactly the 96 English question IDs, `status: "draft"`, `needs_human_review: true` | Pass |
| `render_index.py` rebuild | `index.html` regenerated from the updated source files | Pass — 36 drafted languages embedded, no unreplaced template placeholders |
| Embedded-data spot check | Extracted `SYS_EN`/`SYS_TR`/`SYS_LANGS` blobs directly from the rebuilt `index.html` and confirmed the 4 English changes, the Tamil fix, and the untouched Russian/Hindi CVS05 text are all present exactly as intended | Pass |
| `sw.js` cache version | `CACHE_NAME` bumped `edrt-v12` → `edrt-v13` | Done |
| `test_systems.py` (existing suite) | Full Playwright run | Pass — 0 console errors |
| `test_offline.py` (existing suite) | Full Playwright run, fully offline | Pass — 0 console errors |
| `test6.py` (existing suite) | Full Playwright run | Pass — 0 console errors |
| `test_phaseD_full_matrix.py` (new) | Exercises the app's own `sysGetTranslation()` function for all 96 questions × 36 languages (3,456 cells), online and then fully offline (network disabled, service-worker cache only) — checks for missing/blank/unexpected-English-fallback cells, and verifies the exact new text for `SKIN07`/`EYE05`/`GU03`/`TRAUMA05`/Tamil `NEURO03`, and the unchanged `RESP05`/`ENT05`/Russian `CVS05`/Hindi `CVS05` | Pass — 0 missing, 0 blank, 0 unexpected fallbacks across both passes (6,912 lookups total); 0 console errors |
| `test_phaseD_modules.py` (new) | Walks Patient Details, Pain, Time/Onset, Allergies, Medications, Medical Background, Pregnancy, Neuro (incl. Stroke rapid-access banner and its "not a validated stroke assessment" disclaimer), Examination, Interpreter, Other, and confirms the Systems module home screen is reachable | Pass — 0 console errors, Stroke disclaimer wording intact |
| Obsolete pre-redesign scripts (`test.py`, `test2.py`, `test3.py`) | Attempted run | **Fail by design, not a regression** — these three scripts hardcode a click on `[data-shortcut="symptoms"]`, a home-screen shortcut that was intentionally removed when the Systems module was first built (superseded by Systems; `test_systems.py` itself asserts this element has count 0). They predate the current three-script regression suite (`test_systems.py`, `test_offline.py`, `test6.py`) named in `Testing_Report.md` and are not part of it. No action needed. |

**Net result: zero regressions, zero console errors, across the full existing suite plus two new Phase-D-specific checks covering the complete 96×36 translation matrix and every named clinical module.**

---

## 5. Complete list of what remains unverified

**Every translation in every one of the 36 languages remains an unverified AI draft**, including the ones just changed in this release. Nothing in this release upgrades any cell's `provenance.needs_human_review` (still `true` everywhere) or `status` (still `"draft"` everywhere). In priority order:

1. **Tamil `NEURO03`** (just corrected, applied) — grammatically well-supported but not independently confirmed. Highest-priority item for native-speaker sign-off.
2. **`GU03` and `TRAUMA05` in all 36 languages** (just retranslated) — new AI drafts, same unverified status as every other translation in the project; not yet read by a native speaker.
3. **Russian and Hindi `CVS05`** (unchanged, proposals only) — still collapse into `NEURO11`/`TRAUMA05`'s wording; refined suggestions await native-speaker confirmation before any future application.
4. **The other 5 translation-correction-log findings** (Urdu/Malayalam/Gujarati `CVS05`, Tigrinya `GI03`/`GI04`/`TRAUMA06`, Latvian `CVS06`) — unchanged, proposals only, per `Translation_Correction_Log.xlsx`.
5. **All remaining 3,443 cells across all 36 languages** that were read and classified `no_issue_identified` in the Phase C audit — an AI read is not a substitute for independent native-speaker or professional medical-translator review, and none of them have had one.
6. **`RESP05` and `ENT05`** — unchanged by design; `RESP05` awaits further clinical review, `ENT05` awaits a decision on its overlap with `GI10`, before either is revisited.

**In short: 100% of the translation content in this application is still an unreviewed AI draft.** This release changes *which specific wording* is drafted for 3 questions (`GU03`, `TRAUMA05`, Tamil `NEURO03`) across the relevant languages; it does not change the fact that none of it has been clinically or linguistically verified by a qualified human.

---

## 6. Preservation confirmation

- All 36 `systems.translations.<code>.json` files remain present, matching the 36-language manifest exactly.
- The original Phase A pristine backup (`backup_original_translations/`) is untouched — nothing in this release wrote to or over it.
- A new pre-Phase-D snapshot (`pre_phaseD_snapshot/`) was taken of every translation file and `systems.en.json` immediately before any Phase D edit, as an additional safety net specific to this release.
- `Translation_Correction_Log.xlsx` (all 8 findings, including the one now applied) and `Translation_Clinical_Language_Review.xlsx` (full 3,456-cell matrix) are both preserved and have been re-run through `recalc.py` with 0 errors.

---

## 7. What this release is, and is not

This is a **development release**. It demonstrates that the project owner's decision-round changes build, render, and pass the full regression suite correctly. It does **not** constitute clinical sign-off on any translation, including the ones corrected or newly drafted in this release. No question or answer option in this application should be treated as suitable to replace a qualified interpreter until it has been independently reviewed by a native speaker or qualified medical translator, per every QA report produced for this project to date.
