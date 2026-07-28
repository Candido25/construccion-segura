(() => {
  const STORAGE_KEY = "mi-casa-segura-critical-checklists-v1";

  const checklists = [
    {
      id: "antes-excavar",
      icon: "▽",
      title: "Antes de excavar",
      summary: "Terreno, vecinos, servicios y estabilidad temporal.",
      stages: ["planning", "excavation"],
      items: [
        "Identifiqué si el terreno es natural, rellenado, húmedo o inclinado.",
        "Revisé construcciones vecinas, taludes, muros y zonas que podrían verse afectadas.",
        "Localicé tuberías, cables, desagües u otros servicios antes de abrir zanjas.",
        "Definí dónde se colocará el material excavado sin sobrecargar los bordes.",
        "La excavación tiene acceso, protección y secuencia segura antes de comenzar."
      ]
    },
    {
      id: "antes-vaciar-concreto",
      icon: "▦",
      title: "Antes de vaciar concreto",
      summary: "Planos, medidas, acero, recubrimiento y logística.",
      stages: ["foundations", "structure"],
      items: [
        "Las dimensiones, niveles y ubicación coinciden con los planos.",
        "El acero, estribos, empalmes, anclajes y recubrimientos fueron revisados.",
        "No existen tuberías que corten, desplacen o atraviesen el refuerzo sin detalle aprobado.",
        "El encofrado está firme, limpio, alineado y preparado para la presión del concreto.",
        "Están definidos concreto, acceso, compactación, personal, curado y protección posterior."
      ]
    },
    {
      id: "antes-tapar-instalaciones",
      icon: "≋",
      title: "Antes de tapar instalaciones",
      summary: "Recorridos, pruebas, registros y fotografías.",
      stages: ["installations"],
      items: [
        "Los recorridos coinciden con los planos y no dañan elementos estructurales.",
        "Las redes fueron probadas y no presentan fugas, pérdidas ni uniones forzadas.",
        "Pendientes, ventilaciones, válvulas, cajas y registros quedan accesibles donde corresponde.",
        "Tomé fotografías claras con referencias antes de cubrir tuberías y canalizaciones.",
        "Se corrigieron todas las observaciones antes de rellenar, vaciar o tarrajear."
      ]
    },
    {
      id: "antes-retirar-puntales",
      icon: "⌂",
      title: "Antes de retirar puntales",
      summary: "Resistencia, cargas, secuencia y reapuntalamiento.",
      stages: ["structure"],
      items: [
        "La autorización se basa en resistencia alcanzada y procedimiento, no solo en días transcurridos.",
        "Se revisaron luces, voladizos, temperatura, estado del concreto y secuencia de retiro.",
        "No se almacenarán ladrillos, bolsas, equipos u otras cargas tempranas sobre la losa.",
        "El reapuntalamiento previsto está colocado antes de retirar apoyos principales.",
        "No existen fisuras, deformaciones, vacíos o señales que requieran evaluación previa."
      ]
    },
    {
      id: "antes-tarrajear",
      icon: "▧",
      title: "Antes de tarrajear o revestir",
      summary: "Soporte, humedad, fisuras, pases y muestras.",
      stages: ["finishes"],
      items: [
        "El soporte está limpio, firme y libre de material suelto o contaminantes.",
        "No se ocultarán humedad, filtraciones, grietas activas ni concreto defectuoso.",
        "Las instalaciones empotradas fueron probadas antes de quedar cubiertas.",
        "Pases, cajas, juntas y encuentros están terminados y coordinados.",
        "Se aprobó una muestra de textura, espesor, alineamiento y acabado antes de continuar."
      ]
    },
    {
      id: "antes-energizar",
      icon: "↯",
      title: "Antes de energizar",
      summary: "Tablero, circuitos, protecciones, tierra y terminaciones.",
      stages: ["installations"],
      items: [
        "Cada circuito está identificado y corresponde al cuadro de cargas.",
        "Las protecciones corresponden a los conductores y no existen puentes improvisados.",
        "La puesta a tierra y el interruptor diferencial fueron verificados.",
        "Cajas, empalmes, tapas, canalizaciones y tablero están terminados, secos y protegidos.",
        "No existen cables expuestos, calentamiento, olor, chispas ni partes energizadas accesibles."
      ]
    },
    {
      id: "antes-recibir-etapa",
      icon: "✓",
      title: "Antes de recibir una etapa",
      summary: "Pruebas, observaciones, documentos y pago por avance.",
      stages: ["planning", "foundations", "structure", "installations", "finishes", "maintenance"],
      items: [
        "Comparé el trabajo ejecutado con planos, alcance, medidas y especificaciones acordadas.",
        "Probé instalaciones, herrajes y elementos que luego serán difíciles de corregir.",
        "Registré observaciones con ubicación, responsable y fecha de corrección.",
        "Conservé fotografías, comprobantes, fichas, pruebas y cambios aprobados.",
        "El pago corresponde a un avance comprobado y no a trabajos pendientes u ocultos sin revisar."
      ]
    },
    {
      id: "despues-evento",
      icon: "!",
      title: "Después de sismo, incendio o inundación",
      summary: "Acceso, servicios, daños nuevos y registro seguro.",
      stages: ["maintenance"],
      items: [
        "Comprobé desde un lugar seguro si existen inclinaciones, deformaciones o elementos que pueden caer.",
        "Revisé grietas nuevas en columnas, vigas, muros, escaleras y techos.",
        "No restablecí electricidad o gas cuando hay humedad, olor, humo o instalaciones dañadas.",
        "Restringí el acceso a zonas con desprendimientos, movimiento o señales de inestabilidad.",
        "Registré fecha, evento, daños observados y solicité evaluación cuando corresponde."
      ]
    }
  ];

  window.MI_CASA_SEGURA_CRITICAL_CHECKLISTS = checklists;

  const stageSection = document.getElementById("guia-etapas");
  if (!stageSection) return;

  const readState = () => {
    try {
      const value = window.localStorage.getItem(STORAGE_KEY);
      return value ? JSON.parse(value) : {};
    } catch (error) {
      console.warn("No se pudo leer el avance de listas críticas.", error);
      return {};
    }
  };

  const writeState = (state) => {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    document.dispatchEvent(new CustomEvent("mi-casa-segura:checklists-updated", { detail: { state } }));
  };

  const formatDate = (value) => {
    if (!value) return "Aún no revisada";
    try {
      return `Última revisión: ${new Intl.DateTimeFormat("es-PE", { dateStyle: "medium", timeStyle: "short" }).format(new Date(value))}`;
    } catch {
      return "Revisión registrada";
    }
  };

  const section = document.createElement("section");
  section.className = "critical-checklists-section";
  section.id = "listas-criticas";
  section.setAttribute("aria-labelledby", "critical-checklists-title");
  section.innerHTML = `
    <div class="critical-checklists-heading">
      <p class="eyebrow">Antes de ocultar o continuar</p>
      <h2 id="critical-checklists-title">Listas de verificación críticas</h2>
      <p>Marca los controles que realmente comprobaste. El avance y la fecha quedan guardados únicamente en este dispositivo.</p>
    </div>
    <div class="checklist-overview" id="criticalChecklistOverview" aria-live="polite"></div>
    <div class="critical-checklist-grid" id="criticalChecklistGrid"></div>
  `;
  stageSection.insertAdjacentElement("afterend", section);

  const grid = section.querySelector("#criticalChecklistGrid");
  const overview = section.querySelector("#criticalChecklistOverview");
  let openChecklistId = "";
  let recommendedId = "";

  const getChecklistState = (state, id) => state[id] || { checked: {}, reviewedAt: "" };

  const render = () => {
    const state = readState();
    let completedItems = 0;
    let totalItems = 0;
    let completedLists = 0;

    grid.innerHTML = checklists.map((list) => {
      const listState = getChecklistState(state, list.id);
      const checkedCount = list.items.filter((_, index) => Boolean(listState.checked?.[index])).length;
      totalItems += list.items.length;
      completedItems += checkedCount;
      if (checkedCount === list.items.length) completedLists += 1;

      const open = openChecklistId === list.id;
      const recommended = recommendedId === list.id;
      return `
        <article class="critical-checklist-card${open ? " open" : ""}${recommended ? " is-recommended" : ""}" data-checklist-card="${list.id}">
          <button class="critical-checklist-toggle" type="button" aria-expanded="${open}" data-checklist-toggle="${list.id}">
            <span class="critical-checklist-icon" aria-hidden="true">${list.icon}</span>
            <span class="critical-checklist-copy"><strong>${list.title}</strong><small>${list.summary}${recommended ? " · Recomendada para tu etapa" : ""}</small></span>
            <span class="critical-checklist-progress">${checkedCount}/${list.items.length}</span>
          </button>
          <div class="critical-checklist-body">
            <div class="critical-checklist-items">
              ${list.items.map((item, index) => `
                <label class="critical-checklist-item">
                  <input type="checkbox" data-checklist-id="${list.id}" data-item-index="${index}" ${listState.checked?.[index] ? "checked" : ""}>
                  <span>${item}</span>
                </label>
              `).join("")}
            </div>
            <div class="critical-checklist-meta">
              <span class="critical-checklist-date">${formatDate(listState.reviewedAt)}</span>
              <button class="critical-checklist-reset" type="button" data-reset-checklist="${list.id}">Reiniciar esta lista</button>
            </div>
          </div>
        </article>
      `;
    }).join("");

    overview.innerHTML = `
      <span>${completedItems} de ${totalItems} controles revisados</span>
      <span>${completedLists} de ${checklists.length} listas completas</span>
      <span>${totalItems - completedItems} controles pendientes</span>
    `;
  };

  grid.addEventListener("click", (event) => {
    const toggle = event.target.closest("[data-checklist-toggle]");
    if (toggle) {
      openChecklistId = openChecklistId === toggle.dataset.checklistToggle ? "" : toggle.dataset.checklistToggle;
      render();
      return;
    }

    const reset = event.target.closest("[data-reset-checklist]");
    if (!reset) return;
    const id = reset.dataset.resetChecklist;
    if (!window.confirm("¿Deseas borrar el avance guardado de esta lista?")) return;
    const state = readState();
    delete state[id];
    writeState(state);
    render();
  });

  grid.addEventListener("change", (event) => {
    const input = event.target.closest("input[data-checklist-id]");
    if (!input) return;

    const state = readState();
    const id = input.dataset.checklistId;
    const index = input.dataset.itemIndex;
    const listState = getChecklistState(state, id);
    listState.checked = { ...(listState.checked || {}), [index]: input.checked };
    listState.reviewedAt = new Date().toISOString();
    state[id] = listState;
    openChecklistId = id;
    writeState(state);
    render();
  });

  document.addEventListener("mi-casa-segura:open-checklist", (event) => {
    const id = event.detail?.id;
    if (!checklists.some((list) => list.id === id)) return;
    recommendedId = id;
    openChecklistId = id;
    render();
    section.hidden = false;
    window.requestAnimationFrame(() => {
      section.scrollIntoView({ behavior: "smooth", block: "start" });
      grid.querySelector(`[data-checklist-card="${id}"]`)?.focus?.();
    });
  });

  document.addEventListener("mi-casa-segura:recommend-checklist", (event) => {
    const id = event.detail?.id || "";
    recommendedId = checklists.some((list) => list.id === id) ? id : "";
    render();
  });

  render();
})();