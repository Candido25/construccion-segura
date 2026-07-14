const FACEBOOK_URL = "https://www.facebook.com/ConstruccionSeguraOficial/";
const HERO_BRAND_SOURCE = "/assets/brand/portada-principal-construccion-segura.webp?v=20260714-3";
const HERO_BRAND_FALLBACK = "/assets/site-photos/web/hero-portada.webp";
let heroBrandObjectUrl = null;
let heroBrandLoadPromise = null;

const applyCasesNavigation = () => {
  const navigation = document.querySelector(".site-nav");
  if (navigation && !navigation.querySelector('a[href$="casos-de-obra.html"]')) {
    const casesLink = document.createElement("a");
    casesLink.href = "/casos-de-obra.html";
    casesLink.textContent = "Casos de obra";
    casesLink.dataset.track = "cases_navigation";

    const libraryLink = Array.from(navigation.querySelectorAll("a")).find((link) =>
      (link.getAttribute("href") || "").includes("biblioteca-tecnica.html")
    );

    if (libraryLink) {
      navigation.insertBefore(casesLink, libraryLink);
    } else {
      const callToAction = navigation.querySelector(".nav-cta");
      navigation.insertBefore(casesLink, callToAction || null);
    }
  }

  if (window.location.pathname.endsWith("/casos-de-obra.html")) {
    navigation?.querySelector('a[href$="casos-de-obra.html"]')?.setAttribute("aria-current", "page");
  }

  document.querySelectorAll('a[href*="errores/caso-anonimo-vivienda-multifamiliar-seis-niveles.html"]').forEach((link) => {
    link.href = "/casos/seguimiento-vivienda-multifamiliar-seis-niveles.html";
  });

  const topicLibrary = document.querySelector(".topic-library-grid");
  const caseCard = topicLibrary?.querySelector('a[href$="seguimiento-vivienda-multifamiliar-seis-niveles.html"]');
  if (caseCard) {
    caseCard.querySelector("strong")?.replaceChildren("Seguimiento de vivienda multifamiliar");
    caseCard.querySelector("span")?.replaceChildren("Hallazgos, buenas prácticas, correcciones y aspectos pendientes de verificar.");
  }

  const homeResourcesActions = document.querySelector(".home-conversion-hero .resources .hero-actions");
  if (homeResourcesActions && !homeResourcesActions.querySelector('a[href$="casos-de-obra.html"]')) {
    const casesButton = document.createElement("a");
    casesButton.className = "button button-secondary";
    casesButton.href = "/casos-de-obra.html";
    casesButton.dataset.track = "cases_home_resources";
    casesButton.textContent = "Ver casos de obra";
    homeResourcesActions.appendChild(casesButton);
  }
};

const applyFacebookLinks = () => {
  const navigation = document.querySelector(".site-nav");
  if (navigation && !navigation.querySelector('[data-social="facebook"]')) {
    const facebookLink = document.createElement("a");
    facebookLink.href = FACEBOOK_URL;
    facebookLink.textContent = "Facebook";
    facebookLink.target = "_blank";
    facebookLink.rel = "noopener noreferrer";
    facebookLink.dataset.social = "facebook";
    facebookLink.dataset.track = "facebook_navigation";
    facebookLink.setAttribute("aria-label", "Abrir Facebook oficial de Construcción Segura en una pestaña nueva");

    const callToAction = navigation.querySelector(".nav-cta");
    navigation.insertBefore(facebookLink, callToAction || null);
  }

  const homeContactBlock = document.querySelector(".home-conversion-hero .contact-block");
  if (homeContactBlock && !homeContactBlock.querySelector('[data-social="facebook"]')) {
    const facebookContactLink = document.createElement("a");
    facebookContactLink.href = FACEBOOK_URL;
    facebookContactLink.textContent = "Facebook: Construcción Segura Oficial";
    facebookContactLink.target = "_blank";
    facebookContactLink.rel = "noopener noreferrer";
    facebookContactLink.dataset.social = "facebook";
    facebookContactLink.dataset.track = "facebook_home_contact";
    facebookContactLink.setAttribute("aria-label", "Abrir Facebook oficial de Construcción Segura en una pestaña nueva");

    const emailLink = homeContactBlock.querySelector('a[href^="mailto:"]');
    if (emailLink?.nextSibling) {
      homeContactBlock.insertBefore(facebookContactLink, emailLink.nextSibling);
    } else {
      homeContactBlock.appendChild(facebookContactLink);
    }
  }
};

const readAscii = (bytes, start, length) =>
  String.fromCharCode(...bytes.subarray(start, start + length));

const buildRepairedHeroUrl = async () => {
  const response = await fetch(HERO_BRAND_SOURCE, { cache: "force-cache" });
  if (!response.ok) {
    throw new Error(`No se pudo cargar la imagen de portada: ${response.status}`);
  }

  const bytes = new Uint8Array(await response.arrayBuffer());
  if (bytes.length < 20 || readAscii(bytes, 0, 4) !== "RIFF") {
    throw new Error("El archivo de portada no contiene una cabecera RIFF válida.");
  }

  if (readAscii(bytes, 8, 4) !== "WEBP") {
    bytes.set([0x57, 0x45, 0x42, 0x50], 8);
  }

  const webpChunk = readAscii(bytes, 12, 4);
  if (!webpChunk.startsWith("VP8")) {
    throw new Error("El archivo reparado no contiene datos WebP reconocibles.");
  }

  const blob = new Blob([bytes], { type: "image/webp" });
  heroBrandObjectUrl = URL.createObjectURL(blob);
  return heroBrandObjectUrl;
};

const applyHeroBrandImage = () => {
  const heroImages = document.querySelectorAll(".hero-media-brand .hero-image");
  if (!heroImages.length) return;

  heroImages.forEach((heroImage) => {
    heroImage.style.backgroundImage = `linear-gradient(200deg, rgba(255, 255, 255, 0.01), rgba(20, 34, 42, 0.08)), url("${HERO_BRAND_FALLBACK}")`;
    heroImage.style.backgroundPosition = "center, center";
    heroImage.style.backgroundSize = "cover, cover";
    heroImage.style.backgroundRepeat = "no-repeat";
  });

  heroBrandLoadPromise ||= buildRepairedHeroUrl();
  heroBrandLoadPromise
    .then((imageUrl) => {
      heroImages.forEach((heroImage) => {
        heroImage.style.backgroundImage = `linear-gradient(200deg, rgba(255, 255, 255, 0.01), rgba(20, 34, 42, 0.08)), url("${imageUrl}")`;
        heroImage.dataset.heroBrandReady = "true";
      });
    })
    .catch((error) => {
      console.error("No fue posible mostrar la imagen principal de Construcción Segura.", error);
    });
};

const applyGlobalEnhancements = () => {
  applyCasesNavigation();
  applyFacebookLinks();
  applyHeroBrandImage();
};

applyGlobalEnhancements();
document.addEventListener("DOMContentLoaded", applyGlobalEnhancements, { once: true });
window.setTimeout(applyGlobalEnhancements, 0);
window.setTimeout(applyGlobalEnhancements, 120);
window.addEventListener("pagehide", () => {
  if (heroBrandObjectUrl) URL.revokeObjectURL(heroBrandObjectUrl);
}, { once: true });
