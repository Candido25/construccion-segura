(() => {
  const PROFILE_KEY = "mi-casa-segura-work-profile-v1";
  const choiceSection = document.querySelector(".app-choice-section");
  if (!choiceSection) return;

  const readProfile = () => {
    try {
      const stored = window.localStorage.getItem(PROFILE_KEY);
      return stored ? JSON.parse(stored) : null;
    } catch (error) {
      console.warn("No se pudo leer el perfil de la obra.", error);
      return null;
    }
  };

  const saveProfile = (profile) => {
    window.localStorage.setItem(PROFILE_KEY, JSON.stringify(profile));
  };

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
    </div>
  `;
  choiceSection.insertAdjacentElement("afterend", profileSection);

  const profileDialog = document.createElement("dialog");
  profileDialog.className = "work-profile-dialog";
  profileDialog.id = "workProfileDialog";
  profileDialog.innerHTML = `
    <form id="workProfileForm">
      <div class="work-profile-dialog-heading">
        <div>
          <p class="eyebrow">Perfil local</p>
          <h2>Cuéntanos sobre tu obra</h2>
          <p>Estos datos se almacenan en tu dispositivo. No necesitas crear una cuenta.</p>
        </div>
        <button class="icon-button" type="button" data-close-work-profile aria-label="Cerrar">×</button>
      </div>

      <div class="work-profile-form-grid">
        <label class="work-profile-field work-profile-field-wide">
          <span>Nombre de la obra <small>(opcional)</small></span>
          <input name="workName" type="text" maxlength="60" placeholder="Ejemplo: Casa familiar Huaycán">
        </label>

        <label class="work-profile-field">
          <span>Departamento</span>
          <input name="department" type="text" maxlength="40" value="Lima" placeholder="Ejemplo: Lima">
        </label>

        <label class="work-profile-field">
          <span>Distrito</span>
          <input name="district" type="text" maxlength="40" placeholder="Ejemplo: Ate">
        </label>

        <label class="work-profile-field">
          <span>¿Qué vas a realizar?</span>
          <select name="projectType" required>
            <option value="">Selecciona una opción</option>
            <option value="nueva">Construcción nueva</option>
            <option value="ampliacion">Ampliación</option>
            <option value="remodelacion">Remodelación</option>
            <option value="mantenimiento">Reparación o mantenimiento</option>
          </select>
        </label>

        <label class="work-profile-field">
          <span>¿Cómo es el terreno?</span>
          <select name="terrain" required>
            <option value="">Selecciona una opción</option>
            <option value="flat">Plano o aparentemente firme</option>
            <option value="slope">En ladera o falda de cerro</option>
            <option value="fill">Con relleno o suelo removido</option>
            <option value="unknown">No estoy seguro</option>
          </select>
        </label>

        <label class="work-profile-field">
          <span>Pisos actuales</span>
          <select name="currentFloors" required>
            <option value="0">Ninguno, recién construiré</option>
            <option value="1">Un piso</option>
            <option value="2">Dos pisos</option>
            <option value="3plus">Tres pisos o más</option>
          </select>
        </label>

        <label class="work-profile-field">
          <span>Pisos proyectados</span>
          <select name="plannedFloors" required>
            <option value="">Selecciona una opción</option>
            <option value="1">Un piso</option>
            <option value="2">Dos pisos</option>
            <option value="3plus">Tres pisos o más</option>
          </select>
        </label>

        <label class="work-profile-field work-profile-field-wide">
          <span>Etapa actual</span>
          <select name="stage" required>
            <option value="">Selecciona una opción</option>
            <option value="planning">Planificación, estudios o planos</option>
            <option value="excavation">Excavación y movimiento de tierras</option>
            <option value="foundations">Cimentaciones</option>
            <option value="structure">Columnas, muros, vigas o techos</option>
            <option value="installations">Instalaciones</option>
            <option value="finishes">Acabados</option>
            <option value="maintenance">Vivienda terminada o mantenimiento</option>
          </select>
        </label>

        <label class="work-profile-field">
          <span>Estudio de suelos</span>
          <select name="soilStudy" required>
            <option value="">Selecciona</option>
            <option value="yes">Sí tengo</option>
            <option value="no">No tengo</option>
            <option value="unknown">No estoy seguro</option>
          </select>
        </label>

        <label class="work-profile-field">
          <span>Planos estructurales</span>
          <select name="structuralPlans" required>
            <option value="">Selecciona</option>
            <option value="yes">Sí tengo</option>
            <option value="no">No tengo</option>
            <option value="unknown">No estoy seguro</option>
          </select>
        </label>

        <label class="work-profile-field work-profile-field-wide">
          <span>Licencia o trámite municipal</span>
          <select name="municipalLicense" required>
            <option value="">Selecciona una opción</option>
            <option value="yes">Sí, cuento con licencia</option>
            <option value="processing">Está en trámite</option>
            <option value="no">No tengo</option>
            <option value="unknown">No estoy seguro</option>
          </select>
        </label>
      </div>

      <div class="work-profile-privacy">
        <strong>Privacidad:</strong> este perfil se guarda localmente y no se envía a Construcción Segura.
      </div>

      <div class="work-profile-actions">
        <button class="work-profile-delete" id="deleteWorkProfile" type="button" hidden>Eliminar perfil</button>
        <button class="primary-button" type="submit">Guardar mi obra</button>
      </div>
    </form>
  `;
  document.body.append(profileDialog);

  const profileForm = profileDialog.querySelector("#workProfileForm");
  const profileSummary = profileSection.querySelector("#workProfileSummary");
  const profileTitle = profileSection.querySelector("#work-profile-title");
  const profileIntro = profileSection.querySelector("#workProfileIntro");
  const deleteProfileButton = profileDialog.querySelector("#deleteWorkProfile");
  let continueToGuideAfterSave = false;

  const labels = {
    projectType: {
      nueva: "Construcción nueva",
      ampliacion: "Ampliación",
      remodelacion: "Remodelación",
      mantenimiento: "Reparación o mantenimiento"
    },
    terrain: {
      flat: "Terreno plano",
      slope: "Terreno en ladera",
      fill: "Terreno con relleno",
      unknown: "Terreno sin identificar"
    },
    floors: {
      "0": "Sin pisos construidos",
      "1": "1 piso",
      "2": "2 pisos",
      "3plus": "3 pisos o más"
    },
    stage: {
      planning: "Planificación y planos",
      excavation: "Excavación",
      foundations: "Cimentaciones",
      structure: "Estructura",
      installations: "Instalaciones",
      finishes: "Acabados",
      maintenance: "Mantenimiento"
    }
  };

  const buildProfileWarnings = (profile) => {
    const warnings = [];

    if (profile.terrain === "slope" || profile.terrain === "fill") {
      warnings.push("El terreno declarado requiere atención especial antes de excavar o definir la cimentación.");
    }

    if (profile.plannedFloors === "3plus" && profile.structuralPlans !== "yes") {
      warnings.push("Proyectas tres pisos o más y no has confirmado planos estructurales. No compres ni armes acero antes de definir el proyecto completo.");
    } else if (["nueva", "ampliacion", "remodelacion"].includes(profile.projectType)
      && profile.structuralPlans !== "yes") {
      warnings.push("Antes de intervenir elementos estructurales, confirma que cuentas con planos y revisión profesional.");
    }

    if (profile.soilStudy !== "yes" && ["nueva", "ampliacion"].includes(profile.projectType)) {
      warnings.push("No has confirmado un estudio de suelos para esta obra. La cimentación no debe definirse copiando otra vivienda.");
    }

    if (profile.municipalLicense === "no" || profile.municipalLicense === "unknown") {
      warnings.push("Revisa el trámite municipal aplicable antes de iniciar o continuar trabajos que requieran autorización.");
    }

    return warnings;
  };

  const renderProfile = (profile) => {
    if (!profile) {
      profileTitle.textContent = "Configura los datos básicos de tu proyecto";
      profileIntro.textContent = "La aplicación guardará estos datos únicamente en este dispositivo para mostrarte advertencias más pertinentes.";
      profileSummary.innerHTML = `
        <div class="work-profile-empty">
          <strong>Aún no has configurado tu obra.</strong>
          <span>Registra el tipo de trabajo, terreno, pisos y documentos disponibles.</span>
        </div>
      `;
      profileSection.querySelector("[data-open-work-profile]").textContent = "Configurar mi obra";
      deleteProfileButton.hidden = true;
      return;
    }

    const location = [profile.district, profile.department].filter(Boolean).join(", ") || "Ubicación no indicada";
    const warnings = buildProfileWarnings(profile);
    const chips = [
      labels.projectType[profile.projectType] || "Proyecto",
      labels.terrain[profile.terrain] || "Terreno",
      `${labels.floors[profile.currentFloors] || "Estado actual"} → ${labels.floors[profile.plannedFloors] || "Proyecto"}`,
      labels.stage[profile.stage] || "Etapa no indicada"
    ];

    profileTitle.textContent = profile.workName || "Mi obra";
    profileIntro.textContent = location;
    profileSummary.innerHTML = "";

    const chipList = document.createElement("div");
    chipList.className = "work-profile-chips";
    chips.forEach((text) => {
      const chip = document.createElement("span");
      chip.textContent = text;
      chipList.append(chip);
    });
    profileSummary.append(chipList);

    const status = document.createElement("div");
    status.className = warnings.length ? "work-profile-alert is-warning" : "work-profile-alert is-ready";
    const statusTitle = document.createElement("strong");
    statusTitle.textContent = warnings.length ? "Recomendaciones iniciales" : "Perfil básico completo";
    status.append(statusTitle);

    if (warnings.length) {
      const list = document.createElement("ul");
      warnings.forEach((warning) => {
        const item = document.createElement("li");
        item.textContent = warning;
        list.append(item);
      });
      status.append(list);
    } else {
      const text = document.createElement("p");
      text.textContent = "Usaremos estos datos para ordenar la guía y mostrar advertencias más relacionadas con tu proyecto.";
      status.append(text);
    }

    profileSummary.append(status);
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
    if (typeof profileDialog.showModal === "function") {
      profileDialog.showModal();
    } else {
      profileDialog.setAttribute("open", "");
    }
  };

  document.querySelectorAll("[data-open-work-profile]").forEach((button) => {
    button.addEventListener("click", () => openProfile());
  });

  document.addEventListener("mi-casa-segura:open-work-profile", (event) => {
    openProfile({ continueToGuide: Boolean(event.detail?.continueToGuide) });
  });

  profileDialog.querySelector("[data-close-work-profile]").addEventListener("click", () => {
    profileDialog.close();
  });

  profileDialog.addEventListener("click", (event) => {
    if (event.target === profileDialog) profileDialog.close();
  });

  profileForm.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!profileForm.reportValidity()) return;

    const data = Object.fromEntries(new FormData(profileForm).entries());
    data.updatedAt = new Date().toISOString();
    saveProfile(data);
    renderProfile(data);
    profileDialog.close();

    document.dispatchEvent(new CustomEvent("mi-casa-segura:work-profile-saved", {
      detail: { profile: data, continueToGuide: continueToGuideAfterSave }
    }));
    continueToGuideAfterSave = false;
  });

  deleteProfileButton.addEventListener("click", () => {
    const confirmed = window.confirm("¿Deseas eliminar los datos guardados de esta obra en este dispositivo?");
    if (!confirmed) return;
    window.localStorage.removeItem(PROFILE_KEY);
    renderProfile(null);
    profileDialog.close();
  });

  renderProfile(readProfile());
})();
