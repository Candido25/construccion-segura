(() => {
  const PROFILE_KEY = "mi-casa-segura-work-profile-v1";
  const routeButtons = document.querySelectorAll("[data-app-route]");
  const faqSection = document.getElementById("dudas");
  const faqInput = document.getElementById("faqSearch");
  const stageSection = document.querySelector(".stage-section");
  const problemButton = document.querySelector('[data-module="problemas"]');
  const faqAnswer = document.getElementById("faqAnswer");
  const welcomeCard = document.querySelector(".welcome-card");
  const choiceSection = document.querySelector(".app-choice-section");
  const helpCard = document.querySelector(".help-card");
  const bottomNav = document.querySelector(".bottom-nav");

  if (welcomeCard) welcomeCard.id = "inicio";
  if (stageSection && !stageSection.id) stageSection.id = "guia-etapas";
  if (helpCard) helpCard.id = "ayuda";

  const scrollToElement = (element) => element?.scrollIntoView({ behavior: "smooth", block: "start" });

  const readProfile = () => {
    try {
      const stored = localStorage.getItem(PROFILE_KEY);
      return stored ? JSON.parse(stored) : null;
    } catch (error) {
      console.warn("No se pudo leer el perfil de la obra.", error);
      return null;
    }
  };

  const saveProfile = (profile) => localStorage.setItem(PROFILE_KEY, JSON.stringify(profile));

  const profileSection = document.createElement("section");
  profileSection.className = "work-profile-card";
  profileSection.id = "mi-obra";
  profileSection.setAttribute("aria-labelledby", "work-profile-title");
  profileSection.innerHTML = `
    <div class="work-profile-heading">
      <div>
        <p class="eyebrow">Mi obra</p>
        <h2 id="work-profile-title">Configura los datos básicos de tu proyecto</h2>
        <p id="workProfileIntro">La aplicación guardará estos datos únicamente en este dispositivo para mostrarte advertencias más pertinentes.</p>
      </div>
      <button class="primary-button" type="button" data-open-work-profile>Configurar mi obra</button>
    </div>
    <div class="work-profile-summary" id="workProfileSummary" aria-live="polite">
      <div class="work-profile-empty">
        <strong>Aún no has configurado tu obra.</strong>
        <span>Registra el tipo de trabajo, terreno, pisos y documentos disponibles.</span>
      </div>
    </div>`;
  choiceSection?.insertAdjacentElement("afterend", profileSection);

  const profileDialog = document.createElement("dialog");
  profileDialog.className = "work-profile-dialog";
  profileDialog.id = "workProfileDialog";
  profileDialog.innerHTML = `
    <form id="workProfileForm">
      <div class="work-profile-dialog-heading">
        <div><p class="eyebrow">Perfil local</p><h2>Cuéntanos sobre tu obra</h2><p>Estos datos se almacenan en tu dispositivo. No necesitas crear una cuenta.</p></div>
        <button class="icon-button" type="button" data-close-work-profile aria-label="Cerrar">×</button>
      </div>
      <div class="work-profile-form-grid">
        <label class="work-profile-field work-profile-field-wide"><span>Nombre de la obra <small>(opcional)</small></span><input name="workName" type="text" maxlength="60" placeholder="Ejemplo: Casa familiar Huaycán"></label>
        <label class="work-profile-field"><span>Departamento</span><input name="department" type="text" maxlength="40" value="Lima" placeholder="Ejemplo: Lima"></label>
        <label class="work-profile-field"><span>Distrito</span><input name="district" type="text" maxlength="40" placeholder="Ejemplo: Ate"></label>
        <label class="work-profile-field"><span>¿Qué vas a realizar?</span><select name="projectType" required><option value="">Selecciona una opción</option><option value="nueva">Construcción nueva</option><option value="ampliacion">Ampliación</option><option value="remodelacion">Remodelación</option><option value="mantenimiento">Reparación o mantenimiento</option></select></label>
        <label class="work-profile-field"><span>¿Cómo es el terreno?</span><select name="terrain" required><option value="">Selecciona una opción</option><option value="flat">Plano o aparentemente firme</option><option value="slope">En ladera o falda de cerro</option><option value="fill">Con relleno o suelo removido</option><option value="unknown">No estoy seguro</option></select></label>
        <label class="work-profile-field"><span>Pisos actuales</span><select name="currentFloors" required><option value="0">Ninguno, recién construiré</option><option value="1">Un piso</option><option value="2">Dos pisos</option><option value="3plus">Tres pisos o más</option></select></label>
        <label class="work-profile-field"><span>Pisos proyectados</span><select name="plannedFloors" required><option value="">Selecciona una opción</option><option value="1">Un piso</option><option value="2">Dos pisos</option><option value="3plus">Tres pisos o más</option></select></label>
        <label class="work-profile-field work-profile-field-wide"><span>Etapa actual</span><select name="stage" required><option value="">Selecciona una opción</option><option value="planning">Planificación, estudios o planos</option><option value="excavation">Excavación y movimiento de tierras</option><option value="foundations">Cimentaciones</option><option value="structure">Columnas, muros, vigas o techos</option><option value="installations">Instalaciones</option><option value="finishes">Acabados</option><option value="maintenance">Vivienda terminada o mantenimiento</option></select></label>
        <label class="work-profile-field"><span>Estudio de suelos</span><select name="soilStudy" required><option value="">Selecciona</option><option value="yes">Sí tengo</option><option value="no">No tengo</option><option value="unknown">No estoy seguro</option></select></label>
        <label class="work-profile-field"><span>Planos estructurales</span><select name="structuralPlans" required><option value="">Selecciona</option><option value="yes">Sí tengo</option><option value="no">No tengo</option><option value="unknown">No estoy seguro</option></select></label>
        <label class="work-profile-field work-profile-field-wide"><span>Licencia o trámite municipal</span><select name="municipalLicense" required><option value="">Selecciona una opción</option><option value="yes">Sí, cuento con licencia</option><option value="processing">Está en trámite</option><option value="no">No tengo</option><option value="unknown">No estoy seguro</option></select></label>
      </div>
      <div class="work-profile-privacy"><strong>Privacidad:</strong> este perfil se guarda localmente y no se envía a Construcción Segura.</div>
      <div class="work-profile-actions"><button class="work-profile-delete" id="deleteWorkProfile" type="button" hidden>Eliminar perfil</button><button class="primary-button" type="submit">Guardar mi obra</button></div>
    </form>`;
  document.body.append(profileDialog);

  if (bottomNav) {
    bottomNav.innerHTML = `
      <a class="active" href="#inicio" data-nav-target="inicio"><span>⌂</span>Inicio</a>
      <a href="#guia-etapas" data-nav-target="guia-etapas"><span>☷</span>Guía</a>
      <a href="#dudas" data-nav-target="dudas"><span>⌕</span>Consultar</a>
      <button type="button" data-open-work-profile><span>▣</span>Mi obra</button>
      <a href="#ayuda" data-nav-target="ayuda"><span>?</span>Ayuda</a>`;
  }

  const profileForm = profileDialog.querySelector("#workProfileForm");
  const profileSummary = profileSection.querySelector("#workProfileSummary");
  const profileTitle = profileSection.querySelector("#work-profile-title");
  const profileIntro = profileSection.querySelector("#workProfileIntro");
  const deleteProfileButton = profileDialog.querySelector("#deleteWorkProfile");
  let continueToGuideAfterSave = false;

  const labels = {
    projectType: { nueva: "Construcción nueva", ampliacion: "Ampliación", remodelacion: "Remodelación", mantenimiento: "Reparación o mantenimiento" },
    terrain: { flat: "Terreno plano", slope: "Terreno en ladera", fill: "Terreno con relleno", unknown: "Terreno sin identificar" },
    floors: { "0": "Sin pisos construidos", "1": "1 piso", "2": "2 pisos", "3plus": "3 pisos o más" },
    stage: { planning: "Planificación y planos", excavation: "Excavación", foundations: "Cimentaciones", structure: "Estructura", installations: "Instalaciones", finishes: "Acabados", maintenance: "Mantenimiento" }
  };

  const buildProfileWarnings = (profile) => {
    const warnings = [];
    if (["slope", "fill"].includes(profile.terrain)) warnings.push("El terreno declarado requiere atención especial antes de excavar o definir la cimentación.");
    if (profile.plannedFloors === "3plus" && profile.structuralPlans !== "yes") warnings.push("Proyectas tres pisos o más y no has confirmado planos estructurales. No compres ni armes acero antes de definir el proyecto completo.");
    else if (["nueva", "ampliacion", "remodelacion"].includes(profile.projectType) && profile.structuralPlans !== "yes") warnings.push("Antes de intervenir elementos estructurales, confirma que cuentas con planos y revisión profesional.");
    if (profile.soilStudy !== "yes" && ["nueva", "ampliacion"].includes(profile.projectType)) warnings.push("No has confirmado un estudio de suelos. La cimentación no debe definirse copiando otra vivienda.");
    if (["no", "unknown"].includes(profile.municipalLicense)) warnings.push("Revisa el trámite municipal aplicable antes de iniciar o continuar trabajos que requieran autorización.");
    return warnings;
  };

  const renderProfile = (profile) => {
    if (!profile) {
      profileTitle.textContent = "Configura los datos básicos de tu proyecto";
      profileIntro.textContent = "La aplicación guardará estos datos únicamente en este dispositivo para mostrarte advertencias más pertinentes.";
      profileSummary.innerHTML = '<div class="work-profile-empty"><strong>Aún no has configurado tu obra.</strong><span>Registra el tipo de trabajo, terreno, pisos y documentos disponibles.</span></div>';
      profileSection.querySelector("[data-open-work-profile]").textContent = "Configurar mi obra";
      deleteProfileButton.hidden = true;
      return;
    }

    const location = [profile.district, profile.department].filter(Boolean).join(", ") || "Ubicación no indicada";
    const warnings = buildProfileWarnings(profile);
    const chips = [labels.projectType[profile.projectType], labels.terrain[profile.terrain], `${labels.floors[profile.currentFloors]} → ${labels.floors[profile.plannedFloors]}`, labels.stage[profile.stage]].filter(Boolean);
    profileTitle.textContent = profile.workName || "Mi obra";
    profileIntro.textContent = location;
    profileSummary.innerHTML = `<div class="work-profile-chips">${chips.map((chip) => `<span>${chip}</span>`).join("")}</div><div class="work-profile-alert ${warnings.length ? "is-warning" : "is-ready"}"><strong>${warnings.length ? "Recomendaciones iniciales" : "Perfil básico completo"}</strong>${warnings.length ? `<ul>${warnings.map((warning) => `<li>${warning}</li>`).join("")}</ul>` : "<p>Usaremos estos datos para ordenar la guía y mostrar advertencias relacionadas con tu proyecto.</p>"}</div>`;
    profileSection.querySelector("[data-open-work-profile]").textContent = "Editar mi obra";
    deleteProfileButton.hidden = false;
  };

  const populateForm = (profile) => {
    profileForm.reset();
    profileForm.elements.department.value = "Lima";
    if (!profile) return;
    Object.entries(profile).forEach(([key, value]) => {
      const field = profileForm.elements.namedItem(key);
      if (field) field.value = value;
    });
  };

  const openProfile = ({ continueToGuide = false } = {}) => {
    continueToGuideAfterSave = continueToGuide;
    populateForm(readProfile());
    profileDialog.showModal ? profileDialog.showModal() : profileDialog.setAttribute("open", "");
  };

  document.querySelectorAll("[data-open-work-profile]").forEach((button) => button.addEventListener("click", () => openProfile()));
  profileDialog.querySelector("[data-close-work-profile]").addEventListener("click", () => profileDialog.close());
  profileDialog.addEventListener("click", (event) => { if (event.target === profileDialog) profileDialog.close(); });

  profileForm.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!profileForm.reportValidity()) return;
    const data = Object.fromEntries(new FormData(profileForm).entries());
    data.updatedAt = new Date().toISOString();
    saveProfile(data);
    renderProfile(data);
    profileDialog.close();
    if (continueToGuideAfterSave) {
      continueToGuideAfterSave = false;
      setTimeout(() => scrollToElement(stageSection), 200);
    }
  });

  deleteProfileButton.addEventListener("click", () => {
    if (!confirm("¿Deseas eliminar los datos guardados de esta obra en este dispositivo?")) return;
    localStorage.removeItem(PROFILE_KEY);
    renderProfile(null);
    profileDialog.close();
  });

  routeButtons.forEach((button) => button.addEventListener("click", () => {
    const route = button.dataset.appRoute;
    if (route === "construir") readProfile() ? scrollToElement(stageSection) : openProfile({ continueToGuide: true });
    if (route === "duda") { scrollToElement(faqSection); setTimeout(() => faqInput?.focus(), 450); }
    if (route === "problema") problemButton ? problemButton.click() : scrollToElement(stageSection);
  }));

  bottomNav?.querySelectorAll("[data-nav-target]").forEach((link) => link.addEventListener("click", (event) => {
    const target = document.getElementById(link.dataset.navTarget);
    if (!target) return;
    event.preventDefault();
    bottomNav.querySelectorAll("a, button").forEach((item) => item.classList.remove("active"));
    link.classList.add("active");
    scrollToElement(target);
    if (link.dataset.navTarget === "dudas") setTimeout(() => faqInput?.focus(), 450);
  }));

  renderProfile(readProfile());

  const faqRiskByQuestion = new Map([
    ["¿A qué profundidad deben ir las zapatas?", ["yellow", "el_plano_manda", "2026-07-27"]],
    ["¿Realmente necesito un estudio de suelos para construir mi casa?", ["yellow", "recomendacion_practica", "2026-07-27"]],
    ["¿Puedo construir un piso más sobre mi vivienda?", ["red", "el_plano_manda", "2026-07-27"]],
    ["¿A los cuántos días puedo retirar el encofrado y los puntales?", ["yellow", "el_plano_manda", "2026-07-27"]],
    ["¿Cómo debo curar el concreto después del vaciado?", ["green", "minimo_rne", "2026-07-27"]],
    ["El techo recién vaciado tiene pequeñas rajaduras. ¿Es grave?", ["yellow", "criterio_tecnico_revisado", "2026-07-27"]],
    ["¿La misma mezcla sirve para pegar ladrillos y para tarrajear?", ["yellow", "minimo_rne", "2026-07-27"]],
    ["La pintura se infla y aparece un polvo blanco. ¿Cómo elimino el salitre?", ["yellow", "criterio_tecnico_revisado", "2026-07-27"]],
    ["¿Es lo mismo una llave termomagnética que un interruptor diferencial?", ["green", "minimo_rne", "2026-07-27"]],
    ["¿Qué calibre de cable debo comprar para luces o tomacorrientes?", ["yellow", "el_plano_manda", "2026-07-27"]],
    ["¿Qué pendiente debe tener la tubería de desagüe?", ["green", "minimo_rne", "2026-07-27"]],
    ["El desagüe baja lento, hace ‘glup glup’ o huele mal. ¿Qué puede ser?", ["yellow", "criterio_tecnico_revisado", "2026-07-27"]],
    ["¿Se puede echar piedra grande dentro de una zapata para ahorrar concreto?", ["red", "prohibicion", "2026-07-27"]],
    ["¿Cómo evito pagar de más o quedar con la obra abandonada?", ["green", "recomendacion_practica", "2026-07-27"]]
  ]);

  const riskContent = {
    green: { title: "Orientación preventiva", text: "Puedes usar esta respuesta como guía para revisar y preguntar antes de ejecutar." },
    yellow: { title: "Revisa antes de continuar", text: "No avances hasta comprobar este punto en planos, mediciones, condiciones reales o con una persona competente." },
    red: { title: "Detén y solicita evaluación", text: "Esta situación puede comprometer la seguridad. No ocultes el problema ni continúes hasta contar con una revisión profesional." }
  };

  const classificationLabels = {
    minimo_rne: "Mínimo RNE",
    recomendacion_practica: "Recomendación práctica",
    el_plano_manda: "El plano manda",
    criterio_tecnico_revisado: "Criterio técnico revisado",
    prohibicion: "Prohibición"
  };

  const enhanceAnswer = () => {
    if (!faqAnswer || faqAnswer.hidden || !faqAnswer.textContent.trim()) return;
    faqAnswer.querySelectorAll(".faq-risk-panel, .faq-editorial-meta, .faq-professional-cta").forEach((node) => node.remove());
    const question = faqAnswer.querySelector("h3")?.textContent.trim() || "";
    const [risk, classification, reviewed] = faqRiskByQuestion.get(question) || ["yellow", "criterio_tecnico_revisado", "Pendiente de revisión individual"];
    const content = riskContent[risk];
    const panel = document.createElement("div");
    panel.className = "faq-risk-panel";
    panel.dataset.risk = risk;
    panel.setAttribute("role", "note");
    panel.innerHTML = `<span class="faq-risk-light" aria-hidden="true"></span><span class="faq-risk-copy"><strong>${content.title}</strong><span>${content.text}</span></span>`;
    const category = faqAnswer.querySelector(".faq-answer-category");
    category ? category.insertAdjacentElement("afterend", panel) : faqAnswer.prepend(panel);

    const meta = document.createElement("p");
    meta.className = "faq-editorial-meta";
    meta.innerHTML = `<strong>${classificationLabels[classification] || "Contenido revisado"}</strong> · Revisión: ${reviewed}`;
    faqAnswer.append(meta);

    if (["yellow", "red"].includes(risk)) {
      const cta = document.createElement("a");
      cta.className = "faq-professional-cta";
      cta.href = `/contacto.html?origen=mi-casa-segura&nivel=${risk}`;
      cta.textContent = risk === "red" ? "Solicitar evaluación profesional" : "Solicitar orientación profesional";
      faqAnswer.append(cta);
    }
  };

  if (faqAnswer) new MutationObserver(enhanceAnswer).observe(faqAnswer, { childList: true, subtree: true, attributes: true, attributeFilter: ["hidden"] });
})();