const STORAGE_KEY = "construccion-segura-app-progress-v1";

const modules = {
  "antes-construir": {
    eyebrow: "Primera decisión",
    title: "Antes de construir",
    intro: "Una vivienda segura empieza antes de excavar. Revisa el terreno, define cuántos pisos tendrá la edificación y trabaja con información técnica compatible entre sí.",
    topics: [
      {
        id: "terreno",
        title: "Terreno y ubicación",
        subtitle: "Observa pendientes, rellenos, humedad y construcciones vecinas.",
        blocks: [
          ["info", "Qué debes revisar", "Identifica si el terreno es natural, rellenado, húmedo, inclinado o está cerca de cortes, taludes, muros de contención, quebradas o cauces. Estas condiciones cambian la forma de estudiar y resolver la cimentación."],
          ["warning", "Señal de alerta", "No inicies excavaciones en una ladera, junto a un corte vertical o sobre rellenos sin una evaluación técnica. Un terreno que parece firme en la superficie puede comportarse de manera diferente en profundidad."],
          ["design", "Depende del diseño", "El tipo y profundidad de cimentación deben definirse con información del suelo, cargas de la vivienda, pendiente y condiciones de las edificaciones vecinas."]
        ],
        checks: [
          "Reconocí si el terreno es plano, inclinado, natural o rellenado.",
          "Revisé si existen grietas, filtraciones o movimientos de tierra cercanos.",
          "Identifiqué muros, viviendas o excavaciones que puedan verse afectados."
        ]
      },
      {
        id: "pisos",
        title: "Número real de pisos",
        subtitle: "Diseña desde el inicio para la vivienda que realmente proyectas.",
        blocks: [
          ["info", "Regla básica", "Define desde el inicio el número de pisos que deseas construir ahora y en el futuro. La cimentación, columnas, muros y vigas deben responder al proyecto completo previsto."],
          ["warning", "No improvises después", "Agregar pisos sin verificar la capacidad de la estructura existente puede exigir refuerzos costosos y, en algunos casos, no ser viable."],
          ["design", "Depende del diseño", "No existe una medida única de zapata, columna o acero aplicable a todas las viviendas. Las dimensiones y refuerzos deben provenir del proyecto estructural."]
        ],
        checks: [
          "Definí cuántos pisos tendrá finalmente la vivienda.",
          "Informé al proyectista si pienso ampliar en el futuro.",
          "Evité comprar acero o concreto antes de contar con planos."
        ]
      },
      {
        id: "estudios-planos",
        title: "Estudio de suelos y planos",
        subtitle: "La arquitectura, las estructuras y las instalaciones deben coordinarse.",
        blocks: [
          ["info", "Documentos esenciales", "El estudio del suelo aporta información para elegir la cimentación. Los planos estructurales indican dimensiones, acero, concreto y detalles; los planos de instalaciones ayudan a evitar perforaciones o cruces improvisados."],
          ["warning", "Error frecuente", "Construir solo con un dibujo arquitectónico o copiar las medidas de la vivienda vecina no demuestra que la estructura sea adecuada para tu terreno y tu proyecto."],
          ["design", "Antes de empezar", "Verifica que la ubicación de columnas, muros, escaleras, tuberías y ambientes sea compatible entre todos los planos."]
        ],
        checks: [
          "Cuento con información del suelo elaborada para mi terreno.",
          "Tengo planos estructurales y conozco quién responde por el diseño.",
          "Los planos de arquitectura, estructuras e instalaciones están coordinados."
        ]
      },
      {
        id: "presupuesto-secuencia",
        title: "Presupuesto y secuencia",
        subtitle: "Planifica por etapas sin dejar elementos vulnerables.",
        blocks: [
          ["info", "Planifica el dinero", "Separa recursos para estudios, planos, materiales, mano de obra, control de calidad y contingencias. Ahorrar eliminando controles básicos puede generar retrabajos mayores."],
          ["warning", "No dejes la seguridad para el final", "No empieces una etapa si no puedes completar las protecciones, el curado, los rellenos controlados o la estabilidad temporal que esa etapa necesita."],
          ["design", "Orden de trabajo", "Define qué debe revisarse antes de cada vaciado, qué elementos quedarán ocultos y quién autorizará continuar."]
        ],
        checks: [
          "El presupuesto incluye estudios, planos y controles.",
          "Sé qué revisar antes de cada vaciado.",
          "Tengo una secuencia de construcción y no solo una lista de compras."
        ]
      }
    ]
  },
  cimentaciones: {
    eyebrow: "Etapa crítica",
    title: "Bases y cimentaciones",
    intro: "Antes de vaciar, confirma que excavación, dimensiones, acero, recubrimiento, instalaciones y concreto coincidan con los planos. Después del vaciado, muchos errores quedan ocultos.",
    topics: [
      {
        id: "excavacion",
        title: "Excavación y fondo",
        subtitle: "No vacíes sobre material suelto, agua o suelo alterado.",
        blocks: [
          ["info", "Qué debes revisar", "El fondo debe llegar al nivel y al suelo indicados por el proyecto, estar limpio y conservar su condición natural. Retira material suelto, barro, basura y agua antes de colocar la cimentación."],
          ["warning", "Detén el trabajo", "Si aparecen rellenos, cavidades, filtraciones, suelo muy blando, diferencias importantes entre excavaciones o riesgo de derrumbe, no continúes sin evaluación."],
          ["design", "Depende del terreno", "La profundidad no se define copiando otra obra. Debe responder al suelo encontrado, al proyecto y a las condiciones de estabilidad de la excavación."]
        ],
        checks: [
          "El fondo está limpio, sin barro, basura ni material suelto.",
          "La excavación coincide con niveles y dimensiones del plano.",
          "No existen filtraciones, vacíos o cambios de suelo sin evaluar."
        ]
      },
      {
        id: "zapatas",
        title: "Zapatas de concreto armado",
        subtitle: "No confundas una zapata estructural con concreto ciclópeo.",
        blocks: [
          ["info", "Regla básica", "Una zapata de concreto armado debe ejecutarse con el concreto y el acero especificados en el diseño. No agregues piedras grandes para aumentar volumen o ahorrar mezcla."],
          ["warning", "No permitas esto", "No conviertas una zapata diseñada como concreto armado en una mezcla improvisada con piedra grande. Si el proyecto contempla concreto ciclópeo en otro elemento, debe estar expresamente indicado y detallado."],
          ["design", "Verifica en planos", "Comprueba ancho, largo, espesor, nivel, resistencia del concreto, diámetro y separación de barras, arranques de columnas y recubrimiento."]
        ],
        checks: [
          "Las medidas y el nivel de la zapata coinciden con el plano.",
          "El acero está armado y sostenido para conservar su posición.",
          "No se añadirán piedras grandes ni materiales no previstos al concreto.",
          "Los arranques de columna están alineados y firmes."
        ]
      },
      {
        id: "vigas-cimentacion",
        title: "Vigas de cimentación",
        subtitle: "El acero y los estribos deben seguir el detalle estructural.",
        blocks: [
          ["info", "Regla básica", "Las vigas de cimentación de concreto armado se ejecutan con agregados para concreto y el refuerzo indicado. No se rellenan con piedra grande para reducir el consumo de concreto."],
          ["warning", "Error frecuente", "No cambies por comodidad la posición de barras, empalmes, estribos o ganchos. Tampoco cortes acero para hacer pasar tuberías sin autorización del responsable estructural."],
          ["design", "Revisa el detalle", "La orientación de ganchos, separación de estribos, empalmes y zonas de mayor confinamiento debe respetar el plano. Si el detalle no es claro, consulta antes de armar o vaciar."]
        ],
        checks: [
          "La sección de la viga coincide con el plano.",
          "El número, diámetro y posición de las barras están verificados.",
          "Los estribos y sus ganchos siguen el detalle estructural.",
          "No existen tuberías atravesando o desplazando el acero sin revisión."
        ]
      },
      {
        id: "recubrimiento",
        title: "Recubrimiento y separadores",
        subtitle: "El acero no debe tocar el suelo ni el encofrado.",
        blocks: [
          ["info", "Qué debes revisar", "Usa separadores adecuados para mantener el acero en la posición prevista durante el vaciado. El recubrimiento protege el refuerzo y permite que el elemento trabaje como fue diseñado."],
          ["warning", "No uses cualquier objeto", "Evita apoyar el acero directamente sobre tierra, piedras sueltas, madera o desperdicios. Los apoyos improvisados pueden moverse, absorber agua o dejar recubrimientos irregulares."],
          ["design", "Medida del recubrimiento", "La distancia necesaria depende del elemento, la exposición y el detalle del proyecto. No la determines solo a ojo."]
        ],
        checks: [
          "El acero no toca el suelo ni las caras del encofrado.",
          "Los separadores son firmes y están distribuidos para evitar deformaciones.",
          "La armadura no se hundirá cuando ingresen trabajadores o concreto."
        ]
      },
      {
        id: "concreto-vaciado",
        title: "Concreto y vaciado",
        subtitle: "Coordina mezcla, colocación, vibrado y curado antes de empezar.",
        blocks: [
          ["info", "Antes del vaciado", "Confirma resistencia especificada, volumen, acceso, equipo de compactación, personal, protección y método de curado. Humedecer no significa dejar agua empozada en el fondo."],
          ["warning", "No corrijas con agua", "No agregues agua de manera improvisada para volver más fluido el concreto. Los cambios de consistencia y dosificación deben controlarse técnicamente."],
          ["design", "Durante y después", "Coloca y compacta el concreto evitando segregación y vacíos. Inicia el curado oportunamente y protege los arranques y superficies expuestas."]
        ],
        checks: [
          "El concreto corresponde a la resistencia especificada.",
          "Está listo el equipo de compactación y hay acceso continuo para vaciar.",
          "No se agregará agua ni piedra grande para rendir la mezcla.",
          "El método y duración de curado están definidos antes de vaciar."
        ]
      },
      {
        id: "ladera",
        title: "Cimentación en ladera",
        subtitle: "Excavar puede afectar el talud, vecinos y estructuras existentes.",
        blocks: [
          ["info", "Precaución adicional", "En una ladera deben revisarse estabilidad del terreno, drenaje, cortes, rellenos, niveles escalonados, contención y relación con las viviendas vecinas."],
          ["warning", "Alerta grave", "No socaves el pie de un talud ni dejes cortes altos sin sostenimiento. Grietas nuevas, desprendimientos, inclinaciones, filtraciones o movimientos obligan a detener el trabajo y evaluar."],
          ["design", "No es solo una zapata", "La solución puede requerir drenaje, contención, cimentaciones escalonadas u otras medidas. Debe diseñarse para el caso real, no resolverse únicamente aumentando concreto."]
        ],
        checks: [
          "Existe evaluación de estabilidad y drenaje para la ladera.",
          "La excavación no debilita el terreno ni cimentaciones vecinas.",
          "Los cortes cuentan con una secuencia y protección definida.",
          "Se controlan filtraciones y agua de lluvia antes de continuar."
        ]
      }
    ]
  },
  problemas: {
    eyebrow: "Primero la seguridad",
    title: "Tengo un problema en obra",
    intro: "Estas señales no permiten diagnosticar por sí solas, pero ayudan a reconocer cuándo debes detener una actividad y solicitar una revisión profesional.",
    topics: [
      {
        id: "detener",
        title: "Cuándo detener el trabajo",
        subtitle: "No cubras ni continúes hasta saber qué ocurre.",
        blocks: [
          ["warning", "Detén y protege el área", "Hazlo si observas desplazamiento de tierra, derrumbe parcial, grietas que crecen, columnas o muros inclinados, deformaciones importantes, acero cortado, elementos diferentes al plano o daños producidos durante una excavación."],
          ["info", "Registra la situación", "Toma fotografías generales y cercanas, anota fecha, ubicación, etapa y qué actividad se realizaba. No pongas personas en riesgo para obtener imágenes."],
          ["design", "Siguiente paso", "Evita tapar, tarrajear, rellenar o vaciar encima del problema hasta que se defina una medida técnica."]
        ],
        checks: [
          "La actividad riesgosa está detenida y el área protegida.",
          "Registré fotos seguras, ubicación y momento en que apareció.",
          "No oculté el problema con concreto, relleno o acabado.",
          "Contacté al responsable técnico o solicité una evaluación."
        ]
      },
      {
        id: "consulta-fotos",
        title: "Qué enviar para una consulta",
        subtitle: "Información clara permite definir si el caso puede revisarse a distancia.",
        blocks: [
          ["info", "Envía primero", "Incluye una vista general, acercamientos, una referencia de tamaño, ubicación de la vivienda, número de pisos, etapa de obra, planos disponibles y una descripción breve de lo ocurrido."],
          ["warning", "Limitación importante", "Una fotografía no permite comprobar todo lo que existe dentro del elemento ni las condiciones completas del suelo. Algunos casos requieren visita, medición, ensayo o cálculo."],
          ["design", "No alteres la evidencia", "No piques, cortes, retires acero ni apliques productos antes de recibir indicaciones, salvo una acción inmediata necesaria para proteger a las personas."]
        ],
        checks: [
          "Tengo fotos generales y cercanas con buena iluminación.",
          "Indiqué la ubicación, etapa, número de pisos y duda principal.",
          "Adjunté planos o antecedentes disponibles.",
          "No realicé reparaciones improvisadas antes de la revisión."
        ]
      }
    ]
  }
};

