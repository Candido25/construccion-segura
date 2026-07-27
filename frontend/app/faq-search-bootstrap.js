(async () => {
  const loadStyle = (href) => {
    if (document.querySelector(`link[href="${href}"]`)) return;
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = href;
    document.head.append(link);
  };

  const loadScript = (src) => new Promise((resolve, reject) => {
    if (document.querySelector(`script[src="${src}"]`)) {
      resolve();
      return;
    }
    const script = document.createElement("script");
    script.src = src;
    script.onload = resolve;
    script.onerror = reject;
    document.head.append(script);
  });

  loadStyle("/app/risk-data.css?v=1");

  try {
    await loadScript("/app/faq-risk-data.js?v=1");
    await Promise.all([
      loadScript("/app/risk-evaluator.js?v=1"),
      loadScript("/app/professional-help.js?v=1")
    ]);
    await loadScript("/app/faq-search.js?v=3");
  } catch (error) {
    console.error("No se pudo iniciar el buscador estructurado.", error);
  }
})();
