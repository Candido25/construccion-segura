(() => {
  const diagnostic = document.querySelector(".quick-diagnostic");
  if (!diagnostic) return;

  const problems = [
    {
      id: "grietas",
      title: "Grietas, fisuras o deformaciones",
      summary: "Rajaduras nuevas, desniveles, elementos que se doblan o partes que se desprenden.",
      baseRisk: "yellow",
      immediate: "No tapes ni resanes la grieta antes de registrar su ubicación y evolución.",
      questions: [
        { id: "growth", text: "¿La grieta está creciendo, se abrió rápidamente o reapareció después de repararla?", yesRisk: "red" },
        { id: "structural", text: "¿Atraviesa una columna, viga, muro portante o losa, o existe desnivel entre sus lados?", yesRisk: "red" },
        { id: "deformation", text: "¿Hay hundimiento, inclinación, deformación o desprendimiento de concreto o ladrillo?", yesRisk: "red" },
        { id: "event", text: "¿Apareció después de un sismo, excavación vecina, sobrecarga o ampliación?", yesRisk: "yellow" }
      ]
    },
    {
      id: "terreno",
      title: "Hundimiento, terreno o ladera",
      summary: "Suelo que baja, grietas en el terreno, taludes, rellenos o excavaciones inestables.",
      baseRisk: "yellow",
      immediate: "Aleja a las personas del borde de excavaciones, cortes y zonas con movimiento.",
      questions: [
        { id: "movement", text: "¿El terreno se está moviendo, desprendiendo o hundiendo en este momento?", yesRisk: "red" },
        { id: "affected", text: "¿Hay muros inclinados, puertas trabadas o viviendas vecinas afectadas?", yesRisk: "red" },
        { id: "water", text: "¿Apareció agua, filtración o barro dentro de la excavación o del talud?", yesRisk: "yellow" },
        { id: "fill", text: "¿La construcción está sobre relleno o suelo removido sin evaluación conocida?", yesRisk: "yellow" }
      ]
    },
    {
      id: "estructura-intervenida",
      title: "Cortaron una viga, columna, muro o acero",
      summary: "Perforaciones, demoliciones o cortes realizados para abrir vanos o pasar tuberías.",
      baseRisk: "red",
      immediate: "Detén la intervención y evita cargar o golpear el elemento afectado.",
      questions: [
        { id: "cut", text: "¿Se cortó acero, concreto, una columna, una viga o un muro que podría ser estructural?", yesRisk: "red" },
        { id: "plan", text: "¿El cambio se hizo sin plano, detalle o autorización del responsable estructural?", yesRisk: "red" },
        { id: "crack", text: "¿Aparecieron grietas, ruidos, deformaciones o desprendimientos después del trabajo?", yesRisk: "red" }
      ]
    },
    {
      id: "electricidad",
      title: "Problema eléctrico",
      summary: "Chispas, olor a quemado, tomacorrientes calientes o llaves que se disparan.",
      baseRisk: "yellow",
      immediate: "No toques partes metálicas ni improvises puentes en el tablero.",
      questions: [
        { id: "shock", text: "¿Alguien recibió una descarga o hay partes energizadas expuestas?", yesRisk: "red" },
        { id: "burn", text: "¿Hay chispas, humo, olor a quemado o calentamiento intenso?", yesRisk: "red" },
        { id: "trip", text: "¿La protección se dispara repetidamente o vuelve a dispararse al reconectarla?", yesRisk: "yellow" },
        { id: "wet", text: "¿La humedad o una fuga de agua está cerca de cables, tablero o tomacorrientes?", yesRisk: "red" }
      ]
    },
    {
      id: "gas",
      title: "Olor a gas o combustión deficiente",
      summary: "Olor a GLP o gas, llama inusual, hollín o mareos cerca de un artefacto.",
      baseRisk: "red",
      immediate: "No enciendas ni apagues interruptores, no uses fuego y sal del área. Cierra la válvula solo si puedes hacerlo sin exponerte y contacta al proveedor o servicio de emergencia correspondiente.",
      questions: [
        { id: "odor", text: "¿Percibes olor a gas o escuchas una fuga?", yesRisk: "red" },
        { id: "symptoms", text: "¿Hay mareos, dolor de cabeza, somnolencia o dificultad para respirar?", yesRisk: "red" },
        { id: "flame", text: "¿La llama es amarilla, hay hollín o el ambiente tiene poca ventilación?", yesRisk: "red" }
      ]
    },
    {
      id: "desague",
      title: "Retorno, atoros u olor de desagüe",
      summary: "Aguas residuales que regresan, varios aparatos lentos o malos olores persistentes.",
      baseRisk: "yellow",
      immediate: "Evita el contacto con aguas residuales y no viertas ácidos o mezclas químicas improvisadas.",
      questions: [
        { id: "return", text: "¿Están retornando aguas residuales o inundando ambientes?", yesRisk: "red" },
        { id: "multiple", text: "¿El problema afecta a varios aparatos sanitarios al mismo tiempo?", yesRisk: "yellow" },
        { id: "leak", text: "¿Hay filtración oculta, humedad en losas o paredes, o tuberías rotas?", yesRisk: "yellow" },
        { id: "vent", text: "¿La ventilación sanitaria fue tapada, cortada o nunca llegó al exterior?", yesRisk: "yellow" }
      ]
    },
    {
      id: "humedad",
      title: "Humedad, filtración o salitre",
      summary: "Pintura inflada, polvo blanco, moho, goteo o humedad que reaparece.",
      baseRisk: "yellow",
      immediate: "Identifica y controla la entrada de agua antes de pintar, sellar o tarrajear nuevamente.",
      questions: [
        { id: "electric", text: "¿La humedad está en contacto con instalaciones eléctricas?", yesRisk: "red" },
        { id: "structural", text: "¿Hay acero expuesto, corrosión, desprendimiento o pérdida de material?", yesRisk: "red" },
        { id: "soil", text: "¿La humedad sube desde el suelo o aparece después de lluvias?", yesRisk: "yellow" },
        { id: "repeat", text: "¿Reapareció después de varias reparaciones o pinturas?", yesRisk: "yellow" }
      ]
    },
    {
      id: "concreto",
      title: "Concreto con vacíos, rajaduras o desprendimientos",
      summary: "Cangrejeras, polvo superficial, acero visible o concreto que se desprende.",
      baseRisk: "yellow",
      immediate: "No ocultes el defecto con mortero o acabado antes de determinar su extensión y causa.",
      questions: [
        { id: "steel", text: "¿Se ve acero, hay barras sueltas o recubrimiento desprendido?", yesRisk: "red" },
        { id: "deform", text: "¿El elemento está deformado, inclinado o soporta carga en este momento?", yesRisk: "red" },
        { id: "deep", text: "¿Los vacíos son profundos, continuos o atraviesan gran parte de la sección?", yesRisk: "red" },
        { id: "surface", text: "¿El problema parece superficial pero se extiende por varias zonas?", yesRisk: "yellow" }
      ]
    }
  ];

  const riskRank = { green: 0, yellow: 1, red: 2 };
  const riskCopy = {
    green: {
      title: "Orientación preventiva",
      message: "No aparecen señales críticas en estas respuestas. Revisa el punto y observa si cambia antes de continuar."
    },
    yellow: {
      title: "Revisa antes de continuar",
      message: "Existe al menos una condición que debe comprobarse en la obra, en los planos o con una persona competente."
    },
    red: {
      title: "Detén y solicita evaluación",
      message: "Las respuestas indican una condición que puede comprometer la seguridad. Protege el área y no continúes hasta contar con evaluación."
    }
  };

  const section = document.createElement("section");
  section.className = "problem-evaluator-section";
  section.id = "problemas-evaluador";
  section.setAttribute("aria-labelledby", "problem-evaluator-title");
  section.innerHTML = `
    <div class="problem-evaluator-heading">
      <div>
        <p class="eyebrow">Evaluador de señales</p>
        <h2 id="problem-evaluator-title">Tengo un problema en mi obra</h2>
        <p>Selecciona lo que observas y responde preguntas breves. La herramienta no diagnostica: te ayuda a decidir si debes revisar o detener.</p>
      </div>
      <span class="problem-evaluator-note">Sin registro · Sin cuenta</span>
    </div>
    <div class="problem-evaluator-grid">
      ${problems.map((problem) => `
        <button type="button" class="problem-evaluator-card" data-problem-id="${problem.id}">
          <span class="problem-evaluator-symbol" aria-hidden="true">!</span>
          <span><strong>${problem.title}</strong><small>${problem.summary}</small></span>
          <span class="problem-evaluator-arrow" aria-hidden="true">›</span>
        </button>
      `).join("")}
    </div>
  `;
  diagnostic.insertAdjacentElement("afterend", section);

  const dialog = document.createElement("dialog");
  dialog.className = "problem-evaluator-dialog";
  dialog.id = "problemEvaluatorDialog";
  dialog.innerHTML = `
    <form id="problemEvaluatorForm">
      <div class="problem-dialog-heading">
        <div>
          <p class="eyebrow">Evaluación orientativa</p>
          <h2 id="problemDialogTitle">Problema en obra</h2>
          <p id="problemDialogSummary"></p>
        </div>
        <button class="icon-button" type="button" data-close-problem aria-label="Cerrar">×</button>
      </div>
      <div id="problemQuestions" class="problem-question-list"></div>
      <div class="problem-evaluator-actions">
        <button type="button" class="problem-secondary-button" data-close-problem>Cancelar</button>
        <button type="submit" class="primary-button">Evaluar señales</button>
      </div>
      <div id="problemResult" class="problem-result" hidden aria-live="polite"></div>
    </form>
  `;
  document.body.append(dialog);

  const form = dialog.querySelector("#problemEvaluatorForm");
  const title = dialog.querySelector("#problemDialogTitle");
  const summary = dialog.querySelector("#problemDialogSummary");
  const questions = dialog.querySelector("#problemQuestions");
  const result = dialog.querySelector("#problemResult");
  let activeProblem = null;

  const openProblem = (problem) => {
    activeProblem = problem;
    title.textContent = problem.title;
    summary.textContent = problem.summary;
    result.hidden = true;
    result.innerHTML = "";
    questions.innerHTML = problem.questions.map((question, index) => `
      <fieldset class="problem-question">
        <legend>${index + 1}. ${question.text}</legend>
        <label><input type="radio" name="${question.id}" value="yes" required> Sí</label>
        <label><input type="radio" name="${question.id}" value="no"> No</label>
        <label><input type="radio" name="${question.id}" value="unknown"> No estoy seguro</label>
      </fieldset>
    `).join("");

    if (typeof dialog.showModal === "function") {
      dialog.showModal();
    } else {
      dialog.setAttribute("open", "");
    }
  };

  const evaluate = () => {
    let risk = activeProblem.baseRisk;
    const uncertain = [];

    activeProblem.questions.forEach((question) => {
      const value = form.elements.namedItem(question.id)?.value;
      if (value === "yes" && riskRank[question.yesRisk] > riskRank[risk]) {
        risk = question.yesRisk;
      }
      if (value === "unknown") uncertain.push(question.text);
    });

    if (uncertain.length && riskRank[risk] < riskRank.yellow) risk = "yellow";
    return { risk, uncertain };
  };

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!activeProblem || !form.reportValidity()) return;

    const evaluation = evaluate();
    const copy = riskCopy[evaluation.risk];
    const contactLabel = evaluation.risk === "red"
      ? "Solicitar evaluación profesional"
      : "Solicitar orientación profesional";

    result.dataset.risk = evaluation.risk;
    result.innerHTML = `
      <div class="problem-result-title">
        <span class="problem-result-light" aria-hidden="true"></span>
        <div><strong>${copy.title}</strong><p>${copy.message}</p></div>
      </div>
      <div class="problem-result-immediate"><strong>Acción inmediata</strong><p>${activeProblem.immediate}</p></div>
      ${evaluation.uncertain.length ? `<p class="problem-result-uncertain"><strong>Dato pendiente:</strong> marcaste “No estoy seguro” en ${evaluation.uncertain.length} respuesta(s). Eso justifica revisar antes de continuar.</p>` : ""}
      <p class="problem-result-disclaimer">Este resultado es orientativo y no confirma la causa ni la seguridad de la edificación.</p>
      ${evaluation.risk === "green" ? "" : `<a class="primary-button problem-contact" href="/contacto.html?origen=mi-casa-segura&nivel=${evaluation.risk}&consulta=${encodeURIComponent(activeProblem.title)}">${contactLabel}</a>`}
    `;
    result.hidden = false;
    result.scrollIntoView({ behavior: "smooth", block: "nearest" });
  });

  section.addEventListener("click", (event) => {
    const button = event.target.closest("[data-problem-id]");
    if (!button) return;
    const problem = problems.find((item) => item.id === button.dataset.problemId);
    if (problem) openProblem(problem);
  });

  dialog.querySelectorAll("[data-close-problem]").forEach((button) => {
    button.addEventListener("click", () => dialog.close());
  });

  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) dialog.close();
  });
})();
