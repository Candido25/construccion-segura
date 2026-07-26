/* Privacy and Analytics bootstrap */
const privacyScript = document.createElement("script");
privacyScript.src = "/privacy.js";
privacyScript.async = false;
document.head.appendChild(privacyScript);

/* Menu toggle */
const menuToggle = document.querySelector(".menu-toggle");
const siteNav = document.querySelector(".site-nav");
const navLinks = document.querySelectorAll(".site-nav a");

if (menuToggle && siteNav) {
  const closeMenu = () => {
    siteNav.classList.remove("is-open");
    menuToggle.setAttribute("aria-expanded", "false");
  };

  menuToggle.addEventListener("click", () => {
    const isOpen = siteNav.classList.toggle("is-open");
    menuToggle.setAttribute("aria-expanded", String(isOpen));
  });

  navLinks.forEach((link) => link.addEventListener("click", closeMenu));

  document.addEventListener("click", (event) => {
    if (!siteNav.contains(event.target) && !menuToggle.contains(event.target)) {
      closeMenu();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeMenu();
  });
}

/* Header scroll shadow */
const header = document.querySelector(".site-header");
if (header) {
  const onScroll = () => header.classList.toggle("scrolled", window.scrollY > 40);
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
}

/* Reveal on scroll */
const revealTargets = document.querySelectorAll(".section, .hero-content, .reveal");

if ("IntersectionObserver" in window) {
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;

        const children = entry.target.querySelectorAll(
          ".tip-card, .mistake-card, .service-item, .case-card, .testimonial-card, .faq-card, .timeline article, .story-values article, .price-card"
        );

        if (children.length > 1) {
          children.forEach((child, index) => {
            child.style.transitionDelay = `${index * 75}ms`;
            child.classList.add("reveal");
            requestAnimationFrame(() => child.classList.add("is-visible"));
          });
        }

        entry.target.classList.add("is-visible");
        revealObserver.unobserve(entry.target);
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -5% 0px" }
  );

  revealTargets.forEach((element) => {
    element.classList.add("reveal");
    revealObserver.observe(element);
  });
} else {
  revealTargets.forEach((element) => element.classList.add("is-visible"));
}

/* Floating CTA visibility */
const floatingCta = document.querySelector(".floating-cta");
if (floatingCta) {
  let shown = false;

  const updateFloatingCta = () => {
    const shouldShow = window.scrollY > window.innerHeight * 0.5;
    if (shouldShow === shown) return;

    shown = shouldShow;
    floatingCta.style.opacity = shown ? "1" : "0";
    floatingCta.style.transform = shown ? "translateY(0)" : "translateY(8px)";
    floatingCta.style.pointerEvents = shown ? "auto" : "none";
  };

  floatingCta.style.opacity = "0";
  floatingCta.style.transform = "translateY(8px)";
  floatingCta.style.transition = "opacity 0.4s ease, transform 0.4s ease";
  floatingCta.style.pointerEvents = "none";
  window.addEventListener("scroll", updateFloatingCta, { passive: true });
  updateFloatingCta();
}

/* Optional logo lightbox retained for legacy pages */
const brandZoomTriggers = document.querySelectorAll(".brand-zoom-trigger");
const logoLightbox = document.querySelector(".logo-lightbox");
const logoLightboxBackdrop = document.querySelector(".logo-lightbox-backdrop");
const logoLightboxClose = document.querySelector(".logo-lightbox-close");

if (brandZoomTriggers.length && logoLightbox) {
  const closeLogoLightbox = () => {
    logoLightbox.classList.remove("is-open");
    logoLightbox.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  };

  const openLogoLightbox = () => {
    logoLightbox.classList.add("is-open");
    logoLightbox.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    logoLightboxClose?.focus();
  };

  brandZoomTriggers.forEach((trigger) => {
    trigger.addEventListener("click", (event) => {
      event.preventDefault();
      openLogoLightbox();
    });
  });

  logoLightboxBackdrop?.addEventListener("click", closeLogoLightbox);
  logoLightboxClose?.addEventListener("click", closeLogoLightbox);

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && logoLightbox.classList.contains("is-open")) {
      closeLogoLightbox();
    }
  });
}

