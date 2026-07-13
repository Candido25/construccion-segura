/* Global privacy and legal styles */
if (!document.querySelector('link[href$="privacy.css"]')) {
  const privacyStylesheet = document.createElement("link");
  privacyStylesheet.rel = "stylesheet";
  privacyStylesheet.href = "/privacy.css";
  document.head.appendChild(privacyStylesheet);
}

/* Global site navigation and internal-link enhancements */
if (!document.querySelector('script[src$="site-global.js"]')) {
  const siteGlobalScript = document.createElement("script");
  siteGlobalScript.src = "/site-global.js";
  siteGlobalScript.defer = true;
  document.head.appendChild(siteGlobalScript);
}

/* Privacy-first Google Analytics 4 */
const GA_MEASUREMENT_ID = "G-P6R5L9D52M";
const COOKIE_CONSENT_KEY = "cs_cookie_consent_v1";
const COOKIE_CONSENT_ACCEPTED = "analytics";
const COOKIE_CONSENT_NECESSARY = "necessary";
let analyticsReady = false;

const readCookieConsent = () => {
  try {
    return window.localStorage.getItem(COOKIE_CONSENT_KEY);
  } catch {
    return null;
  }
};

const writeCookieConsent = (value) => {
  try {
    window.localStorage.setItem(COOKIE_CONSENT_KEY, value);
  } catch {
    // The choice still applies during the current page view.
  }
};

const deleteCookie = (name) => {
  const hostParts = window.location.hostname.split(".");
  const domains = ["", window.location.hostname];

  if (hostParts.length >= 2) {
    domains.push(`.${hostParts.slice(-2).join(".")}`);
  }

  domains.forEach((domain) => {
    const domainPart = domain ? `; domain=${domain}` : "";
    document.cookie = `${name}=; Max-Age=0; path=/${domainPart}; SameSite=Lax`;
  });
};

const removeAnalyticsCookies = () => {
  document.cookie
    .split(";")
    .map((cookie) => cookie.trim().split("=")[0])
    .filter((name) => name === "_ga" || name.startsWith("_ga_"))
    .forEach(deleteCookie);
};

const initializeAnalytics = () => {
  if (analyticsReady) return;

  window[`ga-disable-${GA_MEASUREMENT_ID}`] = false;
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function gtag() {
    window.dataLayer.push(arguments);
  };

  window.gtag("js", new Date());
  window.gtag("config", GA_MEASUREMENT_ID, {
    send_page_view: true,
    page_title: document.title,
    page_location: window.location.href,
    allow_google_signals: false,
    allow_ad_personalization_signals: false
  });

  if (!document.querySelector("script[data-analytics-loader]")) {
    const analyticsScript = document.createElement("script");
    analyticsScript.async = true;
    analyticsScript.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(GA_MEASUREMENT_ID)}`;
    analyticsScript.dataset.analyticsLoader = "true";
    document.head.appendChild(analyticsScript);
  }

  analyticsReady = true;
};

const disableAnalytics = () => {
  window[`ga-disable-${GA_MEASUREMENT_ID}`] = true;
  removeAnalyticsCookies();
  analyticsReady = false;
};

const buildLegalLinks = () => {
  if (document.querySelector(".legal-links")) return;

  const legalLinks = document.createElement("div");
  legalLinks.className = "legal-links";
  legalLinks.setAttribute("aria-label", "Información legal y privacidad");
  legalLinks.innerHTML = `
    <a href="/politica-privacidad.html">Privacidad</a>
    <a href="/politica-cookies.html">Cookies</a>
    <a href="/condiciones-servicio.html">Condiciones del servicio</a>
    <button type="button" data-cookie-settings>Configurar cookies</button>
  `;

  const footer = document.querySelector("footer");
  if (footer) {
    footer.appendChild(legalLinks);
  } else {
    document.body.appendChild(legalLinks);
  }
};

const closeCookieBanner = () => {
  document.querySelector(".cookie-banner")?.remove();
};

const applyCookieConsent = (value) => {
  writeCookieConsent(value);

  if (value === COOKIE_CONSENT_ACCEPTED) {
    initializeAnalytics();
  } else {
    disableAnalytics();
  }

  closeCookieBanner();
};

const showCookieBanner = () => {
  closeCookieBanner();

  const banner = document.createElement("aside");
  banner.className = "cookie-banner";
  banner.setAttribute("role", "dialog");
  banner.setAttribute("aria-modal", "false");
  banner.setAttribute("aria-labelledby", "cookie-banner-title");
  banner.innerHTML = `
    <div class="cookie-banner__content">
      <div>
        <strong id="cookie-banner-title">Tu privacidad importa</strong>
        <p>Usamos almacenamiento necesario para recordar tu elección. Google Analytics solo se activa si aceptas la medición; no usamos cookies publicitarias.</p>
        <div class="cookie-banner__links">
          <a href="/politica-cookies.html">Política de cookies</a>
          <a href="/politica-privacidad.html">Política de privacidad</a>
        </div>
      </div>
      <div class="cookie-banner__actions">
        <button class="cookie-button cookie-button--secondary" type="button" data-cookie-reject>Solo necesarias</button>
        <button class="cookie-button cookie-button--primary" type="button" data-cookie-accept>Aceptar analítica</button>
      </div>
    </div>
  `;

  document.body.appendChild(banner);
  banner.querySelector("[data-cookie-accept]")?.addEventListener("click", () => {
    applyCookieConsent(COOKIE_CONSENT_ACCEPTED);
  });
  banner.querySelector("[data-cookie-reject]")?.addEventListener("click", () => {
    applyCookieConsent(COOKIE_CONSENT_NECESSARY);
  });
};

buildLegalLinks();

document.addEventListener("click", (event) => {
  if (event.target.closest("[data-cookie-settings]")) {
    showCookieBanner();
  }
});

const savedConsent = readCookieConsent();
if (savedConsent === COOKIE_CONSENT_ACCEPTED) {
  initializeAnalytics();
} else if (savedConsent === COOKIE_CONSENT_NECESSARY) {
  disableAnalytics();
} else {
  showCookieBanner();
}
