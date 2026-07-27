(() => {
  const routeButtons = document.querySelectorAll("[data-app-route]");
  const faqSection = document.getElementById("dudas");
  const faqInput = document.getElementById("faqSearch");
  const stageSection = document.querySelector(".stage-section");
  const problemButton = document.querySelector('[data-module="problemas"]');
  const faqAnswer = document.getElementById("faqAnswer");

  const scrollToElement = (element) => {
    if (!element) return;
    element.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  routeButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const route = button.dataset.appRoute;

      if (route === "construir") {
        scrollToElement(stageSection);
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

  const classifyRisk = (text) => {
    const normalized = String(text || "")
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");

    const redSignals = [
      "derrumbe", "deslizamiento", "hundimiento", "columna inclinada",
      "viga cortada", "cortar acero", "olor a quemado", "chispas",
      "electrocucion", "fuga de gas", "grieta crece", "atraviesa la losa",
      "deformacion", "desprendimiento", "retorno de aguas residuales",
      "construir un piso mas", "agregar un piso", "ampliacion vertical"
    ];

    const yellowSignals = [
      "zapata", "cimentacion", "encofrado", "puntal", "fisura", "grieta",
      "rajadura", "salitre", "humedad", "cable", "termomagnetico",
      "diferencial", "desague", "pendiente", "escalera", "garganta",
      "estudio de suelos", "concreto", "losa", "techo"
    ];

    if (redSignals.some((signal) => normalized.includes(signal))) return "red";
    if (yellowSignals.some((signal) => normalized.includes(signal))) return "yellow";
    return "green";
  };

  const riskContent = {
    green: {
      title: "Orientación preventiva",
      text: "Puedes usar esta respuesta como guía para revisar y preguntar antes de ejecutar el trabajo."
    },
    yellow: {
      title: "Revisa antes de continuar",
      text: "La consulta puede involucrar una decisión que conviene comprobar en planos, en obra o con una persona competente antes de avanzar."
    },
    red: {
      title: "Detén y solicita evaluación",
      text: "La consulta contiene señales que pueden comprometer la seguridad. No ocultes el problema ni continúes hasta contar con una revisión profesional."
    }
  };

  const enhanceAnswer = () => {
    if (!faqAnswer || faqAnswer.hidden || !faqAnswer.textContent.trim()) return;
    if (faqAnswer.querySelector(".faq-risk-panel")) return;

    const risk = classifyRisk(faqAnswer.textContent);
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

    const category = faqAnswer.querySelector(".faq-answer-category");
    if (category) {
      category.insertAdjacentElement("afterend", panel);
    } else {
      faqAnswer.prepend(panel);
    }

    if (risk === "red" || risk === "yellow") {
      const cta = document.createElement("a");
      cta.className = "faq-professional-cta";
      cta.href = `/contacto.html?origen=mi-casa-segura&nivel=${risk}`;
      cta.textContent = risk === "red"
        ? "Solicitar evaluación profesional"
        : "Solicitar orientación profesional";
      faqAnswer.append(cta);
    }
  };

  if (faqAnswer) {
    const observer = new MutationObserver(enhanceAnswer);
    observer.observe(faqAnswer, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ["hidden"]
    });
  }
})();