/* Conversion and navigation event tracking */
const inferTrackingEvent = (link) => {
  const explicitEvent = link.dataset.track?.trim();
  if (explicitEvent) return explicitEvent;

  const href = link.getAttribute("href") || "";
  const normalizedHref = href.toLowerCase();

  if (normalizedHref.includes("wa.me/") || normalizedHref.includes("whatsapp.com/")) {
    return "whatsapp_click";
  }

  if (normalizedHref.startsWith("mailto:")) return "email_click";
  if (normalizedHref.startsWith("tel:")) return "phone_click";
  if (normalizedHref.includes("servicios.html")) return "services_navigation";
  if (normalizedHref.includes("contacto.html") || normalizedHref === "#contacto") {
    return "contact_navigation";
  }

  try {
    const destinationUrl = new URL(href, window.location.href);
    if (destinationUrl.origin !== window.location.origin) return "outbound_click";
  } catch {
    return null;
  }

  return null;
};

const sendAnalyticsEvent = (eventName, parameters) => {
  if (typeof window.gtag !== "function") return;
  window.gtag("event", eventName, parameters);
};

document.addEventListener("click", (event) => {
  const link = event.target.closest("a");
  if (!link) return;

  const eventName = inferTrackingEvent(link);
  if (!eventName) return;

  const destination = link.getAttribute("href") || "";
  const linkText = (link.textContent || "").replace(/\s+/g, " ").trim().slice(0, 120);
  const eventParameters = {
    event_category: "conversion",
    link_url: destination,
    link_text: linkText,
    page_path: window.location.pathname,
    page_title: document.title
  };

  sendAnalyticsEvent(eventName, eventParameters);

  if (["whatsapp_contact", "whatsapp_floating", "whatsapp_click", "email_contact", "email_click", "phone_click"].includes(eventName)) {
    sendAnalyticsEvent("generate_lead", {
      ...eventParameters,
      method: eventName.startsWith("whatsapp")
        ? "whatsapp"
        : eventName.startsWith("email")
          ? "email"
          : "phone"
    });
  }
});

/* Ongoing anonymous case highlighted in the technical library */
const errorTopicLibrary = document.querySelector(".topic-library-grid");
if (errorTopicLibrary && window.location.pathname.endsWith("/errores-frecuentes.html")) {
  const caseHref = "errores/caso-anonimo-vivienda-multifamiliar-seis-niveles.html";
  const alreadyListed = errorTopicLibrary.querySelector(`a[href="${caseHref}"]`);

  if (!alreadyListed) {
    const caseLink = document.createElement("a");
    caseLink.className = "topic-library-card";
    caseLink.href = caseHref;
    caseLink.dataset.track = "case_multifamily_library";
    caseLink.innerHTML = "<strong>Seguimiento de vivienda multifamiliar</strong><span>Hallazgos por corregir, mejoras y buenas prácticas documentadas.</span>";
    errorTopicLibrary.prepend(caseLink);
  }
}

/* Reusable accessible lightbox for technical photographs */
const technicalPhotoCandidates = Array.from(
  document.querySelectorAll("main figure img:not([data-no-lightbox]), main img[data-technical-photo]")
).filter((image) => {
  const source = image.dataset.fullSrc || image.currentSrc || image.getAttribute("src");
  const linkedWithoutOptIn = image.closest("a") && !image.hasAttribute("data-technical-photo");
  return Boolean(source) && !linkedWithoutOptIn;
});

