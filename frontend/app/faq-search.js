(() => {
  const faqs = Array.isArray(window.MI_CASA_SEGURA_FAQS) ? window.MI_CASA_SEGURA_FAQS : [];
  const input = document.getElementById("faqSearch");
  const suggestions = document.getElementById("faqSuggestions");
  const emptyState = document.getElementById("faqEmpty");
  const answer = document.getElementById("faqAnswer");
  const popular = document.getElementById("faqPopular");

  if (!input || !suggestions || !answer || !faqs.length) return;

  const normalize = (value = "") => value
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9ñ\s]/g, " ")
    .replace(/\s+/g, " ")
    .trim();

  const searchableText = new Map(
    faqs.map((faq) => [
      faq.id,
      normalize([faq.question, faq.category, ...(faq.aliases || [])].join(" "))
    ])
  );

  let activeIndex = -1;
  let currentResults = [];

  const escapeHtml = (value = "") => value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

  const scoreFaq = (faq, query) => {
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

  const getResults = (rawQuery) => {
    const query = normalize(rawQuery);
    if (!query) return [];

    return faqs
      .map((faq) => ({ faq, score: scoreFaq(faq, query) }))
      .filter((item) => item.score > 0)
      .sort((a, b) => b.score - a.score || a.faq.question.localeCompare(b.faq.question, "es"))
      .slice(0, 7)
      .map((item) => item.faq);
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

  const renderSuggestions = (results, query) => {
    currentResults = results;
    activeIndex = -1;
    input.removeAttribute("aria-activedescendant");

    if (!query) {
      suggestions.hidden = true;
      emptyState.hidden = true;
      return;
    }

    if (!results.length) {
      suggestions.hidden = true;
      emptyState.hidden = false;
      emptyState.textContent = "No encontramos una pregunta todavía. Prueba con otra palabra: zapata, grieta, techo, cable, salitre o desagüe.";
      return;
    }

    emptyState.hidden = true;
    suggestions.innerHTML = results.map((faq, index) => `
      <button id="faq-option-${index}" type="button" role="option" aria-selected="false" data-faq-id="${faq.id}">
        <span>${escapeHtml(faq.question)}</span>
        <small>${escapeHtml(faq.category)}</small>
      </button>
    `).join("");
    suggestions.hidden = false;
  };

  const listItems = (items = []) => items.map((item) => `<li>${escapeHtml(item)}</li>`).join("");

  const showAnswer = (faq) => {
    if (!faq) return;

    input.value = faq.question;
    suggestions.hidden = true;
    emptyState.hidden = true;
    activeIndex = -1;

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
    answer.hidden = false;
    answer.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  const chooseById = (faqId) => {
    showAnswer(faqs.find((faq) => faq.id === faqId));
  };

  input.addEventListener("input", () => {
    const query = input.value.trim();
    answer.hidden = true;
    renderSuggestions(getResults(query), query);
  });

  input.addEventListener("focus", () => {
    const query = input.value.trim();
    if (query) renderSuggestions(getResults(query), query);
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
      suggestions.hidden = true;
      emptyState.hidden = true;
      activeIndex = -1;
    }
  });

  suggestions.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-faq-id]");
    if (button) chooseById(button.dataset.faqId);
  });

  popular?.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-faq-id]");
    if (button) chooseById(button.dataset.faqId);
  });

  document.addEventListener("click", (event) => {
    if (!event.target.closest(".faq-search-box")) suggestions.hidden = true;
  });
})();
