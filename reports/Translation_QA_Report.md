> **HISTORICAL DOCUMENT — superseded by `FINAL_RELEASE_REPORT.md`.** This file is kept for its audit trail (what was found/decided/tested at the time) but is no longer the authoritative statement of current status. Where anything below conflicts with `FINAL_RELEASE_REPORT.md`, the final release report is correct. Read that file first.

---

# Resus.ie — Translation QA Report
## Complete Language Extraction, Clinical Translation Review and Quality Assurance

**Date:** 2026-10-13 (updated same day with the project owner's decision round and the completed
full-coverage translation sweep)
**Scope:** Systems module, 96 questions, 36 languages (3,456 translation cells)
**Status:** Phases A, B and C complete, including the full 3,456-cell direct read requested in
the decision round below. Phase D (integration) remains **explicitly paused** — the project owner
has asked for the revised proposals and updated correction log first, and for Phase D not to
proceed yet. Nothing in this report has been applied to the live application.

---

## 1. What this report covers, and what it does not

This report summarises an AI-assisted review. It is **not** a substitute for, and does not
constitute, independent native-speaker review or professional medical-translation validation. No
translation in this project has been reviewed by a human qualified in the target language or in
medical translation. Every translation remains an unverified AI draft — this review does not
change that status for a single cell, and does not claim to. Per the project owner's explicit
instruction, **every change and finding below remains marked as unverified until independently
checked**, however confident the underlying AI analysis is.

What this review *did* do, concretely:
- Extracted and backed up all translation source files (Phase A).
- Reviewed all 96 English master questions against a 10-point rubric (Phase B).
- Ran an automated mechanical consistency check across all 3,456 translation cells (Phase C,
  step 1).
- **Directly read and clinically/linguistically assessed all 3,456 of those cells (100%)** — the
  30 priority question IDs across all 36 languages from the first pass, plus (completed in this
  decision round) the remaining 66 question IDs across all 36 languages. See §4 for detail.
- Took the project owner through a specific, question-by-question decision round on the 6
  proposed English wording changes (§3) and deepened two of the highest-priority translation
  findings at their explicit request (§4.2).

What it did *not* do: independent native-speaker or professional medical-translator review of any
cell. A completed AI read is not that, and is not represented as that anywhere in this project's
deliverables.

---

## 2. Phase A — Extraction

Full detail: `translations/systems/EXTRACTION_REPORT.md`. Unchanged since the previous version of
this report — Phase A was not revisited in this decision round.

- The embedded Systems translations in `index.html` were already byte-identical to the standalone
  `systems.translations.<code>.json` files — no data recovery was needed, only reorganisation,
  backup and reporting, consistent with the brief's own "reuse rather than extract duplicate
  copies" instruction.
- All 36 languages x 96 questions = 3,456 cells verified present and non-empty. Zero missing
  question IDs, zero duplicate keys, zero decode failures.
- The 36-language manifest matches the brief's own named list exactly (accounting for two
  cosmetic naming differences: "Mandarin Chinese" ↔ `zh-Hans`, and "Kurdish Sorani"/"Kurdish
  Kurmanji" ↔ `ku`/`kmr`, correctly kept distinct).
- 8 language codes exist on disk from an earlier, pre-36-language-spec batch (`bs, cs, sk, mk,
  ln, ko`, and an old Traditional-script `zh`) but are **outside** the current 36-language
  manifest — reported, not silently added or dropped.
- A complete backup of every file was made in `backup_original_translations/` before any review
  or correction work began.

## 3. Phase B — English master question review, and the project owner's decision round

Full detail: `English_Question_Review.xlsx`, `english_review_data.py`, `systems.en.revised.json`.

All 96 questions (102 rows in the review table, since 6 question IDs are intentionally listed
under two clinical systems each) were assessed against the brief's 10-point rubric, producing 6
proposed wording changes. The project owner has now reviewed all 6 individually and given a
specific decision on each — not a blanket approval or rejection:

