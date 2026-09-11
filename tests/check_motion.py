"""Entry-motion behavior, reduced motion, and no-JavaScript visibility."""
from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width':1440, 'height':1000}, reduced_motion='no-preference')
    page.add_init_script('''
      window.entryAnimations = [];
      const originalAnimate = Element.prototype.animate;
      Element.prototype.animate = function(frames, options) {
        window.entryAnimations.push({hero:!!this.closest('.hero-visual'), path:!!this.closest('.with-followup'), frames, options});
        return originalAnimate.call(this, frames, options);
      };
    ''')
    page.goto('http://localhost:8000/')
    page.locator('.hero-visual').scroll_into_view_if_needed()
    page.wait_for_function('entryAnimations.filter(a => a.hero).length === 5')
    hero = page.evaluate('entryAnimations.filter(a => a.hero)')
    assert [a['options']['delay'] for a in hero] == [0,300,600,900,1200]
    assert max(a['options']['duration'] + a['options']['delay'] for a in hero) < 2500
    page.locator('.with-followup').scroll_into_view_if_needed()
    page.wait_for_function('entryAnimations.filter(a => a.path).length === 4')
    page.evaluate('Promise.all(document.getAnimations().map(a => a.finished.catch(() => {})))')
    page.locator('#about').scroll_into_view_if_needed()
    page.locator('.hero-visual').scroll_into_view_if_needed()
    page.locator('.with-followup').scroll_into_view_if_needed()
    page.wait_for_timeout(100)
    assert page.evaluate('entryAnimations.filter(a => a.hero).length') == 5
    assert page.evaluate('entryAnimations.filter(a => a.path).length') == 4
    assert all(250 <= a['options']['duration'] <= 450 for a in page.evaluate('entryAnimations'))
    page.emulate_media(reduced_motion='reduce')
    page.wait_for_function('document.getAnimations().length === 0')
    expect(page.locator('.with-followup li').last).to_have_css('opacity','1')
    page.reload()
    page.locator('.with-followup').scroll_into_view_if_needed()
    assert page.evaluate('entryAnimations.length') == 0
    print('PASS: Hero sequence under 2.5s, progressive path, one-time playback, and reduced-motion changes.')
    for width in [320,390,768,1024,1440]:
        page.set_viewport_size({'width':width,'height':1000})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        nodes = page.locator('.with-followup li')
        for node in nodes.all():
            assert node.bounding_box()['height'] >= 58
        if width <= 720:
            assert nodes.nth(1).bounding_box()['y'] > nodes.first.bounding_box()['y']
        else:
            assert nodes.nth(1).bounding_box()['x'] > nodes.first.bounding_box()['x']
        if width in [390,768,1440]:
            page.locator('#how-it-works').screenshot(path=f'/tmp/spark-paths-{width}.png')
    static = browser.new_page(java_script_enabled=False)
    static.goto('http://localhost:8000/')
    expect(static.locator('.hero-visual')).to_be_visible()
    expect(static.locator('.with-followup li')).to_have_count(4)
    expect(static.locator('.with-followup li').last).to_be_visible()
    print('PASS: Readable pathways at five widths, mobile stacking, and content visible without JavaScript.')
    browser.close()
