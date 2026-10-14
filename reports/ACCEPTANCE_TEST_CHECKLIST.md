> **HISTORICAL DOCUMENT — superseded by `FINAL_RELEASE_REPORT.md`.** This file is kept for its audit trail (what was found/decided/tested at the time) but is no longer the authoritative statement of current status. Where anything below conflicts with `FINAL_RELEASE_REPORT.md`, the final release report is correct. Read that file first.

---

# Manual acceptance-test checklist — Systems module

Automated checks already run (see CHANGELOG / QA report): Playwright walkthrough at a 390×780 viewport, zero console errors, legacy modules unaffected, gated/revealed translation states both verified, orphaned legacy phrase IDs still browsable. The following still need a human pass before clinical use:

## Navigation & data integrity
- [ ] Home screen: "Systems" row visible and prominent; "Associated Symptoms" is gone; all other categories unchanged.
- [ ] Each of the 11 systems opens its correct question list and count.
- [ ] A question that belongs to two systems (e.g. `NEURO09`, `MSK06`) shows the *same* recorded answer in both places — confirm editing it in one system updates the other.
- [ ] Deep-link / direct reload at each major view (`index.html`, after navigating into Systems) still works under both a GitHub Pages subpath and a custom domain root — test both if possible.

## Session-state workflow
- [ ] Answer several questions, navigate Home → back into Systems → confirm answers are still there (session, not page, must be preserved).
- [ ] Refresh the browser tab — confirm all answers are gone (session-only is working as intended, nothing persisted).
- [ ] Use Back/Previous, Skip (tap Next without answering), and Edit (reopen an answered question and change it) — confirm no answer is lost accidentally and edits overwrite cleanly.
- [ ] Reset a system — confirm a confirmation step appears, cancelling changes nothing, and confirming clears only that system's answers.

## Summary & Time/Onset hand-off
- [ ] Record a mix of Yes/No/Don't know/Don't understand/unanswered in one system; open its summary; confirm each section lists the right items and "No" shows only a count.
- [ ] Select two or more "Yes" items and record onset/duration for them; confirm the calendar/clock reference opens for exactly those items and returns to the summary afterward with no data lost.
- [ ] From the summary, tap "Edit" on a Don't-know/Don't-understand item — confirm it reopens the correct question.
- [ ] Open the cross-system "Review all recorded answers" entry from the Systems home screen (visible once anything is recorded) — confirm it aggregates correctly across systems.

## Translation display (safety-relevant — check carefully)