| Question | AI proposal | Project owner's decision | Status |
|---|---|---|---|
| `SKIN07` | "Has your skin been painful?" | **Accepted as proposed.** | `accepted` |
| `EYE05` | "Does bright light hurt your eyes?" | **Accepted as proposed.** | `accepted` |
| `GU03` | (AI wording) | **Accepted, with the project owner's own revised wording:** "Have you had a sudden urge to pass urine that was difficult to hold?" — supersedes the AI's original suggestion. | `accepted_user_revised` |
| `TRAUMA05` | (AI wording) | **Accepted, with the project owner's own revised wording:** "Did you black out after the injury?" — supersedes the AI's original suggestion and resolves the open clinical-content question this item was flagged for. | `accepted_user_revised` |
| `RESP05` | (AI wording) | **Left as proposed, pending further clinical review.** Not yet approved for integration. | `pending_clinical_review` |
| `ENT05` | Add disambiguating context vs. `GI10` | **Deferred — reverted to its existing (unchanged) wording** pending a decision about the overlap with `GI10`. The AI's shelved suggestion is preserved in the data (`deferred_proposed_text`) in case the overlap decision favours it later, but it is not live anywhere. | `deferred_pending_decision` |

Supporting findings, unchanged from the first pass:
- **90 of 96 questions: no change proposed.** The existing English question bank was already
  well-drafted — plain register, single symptom per question, clinically load-bearing
  distinctions preserved (pain vs. discomfort, fainting vs. unconsciousness, dizziness vs.
  vertigo, laterality, sudden onset, etc.).
- **5 cross-question findings** spanning multiple IDs, including the `GI10`/`ENT05` near-duplicate
  finding that is the reason `ENT05` was deferred rather than decided outright. Full detail in the
  workbook's "Cross-Question Findings" sheet.
- A possible **content gap** was flagged for clinical-governance consideration (not acted on): no
  question in the 96-question bank directly screens breathing *rate* (tachypnoea) as distinct
  from difficulty/effort breathing.

`systems.en.revised.json` has been rebuilt to reflect this decision round precisely: it merges in
**only** the two `accepted`/`accepted_user_revised` questions that already had concrete proposed
text at the time the merge logic runs — `EYE05`, `GU03`, `SKIN07`, `TRAUMA05` (4 questions
changed from the live master). `RESP05` (`pending_clinical_review`) and `ENT05`
(`deferred_pending_decision`) are intentionally **not** merged in, even though both went through
review, because neither has been approved for integration. A full `_approvalStatus` record for
all 96 questions is embedded in the file for traceability. **`systems.en.json` (the live master)
remains completely unmodified.**

## 4. Phase C — Translation audit across 36 languages: now 100% directly read

Full detail: `Translation_Clinical_Language_Review.xlsx` (all 3,456 cells),
`Translation_Correction_Log.xlsx` (concrete findings), `translation_review_data.py` (source data
and full methodology note).

### 4.1 Mechanical pass (100% coverage)
Clean. No missing/extra question IDs, no empty cells, no script mismatches, no RTL-flag
inconsistencies, no untranslated-looking text in any language. The only automated flags were
length-ratio outliers for Chinese (Simplified) and Cantonese — expected and benign, since
logographic scripts are naturally far more compact than English; **not** a translation defect.

### 4.2 Direct clinical/linguistic read-through — now 3,456 of 3,456 cells (100%)

The prior version of this report directly read 1,344 of 3,456 cells (~39%): the 30
Emergency-Department priority question IDs across all 36 languages, plus the remaining 66
question IDs in 4 representative languages. **At the project owner's explicit request — "please
complete the remaining 2,112 entries, explicitly recording which were genuinely assessed and
which require native-speaker review" — the remaining 2,112 cells (the 66 non-priority question
IDs across the other 32 languages) have now also been individually read and assessed.** Every one
of the 3,456 cells in the matrix now carries `review_method: ai_linguistic_review`; none fall
back to a mechanical-check-only default. `Translation_Clinical_Language_Review.xlsx`'s status
column reflects this directly — its `requires_native_speaker_review` rows are now a deliberate
per-finding classification (6 of the 8 correction-log items), not a blanket catch-all for unread
cells.

