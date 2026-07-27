(() => {
  const localFaqs = Array.isArray(window.MI_CASA_SEGURA_FAQS)
    ? window.MI_CASA_SEGURA_FAQS
    : [];
  const API_BASE_URL = window.CONSTRUCCION_SEGURA_API_URL
    || "https://construccion-segura.onrender.com";
  const LOCAL_LIMIT = 4;
  const REMOTE_LIMIT = 10;
  const DISPLAY_LIMIT = 7;
  const SEARCH_DELAY_MS = 320;
  const API_TIMEOUT_MS = 15000;

  const input = document.getElementById("faqSearch");
  const suggestions = document.getElementById("faqSuggestions");
  const emptyState = document.getElementById("faqEmpty");
  const answer = document.getElementById("faqAnswer");
  const popular = document.getElementById("faqPopular");

  if (!input || !suggestions || !emptyState || !answer) return;

  const riskService = window.MI_CASA_SEGURA_RISK;
  const professionalHelp = window.MI_CASA_SEGURA_PROFESSIONAL_HELP;

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

  const asArray = (value) => {
    if (Array.isArray(value)) return value.filter(Boolean);
    if (typeof value === "string" && value.trim()) return [value.trim()];
    return [];
  };

  const searchableText = new Map(
    localFaqs.map((faq) => [
      faq.id,
      normalize([faq.question, faq.category, ...(faq.aliases || [])].join(" "))
    ])
  );

  let activeIndex = -1;
  let currentResults = [];
  let searchTimer = null;
  let searchController = null;
  let requestSequence = 0;

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

  const enrichLocalFaq = (faq) => {
    const registry = window.MI_CASA_SEGURA_FAQ_RISKS || {};
    const risk = registry[faq.id] || {};
    return {
      ...faq,
      risk: faq.risk || risk.risk || null,
      riskReviewed: faq.riskReviewed ?? risk.reviewed ?? false,
      riskReviewedAt: faq.riskReviewedAt || risk.reviewedAt || "",
      riskRationale: faq.riskRationale || risk.rationale || "",
      source: "local"
    };
  };

  const getLocalResults = (rawQuery) => {
    const query = normalize(rawQuery);
    if (query.length < 2) return [];

    return localFaqs
      .map((faq) => ({ faq: enrichLocalFaq(faq), score: scoreLocalFaq(faq, query) }))
      .filter((item) => item.score > 0)
      .sort((a, b) => b.score - a.score
        || a.faq.question.localeCompare(b.faq.question, "es"))
      .slice(0, LOCAL_LIMIT)
      .map((item) => item.faq);
  };

  const mapRemoteResults = (payload) => {
    if (!payload || !Array.isArray(payload.resultados)) return [];

    return payload.resultados
      .filter((item) => item && item.pregunta && item.respuesta)
      .map((item, index) => ({
        id: `api:${item.id || index}`,
        originalId: item.id || "",
        category: item.categoria || "Base técnica",
        question: item.pregunta,
        quick: item.respuesta,
        review: item.que_revisar || item.revisar || [],
        avoid: item.no_permitir || item.evitar || "",
        standard: item.fuente?.referencia || item.fuente || item.norma || "",
        professional: item.cuando_consultar || "",
        conditions: item.condiciones || [],
        risk: item.riesgo || item.nivel_riesgo || null,
        riskReviewed: Boolean(item.riesgo_revisado || item.nivel_riesgo_revisado),
        riskReviewedAt: item.fecha_revision_riesgo || "",
        updatedAt: item.fecha_revision || item.actualizado || "",
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
      emptyState.textContent = emptyMessage
        || "No encontramos una pregunta todavía. Prueba con otra palabra: zapata, grieta, techo, escalera, cable o desagüe.";
      return;
    }

    emptyState.hidden = true;
    suggestions.innerHTML = results.map((faq, index) => {
      const riskMeta = riskService?.metadataFor(faq);
      const riskLabel = riskMeta?.key === "pending" ? "Riesgo en revisión" : riskMeta?.label;
      return `
        <button id="faq-option-${index}" type="button" role="option" aria-selected="false" data-result-index="${index}">
          <span>${escapeHtml(faq.question)}</span>
          <small>${escapeHtml(faq.category)} · ${escapeHtml(riskLabel || "Respuesta revisada")}</small>
        </button>
      `;
    }).join("");
    suggestions.hidden = false;
    input.setAttribute("aria-expanded", "true");
  };

  const listItems = (items = []) => asArray(items)
    .map((item) => `<li>${escapeHtml(item)}</li>`)
    .join("");

  const renderSection = ({ title, content, className = "" }) => {
    const values = asArray(content);
    if (!values.length) return "";
    const body = values.length > 1
      ? `<ul>${listItems(values)}</ul>`
      : `<p>${escapeHtml(values[0])}</p>`;
    return `<section class="${escapeHtml(className)}"><h4>${escapeHtml(title)}</h4>${body}</section>`;
  };

  const showAnswer = (faq) => {
    if (!faq) return;

    input.value = faq.question;
    hideSuggestions();
    emptyState.hidden = true;

    const riskMeta = riskService?.metadataFor(faq) || {
      key: "pending",
      label: "Clasificación en revisión",
      reviewed: false
    };
    const riskPanel = riskService?.renderPanel(faq, escapeHtml) || "";
    const review = asArray(faq.review);
    const conditions = asArray(faq.conditions);
    const sourceLabel = faq.source === "api"
      ? "Base técnica ampliada"
      : "Pregunta destacada revisada";
    const reviewDate = faq.riskReviewedAt || faq.updatedAt || "";
    const cta = professionalHelp?.ctaFor(faq, riskMeta);

    const fallbackReview = faq.source === "api" && !review.length
      ? ["Comprueba que la respuesta corresponda al elemento, etapa y condiciones reales de tu obra."]
      : [];
    const fallbackProfessional = faq.source === "api" && !faq.professional
      ? "Consulta antes de aplicar la respuesta cuando existan daños, diferencias con los planos o condiciones que no aparecen descritas."
      : "";

    answer.dataset.risk = riskMeta.key;
    answer.innerHTML = `
      <p class="faq-answer-category">${escapeHtml(faq.category)}</p>
      <h3>${escapeHtml(faq.question)}</h3>
      ${riskPanel}
      <div class="faq-answer-quick">
        <strong>Respuesta rápida</strong>
        <p>${escapeHtml(faq.quick)}</p>
      </div>
      <div class="faq-answer-grid">
        ${renderSection({ title: "Qué debes revisar", content: review.length ? review : fallbackReview })}
        ${renderSection({ title: "No permitas esto", content: faq.avoid, className: "faq-answer-warning" })}
        ${renderSection({ title: "Referencia o criterio", content: faq.standard })}
        ${renderSection({ title: "Condiciones y excepciones", content: conditions })}
        ${renderSection({ title: "Cuándo consultar", content: faq.professional || fallbackProfessional, className: "faq-answer-professional" })}
      </div>
      <div class="faq-answer-metadata">
        <span><strong>Origen:</strong> ${escapeHtml(sourceLabel)}</span>
        ${reviewDate ? `<span><strong>Revisión:</strong> ${escapeHtml(reviewDate)}</span>` : ""}
      </div>
      ${cta ? `<a class="faq-professional-cta" href="${escapeHtml(cta.href)}" target="_blank" rel="noopener noreferrer">${escapeHtml(cta.label)}</a>` : ""}
      <p class="faq-disclaimer"><strong>Importante:</strong> esta orientación es educativa y general. No reemplaza el estudio, los planos, el cálculo ni la evaluación profesional de una obra concreta.</p>
    `;

    answer.hidden = false;
    answer.scrollIntoView({ behavior: "smooth", block: "start" });
    document.dispatchEvent(new CustomEvent("mi-casa-segura:answer-shown", {
      detail: { id: faq.id, risk: riskMeta.key, source: faq.source }
    }));
  };

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

    searchController?.abort();
    const controller = new AbortController();
    searchController = controller;
    const currentRequest = ++requestSequence;
    const timeoutId = window.setTimeout(() => controller.abort(), API_TIMEOUT_MS);
    setBusy(true);

    try {
      const remoteResults = await fetchRemoteResults(rawQuery, controller.signal);
      if (currentRequest !== requestSequence
        || normalize(input.value) !== normalizedQuery) return;

      renderSuggestions(mergeResults(localResults, remoteResults), rawQuery);
    } catch (error) {
      if (error?.name === "AbortError" || currentRequest !== requestSequence) return;

      if (!localResults.length) {
        renderSuggestions(
          [],
          rawQuery,
          "No pudimos consultar la base técnica ampliada en este momento. Prueba nuevamente en unos segundos."
        );
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
      searchController?.abort();
      requestSequence += 1;
      hideSuggestions();
      emptyState.hidden = true;
      setBusy(false);
      return;
    }

    if (normalizedQuery.length < 2) {
      searchController?.abort();
      requestSequence += 1;
      renderSuggestions([], rawQuery, "Escribe al menos dos caracteres para buscar.");
      setBusy(false);
      return;
    }

    const localResults = getLocalResults(rawQuery);
    renderSuggestions(
      localResults,
      rawQuery,
      "Buscando en la base técnica ampliada…"
    );

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
      setActiveSuggestion(activeIndex < currentResults.length - 1
        ? activeIndex + 1
        : 0);
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      setActiveSuggestion(activeIndex > 0
        ? activeIndex - 1
        : currentResults.length - 1);
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
    if (!button) return;
    showAnswer(currentResults[Number(button.dataset.resultIndex)]);
  });

  popular?.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-faq-id]");
    if (!button) return;
    const faq = localFaqs.find((item) => item.id === button.dataset.faqId);
    showAnswer(faq ? enrichLocalFaq(faq) : null);
  });

  document.addEventListener("click", (event) => {
    if (!event.target.closest(".faq-search-box")) hideSuggestions();
  });
})();