**Note: language selection is now shared across the whole app** (one language, used everywhere it's supported) — per explicit client decision. The Systems module and the legacy phrasebook still each have their own picker *screen* (different layout — Systems groups by priority tier, legacy is a flat grid — and a different underlying language list), but picking a language in either one now sets it for both.
- [ ] From inside a Systems question, tap the header globe button — confirm it opens the *Systems* picker (banner text mentions "Systems question bank"), not the legacy one.
- [ ] Pick a different language there, return to the question — confirm the header label and the translated question text both show the newly picked language, with no mismatch.
- [ ] From a legacy-phrasebook screen (e.g. Pain), tap the header globe button — confirm it still opens the legacy picker, and picking a language there is also reflected next time you open Systems.
- [ ] Pick a language that's in BOTH lists (e.g. Arabic) in either module — confirm the other module shows it too.
- [ ] Pick a language that's Systems-only (e.g. Georgian, Lithuanian, Polish) from the Systems picker, then open a legacy screen (Pain) — confirm it shows English with a plain "<language> not available here" note, not a blank screen or a crash.
- [ ] Pick a language that's legacy-only (e.g. Bosnian, Czech, Swahili) from the legacy picker, then open Systems — confirm it shows English with a plain "<language> not available in Systems" note, not the old "unavailable — use an interpreter" gate.

> ⚠️ **Behaviour change (explicit client decision):** drafted-language translations now display **directly**, with no "unreviewed AI draft" gate, no reveal-click step, and no on-screen "AI DRAFT — NOT CLINICALLY REVIEWED" warning. This was a deliberate choice made after the clinical-risk trade-off was explained (see CHANGELOG "unreviewed-draft gate removed"). None of the 28 drafted languages have actually been reviewed by a native speaker — only the in-app warning about that has been removed, not the underlying review gap. Flag this to anyone newly picking up the project.

- [ ] Open the Systems-specific language picker — confirm it's grouped into Priority 1 / 2 / 3 sections matching the brief, English is listed separately as "Source language," and **no tile is disabled any more** — all 36 target languages (including the 8 most recently completed: `ka` Georgian, `lt` Lithuanian, `lv` Latvian, `bg` Bulgarian, `ti` Tigrinya, `yue-Hant` Cantonese, `kmr` Kurdish-Kurmanji, `ml` Malayalam) are now selectable, 0 pending.
- [ ] Switch to any of the 36 drafted languages (all 10 Priority-1 languages, e.g. Spanish, Polish, Simplified Mandarin, Arabic, Urdu — plus any Priority-2/3 language, including the 8 newly completed) — confirm the translated text shows **immediately**, the same way English does, with no gate box and no click needed to reveal it.
- [ ] **Offline check (architecture fix — no per-language download at all):** open the app once online (so the service worker caches the page itself), then go offline (airplane mode) and select **any** drafted language — including ones never opened before, e.g. Tamil, Vietnamese, Hungarian, German, or Georgian. Confirm the translated text shows directly, with no "not downloaded" message possible — that message and the code path behind it no longer exist in the app at all. All 36 drafted languages' translations are baked directly into the page itself, the same way Pain/Time-Onset/every other category has always worked, so there is no separate per-language cache to be missing. (Automated: `test_offline.py` checks this for Tamil/Vietnamese/Hungarian/Arabic/Polish/Simplified-Mandarin/German/Georgian, plus confirms a deliberately nonexistent language code still shows the "unavailable" gate.)
- [ ] Spot-check a lower-resource language draft (e.g. Kurdish Sorani, Pashto, Tigrinya, or Kurdish-Kurmanji) with anyone available who can assess it — these were flagged in the QA report as lower-confidence drafts than the higher-resource/Priority-1 languages. This matters more now that there's no on-screen "unreviewed" warning at the point of use.
- [ ] Confirm the Yes/No/Don't know/Don't understand buttons are translated correctly in every language (they come from the separately-sourced, already-reviewed phrase #1 data, not the new Systems drafts) — including the two newly-added Priority-1 languages (Polish, Simplified Mandarin), which use a small separately-tracked fallback set since they're outside the legacy phrasebook's own language set.
- [ ] Confirm the "Listen" (text-to-speech) button appears for every drafted and source language (it no longer needs a reveal step first) and never attempts to speak a gated `pending`-language placeholder.

## Rapid-access Neuro/Stroke
- [ ] Open Neurological/Stroke — confirm the red "Record onset / last-known-well now" banner/button appears above the routine question list and is reachable without answering anything first.
- [ ] Confirm the disclaimer text ("not a validated stroke assessment") is visible.

## Accessibility / device coverage
- [ ] Test at a small phone width (≈360–390px) and a larger phone/tablet width.
- [ ] Test with VoiceOver/TalkBack (or another screen reader) on at least the home screen, one Systems question, and the summary screen.
- [ ] Test keyboard-only navigation (Tab/Enter/Space) through a full Systems question.
- [ ] Test an RTL language (Arabic) for correct text direction and layout mirroring on Systems screens specifically (not just legacy screens, which were already verified).
- [ ] Test in airplane mode / offline after first install — confirm the Systems page loads and works fully offline (no network calls expected at any point).
- [ ] Force a service-worker cache upgrade (reload after the `sw.js` change) — confirm the new version loads cleanly with no mixed old/new asset errors.

## Content sign-off (not a QA/engineering task — flag to clinical lead)
- [ ] Clinical governance review of the English `systems.en.json` question set itself (wording, completeness, any missing red-flag questions).
- [ ] Native-speaker/qualified medical-translator review of the 10 completed draft languages, before switching any of them from "gated" to "reviewed" status.
- [ ] Decision on the `NEURO11`/`TRAUMA05`/`CVS05` wording-overlap finding from the QA report.
