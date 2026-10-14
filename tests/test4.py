from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page(viewport={'width':390,'height':780})
    page.goto('http://localhost:8731/index.html')
    page.wait_for_timeout(300)
    page.click('#disclaimerClose')
    page.wait_for_timeout(150)
    page.screenshot(path='r4_home.png', full_page=True)

    page.click('[data-shortcut="pain"]')
    page.wait_for_timeout(150)
    page.click('#startAllBtn')
    page.wait_for_timeout(150)
    page.screenshot(path='r4_runner_pain.png')

    page.click('#nextBtn')
    page.wait_for_timeout(150)
    page.screenshot(path='r4_runner_scale.png')

    page.click('#nextBtn')
    page.wait_for_timeout(150)
    page.screenshot(path='r4_runner_choice12.png')  # the constant/comes-and-goes choice

    page.click('#homeBtn')
    page.wait_for_timeout(150)
    page.click('[data-shortcut="exam"]')
    page.wait_for_timeout(150)
    page.click('.listrow[data-id="6"]')
    page.wait_for_timeout(150)
    page.screenshot(path='r4_choice_doctor_nurse.png')

    browser.close()
