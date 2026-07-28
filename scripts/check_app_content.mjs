import fs from "node:fs";
import vm from "node:vm";

const DATA_PATH = "frontend/app/faq-data-v2.js";
const sandbox = { window: {} };
vm.createContext(sandbox);
vm.runInContext(fs.readFileSync(DATA_PATH, "utf8"), sandbox, { filename: DATA_PATH });

const faqs = sandbox.window.MI_CASA_SEGURA_FAQS;
if (!Array.isArray(faqs) || faqs.length < 14) {
  throw new Error("La aplicación debe conservar por lo menos 14 preguntas destacadas revisadas.");
}

const allowedRisks = new Set(["green", "yellow", "red"]);
const allowedClassifications = new Set([
  "minimo_rne",
  "maximo_rne",
  "formula_normativa",
  "condicion_normativa",
  "prohibicion",
  "recomendacion_practica",
  "el_plano_manda",
  "criterio_tecnico_revisado"
]);
const ids = new Set();

for (const faq of faqs) {
  const requiredTextFields = [
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
    "avoid",
    "standard",
    "professional"
  ];

  for (const field of requiredTextFields) {
    if (typeof faq[field] !== "string" || !faq[field].trim()) {
      throw new Error(`La pregunta ${faq.id || "sin ID"} no tiene un valor válido en ${field}.`);
    }
  }

  if (ids.has(faq.id)) throw new Error(`ID duplicado: ${faq.id}`);
  ids.add(faq.id);

  if (!allowedRisks.has(faq.risk)) {
    throw new Error(`Riesgo inválido para ${faq.id}: ${faq.risk}`);
  }
  if (!allowedClassifications.has(faq.classification)) {
    throw new Error(`Clasificación inválida para ${faq.id}: ${faq.classification}`);
  }
  if (faq.editorialStatus !== "approved") {
    throw new Error(`La pregunta ${faq.id} no está aprobada editorialmente.`);
  }
  if (!/^\d{4}-\d{2}-\d{2}$/.test(faq.reviewedAt)) {
    throw new Error(`Fecha de revisión inválida para ${faq.id}: ${faq.reviewedAt}`);
  }
  if (!Array.isArray(faq.review) || faq.review.length === 0) {
    throw new Error(`La pregunta ${faq.id} no contiene controles de revisión.`);
  }
  if (!Array.isArray(faq.aliases) || faq.aliases.length === 0) {
    throw new Error(`La pregunta ${faq.id} no contiene sinónimos de búsqueda.`);
  }
}

console.log(
  `Contenido válido: ${faqs.length} preguntas destacadas con esquema editorial, riesgo y fecha de revisión.`
);
