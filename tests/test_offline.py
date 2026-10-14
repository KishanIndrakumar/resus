"""
Offline-architecture regression test for the Systems module (embedded-translations design,
no gating/reveal step).

Every drafted language's content is embedded directly in index.html at build time (SYS_TR),
exactly like the legacy phrasebook's PHRASES data. There is no "language pack download" step,
no per-language cache, and no "Translation not downloaded for offline use" state. Per an
explicit client decision, drafted translations are also shown directly (no "unreviewed AI
draft" gate/reveal step, no on-screen AI-draft banner) -- the same way the legacy phrasebook's
own translations have always been shown. Only a genuinely PENDING (never-drafted) language still
shows the "Translation unavailable -- use a qualified interpreter" message, since there is
nothing else to show for it.

This test confirms both the offline-reliability property and the current (gate-free) display
behaviour, fully offline from the very first interaction with each language.
"""
from playwright.sync_api import sync_playwright
import json
import os

# Resolve the manifest relative to this script's own location, not the caller's cwd, so this
# test runs correctly whether invoked from the release root, from tests/, or anywhere else --
# in this release's packaged layout, systems.languages.json lives in ../src/ relative to this
# script (tests/ and src/ are sibling folders). Falls back to a bare relative/absolute path if
# one was already provided via that same filename sitting next to the script (older flat layout).
_HERE = os.path.dirname(os.path.abspath(__file__))
_CANDIDATES = [
    os.path.join(_HERE, 'systems.languages.json'),             # same folder as this script
    os.path.join(_HERE, '..', 'src', 'systems.languages.json'),  # this release's tests/ + src/ layout
    'systems.languages.json',                                  # caller's cwd, last resort
]
_MANIFEST_PATH = next((p for p in _CANDIDATES if os.path.exists(p)), _CANDIDATES[0])
MANIFEST = json.load(open(_MANIFEST_PATH, encoding='utf-8'))
DRAFTED = sorted(l['code'] for l in MANIFEST['languages'] if l['status'] == 'draft')
assert len(DRAFTED) == 36, f'expected 36 drafted languages (all target languages now complete), got {len(DRAFTED)}'
PENDING = sorted(l['code'] for l in MANIFEST['languages'] if l['status'] == 'pending')
assert len(PENDING) == 0, f'expected 0 pending languages, got {len(PENDING)}: {PENDING}'

errors = []
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    context = browser.new_context(viewport={'width': 390, 'height': 780}, service_workers='allow')
    page = context.new_page()
    page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
    page.on('pageerror', lambda exc: errors.append(str(exc)))

    # One ordinary online visit first, so the service worker installs and caches the app shell
    # (index.html itself) -- same as any PWA's first-ever load. The point of this test is that,
    # from here on, NO language was ever individually "downloaded" or pre-visited -- every one
    # of them still works purely because its translations are baked into index.html itself.
    page.goto('http://localhost:8731/index.html')
    page.wait_for_timeout(300)
    page.click('#disclaimerClose')
    page.wait_for_timeout(150)

    # Now go fully offline (network-level emulation, not just closing Wi-Fi in the app) and
    # reload, so the only thing served is whatever the service worker cached -- proving the
    # Systems module needs nothing beyond the cached page itself.
    context.set_offline(True)
    page.reload()
    page.wait_for_timeout(400)
    disclaimer = page.locator('#disclaimerClose')
    if disclaimer.count() and disclaimer.is_visible():
        disclaimer.click()
    page.wait_for_timeout(150)

    def check_language(code):
        page.click('#homeBtn')
        page.wait_for_timeout(60)
        page.click('#systemsHomeBtn')
        page.wait_for_timeout(60)
        page.click('#sysLangBtn')
        page.wait_for_timeout(60)
        page.click(f'.langtile[data-code="{code}"]')
        page.wait_for_timeout(60)
        page.click('[data-sys="respiratory"]')
        page.wait_for_timeout(80)
        page.click('#sysStartBtn')
        page.wait_for_timeout(100)
        gated = page.locator('.unavailable-box').count()
        tgt_text = page.locator('.tgtText').inner_text() if page.locator('.tgtText').count() else ''
        return gated, tgt_text

    # Spot-check across the priority tiers, all offline from first load. Every drafted language
    # should show its translated text directly -- no gate box at all.
    for code in ('ta', 'vi', 'hu', 'ar', 'pl', 'zh-Hans', 'de'):
        gated, tgt_text = check_language(code)
        assert gated == 0, f'{code}: drafted language should show translated text directly, not the "unavailable" gate'
        assert len(tgt_text.strip()) > 0, f'{code}: translated text should not be blank'
    print('Checked 7 drafted languages fully offline from the very first page load -- all show translated text directly, no gate, no "not downloaded" state.')

    # Confirm the shown text is genuinely translated (not the English source re-shown).
    gated, ta_text = check_language('ta')
    src_text = page.locator('.srcText').inner_text()
    assert ta_text.strip() != src_text.strip(), 'Tamil text should not just be the English source re-shown'
    page.screenshot(path='offline_embedded_ta.png')
    print('Tamil text confirmed non-blank and non-English while fully offline:', ta_text)

    # All 36 target languages are now drafted (0 pending) -- confirm Georgian ('ka'), one of the
    # 8 languages completed this round, now shows translated text directly offline too, same as
    # every other drafted language (previously this was the one case still gated as "pending").
    page.click('#homeBtn'); page.wait_for_timeout(60)
    page.click('#systemsHomeBtn'); page.wait_for_timeout(60)
    page.evaluate("() => { state.lang = 'ka'; saveLang(); }")
    page.click('[data-sys="respiratory"]'); page.wait_for_timeout(80)
    page.click('#sysStartBtn'); page.wait_for_timeout(100)
    assert page.locator('.unavailable-box').count() == 0, 'Georgian is now drafted -- should show directly, no gate, even offline'
    ka_text = page.locator('.tgtText').inner_text()
    assert len(ka_text.strip()) > 0, 'Georgian translated text should not be blank, offline'
    page.screenshot(path='offline_embedded_ka.png')
    print('Georgian (newly drafted) correctly shows translated text directly, fully offline:', ka_text)

    # A genuinely unknown language code (never part of any spec) should still show the honest
    # "unavailable" gate -- there is genuinely nothing to show for it, so this remains the one
    # case that should still be gated.
    page.click('#homeBtn'); page.wait_for_timeout(60)
    page.click('#systemsHomeBtn'); page.wait_for_timeout(60)
    page.evaluate("() => { state.lang = 'xx-nonexistent'; saveLang(); }")
    page.click('[data-sys="respiratory"]'); page.wait_for_timeout(80)
    page.click('#sysStartBtn'); page.wait_for_timeout(100)
    assert page.locator('.unavailable-box').count() == 1, 'Unknown/unspecified language code should still show the "unavailable" gate'
    page.screenshot(path='offline_embedded_pending_unknown.png')
    print('Unknown language code correctly shows the "unavailable" gate, fully offline.')

    browser.close()

print('ERRORS:', errors)
assert not errors, f'Console/page errors detected: {errors}'
print('ALL EMBEDDED-OFFLINE CHECKS PASSED')
