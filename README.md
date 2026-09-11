# Spark Standby — Business Website

Static HTML/CSS/JavaScript website for Spark Standby, operated by Seif Sharara,
a sole proprietor. No framework, build step, backend, or runtime packages.

## Run and deploy

Run `python3 -m http.server 8000` and open http://localhost:8000/.
Netlify publishes `.` with no build command, using the existing `netlify.toml`.
Routes use directories containing `index.html`:
`/`, `/demo/`, `/demo/ready/`, `/privacy/`, `/terms/`, `/sms-consent/`.
The ready page is noindex and omitted from the sitemap.

The production domain is not configured in the repository. sparkstandby.com is
an intended future domain, not a verified deployment. Canonical/OG URLs and the
sitemap remain relative until the production domain is confirmed.

## Identity and configuration

`js/config.js` supplies the shared header/footer:
- `brandName`: Spark Standby.
- `businessName`: Seif Sharara, the operator and copyright holder.
- `contactPhone` / `contactPhoneDisplay`: +17036781815 / (703) 678-1815.
- `demoPhone` / `demoPhoneDisplay`: +15715565051 / (571) 556-5051.
- Email: seifsharara@gmail.com; location: Sterling, Virginia.

The brand is not represented as an LLC, corporation, or registered DBA.
Contact information, demo phone links, metadata, and legal dates also exist in
static HTML. Update those occurrences together with config; config does not
rewrite static page content. Shared styling is in `css/styles.css`.

## Live demo: pending external integration

Intended flow:
Website opt-in → HighLevel records consent → /demo/ready/ → user calls
571-556-5051 from the submitted mobile number → HighLevel verifies consent →
missed-call demo workflow → clearly identified demo SMS conversation.

The actual form exists externally, but no embed snippet is available here.
`demo/index.html` contains a visibly nonfunctional placeholder at
`#highlevel-form-container` and an exact integration TODO. It has no fields,
submit action, local consent state, API endpoint, or browser PII storage.
All program pages disclose that the live demo is not yet available.

### Next HighLevel steps (external; not implemented here)

1. Obtain the real form embed and replace the entire placeholder. Verify First
   Name and Phone labels, plus a separate optional unchecked non-marketing SMS
   checkbox identifying Spark Standby, operated by Seif Sharara, and the requested
   live demo. Verify frequency, rates, HELP, STOP, and direct legal links.
2. Configure successful form submission to redirect to the production
   `/demo/ready/`, without names, phone numbers, or consent URL parameters.
   Unchecked consent must not prevent submission or grant SMS permission.
3. Verify stored consent status and available timestamp/source/disclosure
   evidence in HighLevel. Confirm returning-contact and prior STOP behavior.
4. Build the external inbound missed-call workflow for +15715565051. Match the
   caller to the submitted number and check affirmative consent and opt-out
   status before sending. A page visit or call alone is never consent. Ensure
   other automations cannot send an unsolicited acknowledgment on submission.
5. Use demo-labeled messages from Spark Standby, operated by Seif Sharara;
   do not impersonate an HVAC contractor. Implement and test HELP and STOP.
6. Test opted-in, unchecked, different-number, unregistered caller, direct-ready
   visit, failed submission, repeated submission, and opted-out scenarios.
7. Verify the embed's network requests, cookies/tracking, retention, and privacy
   statements. Remove preparation notices only after the form and workflow are
   verified. Capture genuine current form evidence and align the A2P submission
   CTA, program description, samples, number, and legal URLs before resubmitting.

`images/ivr-verbal-consent-evidence.png` is retained as historical evidence only.
It describes the retired IVR consent approach and is not linked as current
program evidence. Do not reuse it for the web-form campaign or fabricate evidence.

## Existing simulation

`/#demo` and `js/demo.js` retain the browser-only Northline Heating & Air / Sarah
Mitchell simulation. Both identities are fictional. It makes no API requests,
collects no visitor information, and sends no calls or texts. The homepage links
separately to `/demo/` and explains that live enrollment is pending.
The existing favicon and Open Graph image remain solid-color placeholders.

## Verification

With the local server running and existing Python Playwright/Chromium available:

```sh
python3 tests/check_consent.py
python3 tests/check_site.py
```

Checks cover the six routes, live-demo/consent links, number and identity
consistency, absence of fake submission/state, mobile overflow, navigation,
and all twelve simulation branches. No package installation is needed in the
current development environment. These checks do not verify HighLevel or SMS.
