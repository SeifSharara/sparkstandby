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

## Live demo

`/demo/` embeds the real HighLevel form `5WP9sjNGRUWmi2fYcQGk` and its
provided resizing script. No local fields, fake consent state, PII storage,
or consent query parameters are added. The homepage simulation is separate.

Flow: website opt-in → HighLevel records consent → `/demo/ready/` → caller uses
571-556-5051 from the submitted mobile number → external workflow checks
permission before sending the requested demo SMS.

On September 11, 2026, the public form exposes a separate optional, unchecked
SMS checkbox and a redirect to `https://sparkstandby.netlify.app/demo/ready/`.
This repository does not configure or verify the SMS workflow. Its operator
must verify consent records, same-number matching, opt-outs, STOP/HELP handling,
and the no-consent path before treating the messaging experience as ready.
The ready page provides call instructions; visiting it never grants consent.

See [REFINEMENT-REVIEW.md](REFINEMENT-REVIEW.md) for verification results,
remaining review items, and optional manual HighLevel styling changes.

`images/ivr-verbal-consent-evidence.png` is retained as historical evidence only.
It describes the retired IVR consent approach and is not linked as current
program evidence. Do not reuse it for the web-form campaign or fabricate evidence.

## Existing simulation

`/#demo` and `js/demo.js` retain the browser-only Northline Heating & Air / Sarah
Mitchell simulation. Both identities are fictional. It makes no API requests,
collects no visitor information, and sends no calls or texts. The homepage links
separately to `/demo/` and explains that SMS requires affirmative permission.
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

`python3 tests/check_embed.py` additionally checks the live embed at four widths,
including optional unchecked consent and legal links. It requires network access
and may be blocked by HighLevel/Cloudflare; it never submits or enters PII.

`python3 tests/check_motion.py` checks one-time viewport entry, the hero sequence
budget, reduced-motion changes, stacked pathways, and no-JavaScript visibility.
