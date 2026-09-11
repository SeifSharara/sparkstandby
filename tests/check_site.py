"""Optional browser smoke checks. Requires Python Playwright and Chromium.
Run against the local static server: python3 tests/check_site.py
"""
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright, expect

BASE = 'http://localhost:8000'
ROOT = Path(__file__).resolve().parents[1]
BRANCHES = [
    ('My AC isn’t cooling', 'AC Repair', ['Running, but blowing warm air', 'It has stopped running'], ['As soon as possible', 'Tomorrow works'], ['System is running but blowing warm air.', 'AC system has stopped running entirely.']),
    ('I need a quote', 'Installation Quote', ['Replacing my current system', 'An installation in a new space'], ['I’m ready to get started', 'Just planning ahead'], ['replace an existing HVAC system', 'installation in a new space']),
    ('I need maintenance', 'HVAC Maintenance', ['A seasonal tune-up', 'It’s making an unusual noise'], ['As soon as possible', 'Sometime this week'], ['seasonal HVAC tune-up', 'unusual noise']),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 1000}, reduced_motion='reduce')
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(BASE)
    expect(page.locator('main > section')).to_have_count(5)
    expect(page.get_by_role('heading', level=1)).to_have_count(1)

    for width in [320, 375, 390, 640, 720, 768, 1024, 1440, 1920]:
        page.set_viewport_size({'width': width, 'height': 900})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'Overflow at {width}px'
    print('PASS: Homepage fits 9 screen widths, including narrow and zoom-equivalent layouts.')

    for route in ['/', '/demo/', '/demo/ready/', '/privacy/', '/terms/', '/sms-consent/']:
        response = page.goto(BASE + route)
        assert response.status == 200
        for width in [320, 375, 390, 640, 720, 768, 1024, 1440, 1920]:
            page.set_viewport_size({'width': width, 'height': 900})
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'{route} overflows at {width}'
            if width in [390, 1440]:
                page.screenshot(path=f'/tmp/spark-{route.strip(chr(47)).replace(chr(47), chr(45)) or "home"}-{width}.png', full_page=True)
        for link in page.locator('a[href]').evaluate_all('(links) => links.map(a => a.getAttribute("href"))'):
            parsed = urlparse(link)
            if parsed.scheme or parsed.netloc:
                continue
            path = ROOT / parsed.path.lstrip('/') if parsed.path else ROOT / route.lstrip('/')
            if path.is_dir():
                path /= 'index.html'
            assert path.exists(), f'Broken internal link: {link}'
            if parsed.fragment:
                assert f'id="{parsed.fragment}"' in path.read_text(), f'Missing anchor: {link}'
        if route != '/':
            expect(page.get_by_role('link', name='SMS Consent', exact=True).first).to_be_visible()
    print('PASS: All six routes render, fit mobile, and have valid internal links.')

    page.goto(BASE)
    page.set_viewport_size({'width': 390, 'height': 844})
    toggle = page.get_by_role('button', name='Toggle navigation menu')
    nav = page.get_by_role('navigation', name='Primary', exact=True)
    expect(nav).to_be_hidden()
    toggle.focus()
    page.keyboard.press('Enter')
    expect(nav).to_be_visible()
    page.keyboard.press('Escape')
    expect(nav).to_be_hidden()
    expect(toggle).to_be_focused()
    toggle.click()
    page.get_by_role('link', name='Who it’s for', exact=True).click()
    expect(nav).to_be_hidden()
    expect(toggle).to_have_attribute('aria-expanded', 'false')
    print('PASS: Mobile navigation opens by keyboard and closes on Escape and selection.')

    miss_call = page.locator('#miss-call')
    assert miss_call.evaluate('(el) => getComputedStyle(el).backgroundColor') == 'rgb(37, 99, 235)'
    assert miss_call.bounding_box()['height'] >= 44

    requests = []
    page.on('request', lambda request: requests.append(request.url))
    for label, service, details, preferences, summaries in BRANCHES:
        for detail_index, detail in enumerate(details):
            for preference in preferences:
                page.get_by_role('button', name='Restart', exact=True).click()
                expect(page.locator('#miss-call')).to_be_focused()
                page.keyboard.press('Enter')
                page.get_by_role('button', name=label, exact=True).click()
                page.get_by_role('button', name=detail, exact=True).click()
                page.get_by_role('button', name=preference, exact=True).click()
                expect(page.get_by_role('button', name='See the business side →', exact=True)).to_be_visible()
                ending = page.locator('#messages .automated').last
                expect(ending).to_contain_text('I’ve noted')
                expect(ending).to_contain_text('The team would have that context when they follow up.')
                assert not any(claim in ending.inner_text() for claim in ['I’ve shared', 'I’ve sent', 'I notified', 'I’ll pass along', 'will confirm'])
                assert page.locator('#messages').evaluate('(el) => el.scrollHeight - el.scrollTop - el.clientHeight < 2'), 'Latest message is clipped after choices render'
                page.get_by_role('button', name='See the business side →', exact=True).click()
                expected_service = 'Replacement Quote' if service == 'Installation Quote' and detail_index == 0 else service
                expect(page.locator('#lead-service')).to_have_text(expected_service)
                expect(page.locator('#demo-perspective')).to_have_text('The business experience')
                expect(page.locator('#owner-panel')).to_be_focused()
                expect(page.locator('#lead-summary')).to_contain_text(summaries[detail_index])
                next_steps = {
                    'AC Repair': ['Call Sarah about the cooling issue', 'Call Sarah about the stopped system'],
                    'Installation Quote': ['Discuss replacement scope and timing.', 'Discuss installation scope and timing.'],
                    'HVAC Maintenance': ['Discuss a seasonal tune-up', 'Discuss a system inspection'],
                }
                expect(page.locator('#lead-next-step')).to_have_text(next_steps[service][detail_index])
                if preference == 'Tomorrow works':
                    expect(page.locator('#messages .automated').last).to_contain_text('callback tomorrow')
                if preference == 'Just planning ahead':
                    expect(page.locator('#messages .automated').last).to_contain_text('still comparing options')
                    expect(page.locator('#messages .automated').last).to_contain_text('replace your current system' if detail_index == 0 else 'install a system in a new space')
                if preference == 'Sometime this week':
                    expect(page.locator('#messages .automated').last).to_contain_text('callback this week')
                expect(page.locator('#workflow-statuses .done')).to_have_count(4)
                expect(page.locator('#demo-result')).to_be_visible()
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                page.get_by_role('button', name='View the conversation').click()
                expect(page.locator('#messages')).to_be_focused()
                expect(page.locator('#view-conversation')).to_have_attribute('aria-expanded', 'true')
                expect(page.locator('#messages')).to_contain_text(detail)
                expect(page.locator('#messages')).to_contain_text(preference)
                page.get_by_role('button', name='Hide the conversation').click()
    page.get_by_role('button', name='Try another scenario').click()
    expect(page.locator('#miss-call')).to_be_focused()
    expect(page.locator('#demo-perspective')).to_have_text('The customer experience')
    expect(page.locator('#demo-result')).to_be_hidden()
    page.locator('.demo-consent-details summary').click()
    expect(page.locator('.demo-consent-details p')).to_contain_text('Providing a phone number alone is not consent.')
    page.locator('.demo-consent-details summary').click()
    assert requests == [], f'Demo unexpectedly made network requests: {requests}'
    print('PASS: All 12 conversation paths, accurate lead summaries, four status checks, transcript review, and no network requests.')

    # Exercise timers and restart while the animated flow is still pending.
    page.emulate_media(reduced_motion='no-preference')
    page.get_by_role('button', name='Restart', exact=True).click()
    page.locator('#miss-call').click()
    page.get_by_role('button', name='Restart', exact=True).click()
    page.wait_for_timeout(2500)
    expect(page.locator('#call-state')).to_have_text('Incoming call')
    expect(page.locator('#sms-screen')).to_be_hidden()
    page.locator('#miss-call').click()
    page.get_by_role('button', name='My AC isn’t cooling', exact=True).click()
    page.get_by_role('button', name='Restart', exact=True).click()
    page.wait_for_timeout(1000)
    expect(page.locator('#messages')).to_be_empty()
    expect(page.locator('#reply-choices')).to_be_empty()
    print('PASS: Restart cancels in-flight call transitions and typing callbacks.')

    page.emulate_media(reduced_motion='reduce')
    page.locator('#miss-call').click()
    page.get_by_role('button', name='I need a quote', exact=True).click()
    page.get_by_role('button', name='Replacing my current system', exact=True).click()
    page.get_by_role('button', name='Just planning ahead', exact=True).click()
    expect(page.get_by_role('button', name='See the business side →')).to_be_visible()
    page.emulate_media(reduced_motion='no-preference')
    page.get_by_role('button', name='See the business side →').focus()
    page.keyboard.press('Enter')
    page.evaluate("document.getElementById('demo-reset').click()")
    page.wait_for_timeout(1500)
    expect(page.locator('#owner-panel')).to_be_hidden()
    expect(page.locator('#demo-result')).to_be_hidden()
    expect(page.locator('#call-state')).to_have_text('Incoming call')
    expect(page.locator('.is-leaving')).to_have_count(0)
    print('PASS: Consent detail disclosure, replay, and reset during the owner handoff.')

    # Complete the animated path with only the keyboard, including focus handoffs.
    page.locator('#miss-call').focus()
    page.keyboard.press('Enter')
    for name, count in [('My AC isn’t cooling', 1), ('Running, but blowing warm air', 2), ('As soon as possible', 3)]:
        expect(page.get_by_role('button', name=name, exact=True)).to_be_focused()
        expect(page.locator('#reply-label')).to_contain_text(f'{count} of 3')
        page.keyboard.press('Enter')
    expect(page.get_by_role('button', name='See the business side →')).to_be_focused()
    page.keyboard.press('Enter')
    expect(page.locator('#owner-panel')).to_be_focused()
    expect(page.locator('#workflow-statuses .done')).to_have_count(4)
    expect(page.locator('#demo-result')).to_be_visible()
    print('PASS: Entire animated conversation and business reveal work by keyboard.')

    # Check the phone and handoff at narrow mobile, tablet, and desktop sizes.
    page.emulate_media(reduced_motion='reduce')
    for width in [320, 768, 1440]:
        page.set_viewport_size({'width': width, 'height': 1000})
        page.get_by_role('button', name='Restart', exact=True).click()
        page.locator('#miss-call').click()
        for reply in ['I need a quote', 'Replacing my current system', 'Just planning ahead']:
            button = page.get_by_role('button', name=reply, exact=True)
            expect(button).to_be_visible()
            assert button.bounding_box()['height'] >= 44
            button.click()
        reveal = page.get_by_role('button', name='See the business side →')
        expect(reveal).to_be_visible()
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        page.locator('#phone-shell').screenshot(path=f'/tmp/spark-conversation-{width}.png')
        reveal.click()
        expect(page.locator('#demo-result')).to_be_visible()
        expect(page.locator('#lead-service')).to_have_text('Replacement Quote')
        expect(page.locator('#lead-summary')).to_have_text('Customer wants a quote to replace an existing HVAC system and is still comparing options.')
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        page.locator('#demo-workspace').screenshot(path=f'/tmp/spark-business-{width}.png')
    print('PASS: Phone replies and business handoff fit 320px, tablet, and desktop; reply targets are at least 44px.')

    assert not errors, errors
    print('PASS: No browser runtime errors.')
    browser.close()