**No 9th issue was found.** All 2,112 newly-read cells classified `no_issue_identified`,
including an explicit per-language check, in every one of the 32 languages, of the two
cross-question patterns the task brief calls out: `GU07` (flank/side pain) vs. `MSK06` (back
pain) staying lexically distinct, and `GI10`/`ENT05` (swallowing) correctly mirroring their
English-level near-duplication rather than introducing a new translation-level ambiguity.

**8 concrete findings** (unchanged in count, two deepened at the project owner's request — see
below), overwhelmingly concentrated in the `CVS05` / `NEURO11` / `TRAUMA05`
fainting-vs.-unconsciousness cluster the brief itself flags as a known risk area.

| # | Question(s) | Language | Category | Severity | Confidence | Summary |
|---|---|---|---|---|---|---|
| 1 | CVS05 | Russian | clinical_meaning_concern | High | High | **Updated this round.** Still flags that the existing text collapses CVS05 into NEURO11/TRAUMA05. Primary suggestion revised to a more natural, patient-facing phrasing — "Вы падали в обморок?" (colloquial, "did you fall into a faint") — with the previous, more clinical noun-phrase wording "У вас был обморок?" kept as an alternate. Either phrasing preserves the three-way distinction; the choice between them is a register preference for a native speaker to confirm. |
| 2 | CVS05 | Hindi | clinical_meaning_concern | High | Medium | **Updated this round.** Primary suggestion revised to a colloquial Hindi-Urdu-belt term — "क्या आपको गश आया है?" (गश) — judged more natural and patient-friendly than the more Sanskritized "क्या आपको मूर्छा आई है?" (मूर्छा), which is kept as an alternate for regions/registers where it reads more appropriately. Confidence remains medium pending native-speaker confirmation of the regional register preference. |
| 3 | NEURO03 | Tamil | major_translation_error | High | **High (upgraded from Medium)** | **Confirmed this round, at the project owner's explicit priority request.** A full morphological decomposition of the existing Tamil text was performed: the suffix `-க்காத` in அனுபவிக்காத is Tamil's standard negative relative-participle marker (the same productive pattern as படிக்காத பையன் = "the boy who has *not* studied"), which grammatically proves the existing text inverts "ever had" into "has never experienced" on the single highest-stakes red-flag question (subarachnoid-haemorrhage screening) in the Neuro cluster. This raises confidence in the AI's own grammatical analysis from medium to high — it does **not** constitute native-speaker sign-off, and the finding remains an unverified AI suggestion pending one, per the project owner's standing instruction. |
| 4 | CVS05 | Urdu | requires_native_speaker_review | Medium | Low | Unchanged. Shares the same root word as NEURO11/TRAUMA05; unclear if this is a meaningful distinction in natural Urdu. |
| 5 | CVS05 | Malayalam | requires_native_speaker_review | Low | Low | Unchanged. Related root to NEURO11, different compound — likely fine, needs confirmation. |
| 6 | CVS05 | Gujarati | requires_native_speaker_review | Low | Low | Unchanged. Same pattern as Malayalam. |
| 7 | GI03/GI04/TRAUMA06 | Tigrinya | requires_native_speaker_review | Medium | Low | Unchanged. The verb used for "vomited" (ተመሊስካ, literally "returned") is given a clarifying gloss by the translator in GI03 but not in GI04/TRAUMA06 — an internal-consistency flag, not a confirmed error, in one of the two lowest-confidence languages in this project. |
| 8 | CVS06 | Latvian | minor_language_improvement | Low | Medium | Unchanged. "Lying flat" translated narrowly as "lying on your back" — unlikely to change a patient's actual answer in practice, flagged for confirmation. |

`Translation_Correction_Log.xlsx` now includes an "Alternate Suggestion (if any)" column
recording the Russian and Hindi CVS05 alternates above, so a native-speaker reviewer can choose
between the two registers rather than being handed only one option.

**Everywhere else in the full 3,456-cell matrix** — the entire fainting/LOC cluster in every
language, the full stroke-symptom cluster, headache cluster, melaena/haematemesis, urinary
retention, trauma/head-injury cluster, and now also every GI, GU, MSK, ENT, Skin, Eye and General
question in all 36 languages — the translations were assessed as natural, patient-facing, and
clinically faithful.

### 4.3 What "100% directly read" does and does not establish

