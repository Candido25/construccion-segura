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
const serviceWorker = read("service-worker.js");
const privacy = read("politica-privacidad.html");

const requiredStyles = [
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

const requiredScripts = [
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

for (const resource of [...requiredStyles, ...requiredScripts]) {
  if (!index.includes(resource)) fail(`index.html no carga ${resource}.`);
}

if (index.includes("app-experience.js")) {
  fail("index.html todavía carga el módulo experimental app-experience.js.");
}

const appIndex = index.indexOf('app.js?v=1');
const rneIndex = index.indexOf('modules-rne.js?v=1');
const stageIndex = index.indexOf('stage-expander.js?v=1');
if (!(appIndex >= 0 && rneIndex > appIndex && stageIndex > rneIndex)) {
  fail("El orden de carga debe ser app.js, modules-rne.js y luego stage-expander.js.");
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
const problemEvaluator = read("frontend/app/problem-evaluator.js");
const homeNavigation = read("frontend/app/home-navigation.js");
const workProfile = read("frontend/app/work-profile.js");
const stageExpander = read("frontend/app/stage-expander.js");
const stageView = read("frontend/app/stage-view-controller.js");
const helpCenter = read("frontend/app/help-center.js");
const professionalHelp = read("frontend/app/professional-help.js");
const relatedQuestions = read("frontend/app/related-questions.js");

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
if (!homeNavigation.includes("problemas-evaluador")) {
  fail("La ruta Tengo un problema no dirige al evaluador guiado.");
}
if (!workProfile.includes("mi-casa-segura-work-profile-v1")) {
  fail("Mi obra no utiliza la clave local versionada.");
}
if (!problemEvaluator.includes("const problems = [")) {
  fail("El evaluador no contiene una base estructurada de problemas.");
}
if (!problemEvaluator.includes("baseRisk") || !problemEvaluator.includes("yesRisk")) {
  fail("El evaluador no define riesgo mediante reglas explícitas en los datos.");
}
if (/classifyRisk|redSignals|yellowSignals/.test(problemEvaluator)) {
  fail("El evaluador guiado no debe decidir el riesgo mediante coincidencias de palabras.");
}
if (!stageView.includes("moduleView.scrollIntoView")) {
  fail("La vista de etapas no lleva al usuario al módulo abierto.");
}
if (!helpCenter.includes("politica-privacidad.html") || !helpCenter.includes("Qué no hace")) {
  fail("El centro de ayuda no explica el alcance o la privacidad.");
}
if (!professionalHelp.includes("51968481482") || !professionalHelp.includes("wa.me")) {
  fail("La orientación profesional no está contextualizada hacia WhatsApp.");
}
if (!relatedQuestions.includes("Preguntas relacionadas") || !relatedQuestions.includes("data-related-faq")) {
  fail("Las respuestas destacadas no incorporan navegación relacionada.");
}
if (!privacy.includes("Mi Casa Segura: Guía de Obra") || !privacy.includes("Mi obra")) {
  fail("La política de privacidad no describe el comportamiento de la aplicación.");
}

const requiredStages = [
  "antes-construir",
  "terreno-movimiento",
  "cimentaciones",
  "columnas-muros",
  "vigas-techos",
  "sanitarias",
  "electricas",
  "impermeabilizacion",
  "acabados",
  "ampliaciones",
  "seguridad",
  "mantenimiento"
];

for (const stage of requiredStages) {
  if (!stageExpander.includes(`\"${stage}\"`)) {
    fail(`La guía no incluye la etapa ${stage}.`);
  }
}

if (!stageExpander.includes("Vigas, escaleras y techos")) {
  fail("La guía no ha incorporado las escaleras a la etapa estructural correspondiente.");
}
if (!stageExpander.includes("stageGrid.innerHTML")) {
  fail("El expansor no reconstruye la navegación de las doce etapas.");
}

for (const resource of [
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
  "/app/related-questions.js?v=1",
  "/app/faq-answer-v2.css?v=1",
  "/app/problem-evaluator.css?v=1",
  "/app/help-center.css?v=1",
  "/app/related-questions.css?v=1",
  "/politica-privacidad.html"
]) {
  if (!serviceWorker.includes(resource)) {
    fail(`El service worker no guarda ${resource} para uso sin conexión.`);
  }
}

if (!serviceWorker.includes('mi-casa-segura-pwa-v24')) {
  fail("La caché pública no corresponde a la versión v24 del MVP.");
}

for (const file of [
  "faq-data-v2.js",
  "faq-search-v3.js",
  "problem-evaluator.js",
  "home-navigation.js",
  "work-profile.js",
  "risk-evaluator.js",
  "stage-expander.js",
  "stage-view-controller.js",
  "help-center.js",
  "professional-help.js",
  "related-questions.js",
  "faq-answer-v2.css",
  "problem-evaluator.css",
  "help-center.css",
  "related-questions.css"
]) {
  if (!fs.existsSync(path.join(appDir, file))) fail(`No existe frontend/app/${file}.`);
}

console.log(`Arquitectura de Mi Casa Segura validada: ${faqs.length} preguntas destacadas, evaluador guiado, ${requiredStages.length} etapas, ayuda y preguntas relacionadas.`);
