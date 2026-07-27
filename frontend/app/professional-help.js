(() => {
  const PHONE = "51968481482";

  const buildWhatsAppUrl = (message) => `https://wa.me/${PHONE}?text=${encodeURIComponent(message)}`;

  const configureLink = (link, message) => {
    if (!link) return;
    link.href = buildWhatsAppUrl(message);
    link.target = "_blank";
    link.rel = "noopener noreferrer";
  };

  document.addEventListener("mi-casa-segura:faq-shown", (event) => {
    const faq = event.detail?.faq || {};
    window.requestAnimationFrame(() => {
      const link = document.querySelector("#faqAnswer .faq-professional-cta");
      if (!link) return;
      const level = faq.risk === "red" ? "rojo" : "amarillo";
      configureLink(
        link,
        `Hola, soy usuario de Mi Casa Segura. La aplicación mostró un nivel ${level} para esta consulta: “${faq.question || "Consulta de obra"}”. Necesito orientación profesional.`
      );
    });
  });

  const problemResult = document.getElementById("problemResult");
  if (problemResult) {
    const observer = new MutationObserver(() => {
      const link = problemResult.querySelector(".problem-contact");
      if (!link) return;
      const title = document.getElementById("problemDialogTitle")?.textContent?.trim() || "Problema en obra";
      const level = problemResult.dataset.risk === "red" ? "rojo" : "amarillo";
      configureLink(
        link,
        `Hola, soy usuario de Mi Casa Segura. El evaluador mostró un nivel ${level} para: “${title}”. Necesito orientación profesional.`
      );
    });
    observer.observe(problemResult, { childList: true, subtree: true, attributes: true });
  }

  const generalLink = document.querySelector('[data-professional-help="general"]');
  configureLink(
    generalLink,
    "Hola, soy usuario de Mi Casa Segura. Necesito orientación profesional sobre una construcción, ampliación, remodelación o problema en mi vivienda."
  );
})();