Every cell's classification now reflects an actual AI read of that specific text, not a
mechanical-pass default. It does **not** mean every cell is clinically approved or
linguistically verified. Per the project owner's explicit instruction, **all 8 findings, and
every "no issue identified" classification, remain unverified AI judgments** pending independent
native-speaker or professional medical-translator review. A specific tier of languages is flagged
for extra caution regardless of a clean AI read — generally lower-resourced languages in the
underlying model: `ps, ku, ka, lt, lv, bg, ti, am, yue-Hant, kmr, ta, ml, pa, gu, so`.

## 5. Languages and questions requiring priority human review

In order of urgency:

1. **Tamil `NEURO03`** — grammatically confirmed (not merely suspected) negation inversion on a
   red-flag SAH-screening question. Single highest-priority item in this entire audit; now
   high-confidence in the AI's own analysis, but still requires native-speaker sign-off before any
   change is applied.
2. **Russian and Hindi `CVS05`** — the fainting/loss-of-consciousness clinical distinction is
   fully lost in both languages' existing text. Two candidate replacement phrasings are now
   offered for each (one more colloquial/patient-friendly, one more formal/clinical) for a native
   speaker to choose between.
3. **Tigrinya and Kurdish Kurmanji**, generally — the two lowest-confidence languages in this
   project (per this and earlier QA reports) — recommend both be prioritised for full
   native-speaker review ahead of every other language.
4. **All 36 languages, all 3,456 cells** — this review is now complete in its AI-read coverage,
   but that coverage narrows, rather than replaces, the need for full native-speaker/qualified-
   medical-translator review across every language, as stated throughout this project's QA
   history.

## 6. Provenance and status — unchanged

No translation's `provenance`/`status` metadata has been altered by this review. Every
`systems.translations.<code>.json` file still correctly records `status: "draft"` and
`provenance.source: "ai_draft"` / `needs_human_review: true`. This review does not and cannot
upgrade that status — only independent native-speaker or professional medical-translator review
can do that.

## 7. Phase D — explicit decision: still paused, nothing applied to the live application

Per the task brief's own implementation sequence: *"Phase D — Integration: After approval of the
English changes, update the translation source files. Rebuild the application. Verify offline
behaviour and existing functionality."*

The project owner has now reviewed both proposal sets in detail (§3, §4) and given specific,
question-by-question and finding-by-finding decisions — but has explicitly instructed that **Phase
D integration is not to proceed yet**, and that the revised proposals and updated correction log
be provided first. Accordingly:

- **English wording changes:** 4 of 6 accepted (2 as proposed, 2 with the project owner's own
  revised wording) and captured in `systems.en.revised.json`; 1 left pending clinical review; 1
  deferred. **`systems.en.json` (the live master) has not been touched** — `systems.en.revised.json`
  remains a proposed file only, not wired into the application.
- **Translation corrections (all 8):** none applied. Two of the three findings with a concrete
  suggested replacement (Russian `CVS05`, Hindi `CVS05`) have been deepened with a natural
  alternate phrasing at the project owner's request; the Tamil `NEURO03` finding has been
  confirmed with a full grammatical proof. All 8 remain explicitly unverified. Every
  `systems.translations.<code>.json` file remains completely unchanged.

**Consequence: the live application (`systems.en.json`, every `systems.translations.<code>.json`,
`index.html`, `sw.js`) is byte-for-byte unchanged by this entire review**, from Phase A through
this report. There is nothing to rebuild, no cache-version bump, and no new regression testing
needed — the application is in exactly the state it was in before this task began, and its last
known-clean regression results (see the project's standing CHANGELOG/QA history) still apply.

If and when Phase D is authorised, integration remains mechanically straightforward:
`render_index.py` already builds `index.html` correctly from the separate source files (confirmed
in Phase A — no code change needed there), so integration would be a matter of updating the
relevant source JSON file(s) per the now-finalised decision record in `systems.en.revised.json`'s
`_approvalStatus`, rebuilding, bumping `sw.js`'s `CACHE_NAME`, and re-running the existing
regression suite plus an offline spot-check of the representative languages the brief names
(Arabic, Urdu, Ukrainian, Polish, Mandarin, Tamil, Malayalam).
