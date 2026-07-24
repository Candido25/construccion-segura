const applyRecubrimientoObservation = () => {
  if (!window.location.pathname.endsWith("/casos/seguimiento-vivienda-multifamiliar-seis-niveles.html")) return;

  const imageUrl = "/assets/site-photos/casos/multifamiliar-seis-niveles/recubrimiento-viga-caseton-20260721.webp";
  const guideUrl = "/errores/falta-recubrimiento-acero.html";

  document.title = document.title.replace(/(?:Cuatro|Cinco|Seis) observaciones/i, "Seis observaciones");
  document.querySelector('meta[property="og:title"]')?.setAttribute("content", "Seis observaciones técnicas en una vivienda multifamiliar de seis niveles");

  const heading = document.querySelector(".article-copy h1");
  if (heading) heading.textContent = "Vivienda multifamiliar de seis niveles: seis observaciones técnicas.";

  const lead = document.querySelector(".article-copy .article-lead");
  if (lead) lead.textContent = "Las fotografías permiten reconocer errores de albañilería, recubrimiento del acero y ejecución de elementos estructurales. Cada observación diferencia lo visible de aquello que todavía debe medirse o compararse con los planos.";

  const status = document.querySelector(".project-status strong");
  if (status) status.textContent = "6 fotografías analizadas · Lima";

  const reviewedFact = Array.from(document.querySelectorAll(".project-fact")).find((item) =>
    item.querySelector("span")?.textContent.trim() === "Elementos revisados"
  );
  reviewedFact?.querySelector("strong")?.replaceChildren("Albañilería, recubrimiento, vano, columna, escalera y viga");

  const caseIndex = document.querySelector(".case-index");
  if (caseIndex && !caseIndex.querySelector('a[href="#recubrimiento-viga-caseton"]')) {
    const card = document.createElement("a");
    card.className = "case-index-card case-index-alert";
    card.href = "#recubrimiento-viga-caseton";
    card.innerHTML = '<span>Pendiente de medición</span><strong>Recubrimiento de viga</strong><small>El acero debe quedar separado del encofrado y rodeado por suficiente concreto.</small>';
    const panderetaCard = caseIndex.querySelector('a[href="#pandereta-de-canto"]');
    if (panderetaCard) panderetaCard.after(card); else caseIndex.prepend(card);
  }

  const caseList = document.querySelector(".case-list");
  if (caseList && !document.querySelector("#recubrimiento-viga-caseton")) {
    const article = document.createElement("article");
    article.className = "case-item reveal is-visible";
    article.id = "recubrimiento-viga-caseton";
    article.innerHTML = `
      <figure class="case-photo">
        <img src="${imageUrl}" alt="Armadura de una viga aparentemente muy próxima al encofrado y a casetones de tecnopor" width="800" height="450" loading="lazy" style="width:100%;height:auto;aspect-ratio:16/9;object-fit:cover">
        <figcaption>Observación 6. Armadura de viga y casetones de tecnopor registrados el 21 de julio de 2026. La distancia exacta debe comprobarse mediante medición directa.</figcaption>
      </figure>
      <div class="case-copy">
        <span class="case-number">06 · Concreto armado y durabilidad</span>
        <div class="case-meta"><span>Condición: pendiente de medición</span><span>Elemento: viga junto a casetones de EPS</span></div>
        <h2>El acero de una viga debe quedar rodeado por suficiente concreto.</h2>
        <p class="case-summary"><strong>Qué se observa:</strong> el estribo inferior y lateral aparenta estar muy próximo al encofrado. Los casetones de tecnopor también dejan pasos estrechos junto al armado. La fotografía alerta sobre el problema, pero no permite confirmar una medida exacta.</p>
        <h3>Por qué importa el recubrimiento</h3>
        <p>La capa de concreto protege el acero frente a humedad, corrosión, fuego y desprendimientos. También ayuda a que el refuerzo quede correctamente adherido y trabaje dentro de la sección prevista.</p>
        <p><strong>¿De dónde salen los 4 cm?</strong> En una viga vaciada en obra que no está expuesta al suelo ni directamente a la intemperie, la Norma E.060 establece un recubrimiento mínimo de 40 mm. Esa distancia se mide desde la cara del concreto hasta el acero más exterior, que normalmente es el estribo. En otras condiciones el proyecto puede exigir una distancia mayor.</p>
        <p><strong>¿Y junto al casetón?</strong> No se aplica automáticamente una regla de 4 cm a cada barra. Lo indispensable es respetar los planos y dejar espacio suficiente para que el concreto ingrese, rodee las barras y pueda vibrarse sin formar vacíos o cangrejeras.</p>
        <p class="technical-note">Antes del vaciado debe medirse el recubrimiento en todas las caras, colocar separadores firmes y asegurar que el armado y los casetones no se desplacen. Si no existe la separación prevista, la corrección debe realizarse antes de cubrir el acero.</p>
        <p><a class="inline-link" href="${guideUrl}">Leer la explicación completa sobre recubrimiento del acero</a></p>
      </div>`;

    const panderetaArticle = document.querySelector("#pandereta-de-canto");
    if (panderetaArticle) panderetaArticle.after(article); else caseList.appendChild(article);
  }

  const futureGrid = document.querySelector(".future-grid");
  if (futureGrid && !futureGrid.querySelector("[data-recubrimiento-verification]")) {
    futureGrid.insertAdjacentHTML("beforeend", '<article class="future-card" data-recubrimiento-verification><span>06</span><h3>Medir el recubrimiento de la viga</h3><p>Comprobar la distancia desde el encofrado hasta el estribo y el espacio disponible para colocar y compactar el concreto junto a los casetones.</p></article>');
  }

  const footerStatus = document.querySelector(".article-footer span");
  if (footerStatus?.textContent.includes("Revisión técnica")) {
    footerStatus.textContent = "Revisión técnica actualizada: 23 de julio de 2026 · Proyecto ubicado en Lima";
  }
};

applyRecubrimientoObservation();
document.addEventListener("DOMContentLoaded", applyRecubrimientoObservation, { once: true });
window.setTimeout(applyRecubrimientoObservation, 0);
window.setTimeout(applyRecubrimientoObservation, 150);
