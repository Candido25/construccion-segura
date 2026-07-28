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
const exists = (relativePath) => fs.existsSync(path.join(root, relativePath));

const index = read("frontend/app/index.html");
const serviceWorker = read("service-worker.js");
const privacy = read("politica-privacidad.html");
const professionalHelp = read("frontend/app/professional-help.js");
const bootstrap = read("frontend/app/phase1-bootstrap.js");

const stableStyles = [
  "brand.css?v=20260714-1",
  "app.css?v=2",
  "faq.css?v=1",
  "normative.css?v=1",
  "app-experience.css?v=1",
  "faq-answer-v2.css?v=1",
  "problem-evaluator.css?v=1",
  "help-center.css?v=1",
  "related-questions.css?v=1"
];

const stableScripts = [
  "faq-data-v2.js?v=1",
  "faq-search-v3.js?v=1",
  "problem-evaluator.js?v=1",
  "home-navigation.js?v=1",
  "work-profile.js?v=1",
  "risk-evaluator.js?v=1",
  "normative-module.js?v=1",
  "app.js?v=1",
  "modules-rne.js?v=1",
  "stage-expander.js?v=1",
  "stage-view-controller.js?v=1",
  "help-center.js?v=1",
  "professional-help.js?v=1",
  "related-questions.js?v=1"
];

for (const resource of [...stableStyles, ...stableScripts]) {
  if (!index.includes(resource)) fail(`index.html no carga ${resource}.`);
}

if (index.includes("app-experience.js")) {
  fail("index.html todavía carga el controlador experimental app-experience.js.");
}

for (const label of ["Inicio", "Guía", "Consultar", "Mi obra", "Ayuda"]) {
  if (!index.includes(`>${label}<`)) fail(`Falta el acceso principal ${label}.`);
}

for (const route of ["construir", "duda", "problema"]) {
  if (!index.includes(`data-app-route="${route}"`)) fail(`Falta la ruta ${route}.`);
}

const faqCode = read("frontend/app/faq-data-v2.js");
const sandbox = { window: {} };
vm.createContext(sandbox);
vm.runInContext(faqCode, sandbox, { filename: "faq-data-v2.js" });
const faqs = sandbox.window.MI_CASA_SEGURA_FAQS;

if (!Array.isArray(faqs) || faqs.length < 14) {
  fail("La base destacada debe conservar por lo menos 14 preguntas.");
}

const validRisks = new Set(["green", "yellow", "red"]);
const ids = new Set();
for (const faq of faqs) {
  for (const field of [
    "id", "category", "stage", "system", "classification", "risk",
    "reviewedAt", "editorialStatus", "question", "quick", "review",
    "avoid", "standard", "professional"
  ]) {
    if (faq[field] === undefined || faq[field] === null || faq[field] === "") {
      fail(`La pregunta ${faq.id || "sin ID"} no tiene ${field}.`);
    }
  }
  if (ids.has(faq.id)) fail(`ID duplicado: ${faq.id}.`);
  ids.add(faq.id);
  if (!validRisks.has(faq.risk)) fail(`Riesgo inválido: ${faq.id}.`);
  if (faq.editorialStatus !== "approved") fail(`Pregunta no aprobada: ${faq.id}.`);
}

const stageExpander = read("frontend/app/stage-expander.js");
const stages = [
  "antes-construir", "terreno-movimiento", "cimentaciones", "columnas-muros",
  "vigas-techos", "sanitarias", "electricas", "impermeabilizacion",
  "acabados", "ampliaciones", "seguridad", "mantenimiento"
];
for (const stage of stages) {
  if (!stageExpander.includes(`"${stage}"`)) fail(`Falta la etapa ${stage}.`);
}
if (!stageExpander.includes("Vigas, escaleras y techos")) {
  fail("La guía no incorpora escaleras en la etapa estructural.");
}

const riskEvaluator = read("frontend/app/risk-evaluator.js");
const problemEvaluator = read("frontend/app/problem-evaluator.js");
if (/classifyRisk|redSignals|yellowSignals/.test(riskEvaluator)) {
  fail("El riesgo de respuestas no debe definirse mediante palabras clave.");
}
if (!problemEvaluator.includes("baseRisk") || !problemEvaluator.includes("yesRisk")) {
  fail("El evaluador de problemas no usa reglas explícitas.");
}

const phase1Files = [
  "frontend/app/phase1-bootstrap.js",
  "frontend/app/phase1-mvp.css",
  "frontend/app/critical-checklists.js",
  "frontend/app/work-personalization.js",
  "frontend/app/stage-enhancements.js",
  "frontend/app/search-insights.js"
];
for (const file of phase1Files) {
  if (!exists(file)) fail(`Falta ${file}.`);
}

for (const resource of [
  "/app/phase1-mvp.css?v=1",
  "/app/phase1-bootstrap.js?v=1",
  "/app/critical-checklists.js?v=1",
  "/app/work-personalization.js?v=1",
  "/app/stage-enhancements.js?v=1",
  "/app/search-insights.js?v=1"
]) {
  if (!serviceWorker.includes(resource)) fail(`El modo sin conexión no incluye ${resource}.`);
}

if (!serviceWorker.includes('CACHE_VERSION = "mi-casa-segura-pwa-v25"')) {
  fail("La PWA debe usar la caché v25.");
}

if (!professionalHelp.includes("phase1-bootstrap.js?v=1")) {
  fail("La aplicación no activa el arranque de la Fase 1.");
}
for (const resource of [
  "phase1-mvp.css?v=1",
  "critical-checklists.js?v=1",
  "work-personalization.js?v=1",
  "stage-enhancements.js?v=1",
  "search-insights.js?v=1"
]) {
  if (!bootstrap.includes(resource)) fail(`El arranque de Fase 1 no carga ${resource}.`);
}

if (!privacy.includes("Mi Casa Segura: Guía de Obra") || !privacy.includes("Mi obra")) {
  fail("La política de privacidad no describe la aplicación y el perfil local.");
}

console.log(`Arquitectura válida: ${faqs.length} preguntas, ${stages.length} etapas, evaluador explícito y módulos del MVP funcional.`);
