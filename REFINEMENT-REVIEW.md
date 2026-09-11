# Spark Standby refinement review

September 11, 2026. Local changes only; not committed, pushed, or deployed.

## 1. Files changed

- `index.html`: five-section homepage, shorter copy, compact services and founder/contact sections.
- `css/styles.css`: shared theme, spacing, form wrapper, simulation controls, responsive refinements; removed obsolete section styles.
- `js/demo.js`: clearer role instructions, detail-aware quote replies, concise business summaries.
- `js/config.js`: preferred navigation order and updated legal revision date.
- `demo/index.html`: form-first layout, native outer wrapper, three steps below the form.
- `demo/ready/index.html`: focused call instructions and quiet disclosures.
- `privacy/index.html`, `terms/index.html`: corrected stale form-availability notes, updated revision dates, added keyboard skip links. Substantive consent and legal provisions preserved.
- `sms-consent/index.html`: accurate connected-form status and reviewer-facing verification note; consent disclosure preserved.
- `tests/check_consent.py`, `tests/check_site.py`: updated checks for the refined content and simulation.
- `tests/check_embed.py`: new read-only live iframe check; never enters PII or submits.
- `README.md`, `PRODUCT.md`: current integration status and test instructions.
- `REFINEMENT-REVIEW.md`: this review and manual HighLevel notes.

## 2. Sections removed

Removed the standalone five-step process, “A better starting point” comparison,
repeated industry strip, six large industry cards, separate capabilities matrix,
and separate closing CTA. Removed numbered marketing-section labels.

## 3. Sections merged

The homepage now has five major sections instead of nine:
hero; problem/outcome journey; simulation; industries plus possible follow-up
workflows; founder plus contact. `#how-it-works`, `#demo`, `#industries`, `#services`,
`#about`, and `#contact` all resolve to relevant content.

## 4. Copy materially rewritten

Shortened the hero support, problem explanation, simulation introduction,
industry/expansion copy, founder story, live-demo introduction and ready-page
instructions. Kept the headline, blue emphasis, tagline, and two hero CTAs.
Removed the simulated result’s implied guarantee that the lead was not lost.

## 5. Simulation improvements

Blue active Miss Call button with an explicit instruction. Clear Sarah role-play
and explanation that reply buttons are simulation controls, while real messages
use SMS. Quote endings reflect both replacement/new-installation choice and
readiness. Business cards prioritize service, summary, and next step, followed
by four compact status checks. Fictional identity, assumed consent, STOP text,
no-real-lead notice, transcript review, keyboard focus, and reset remain intact.
Reply targets are at least 44px tall, including narrow mobile.

## 6. Live demo improvements

The original iframe and supplied embedding script remain unchanged. Form moved
immediately below the short intro; removed dashed outer card and duplicate
standalone legal links. Privacy and Terms remain inside the form and in the
shared footer. Three steps follow the form. Ready page leads with same-number
calling instructions and its call button. No local fields, consent state,
PII storage, or PII URL parameters were added.

## 7. Theme/design refinements

Warmer off-white `#F8F8F3`, softer charcoal `#202322`, quiet borders `#E5E6E0`,
existing electric blue `#2563EB`, softer corners, tighter section/footer spacing,
less uppercase tracking, fewer dividers and grids. No new framework, libraries,
fonts, stock imagery, or animation dependencies.

## 8. A2P/legal content preserved

Operator and sole-proprietor identity; affirmative, separate, optional unchecked
SMS consent; phone number alone is not consent; STOP/HELP; frequency/rates;
mobile-information privacy and restrictions on marketing sharing; no SMS without
opt-in; direct ready-page visit is not consent; no dispatch, diagnosis, or real
HVAC appointment. The 571 number remains the demo number; 703 remains general
contact. No active 857 number or retired IVR-evidence link is present.

Only stale operational status text and dates changed in Privacy/Terms; their
substantive provisions were not shortened. SMS Consent still explicitly notes
that the external messaging workflow requires end-to-end verification.

## 9. Remaining iframe mismatch

HighLevel controls its own font metrics, stronger labels, checkbox alignment,
field borders, button styling, and card shadow. The outer site now fits it
without a second card. No cross-origin CSS or event interception was added.

## 10. Recommended manual HighLevel styling

Optional changes inside HighLevel only, if supported by its form settings:

