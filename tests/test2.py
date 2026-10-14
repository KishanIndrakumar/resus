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

    # switch to Arabic (RTL)
    page.click('#langBtn')
    page.wait_for_timeout(150)
    page.click('.langtile[data-code="ar"]')
    page.wait_for_timeout(150)

    page.click('[data-shortcut="history"]')
    page.wait_for_timeout(150)
    page.click('.listrow[data-id="26.2"]')  # epilepsy - highlighted context card
    page.wait_for_timeout(150)
    page.screenshot(path='shot_ar_highlight.png')
    ov = page.evaluate("document.querySelector('.main').scrollHeight - document.querySelector('.main').clientHeight")
    print('ar highlight overflow:', ov)

    page.click('#homeBtn')
    page.wait_for_timeout(150)
    page.click('[data-shortcut="symptoms"]')
    page.wait_for_timeout(150)
    page.click('.listrow[data-id="14.3"]')  # colour choice
    page.wait_for_timeout(150)
    page.screenshot(path='shot_choice_colour.png')

    page.click('#homeBtn')
    page.wait_for_timeout(150)
    page.click('[data-shortcut="exam"]')
    page.wait_for_timeout(150)
    page.click('.listrow[data-id="45"]')  # body-part choice
    page.wait_for_timeout(150)
    page.screenshot(path='shot_choice_bodypart.png')
    ov2 = page.evaluate("document.querySelector('.main').scrollHeight - document.querySelector('.main').clientHeight")
    print('bodypart overflow:', ov2)

    page.click('#homeBtn')
    page.wait_for_timeout(150)
    page.click('[data-shortcut="exam"]')
    page.wait_for_timeout(150)
    page.click('.listrow[data-id="34.2"]')
    page.wait_for_timeout(150)
    page.screenshot(path='shot_choice_examiner.png')

    browser.close()

print('ERRORS:', errors)
