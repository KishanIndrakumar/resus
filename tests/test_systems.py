from playwright.sync_api import sync_playwright

errors = []
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page(viewport={'width':390,'height':780})
    page.on('console', lambda msg: errors.append(msg.text) if msg.type=='error' else None)
    page.on('pageerror', lambda exc: errors.append(str(exc)))
    page.goto('http://localhost:8731/index.html')
    page.wait_for_timeout(300)
    page.click('#disclaimerClose')
    page.wait_for_timeout(150)
    page.screenshot(path='sys_home.png', full_page=True)

    # 1. Associated Symptoms must be gone from home
    assert page.locator('[data-shortcut="symptoms"]').count() == 0, 'Associated Symptoms still on home screen'
    assert page.locator('#systemsHomeBtn').count() == 1, 'Systems row missing from home screen'

    # 2. Legacy categories still work -- quick smoke test on Pain
    page.click('[data-shortcut="pain"]')
    page.wait_for_timeout(100)
    page.click('#startAllBtn')
    page.wait_for_timeout(100)
    page.screenshot(path='sys_legacy_pain.png')
    page.click('#homeBtn')
    page.wait_for_timeout(100)

    # 3. Neuro rapid-access banner
    page.click('[data-shortcut="neuro"]')
    page.wait_for_timeout(100)
    assert page.locator('#neuroUrgentBtn').count() == 1, 'Neuro rapid-access button missing'
    page.screenshot(path='sys_neuro.png')
    page.click('#neuroUrgentBtn')
    page.wait_for_timeout(100)
    page.screenshot(path='sys_neuro_timing_modal.png')
    page.click('#closeGeneric')
    page.wait_for_timeout(100)
    page.click('#homeBtn')
    page.wait_for_timeout(100)

    # 4. Systems module: English walkthrough on General symptoms
    page.click('#systemsHomeBtn')
    page.wait_for_timeout(100)
    page.screenshot(path='sys_systems_home.png')
    page.click('[data-sys="general"]')
    page.wait_for_timeout(100)
    page.screenshot(path='sys_general_list.png')
    page.click('#sysStartBtn')
    page.wait_for_timeout(100)
    page.screenshot(path='sys_runner_q1_en.png')
    # answer yes to q1, no to q2, dont_know to q3
    page.click('.rbtn.yes')
    page.wait_for_timeout(80)
    page.click('#nextBtn')
    page.wait_for_timeout(100)
    page.click('.rbtn.no')
    page.wait_for_timeout(80)
    page.click('#nextBtn')
    page.wait_for_timeout(100)
    page.click('.rbtn.dontknow')
    page.wait_for_timeout(80)
    page.click('#nextBtn')
    page.wait_for_timeout(100)
    # skip remaining to the end
    for _ in range(10):
        nxt = page.locator('#nextBtn')
        if nxt.count()==0: break
        txt = nxt.inner_text()
        nxt.click()
        page.wait_for_timeout(80)
        if 'summary' in txt.lower():
            break
    page.wait_for_timeout(150)
    page.screenshot(path='sys_summary_general.png')

    # 5. Edit a prior answer from summary
    edit_btns = page.locator('.editq')
    if edit_btns.count() > 0:
        edit_btns.first.click()
        page.wait_for_timeout(100)
        page.screenshot(path='sys_edit_from_summary.png')

    # 6. Systems module now has its OWN language picker (state.sysLang), separate from the
    # main phrasebook's #langBtn/state.lang -- switch to Arabic there and confirm the runner
    # shows translated text + RTL directly (embedded in the page, no fetch/gate/reveal step).
    page.click('#homeBtn')
    page.wait_for_timeout(100)
    page.click('#systemsHomeBtn')
    page.wait_for_timeout(100)
    page.click('#sysLangBtn')
    page.wait_for_timeout(100)
    page.screenshot(path='sys_lang_picker.png')
    # Priority-grouped picker: all 36 languages are now drafted (0 pending), so no tile should
    # be disabled any more -- confirm Georgian ('ka'), one of the 8 languages completed this
    # round, is now a selectable (non-disabled) tile.
    assert page.locator('.langtile[disabled]').count() == 0, 'No language should be disabled now -- all 36 are drafted'
    assert page.locator('.langtile[data-code="ka"]:not([disabled])').count() == 1, 'Georgian should now be a selectable tile'
    page.click('.langtile[data-code="ar"]')
    page.wait_for_timeout(100)
    page.click('[data-sys="respiratory"]')
    page.wait_for_timeout(100)
    page.click('#sysStartBtn')
    page.wait_for_timeout(100)
    assert page.locator('.unavailable-box').count() == 0, 'Arabic is drafted -- translated text should show directly, no gate'
    assert page.locator('.tgtText').count() == 1, 'Expected Arabic translated text to be visible'
    assert page.locator('.aiTag').count() == 1, 'Drafted language should show a small "AI translated" tag'
    assert 'AI translated' in page.locator('.aiTag').inner_text(), 'AI tag should read "AI translated"'
    page.screenshot(path='sys_runner_ar.png')

    # 6b. English (source, not a draft) should NOT show the "AI translated" tag.
    page.click('#homeBtn')
    page.wait_for_timeout(100)
    page.click('#systemsHomeBtn')
    page.wait_for_timeout(100)
    page.click('#sysLangBtn')
    page.wait_for_timeout(100)
    page.click('.langtile[data-code="en"]')
    page.wait_for_timeout(100)
    page.click('[data-sys="respiratory"]')
    page.wait_for_timeout(100)
    page.click('#sysStartBtn')
    page.wait_for_timeout(100)
    assert page.locator('.aiTag').count() == 0, 'English source text should not show an "AI translated" tag'

    # 7. All drafted languages (no "unreviewed draft" gate any more -- translated text shows
    # directly for every drafted language, same as English/source). Turkish (Priority 2,
    # drafted) should show its translated text immediately, with no gate and no reveal step.
    page.click('#homeBtn')
    page.wait_for_timeout(100)
    page.click('#systemsHomeBtn')
    page.wait_for_timeout(100)
    page.click('#sysLangBtn')
    page.wait_for_timeout(100)
    page.click('.langtile[data-code="tr"]')
    page.wait_for_timeout(100)
    page.click('[data-sys="respiratory"]')
    page.wait_for_timeout(100)
    page.click('#sysStartBtn')
    page.wait_for_timeout(100)
    assert page.locator('.unavailable-box').count() == 0, 'Turkish is drafted -- should show directly, no gate'
    tgt_text = page.locator('.tgtText').inner_text()
    assert len(tgt_text.strip()) > 0, 'Turkish translated text should not be blank'
    page.screenshot(path='sys_runner_tr.png')

    # 7b. Georgian ('ka') was one of the 8 languages completed this round (previously pending,
    # now drafted). Confirm it's selectable via the normal UI click and shows translated text
    # directly, same as every other drafted language -- no more "unavailable" gate for it.
    page.click('#homeBtn')
    page.wait_for_timeout(100)
    page.click('#systemsHomeBtn')
    page.wait_for_timeout(100)
    page.click('#sysLangBtn')
    page.wait_for_timeout(100)
    page.click('.langtile[data-code="ka"]')
    page.wait_for_timeout(100)
    page.click('[data-sys="respiratory"]')
    page.wait_for_timeout(100)
    page.click('#sysStartBtn')
    page.wait_for_timeout(150)
    assert page.locator('.unavailable-box').count() == 0, 'Georgian is now drafted -- should show directly, no gate'
    geo_text = page.locator('.tgtText').inner_text()
    assert len(geo_text.strip()) > 0, 'Georgian translated text should not be blank'
    page.screenshot(path='sys_runner_ka.png')
    # reset back to English for the rest of the run
    page.evaluate("() => { state.lang = 'en'; saveLang(); }")

    # 7c. Bug reported by client: while answering a Systems question, the header's globe button
    # (top-right, always visible) used to always open the LEGACY phrasebook's language picker,
    # changing state.lang and updating the header label -- but the question underneath uses
    # state.sysLang, which that picker doesn't touch. So picking a language there changed the
    # header label (e.g. to Bengali) while the visible translated text stayed on whatever
    # state.sysLang was previously set to (e.g. Japanese), a confusing mismatch. Fix: the header
    # button must now open the SYSTEMS picker instead whenever a Systems view is on screen, and
    # its own label must reflect sysLang (not the legacy lang) while there.
    page.click('#homeBtn')
    page.wait_for_timeout(100)
    page.click('#systemsHomeBtn')
    page.wait_for_timeout(100)
    page.click('#sysLangBtn')
    page.wait_for_timeout(100)
    page.click('.langtile[data-code="ja"]')
    page.wait_for_timeout(100)
    page.click('[data-sys="respiratory"]')
    page.wait_for_timeout(100)
    page.click('#sysStartBtn')
    page.wait_for_timeout(100)
    assert 'Japanese' in page.locator('#langBtnLabel').inner_text() or page.locator('.tgtText[lang="ja"]').count() == 1, 'Expected Japanese question text while sysLang=ja'
    ja_text_before = page.locator('.tgtText').inner_text()
    # Tap the header globe button -- while in a Systems view, this must open the Systems picker,
    # not the legacy one.
    page.click('#langBtn')
    page.wait_for_timeout(100)
    assert page.locator('.sysbanner').count() == 1, 'Header globe button should open the SYSTEMS language picker while in a Systems view'
    page.click('.langtile[data-code="bn"]')
    page.wait_for_timeout(150)
    # Picking a language from the Systems picker always returns to Systems home (confirmed
    # separately as expected/accepted behaviour) -- re-enter the question to check its text.
    header_label = page.locator('#langBtnLabel').inner_text()
    assert 'বাংলা' in header_label or 'Bengali' in header_label, f'Header label should show Bengali, got: {header_label}'
    page.click('[data-sys="respiratory"]')
    page.wait_for_timeout(100)
    page.click('#sysStartBtn')
    page.wait_for_timeout(100)
    # Both the header label and the visible question text must agree -- both should now reflect
    # Bengali, not a stale previous language.
    header_label2 = page.locator('#langBtnLabel').inner_text()
    assert 'বাংলা' in header_label2 or 'Bengali' in header_label2, f'Header label should still show Bengali, got: {header_label2}'
    bn_text = page.locator('.tgtText').inner_text()
    assert bn_text.strip() != ja_text_before.strip(), 'Question text should have changed from Japanese to Bengali, not stayed stale'
    page.screenshot(path='sys_langbtn_in_context.png')
    # reset back to English for the rest of the run
    page.evaluate("() => { state.lang = 'en'; saveLang(); }")

    # 7d. Outside a Systems view, the header globe button must still control the legacy
    # phrasebook language as before (no regression to existing behaviour).
    page.click('#homeBtn')
    page.wait_for_timeout(100)
    page.click('#langBtn')
    page.wait_for_timeout(100)
    assert page.locator('.sysbanner').count() == 0, 'Header globe button should open the LEGACY language picker outside a Systems view'
    page.click('#backBtn2')
    page.wait_for_timeout(100)

    # 7e. Shared-language feature: picking a language in EITHER module now sets the same
    # app-wide `state.lang`, used by both -- but only where both support it. Pick Arabic (in
    # both lists) from the legacy phrasebook (Pain), then confirm Systems also reflects Arabic.
    page.click('[data-shortcut="pain"]')
    page.wait_for_timeout(100)
    page.click('#langBtn')
    page.wait_for_timeout(100)
    page.click('.langtile[data-code="ar"]')
    page.wait_for_timeout(100)
    page.click('#homeBtn')
    page.wait_for_timeout(100)
    page.click('#systemsHomeBtn')
    page.wait_for_timeout(100)
    sys_home_label = page.locator('#sysLangBtn').inner_text()
    assert 'العربية' in sys_home_label, f'Systems home should show Arabic (picked from the legacy picker), got: {sys_home_label}'
    page.click('[data-sys="respiratory"]')
    page.wait_for_timeout(100)
    page.click('#sysStartBtn')
    page.wait_for_timeout(100)
    assert page.locator('.tgtText[lang="ar"]').count() == 1, 'Systems question should show Arabic, set via the legacy picker'

    # 7f. Pick a language that's Systems-only (Georgian, 'ka' -- not in the legacy phrasebook's
    # own ~35-language list) from the Systems picker, then confirm the LEGACY module (Pain)
    # falls back to English with a plain note, rather than crashing or showing a blank/garbled
    # translation.
    page.click('#toSysCat')
    page.wait_for_timeout(100)
    page.click('#toSysHome')
    page.wait_for_timeout(100)
    page.click('#sysLangBtn')
    page.wait_for_timeout(100)
    page.click('.langtile[data-code="ka"]')
    page.wait_for_timeout(100)
    page.click('[data-sys="respiratory"]')
    page.wait_for_timeout(100)
    page.click('#sysStartBtn')
    page.wait_for_timeout(100)
    assert page.locator('.tgtText[lang="ka"]').count() == 1, 'Systems question should show Georgian directly (Systems supports it)'
    page.click('#homeBtn')
    page.wait_for_timeout(100)
    page.click('[data-shortcut="pain"]')
    page.wait_for_timeout(100)
    page.click('#startAllBtn')
    page.wait_for_timeout(100)
    assert page.locator('.tgtText').count() == 1, 'Legacy Pain screen should still render (fallback to English, not a crash)'
    pain_label = page.locator('.tgtLabel').inner_text()
    assert 'english' in pain_label.lower() and 'ქართული' in pain_label and 'not available' in pain_label.lower(), f'Pain should show English with a Georgian-not-available note, got: {pain_label}'
    page.screenshot(path='sys_legacy_fallback_ka.png')

    # 7g. Pick a language that's legacy-only (Bosnian, 'bs' -- not in the Systems 36-language
    # spec) from the legacy picker, then confirm Systems falls back to English with a plain
    # note, rather than the old "unavailable -- use an interpreter" gate.
    page.click('#homeBtn')
    page.wait_for_timeout(100)
    page.click('[data-shortcut="pain"]')
    page.wait_for_timeout(100)
    page.click('#langBtn')
    page.wait_for_timeout(100)
    page.click('.langtile[data-code="bs"]')
    page.wait_for_timeout(100)
    page.click('#homeBtn')
    page.wait_for_timeout(100)
    page.click('#systemsHomeBtn')
    page.wait_for_timeout(100)
    page.click('[data-sys="respiratory"]')
    page.wait_for_timeout(100)
    page.click('#sysStartBtn')
    page.wait_for_timeout(100)
    assert page.locator('.unavailable-box').count() == 0, 'Bosnian-not-in-Systems should fall back to English, not the old unavailable gate'
    sys_label = page.locator('.tgtLabel').inner_text()
    assert 'english' in sys_label.lower() and 'not available in systems' in sys_label.lower(), f'Systems should show English with a Bosnian-not-available note, got: {sys_label}'
    sys_text = page.locator('.tgtText').inner_text()
    assert sys_text.strip() == 'Have you had difficulty breathing?', f'Systems fallback text should be the real English question, got: {sys_text}'
    page.screenshot(path='sys_cross_fallback_bs.png')
    # reset back to English for the rest of the run
    page.evaluate("() => { state.lang = 'en'; saveLang(); }")

    # 8. Browse all phrases still reachable (legacy ids orphaned from Associated Symptoms remain browsable)
    page.click('#homeBtn')
    page.wait_for_timeout(100)
    page.click('#browseAllBtn')
    page.wait_for_timeout(100)
    assert page.locator('.listrow[data-id="17"]').count() == 1, 'Orphaned legacy phrase #17 should still be browsable'

    browser.close()
print('ERRORS:', errors)
