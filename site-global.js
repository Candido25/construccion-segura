const applyAppOfficialBranding = () => {
  if (!window.location.pathname.startsWith("/app")) return;

  if (!document.querySelector('link[data-app-brand="official"]')) {
    const brandStyles = document.createElement("link");
    brandStyles.rel = "stylesheet";
    brandStyles.href = "/app/brand.css?v=20260714-1";
    brandStyles.dataset.appBrand = "official";
    document.head.appendChild(brandStyles);
  }

  const brandImage = document.querySelector(".app-brand img");
  if (brandImage) {
    brandImage.src = "/assets/brand/logo-marca-construccion-segura-transparente.png";
    brandImage.alt = "Construcción Segura";
    brandImage.removeAttribute("width");
    brandImage.removeAttribute("height");
  }

  const themeMeta = document.querySelector('meta[name="theme-color"]');
  if (themeMeta) themeMeta.setAttribute("content", "#071e38");
};

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

const applyPanderetaObservation = () => {
  const pathname = window.location.pathname;
  const articleUrl = "/errores/ladrillo-pandereta-muro-portante-asentado-de-canto.html";
  const imageUrl = "/assets/site-photos/casos/multifamiliar-seis-niveles/ladrillo-pandereta-de-canto.svg";

  if (pathname.endsWith("/errores-frecuentes.html")) {
    const topicLibrary = document.querySelector(".topic-library-grid");
    if (topicLibrary && !topicLibrary.querySelector(`a[href$="${articleUrl.split("/").pop()}"]`)) {
      topicLibrary.insertAdjacentHTML(
        "afterbegin",
        `<a class="topic-library-card" href="${articleUrl}"><strong>Ladrillo pandereta como muro portante o de canto</strong><span>Una unidad tubular no debe recibir carga ni perder espesor resistente.</span></a>`
      );
    }

    const errorGallery = document.querySelector("#galeria-errores");
    if (errorGallery && !document.querySelector("#error-pandereta-de-canto")) {
      const firstArticle = errorGallery.querySelector(".error-article");
      const summary = document.createElement("div");
      summary.id = "error-pandereta-de-canto";
      summary.className = "error-article reveal is-visible";
      summary.innerHTML = `
        <div class="error-media watermark-frame">
          <img src="${imageUrl}" alt="Ladrillo pandereta colocado de canto y con juntas irregulares" loading="lazy">
        </div>
        <div>
          <span>Albañilería y sismorresistencia</span>
          <h3>Usar ladrillo pandereta como muro portante o colocarlo de canto.</h3>
          <p>La pandereta es una unidad tubular destinada principalmente a tabiquería. No debe recibir cargas de una losa, viga o pisos superiores. Al colocarla de canto se reduce el espesor efectivo del paño y disminuye su rigidez frente a acciones perpendiculares.</p>
          <ul>
            <li>Qué problema genera: mayor esbeltez, fisuración, desprendimiento o volcamiento y una respuesta frágil durante un sismo.</li>
            <li>Qué debería pasar: confirmar que sea un tabique no portante, respetar la orientación normal de la unidad y ejecutar juntas, arriostres y conexiones conforme al proyecto.</li>
            <li>Qué demuestra: ganar unos centímetros de espacio no justifica reducir la seguridad del muro.</li>
          </ul>
          <p>Referencia útil: la <a class="inline-link" href="https://cdn.www.gob.pe/uploads/document/file/2366661/56%20E.070%20ALBA%C3%91ILERIA.pdf?v=1677250657" target="_blank" rel="noreferrer">Norma E.070 Albañilería</a> diferencia las unidades tubulares y limita su empleo estructural.</p>
          <p><a class="inline-link" href="${articleUrl}">Ver observación técnica completa</a></p>
        </div>`;
      if (firstArticle) {
        firstArticle.before(summary);
      } else {
        errorGallery.appendChild(summary);
      }
    }
  }

  if (pathname.endsWith("/casos/seguimiento-vivienda-multifamiliar-seis-niveles.html")) {
    document.title = document.title.replace("Cuatro observaciones", "Cinco observaciones");
    document.querySelector('meta[property="og:title"]')?.setAttribute("content", "Cinco observaciones técnicas en una vivienda multifamiliar de seis niveles");

    const heading = document.querySelector(".article-copy h1");
    if (heading) heading.textContent = "Vivienda multifamiliar de seis niveles: cinco observaciones técnicas.";

    const lead = document.querySelector(".article-copy .article-lead");
    if (lead) lead.textContent = "Las fotografías muestran una unidad tubular colocada de canto, un vano de albañilería, una columna de concreto armado, una escalera y una viga. El análisis distingue las deficiencias visibles de los aspectos que todavía deben medirse o compararse con los planos.";

    const status = document.querySelector(".project-status strong");
    if (status) status.textContent = "5 fotografías analizadas · Lima";

    const reviewedFact = Array.from(document.querySelectorAll(".project-fact")).find((item) =>
      item.querySelector("span")?.textContent.trim() === "Elementos revisados"
    );
    reviewedFact?.querySelector("strong")?.replaceChildren("Unidad tubular, vano, columna, escalera y viga");

    const caseIndex = document.querySelector(".case-index");
    if (caseIndex && !caseIndex.querySelector('a[href="#pandereta-de-canto"]')) {
      caseIndex.insertAdjacentHTML(
        "afterbegin",
        '<a class="case-index-card case-index-alert" href="#pandereta-de-canto"><span>Deficiencia visible</span><strong>Pandereta de canto</strong><small>La unidad tubular no debe recibir carga ni formar un paño resistente improvisado.</small></a>'
      );
    }

    const caseList = document.querySelector(".case-list");
    if (caseList && !document.querySelector("#pandereta-de-canto")) {
      caseList.insertAdjacentHTML(
        "beforeend",
        `<article class="case-item reveal is-visible" id="pandereta-de-canto">
          <figure class="case-photo watermark-frame">
            <img src="${imageUrl}" alt="Ladrillo pandereta colocado de canto y con juntas irregulares junto a elementos de concreto">
            <figcaption>Observación 5. Unidad tubular colocada de canto, con juntas irregulares, registrada el 21 de julio de 2026.</figcaption>
          </figure>
          <div class="case-copy">
            <span class="case-number">05 · Albañilería y comportamiento sísmico</span>
            <div class="case-meta"><span>Condición: deficiencia visible</span><span>Elemento: muro con unidad tubular</span></div>
            <h2>El ladrillo pandereta no debe trabajar como muro portante ni asentarse de canto.</h2>
            <p class="case-summary"><strong>Descripción:</strong> se observa una unidad tubular tipo pandereta colocada de canto. Las juntas presentan espesores variables y el paño está en contacto con elementos de concreto.</p>
            <h3>Por qué requiere corrección</h3>
            <p>La pandereta se emplea principalmente en tabiquería y no debe recibir cargas de losas, vigas o niveles superiores. En una vivienda multifamiliar de seis niveles en Lima no corresponde considerarla una unidad para muros portantes.</p>
            <p>Al colocarla de canto disminuye el espesor efectivo del paño. Como el momento de inercia geométrico depende fuertemente de esa dimensión, la rigidez frente a flexión fuera del plano se reduce de manera marcada. Esto aumenta la esbeltez y la vulnerabilidad ante aceleraciones sísmicas, empujes perpendiculares, fisuración, desprendimiento o volcamiento.</p>
            <p class="technical-note">Antes de tarrajear debe verificarse en planos que sea un tabique no portante, impedir que reciba carga estructural y revisar orientación, trabazón, plomo, arriostramiento, conexión con la estructura y las juntas.</p>
            <p><a class="inline-link" href="${articleUrl}">Ver guía completa sobre pandereta, inercia y sismorresistencia</a></p>
          </div>
        </article>`
      );
    }

    const futureGrid = document.querySelector(".future-grid");
    if (futureGrid && !futureGrid.querySelector('[data-pandereta-verification]')) {
      futureGrid.insertAdjacentHTML(
        "beforeend",
        '<article class="future-card" data-pandereta-verification><span>05</span><h3>Función del muro de pandereta</h3><p>Confirmar que sea un tabique no portante, que no reciba carga y que su orientación, juntas y arriostramiento correspondan al proyecto.</p></article>'
      );
    }

    const footerStatus = document.querySelector(".article-footer span");
    if (footerStatus?.textContent.includes("Revisión técnica publicada")) {
      footerStatus.textContent = "Revisión técnica actualizada: 21 de julio de 2026 · Proyecto ubicado en Lima";
    }
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

applyAppOfficialBranding();
applyCasesNavigation();
applyPanderetaObservation();
registerConstruccionSeguraPWA();
document.addEventListener("DOMContentLoaded", () => {
  applyAppOfficialBranding();
  applyCasesNavigation();
  applyPanderetaObservation();
}, { once: true });
window.setTimeout(applyAppOfficialBranding, 0);
window.setTimeout(applyCasesNavigation, 0);
window.setTimeout(applyPanderetaObservation, 0);
window.setTimeout(applyAppOfficialBranding, 120);
window.setTimeout(applyCasesNavigation, 120);
window.setTimeout(applyPanderetaObservation, 120);
