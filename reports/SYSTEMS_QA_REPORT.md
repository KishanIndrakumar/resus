> **HISTORICAL DOCUMENT — superseded by `FINAL_RELEASE_REPORT.md`.** This file is kept for its audit trail (what was found/decided/tested at the time) but is no longer the authoritative statement of current status. Where anything below conflicts with `FINAL_RELEASE_REPORT.md`, the final release report is correct. Read that file first.

---

# Systems Module — Translation QA Report (updated: 36-language architecture)

> ⚠️ **Display-behaviour change, read this first:** as of this update, drafted-language translations display **directly to the user, with no "unreviewed AI draft" gate and no on-screen AI-draft warning** — this was an explicit client decision (see CHANGELOG "unreviewed-draft gate removed"), made after being told that none of these 28 languages have been reviewed by a native speaker or qualified medical translator. Everything below about review status is still fully accurate and still the most important open item — it simply no longer has a UI safeguard reminding the user of it at the point of use. Treat clinical sign-off and native-speaker review as more urgent, not less, now that the app itself no longer flags these as unreviewed.

Generated automatically against `systems.languages.json` (the manifest) and each `systems.translations.<code>.json` file, checked against `systems.en.json`. 96 questions, 36 target languages (+ English as source).

**This report supersedes the prior 34-language, single-file report.** The underlying translation architecture changed (one JSON file per language + a manifest, replacing the single `systems.translations.draft.json` blob) to meet a new, more specific client brief; see `CHANGELOG.md` for the full architecture change. Translation **content** for the 28 languages carried over from the old batch is unchanged; two languages (Polish, Simplified Mandarin) are newly translated; eight languages are honestly marked `pending` (not drafted at all), per the brief's own instruction to prioritise the 10 core languages first.

## Completion status

| | |
|---|---|
| Total target languages | **36** (Priority 1: 10, Priority 2: 16, Priority 3: 10) |
| Languages with all 96 questions drafted | **36 / 36 — complete** |
| Languages `pending` (no draft at all) | **0 / 36** — the final 8 (`ka` Georgian, `lt` Lithuanian, `lv` Latvian, `bg` Bulgarian, `ti` Tigrinya, `yue-Hant` Cantonese/Traditional script, `kmr` Kurdish-Kurmanji, `ml` Malayalam) were drafted in this update |
| **Priority 1 (core, 10 languages) completion** | **10 / 10 — fully drafted** |
| Priority 2 (16 languages) completion | **16 / 16 — fully drafted** |
| Priority 3 (10 languages) completion | **10 / 10 — fully drafted** |
| Key / ID mismatches | None — all 96 IDs present (as either text or explicit `null`) in every language file |
| Accidental English fallbacks | None found — every drafted cell is a genuine translation, never copied English text; every `pending` cell is explicit `null`, never blank or defaulted to English |
| Duplicate keys | None |

