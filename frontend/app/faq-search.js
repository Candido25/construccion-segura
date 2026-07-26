(() => {
  const API_BASE_URL = "https://construccion-segura.onrender.com";
  const API_RESULT_LIMIT = 10;
  const REMOTE_TIMEOUT_MS = 15000;
  const faqs = Array.isArray(window.MI_CASA_SEGURA_FAQS) ? window.MI_CASA_SEGURA_FAQS : [];
  const localFaqs = Array.isArray(window.MI_CASA_SEGURA_FAQS) ? window.MI_CASA_SEGURA_FAQS : [];
  const API_BASE_URL = window.CONSTRUCCION_SEGURA_API_URL || "https://construccion-segura.onrender.com";
  const LOCAL_LIMIT = 4;
  const REMOTE_LIMIT = 10;
  const DISPLAY_LIMIT = 7;
  const SEARCH_DELAY_MS = 320;
  const API_TIMEOUT_MS = 20000;

  const input = document.getElementById("faqSearch");
  const suggestions = document.getElementById("faqSuggestions");
  const emptyState = document.getElementById("faqEmpty");
  const answer = document.getElementById("faqAnswer");
  const popular = document.getElementById("faqPopular");

  if (!input || !suggestions || !emptyState || !answer) return;

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

  const searchableText = new Map(
    localFaqs.map((faq) => [
      faq.id,
      normalize([faq.question, faq.category, ...(faq.aliases || [])].join(" "))
    ])
  );

  let activeIndex = -1;
  let currentResults = [];
  let debounceTimer = null;
  let activeController = null;
  let requestSequence = 0;
  let searchTimer = null;
  let searchController = null;
  let requestSequence = 0;

  const escapeHtml = (value = "") => String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

  const scoreLocalFaq = (faq, query) => {
    const normalizedQuestion = normalize(faq.question);
    const normalizedCategory = normalize(faq.category);
    const aliases = (faq.aliases || []).map(normalize);
    const haystack = searchableText.get(faq.id) || "";
    let score = 0;

    if (normalizedQuestion === query) score += 100;
    if (normalizedQuestion.startsWith(query)) score += 55;
    if (normalizedQuestion.includes(query)) score += 35;
    if (aliases.some((alias) => alias.startsWith(query))) score += 30;
    if (aliases.some((alias) => alias.includes(query))) score += 20;
    if (normalizedCategory.includes(query)) score += 12;

    const words = query.split(" ").filter(Boolean);
    const matches = words.filter((word) => haystack.includes(word)).length;
    score += matches * 8;
    if (matches === words.length && words.length > 1) score += 15;
    return score;
  };

  const getLocalResults = (rawQuery) => {
    const query = normalize(rawQuery);
    if (query.length < 2) return [];

    return localFaqs
      .map((faq) => ({ faq: { ...faq, source: "local" }, score: scoreLocalFaq(faq, query) }))
      .filter((item) => item.score > 0)
      .sort((a, b) => b.score - a.score || a.faq.question.localeCompare(b.faq.question, "es"))
      .slice(0, 7)
      .map((item) => ({ source: "local", ...item.faq }));
  };

  const fetchRemoteResults = async (query, signal) => {
    const url = new URL("/buscar", API_BASE_URL);
    url.searchParams.set("termino", query);
    url.searchParams.set("limite", String(API_RESULT_LIMIT));

    const response = await fetch(url, {
      method: "GET",
      headers: { Accept: "application/json" },
      mode: "cors",
      signal,
    });

    if (!response.ok) throw new Error(`API respondió ${response.status}`);
    const payload = await response.json();
    const results = Array.isArray(payload.resultados) ? payload.resultados : [];

    return results.map((item) => ({
      source: "remote",
      id: `api-${item.id || normalize(item.pregunta)}`,
      category: item.categoria || "Consulta técnica",
      question: item.pregunta || "Pregunta técnica",
      response: item.respuesta || "Respuesta no disponible.",
    }));
  };

  const mergeResults = (localResults, remoteResults) => {
    const seen = new Set();
    return [...localResults, ...remoteResults]
      .filter((item) => {
        const key = normalize(item.question);
        if (!key || seen.has(key)) return false;
        seen.add(key);
        return true;
      })
      .slice(0, 10);
      .slice(0, LOCAL_LIMIT)
      .map((item) => item.faq);
  };

  const mapRemoteResults = (payload) => {
    if (!payload || !Array.isArray(payload.resultados)) return [];

    return payload.resultados
      .filter((item) => item && item.pregunta && item.respuesta)
      .map((item, index) => ({
        id: `api:${item.id || index}`,
        category: item.categoria || "Base técnica",
        question: item.pregunta,
        quick: item.respuesta,
        source: "api"
      }));
  };

  const mergeResults = (localResults, remoteResults) => {
    const seenQuestions = new Set();
    const combined = [];

    [...localResults, ...remoteResults].forEach((faq) => {
      const key = normalize(faq.question);
      if (!key || seenQuestions.has(key)) return;
      seenQuestions.add(key);
      combined.push(faq);
    });

    return combined.slice(0, DISPLAY_LIMIT);
  };

  const setBusy = (busy) => {
    input.setAttribute("aria-busy", String(busy));
  };

  const hideSuggestions = () => {
    suggestions.hidden = true;
    input.setAttribute("aria-expanded", "false");
    activeIndex = -1;
    input.removeAttribute("aria-activedescendant");
  };

  const setActiveSuggestion = (nextIndex) => {
    const buttons = [...suggestions.querySelectorAll("button")];
    if (!buttons.length) {
      activeIndex = -1;
      input.removeAttribute("aria-activedescendant");
      return;
    }

    activeIndex = Math.max(0, Math.min(nextIndex, buttons.length - 1));
    buttons.forEach((button, index) => {
      const selected = index === activeIndex;
      button.classList.toggle("is-active", selected);
      button.setAttribute("aria-selected", String(selected));
      if (selected) {
        input.setAttribute("aria-activedescendant", button.id);
        button.scrollIntoView({ block: "nearest" });
      }
    });
  };

  const renderSuggestions = (results, query, statusMessage = "") => {
  const renderSuggestions = (results, query, emptyMessage = "") => {
    currentResults = results;
    activeIndex = -1;
    input.removeAttribute("aria-activedescendant");

    if (!query) {
      hideSuggestions();
      emptyState.hidden = true;
      return;
    }

    if (!results.length) {
      hideSuggestions();
      emptyState.hidden = false;
      emptyState.textContent = statusMessage || "No encontramos resultados. Prueba con otra palabra relacionada con tu obra.";
      emptyState.textContent = emptyMessage || "No encontramos una pregunta todavía. Prueba con otra palabra: zapata, grieta, techo, escalera, cable o desagüe.";
      return;
    }

    emptyState.hidden = true;
    suggestions.innerHTML = results.map((item, index) => `
      <button id="faq-option-${index}" type="button" role="option" aria-selected="false" data-result-index="${index}">
        <span>${escapeHtml(item.question)}</span>
        <small>${escapeHtml(item.category)}${item.source === "remote" ? " · Base técnica" : " · Destacada"}</small>
    suggestions.innerHTML = results.map((faq, index) => `
      <button id="faq-option-${index}" type="button" role="option" aria-selected="false" data-result-index="${index}">
        <span>${escapeHtml(faq.question)}</span>
        <small>${escapeHtml(faq.category)}${faq.source === "api" ? " · Base técnica ampliada" : " · Pregunta destacada"}</small>
      </button>
    `).join("");
    suggestions.hidden = false;
    input.setAttribute("aria-expanded", "true");
  };

  const listItems = (items = []) => items.map((item) => `<li>${escapeHtml(item)}</li>`).join("");

  const showAnswer = (item) => {
    if (!item) return;
    input.value = item.question;
    suggestions.hidden = true;
  const showAnswer = (faq) => {
    if (!faq) return;

    input.value = faq.question;
    hideSuggestions();
    emptyState.hidden = true;

    if (item.source === "remote") {
      answer.innerHTML = `
        <p class="faq-answer-category">${escapeHtml(item.category)}</p>
        <h3>${escapeHtml(item.question)}</h3>
        <div class="faq-answer-quick">
          <strong>Respuesta técnica</strong>
          <p>${escapeHtml(item.response)}</p>
        </div>
        <p class="faq-disclaimer"><strong>Importante:</strong> esta orientación es educativa y no reemplaza el estudio, los planos, el cálculo ni la revisión profesional de tu caso.</p>
      `;
    } else {
      answer.innerHTML = `
        <p class="faq-answer-category">${escapeHtml(item.category)}</p>
        <h3>${escapeHtml(item.question)}</h3>
        <div class="faq-answer-quick">
          <strong>Respuesta rápida</strong>
          <p>${escapeHtml(item.quick)}</p>
        </div>
        <div class="faq-answer-grid">
          <section><h4>Qué debes revisar</h4><ul>${listItems(item.review)}</ul></section>
          <section class="faq-answer-warning"><h4>No permitas esto</h4><p>${escapeHtml(item.avoid)}</p></section>
          <section><h4>Referencia normativa</h4><p>${escapeHtml(item.standard)}</p></section>
          <section class="faq-answer-professional"><h4>Cuándo consultar</h4><p>${escapeHtml(item.professional)}</p></section>
    if (faq.source === "api") {
      answer.innerHTML = `
        <p class="faq-answer-category">${escapeHtml(faq.category)}</p>
        <h3>${escapeHtml(faq.question)}</h3>
        <div class="faq-answer-quick">
          <strong>Respuesta técnica</strong>
          <p>${escapeHtml(faq.quick)}</p>
        </div>
        <p class="faq-disclaimer"><strong>Importante:</strong> esta orientación es educativa y general. No reemplaza el estudio, los planos, el cálculo ni la revisión profesional de una obra concreta.</p>
      `;
    } else {
      answer.innerHTML = `
        <p class="faq-answer-category">${escapeHtml(faq.category)}</p>
        <h3>${escapeHtml(faq.question)}</h3>
        <div class="faq-answer-quick">
          <strong>Respuesta rápida</strong>
          <p>${escapeHtml(faq.quick)}</p>
        </div>
        <div class="faq-answer-grid">
          <section>
            <h4>Qué debes revisar</h4>
            <ul>${listItems(faq.review)}</ul>
          </section>
          <section class="faq-answer-warning">
            <h4>No permitas esto</h4>
            <p>${escapeHtml(faq.avoid)}</p>
          </section>
          <section>
            <h4>Referencia normativa</h4>
            <p>${escapeHtml(faq.standard)}</p>
          </section>
          <section class="faq-answer-professional">
            <h4>Cuándo consultar</h4>
            <p>${escapeHtml(faq.professional)}</p>
          </section>
        </div>
        <p class="faq-disclaimer"><strong>Importante:</strong> esta orientación es educativa y no reemplaza el estudio, los planos, el cálculo ni la revisión profesional de tu caso.</p>
      `;
    }

    answer.hidden = false;
    answer.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  const runSearch = async (rawQuery) => {
    const query = rawQuery.trim();
    const normalizedQuery = normalize(query);
    const sequence = ++requestSequence;
    const localResults = getLocalResults(query);

    activeController?.abort();
    activeController = null;

    if (!normalizedQuery) {
      renderSuggestions([], "");
      return;
    }

    if (normalizedQuery.length < 2) {
      renderSuggestions(localResults, query, localResults.length ? "" : "Escribe al menos dos caracteres para buscar en la base técnica.");
      return;
    }

    renderSuggestions(localResults, query, localResults.length ? "" : "Buscando en la base técnica…");

    const controller = new AbortController();
    activeController = controller;
    const timeoutId = window.setTimeout(() => controller.abort(), REMOTE_TIMEOUT_MS);

    try {
      const remoteResults = await fetchRemoteResults(query, controller.signal);
      if (sequence !== requestSequence) return;
      const combined = mergeResults(localResults, remoteResults);
      renderSuggestions(combined, query);
    } catch (error) {
      if (sequence !== requestSequence || error?.name === "AbortError") return;
      renderSuggestions(
        localResults,
        query,
        "La base técnica está tardando en responder. Las preguntas destacadas siguen disponibles."
      );
    } finally {
      window.clearTimeout(timeoutId);
      if (activeController === controller) activeController = null;
    }
  };

  input.addEventListener("input", () => {
    const query = input.value;
    answer.hidden = true;
    window.clearTimeout(debounceTimer);
    debounceTimer = window.setTimeout(() => runSearch(query), 320);
  });

  input.addEventListener("focus", () => {
    const query = input.value.trim();
    if (query) runSearch(query);
  const fetchRemoteResults = async (rawQuery, signal) => {
    const endpoint = new URL("/buscar", API_BASE_URL);
    endpoint.searchParams.set("termino", rawQuery);
    endpoint.searchParams.set("limite", String(REMOTE_LIMIT));

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

    return mapRemoteResults(await response.json());
  };

  const searchExpandedDatabase = async (rawQuery, localResults) => {
    const normalizedQuery = normalize(rawQuery);
    if (normalizedQuery.length < 2) return;

    if (searchController) searchController.abort();
    const controller = new AbortController();
    searchController = controller;
    const currentRequest = ++requestSequence;
    const timeoutId = window.setTimeout(() => controller.abort(), API_TIMEOUT_MS);
    setBusy(true);

    try {
      const remoteResults = await fetchRemoteResults(rawQuery, controller.signal);
      if (currentRequest !== requestSequence || normalize(input.value) !== normalizedQuery) return;

      const combined = mergeResults(localResults, remoteResults);
      renderSuggestions(combined, rawQuery);
    } catch (error) {
      if (error?.name === "AbortError" || currentRequest !== requestSequence) return;

      if (!localResults.length) {
        renderSuggestions([], rawQuery, "No pudimos consultar la base técnica ampliada en este momento. Prueba nuevamente en unos segundos.");
      }
    } finally {
      window.clearTimeout(timeoutId);
      if (currentRequest === requestSequence) setBusy(false);
    }
  };

  const runSearch = () => {
    window.clearTimeout(searchTimer);
    const rawQuery = input.value.trim();
    const normalizedQuery = normalize(rawQuery);
    answer.hidden = true;

    if (!normalizedQuery) {
      if (searchController) searchController.abort();
      hideSuggestions();
      emptyState.hidden = true;
      setBusy(false);
      return;
    }

    if (normalizedQuery.length < 2) {
      if (searchController) searchController.abort();
      renderSuggestions([], rawQuery, "Escribe al menos dos caracteres para buscar.");
      setBusy(false);
      return;
    }

    const localResults = getLocalResults(rawQuery);
    renderSuggestions(localResults, rawQuery, "Buscando en la base técnica ampliada…");

    searchTimer = window.setTimeout(() => {
      searchExpandedDatabase(rawQuery, localResults);
    }, SEARCH_DELAY_MS);
  };

  input.addEventListener("input", runSearch);

  input.addEventListener("focus", () => {
    if (input.value.trim()) runSearch();
  });

  input.addEventListener("keydown", (event) => {
    if (suggestions.hidden || !currentResults.length) return;

    if (event.key === "ArrowDown") {
      event.preventDefault();
      setActiveSuggestion(activeIndex < currentResults.length - 1 ? activeIndex + 1 : 0);
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      setActiveSuggestion(activeIndex > 0 ? activeIndex - 1 : currentResults.length - 1);
    } else if (event.key === "Enter" && activeIndex >= 0) {
      event.preventDefault();
      showAnswer(currentResults[activeIndex]);
    } else if (event.key === "Escape") {
      hideSuggestions();
      emptyState.hidden = true;
    }
  });

  suggestions.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-result-index]");
    if (button) showAnswer(currentResults[Number(button.dataset.resultIndex)]);
    if (!button) return;
    showAnswer(currentResults[Number(button.dataset.resultIndex)]);
  });

  popular?.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-faq-id]");
    if (!button) return;
    const faq = faqs.find((item) => item.id === button.dataset.faqId);
    if (faq) showAnswer({ source: "local", ...faq });
    showAnswer(localFaqs.find((faq) => faq.id === button.dataset.faqId));
  });

  document.addEventListener("click", (event) => {
    if (!event.target.closest(".faq-search-box")) hideSuggestions();
  });
})();