if (technicalPhotoCandidates.length) {
  const lightboxStyles = document.createElement("link");
  lightboxStyles.rel = "stylesheet";
  lightboxStyles.href = "/technical-lightbox.css";
  document.head.appendChild(lightboxStyles);

  const absoluteSource = (source) => {
    try {
      return new URL(source, document.baseURI).href;
    } catch {
      return source;
    }
  };

  const captionForImage = (image) => {
    const explicitCaption = image.dataset.caption?.trim();
    const figureCaption = image.closest("figure")?.querySelector("figcaption")?.textContent?.replace(/\s+/g, " ").trim();
    return explicitCaption || figureCaption || image.alt?.trim() || "Fotografía técnica";
  };

  const itemBySource = new Map();
  const sourceForImage = new WeakMap();

  technicalPhotoCandidates.forEach((image) => {
    const source = absoluteSource(image.dataset.fullSrc || image.currentSrc || image.getAttribute("src"));
    const caption = captionForImage(image);
    const isDetailedCasePhoto = Boolean(image.closest(".case-photo"));
    const existingItem = itemBySource.get(source);

    if (!existingItem) {
      itemBySource.set(source, {
        source,
        caption,
        alt: image.alt?.trim() || caption,
        preferred: isDetailedCasePhoto
      });
    } else if (isDetailedCasePhoto || (!existingItem.preferred && caption.length > existingItem.caption.length)) {
      existingItem.caption = caption;
      existingItem.alt = image.alt?.trim() || caption;
      existingItem.preferred = isDetailedCasePhoto;
    }

    sourceForImage.set(image, source);
  });

  const technicalPhotoItems = Array.from(itemBySource.values());
  const indexBySource = new Map(technicalPhotoItems.map((item, index) => [item.source, index]));
  let activeIndex = 0;
  let previouslyFocusedElement = null;
  let closeTimer = null;

  const lightbox = document.createElement("div");
  lightbox.className = "technical-lightbox";
  lightbox.hidden = true;
  lightbox.setAttribute("aria-hidden", "true");
  lightbox.innerHTML = `
    <section class="technical-lightbox-dialog" role="dialog" aria-modal="true" aria-label="Visor de fotografías técnicas">
      <button class="technical-lightbox-close" type="button" aria-label="Cerrar fotografía ampliada">
        <span aria-hidden="true">×</span>
      </button>
      <div class="technical-lightbox-stage">
        <button class="technical-lightbox-nav technical-lightbox-prev" type="button" aria-label="Fotografía anterior">
          <span aria-hidden="true">‹</span>
        </button>
        <img class="technical-lightbox-image" alt="">
        <button class="technical-lightbox-nav technical-lightbox-next" type="button" aria-label="Fotografía siguiente">
          <span aria-hidden="true">›</span>
        </button>
      </div>
      <div class="technical-lightbox-meta">
        <span class="technical-lightbox-counter" aria-live="polite"></span>
        <p class="technical-lightbox-caption"></p>
        <p class="technical-lightbox-help">Usa las flechas para cambiar de fotografía y Esc para cerrar. En celular puedes ampliar con el gesto de pellizcar.</p>
      </div>
    </section>
  `;
  document.body.appendChild(lightbox);

  const lightboxImage = lightbox.querySelector(".technical-lightbox-image");
  const lightboxCaption = lightbox.querySelector(".technical-lightbox-caption");
  const lightboxCounter = lightbox.querySelector(".technical-lightbox-counter");
  const closeButton = lightbox.querySelector(".technical-lightbox-close");
  const previousButton = lightbox.querySelector(".technical-lightbox-prev");
  const nextButton = lightbox.querySelector(".technical-lightbox-next");
  const navigationButtons = [previousButton, nextButton];

  const updateTechnicalPhoto = (nextIndex) => {
    activeIndex = (nextIndex + technicalPhotoItems.length) % technicalPhotoItems.length;
    const item = technicalPhotoItems[activeIndex];

    lightboxImage.classList.add("is-loading");
    lightboxImage.alt = item.alt;
    lightboxCaption.textContent = item.caption;
    lightboxCounter.textContent = `${activeIndex + 1} de ${technicalPhotoItems.length}`;
    navigationButtons.forEach((button) => {
      button.hidden = technicalPhotoItems.length < 2;
    });

    if (lightboxImage.src !== item.source) {
      lightboxImage.src = item.source;
    } else if (lightboxImage.complete) {
      lightboxImage.classList.remove("is-loading");
    }
  };

  lightboxImage.addEventListener("load", () => {
    lightboxImage.classList.remove("is-loading");
  });

  lightboxImage.addEventListener("error", () => {
    lightboxImage.classList.remove("is-loading");
    lightboxCaption.textContent = "No fue posible cargar la fotografía ampliada.";
  });

  const openTechnicalLightbox = (index, trigger) => {
    if (closeTimer) window.clearTimeout(closeTimer);
    previouslyFocusedElement = trigger || document.activeElement;
    lightbox.hidden = false;
    lightbox.setAttribute("aria-hidden", "false");
    document.body.classList.add("technical-lightbox-open");
    updateTechnicalPhoto(index);
    requestAnimationFrame(() => lightbox.classList.add("is-open"));
    closeButton.focus();

    const item = technicalPhotoItems[index];
    sendAnalyticsEvent("technical_photo_open", {
      event_category: "engagement",
      photo_url: item.source,
      photo_number: index + 1,
      page_path: window.location.pathname,
      page_title: document.title
    });
  };

  const closeTechnicalLightbox = () => {
    lightbox.classList.remove("is-open");
    lightbox.setAttribute("aria-hidden", "true");
    document.body.classList.remove("technical-lightbox-open");

    closeTimer = window.setTimeout(() => {
      if (!lightbox.classList.contains("is-open")) lightbox.hidden = true;
    }, 220);

    if (previouslyFocusedElement instanceof HTMLElement) {
      previouslyFocusedElement.focus();
    }
  };

  technicalPhotoCandidates.forEach((image) => {
    const source = sourceForImage.get(image);
    const itemIndex = indexBySource.get(source) ?? 0;
    const accessibleCaption = captionForImage(image);

    image.classList.add("technical-photo-zoom");
    image.setAttribute("role", "button");
    image.setAttribute("tabindex", "0");
    image.setAttribute("aria-label", `Ampliar fotografía: ${accessibleCaption}`);
    image.closest("figure")?.classList.add("has-technical-lightbox");

    image.addEventListener("click", () => openTechnicalLightbox(itemIndex, image));
    image.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        openTechnicalLightbox(itemIndex, image);
      }
    });
  });

  previousButton.addEventListener("click", () => updateTechnicalPhoto(activeIndex - 1));
  nextButton.addEventListener("click", () => updateTechnicalPhoto(activeIndex + 1));
  closeButton.addEventListener("click", closeTechnicalLightbox);

  lightbox.addEventListener("click", (event) => {
    if (event.target === lightbox) closeTechnicalLightbox();
  });

  document.addEventListener("keydown", (event) => {
    if (!lightbox.classList.contains("is-open")) return;

    if (event.key === "Escape") {
      event.preventDefault();
      closeTechnicalLightbox();
      return;
    }

    if (event.key === "ArrowLeft" && technicalPhotoItems.length > 1) {
      event.preventDefault();
      updateTechnicalPhoto(activeIndex - 1);
      return;
    }

    if (event.key === "ArrowRight" && technicalPhotoItems.length > 1) {
      event.preventDefault();
      updateTechnicalPhoto(activeIndex + 1);
      return;
    }

    if (event.key === "Tab") {
      const focusable = Array.from(
        lightbox.querySelectorAll("button:not([hidden]):not([disabled]), [href], [tabindex]:not([tabindex='-1'])")
      );
      if (!focusable.length) return;

      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }
  });
}
