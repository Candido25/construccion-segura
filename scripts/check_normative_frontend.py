from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "frontend" / "app"
INDEX = APP / "index.html"
MODULE = APP / "normative-module.js"
STYLES = APP / "normative.css"
SERVICE_WORKER = ROOT / "service-worker.js"


REQUIRED_IDS = {
    "normativeForm",
    "normativeSearch",
    "normativeCategory",
    "normativeElement",
    "normativeClassification",
    "normativeResults",
    "normativeEmpty",
    "normativeStatus",
    "normativeNotice",
    "retryNormative",
}

REQUIRED_MODULE_TOKENS = {
    "/api/v1/normativa/elementos",
    "/api/v1/normativa/parametros",
    "AbortController",
    "localStorage",
    "escapeHtml",
    "cache: \"no-store\"",
    "aria-busy",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    for path in (INDEX, MODULE, STYLES, SERVICE_WORKER):
        require(path.is_file(), f"Falta el archivo requerido: {path.relative_to(ROOT)}")

    index_text = INDEX.read_text(encoding="utf-8")
    module_text = MODULE.read_text(encoding="utf-8")
    styles_text = STYLES.read_text(encoding="utf-8")
    worker_text = SERVICE_WORKER.read_text(encoding="utf-8")

    for element_id in REQUIRED_IDS:
        require(
            f'id="{element_id}"' in index_text,
            f"Falta el elemento #{element_id} en frontend/app/index.html",
        )

    require(
        'href="normative.css?v=1"' in index_text,
        "La interfaz no carga normative.css?v=1.",
    )
    require(
        'src="normative-module.js?v=1"' in index_text,
        "La interfaz no carga normative-module.js?v=1.",
    )

    for token in REQUIRED_MODULE_TOKENS:
        require(token in module_text, f"El módulo normativo no contiene: {token}")

    require(
        "innerHTML = payload" not in module_text,
        "No se debe insertar directamente una respuesta de la API en innerHTML.",
    )
    require(
        ".normative-card" in styles_text and "@media (min-width: 720px)" in styles_text,
        "Faltan estilos de tarjetas o adaptación responsive.",
    )
    require(
        'CACHE_VERSION = "mi-casa-segura-pwa-v18"' in worker_text,
        "El service worker debe usar la caché v18.",
    )
    require(
        '"/app/normative.css?v=1"' in worker_text,
        "El service worker no precarga normative.css.",
    )
    require(
        '"/app/normative-module.js?v=1"' in worker_text,
        "El service worker no precarga normative-module.js.",
    )

    print(
        "Módulo normativo frontend válido:",
        f"{len(REQUIRED_IDS)} controles,",
        "API versionada, caché local y PWA v18.",
    )


if __name__ == "__main__":
    main()
