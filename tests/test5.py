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
    print('cat-row count:', page.locator('.cat-row').count(), 'errors so far:', errors)

    # phrase #1 as a choice card, under Interpreter
    page.click('[data-shortcut="interpreter"]')
    page.wait_for_timeout(120)
    page.click('.listrow[data-id="1"]')
    page.wait_for_timeout(120)
    page.screenshot(path='r5_phrase1_choice_en.png')

    # switch to Tamil and re-check #1 and the 22.x context cards
    page.click('#langBtn')
    page.wait_for_timeout(100)
    page.screenshot(path='r5_langpicker.png')  # confirm no English tile
    page.click('.langtile[data-code="ta"]')
    page.wait_for_timeout(100)
    page.click('#homeBtn')
    page.wait_for_timeout(100)
    page.click('[data-shortcut="interpreter"]')
    page.wait_for_timeout(100)
    page.click('.listrow[data-id="1"]')
    page.wait_for_timeout(100)
    page.screenshot(path='r5_phrase1_choice_ta.png')

    page.click('#homeBtn')
    page.wait_for_timeout(100)
    page.click('[data-shortcut="neuro"]')
    page.wait_for_timeout(100)
    page.click('.listrow[data-id="22.1"]')
    page.wait_for_timeout(100)
    page.screenshot(path='r5_ctx22_ta.png')

    page.click('#homeBtn')
    page.wait_for_timeout(100)
    page.click('[data-shortcut="history"]')
    page.wait_for_timeout(100)
    page.click('.listrow[data-id="27.7"]')
    page.wait_for_timeout(100)
    page.screenshot(path='r5_ctx27_ta.png')

    browser.close()
print('ERRORS:', errors)
