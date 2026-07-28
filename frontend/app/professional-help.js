(() => {
  const PHONE = "51968481482";
  const PROFILE_KEY = "mi-casa-segura-work-profile-v1";

  const buildWhatsAppUrl = (message) => `https://wa.me/${PHONE}?text=${encodeURIComponent(message)}`;

  const configureLink = (link, message) => {
    if (!link) return;
    link.href = buildWhatsAppUrl(message);
    link.target = "_blank";
    link.rel = "noopener noreferrer";
  };

  const readProfile = () => {
    try {
      const stored = window.localStorage.getItem(PROFILE_KEY);
      return stored ? JSON.parse(stored) : null;
    } catch {
      return null;
    }
  };

  const stageLabels = {
    planning: "planificación, estudios o planos",
    excavation: "excavación y movimiento de tierras",
    foundations: "cimentaciones",
    structure: "estructura",
    installations: "instalaciones",
    finishes: "acabados",
    maintenance: "mantenimiento o vivienda terminada"
  };

  const profileContext = () => {
    const profile = readProfile();
    if (!profile) return "Etapa de la obra: no indicada.";
    const location = [profile.district, profile.department].filter(Boolean).join(", ");
    const stage = stageLabels[profile.stage] || "no indicada";
    return `Etapa de la obra: ${stage}.${location ? ` Ubicación referencial: ${location}.` : ""}`;
  };

  const suggestedService = (context = {}) => {
    const text = `${context.question || ""} ${context.stage || ""} ${context.system || ""}`.toLowerCase();
    if (text.includes("grieta") || text.includes("rajadura") || text.includes("fisura") || text.includes("daño")) {
      return "evaluación de grietas y daños";
    }
    if (text.includes("ampli") || text.includes("otro piso") || text.includes("agregar un piso")) {
      return "orientación para ampliaciones";
    }
    if (text.includes("zapata") || text.includes("ciment") || text.includes("vaciado") || text.includes("concreto")) {
      return "revisión antes de vaciado o revisión estructural";
    }
    if (context.risk === "red") return "inspección técnica prioritaria";
    return "consulta remota inicial";
  };

  document.addEventListener("mi-casa-segura:faq-shown", (event) => {
    const faq = event.detail?.faq || {};
    window.requestAnimationFrame(() => {
      const link = document.querySelector("#faqAnswer .faq-professional-cta");
      if (!link) return;
      const level = faq.risk === "red" ? "rojo" : faq.risk === "yellow" ? "amarillo" : "verde";
      const service = suggestedService({ ...faq, risk: faq.risk });
      configureLink(
        link,
        [
          "Hola, soy usuario de Mi Casa Segura.",
          "Origen: buscador de preguntas.",
          `Tema consultado: ${faq.question || "Consulta de obra"}.`,
          `Etapa relacionada: ${faq.stage || "no indicada"}.`,
          `Nivel mostrado por la aplicación: ${level}.`,
          `Servicio sugerido: ${service}.`,
          profileContext(),
          "Necesito orientación profesional."
        ].join(" ")
      );
    });
  });

  const problemResult = document.getElementById("problemResult");
  if (problemResult) {
    const observer = new MutationObserver(() => {
      const link = problemResult.querySelector(".problem-contact");
      if (!link) return;
      const title = document.getElementById("problemDialogTitle")?.textContent?.trim() || "Problema en obra";
      const risk = problemResult.dataset.risk || "yellow";
      const level = risk === "red" ? "rojo" : risk === "yellow" ? "amarillo" : "verde";
      const service = suggestedService({ question: title, risk });
      configureLink(
        link,
        [
          "Hola, soy usuario de Mi Casa Segura.",
          "Origen: evaluador guiado de problemas.",
          `Tema evaluado: ${title}.`,
          `Nivel mostrado por la aplicación: ${level}.`,
          `Servicio sugerido: ${service}.`,
          profileContext(),
          "Necesito orientación profesional."
        ].join(" ")
      );
    });
    observer.observe(problemResult, { childList: true, subtree: true, attributes: true });
  }

  const generalLink = document.querySelector('[data-professional-help="general"]');
  configureLink(
    generalLink,
    `Hola, soy usuario de Mi Casa Segura. Origen: centro de ayuda. ${profileContext()} Necesito una consulta remota inicial sobre una construcción, ampliación, remodelación o problema en mi vivienda.`
  );

  if (!document.querySelector('script[src="/app/phase1-bootstrap.js?v=1"]')) {
    const script = document.createElement("script");
    script.src = "/app/phase1-bootstrap.js?v=1";
    document.body.append(script);
  }
})();