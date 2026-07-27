(() => {
  const faqs = Array.isArray(window.MI_CASA_SEGURA_FAQS)
    ? window.MI_CASA_SEGURA_FAQS
    : [];
  const answer = document.getElementById("faqAnswer");
  const input = document.getElementById("faqSearch");
  const suggestions = document.getElementById("faqSuggestions");

  if (!answer || !input || !suggestions || !faqs.length) return;

  const normalize = (value = "") => String(value)
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .trim();

  const findRelated = (current) => faqs
    .filter((faq) => faq.id !== current.id)
    .map((faq) => {
      let score = 0;
      if (faq.category === current.category) score += 5;
      if (faq.stage === current.stage) score += 4;
      if (faq.system === current.system) score += 3;
      if (faq.risk === current.risk) score += 1;
      return { faq, score };
    })
    .filter((item) => item.score > 0)
    .sort((a, b) => b.score - a.score || a.faq.question.localeCompare(b.faq.question, "es"))
    .slice(0, 3)
    .map((item) => item.faq);

  const openRelated = (faq) => {
    input.value = faq.question;
    input.dispatchEvent(new Event("input", { bubbles: true }));

    window.setTimeout(() => {
      const option = [...suggestions.querySelectorAll("button[data-result-index]")]
        .find((button) => normalize(button.querySelector("span")?.textContent) === normalize(faq.question));
      if (option) {
        option.click();
      } else {
        input.focus();
        suggestions.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
    }, 30);
  };

  document.addEventListener("mi-casa-segura:faq-shown", (event) => {
    const current = event.detail?.faq;
    answer.querySelector(".faq-related")?.remove();
    if (!current || current.source === "api") return;

    const related = findRelated(current);
    if (!related.length) return;

    const section = document.createElement("section");
    section.className = "faq-related";
    section.setAttribute("aria-labelledby", "faq-related-title");
    section.innerHTML = `
      <h4 id="faq-related-title">Preguntas relacionadas</h4>
      <div class="faq-related-list">
        ${related.map((faq) => `
          <button type="button" data-related-faq="${faq.id}">
            <span>${faq.question}</span>
            <small>${faq.category}</small>
          </button>
        `).join("")}
      </div>
    `;

    const disclaimer = answer.querySelector(".faq-disclaimer");
    if (disclaimer) {
      disclaimer.insertAdjacentElement("beforebegin", section);
    } else {
      answer.append(section);
    }

    section.addEventListener("click", (clickEvent) => {
      const button = clickEvent.target.closest("[data-related-faq]");
      if (!button) return;
      const faq = faqs.find((item) => item.id === button.dataset.relatedFaq);
      if (faq) openRelated(faq);
    });
  });
})();
