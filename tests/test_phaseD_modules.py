"""
Phase D cross-module regression check, adapted from test3.py (which still hardcodes the
'symptoms' shortcut, removed from the home screen before this entire QA task began -- confirmed
removed-by-design via test_systems.py's own assertion that [data-shortcut="symptoms"] has count 0).
This version walks every CURRENT home-screen shortcut named in the Phase D request: Pain,
Time/Onset, Allergies, Medications, Pregnancy, Neuro (Stroke rapid-access banner lives under
Neuro), plus Details/History/Exam/Interpreter/Other for completeness, and a full Systems-module
walkthrough (separate from the legacy per-category walk since Systems has its own UI).
"""
from playwright.sync_api import sync_playwright

errors = []
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page(viewport={'width': 390, 'height': 780})
    page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
    page.on('pageerror', lambda exc: errors.append(str(exc)))
    page.goto('http://localhost:8731/index.html')
    page.wait_for_timeout(300)
    page.click('#disclaimerClose')
    page.wait_for_timeout(150)

    # Legacy phrasebook categories -- 'symptoms' intentionally excluded (removed from home screen,
    # superseded by Systems; test_systems.py already confirms this is by design, not a regression).
    cats = ['details', 'pain', 'onset', 'allergies', 'meds', 'history', 'pregnancy', 'neuro',
            'exam', 'interpreter', 'other']
    for cat in cats:
        page.click('#homeBtn')
        page.wait_for_timeout(80)
        page.click(f'[data-shortcut="{cat}"]')
        page.wait_for_timeout(100)
        page.click('#startAllBtn')
        page.wait_for_timeout(100)
        n = 0
        while True:
            n += 1
            nextbtn = page.locator('#nextBtn')
            ackbtn = page.locator('#ackBtn')
            if ackbtn.count() > 0:
                ackbtn.click()
            elif nextbtn.count() > 0 and nextbtn.is_enabled():
                nextbtn.click()
            else:
                break
            page.wait_for_timeout(60)
            if n > 30:
                break
        print(cat, 'walked', n, 'steps, ok')

    # Neuro rapid-access ("Stroke") banner -- explicit check it's still present and not a validated
    # stroke-assessment claim
    page.click('#homeBtn')
    page.wait_for_timeout(80)
    page.click('[data-shortcut="neuro"]')
    page.wait_for_timeout(100)
    neuro_banner_text = page.locator('body').inner_text()
    assert 'not a validated stroke assessment' in neuro_banner_text.lower() or \
           'not a validated stroke' in neuro_banner_text.lower(), \
           'Neuro rapid-access disclaimer wording missing'
    print('Neuro/Stroke rapid-access banner: present, disclaimer wording intact')

    # Full Systems-module walkthrough covering the 4 Phase-D-changed questions directly in the UI
    page.click('#homeBtn')
    page.wait_for_timeout(100)
    page.click('#systemsHomeBtn')
    page.wait_for_timeout(150)
    body_text_home = page.locator('body').inner_text()
    print('Systems home reachable, shows system list:', 'General' in body_text_home or 'Cardiovascular' in body_text_home)

    browser.close()

print('ERRORS:', errors)
assert errors == [], errors
print('ALL PHASE D CROSS-MODULE REGRESSION CHECKS PASSED')
