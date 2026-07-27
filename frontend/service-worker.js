const CACHE_VERSION = "mi-casa-segura-pwa-v24";
const APP_SHELL = [
  "/",
  "/index.html",
  "/app/",
  "/app/index.html",
  "/app/app.css?v=2",
  "/app/faq.css?v=1",
  "/app/normative.css?v=1",
  "/app/app-experience.css?v=1",
  "/app/faq-answer-v2.css?v=1",
  "/app/problem-evaluator.css?v=1",
  "/app/help-center.css?v=1",
  "/app/related-questions.css?v=1",
  "/app/brand.css?v=20260714-1",
  "/app/app.js?v=1",
  "/app/modules-rne.js?v=1",
  "/app/stage-expander.js?v=1",
  "/app/stage-view-controller.js?v=1",
  "/app/faq-data-v2.js?v=1",
  "/app/faq-search-v3.js?v=1",
  "/app/problem-evaluator.js?v=1",
  "/app/home-navigation.js?v=1",
  "/app/work-profile.js?v=1",
  "/app/risk-evaluator.js?v=1",
  "/app/help-center.js?v=1",
  "/app/professional-help.js?v=1",
  "/app/related-questions.js?v=1",
  "/app/normative-module.js?v=1",
  "/offline.html",
  "/styles.css",
  "/site-pages.css",
  "/conversion.css",
  "/hero.css",
  "/site-global.js",
  "/recubrimiento-observation.js?v=20260723-1",
  "/losa-nervada-observation.js?v=20260724-1",
  "/viga-discontinuidad-observation.js?v=20260724-1",
  "/script.js",
  "/site.webmanifest",
  "/politica-privacidad.html",
  "/app-icon-192.png",
  "/app-icon-maskable-512.png",
  "/favicon-48.png",
  "/favicon-192.png",
  "/apple-touch-icon.png",
  "/assets/site-photos/web/hero-portada.webp",
  "/assets/brand/logo-marca-construccion-segura-transparente.png"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_VERSION)
      .then((cache) => cache.addAll(APP_SHELL))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys
          .filter((key) => key !== CACHE_VERSION)
          .map((key) => caches.delete(key))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("message", (event) => {
  if (event.data === "SKIP_WAITING") {
    self.skipWaiting();
  }
});

self.addEventListener("fetch", (event) => {
  const request = event.request;

  if (request.method !== "GET") return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  if (request.mode === "navigate") {
    event.respondWith(
      fetch(request)
        .then((response) => {
          if (response && response.ok) {
            const copy = response.clone();
            caches.open(CACHE_VERSION).then((cache) => cache.put(request, copy));
          }
          return response;
        })
        .catch(async () => {
          const cachedPage = await caches.match(request);
          return cachedPage || caches.match("/app/") || caches.match("/offline.html");
        })
    );
    return;
  }

  event.respondWith(
    caches.match(request).then((cachedResponse) => {
      const networkResponse = fetch(request)
        .then((response) => {
          if (response && response.ok) {
            const copy = response.clone();
            caches.open(CACHE_VERSION).then((cache) => cache.put(request, copy));
          }
          return response;
        })
        .catch(() => cachedResponse);

      return cachedResponse || networkResponse;
    })
  );
});