- Match the site's system sans-serif stack; avoid adding font dependencies.
- Keep consent at least 16px, normal weight, line-height around 1.5–1.6.
- Align the checkbox with the start of its disclosure instead of the middle.
- Use a neutral white/off-white form background, 18px outer radius, and a lighter or absent card shadow.
- Use subtle `#E5E6E0` field borders and 9px field/button radii.
- Match labels to soft charcoal `#202322` rather than dark navy.
- Slightly tighten field spacing if supported, keeping labels and consent easy to read.
- Use `#2563EB` for the primary button; maintain white text and 44px minimum height.
- Preserve the complete disclosure, optional/unchecked state, legal links,
  cookie-consent attributes, redirect and workflow behavior.

None of these HighLevel changes were made as part of this refinement.

## 11. Verification and review before deployment

Passed:

- `python3 tests/check_consent.py` and JavaScript syntax/whitespace checks.
- `python3 tests/check_site.py`: six routes at nine widths (320–1920px), all
  twelve reply paths, all navigation/anchors, keyboard operation, reset during
  timers and handoff, transcript review, no simulation network requests/errors.
- Narrow-mobile/tablet/desktop simulation snapshots; no horizontal overflow;
  reply targets at least 44px tall.
- `python3 tests/check_embed.py`: real form loaded at 320, 390, 768, 1440px;
  automatic iframe height, no clipped content, optional unchecked SMS checkbox,
  and visible submit/legal links.

The current public HighLevel configuration points successful submission to
`https://sparkstandby.netlify.app/demo/ready/`. The former required-checkbox
problem has been corrected externally: it is now optional and unchecked.
A test with the previously authorized details and SMS unchecked encountered a
Cloudflare challenge and did not redirect. Actual successful submission is
therefore **not verified**. No CAPTCHA workaround or HighLevel modification was
attempted, and SMS consent was left unchecked.

Before deployment, manually test a successful submission in a normal browser,
confirm the ready URL loads publicly, and verify the real messaging workflow
(consent/opt-out checks and STOP/HELP). The ready-page preparation block was
removed as requested for the intended live experience; that copy does not
establish that the external workflow has passed testing. This pass does not
claim that any SMS was delivered or that Netlify deployment was verified.


## Final polish pass

The five-section homepage and all existing page structures are preserved.
Only these files changed in the final polish pass:
`index.html`, `css/styles.css`, `js/demo.js`, `tests/check_site.py`, and this review.
Earlier refinement changes remain in the working tree; nothing was deployed.

### Copy and simulation honesty

All six scenario endings now use “I’ve noted…” and “The team would have that
context when they follow up.” Removed claims of sharing information and future
handoff promises. Requested callback preferences remain preferences, not
promised timing. The card is labeled “Example missed-call lead”; screen-reader
announcements now explicitly describe simulated actions and an example lead.
The key takeaway, Sarah instructions, four checklist items and simulation-only
reply-button explanation remain intact. Hero and founder copy are unchanged.

### Visual polish

Cards now share the existing 18px radius; controls use the existing 9px radius.
The phone silhouette and chat bubbles retain their distinct shapes. Hero,
Miss Call and business-reveal actions have a consistent 48px minimum height;
reply choices retain at least 44px. Mobile hero CTAs stack at equal full width.
Tightened hero rhythm, desktop section spacing, founder gap, and space beneath
the form. Comparison labels and tablet steps are larger; the final conversation
outcome has stronger blue emphasis. The form wrapper is transparent, without
another card surface. The consent explanation is quieter but readable.
Capability pills, including AI-assisted conversations, retain equal weight.

### Final QA

Passed all three existing suites: `check_consent.py`, `check_site.py`, and
`check_embed.py`, plus JavaScript syntax and whitespace checks. Checks cover
all 12 simulation paths, honest ending language, reset during transitions,
keyboard operation, links, the ready phone link, nine site widths, and the real
HighLevel form at four widths. Reviewed mobile conversation and form captures.
No horizontal overflow, clipped final messages or tiny reply targets were found.
Live-demo HTML, ready HTML, Privacy, Terms, and SMS Consent are byte-for-byte
unchanged from the start of this polish pass; all A2P disclosures are preserved.

The iframe's internal styling remains controlled by HighLevel. Manual styling
recommendations are in section 10. A normal-browser successful submission and
real SMS workflow test remain outstanding from the earlier Cloudflare-blocked
attempt. This polish pass did not resubmit personal details or modify HighLevel.
