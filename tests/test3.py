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

    cats = ['details','pain','symptoms','onset','allergies','meds','history','pregnancy','neuro','exam','interpreter','other']
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
            if n > 25: break
        print(cat, 'walked', n, 'steps, ok')

    # Browse all
    page.click('#homeBtn')
    page.wait_for_timeout(80)
    page.click('#browseAllBtn')
    page.wait_for_timeout(100)
    rows = page.locator('.listrow').count()
    print('browse all rows:', rows)

    # test Urdu RTL on a plain (non-html) card
    page.click('#homeBtn')
    page.wait_for_timeout(80)
    page.click('#langBtn')
    page.wait_for_timeout(100)
    page.click('.langtile[data-code="ur"]')
    page.wait_for_timeout(100)
    page.click('[data-shortcut="details"]')
    page.wait_for_timeout(100)
    page.click('#startAllBtn')
    page.wait_for_timeout(100)
    page.screenshot(path='shot_urdu.png')

    browser.close()

print('ERRORS:', errors)
