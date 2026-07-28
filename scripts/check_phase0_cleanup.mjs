import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const appDir = path.join(root, "frontend", "app");
const indexPath = path.join(appDir, "index.html");
const workerPath = path.join(root, "service-worker.js");

const fail = (message) => {
  throw new Error(message);
};

const legacyFiles = [
  "app-experience.js",
  "faq-data.js",
  "faq-risk-data.js",
  "faq-search.js",
  "faq-search-bootstrap.js",
  "problem-data.js",
  "risk-data.css"
];

for (const file of legacyFiles) {
  if (fs.existsSync(path.join(appDir, file))) {
    fail(`Archivo provisional todavía presente: frontend/app/${file}`);
  }
}

const index = fs.readFileSync(indexPath, "utf8");
const worker = fs.readFileSync(workerPath, "utf8");

const scriptSources = [...index.matchAll(/<script\s+[^>]*src="([^"]+)"/g)].map((match) => match[1]);
const styleSources = [...index.matchAll(/<link\s+[^>]*rel="stylesheet"[^>]*href="([^"]+)"/g)].map((match) => match[1]);

for (const [label, resources] of [["script", scriptSources], ["estilo", styleSources]]) {
  const seen = new Set();
  for (const resource of resources) {
    if (seen.has(resource)) fail(`Recurso ${label} duplicado en index.html: ${resource}`);
    seen.add(resource);
  }
}

const shellMatch = worker.match(/const APP_SHELL = \[([\s\S]*?)\];/);
if (!shellMatch) fail("No se pudo leer APP_SHELL del service worker.");

const shellResources = [...shellMatch[1].matchAll(/"([^"]+)"/g)].map((match) => match[1]);
const shellSet = new Set();
for (const resource of shellResources) {
  if (shellSet.has(resource)) fail(`Recurso duplicado en APP_SHELL: ${resource}`);
  shellSet.add(resource);
}

const canonicalAssets = [
  "/app/faq-data-v2.js?v=1",
  "/app/faq-search-v3.js?v=1",
  "/app/problem-evaluator.js?v=1",
  "/app/home-navigation.js?v=1",
  "/app/work-profile.js?v=1",
  "/app/risk-evaluator.js?v=1",
  "/app/stage-expander.js?v=1",
  "/app/stage-view-controller.js?v=1",
  "/app/help-center.js?v=1",
  "/app/professional-help.js?v=1",
  "/app/related-questions.js?v=1"
];

for (const asset of canonicalAssets) {
  if (!shellSet.has(asset)) fail(`El service worker no precarga el módulo estable: ${asset}`);
}

console.log(
  `Limpieza Fase 0 válida: ${legacyFiles.length} archivos provisionales ausentes, ` +
  `${scriptSources.length} scripts y ${shellResources.length} recursos de caché sin duplicados.`
);
