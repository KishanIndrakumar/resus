from playwright.sync_api import sync_playwright
import sys

errors = []
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page(viewport={'width':390,'height':780})
    page.on('console', lambda msg: errors.append(msg.text) if msg.type=='error' else None)
    page.on('pageerror', lambda exc: errors.append(str(exc)))
    page.goto('http://localhost:8731/index.html')
    page.wait_for_timeout(300)
    page.click('#disclaimerClose')
    page.wait_for_timeout(200)
    page.screenshot(path='shot_home.png')

    # Check no-scroll on home
    overflow = page.evaluate("document.querySelector('.main').scrollHeight - document.querySelector('.main').clientHeight")
    print('home overflow px:', overflow)

    # symptoms category (weight loss check)
    page.click('[data-shortcut="symptoms"]')
    page.wait_for_timeout(200)
    page.screenshot(path='shot_symptoms.png')
    rows = page.locator('.listrow').all_inner_texts()
    print('symptoms rows:', rows)

    # history category (weight loss should be absent)
    page.click('#toHome')
    page.wait_for_timeout(150)
    page.click('[data-shortcut="history"]')
    page.wait_for_timeout(200)
    hist_rows = page.locator('.listrow').all_inner_texts()
    print('history rows:', hist_rows)
    has_weight = any('weight' in r.lower() for r in hist_rows)
    print('history contains weight loss?', has_weight)

    # start runner from symptoms, check single-screen fit
    page.click('#toHome')
    page.wait_for_timeout(150)
    page.click('[data-shortcut="symptoms"]')
    page.wait_for_timeout(150)
    page.click('#startAllBtn')
    page.wait_for_timeout(200)
    page.screenshot(path='shot_runner1.png')
    ov = page.evaluate("document.querySelector('.main').scrollHeight - document.querySelector('.main').clientHeight")
    print('runner1 overflow px:', ov)

    # click through cough compound split (14.1/14.2/14.3) and difficulty split (22.x)
    titles = []
    for i in range(20):
        t = page.locator('.srcText').inner_text()
        titles.append(t)
        nextbtn = page.locator('#nextBtn')
        ackbtn = page.locator('#ackBtn')
        if ackbtn.count() > 0:
            ackbtn.click()
        elif nextbtn.count() > 0 and nextbtn.is_enabled():
            nextbtn.click()
        else:
            break
        page.wait_for_timeout(120)
    print('titles walked:', titles)

    browser.close()

print('CONSOLE ERRORS:', errors)
