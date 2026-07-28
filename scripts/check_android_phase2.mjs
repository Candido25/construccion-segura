import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const androidDir = path.join(root, "android");

const fail = (message) => {
  console.error(`ERROR: ${message}`);
  process.exit(1);
};

const read = (relativePath) => {
  const fullPath = path.join(root, relativePath);
  if (!fs.existsSync(fullPath)) fail(`Falta ${relativePath}.`);
  return fs.readFileSync(fullPath, "utf8");
};

const appBuild = read("android/app/build.gradle.kts");
const manifest = read("android/app/src/main/AndroidManifest.xml");
const strings = read("android/app/src/main/res/values/strings.xml");
const assetlinksTemplate = read("android/assetlinks.template.json");
const gitignore = read("android/.gitignore");

for (const token of [
  'applicationId = "pe.org.construccionsegura.app"',
  'namespace = "pe.org.construccionsegura.app"',
  "compileSdk = 36",
  "targetSdk = 36",
  "minSdk = 23",
  "versionCode = 1",
  'versionName = "1.0.0"',
  'androidbrowserhelper:2.7.2'
]) {
  if (!appBuild.includes(token)) fail(`La configuración Android no contiene: ${token}`);
}

if (!appBuild.includes("MCS_KEYSTORE_PATH") || !appBuild.includes("MCS_KEY_PASSWORD")) {
  fail("La firma de publicación no está preparada mediante variables privadas.");
}

for (const token of [
  'android.permission.INTERNET',
  'android:usesCleartextTraffic="false"',
  'com.google.androidbrowserhelper.trusted.LauncherActivity',
  'com.google.androidbrowserhelper.trusted.ManageDataLauncherActivity',
  'com.google.androidbrowserhelper.trusted.FocusActivity',
  'com.google.androidbrowserhelper.trusted.DelegationService',
  'android.support.customtabs.trusted.TRUSTED_WEB_ACTIVITY_SERVICE',
  'android.support.customtabs.trusted.DEFAULT_URL',
  'android.support.customtabs.trusted.MANAGE_SPACE_URL',
  'android:host="www.construccionsegura.org.pe"',
  'android:pathPrefix="/app"',
  'android:autoVerify="true"'
]) {
  if (!manifest.includes(token)) fail(`AndroidManifest.xml no contiene: ${token}`);
}

const permissions = [...manifest.matchAll(/<uses-permission\s+android:name="([^"]+)"/g)]
  .map((match) => match[1]);
if (permissions.length !== 1 || permissions[0] !== "android.permission.INTERNET") {
  fail(`La primera versión solo debe solicitar INTERNET. Encontrado: ${permissions.join(", ")}`);
}

for (const token of [
  "Mi Casa Segura",
  "https://www.construccionsegura.org.pe/app/",
  "delegate_permission/common.handle_all_urls"
]) {
  if (!strings.includes(token)) fail(`strings.xml no contiene: ${token}`);
}

const assetlinks = JSON.parse(assetlinksTemplate);
const target = assetlinks?.[0]?.target;
if (target?.package_name !== "pe.org.construccionsegura.app") {
  fail("La plantilla de Digital Asset Links usa un paquete incorrecto.");
}
if (!target?.sha256_cert_fingerprints?.includes("REEMPLAZAR_CON_HUELLA_SHA256_DE_PLAY_APP_SIGNING")) {
  fail("La plantilla debe conservar el marcador hasta recibir la huella de Play App Signing.");
}

for (const pattern of ["*.jks", "*.keystore", "signing.properties"]) {
  if (!gitignore.includes(pattern)) fail(`android/.gitignore no excluye ${pattern}.`);
}

const forbiddenNames = new Set(["signing.properties"]);
const forbiddenExtensions = new Set([".jks", ".keystore"]);
const walk = (directory) => {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      if (!["build", ".gradle", ".idea"].includes(entry.name)) walk(fullPath);
      continue;
    }
    if (forbiddenNames.has(entry.name) || forbiddenExtensions.has(path.extname(entry.name))) {
      fail(`Se encontró material de firma prohibido en el repositorio: ${path.relative(root, fullPath)}`);
    }
  }
};
walk(androidDir);

const liveAssetlinks = path.join(root, ".well-known", "assetlinks.json");
if (fs.existsSync(liveAssetlinks)) {
  const liveText = fs.readFileSync(liveAssetlinks, "utf8");
  if (liveText.includes("REEMPLAZAR_CON_HUELLA")) {
    fail("No se debe publicar Digital Asset Links con una huella de reemplazo.");
  }
}

console.log(
  "Proyecto Android válido: paquete pe.org.construccionsegura.app, API 36, " +
  "componentes completos de Android Browser Helper, TWA HTTPS, un solo permiso y firma privada excluida."
);
