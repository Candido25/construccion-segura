(() => {
  const answer = document.getElementById("faqAnswer");
  if (!answer) return;

  const riskContent = {
    green: {
      title: "Orientación preventiva",
      text: "Puedes usar esta respuesta como guía para revisar y preguntar antes de ejecutar el trabajo."
    },
    yellow: {
      title: "Revisa antes de continuar",
      text: "No avances hasta comprobar este punto en los planos, en la obra o con una persona competente."
    },
    red: {
      title: "Detén y solicita evaluación",
      text: "No ocultes el problema ni continúes la actividad hasta contar con una revisión profesional."
    },
    unclassified: {
      title: "Orientación técnica general",
      text: "Esta respuesta todavía no tiene una clasificación de riesgo individual. Úsala como referencia y solicita revisión cuando tu caso afecte estructura, electricidad, gas, excavaciones o seguridad de personas."
    }
  };

  const normalizeRisk = (value) => {
    const risk = String(value || "").toLowerCase();
    return ["green", "yellow", "red"].includes(risk) ? risk : "unclassified";
  };

  const clearPreviousEnhancements = () => {
    answer.querySelectorAll(".faq-risk-panel, .faq-professional-cta").forEach((element) => element.remove());
  };

  const renderRisk = (event) => {
    clearPreviousEnhancements();

    const faq = event?.detail?.faq || {};
    const risk = normalizeRisk(faq.risk);
    const content = riskContent[risk];
    const panel = document.createElement("div");
    panel.className = "faq-risk-panel";
    panel.dataset.risk = risk;
    panel.setAttribute("role", "note");
    panel.innerHTML = `
      <span class="faq-risk-light" aria-hidden="true"></span>
      <span class="faq-risk-copy">
        <strong>${content.title}</strong>
        <span>${content.text}</span>
      </span>
    `;

    const category = answer.querySelector(".faq-answer-category");
    if (category) {
      category.insertAdjacentElement("afterend", panel);
    } else {
      answer.prepend(panel);
    }

    if (risk === "yellow" || risk === "red") {
      const cta = document.createElement("a");
      cta.className = "faq-professional-cta";
      cta.href = `/contacto.html?origen=mi-casa-segura&nivel=${risk}&consulta=${encodeURIComponent(faq.question || "")}`;
      cta.textContent = risk === "red"
        ? "Solicitar evaluación profesional"
        : "Solicitar orientación profesional";
      answer.append(cta);
    }
  };

  document.addEventListener("mi-casa-segura:faq-shown", renderRisk);
})();
