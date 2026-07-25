const applyLosaNervadaObservation = () => {
  const pathname = window.location.pathname;
  const guideUrl = "/errores/casetones-invaden-seccion-viga-modulacion-losa.html";
  const modulationImage = "/assets/site-photos/casos/multifamiliar-seis-niveles/modulacion-losa-vigueta-20260721.webp";
  const intrusionImage = "/assets/site-photos/casos/multifamiliar-seis-niveles/casetones-invaden-viga-20260721.webp";

  if (pathname.endsWith("/errores-frecuentes.html")) {
    const topicLibrary = document.querySelector(".topic-library-grid");
    if (topicLibrary && !topicLibrary.querySelector(`a[href$="${guideUrl.split("/").pop()}"]`)) {
      topicLibrary.insertAdjacentHTML(
        "afterbegin",
        `<a class="topic-library-card" href="${guideUrl}"><strong>Casetones dentro de una viga</strong><span>Por qué el relleno no debe reducir la sección ni alterar la modulación de la losa.</span></a>`
      );
    }

    const errorGallery = document.querySelector("#galeria-errores");
    if (errorGallery && !document.querySelector("#error-casetones-invaden-viga")) {
      const firstArticle = errorGallery.querySelector(".error-article");
      const summary = document.createElement("div");
      summary.id = "error-casetones-invaden-viga";
      summary.className = "error-article reveal is-visible";
      summary.innerHTML = `
        <div class="error-media">
          <img src="${intrusionImage}" alt="Casetones de tecnopor que ingresan repetidamente en el espacio de una armadura de viga" width="400" height="225" loading="lazy" style="width:100%;height:auto;aspect-ratio:16/9;object-fit:cover">
        </div>
        <div>
          <span>Losa nervada y vigas</span>
          <h3>Los casetones no deben ocupar el espacio que corresponde al concreto de una viga.</h3>
          <p>El tecnopor y las piezas de arcilla sirven como relleno o para formar vacíos. No deben introducirse dentro de la armadura de una viga ni utilizarse para que una modulación improvisada logre encajar.</p>
          <ul>
            <li><strong>Qué puede ocurrir:</strong> reducción de la sección de concreto, vacíos alrededor del acero y una losa distinta de la calculada.</li>
            <li><strong>Cómo reconocerlo:</strong> casetones dentro del ancho de la viga, rellenos de arcilla improvisados y viguetas que no mantienen la secuencia de los planos.</li>
            <li><strong>Qué debe hacerse:</strong> corregir la geometría y la modulación antes de colocar el concreto.</li>
          </ul>
          <p><a class="inline-link" href="${guideUrl}">Conocer por qué este error puede afectar la estructura</a></p>
        </div>`;
      if (firstArticle) firstArticle.before(summary); else errorGallery.appendChild(summary);
    }
  }

  if (pathname.endsWith("/casos/seguimiento-vivienda-multifamiliar-seis-niveles.html")) {
    document.title = document.title.replace(/(?:Cuatro|Cinco|Seis|Siete) observaciones/i, "Siete observaciones");
    document.querySelector('meta[property="og:title"]')?.setAttribute("content", "Siete observaciones técnicas en una vivienda multifamiliar de seis niveles");

    const heading = document.querySelector(".article-copy h1");
    if (heading) heading.textContent = "Vivienda multifamiliar de seis niveles: siete observaciones técnicas.";

    const lead = document.querySelector(".article-copy .article-lead");
    if (lead) lead.textContent = "Ocho fotografías permiten reconocer errores de albañilería, recubrimiento, modulación de la losa y ejecución de elementos estructurales. El análisis distingue lo visible de aquello que todavía debe medirse o compararse con los planos.";

    const status = document.querySelector(".project-status strong");
    if (status) status.textContent = "7 observaciones · 8 fotografías analizadas · Lima";

    const reviewedFact = Array.from(document.querySelectorAll(".project-fact")).find((item) =>
      item.querySelector("span")?.textContent.trim() === "Elementos revisados"
    );
    reviewedFact?.querySelector("strong")?.replaceChildren("Albañilería, losa nervada, recubrimiento, vano, columna, escalera y viga");

    const caseIndex = document.querySelector(".case-index");
    if (caseIndex && !caseIndex.querySelector('a[href="#casetones-invaden-viga"]')) {
      const card = document.createElement("a");
      card.className = "case-index-card case-index-alert";
      card.href = "#casetones-invaden-viga";
      card.innerHTML = '<span>Deficiencia visible y repetida</span><strong>Casetones dentro de la viga</strong><small>El relleno invade la sección y altera la modulación prevista de la losa.</small>';
      const recubrimientoCard = caseIndex.querySelector('a[href="#recubrimiento-viga-caseton"]');
      if (recubrimientoCard) recubrimientoCard.after(card); else caseIndex.prepend(card);
    }

    const caseList = document.querySelector(".case-list");
    if (caseList && !document.querySelector("#casetones-invaden-viga")) {
      const article = document.createElement("article");
      article.className = "case-item reveal is-visible";
      article.id = "casetones-invaden-viga";
      article.innerHTML = `
        <div style="display:grid;gap:1rem">
          <figure class="case-photo">
            <img src="${modulationImage}" alt="Piezas de arcilla y casetones que alteran la secuencia de viguetas junto a una viga" width="400" height="225" loading="lazy" style="width:100%;height:auto;aspect-ratio:16/9;object-fit:cover">
            <figcaption>Vista 1. Piezas de arcilla y rellenos colocados en el borde modifican la secuencia regular de la losa.</figcaption>
          </figure>
          <figure class="case-photo">
            <img src="${intrusionImage}" alt="Casetones de tecnopor que invaden repetidamente la sección delimitada por la armadura de una viga" width="400" height="225" loading="lazy" style="width:100%;height:auto;aspect-ratio:16/9;object-fit:cover">
            <figcaption>Vista 2. La invasión se repite a lo largo del elemento, por lo que corresponde a un patrón sistemático de ejecución y no a un desplazamiento aislado.</figcaption>
          </figure>
        </div>
        <div class="case-copy">
          <span class="case-number">07 · Losa nervada y vigas</span>
          <div class="case-meta"><span>Condición: deficiencia visible y repetida</span><span>Elemento: encuentro entre viga, viguetas y casetones</span></div>
          <h2>Los casetones no deben invadir la sección de la viga ni obligar a cambiar la modulación de la losa.</h2>
          <p class="case-summary"><strong>Qué se observa:</strong> en una vista se han colocado piezas de arcilla y rellenos que alteran la secuencia prevista en el borde de la losa. En la segunda, varios casetones ingresan repetidamente dentro del espacio delimitado por la armadura de la viga.</p>
          <h3>Por qué representa una mala práctica</h3>
          <p>El casetón solo forma un vacío y no reemplaza al concreto resistente. Si invade la viga, ocupa parte del ancho y del volumen que deben vaciarse, dificulta que el concreto rodee el acero y puede generar vacíos o cangrejeras.</p>
          <p>La ubicación de la primera vigueta y la separación entre nervios no se decide con una regla universal de 15 o 30 centímetros. Debe coincidir con la modulación, las dimensiones y los refuerzos indicados en los planos estructurales. Agregar ladrillos para completar espacios no demuestra que la geometría resultante sea correcta.</p>
          <p>La repetición visible permite calificarla como un patrón sistemático de ejecución. La fotografía no permite atribuir una intención personal, pero sí descarta que se trate únicamente de un casetón movido accidentalmente.</p>
          <p class="technical-note">Antes del vaciado deben retirarse o recortarse todos los rellenos que invaden la viga, recuperar su sección completa, verificar la posición de la primera vigueta y revisar toda la modulación con los planos. Después debe comprobarse que exista espacio para colocar y vibrar el concreto.</p>
          <p><a class="inline-link" href="${guideUrl}">Leer la explicación completa para propietarios</a></p>
        </div>`;
      const recubrimientoArticle = document.querySelector("#recubrimiento-viga-caseton");
      if (recubrimientoArticle) recubrimientoArticle.after(article); else caseList.appendChild(article);
    }

    const futureGrid = document.querySelector(".future-grid");
    if (futureGrid && !futureGrid.querySelector("[data-losa-modulation-verification]")) {
      futureGrid.insertAdjacentHTML("beforeend", '<article class="future-card" data-losa-modulation-verification><span>07</span><h3>Verificar la modulación de la losa</h3><p>Comparar la posición de la primera vigueta, el ancho de la viga, los nervios y los rellenos con los planos estructurales antes del vaciado.</p></article>');
    }

    const footerStatus = document.querySelector(".article-footer span");
    if (footerStatus?.textContent.includes("Revisión técnica")) {
      footerStatus.textContent = "Revisión técnica actualizada: 24 de julio de 2026 · Proyecto ubicado en Lima";
    }
  }
};

applyLosaNervadaObservation();
document.addEventListener("DOMContentLoaded", applyLosaNervadaObservation, { once: true });
window.setTimeout(applyLosaNervadaObservation, 0);
window.setTimeout(applyLosaNervadaObservation, 180);
