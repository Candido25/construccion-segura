(() => {
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
    script.defer = false;
    script.addEventListener("load", resolve, { once: true });
    script.addEventListener("error", () => reject(new Error(`No se pudo cargar ${src}`)), { once: true });
    document.body.append(script);
  });

  loadStyle("/app/phase1-mvp.css?v=1");

  const modules = [
    "/app/critical-checklists.js?v=1",
    "/app/work-personalization.js?v=1",
    "/app/stage-enhancements.js?v=1",
    "/app/search-insights.js?v=1"
  ];

  modules.reduce(
    (chain, src) => chain.then(() => loadScript(src)),
    Promise.resolve()
  ).catch((error) => console.error("No se pudieron activar todas las funciones de la Fase 1.", error));
})();