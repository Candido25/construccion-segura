(() => {
  const FACEBOOK_URL = "https://www.facebook.com/ConstruccionSeguraOficial/";
  const HERO_BRAND_DATA_URI = "data:image/webp;base64,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";
  const HERO_BRAND_ALT = "Afiche de Construcción Segura con vivienda, casco, planos y mensaje de asesoría técnica para proteger la vivienda y la inversión.";

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

  const ensureHeroStyle = () => {
    if (document.getElementById("cs-hero-fit-style")) return;
    const style = document.createElement("style");
    style.id = "cs-hero-fit-style";
    style.textContent = `
      @media (min-width: 1081px) {
        .home-conversion-hero .hero {
          min-height: calc(100svh - 4.15rem);
          padding-top: 4.15rem;
          grid-template-columns: minmax(0, 0.98fr) minmax(30rem, 0.82fr);
        }
        .home-conversion-hero .hero-content {
          min-height: calc(100svh - 4.15rem);
          padding: clamp(1rem, 2vh, 1.4rem) clamp(1.6rem, 2.4vw, 2.2rem) 1rem;
          justify-content: center;
        }
        .home-conversion-hero .hero-brand {
          font-size: clamp(1.9rem, 2.7vw, 2.75rem);
          margin-bottom: 0.35rem;
        }
        .home-conversion-hero .eyebrow {
          margin-bottom: 0.75rem;
          font-size: clamp(0.62rem, 0.72vw, 0.73rem);
          letter-spacing: 0.2em;
        }
        .home-conversion-hero .hero h1 {
          font-size: clamp(2.7rem, 3.75vw, 4.05rem);
          max-width: 14ch;
        }
        .home-conversion-hero .hero-text {
          margin-top: 1.05rem;
          line-height: 1.68;
          font-size: clamp(0.93rem, 0.95vw, 1.02rem);
        }
        .home-conversion-hero .hero-actions {
          margin: 1.45rem 0 1rem;
        }
        .home-conversion-hero .hero-review-panel {
          margin-bottom: 0;
          padding: 0.9rem 1rem;
        }
        .home-conversion-hero .hero-review-panel strong {
          margin-bottom: 0.45rem;
        }
        .home-conversion-hero .hero-review-list li {
          padding-top: 0.38rem;
          padding-bottom: 0.38rem;
          line-height: 1.45;
        }
        .home-conversion-hero .hero-points {
          display: none;
        }
        .authority-strip {
          margin-top: 0.75rem;
        }
      }

      .home-conversion-hero .hero-media-brand {
        display: grid;
        place-items: center;
        min-height: calc(100svh - 4.15rem);
        padding: clamp(0.75rem, 1.2vw, 1.2rem);
        background: #eef2f4;
      }
      .home-conversion-hero .hero-media-brand .hero-image {
        width: 100%;
        height: 100%;
        min-height: 0;
        display: grid;
        place-items: center;
        background: #fff !important;
        filter: none;
        overflow: hidden;
      }
      .home-conversion-hero .hero-media-brand .hero-image img {
        width: 100%;
        height: 100%;
        object-fit: contain;
        object-position: center;
        display: block;
      }

      @media (max-width: 1080px) {
        .home-conversion-hero .hero-media-brand {
          min-height: auto;
          padding: 0.75rem;
        }
        .home-conversion-hero .hero-media-brand .hero-image {
          aspect-ratio: 3 / 2;
          height: auto;
        }
      }
    `;
    document.head.appendChild(style);
  };

  const applyHeroBrandImage = () => {
    ensureHeroStyle();
    document.querySelectorAll(".hero-media-brand .hero-image").forEach((heroImage) => {
      let img = heroImage.querySelector("img[data-hero-brand-image]");
      if (!img) {
        img = document.createElement("img");
        img.dataset.heroBrandImage = "true";
        img.alt = HERO_BRAND_ALT;
        img.width = 1536;
        img.height = 1024;
        img.decoding = "async";
        img.loading = "eager";
        img.fetchPriority = "high";
        heroImage.replaceChildren(img);
      }
      if (img.src !== HERO_BRAND_DATA_URI) {
        img.src = HERO_BRAND_DATA_URI;
      }
      heroImage.dataset.heroBrandReady = "true";
    });
  };

  const applyGlobalEnhancements = () => {
    applyCasesNavigation();
    applyFacebookLinks();
    applyHeroBrandImage();
  };

  applyGlobalEnhancements();
  document.addEventListener("DOMContentLoaded", applyGlobalEnhancements, { once: true });
  [0, 120, 500, 1500].forEach((delay) => window.setTimeout(applyGlobalEnhancements, delay));
})();
