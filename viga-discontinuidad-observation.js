const applyVigaDiscontinuidadObservation = () => {
  const pathname = window.location.pathname;
  const guideUrl = "/errores/reduccion-discontinuidad-viga-junto-ducto.html";
  const imageUrl = "/assets/site-photos/casos/multifamiliar-seis-niveles/reduccion-viga-ducto-20260721.webp";

  if (pathname.endsWith("/errores-frecuentes.html")) {
    const topicLibrary = document.querySelector(".topic-library-grid");
    if (topicLibrary && !topicLibrary.querySelector(`a[href$="${guideUrl.split("/").pop()}"]`)) {
      topicLibrary.insertAdjacentHTML(
        "afterbegin",
        `<a class="topic-library-card" href="${guideUrl}"><strong>Viga reducida junto a un ducto</strong><span>Por qué una viga no debe estrecharse o interrumpirse sin un detalle estructural calculado.</span></a>`
      );
    }

    const errorGallery = document.querySelector("#galeria-errores");
    if (errorGallery && !document.querySelector("#error-reduccion-viga-ducto")) {
      const firstArticle = errorGallery.querySelector(".error-article");
      const summary = document.createElement("div");
      summary.id = "error-reduccion-viga-ducto";
      summary.className = "error-article reveal is-visible";
      summary.innerHTML = `
        <div class="error-media">
          <img src="${imageUrl}" alt="Vista superior de una losa donde una viga aparenta reducir abruptamente su ancho junto a un ducto" width="400" height="225" loading="lazy" style="width:100%;height:auto;aspect-ratio:16/9;object-fit:cover">
        </div>
        <div>
          <span>Vigas, ductos y continuidad estructural</span>
          <h3>Una viga no debe reducirse abruptamente ni terminar junto a un ducto sin que el cambio esté calculado.</h3>
          <p>En la fotografía, una franja que aparenta corresponder a una viga ancha llega al ducto y continúa con un ancho mucho menor, próximo al espesor de una pieza de relleno.</p>
          <ul>
            <li><strong>Qué puede ocurrir:</strong> pérdida de sección y rigidez, concentración de esfuerzos y menor espacio para colocar acero y concreto.</li>
            <li><strong>Cómo reconocerlo:</strong> cambio brusco de ancho, barras que no continúan como indica el plano o un ducto que interrumpe el recorrido de la viga.</li>
            <li><strong>Qué debe hacerse:</strong> detener el vaciado, medir y comparar el encuentro con los planos estructurales.</li>
          </ul>
          <p><a class="inline-link" href="${guideUrl}">Comprender por qué este cambio puede ser crítico</a></p>
        </div>`;
      if (firstArticle) firstArticle.before(summary); else errorGallery.appendChild(summary);
    }
  }

  if (pathname.endsWith("/casos/seguimiento-vivienda-multifamiliar-seis-niveles.html")) {
    document.title = document.title.replace(/(?:Cuatro|Cinco|Seis|Siete|Ocho) observaciones/i, "Ocho observaciones");
    document.querySelector('meta[property="og:title"]')?.setAttribute("content", "Ocho observaciones técnicas en una vivienda multifamiliar de seis niveles");

    const heading = document.querySelector(".article-copy h1");
    if (heading) heading.textContent = "Vivienda multifamiliar de seis niveles: ocho observaciones técnicas.";

    const lead = document.querySelector(".article-copy .article-lead");
    if (lead) lead.textContent = "Nueve fotografías permiten reconocer errores de albañilería, recubrimiento, modulación de la losa, continuidad de vigas y ejecución de elementos estructurales. El análisis distingue lo visible de aquello que todavía debe medirse o compararse con los planos.";

    const status = document.querySelector(".project-status strong");
    if (status) status.textContent = "8 observaciones · 9 fotografías analizadas · Lima";

    const reviewedFact = Array.from(document.querySelectorAll(".project-fact")).find((item) =>
      item.querySelector("span")?.textContent.trim() === "Elementos revisados"
    );
    reviewedFact?.querySelector("strong")?.replaceChildren("Albañilería, losa nervada, continuidad de vigas, recubrimiento, vano, columna y escalera");

    const caseIndex = document.querySelector(".case-index");
    if (caseIndex && !caseIndex.querySelector('a[href="#reduccion-viga-ducto"]')) {
      const card = document.createElement("a");
      card.className = "case-index-card case-index-alert";
      card.href = "#reduccion-viga-ducto";
      card.innerHTML = '<span>Condición crítica por verificar</span><strong>Viga reducida junto a ducto</strong><small>Un cambio abrupto de sección puede interrumpir la ruta prevista de las cargas.</small>';
      const losaCard = caseIndex.querySelector('a[href="#casetones-invaden-viga"]');
      if (losaCard) losaCard.after(card); else caseIndex.prepend(card);
    }

    const caseList = document.querySelector(".case-list");
    if (caseList && !document.querySelector("#reduccion-viga-ducto")) {
      const article = document.createElement("article");
      article.className = "case-item reveal is-visible";
      article.id = "reduccion-viga-ducto";
      article.innerHTML = `
        <figure class="case-photo">
          <img src="${imageUrl}" alt="Vista superior de una losa con aparente reducción abrupta del ancho de una viga al llegar a un ducto" width="400" height="225" loading="lazy" style="width:100%;height:auto;aspect-ratio:16/9;object-fit:cover">
          <figcaption>Observación 8. Encuentro entre una viga y un ducto registrado el 21 de julio de 2026. Las medidas deben confirmarse directamente y compararse con los planos.</figcaption>
        </figure>
        <div class="case-copy">
          <span class="case-number">08 · Vigas y continuidad estructural</span>
          <div class="case-meta"><span>Condición: crítica por verificar antes del vaciado</span><span>Elemento: viga junto a ducto o abertura</span></div>
          <h2>Una viga no debe perder bruscamente su ancho ni interrumpir su continuidad para dejar pasar un ducto.</h2>
          <p class="case-summary"><strong>Qué se observa:</strong> la franja de armado que aparenta corresponder a una viga longitudinal llega hasta el ducto y, después del encuentro, continúa con un ancho mucho menor. En obra se ha estimado un cambio aproximado de 25 cm a 13 cm, pero la fotografía no permite certificar esas dimensiones.</p>
          <h3>Por qué esta observación es seria</h3>
          <p>Las vigas conducen cargas hacia columnas y otros apoyos. Una reducción abrupta disminuye el área de concreto, la rigidez y el espacio disponible para el refuerzo. El borde del ducto también puede concentrar esfuerzos y exigir vigas de borde, refuerzos adicionales o una solución especial calculada.</p>
          <p>Una viga sí puede cambiar de geometría cuando el ingeniero estructural lo ha diseñado y detallado. Lo peligroso es que el cambio aparezca en obra para acomodar el ducto, el ladrillo o el casetón sin que figure en los planos.</p>
          <p><strong>Ejemplo orientativo:</strong> si el ancho realmente pasara de 25 cm a 13 cm y el peralte fuera igual, quedaría aproximadamente el 52 % del ancho original. Este cálculo no determina por sí solo la resistencia, pero muestra que no se trata de una variación menor.</p>
          <p class="technical-note">Antes del vaciado deben medirse el ancho, peralte y refuerzo en ambos lados del ducto; revisar la continuidad y anclaje de las barras; y exigir el detalle del ingeniero estructural. Si el cambio no está proyectado, no debe cubrirse con concreto hasta definir y ejecutar la corrección.</p>
          <p><a class="inline-link" href="${guideUrl}">Leer la explicación completa para propietarios</a></p>
        </div>`;
      const losaArticle = document.querySelector("#casetones-invaden-viga");
      if (losaArticle) losaArticle.after(article); else caseList.appendChild(article);
    }

    const futureGrid = document.querySelector(".future-grid");
    if (futureGrid && !futureGrid.querySelector("[data-viga-ducto-verification]")) {
      futureGrid.insertAdjacentHTML("beforeend", '<article class="future-card" data-viga-ducto-verification><span>08</span><h3>Verificar la continuidad de la viga</h3><p>Medir la sección a ambos lados del ducto y confirmar en los planos cómo se transmiten las cargas alrededor de la abertura.</p></article>');
    }

    const footerStatus = document.querySelector(".article-footer span");
    if (footerStatus?.textContent.includes("Revisión técnica")) {
      footerStatus.textContent = "Revisión técnica actualizada: 24 de julio de 2026 · Proyecto ubicado en Lima";
    }
  }
};

applyVigaDiscontinuidadObservation();
document.addEventListener("DOMContentLoaded", applyVigaDiscontinuidadObservation, { once: true });
window.setTimeout(applyVigaDiscontinuidadObservation, 0);
window.setTimeout(applyVigaDiscontinuidadObservation, 220);
