import fs from "node:fs";
import vm from "node:vm";

const readGlobal = (path, globalName) => {
  const sandbox = { window: {} };
  vm.runInNewContext(fs.readFileSync(path, "utf8"), sandbox, { filename: path });
  return sandbox.window[globalName];
};

const faqs = readGlobal("frontend/app/faq-data.js", "MI_CASA_SEGURA_FAQS");
const risks = readGlobal("frontend/app/faq-risk-data.js", "MI_CASA_SEGURA_FAQ_RISKS");

if (!Array.isArray(faqs) || faqs.length < 10) {
  throw new Error("La aplicación debe conservar por lo menos diez preguntas destacadas.");
}

const allowedRisks = new Set(["green", "yellow", "red"]);
const ids = new Set();

for (const faq of faqs) {
  if (!faq.id || !faq.question || !faq.quick || !faq.category) {
    throw new Error(`Pregunta incompleta: ${JSON.stringify(faq)}`);
  }
  if (ids.has(faq.id)) throw new Error(`ID duplicado: ${faq.id}`);
  ids.add(faq.id);

  const risk = risks?.[faq.id];
  if (!risk) throw new Error(`Falta clasificación de riesgo para ${faq.id}`);
  if (!allowedRisks.has(risk.risk)) throw new Error(`Riesgo inválido para ${faq.id}`);
  if (risk.reviewed !== true || !risk.reviewedAt) {
    throw new Error(`El riesgo de ${faq.id} no tiene revisión editorial completa.`);
  }
}

for (const id of Object.keys(risks || {})) {
  if (!ids.has(id)) throw new Error(`Clasificación huérfana: ${id}`);
}

console.log(`Contenido válido: ${faqs.length} preguntas destacadas con riesgo revisado.`);
