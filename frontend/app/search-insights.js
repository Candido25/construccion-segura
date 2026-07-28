(() => {
  const STORAGE_KEY = "mi-casa-segura-search-gaps-v1";
  const input = document.getElementById("faqSearch");
  const emptyState = document.getElementById("faqEmpty");
  if (!input || !emptyState) return;

  const corrections = new Map([
    ["escalra", "escalera"],
    ["escaleraa", "escalera"],
    ["gargnta", "garganta"],
    ["simientacion", "cimentación"],
    ["cimentasion", "cimentación"],
    ["zaptata", "zapata"],
    ["sapatas", "zapatas"],
    ["rajadra", "rajadura"],
    ["raajadura", "rajadura"],
    ["desaguee", "desagüe"],
    ["termomagnetca", "termomagnética"],
    ["diferensial", "diferencial"],
    ["salitree", "salitre"],
    ["tarajeo", "tarrajeo"],
    ["tarrageo", "tarrajeo"],
    ["encofradoo", "encofrado"],
    ["puntlaes", "puntales"],
    ["columa", "columna"],
    ["vigaa", "viga"],
    ["losaa", "losa"]
  ]);

  const normalize = (value = "") => String(value)
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9ñ\s]/g, " ")
    .replace(/\s+/g, " ")
    .trim();

  const readState = () => {
    try {
      const stored = window.localStorage.getItem(STORAGE_KEY);
      return stored ? JSON.parse(stored) : {};
    } catch {
      return {};
    }
  };

  const writeState = (state) => {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  };

  let correctionNote = null;
  let logTimer = null;
  let lastLoggedSignature = "";

  const showCorrection = (original, corrected) => {
    if (!correctionNote) {
      correctionNote = document.createElement("p");
      correctionNote.className = "search-correction-note";
      correctionNote.setAttribute("role", "status");
      input.closest(".faq-search-box")?.append(correctionNote);
    }
    correctionNote.textContent = `Corregimos “${original}” por “${corrected}” para ayudarte a buscar.`;
  };

  document.addEventListener("input", (event) => {
    if (event.target !== input) return;
    const originalValue = input.value;
    const tokens = originalValue.split(/(\s+)/);
    let changed = false;

    const correctedTokens = tokens.map((token) => {
      const key = normalize(token);
      if (!key || !corrections.has(key)) return token;
      changed = true;
      return corrections.get(key);
    });

    if (changed) {
      const correctedValue = correctedTokens.join("");
      input.value = correctedValue;
      showCorrection(originalValue, correctedValue);
    } else if (correctionNote) {
      correctionNote.remove();
      correctionNote = null;
    }
  }, true);

  const recordGap = () => {
    const query = input.value.trim();
    const normalizedQuery = normalize(query);
    if (normalizedQuery.length < 2 || emptyState.hidden) return;
    if (!emptyState.textContent.includes("No encontramos una pregunta")) return;

    const signature = `${normalizedQuery}:${emptyState.textContent}`;
    if (signature === lastLoggedSignature) return;
    lastLoggedSignature = signature;

    const state = readState();
    const current = state[normalizedQuery] || {
      query,
      normalized: normalizedQuery,
      count: 0,
      firstSeenAt: new Date().toISOString()
    };
    current.query = query;
    current.count += 1;
    current.lastSeenAt = new Date().toISOString();
    state[normalizedQuery] = current;

    const ordered = Object.values(state)
      .sort((a, b) => String(b.lastSeenAt).localeCompare(String(a.lastSeenAt)))
      .slice(0, 100);
    writeState(Object.fromEntries(ordered.map((item) => [item.normalized, item])));

    document.dispatchEvent(new CustomEvent("mi-casa-segura:search-gap-recorded", {
      detail: { query, normalizedQuery, count: current.count }
    }));
  };

  const scheduleRecord = () => {
    window.clearTimeout(logTimer);
    logTimer = window.setTimeout(recordGap, 900);
  };

  const observer = new MutationObserver(scheduleRecord);
  observer.observe(emptyState, {
    childList: true,
    subtree: true,
    characterData: true,
    attributes: true,
    attributeFilter: ["hidden"]
  });

  input.addEventListener("input", () => {
    lastLoggedSignature = "";
    scheduleRecord();
  });
})();