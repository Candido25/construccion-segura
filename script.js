/* ── MENU TOGGLE ─────────────────────────────────────────────────── */
const menuToggle  = document.querySelector(".menu-toggle");
const siteNav     = document.querySelector(".site-nav");
const navLinks    = document.querySelectorAll(".site-nav a");

if (menuToggle && siteNav) {
  menuToggle.addEventListener("click", () => {
    const isOpen = siteNav.classList.toggle("is-open");
    menuToggle.setAttribute("aria-expanded", String(isOpen));
  });

  navLinks.forEach((link) => {
    link.addEventListener("click", () => {
      siteNav.classList.remove("is-open");
      menuToggle.setAttribute("aria-expanded", "false");
    });
  });

  // Cerrar con clic fuera
  document.addEventListener("click", (e) => {
    if (!siteNav.contains(e.target) && !menuToggle.contains(e.target)) {
      siteNav.classList.remove("is-open");
      menuToggle.setAttribute("aria-expanded", "false");
    }
  });
}

/* ── HEADER SCROLL SHADOW ────────────────────────────────────────── */
const header = document.querySelector(".site-header");
if (header) {
  const onScroll = () => {
    header.classList.toggle("scrolled", window.scrollY > 40);
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
}

/* ── REVEAL ON SCROLL ────────────────────────────────────────────── */
const revealTargets = document.querySelectorAll(".section, .hero-content, .reveal");

if ("IntersectionObserver" in window) {
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          // Staggered delay for grid children
          const children = entry.target.querySelectorAll(
            ".tip-card, .mistake-card, .service-item, .case-card, .testimonial-card, .faq-card, .timeline article, .story-values article"
          );
          if (children.length > 1) {
            children.forEach((child, i) => {
              child.style.transitionDelay = `${i * 75}ms`;
              child.classList.add("reveal");
              requestAnimationFrame(() => child.classList.add("is-visible"));
            });
          }

          entry.target.classList.add("is-visible");
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -5% 0px" }
  );

  revealTargets.forEach((el) => {
    el.classList.add("reveal");
    revealObserver.observe(el);
  });
} else {
  revealTargets.forEach((el) => el.classList.add("is-visible"));
}

/* ── FLOATING CTA VISIBILITY ─────────────────────────────────────── */
const floatingCta = document.querySelector(".floating-cta");
if (floatingCta) {
  let shown = false;
  window.addEventListener("scroll", () => {
    const shouldShow = window.scrollY > window.innerHeight * 0.5;
    if (shouldShow !== shown) {
      shown = shouldShow;
      floatingCta.style.opacity    = shown ? "1" : "0";
      floatingCta.style.transform  = shown ? "translateY(0)" : "translateY(8px)";
      floatingCta.style.pointerEvents = shown ? "auto" : "none";
    }
  }, { passive: true });

  // Iniciar oculto
  floatingCta.style.opacity   = "0";
  floatingCta.style.transform = "translateY(8px)";
  floatingCta.style.transition = "opacity 0.4s ease, transform 0.4s ease";
  floatingCta.style.pointerEvents = "none";
}

/* ── LOGO LIGHTBOX ───────────────────────────────────────────────── */
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
