(() => {
  const API_BASE_URL = window.CONSTRUCCION_SEGURA_API_URL
    || "https://construccion-segura.onrender.com";
  const API_TIMEOUT_MS = 20000;
  const SEARCH_DELAY_MS = 320;
  const RESULT_LIMIT = 50;
  const CACHE_KEY = "mi-casa-segura-normativa-cache-v1";

  const form = document.getElementById("normativeForm");
  const input = document.getElementById("normativeSearch");
  const categorySelect = document.getElementById("normativeCategory");
  const elementSelect = document.getElementById("normativeElement");
  const classificationSelect = document.getElementById("normativeClassification");
  const clearButton = document.getElementById("clearNormative");
  const retryButton = document.getElementById("retryNormative");
  const popular = document.getElementById("normativePopular");
  const status = document.getElementById("normativeStatus");
  const notice = document.getElementById("normativeNotice");
  const summary = document.getElementById("normativeSummary");
  const results = document.getElementById("normativeResults");
  const emptyState = document.getElementById("normativeEmpty");

  if (!form || !input || !categorySelect || !elementSelect
    || !classificationSelect || !results || !emptyState) return;

  const classificationLabels = {
    minimo_normativo: "Mínimo normativo",
    maximo_normativo: "Máximo normativo",
    formula_normativa: "Fórmula normativa",
    condicion_normativa: "Condición normativa",
    depende_calculo: "Depende del cálculo",
    prohibicion: "Prohibición",
    recomendacion: "Recomendación"
  };

  const reviewLabels = {
    piloto_verificado: "Piloto revisado",
    validado_con_numeral: "Validado con numeral",
    borrador: "Borrador editorial",
    retirado: "Retirado"
  };

  let catalog = [];
  let searchTimer = null;
  let searchController = null;
  let requestSequence = 0;

  const normalize = (value = "") => String(value)
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9ñ\s]/g, " ")
    .replace(/\s+/g, " ")
    .trim();

  const escapeHtml = (value = "") => String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

  const safeOfficialUrl = (value = "") => {
    try {
      const url = new URL(String(value));
      return ["http:", "https:"].includes(url.protocol) ? url.href : "";
    } catch {
      return "";
    }
  };

  const readCache = () => {
    try {
      const cached = JSON.parse(localStorage.getItem(CACHE_KEY));
      if (!cached || !Array.isArray(cached.payload?.resultados)) return null;
      return cached;
    } catch {
      return null;
    }
  };

  const saveCache = (payload) => {
    try {
      localStorage.setItem(CACHE_KEY, JSON.stringify({
        savedAt: new Date().toISOString(),
        payload
      }));
    } catch {
      // La consulta sigue funcionando aunque el almacenamiento esté bloqueado.
    }
  };

  const setConnectionState = (kind, message) => {
    if (!status) return;
    status.className = `normative-status is-${kind}`;
    status.textContent = message;
  };

  const setNotice = (message = "", kind = "info") => {
    if (!notice) return;
    notice.hidden = !message;
    notice.className = `normative-notice is-${kind}`;
    notice.textContent = message;
  };

  const setBusy = (busy) => {
    results.setAttribute("aria-busy", String(busy));
    form.setAttribute("aria-busy", String(busy));
    form.querySelectorAll("input, select, button[type='submit']").forEach((control) => {
      control.toggleAttribute("data-loading", busy);
    });
  };

  const fetchJson = async (path, signal) => {
    const endpoint = new URL(path, API_BASE_URL);
    const response = await fetch(endpoint, {
      method: "GET",
      mode: "cors",
      cache: "no-store",
      headers: { Accept: "application/json" },
      signal
    });

    if (!response.ok) {
      throw new Error(`La API respondió con el estado ${response.status}`);
    }

    return response.json();
  };

  const uniqueSorted = (values) => [...new Set(values.filter(Boolean))]
    .sort((a, b) => a.localeCompare(b, "es"));

  const populateCategories = () => {
    const selected = categorySelect.value;
    const categories = uniqueSorted(catalog.map((item) => item.categoria));
    categorySelect.innerHTML = [
      '<option value="">Todas las categorías</option>',
      ...categories.map((category) => (
        `<option value="${escapeHtml(category)}">${escapeHtml(category)}</option>`
      ))
    ].join("");
    if (categories.includes(selected)) categorySelect.value = selected;
    populateElements();
  };

  const populateElements = () => {
    const selected = elementSelect.value;
    const selectedCategory = categorySelect.value;
    const elements = uniqueSorted(
      catalog
        .filter((item) => !selectedCategory || item.categoria === selectedCategory)
        .map((item) => item.elemento)
    );

    elementSelect.innerHTML = [
      '<option value="">Todos los elementos</option>',
      ...elements.map((element) => (
        `<option value="${escapeHtml(element)}">${escapeHtml(element)}</option>`
      ))
    ].join("");
    elementSelect.disabled = elements.length === 0;
    if (elements.includes(selected)) elementSelect.value = selected;
  };

  const renderList = (items = []) => items
    .map((item) => `<li>${escapeHtml(item)}</li>`)
    .join("");

  const renderSource = (source = {}) => {
    const officialUrl = safeOfficialUrl(source.url_oficial);
    const title = [source.tipo, source.norma, source.denominacion]
      .filter(Boolean)
      .join(" · ");
    const device = source.dispositivo
      ? `<span>${escapeHtml(source.dispositivo)}</span>`
      : "";
    const numeral = source.numeral_confirmado && source.numeral
      ? `<span>Numeral ${escapeHtml(source.numeral)}</span>`
      : '<span class="is-pending">Numeral específico pendiente de verificación editorial</span>';
    const titleMarkup = officialUrl
      ? `<a href="${escapeHtml(officialUrl)}" target="_blank" rel="noopener noreferrer">${escapeHtml(title)}</a>`
      : `<strong>${escapeHtml(title)}</strong>`;

    return `<div class="normative-source">${titleMarkup}${device}${numeral}</div>`;
  };

  const renderCard = (item) => {
    const classification = classificationLabels[item.clasificacion]
      || item.clasificacion
      || "Parámetro técnico";
    const review = reviewLabels[item.estado_revision]
      || item.estado_revision
      || "En revisión";
    const conditions = Array.isArray(item.condiciones) ? item.condiciones : [];
    const valueText = item.valor?.texto || "Valor no disponible";

    return `
      <article class="normative-card" data-classification="${escapeHtml(item.clasificacion || "")}">
        <header class="normative-card-heading">
          <div>
            <p class="normative-card-category">${escapeHtml(item.categoria || "Base normativa")}</p>
            <h3>${escapeHtml(item.parametro || "Parámetro técnico")}</h3>
            <p class="normative-card-element">${escapeHtml(item.elemento || "Elemento no indicado")}</p>
          </div>
          <span class="normative-badge">${escapeHtml(classification)}</span>
        </header>

        <div class="normative-value">
          <span>Valor o regla aplicable</span>
          <strong>${escapeHtml(valueText)}</strong>
        </div>

        ${conditions.length ? `
          <details class="normative-details">
            <summary>Condiciones de aplicación</summary>
            <ul>${renderList(conditions)}</ul>
          </details>
        ` : ""}

        ${item.advertencia ? `
          <div class="normative-warning">
            <strong>Importante</strong>
            <p>${escapeHtml(item.advertencia)}</p>
          </div>
        ` : ""}

        <footer>
          ${renderSource(item.fuente)}
          <span class="normative-review-state">${escapeHtml(review)}</span>
        </footer>
      </article>
    `;
  };

  const renderResults = (payload, { cached = false } = {}) => {
    const items = Array.isArray(payload?.resultados) ? payload.resultados : [];
    results.innerHTML = items.map(renderCard).join("");
    results.hidden = items.length === 0;
    emptyState.hidden = items.length !== 0;
    retryButton?.setAttribute("hidden", "");

    if (summary) {
      summary.hidden = false;
      const total = Number(payload?.total_encontrados ?? items.length);
      const shown = Number(payload?.mostrados ?? items.length);
      summary.textContent = total === shown
        ? `${total} ${total === 1 ? "parámetro encontrado" : "parámetros encontrados"}`
        : `${shown} de ${total} parámetros mostrados`;
    }

    if (cached) {
      setConnectionState("cached", "Copia guardada");
      setNotice(
        "No pudimos actualizar la base en este momento. Mostramos la última copia guardada en este dispositivo.",
        "warning"
      );
    } else {
      setConnectionState("online", "Base disponible");
      setNotice(payload?.advertencia_general || "", "info");
    }
  };

  const filterCachedPayload = (payload) => {
    const query = normalize(input.value);
    const category = categorySelect.value;
    const element = elementSelect.value;
    const classification = classificationSelect.value;
    const allItems = Array.isArray(payload?.resultados) ? payload.resultados : [];

    const filtered = allItems.filter((item) => {
      if (category && item.categoria !== category) return false;
      if (element && item.elemento !== element) return false;
      if (classification && item.clasificacion !== classification) return false;
      if (!query) return true;

      const searchable = normalize([
        item.categoria,
        item.elemento,
        item.parametro,
        item.valor?.texto,
        ...(item.condiciones || [])
      ].join(" "));
      return query.split(" ").every((word) => searchable.includes(word));
    });

    return {
      ...payload,
      total_encontrados: filtered.length,
      mostrados: filtered.length,
      resultados: filtered
    };
  };

  const buildParametersPath = () => {
    const endpoint = new URL("/api/v1/normativa/parametros", API_BASE_URL);
    const rawQuery = input.value.trim();
    if (rawQuery) endpoint.searchParams.set("consulta", rawQuery);
    if (categorySelect.value) endpoint.searchParams.set("categoria", categorySelect.value);
    if (elementSelect.value) endpoint.searchParams.set("elemento", elementSelect.value);
    if (classificationSelect.value) {
      endpoint.searchParams.set("clasificacion", classificationSelect.value);
    }
    endpoint.searchParams.set("limite", String(RESULT_LIMIT));
    return `${endpoint.pathname}${endpoint.search}`;
  };

  const hasActiveFilters = () => Boolean(
    input.value.trim()
    || categorySelect.value
    || elementSelect.value
    || classificationSelect.value
  );

  const searchParameters = async ({ cacheFullPayload = false } = {}) => {
    const normalizedQuery = normalize(input.value);
    if (normalizedQuery.length === 1) {
      setNotice("Escribe al menos dos caracteres para buscar por texto.", "warning");
      return;
    }

    searchController?.abort();
    const controller = new AbortController();
    searchController = controller;
    const currentRequest = ++requestSequence;
    const timeoutId = window.setTimeout(() => controller.abort(), API_TIMEOUT_MS);

    setBusy(true);
    setConnectionState("loading", "Consultando…");
    retryButton?.setAttribute("hidden", "");

    try {
      const payload = await fetchJson(buildParametersPath(), controller.signal);
      if (currentRequest !== requestSequence) return;
      renderResults(payload);
      if (cacheFullPayload && !hasActiveFilters()) saveCache(payload);
    } catch (error) {
      if (error?.name === "AbortError" && currentRequest !== requestSequence) return;
      if (currentRequest !== requestSequence) return;

      const cached = readCache();
      if (cached) {
        renderResults(filterCachedPayload(cached.payload), { cached: true });
      } else {
        results.hidden = true;
        emptyState.hidden = false;
        emptyState.innerHTML = `
          <strong>No pudimos consultar la base normativa.</strong>
          <span>Render puede estar iniciando el servicio. Espera unos segundos y vuelve a intentar.</span>
        `;
        retryButton?.removeAttribute("hidden");
        summary?.setAttribute("hidden", "");
        setConnectionState("error", "Sin conexión");
        setNotice("La búsqueda no está disponible temporalmente.", "warning");
      }
    } finally {
      window.clearTimeout(timeoutId);
      if (currentRequest === requestSequence) setBusy(false);
    }
  };

  const loadCatalog = async () => {
    const controller = new AbortController();
    const timeoutId = window.setTimeout(() => controller.abort(), API_TIMEOUT_MS);
    try {
      const payload = await fetchJson("/api/v1/normativa/elementos", controller.signal);
      catalog = Array.isArray(payload?.elementos) ? payload.elementos : [];
      populateCategories();
    } catch {
      const cached = readCache();
      if (cached) {
        catalog = uniqueSorted(
          cached.payload.resultados.map((item) => `${item.categoria}\u0000${item.elemento}`)
        ).map((value) => {
          const [categoria, elemento] = value.split("\u0000");
          return { categoria, elemento };
        });
        populateCategories();
      }
    } finally {
      window.clearTimeout(timeoutId);
    }
  };

  const scheduleSearch = () => {
    window.clearTimeout(searchTimer);
    const normalizedQuery = normalize(input.value);
    if (normalizedQuery.length === 1) {
      setNotice("Escribe al menos dos caracteres para buscar por texto.", "warning");
      return;
    }
    searchTimer = window.setTimeout(() => searchParameters(), SEARCH_DELAY_MS);
  };

  const clearFilters = () => {
    window.clearTimeout(searchTimer);
    input.value = "";
    categorySelect.value = "";
    populateElements();
    elementSelect.value = "";
    classificationSelect.value = "";
    searchParameters({ cacheFullPayload: true });
  };

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    window.clearTimeout(searchTimer);
    searchParameters();
  });

  input.addEventListener("input", scheduleSearch);

  categorySelect.addEventListener("change", () => {
    populateElements();
    searchParameters();
  });

  elementSelect.addEventListener("change", () => searchParameters());
  classificationSelect.addEventListener("change", () => searchParameters());
  clearButton?.addEventListener("click", clearFilters);
  retryButton?.addEventListener("click", () => searchParameters({
    cacheFullPayload: !hasActiveFilters()
  }));

  popular?.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-normative-query]");
    if (!button) return;
    input.value = button.dataset.normativeQuery || "";
    window.clearTimeout(searchTimer);
    searchParameters();
  });

  const initialize = async () => {
    const cached = readCache();
    if (cached) renderResults(cached.payload, { cached: true });
    else setConnectionState("loading", "Conectando…");

    await Promise.allSettled([
      loadCatalog(),
      searchParameters({ cacheFullPayload: true })
    ]);
  };

  initialize();
})();
