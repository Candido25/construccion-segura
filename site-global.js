const FACEBOOK_URL = "https://www.facebook.com/ConstruccionSeguraOficial/";
const HERO_BRAND_WEBP = "/assets/brand/portada-principal-construccion-segura.webp";

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
    facebookContactLink.textContent = "Facebook: Construcción Segura";
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

const applyHeroBrandImage = () => {
  document.querySelectorAll(".hero-media-brand .hero-image").forEach((heroImage) => {
    heroImage.style.backgroundImage = `linear-gradient(200deg, rgba(255, 255, 255, 0.01), rgba(20, 34, 42, 0.08)), url("${HERO_BRAND_WEBP}")`;
    heroImage.style.backgroundPosition = "center, center";
    heroImage.style.backgroundSize = "cover, cover";
    heroImage.style.backgroundRepeat = "no-repeat";
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