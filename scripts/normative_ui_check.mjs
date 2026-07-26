#!/usr/bin/env node

import assert from "node:assert/strict";
import process from "node:process";
import { chromium } from "playwright";

const baseUrl = process.env.APP_BASE_URL || "http://127.0.0.1:8000";

const elements = [
  { categoria: "Escaleras", elemento: "Escalera" },
  { categoria: "Escaleras", elemento: "Losa de escalera de concreto armado" },
  { categoria: "Cimentaciones", elemento: "Cimiento corrido" }
];

const parameters = [
  {
    id: "a010-escalera-contrahuella-maxima",
    categoria: "Escaleras",
    elemento: "Escalera",
    parametro: "Contrahuella o contrapaso",
    clasificacion: "maximo_normativo",
    valor: { tipo: "numero", valor: 0.18, unidad: "m", texto: "Contrahuella máxima: 0.18 m." },
    condiciones: ["Los contrapasos del tramo deben conservar una geometría uniforme."],
    fuente: {
      tipo: "RNE",
      norma: "A.010",
      denominacion: "Condiciones Generales de Diseño",
      dispositivo: "RM N.° 191-2021-VIVIENDA",
      numeral: null,
      numeral_confirmado: false,
      url_oficial: "https://www.gob.pe/institucion/vivienda/informes-publicaciones/2309793-reglamento-nacional-de-edificaciones-rne"
    },
    estado_revision: "piloto_verificado",
    advertencia: "No debe corregirse un tramo irregular únicamente con el acabado.",
    faq_relacionadas: ["q1375"],
    fecha_revision: "2026-07-26"
  },
  {
    id: "e060-escalera-garganta-sin-minimo-universal",
    categoria: "Escaleras",
    elemento: "Losa de escalera de concreto armado",
    parametro: "Espesor de garganta",
    clasificacion: "depende_calculo",
    valor: {
      tipo: "sin_valor_universal",
      texto: "No existe un espesor único aplicable a toda escalera; depende del cálculo estructural."
    },
    condiciones: ["La garganta se mide perpendicularmente al plano inclinado."],
    fuente: {
      tipo: "RNE",
      norma: "E.060",
      denominacion: "Concreto Armado",
      dispositivo: "DS N.° 010-2009-VIVIENDA",
      numeral: null,
      numeral_confirmado: false,
      url_oficial: "https://www.gob.pe/institucion/vivienda/informes-publicaciones/2309793-reglamento-nacional-de-edificaciones-rne"
    },
    estado_revision: "piloto_verificado",
    advertencia: "No debe publicarse un espesor como mínimo universal.",
    faq_relacionadas: ["q1422"],
    fecha_revision: "2026-07-26"
  },
  {
    id: "e050-cimiento-corrido-ancho",
    categoria: "Cimentaciones",
    elemento: "Cimiento corrido",
    parametro: "Ancho",
    clasificacion: "depende_calculo",
    valor: {
      tipo: "sin_valor_universal",
      texto: "El RNE no fija un ancho universal; se determina con suelo, cargas y diseño."
    },
    condiciones: ["Debe corresponder al terreno real y figurar en los planos."],
    fuente: {
      tipo: "RNE",
      norma: "E.050",
      denominacion: "Suelos y Cimentaciones",
      dispositivo: "RM N.° 406-2018-VIVIENDA",
      numeral: null,
      numeral_confirmado: false,
      url_oficial: "https://www.gob.pe/institucion/vivienda/informes-publicaciones/2309793-reglamento-nacional-de-edificaciones-rne"
    },
    estado_revision: "piloto_verificado",
    advertencia: "No debe copiarse el ancho de otra obra.",
    faq_relacionadas: ["q109"],
    fecha_revision: "2026-07-26"
  }
];

const normalize = (value = "") => String(value)
  .toLowerCase()
  .normalize("NFD")
  .replace(/[\u0300-\u036f]/g, "")
  .trim();

function filterParameters(url) {
  const query = normalize(url.searchParams.get("consulta") || "");
  const category = url.searchParams.get("categoria") || "";
  const element = url.searchParams.get("elemento") || "";
  const classification = url.searchParams.get("clasificacion") || "";

  return parameters.filter((item) => {
    if (category && item.categoria !== category) return false;
    if (element && item.elemento !== element) return false;
    if (classification && item.clasificacion !== classification) return false;
    if (!query) return true;
    const text = normalize([
      item.categoria,
      item.elemento,
      item.parametro,
      item.valor.texto,
      ...item.condiciones
    ].join(" "));
    return query.split(/\s+/).every((word) => text.includes(word));
  });
}

async function main() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    locale: "es-PE",
    timezoneId: "America/Lima"
  });
  const page = await context.newPage();
  const pageErrors = [];
  const consoleErrors = [];

  page.on("pageerror", (error) => pageErrors.push(error.message));
  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });

  await page.route("https://construccion-segura.onrender.com/api/v1/normativa/**", async (route) => {
    const url = new URL(route.request().url());
    if (url.pathname.endsWith("/elementos")) {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ version: "1.0.0-piloto", total_elementos: elements.length, elementos: elements })
      });
      return;
    }

    const filtered = filterParameters(url);
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        version: "1.0.0-piloto",
        advertencia_general: "Contenido piloto para consulta educativa.",
        total_encontrados: filtered.length,
        mostrados: filtered.length,
        resultados: filtered
      })
    });
  });

  await page.goto(new URL("/app/", `${baseUrl}/`).href, {
    waitUntil: "networkidle",
    timeout: 45_000
  });

  await page.waitForSelector("#normativeResults .normative-card", { timeout: 10_000 });
  assert.equal(await page.locator("#normativeResults .normative-card").count(), 3);
  assert.match(await page.locator("#normativeStatus").textContent(), /Base disponible/);

  await page.locator("#normativeSearch").fill("garganta");
  await page.waitForFunction(() => (
    document.querySelectorAll("#normativeResults .normative-card").length === 1
    && document.querySelector("#normativeResults")?.textContent?.includes("Espesor de garganta")
  ));

  await page.locator("#clearNormative").click();
  await page.waitForFunction(() => (
    document.querySelectorAll("#normativeResults .normative-card").length === 3
  ));

  await page.locator("#normativeClassification").selectOption("maximo_normativo");
  await page.waitForFunction(() => (
    document.querySelectorAll("#normativeResults .normative-card").length === 1
    && document.querySelector("#normativeResults")?.textContent?.includes("Contrahuella")
  ));

  const sourceLink = page.locator("#normativeResults .normative-source a").first();
  assert.equal(await sourceLink.getAttribute("target"), "_blank");
  assert.match(await sourceLink.getAttribute("rel"), /noopener/);

  const horizontalOverflow = await page.evaluate(() => (
    Math.max(document.documentElement.scrollWidth, document.body.scrollWidth) - window.innerWidth
  ));
  assert.ok(horizontalOverflow <= 1, `Desbordamiento horizontal: ${horizontalOverflow}px`);
  assert.deepEqual(pageErrors, []);
  assert.deepEqual(consoleErrors, []);

  await context.close();
  await browser.close();
  console.log("Normative frontend interaction passed on a 390px viewport.");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
