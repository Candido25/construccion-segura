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
  const imageUrl = "/assets/site-photos/casos/multifamiliar-seis-niveles/ladrillo-pandereta-de-canto.webp";

  if (pathname.endsWith("/errores-frecuentes.html")) {
    const topicLibrary = document.querySelector(".topic-library-grid");
    if (topicLibrary && !topicLibrary.querySelector(`a[href$="${articleUrl.split("/").pop()}"]`)) {
      topicLibrary.insertAdjacentHTML(
        "afterbegin",
        `<a class="topic-library-card" href="${articleUrl}"><strong>Ladrillo pandereta usado para soportar peso</strong><span>Por qué no debe emplearse como muro portante ni colocarse de canto.</span></a>`
      );
    }

    const errorGallery = document.querySelector("#galeria-errores");
    if (errorGallery && !document.querySelector("#error-pandereta-de-canto")) {
      const firstArticle = errorGallery.querySelector(".error-article");
      const summary = document.createElement("div");
      summary.id = "error-pandereta-de-canto";
      summary.className = "error-article reveal is-visible";
      summary.innerHTML = `
        <div class="error-media">
          <img src="${imageUrl}" alt="Ladrillo pandereta colocado de canto y con juntas irregulares" width="640" height="360" loading="lazy" style="width:100%;height:auto;aspect-ratio:16/9;object-fit:cover">
        </div>
        <div>
          <span>Albañilería y seguridad sísmica</span>
          <h3>Por qué el ladrillo pandereta no debe soportar cargas ni colocarse de canto.</h3>
          <p>El ladrillo pandereta está pensado principalmente para dividir ambientes. No debe sostener losas, vigas ni pisos superiores. Cuando se coloca de canto, el muro queda más delgado y ofrece menos resistencia frente a movimientos y empujes perpendiculares, como los que pueden presentarse durante un sismo.</p>
          <ul>
            <li><strong>Qué puede ocurrir:</strong> el muro puede agrietarse, desprenderse o volcarse con mayor facilidad durante un sismo.</li>
            <li><strong>Cómo reconocer una ejecución segura:</strong> el muro debe funcionar solamente como división, conservar el espesor previsto y estar correctamente unido o arriostrado.</li>
            <li><strong>Recomendación principal:</strong> no utilizar este ladrillo para cargar peso ni colocarlo de canto para ganar espacio.</li>
          </ul>
          <p>La <a class="inline-link" href="https://cdn.www.gob.pe/uploads/document/file/2366661/56%20E.070%20ALBA%C3%91ILERIA.pdf?v=1677250657" target="_blank" rel="noreferrer">Norma E.070 de Albañilería</a> diferencia estas unidades y limita su uso como elemento estructural.</p>
          <p><a class="inline-link" href="${articleUrl}">Conocer más sobre este error de construcción</a></p>
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
        '<a class="case-index-card case-index-alert" href="#pandereta-de-canto"><span>Deficiencia visible</span><strong>Pandereta de canto</strong><small>Un ladrillo para dividir ambientes no debe emplearse para sostener la edificación.</small></a>'
      );
    }

    const caseList = document.querySelector(".case-list");
    if (caseList && !document.querySelector("#pandereta-de-canto")) {
      caseList.insertAdjacentHTML(
        "beforeend",
        `<article class="case-item reveal is-visible" id="pandereta-de-canto">
          <figure class="case-photo">
            <img src="${imageUrl}" alt="Ladrillo pandereta colocado de canto y con juntas irregulares junto a elementos de concreto" width="640" height="360" style="width:100%;height:auto;aspect-ratio:16/9;object-fit:cover">
            <figcaption>Observación 5. Ladrillo pandereta colocado de canto, con juntas irregulares, registrado el 21 de julio de 2026.</figcaption>
          </figure>
          <div class="case-copy">
            <span class="case-number">05 · Albañilería y comportamiento sísmico</span>
            <div class="case-meta"><span>Condición: deficiencia visible</span><span>Elemento: muro con unidad tubular</span></div>
            <h2>Un ladrillo para dividir ambientes no debe utilizarse para sostener la edificación.</h2>
            <p class="case-summary"><strong>Descripción:</strong> se observa un ladrillo pandereta colocado de canto. Las juntas presentan espesores variables y el paño está en contacto con elementos de concreto.</p>
            <h3>Por qué representa un riesgo</h3>
            <p>La pandereta se utiliza principalmente para separar ambientes. No debe recibir el peso de losas, vigas o pisos superiores. En una edificación de varios niveles, confundir un tabique con un muro portante puede generar una condición insegura.</p>
            <p>Al colocarla de canto, el muro queda más delgado. Esa reducción disminuye notablemente su rigidez frente a movimientos perpendiculares, aumenta su esbeltez y facilita la aparición de grietas, desprendimientos o volcamiento durante un sismo.</p>
            <p class="technical-note">Antes de cubrir el muro conviene confirmar que sea únicamente una división, que no esté soportando peso y que su orientación, juntas y unión con la estructura sean las previstas en el proyecto.</p>
            <p><a class="inline-link" href="${articleUrl}">Leer la explicación completa en lenguaje sencillo</a></p>
          </div>
        </article>`
      );
    }

    const futureGrid = document.querySelector(".future-grid");
    if (futureGrid && !futureGrid.querySelector('[data-pandereta-verification]')) {
      futureGrid.insertAdjacentHTML(
        "beforeend",
        '<article class="future-card" data-pandereta-verification><span>05</span><h3>Comprobar para qué sirve el muro</h3><p>Verificar que solo divida ambientes, que no sostenga peso y que esté colocado y unido de acuerdo con los planos.</p></article>'
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
