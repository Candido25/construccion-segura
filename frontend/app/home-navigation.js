(() => {
  const PROFILE_KEY = "mi-casa-segura-work-profile-v1";
  const routeButtons = document.querySelectorAll("[data-app-route]");
  const faqSection = document.getElementById("dudas");
  const faqInput = document.getElementById("faqSearch");
  const stageSection = document.querySelector(".stage-section");
  const problemButton = document.querySelector('[data-module="problemas"]');
  const welcomeCard = document.querySelector(".welcome-card");
  const helpCard = document.querySelector(".help-card");
  const bottomNav = document.querySelector(".bottom-nav");

  if (welcomeCard) welcomeCard.id = "inicio";
  if (stageSection && !stageSection.id) stageSection.id = "guia-etapas";
  if (helpCard) helpCard.id = "ayuda";

  const scrollToElement = (element) => {
    if (!element) return;
    element.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  const hasWorkProfile = () => {
    try {
      return Boolean(window.localStorage.getItem(PROFILE_KEY));
    } catch (error) {
      return false;
    }
  };

  if (bottomNav) {
    bottomNav.innerHTML = `
      <a class="active" href="#inicio" data-nav-target="inicio"><span>⌂</span>Inicio</a>
      <a href="#guia-etapas" data-nav-target="guia-etapas"><span>☷</span>Guía</a>
      <a href="#dudas" data-nav-target="dudas"><span>⌕</span>Consultar</a>
      <button type="button" data-open-work-profile><span>▣</span>Mi obra</button>
      <a href="#ayuda" data-nav-target="ayuda"><span>?</span>Ayuda</a>
    `;
  }

  routeButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const route = button.dataset.appRoute;

      if (route === "construir") {
        if (!hasWorkProfile()) {
          document.dispatchEvent(new CustomEvent("mi-casa-segura:open-work-profile", {
            detail: { continueToGuide: true }
          }));
        } else {
          scrollToElement(stageSection);
        }
      }

      if (route === "duda") {
        scrollToElement(faqSection);
        window.setTimeout(() => faqInput?.focus(), 450);
      }

      if (route === "problema") {
        if (problemButton) {
          problemButton.click();
        } else {
          scrollToElement(stageSection);
        }
      }
    });
  });

  bottomNav?.querySelectorAll("[data-nav-target]").forEach((link) => {
    link.addEventListener("click", (event) => {
      const target = document.getElementById(link.dataset.navTarget);
      if (!target) return;
      event.preventDefault();
      bottomNav.querySelectorAll("a, button").forEach((item) => item.classList.remove("active"));
      link.classList.add("active");
      scrollToElement(target);
      if (link.dataset.navTarget === "dudas") {
        window.setTimeout(() => faqInput?.focus(), 450);
      }
    });
  });

  document.addEventListener("mi-casa-segura:work-profile-saved", (event) => {
    if (event.detail?.continueToGuide) {
      window.setTimeout(() => scrollToElement(stageSection), 200);
    }
  });
})();
