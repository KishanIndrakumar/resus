"""
Phase D full-matrix check: exercises the app's OWN sysGetTranslation() function (not just the raw
embedded JSON) for all 96 question IDs x 36 drafted languages (3,456 cells), online first and
then fully offline (service worker cache only, network blocked). Confirms:
  - every cell returns status 'draft' (or 'source' for English) with non-empty text
  - no cell silently falls back to English for a language that IS in the 36-language manifest
  - the four Phase D content changes (SKIN07, EYE05, GU03, TRAUMA05) and the Tamil NEURO03
    correction are visible to the app's own lookup function, not just the raw JSON
  - identical behaviour offline as online (same cache-embedding design as test_offline.py)
"""
from playwright.sync_api import sync_playwright
import json

errors = []

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    context = browser.new_context(viewport={'width': 390, 'height': 780}, service_workers='allow')
    page = context.new_page()
    page.on('console', lambda msg: errors.append(('console', msg.text)) if msg.type == 'error' else None)
    page.on('pageerror', lambda exc: errors.append(('pageerror', str(exc))))

    page.goto('http://localhost:8731/index.html')
    page.wait_for_timeout(300)
    # Let the service worker install and cache core assets before going offline
    page.wait_for_timeout(500)

    def run_matrix_check(label):
        result = page.evaluate("""
        () => {
            const qids = Object.keys(SYS_QUESTIONS);
            const langs = SYS_LANGS_MANIFEST.languages.filter(l => l.status === 'draft').map(l => l.code);
            let total = 0, missing = 0, englishFallback = 0, blank = 0;
            const badCells = [];
            for (const qid of qids) {
                for (const lang of langs) {
                    total++;
                    const r = sysGetTranslation(qid, lang);
                    if (r.status === 'missing') { missing++; badCells.push([qid, lang, 'missing']); continue; }
                    if (!r.text || r.text.trim() === '') { blank++; badCells.push([qid, lang, 'blank']); continue; }
                    if (r.status === 'crossModuleFallback') { englishFallback++; badCells.push([qid, lang, 'crossModuleFallback']); continue; }
                }
            }
            return {
                total, missing, englishFallback, blank,
                qidCount: qids.length, langCount: langs.length,
                badCells: badCells.slice(0, 20),
                // Spot-check the Phase D changes via the app's own function
                skin07: sysGetTranslation('SKIN07', 'en'),
                eye05: sysGetTranslation('EYE05', 'en'),
                gu03: sysGetTranslation('GU03', 'en'),
                trauma05: sysGetTranslation('TRAUMA05', 'en'),
                resp05: sysGetTranslation('RESP05', 'en'),
                ent05: sysGetTranslation('ENT05', 'en'),
                ta_neuro03: sysGetTranslation('NEURO03', 'ta'),
                ru_cvs05: sysGetTranslation('CVS05', 'ru'),
                hi_cvs05: sysGetTranslation('CVS05', 'hi'),
            };
        }
        """)
        print(f'--- {label} ---')
        print(f"  Matrix: {result['qidCount']} question IDs x {result['langCount']} languages = {result['total']} cells checked")
        print(f"  missing={result['missing']}  blank={result['blank']}  crossModuleFallback={result['englishFallback']}")
        if result['badCells']:
            print('  Sample bad cells:', result['badCells'])
        assert result['qidCount'] == 96, result['qidCount']
        assert result['langCount'] == 36, result['langCount']
        assert result['total'] == 96 * 36, result['total']
        assert result['missing'] == 0, f"{result['missing']} missing cells"
        assert result['blank'] == 0, f"{result['blank']} blank cells"
        assert result['englishFallback'] == 0, f"{result['englishFallback']} unexpected English-fallback cells (all 36 manifest languages should have real entries)"
        print('  SKIN07 (en):', result['skin07']['text'])
        print('  EYE05 (en):', result['eye05']['text'])
        print('  GU03 (en):', result['gu03']['text'])
        print('  TRAUMA05 (en):', result['trauma05']['text'])
        print('  RESP05 (en, unchanged):', result['resp05']['text'])
        print('  ENT05 (en, unchanged):', result['ent05']['text'])
        print('  NEURO03 (ta):', result['ta_neuro03']['text'])
        print('  CVS05 (ru, unchanged):', result['ru_cvs05']['text'])
        print('  CVS05 (hi, unchanged):', result['hi_cvs05']['text'])
        assert result['skin07']['text'] == 'Has your skin been painful?'
        assert result['eye05']['text'] == 'Does bright light hurt your eyes?'
        assert result['gu03']['text'] == 'Have you had a sudden urge to pass urine that was difficult to hold?'
        assert result['trauma05']['text'] == 'Did you black out after the injury?'
        assert result['resp05']['text'] == 'Have you noticed unusual sounds when breathing?'
        assert result['ent05']['text'] == 'Have you had difficulty swallowing?'
        assert 'அனுபவித்ததிலேயே' in result['ta_neuro03']['text'], 'Tamil NEURO03 fix not visible via sysGetTranslation'
        assert 'அனுபவிக்காத' not in result['ta_neuro03']['text'], 'Old (inverted-negation) Tamil NEURO03 text still showing'
        assert result['ru_cvs05']['text'] == 'Вы теряли сознание?', 'ru CVS05 should remain unchanged (proposal only)'
        assert result['hi_cvs05']['text'] == 'क्या आप बेहोश हुए हैं?', 'hi CVS05 should remain unchanged (proposal only)'
        print(f'  ALL {label} CHECKS PASSED')
        print()

    run_matrix_check('ONLINE')

    # Now go fully offline, exactly like test_offline.py does: flip the same context's network
    # state and reload, so only the service-worker-cached index.html is served (no language was
    # ever individually "downloaded" -- everything is embedded in the one cached page).
    context.set_offline(True)
    page.reload()
    page.wait_for_timeout(400)
    disclaimer = page.locator('#disclaimerClose')
    if disclaimer.count() and disclaimer.is_visible():
        page.click('#disclaimerClose')
        page.wait_for_timeout(150)

    run_matrix_check('OFFLINE (network disabled)')

    browser.close()

print('ERRORS:', errors)
assert errors == [], errors
print('ALL PHASE D FULL-MATRIX CHECKS PASSED (3,456 cells x 2 passes = 6,912 lookups, online + offline)')
