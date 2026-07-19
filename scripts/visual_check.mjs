#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { chromium } from "playwright";

const currentBaseUrl = process.env.CURRENT_BASE_URL || "http://127.0.0.1:8000";
const baselineBaseUrl = process.env.BASELINE_BASE_URL || "http://127.0.0.1:8001";
const outputDirectory = path.resolve(process.env.VISUAL_OUTPUT_DIR || "visual-artifacts");

const profiles = [
  { name: "home-desktop", route: "/", width: 1440, height: 900 },
  { name: "home-tablet", route: "/", width: 768, height: 1024 },
  { name: "home-mobile", route: "/", width: 390, height: 844 },
  { name: "app-desktop", route: "/app/", width: 1440, height: 900 },
  { name: "app-mobile", route: "/app/", width: 390, height: 844 },
];

const results = [];
const failures = [];

function normalizeBaseUrl(value) {
  return value.endsWith("/") ? value.slice(0, -1) : value;
}

async function waitForDocumentFonts(page) {
  await page.evaluate(async () => {
    if (document.fonts?.ready) {
      await document.fonts.ready;
    }
  });
}

async function exercisePage(page) {
  await page.waitForLoadState("networkidle");
  await waitForDocumentFonts(page);

  await page.evaluate(async () => {
    const pause = (milliseconds) => new Promise((resolve) => setTimeout(resolve, milliseconds));
    const maximum = Math.max(
      document.documentElement.scrollHeight,
      document.body?.scrollHeight || 0
    );
    const step = Math.max(240, Math.floor(window.innerHeight * 0.72));

    for (let position = 0; position < maximum; position += step) {
      window.scrollTo(0, position);
      await pause(45);
    }

    window.scrollTo(0, maximum);
    await pause(180);
    window.scrollTo(0, 0);
    await pause(180);
  });

  await waitForDocumentFonts(page);
}

async function inspectPage(page, sameOrigin) {
  return page.evaluate((expectedOrigin) => {
    const root = document.documentElement;
    const body = document.body;
    const horizontalOverflow = Math.max(root.scrollWidth, body?.scrollWidth || 0) - window.innerWidth;

    const brokenImages = Array.from(document.images)
      .filter((image) => image.currentSrc && (image.naturalWidth === 0 || image.naturalHeight === 0))
      .map((image) => ({
        src: image.currentSrc,
        alt: image.alt || "",
      }));

    const hiddenRevealElements = Array.from(document.querySelectorAll(".reveal"))
      .filter((element) => {
        const style = getComputedStyle(element);
        const rect = element.getBoundingClientRect();
        const participatesInLayout =
          style.display !== "none" &&
          style.visibility !== "hidden" &&
          rect.width > 0 &&
          rect.height > 0;
        return participatesInLayout && Number.parseFloat(style.opacity || "1") < 0.99;
      })
      .map((element) => ({
        tag: element.tagName.toLowerCase(),
        id: element.id || "",
        className: element.className || "",
      }))
      .slice(0, 20);

    const requiredSelectors = location.pathname.startsWith("/app")
      ? [".app-header", ".app-brand", "main"]
      : [".site-header", ".hero", ".hero-media", ".hero-content", "main"];

    const missingRequiredSelectors = requiredSelectors.filter(
      (selector) => !document.querySelector(selector)
    );

    const sameOriginLinks = Array.from(document.querySelectorAll("link[href], script[src]"))
      .map((element) => {
        const raw = element.getAttribute("href") || element.getAttribute("src") || "";
        try {
          const url = new URL(raw, document.baseURI);
          return url.origin === expectedOrigin ? url.href : null;
        } catch {
          return null;
        }
      })
      .filter(Boolean);

    return {
      title: document.title,
      path: location.pathname,
      horizontalOverflow,
      brokenImages,
      hiddenRevealElements,
      missingRequiredSelectors,
      sameOriginResources: sameOriginLinks.length,
      documentHeight: Math.max(root.scrollHeight, body?.scrollHeight || 0),
    };
  }, sameOrigin);
}

