import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const currentFile = fileURLToPath(import.meta.url);
const root = path.resolve(path.dirname(currentFile), "..");
const appDir = path.join(root, "frontend", "app");

const fail = (message) => {
  console.error(`ERROR: ${message}`);
  process.exit(1);
};

const read = (relativePath) => fs.readFileSync(path.join(root, relativePath), "utf8");

const index = read("frontend/app/index.html");
const serviceWorker = read("frontend/service-worker.js");

const requiredStyles = [
  "brand.css?v=20260714-1",
  "app.css?v=2",
  "faq.css?v=1",
  "normative.css?v=1",
  "app-experience.css?v=1",
  "faq-answer-v2.css?v=1"
];

const requiredScripts = [
  "faq-data-v2.js?v=1",
  "faq-search-v3.js?v=1",
  "home-navigation.js?v=1",
  "work-profile.js?v=1",
  "risk-evaluator.js?v=1",
  "normative-module.js?v=1",
  "app.js?v=1",
  "modules-rne.js?v=1"
];

for (const resource of [...requiredStyles, ...requiredScripts]) {
  if (!index.includes(resource)) fail(`index.html no carga ${resource}.`);
}

if (index.includes("app-experience.js")) {
  fail("index.html todavía carga el módulo experimental app-experience.js.");
}

for (const label of ["Inicio", "Guía", "Consultar", "Mi obra", "Ayuda"]) {
  if (!index.includes(`>${label}<`)) fail(`Falta la sección principal ${label}.`);
}

for (const route of ["construir", "duda", "problema"]) {
  if (!index.includes(`data-app-route=\"${route}\"`)) {
    fail(`Falta la ruta de usuario ${route}.`);
  }
}

const faqCode = read("frontend/app/faq-data-v2.js");
const sandbox = { window: {} };
vm.createContext(sandbox);
vm.runInContext(faqCode, sandbox, { filename: "faq-data-v2.js" });

const faqs = sandbox.window.MI_CASA_SEGURA_FAQS;
if (!Array.isArray(faqs) || faqs.length < 14) {
  fail("La base destacada debe contener por lo menos 14 preguntas revisadas.");
}

const validRisks = new Set(["green", "yellow", "red"]);
const requiredFaqFields = [
  "id",
  "category",
  "stage",
  "system",
  "classification",
  "risk",
  "reviewedAt",
  "editorialStatus",
  "question",
  "quick",
  "review",
  "avoid",
  "standard",
  "professional"
];

const ids = new Set();
for (const faq of faqs) {
  for (const field of requiredFaqFields) {
    const value = faq[field];
    if (value === undefined || value === null || value === "") {
      fail(`La pregunta ${faq.id || "sin ID"} no tiene el campo ${field}.`);
    }
  }

  if (ids.has(faq.id)) fail(`ID de pregunta duplicado: ${faq.id}.`);
  ids.add(faq.id);

  if (!validRisks.has(faq.risk)) fail(`Riesgo inválido en ${faq.id}: ${faq.risk}.`);
  if (faq.editorialStatus !== "approved") {
    fail(`La pregunta destacada ${faq.id} no está aprobada editorialmente.`);
  }
  if (!Array.isArray(faq.review) || faq.review.length === 0) {
    fail(`La pregunta ${faq.id} no contiene controles de revisión.`);
  }
}

const faqSearch = read("frontend/app/faq-search-v3.js");
const riskEvaluator = read("frontend/app/risk-evaluator.js");
const homeNavigation = read("frontend/app/home-navigation.js");
const workProfile = read("frontend/app/work-profile.js");

if (!faqSearch.includes("mi-casa-segura:faq-shown")) {
  fail("El buscador no emite el evento de respuesta seleccionada.");
}
if (!riskEvaluator.includes("mi-casa-segura:faq-shown")) {
  fail("El evaluador de riesgo no consume el evento de respuesta.");
}
if (/classifyRisk|redSignals|yellowSignals/.test(riskEvaluator)) {
  fail("El evaluador de riesgo no debe clasificar por palabras clave.");
}
if (!homeNavigation.includes("mi-casa-segura:open-work-profile")) {
  fail("La navegación no coordina la apertura de Mi obra.");
}
if (!workProfile.includes("mi-casa-segura-work-profile-v1")) {
  fail("Mi obra no utiliza la clave local versionada.");
}

for (const resource of [
  "/app/faq-data-v2.js?v=1",
  "/app/faq-search-v3.js?v=1",
  "/app/home-navigation.js?v=1",
  "/app/work-profile.js?v=1",
  "/app/risk-evaluator.js?v=1",
  "/app/faq-answer-v2.css?v=1"
]) {
  if (!serviceWorker.includes(resource)) {
    fail(`El service worker no guarda ${resource} para uso sin conexión.`);
  }
}

if (!serviceWorker.includes('mi-casa-segura-pwa-v20')) {
  fail("La caché pública no corresponde a la versión v20 de estabilización.");
}

for (const file of [
  "faq-data-v2.js",
  "faq-search-v3.js",
  "home-navigation.js",
  "work-profile.js",
  "risk-evaluator.js",
  "faq-answer-v2.css"
]) {
  if (!fs.existsSync(path.join(appDir, file))) fail(`No existe frontend/app/${file}.`);
}

console.log(`Arquitectura de Mi Casa Segura validada: ${faqs.length} preguntas destacadas.`);
