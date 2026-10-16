# Changelog

## 2.1.1 — 16 October 2026

- Removed the negative navigation margin and added a 12px gap between search and category selection to prevent the controls overlapping.

## 2.1.0 — 16 October 2026

- Replaced the permanent sidebar and large introduction with compact mobile category cards, a small sticky header, and one bottom navigation bar.
- Added searchable header language selection, English source display by default, and an explicit English reset. Existing non-English approval checks remain unchanged.
- Made question cards compact, moved technical metadata into review details, and added a patient display with audio, RTL and a clear exit.
- Added persistent `Summary (count)`, factual session/system reviews, answer editing/removal and explicit clipboard confirmation. All answers and timing remain in memory.
- Added separate timing slots for each eligible symptom, including uncertainty, ongoing symptoms, onset pattern, exact time and clinician-marked approximate timing. Returning restores the prior question/system/summary context.
- Added a compact review of positive/unknown answers at the end of each system, timing actions per symptom, and next-system navigation. Non-understanding is shown as a communication issue.
- Added Directions / Instructions using references to existing IDs. Missing requested directions are proposals only.
- Preserved all 287 canonical phrases, 38 bundles, provenance, statuses, import scripts, offline caching and restricted clinical filtering. Hash regression tests verify the preservation.

No deployment or translation reconciliation was performed. Physical-device, screen-reader and clinical governance checks remain required.