async function captureVariant(browser, label, baseUrl, profile) {
  const normalizedBaseUrl = normalizeBaseUrl(baseUrl);
  const context = await browser.newContext({
    viewport: { width: profile.width, height: profile.height },
    deviceScaleFactor: 1,
    reducedMotion: "reduce",
    colorScheme: "light",
    locale: "es-PE",
    timezoneId: "America/Lima",
  });

  await context.addInitScript(() => {
    try {
      localStorage.setItem("cs_cookie_consent_v1", "necessary");
    } catch {
      // La página sigue siendo comprobable aunque el almacenamiento no esté disponible.
    }
  });

  const page = await context.newPage();
  const consoleErrors = [];
  const pageErrors = [];
  const sameOriginRequestFailures = [];
  const sameOriginHttpErrors = [];
  const expectedOrigin = new URL(normalizedBaseUrl).origin;

  page.on("console", (message) => {
    if (message.type() === "error") {
      consoleErrors.push(message.text());
    }
  });

  page.on("pageerror", (error) => {
    pageErrors.push(error.message);
  });

  page.on("requestfailed", (request) => {
    const url = request.url();
    if (url.startsWith(expectedOrigin)) {
      sameOriginRequestFailures.push({
        url,
        error: request.failure()?.errorText || "request failed",
      });
    }
  });

  page.on("response", (response) => {
    const url = response.url();
    if (url.startsWith(expectedOrigin) && response.status() >= 400) {
      sameOriginHttpErrors.push({
        url,
        status: response.status(),
      });
    }
  });

  await page.route("**/*", async (route) => {
    const url = new URL(route.request().url());
    if (url.origin !== expectedOrigin) {
      const resourceType = route.request().resourceType();
      const contentType =
        resourceType === "stylesheet"
          ? "text/css"
          : resourceType === "script"
            ? "application/javascript"
            : "text/plain";
      await route.fulfill({
        status: 200,
        contentType,
        body: "",
      });
      return;
    }
    await route.continue();
  });

  const targetUrl = new URL(profile.route, `${normalizedBaseUrl}/`).href;
  const response = await page.goto(targetUrl, {
    waitUntil: "domcontentloaded",
    timeout: 45_000,
  });

  if (!response || response.status() >= 400) {
    failures.push(`${label}/${profile.name}: navegación inválida a ${targetUrl}`);
  }

  await exercisePage(page);
  const inspection = await inspectPage(page, expectedOrigin);

  const directory = path.join(outputDirectory, label);
  await fs.mkdir(directory, { recursive: true });

  const viewportFile = path.join(directory, `${profile.name}-viewport.png`);
  const fullPageFile = path.join(directory, `${profile.name}-full.png`);
  await page.screenshot({ path: viewportFile, fullPage: false, animations: "disabled" });
  await page.screenshot({ path: fullPageFile, fullPage: true, animations: "disabled" });

  const record = {
    variant: label,
    profile: profile.name,
    url: targetUrl,
    viewport: { width: profile.width, height: profile.height },
    inspection,
    consoleErrors,
    pageErrors,
    sameOriginRequestFailures,
    sameOriginHttpErrors,
    screenshots: {
      viewport: path.relative(outputDirectory, viewportFile),
      fullPage: path.relative(outputDirectory, fullPageFile),
    },
  };
  results.push(record);

  if (inspection.horizontalOverflow > 1) {
    failures.push(
      `${label}/${profile.name}: desbordamiento horizontal de ${inspection.horizontalOverflow}px`
    );
  }
  if (inspection.brokenImages.length) {
    failures.push(`${label}/${profile.name}: imágenes rotas ${JSON.stringify(inspection.brokenImages)}`);
  }
  if (inspection.hiddenRevealElements.length) {
    failures.push(
      `${label}/${profile.name}: elementos reveal invisibles ${JSON.stringify(
        inspection.hiddenRevealElements
      )}`
    );
  }
  if (inspection.missingRequiredSelectors.length) {
    failures.push(
      `${label}/${profile.name}: faltan selectores ${inspection.missingRequiredSelectors.join(", ")}`
    );
  }
  if (consoleErrors.length) {
    failures.push(`${label}/${profile.name}: errores de consola ${JSON.stringify(consoleErrors)}`);
  }
  if (pageErrors.length) {
    failures.push(`${label}/${profile.name}: errores JavaScript ${JSON.stringify(pageErrors)}`);
  }
  if (sameOriginRequestFailures.length) {
    failures.push(
      `${label}/${profile.name}: solicitudes locales fallidas ${JSON.stringify(
        sameOriginRequestFailures
      )}`
    );
  }
  if (sameOriginHttpErrors.length) {
    failures.push(
      `${label}/${profile.name}: respuestas HTTP locales inválidas ${JSON.stringify(
        sameOriginHttpErrors
      )}`
    );
  }

  await context.close();
}

async function main() {
  await fs.rm(outputDirectory, { recursive: true, force: true });
  await fs.mkdir(outputDirectory, { recursive: true });

  const browser = await chromium.launch({ headless: true });
  try {
    for (const profile of profiles) {
      await captureVariant(browser, "current", currentBaseUrl, profile);
      await captureVariant(browser, "baseline", baselineBaseUrl, profile);
    }
  } finally {
    await browser.close();
  }

  const report = {
    generatedAt: new Date().toISOString(),
    currentBaseUrl,
    baselineBaseUrl,
    results,
    failures,
  };
  await fs.writeFile(
    path.join(outputDirectory, "browser-report.json"),
    `${JSON.stringify(report, null, 2)}\n`,
    "utf8"
  );

  if (failures.length) {
    console.error("Visual browser checks failed:");
    for (const failure of failures) {
      console.error(`- ${failure}`);
    }
    process.exit(1);
  }

  console.log(`Visual browser checks passed for ${profiles.length * 2} page variants.`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