const stageSection = document.querySelector(".stage-section");
const quickDiagnostic = document.querySelector(".quick-diagnostic");
const moduleView = document.getElementById("moduleView");
const moduleContent = document.getElementById("moduleContent");
const completedCount = document.getElementById("completedCount");
const diagnosticDialog = document.getElementById("diagnosticDialog");
const diagnosticForm = document.getElementById("diagnosticForm");
const diagnosticResult = document.getElementById("diagnosticResult");

const getProgress = () => {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
  } catch {
    return {};
  }
};

const saveProgress = (progress) => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
  updateProgressSummary();
};

const updateProgressSummary = () => {
  const progress = getProgress();
  completedCount.textContent = Object.values(progress).filter(Boolean).length;
};

const blockClass = (type) => `${type}-block`;

const renderModule = (moduleId) => {
  const module = modules[moduleId];
  if (!module) return;
  const progress = getProgress();

  moduleContent.innerHTML = `
    <article class="module-shell">
      <header class="module-hero">
        <p class="eyebrow">${module.eyebrow}</p>
        <h1>${module.title}</h1>
        <p>${module.intro}</p>
      </header>
      <div class="topic-list">
        ${module.topics.map((topic, index) => `
          <article class="topic-card${index === 0 ? " open" : ""}">
            <button class="topic-toggle" type="button" aria-expanded="${index === 0}">
              <strong>${topic.title}<small>${topic.subtitle}</small></strong><span>+</span>
            </button>
            <div class="topic-content">
              ${topic.blocks.map(([type, title, text]) => `
                <div class="${blockClass(type)}"><strong>${title}</strong><p>${text}</p></div>
              `).join("")}
              <div class="checklist" aria-label="Lista de verificación de ${topic.title}">
                ${topic.checks.map((check, checkIndex) => {
                  const key = `${moduleId}:${topic.id}:${checkIndex}`;
                  return `<label class="check-item"><input type="checkbox" data-progress-key="${key}" ${progress[key] ? "checked" : ""}><span>${check}</span></label>`;
                }).join("")}
              </div>
            </div>
          </article>
        `).join("")}
      </div>
    </article>`;

  stageSection.hidden = true;
  quickDiagnostic.hidden = true;
  moduleView.hidden = false;
  window.scrollTo({ top: 0, behavior: "smooth" });

  moduleContent.querySelectorAll(".topic-toggle").forEach((button) => {
    button.addEventListener("click", () => {
      const card = button.closest(".topic-card");
      const isOpen = card.classList.toggle("open");
      button.setAttribute("aria-expanded", String(isOpen));
    });
  });

  moduleContent.querySelectorAll("[data-progress-key]").forEach((input) => {
    input.addEventListener("change", () => {
      const next = getProgress();
      next[input.dataset.progressKey] = input.checked;
      saveProgress(next);
    });
  });
};

