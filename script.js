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

/* Conversion event tracking. Works when Google Analytics gtag is installed. */
document.addEventListener("click", (event) => {
  const trackedLink = event.target.closest("[data-track]");
  if (!trackedLink) return;

  const eventName = trackedLink.dataset.track;
  const destination = trackedLink.getAttribute("href") || "";

  if (typeof window.gtag === "function") {
    window.gtag("event", eventName, {
      event_category: "conversion",
      link_url: destination,
      page_path: window.location.pathname
    });
  }
});
