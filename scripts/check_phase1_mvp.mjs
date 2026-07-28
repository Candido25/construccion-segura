import fs from "node:fs";
import vm from "node:vm";

const read = (path) => fs.readFileSync(path, "utf8");
const fail = (message) => {
  console.error(`ERROR: ${message}`);
  process.exit(1);
};

const checklistCode = read("frontend/app/critical-checklists.js");
const sandbox = {
  window: { localStorage: {} },
  document: { getElementById: () => null },
  console
};
vm.createContext(sandbox);
vm.runInContext(checklistCode, sandbox, { filename: "critical-checklists.js" });

const checklists = sandbox.window.MI_CASA_SEGURA_CRITICAL_CHECKLISTS;
if (!Array.isArray(checklists) || checklists.length !== 8) {
  fail("La Fase 1 debe tener exactamente ocho listas críticas iniciales.");
}

const requiredChecklistIds = new Set([
  "antes-excavar",
  "antes-vaciar-concreto",
  "antes-tapar-instalaciones",
  "antes-retirar-puntales",
  "antes-tarrajear",
  "antes-energizar",
  "antes-recibir-etapa",
  "despues-evento"
]);

for (const checklist of checklists) {
  if (!requiredChecklistIds.delete(checklist.id)) fail(`Lista inesperada o duplicada: ${checklist.id}.`);
  if (!checklist.title || !checklist.summary || !Array.isArray(checklist.items) || checklist.items.length < 5) {
    fail(`La lista ${checklist.id} no tiene contenido suficiente.`);
  }
}
if (requiredChecklistIds.size) fail(`Faltan listas: ${[...requiredChecklistIds].join(", ")}.`);

if (!checklistCode.includes("mi-casa-segura-critical-checklists-v1")) {
  fail("Las listas no usan almacenamiento local versionado.");
}
if (!checklistCode.includes("reviewedAt") || !checklistCode.includes("Reiniciar esta lista")) {
  fail("Las listas no registran fecha o no permiten reinicio individual.");
}
if (!checklistCode.includes("mi-casa-segura:checklists-updated")) {
  fail("Las listas no notifican cambios a la personalización.");
}

const personalization = read("frontend/app/work-personalization.js");
for (const stage of [
  "planning", "excavation", "foundations", "structure",
  "installations", "finishes", "maintenance"
]) {
  if (!personalization.includes(`${stage}:`)) fail(`Mi obra no personaliza la etapa ${stage}.`);
}
if (!personalization.includes("mi-casa-segura:recommend-checklist")) {
  fail("Mi obra no recomienda una lista crítica.");
}

const stageEnhancements = read("frontend/app/stage-enhancements.js");
const stageIds = [
  "antes-construir", "terreno-movimiento", "cimentaciones", "columnas-muros",
  "vigas-techos", "sanitarias", "electricas", "impermeabilizacion",
  "acabados", "ampliaciones", "seguridad", "mantenimiento"
];
for (const id of stageIds) {
  if (!stageEnhancements.includes(`${JSON.stringify(id)}:`) && !stageEnhancements.includes(`${id}:`)) {
    fail(`La etapa ${id} no tiene alertas y accesos relacionados.`);
  }
}
for (const token of ["open-checklist", "faqSearch", "normativeSearch", "stage-support-panel"]) {
  if (!stageEnhancements.includes(token)) fail(`Falta integración de etapas: ${token}.`);
}

const problemEvaluator = read("frontend/app/problem-evaluator.js");
const problemIds = [
  "grietas", "terreno", "estructura-intervenida", "humedad", "concreto",
  "desague", "electricidad", "gas", "desprendimiento", "post-evento"
];
for (const id of problemIds) {
  if (!problemEvaluator.includes(`id: "${id}"`)) fail(`Falta la categoría de problema ${id}.`);
}
if (!problemEvaluator.includes("MI_CASA_SEGURA_PROBLEM_COUNT = problems.length")) {
  fail("El evaluador no publica el conteo de categorías para control de calidad.");
}
for (const risk of ["green", "yellow", "red"]) {
  if (!problemEvaluator.includes(`${risk}: {`)) fail(`El evaluador no presenta el nivel ${risk}.`);
}

const searchInsights = read("frontend/app/search-insights.js");
if (!searchInsights.includes("mi-casa-segura-search-gaps-v1")) {
  fail("El buscador no registra localmente consultas sin resultado.");
}
if (!searchInsights.includes("corrections") || !searchInsights.includes("No encontramos una pregunta")) {
  fail("El buscador no contempla errores simples o brechas de contenido.");
}

const professionalHelp = read("frontend/app/professional-help.js");
for (const token of [
  "Origen: buscador de preguntas",
  "Etapa relacionada",
  "Nivel mostrado por la aplicación",
  "Servicio sugerido",
  "mi-casa-segura-work-profile-v1"
]) {
  if (!professionalHelp.includes(token)) fail(`La ayuda profesional no incluye: ${token}.`);
}

const privacy = read("politica-privacidad.html");
for (const token of [
  "avance de las listas de verificación",
  "búsquedas que no encuentran una respuesta",
  "no se envía automáticamente"
]) {
  if (!privacy.includes(token)) fail(`La política de privacidad no informa: ${token}.`);
}

const serviceWorker = read("service-worker.js");
if (!serviceWorker.includes('CACHE_VERSION = "mi-casa-segura-pwa-v25"')) {
  fail("El MVP funcional debe usar la caché v25.");
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

console.log(`Fase 1 válida: ${checklists.length} listas críticas, ${problemIds.length} categorías de problemas, personalización, doce etapas vinculadas, brechas de búsqueda y ayuda contextual.`);