document.querySelectorAll("[data-module]").forEach((button) => {
  button.addEventListener("click", () => renderModule(button.dataset.module));
});

document.getElementById("closeModule").addEventListener("click", () => {
  moduleView.hidden = true;
  stageSection.hidden = false;
  quickDiagnostic.hidden = false;
  window.scrollTo({ top: 0, behavior: "smooth" });
});

document.getElementById("resetProgress").addEventListener("click", () => {
  if (window.confirm("¿Deseas borrar todas las listas marcadas en la aplicación?")) {
    localStorage.removeItem(STORAGE_KEY);
    updateProgressSummary();
  }
});

document.getElementById("shareApp").addEventListener("click", async () => {
  const shareData = {
    title: "Construcción Segura",
    text: "Guía práctica para revisar la construcción de tu vivienda.",
    url: "https://www.construccionsegura.org.pe/app/"
  };

  try {
    if (navigator.share) {
      await navigator.share(shareData);
    } else {
      await navigator.clipboard.writeText(shareData.url);
      window.alert("Enlace copiado para compartir.");
    }
  } catch (error) {
    if (error?.name !== "AbortError") window.alert("No se pudo compartir en este momento.");
  }
});

document.getElementById("openDiagnostic").addEventListener("click", () => {
  diagnosticResult.hidden = true;
  diagnosticDialog.showModal();
});

diagnosticForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const data = new FormData(diagnosticForm);
  const terrain = data.get("terrain");
  const floors = data.get("floors");
  const soil = data.get("soil");
  const plans = data.get("plans");

  const alerts = [];
  if (terrain === "slope") alerts.push("Por estar en ladera, revisa estabilidad, drenaje, cortes, contención y efecto sobre las viviendas vecinas antes de excavar.");
  if (terrain === "fill") alerts.push("Un terreno con relleno necesita identificar su espesor, composición y compactación; no asumas que puede recibir una cimentación convencional.");
  if (terrain === "unknown") alerts.push("Antes de definir cimentaciones, identifica si existe relleno, humedad, pendiente, suelo removido o antecedentes de deslizamiento.");
  if (floors === "3plus") alerts.push("Para tres pisos o más, evita cualquier decisión basada solo en experiencia empírica o medidas copiadas de otra vivienda.");
  if (soil === "no") alerts.push("Obtén información geotécnica apropiada para el proyecto antes de fijar tipo, tamaño y profundidad de cimentación.");
  if (plans === "no") alerts.push("No compres ni armes acero estructural sin planos que definan dimensiones, refuerzos, empalmes, recubrimientos y resistencia del concreto.");
  if (!alerts.length) alerts.push("Tienes una base inicial favorable. Aun así, verifica que estudio, planos, terreno y ejecución coincidan antes de cada etapa.");

  diagnosticResult.innerHTML = `<h3>Recomendaciones iniciales</h3><ul>${alerts.map((item) => `<li>${item}</li>`).join("")}</ul><p><strong>Importante:</strong> este diagnóstico es orientativo y no reemplaza una evaluación del terreno ni el diseño estructural.</p>`;
  diagnosticResult.hidden = false;
});

updateProgressSummary();
