# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary users are owners/managers of local service businesses (e.g. contractors, clinics, and similar) evaluating Spark Standby for lead follow-up and customer communication systems. They land on the site to assess credibility and decide whether to reach out by email or phone.

## Product Purpose

The site serves two durable purposes:
1. A business marketing site for Spark Standby, operated by Seif Sharara, providing missed-call follow-up and customer communication systems for home-service businesses.
2. Public documentation required for A2P 10DLC SMS registration: SMS Consent, Privacy Policy, and Terms & Conditions pages, each independently reachable at a stable clean URL (`/demo/`, `/sms-consent/`, `/privacy/`, `/terms/`).

## Positioning

Practical, easy-to-manage lead follow-up and communication systems for local service businesses — not a generic marketing agency or a complex enterprise automation platform.

## Operating Context

- Static site, no build step, no backend (plain HTML/CSS/JS).
- Deployed on Netlify; each legal/consent page is its own folder with its own `index.html` for clean URLs.
- Shared header/footer and all business contact info (`brandName`, `businessName`, `email`, `contactPhone`, `demoPhone`, `city`/`state`, `effectiveDate`) are configured in `js/config.js` (`window.SITE_CONFIG`) for shared navigation/footer. Static HTML contact details and dates must be updated separately.
- Business is based in Sterling, Virginia.

## Capabilities and Constraints

- No build tools/framework — must remain plain static HTML/CSS/JS per README.
- Favicon and OG image (`images/favicon.png`, `images/og-image.png`) are solid-color placeholders pending real brand assets.
- Canonical/OG URLs and `sitemap.xml` currently use relative paths pending a final custom domain.
- Compliance constraint (A2P 10DLC): no fake claims, testimonials, client counts, or statistics; no purchased/rented/affiliate lead-list language.

## Brand Commitments

Public working brand: "Spark Standby", presented as a text-only wordmark using
existing typography. No spark/star/lightning logo and no "SS" monogram.

Primary tagline: "When you can’t answer, Spark stands by."

Founder and existing legal/operator/SMS identity: "Seif Sharara" — preserved in
legal documents and the A2P disclosure. `brandName` and `businessName` are separate
configuration fields. The shared footer says Spark Standby is operated by Seif
Sharara; no new registered entity is implied.

The fictional Northline Heating & Air identity remains inside the customer demo.
The approved warm-white, charcoal, and blue design and static deployment stay in
place. sparkstandby.com is an intended future domain, not a configured site URL.

## Evidence on Hand

No testimonials, case studies, client counts, or press are present or should be fabricated — the pre-submission checklist explicitly prohibits fake claims/statistics.

## Product Principles

- Stay practical and plain-spoken, not agency-generic — the service is about fixing a concrete problem (slow follow-up, missed calls), not abstract "automation."
- Never fabricate credibility signals (testimonials, stats, client counts); credibility comes from clarity and directness instead.
- Keep the legal/consent pages independently reachable and unambiguous — they are load-bearing for SMS registration compliance, not incidental footer links.
- Keep the site technically simple (no build step) so contact info and dates stay trivially editable via `js/config.js`.

## Accessibility & Inclusion

No product-specific accessibility requirement established beyond standard web accessibility practice.

## Live Demo Readiness

`/demo/` explains the requested non-marketing demonstration and contains a
clearly labeled HighLevel form placeholder. No local form or consent state exists.
`/demo/ready/` provides same-number calling instructions, is noindex, and does
not establish consent. Both pages disclose that the live demo is not yet available.

Intended flow: website opt-in → HighLevel records consent → /demo/ready/ →
user calls 571-556-5051 → HighLevel verifies consent → missed-call demo workflow
→ demo SMS conversation. SMS consent is separate, optional, and unchecked;
phone entry alone is not consent. General contact remains 703-678-1815.

The external HighLevel embed must be supplied, and its workflow must still be
built and tested. The legal and SMS pages describe this pending web-form flow.
The old IVR evidence image is historical only, not current consent evidence.
New genuine evidence must be captured after deployment and verification.
