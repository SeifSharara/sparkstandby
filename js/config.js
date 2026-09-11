/**
 * SITE CONFIGURATION
 * ===================
 * Edit the values below to update business info across the entire site.
 * This file is loaded on every page and used to fill in contact details,
 * the footer, and the copyright year automatically.
 *
 * NOTE: This is plain static HTML/CSS/JS with no build step, so the
 * email and phone number are also duplicated directly in the HTML of
 * index.html, privacy/index.html, and terms/index.html. If you change
 * them here, update those files too (search for the old value).
 */
window.SITE_CONFIG = {
  // Public brand is separate from the existing legal/operator and SMS identity.
  brandName: "Spark Standby",
  businessName: "Seif Sharara",
  email: "seifsharara@gmail.com",
  contactPhone: "+17036781815",
  contactPhoneDisplay: "(703) 678-1815",
  city: "Sterling",
  state: "Virginia",
  // Leave blank until a public street address is ready to publish.
  streetAddress: "",
  effectiveDate: "September 10, 2026",
  currentYear: "2026",

  // Demo pages also contain static, accessible phone links; update those together.
  demoPhone: "+15715565051",
  demoPhoneDisplay: "(571) 556-5051",

};

/**
 * Renders the shared site header and footer into any page that includes
 * <div id="site-header"></div> and <div id="site-footer"></div>.
 */
(function () {
  function locationLine() {
    var c = window.SITE_CONFIG;
    if (c.streetAddress) {
      return c.streetAddress + ", " + c.city + ", " + c.state;
    }
    return c.city + ", " + c.state;
  }

  function renderHeader() {
    var el = document.getElementById("site-header");
    if (!el) return;
    el.innerHTML =
      '<div class="nav-wrap">' +
      '<a class="brand" href="/">' + window.SITE_CONFIG.brandName + "</a>" +
      '<button class="nav-toggle" id="nav-toggle" aria-expanded="false" aria-controls="primary-nav" aria-label="Toggle navigation menu">' +
      '<span></span><span></span><span></span>' +
      "</button>" +
      '<nav id="primary-nav" class="primary-nav" aria-label="Primary">' +
      '<a href="/#how-it-works">How it works</a>' +
      '<a href="/#industries">Who it’s for</a>' +
      '<a href="/#about">About</a>' +
      '<a href="/demo/">Live Demo</a>' +
      '<a class="nav-cta" href="/#contact">Talk to me <span aria-hidden="true">↗</span></a>' +
      "</nav>" +
      "</div>";

    var toggle = document.getElementById("nav-toggle");
    var nav = document.getElementById("primary-nav");
    if (toggle && nav) {
      toggle.addEventListener("click", function () {
        var isOpen = nav.classList.toggle("open");
        toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
      });
      function closeNav(returnFocus) {
        nav.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
        if (returnFocus) toggle.focus();
      }
      nav.addEventListener("click", function (event) {
        if (event.target.closest("a")) closeNav(false);
      });
      document.addEventListener("keydown", function (event) {
        if (event.key === "Escape" && nav.classList.contains("open")) closeNav(true);
      });
      document.addEventListener("click", function (event) {
        if (!el.contains(event.target)) closeNav(false);
      });
      window.matchMedia("(max-width: 720px)").addEventListener("change", function () { closeNav(false); });
    }
  }

  function renderFooter() {
    var el = document.getElementById("site-footer");
    if (!el) return;
    var c = window.SITE_CONFIG;
    el.innerHTML =
      '<div class="footer-wrap">' +
      '<div class="footer-brand">' +
      "<strong>" + c.brandName + "</strong>" +
      "<span>Operated by " + c.businessName + "</span>" +
      "<span>" + locationLine() + "</span>" +
      '<span><a href="mailto:' + c.email + '">' + c.email + "</a></span>" +
      '<span>General contact: <a href="tel:' + c.contactPhone + '">' + c.contactPhoneDisplay + "</a></span>" +
      "</div>" +
      '<nav class="footer-nav" aria-label="Footer">' +
      '<a href="/">Home</a>' +
      '<a href="/sms-consent/">SMS Consent</a>' +
      '<a href="/privacy/">Privacy Policy</a>' +
      '<a href="/terms/">Terms &amp; Conditions</a>' +
      "</nav>" +
      "</div>" +
      '<div class="footer-bottom"><span>Practical systems. Better follow-through.</span><span>© ' + c.currentYear + " " + c.businessName + ". All rights reserved.</span></div>";
  }

  document.addEventListener("DOMContentLoaded", function () {
    renderHeader();
    renderFooter();
  });
})();
