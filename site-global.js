const applyCasesNavigation = () => {
  const navigation = document.querySelector(".site-nav");

  if (navigation && !navigation.querySelector('a[href="/app/"]')) {
    const appLink = document.createElement("a");
    appLink.href = "/app/";
    appLink.textContent = "Guía para construir";
    appLink.dataset.track = "app_navigation";

    const libraryLink = Array.from(navigation.querySelectorAll("a")).find((link) =>
      (link.getAttribute("href") || "").includes("biblioteca-tecnica.html")
    );
    navigation.insertBefore(appLink, libraryLink || navigation.firstChild);
  }

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
  if (homeResourcesActions && !homeResourcesActions.querySelector('a[href="/app/"]')) {
    const appButton = document.createElement("a");
    appButton.className = "button button-primary";
    appButton.href = "/app/";
    appButton.dataset.track = "app_home_resources";
    appButton.textContent = "Abrir guía para construir";
    homeResourcesActions.prepend(appButton);
  }

  if (homeResourcesActions && !homeResourcesActions.querySelector('a[href$="casos-de-obra.html"]')) {
    const casesButton = document.createElement("a");
    casesButton.className = "button button-secondary";
    casesButton.href = "/casos-de-obra.html";
    casesButton.dataset.track = "cases_home_resources";
    casesButton.textContent = "Ver casos de obra";
    homeResourcesActions.appendChild(casesButton);
  }
};

const registerConstruccionSeguraPWA = () => {
  if (!("serviceWorker" in navigator) || window.location.protocol !== "https:") return;

  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/service-worker.js", { scope: "/" })
      .then((registration) => {
        registration.update().catch(() => {});
      })
      .catch((error) => {
        console.warn("No se pudo activar el modo aplicación de Construcción Segura.", error);
      });
  }, { once: true });
};

applyCasesNavigation();
registerConstruccionSeguraPWA();
document.addEventListener("DOMContentLoaded", applyCasesNavigation, { once: true });
window.setTimeout(applyCasesNavigation, 0);
window.setTimeout(applyCasesNavigation, 120);
