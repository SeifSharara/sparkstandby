"""Read-only live HighLevel check; requires network, Playwright, and local server.
Does not submit the form or enter visitor details. External challenges may block it.
"""
from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 1000})
    page.goto('http://localhost:8000/demo/')
    iframe = page.locator('#inline-5WP9sjNGRUWmi2fYcQGk')
    expect(iframe).to_have_count(1)
    frame = iframe.content_frame
    frame.locator('input[name=first_name]').wait_for(timeout=60000)
    expect(frame.locator('input[type=tel]')).to_have_count(1)
    consent = frame.locator('input[type=checkbox]')
    expect(consent).to_have_count(1)
    expect(consent).not_to_be_checked()
    expect(consent).to_have_attribute('data-required', 'false')
    expect(frame.get_by_role('button', name='Start the live demo')).to_be_visible()
    for label in ['Privacy Policy', 'Terms & Conditions']:
        expect(frame.get_by_role('link', name=label, exact=True)).to_be_visible()
    for width in [1440, 768, 390, 320]:
        page.set_viewport_size({'width': width, 'height': 1000})
        # HighLevel asynchronously reports its height to the parent after resizing.
        page.wait_for_timeout(1500)
        box = iframe.bounding_box()
        inner = frame.locator('body').evaluate('() => ({width:innerWidth, scroll:document.documentElement.scrollWidth, height:document.documentElement.scrollHeight})')
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), width
        assert inner['scroll'] <= inner['width'], (width, inner)
        assert box['height'] >= 448 and inner['height'] <= box['height'] + 2, (width, box, inner)
        page.evaluate('window.scrollTo(0, 0)')
        page.screenshot(path=f'/tmp/spark-live-form-{width}.png', full_page=True)
        print(f'PASS: Loaded HighLevel form fits {width}px without overflow or clipped content.', flush=True)
    print('PASS: One real form, optional unchecked consent, visible submit and legal links. No submission performed.')
    browser.close()
