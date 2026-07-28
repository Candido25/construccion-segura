(() => {
  const supportByStage = {
    "antes-construir": {
      checklist: "antes-excavar",
      faq: "estudio de suelos planos número de pisos",
      parameter: "calicata",
      tags: ["Preconstrucción", "Suelos", "Planos"],
      alerts: [
        "No compres acero estructural sin definir el número final de pisos y el proyecto completo.",
        "No copies la cimentación, columnas o vigas de una vivienda vecina."
      ]
    },
    "terreno-movimiento": {
      checklist: "antes-excavar",
      faq: "relleno ladera excavación suelo blando agua",
      parameter: "calicata cimentación",
      tags: ["Excavación", "Laderas", "Drenaje"],
      alerts: [
        "Detén la excavación ante desprendimientos, grietas en el terreno, filtraciones o suelo no previsto.",
        "No acumules material ni permitas tránsito pesado junto al borde de una excavación inestable."
      ]
    },
    cimentaciones: {
      checklist: "antes-vaciar-concreto",
      faq: "zapata profundidad piedra recubrimiento",
      parameter: "cimiento corrido zapata recubrimiento",
      tags: ["Zapatas", "Concreto", "Acero"],
      alerts: [
        "No vacíes sobre barro, relleno suelto, agua o un fondo alterado sin revisión.",
        "No agregues piedra grande a una zapata diseñada como concreto armado."
      ]
    },
    "columnas-muros": {
      checklist: "antes-vaciar-concreto",
      faq: "columnas muros albañilería confinamiento",
      parameter: "columna confinamiento muro",
      tags: ["Albañilería", "Confinamiento", "Continuidad"],
      alerts: [
        "No interrumpas columnas, muros portantes, vigas soleras o conexiones previstas en el plano.",
        "No cambies ubicación, sección o acero para acomodar un ambiente sin revisión estructural."
      ]
    },
    "vigas-techos": {
      checklist: "antes-retirar-puntales",
      faq: "losa techo escalera puntales curado",
      parameter: "escalera garganta losa viga",
      tags: ["Vigas", "Losas", "Escaleras"],
      alerts: [
        "No retires puntales por costumbre ni cargues una losa sin confirmar resistencia y secuencia.",
        "No cortes vigas, losas o acero para hacer entrar una escalera o tubería."
      ]
    },
    sanitarias: {
      checklist: "antes-tapar-instalaciones",
      faq: "desagüe pendiente ventilación fuga",
      parameter: "pendiente desagüe ventilación",
      tags: ["Agua", "Desagüe", "Ventilación"],
      alerts: [
        "No tapes una tubería sin prueba ni dejes registros inaccesibles.",
        "No atravieses vigas o columnas para resolver un recorrido improvisado."
      ]
    },
    electricas: {
      checklist: "antes-energizar",
      faq: "cable termomagnético diferencial tierra",
      parameter: "instalación eléctrica protección",
      tags: ["Circuitos", "Protecciones", "Tierra"],
      alerts: [
        "No aumentes el amperaje de una llave para evitar que se dispare sin revisar el circuito.",
        "Olor a quemado, chispas, calentamiento o descarga requieren desconexión segura y revisión."
      ]
    },
    impermeabilizacion: {
      checklist: "antes-tarrajear",
      faq: "humedad salitre filtración impermeabilización",
      parameter: "impermeabilización pendiente",
      tags: ["Humedad", "Techos", "Pruebas"],
      alerts: [
        "No pintes ni selles antes de identificar y detener el ingreso de agua.",
        "No cubras un sistema impermeable sin realizar la prueba prevista."
      ]
    },
    acabados: {
      checklist: "antes-tarrajear",
      faq: "tarrajeo acabado fisura humedad",
      parameter: "juntas baranda altura",
      tags: ["Tarrajeo", "Enchapes", "Recepción"],
      alerts: [
        "No uses acabados para ocultar humedad, grietas activas o defectos de instalaciones.",
        "Aprueba una muestra antes de repetir un acabado en toda la vivienda."
      ]
    },
    ampliaciones: {
      checklist: "antes-recibir-etapa",
      faq: "agregar piso ampliación cortar muro viga",
      parameter: "escalera ampliación carga",
      tags: ["Evaluación", "Demolición", "Permisos"],
      alerts: [
        "No agregues pisos sin revisar cimentación y estructura existentes.",
        "No abras vanos ni retires muros sin identificar primero su función y la secuencia de soporte."
      ]
    },
    seguridad: {
      checklist: "antes-excavar",
      faq: "seguridad caída excavación electricidad obra",
      parameter: "baranda escalera",
      tags: ["Caídas", "Excavaciones", "Herramientas"],
      alerts: [
        "Aísla huecos, bordes y excavaciones antes de permitir tránsito o trabajo cercano.",
        "Retira herramientas, cables y plataformas dañadas; el equipo personal no corrige una condición insegura."
      ]
    },
    mantenimiento: {
      checklist: "despues-evento",
      faq: "mantenimiento grieta humedad después de sismo",
      parameter: "baranda mantenimiento",
      tags: ["Recepción", "Inspección", "Vida útil"],
      alerts: [
        "Después de un evento, prioriza estructura, electricidad, gas y elementos que puedan caer.",
        "No repares el acabado sin corregir primero la causa del deterioro."
      ]
    }
  };

  const closeModule = () => {
    const moduleView = document.getElementById("moduleView");
    if (moduleView && !moduleView.hidden) document.getElementById("closeModule")?.click();
  };

  const openFaqSearch = (query) => {
    closeModule();
    window.setTimeout(() => {
      const input = document.getElementById("faqSearch");
      if (!input) return;
      input.value = query;
      input.dispatchEvent(new Event("input", { bubbles: true }));
      document.getElementById("dudas")?.scrollIntoView({ behavior: "smooth", block: "start" });
      input.focus({ preventScroll: true });
    }, 120);
  };

  const openParameterSearch = (query) => {
    closeModule();
    window.setTimeout(() => {
      const input = document.getElementById("normativeSearch");
      const form = document.getElementById("normativeForm");
      if (!input || !form) return;
      input.value = query;
      document.getElementById("parametros-tecnicos")?.scrollIntoView({ behavior: "smooth", block: "start" });
      if (typeof form.requestSubmit === "function") form.requestSubmit();
      else form.dispatchEvent(new Event("submit", { bubbles: true, cancelable: true }));
    }, 120);
  };

  const enhanceModule = (stageId) => {
    const support = supportByStage[stageId];
    const shell = document.querySelector("#moduleContent .module-shell");
    if (!support || !shell || shell.querySelector(".stage-support-panel")) return;

    const panel = document.createElement("section");
    panel.className = "stage-support-panel";
    panel.dataset.stageSupport = stageId;
    panel.innerHTML = `
      <p class="eyebrow">Antes de continuar</p>
      <h2>Controles y consultas relacionadas</h2>
      <ul class="stage-support-alerts">${support.alerts.map((item) => `<li>${item}</li>`).join("")}</ul>
      <div class="stage-support-tags">${support.tags.map((tag) => `<span>${tag}</span>`).join("")}</div>
      <div class="stage-support-actions">
        <button type="button" data-stage-support-action="checklist">Abrir lista crítica</button>
        <button type="button" data-stage-support-action="faq">Consultar dudas relacionadas</button>
        <button type="button" data-stage-support-action="parameter">Ver parámetros técnicos</button>
      </div>
    `;

    panel.addEventListener("click", (event) => {
      const button = event.target.closest("[data-stage-support-action]");
      if (!button) return;
      const action = button.dataset.stageSupportAction;

      if (action === "checklist") {
        closeModule();
        window.setTimeout(() => {
          document.dispatchEvent(new CustomEvent("mi-casa-segura:open-checklist", {
            detail: { id: support.checklist }
          }));
        }, 120);
      } else if (action === "faq") {
        openFaqSearch(support.faq);
      } else if (action === "parameter") {
        openParameterSearch(support.parameter);
      }
    });

    shell.append(panel);
    document.dispatchEvent(new CustomEvent("mi-casa-segura:stage-opened", {
      detail: { stageId, support }
    }));
  };

  document.addEventListener("click", (event) => {
    const button = event.target.closest("[data-module]");
    if (!button) return;
    const stageId = button.dataset.module;
    if (!supportByStage[stageId]) return;
    window.setTimeout(() => enhanceModule(stageId), 0);
  });
})();