**Honesty check (per the brief's own instruction, "do not silently fall back to English"):** every one of the 36 drafted languages has all 96 questions translated — none are partially drafted, and there are no more `pending` languages at all. **None of the 36 drafted languages — old batch, the two 2025 additions (Polish, Simplified Mandarin), or the 8 most-recently-completed (Georgian, Lithuanian, Latvian, Bulgarian, Tigrinya, Cantonese-Traditional, Kurdish-Kurmanji, Malayalam) — has been reviewed by a native-speaker clinician or professional medical translator.** Full draft coverage of a language is not the same as clinical sign-off; see "What's needed before clinical use" below.

**Translation-style recheck (added this update):** at the client's request, a spot-check was done across a sample of higher-resource languages (Spanish, Arabic, French, Hindi, Urdu, Simplified Mandarin, Polish, Somali, Pashto, Kurdish Sorani) against ten of the highest-risk/most idiom-prone questions, specifically checking for literal/word-for-word translation versus natural, context-appropriate ED-patient phrasing. Result: the existing drafts already use natural idioms and correct formal register (e.g. French's "mal au ventre" rather than a literal rendering, Polish/German/French's polite-address conjugations), consistent with the project's original drafting brief. No word-for-word artifacts were found in the sampled languages. This is a style spot-check, not a substitute for native-speaker or clinical-terminology review — it confirms the drafting *approach* held up under self-review, not that every one of the 36×96 lines is clinically and linguistically correct.

## Automated checks (re-run against the new per-language files)

- **Null/gap check:** 0 languages have a partial draft (either all 96 questions present, or all 96 explicitly null). No language is silently incomplete.
- **Duplicate text within a language, across different question IDs:** the same `NEURO11` / `TRAUMA05` pair flagged in every prior report recurs in **26 of the 28 drafted languages**, including both newly-translated languages (Polish, Simplified Mandarin). This is expected, not a new defect — the English source questions are themselves near-duplicates:
  - `NEURO11`: "Have you lost consciousness?" (general neuro screening)
  - `TRAUMA05`: "Did you lose consciousness?" (post-injury screening)
  
  In Russian and Hindi, `CVS05` ("Have you fainted?") also collapses to the same wording as the other two. **This is still an open clinical-content decision, carried over unchanged from every prior QA report** — see recommendation below; it has not been resolved by this architecture change, and translating two new languages (Polish, Simplified Mandarin) reproduced the exact same pattern, which is further evidence it is a property of the English source wording, not of any one translation pass.
- **Suspiciously short entries (<8 characters):** 21 flagged across the 28 previously-drafted languages (not yet re-run against the 8 newly-added ones). All are false positives on inspection: short, grammatically complete clinical questions in the relevant script (e.g. short Chinese/CJK questions, `Caiu?` Portuguese, `A ranë?` Albanian). No action needed.
- **Suspiciously long entries (>140 characters):** none found.
- **Clinical wording concerns to flag for review (beyond the duplicate above):**
  - `GU03` / `GU04` / `GU08` (urinary urgency, haematuria, incontinence) and `NEURO03` ("worst headache ever") remain the highest-acuity red-flag questions across all drafted languages — reviewers should prioritise these first in every language, Priority-1 languages first of all.
  - `TRAUMA05` vs `NEURO11` vs `CVS05` — see duplicate finding above; this recurs in the 8 newly-drafted languages too, confirming again that it's a property of the English source wording.
  - Lower-resource languages (`ku` Kurdish Sorani, `ps` Pashto, and — newly — `ti` Tigrinya and `kmr` Kurdish-Kurmanji) were drafted with lower underlying model confidence than the higher-resource/Priority-1 languages. Not flagged as wrong, but should be **prioritised early** for native-speaker review precisely because translation confidence is lowest there.
  - One disambiguation made during this update: Latvian's `ENT04` (sore throat) was translated as "rīkle" rather than the more ambiguous "kakls" (which can mean either "throat" or "neck"), to keep it distinct from `MSK07` (neck pain), which correctly uses "kakls."
  - Source English (`systems.en.json`) was not altered. Any wording concerns about the English source itself are a separate, pre-existing item — see the main redesign changelog.

## Provenance

Every drafted language's `systems.translations.<code>.json` carries its own `provenance` block: `source: "ai_draft"`, `needs_human_review: true`, `generated` (date), `generated_by: "Claude (Sonnet 5), as a translation draft — not a qualified medical translator"`. Every `pending` language's file carries `provenance: {source: null, needs_human_review: null, generated: null, generated_by: null}` and all-`null` questions — an honest "nothing has been generated for this language yet" record, not a placeholder claiming draft status it doesn't have. **None of the Systems-module translations, in any language, have been reviewed by a native-speaker clinician or professional medical translator.** This is distinct from the legacy phrasebook content, which is reproduced from the published British Red Cross / NHS source material and carries that source's own review history.

## What's needed before clinical use

0. **(Still the most urgent item, though partially mitigated.)** A small "AI translated" tag now appears next to the translated text for every drafted language (see CHANGELOG "Change #5") — this is a lightweight visibility cue, not a safety gate: it does not block or hide the text, require a click, or explain what "unreviewed" means. It is a real improvement over showing nothing, but it is **not equivalent** to the previous full gate/banner, and it does not reduce how urgent native-speaker review is. Until that review happens, anyone relying on a drafted translation has only a small tag, not a warning, as the in-app signal that it hasn't been checked.
1. Native-speaker / qualified medical-translator review of all **36** drafted languages (now 0 pending), prioritising:
   - All 10 Priority-1 (core) languages first, per the brief's own instruction.
   - The red-flag questions listed above, in every language.
   - Lower-resource languages (`ku` Sorani, `ps` Pashto, `ti` Tigrinya, `kmr` Kurdish-Kurmanji, and other less-common languages outside Priority 1) next, since translation confidence is lowest there.
2. ~~Drafting the remaining 8 Priority-2/3 `pending` languages~~ — **done**: all 8 (`ka, lt, lv, bg, ti, yue-Hant, kmr, ml`) are now drafted; 36/36 complete.
3. A decision on the `NEURO11` / `TRAUMA05` / `CVS05` wording-overlap finding — confirmed again across the 8 newly-drafted languages in this update; should be resolved once (by adjusting the English source wording if needed) rather than per-language, per-batch.
4. Sign-off from clinical governance on the Systems question set itself (`systems.en.json`) — unchanged across every translation pass so far; the brief asked for any proposed English wording changes to be separately documented, and none have been made.
5. A decision on the access-control/mode-mechanism gap noted in `SETUP_AND_REMAINING_ISSUES.md` — now more relevant with 36/36 languages drafted (previously 28/36), since every non-English, non-reviewed user will encounter the drafted translation directly with no in-app "unreviewed" indicator at all.
