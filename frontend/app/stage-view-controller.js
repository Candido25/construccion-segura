(() => {
  const moduleView = document.getElementById("moduleView");
  const moduleContent = document.getElementById("moduleContent");
  if (!moduleView || !moduleContent) return;

  const selectorsToHide = [
    ".welcome-card",
    ".app-choice-section",
    ".work-profile-card",
    ".quick-diagnostic",
    ".problem-evaluator-section",
    ".faq-section",
    ".normative-section",
    ".help-card"
  ];

  const preservedState = new Map();

  const enterModuleMode = () => {
    selectorsToHide.forEach((selector) => {
      const element = document.querySelector(selector);
      if (!element) return;
      if (!preservedState.has(element)) preservedState.set(element, element.hidden);
      element.hidden = true;
    });

    window.requestAnimationFrame(() => {
      moduleView.scrollIntoView({ behavior: "smooth", block: "start" });
      const heading = moduleContent.querySelector("h1");
      if (heading) {
        heading.setAttribute("tabindex", "-1");
        heading.focus({ preventScroll: true });
      }
    });
  };

  const leaveModuleMode = () => {
    preservedState.forEach((wasHidden, element) => {
      element.hidden = wasHidden;
    });
    preservedState.clear();
  };

  const synchronizeView = () => {
    if (moduleView.hidden) {
      leaveModuleMode();
    } else {
      enterModuleMode();
    }
  };

  const observer = new MutationObserver(synchronizeView);
  observer.observe(moduleView, { attributes: true, attributeFilter: ["hidden"] });
})();
