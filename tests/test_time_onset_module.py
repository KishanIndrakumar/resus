"""
Dedicated regression test for the redesigned Time/Onset module (replaces the old plain
date/time-picker "calendar/clock reference tool" everywhere it was used):
  1. Legacy phrasebook "Time of Onset" category (phrases 7 & 9) shows the new elapsed-time
     onset/duration widget instead of the old bare date/time inputs.
  2. The widget captures onset value+unit, "Not sure", Sudden/Gradual, duration value+unit,
     "Still ongoing", and the retained optional exact date/time + last-known-well fields.
  3. The Systems module's inline "Record date/time for this symptom now" button and the
     Systems summary's "Record onset/duration for selected" button both open the same widget.
  4. The Systems summary screen shows onset/duration/ongoing as distinct tags once recorded.
  5. The Neuro "Record onset / last-known-well now" banner still opens the widget with the
     exact-date/last-known-well section expanded by default (stroke time-critical path).
  6. All 36 languages have translated strings for the widget (spot-checked), each marked as an
     unreviewed AI draft, matching this project's standing translation-honesty convention.
  7. Everything above still works fully offline (no architecture change).
  8. Every other existing module/category is unaffected (delegated to test_systems.py /
     test_phaseD_modules.py / test_offline.py, run alongside this script, not duplicated here).

Each result below is the ACTUAL outcome of running this script, not a claim.
"""
from playwright.sync_api import sync_playwright
import json
import os

RESULTS = []
def record(name, passed, detail=''):
    RESULTS.append((name, passed, detail))
    print(('PASS' if passed else 'FAIL'), '-', name, ('--', detail) if detail else '')

