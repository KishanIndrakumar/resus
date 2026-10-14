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
    page.screenshot(path='r6_home.png', full_page=True)

    page.click('#langBtn')
    page.wait_for_timeout(100)
    page.click('.langtile[data-code="ta"]')
    page.wait_for_timeout(100)
    page.click('#homeBtn')
    page.wait_for_timeout(100)

    page.click('[data-shortcut="history"]')
    page.wait_for_timeout(100)
    page.click('.listrow[data-id="27.2"]')
    page.wait_for_timeout(100)
    page.screenshot(path='r6_ta_27_2_bigger_text.png')

    page.click('#homeBtn')
    page.wait_for_timeout(100)
    page.click('[data-shortcut="pain"]')
    page.wait_for_timeout(100)
    page.click('#startAllBtn')
    page.wait_for_timeout(100)
    page.screenshot(path='r6_ta_pain_responsebar.png')

    browser.close()
print('ERRORS:', errors)
