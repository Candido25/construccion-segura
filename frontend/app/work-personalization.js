(() => {
  const PROFILE_KEY = "mi-casa-segura-work-profile-v1";
  const CHECKLIST_KEY = "mi-casa-segura-critical-checklists-v1";
  const profileSection = document.getElementById("mi-obra");
  if (!profileSection) return;

  const stagePlan = {
    planning: {
      stageId: "antes-construir",
      checklistId: "antes-excavar",
      title: "Ordena estudios, planos y permisos antes de excavar",
      text: "Tu siguiente control recomendado es comprobar terreno, vecinos, servicios y secuencia de excavación."
    },
    excavation: {
      stageId: "terreno-movimiento",
      checklistId: "antes-excavar",
      title: "Verifica la excavación antes de retirar más material",
      text: "Confirma estabilidad, agua, bordes, acceso y condición real del suelo antes de continuar."
    },
    foundations: {
      stageId: "cimentaciones",
      checklistId: "antes-vaciar-concreto",
      title: "No vacíes hasta revisar cimentación, acero y recubrimiento",
      text: "Compara el armado con los planos y verifica el fondo, los separadores y la logística del concreto."
    },
    structure: {
      stageId: "vigas-techos",
      checklistId: "antes-vaciar-concreto",
      title: "Revisa estructura antes de cada vaciado",
      text: "Medidas, acero, encofrado, instalaciones y curado deben estar comprobados antes de ocultarse."
    },
    installations: {
      stageId: "sanitarias",
      checklistId: "antes-tapar-instalaciones",
      title: "Prueba las instalaciones antes de taparlas",
      text: "No cierres pisos, muros o ductos sin comprobar recorridos, fugas, pendientes, registros y fotografías."
    },
    finishes: {
      stageId: "acabados",
      checklistId: "antes-tarrajear",
      title: "No ocultes fallas con acabados",
      text: "Comprueba soporte, humedad, fisuras e instalaciones antes de tarrajear, pintar o enchapar."
    },
    maintenance: {
      stageId: "mantenimiento",
      checklistId: "antes-recibir-etapa",
      title: "Organiza la recepción y el mantenimiento",
      text: "Guarda documentos, registra cambios y atiende las causas de cualquier deterioro antes de repararlo."
    }
  };

  const readJson = (key) => {
    try {
      const value = window.localStorage.getItem(key);
      return value ? JSON.parse(value) : null;
    } catch {
      return null;
    }
  };

  const getChecklistProgress = (checklistId) => {
    const state = readJson(CHECKLIST_KEY) || {};
    const list = (window.MI_CASA_SEGURA_CRITICAL_CHECKLISTS || []).find((item) => item.id === checklistId);
    const checked = state[checklistId]?.checked || {};
    const total = list?.items?.length || 0;
    const completed = Object.values(checked).filter(Boolean).length;
    return { completed, total, pending: Math.max(0, total - completed) };
  };

  const ensureCard = () => {
    let card = profileSection.querySelector("#workNextAction");
    if (card) return card;
    card = document.createElement("div");
    card.className = "next-action-card";
    card.id = "workNextAction";
    card.setAttribute("aria-live", "polite");
    profileSection.append(card);
    return card;
  };

  const render = () => {
    const profile = readJson(PROFILE_KEY);
    const card = ensureCard();

    if (!profile) {
      card.dataset.level = "warning";
      card.innerHTML = `
        <div class="next-action-title"><span class="next-action-dot" aria-hidden="true"></span><h3>Configura Mi obra para recibir una ruta recomendada</h3></div>
        <p>La personalización se realiza únicamente con los datos guardados en este dispositivo.</p>
        <div class="next-action-actions"><button type="button" data-personal-action="profile">Configurar mi obra</button></div>
      `;
      return;
    }

    const plan = stagePlan[profile.stage] || stagePlan.planning;
    const progress = getChecklistProgress(plan.checklistId);
    const warnings = [];

    if (["slope", "fill"].includes(profile.terrain)) {
      warnings.push("El terreno indicado requiere atención especial antes de excavar o definir cimentaciones.");
    }
    if (profile.plannedFloors === "3plus" && profile.structuralPlans !== "yes") {
      warnings.push("No has confirmado planos estructurales para tres pisos o más.");
    }
    if (["nueva", "ampliacion"].includes(profile.projectType) && profile.soilStudy !== "yes") {
      warnings.push("No has confirmado información de suelos para la obra proyectada.");
    }

    card.dataset.level = warnings.length ? "warning" : "ready";
    card.innerHTML = `
      <div class="next-action-title"><span class="next-action-dot" aria-hidden="true"></span><h3>${plan.title}</h3></div>
      <p>${plan.text}</p>
      <div class="checklist-overview">
        <span>${progress.completed} de ${progress.total || 0} controles revisados</span>
        <span>${progress.pending} pendientes</span>
      </div>
      ${warnings.length ? `<ul class="stage-support-alerts">${warnings.map((item) => `<li>${item}</li>`).join("")}</ul>` : ""}
      <div class="next-action-actions">
        <button type="button" data-personal-action="checklist" data-checklist-id="${plan.checklistId}">Abrir lista recomendada</button>
        <button type="button" data-personal-action="stage" data-stage-id="${plan.stageId}">Abrir etapa relacionada</button>
        <button type="button" data-personal-action="profile">Editar mi obra</button>
      </div>
    `;

    document.dispatchEvent(new CustomEvent("mi-casa-segura:recommend-checklist", {
      detail: { id: plan.checklistId }
    }));
  };

  profileSection.addEventListener("click", (event) => {
    const button = event.target.closest("[data-personal-action]");
    if (!button) return;

    if (button.dataset.personalAction === "profile") {
      document.dispatchEvent(new CustomEvent("mi-casa-segura:open-work-profile"));
      return;
    }

    if (button.dataset.personalAction === "checklist") {
      document.dispatchEvent(new CustomEvent("mi-casa-segura:open-checklist", {
        detail: { id: button.dataset.checklistId }
      }));
      return;
    }

    if (button.dataset.personalAction === "stage") {
      document.querySelector(`[data-module="${button.dataset.stageId}"]`)?.click();
    }
  });

  document.addEventListener("mi-casa-segura:work-profile-saved", render);
  document.addEventListener("mi-casa-segura:checklists-updated", render);
  window.addEventListener("storage", (event) => {
    if ([PROFILE_KEY, CHECKLIST_KEY].includes(event.key)) render();
  });

  render();
})();