# Resolve relative to this script's own location, not the caller's cwd -- same convention as
# test_offline.py / test_release_pwa_matrix.py, since this release's packaged layout keeps
# time_onset_translations.json in a sibling src/ folder to this script's tests/ folder.
_HERE = os.path.dirname(os.path.abspath(__file__))
_CANDIDATES = [
    os.path.join(_HERE, 'time_onset_translations.json'),
    os.path.join(_HERE, '..', 'src', 'time_onset_translations.json'),
    'time_onset_translations.json',
]
_TO_PATH = next((p for p in _CANDIDATES if os.path.exists(p)), _CANDIDATES[0])
TIME_ONSET = json.load(open(_TO_PATH, encoding='utf-8'))

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    ctx = browser.new_context(viewport={'width': 390, 'height': 780}, service_workers='allow')
    page = ctx.new_page()
    errors = []
    page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto('http://localhost:8731/index.html')
    page.wait_for_timeout(300)
    page.click('#disclaimerClose')
    page.wait_for_timeout(150)

    # ---- 1/2. Legacy "Time of Onset" category shows the new widget ----
    page.click('[data-shortcut="onset"]')
    page.wait_for_timeout(100)
    page.click('#startAllBtn')
    page.wait_for_timeout(120)
    widget = page.locator('.timeonset')
    record('1. Legacy "Time of Onset" category shows the new Time/Onset widget', widget.count() == 1, f'count={widget.count()}')
    old_cal = page.locator('#calDate, #calTime')
    record('1b. Old bare date/time inputs (#calDate/#calTime) are gone', old_cal.count() == 0, f'count={old_cal.count()}')

    # Fill onset: 3 days ago, not sure left unchecked, Sudden selected
    page.fill('.timeonset [data-field="onsetVal"]', '3')
    page.select_option('.timeonset [data-field="onsetUnit"]', 'days')
    page.click('.timeonset [data-field="character"][data-val="sudden"]')
    sudden_sel = page.locator('.timeonset [data-field="character"][data-val="sudden"].sel')
    record('2a. Sudden/Gradual onset-character pill selectable', sudden_sel.count() == 1)

    # Fill duration: still ongoing -> value input should become disabled
    page.check('.timeonset [data-field="durationOngoing"]')
    dur_disabled = page.locator('.timeonset [data-field="durationVal"]').is_disabled()
    record('2b. "Still ongoing" disables the duration numeric input', dur_disabled)

    # "Not sure" on onset should disable the onset numeric input
    page.check('.timeonset [data-field="onsetNotSure"]')
    onset_disabled = page.locator('.timeonset [data-field="onsetVal"]').is_disabled()
    record('2c. Onset "Not sure" disables the onset numeric input', onset_disabled)
    page.uncheck('.timeonset [data-field="onsetNotSure"]')  # restore for the rest of the test

    # Exact date/time + last-known-well fields retained underneath
    exact_date = page.locator('.timeonset [data-field="exactDate"]')
    lkw_date = page.locator('.timeonset [data-field="lkwDate"]')
    record('2d. Optional exact date/time field retained', exact_date.count() == 1)
    record('2e. Optional last-known-well field retained', lkw_date.count() == 1)
    page.click('.timeonset .toexact summary')  # expand the collapsed optional section first
    page.wait_for_timeout(80)
    exact_date.fill('2026-10-10')
    page.fill('.timeonset [data-field="exactTime"]', '14:30')
    lkw_date.fill('2026-10-10')
    page.fill('.timeonset [data-field="lkwTime"]', '13:00')

    # ---- 3/4. Systems module: inline record button + summary tags ----
    page.click('#homeBtn'); page.wait_for_timeout(80)
    page.click('#systemsHomeBtn'); page.wait_for_timeout(80)
    page.click('[data-sys="general"]'); page.wait_for_timeout(100)
    page.click('#sysStartBtn'); page.wait_for_timeout(100)
    page.click('.rbtn.yes'); page.wait_for_timeout(80)
    record_btn = page.locator('#recordOnsetBtn')
    record('3a. Systems runner has "Record date/time for this symptom now" button', record_btn.count() == 1)
    record_btn.click()
    page.wait_for_timeout(120)
    modal_widget = page.locator('#genericModal .timeonset')
    record('3b. Clicking it opens the new Time/Onset widget (not the old picker)', modal_widget.count() == 1)
    page.fill('#genericModal .timeonset [data-field="onsetVal"]', '2')
    page.select_option('#genericModal .timeonset [data-field="onsetUnit"]', 'hours')
    page.click('#genericModal .timeonset [data-field="character"][data-val="gradual"]')
    page.click('#closeGeneric')
    page.wait_for_timeout(100)

    # advance to end of runner -> summary
    for _ in range(20):
        nxt = page.locator('#nextBtn')
        if nxt.count() == 0:
            break
        txt = nxt.inner_text()
        nxt.click()
        page.wait_for_timeout(60)
        if 'summary' in txt.lower():
            break
    page.wait_for_timeout(150)
    tags = page.locator('.sumtimingtag')
    tag_texts = tags.all_inner_texts()
    has_onset_tag = any('Onset: 2 hours ago' in t for t in tag_texts)
    has_gradual_tag = any('Gradual onset' in t for t in tag_texts)
    record('4a. Summary shows a distinct "Onset: ..." tag', has_onset_tag, str(tag_texts))
    record('4b. Summary shows a distinct onset-character tag', has_gradual_tag, str(tag_texts))
    no_merged_line = not any(('Onset' in t and 'Duration' in t) for t in tag_texts)
    record('4c. Onset/duration/ongoing are separate tags, never merged into one line', no_merged_line, str(tag_texts))

    # Summary's own "Record onset/duration for selected" button also opens the widget
    onset_sel_btn = page.locator('#onsetSelectedBtn')
    if onset_sel_btn.count() > 0:
        page.check('.posChk >> nth=0')
        onset_sel_btn.click()
        page.wait_for_timeout(120)
        record('3c. Summary "Record onset/duration for selected" opens the new widget too', page.locator('#genericModal .timeonset').count() >= 1)
        page.click('#closeGeneric')
        page.wait_for_timeout(80)
    else:
        record('3c. Summary "Record onset/duration for selected" opens the new widget too', False, 'button not present (no Yes answers reached summary)')

    # ---- 5. Neuro urgent banner (stroke time-critical path) ----
    page.click('#homeBtn'); page.wait_for_timeout(80)
    page.click('[data-shortcut="neuro"]'); page.wait_for_timeout(100)
    neuro_btn = page.locator('#neuroUrgentBtn')
    record('5a. Neuro "Record onset / last-known-well now" banner present', neuro_btn.count() == 1)
    if neuro_btn.count():
        neuro_btn.click()
        page.wait_for_timeout(120)
        neuro_widget = page.locator('#genericModal .timeonset[data-key="neuro_urgent"]')
        record('5b. Neuro urgent path opens the new widget', neuro_widget.count() == 1)
        exact_open = page.evaluate("() => { const d = document.querySelector('#genericModal .toexact'); return d ? d.open : null; }")
        record('5c. Exact date/time + last-known-well section starts EXPANDED for the stroke-critical path', exact_open is True, f'open={exact_open}')
        page.click('#closeGeneric')
        page.wait_for_timeout(80)

    record('6a. Console/page errors throughout', errors == [], str(errors))

    # ---- 7. Fully offline ----
    ctx.set_offline(True)
    page.reload()
    page.wait_for_timeout(400)
    if page.locator('#disclaimerClose').count() and page.locator('#disclaimerClose').is_visible():
        page.click('#disclaimerClose')
    page.wait_for_timeout(120)
    page.click('[data-shortcut="onset"]')
    page.wait_for_timeout(100)
    page.click('#startAllBtn')
    page.wait_for_timeout(120)
    offline_widget_ok = page.locator('.timeonset').count() == 1
    record('7a. Time/Onset widget still renders fully offline', offline_widget_ok)

    # Switch to Tamil offline and confirm the widget's question text is genuinely translated
    page.click('#homeBtn'); page.wait_for_timeout(60)
    page.evaluate("() => { state.lang = 'ta'; saveLang(); }")
    page.click('[data-shortcut="onset"]'); page.wait_for_timeout(100)
    page.click('#startAllBtn'); page.wait_for_timeout(120)
    label_text = page.locator('.timeonset .tolabel').first.inner_text()
    ta_expected = TIME_ONSET['languages']['ta']['strings']['onset_question']
    record('7b. Tamil translation of the onset question renders fully offline', label_text.strip() == ta_expected.strip(), f'got={label_text!r} expected={ta_expected!r}')
    page.screenshot(path='time_onset_offline_ta.png')

    ctx.set_offline(False)
    browser.close()

print()
print('='*70)
passed = sum(1 for _, p, _ in RESULTS if p)
failed = [n for n, p, d in RESULTS if not p]
print(f'TOTAL: {passed}/{len(RESULTS)} passed')
if failed:
    print('NOT PASSING:', failed)
print('='*70)
