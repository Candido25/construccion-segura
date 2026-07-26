#!/usr/bin/env python3
"""Migración temporal: web institucional en raíz, app en frontend/app y publicación en public/."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"
APP = FRONTEND / "app"
SCRIPTS = ROOT / "scripts"
WORKFLOWS = ROOT / ".github" / "workflows"
MANIFEST = SCRIPTS / "public_root_entries.txt"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def move_public_sources() -> tuple[str, ...]:
    if not APP.is_dir():
        raise RuntimeError("No se encontró frontend/app; se cancela la migración.")

    legacy = sorted(
        (path for path in FRONTEND.iterdir() if path.name != "app"),
        key=lambda path: path.name.casefold(),
    )
    if legacy:
        collisions = sorted(path.name for path in legacy if (ROOT / path.name).exists())
        if collisions:
            raise RuntimeError(f"Hay colisiones en la raíz: {collisions}")
        for source in legacy:
            shutil.move(str(source), str(ROOT / source.name))
        entries = {path.name for path in legacy}
    elif MANIFEST.is_file():
        entries = {
            line.strip()
            for line in MANIFEST.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
    else:
        raise RuntimeError("No hay fuentes que migrar ni manifiesto público existente.")

    if (ROOT / "CNAME").is_file():
        entries.add("CNAME")

    required = {
        "index.html",
        "styles.css",
        "hero.css",
        "conversion.css",
        "script.js",
        "assets",
        "errores",
        "casos",
        "service-worker.js",
        "site.webmanifest",
    }
    missing = sorted(required.difference(entries))
    if missing:
        raise RuntimeError(f"Faltan entradas públicas requeridas: {missing}")

    ordered = tuple(sorted(entries, key=str.casefold))
    write(
        MANIFEST,
        "# Entradas públicas de la web institucional ubicadas en la raíz.\n"
        "# frontend/app se empaqueta por separado como /app/.\n"
        + "\n".join(ordered),
    )
    return ordered


def write_prepare_script() -> None:
    write(
        SCRIPTS / "prepare_frontend.py",
        '''#!/usr/bin/env python3
"""Construye `public/` sin exponer el backend ni archivos internos."""

from __future__ import annotations

import shutil
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_ROOT = REPOSITORY_ROOT / "frontend"
APP_SOURCE = FRONTEND_ROOT / "app"
PUBLIC_ROOT = REPOSITORY_ROOT / "public"
MANIFEST_PATH = REPOSITORY_ROOT / "scripts" / "public_root_entries.txt"
FORBIDDEN_PUBLIC_ENTRIES = {
    ".git",
    ".github",
    "backend",
    "docs",
    "scripts",
    "requirements.txt",
    "AGENTS.md",
    "README.md",
    "public",
}


def load_public_entries() -> tuple[str, ...]:
    if not MANIFEST_PATH.is_file():
        raise FileNotFoundError(f"No se encontró el manifiesto público: {MANIFEST_PATH}")
    entries = tuple(
        line.strip()
        for line in MANIFEST_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    )
    if not entries:
        raise RuntimeError("El manifiesto público está vacío.")
    if len(entries) != len(set(entries)):
        raise RuntimeError("El manifiesto público contiene entradas duplicadas.")
    forbidden = sorted(set(entries).intersection(FORBIDDEN_PUBLIC_ENTRIES))
    if forbidden:
        raise RuntimeError(f"El manifiesto intenta publicar rutas internas: {forbidden}")
    return entries


def validate_source(entries: tuple[str, ...]) -> None:
    if not FRONTEND_ROOT.is_dir():
        raise FileNotFoundError(f"No se encontró {FRONTEND_ROOT}")
    if not APP_SOURCE.is_dir():
        raise FileNotFoundError(f"No se encontró el cliente dinámico: {APP_SOURCE}")

    unexpected = sorted(child.name for child in FRONTEND_ROOT.iterdir() if child.name != "app")
    if unexpected:
        raise RuntimeError(
            "frontend/ debe contener únicamente app/. Entradas inesperadas: "
            f"{unexpected}"
        )

    missing = [entry for entry in entries if not (REPOSITORY_ROOT / entry).exists()]
    if missing:
        raise FileNotFoundError(f"Faltan fuentes públicas en la raíz: {missing}")

    for required in ("index.html", "styles.css", "script.js"):
        if required not in entries:
            raise RuntimeError(f"El manifiesto no incluye {required}")


def copy_entry(source: Path, destination: Path) -> None:
    if source.is_dir():
        shutil.copytree(source, destination)
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def build_public_site() -> int:
    entries = load_public_entries()
    validate_source(entries)

    if PUBLIC_ROOT.exists():
        shutil.rmtree(PUBLIC_ROOT)
    PUBLIC_ROOT.mkdir(parents=True)

    for entry in entries:
        copy_entry(REPOSITORY_ROOT / entry, PUBLIC_ROOT / entry)
    copy_entry(APP_SOURCE, PUBLIC_ROOT / "app")

    leaked = sorted(name for name in FORBIDDEN_PUBLIC_ENTRIES if (PUBLIC_ROOT / name).exists())
    if leaked:
        raise RuntimeError(f"El paquete público contiene rutas internas: {leaked}")

    required_outputs = (
        PUBLIC_ROOT / "index.html",
        PUBLIC_ROOT / "app" / "index.html",
        PUBLIC_ROOT / "service-worker.js",
        PUBLIC_ROOT / "site.webmanifest",
    )
    missing_outputs = [str(path) for path in required_outputs if not path.is_file()]
    if missing_outputs:
        raise FileNotFoundError(f"El paquete público quedó incompleto: {missing_outputs}")

    return sum(1 for path in PUBLIC_ROOT.rglob("*") if path.is_file())


def main() -> int:
    total = build_public_site()
    print(
        "Paquete público preparado correctamente en public/: "
        f"{total} archivos, web institucional desde la raíz y app desde frontend/app/."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
''',
    )
    (SCRIPTS / "prepare_frontend.py").chmod(0o755)


def update_validator_scripts() -> None:
    check_site = SCRIPTS / "check_site.py"
    text = check_site.read_text(encoding="utf-8")
    text = text.replace(
        'SITE_ROOT = REPOSITORY_ROOT / "frontend"',
        'SITE_ROOT = REPOSITORY_ROOT / "public"',
    )
    text = text.replace("HTML files in frontend/.", "HTML files in public/.")
    check_site.write_text(text, encoding="utf-8")
    check_site.chmod(0o755)

    write(
        SCRIPTS / "run_frontend_validator.py",
        '''#!/usr/bin/env python3
"""Ejecuta los validadores sobre el paquete estático generado en `public/`."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

VALIDATORS = {"check_assets", "check_resources", "check_site"}
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ROOT = REPOSITORY_ROOT / "public"


def load_validator(name: str):
    path = REPOSITORY_ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"public_validator_{name}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"No se pudo cargar {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def display_relative(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(PUBLIC_ROOT).as_posix()
    except ValueError:
        return resolved.relative_to(REPOSITORY_ROOT).as_posix()


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in VALIDATORS:
        available = ", ".join(sorted(VALIDATORS))
        print(f"Uso: {Path(sys.argv[0]).name} <{available}>", file=sys.stderr)
        return 2
    if not PUBLIC_ROOT.is_dir():
        print(
            "No se encontró public/. Ejecuta primero scripts/prepare_frontend.py.",
            file=sys.stderr,
        )
        return 2

    name = sys.argv[1]
    validator = load_validator(name)
    validator.ROOT = PUBLIC_ROOT

    if name == "check_assets":
        validator.relative = display_relative
        validator.FORBIDDEN_PATHS = (
            REPOSITORY_ROOT / "review_photos",
            REPOSITORY_ROOT / "_incoming",
            REPOSITORY_ROOT / "debug.log",
            PUBLIC_ROOT / "review_photos",
            PUBLIC_ROOT / "_incoming",
            PUBLIC_ROOT / "debug.log",
        )

    return int(validator.main())


if __name__ == "__main__":
    raise SystemExit(main())
''',
    )
    (SCRIPTS / "run_frontend_validator.py").chmod(0o755)


def update_workflows() -> None:
    write(
        WORKFLOWS / "static.yml",
        '''# Deploy only the generated static package to GitHub Pages
name: Deploy static content to Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Prepare isolated public package
        run: python scripts/prepare_frontend.py

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Upload public package
        uses: actions/upload-pages-artifact@v3
        with:
          path: "./public"

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v5
''',
    )

    write(
        WORKFLOWS / "site-checks.yml",
        '''name: Site checks

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  validate-static-site:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4
        with:
          show-progress: false

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Prepare isolated public package
        run: python scripts/prepare_frontend.py

      - name: Ensure public identity uses Ingeniero
        run: |
          matches=$(grep -RIlE 'Ing\. Civil|Ingeniero civil|ingeniero civil' public --include='*.html' || true)
          if [ -n "$matches" ]; then
            echo "Retired specialty found in:"
            printf '%s\n' "$matches"
            exit 1
          fi

      - name: Validate local links and duplicate IDs
        run: python scripts/run_frontend_validator.py check_site

      - name: Validate backend API syntax
        run: python -m py_compile backend/api.py

      - name: Validate all public JavaScript syntax
        shell: bash
        run: |
          while IFS= read -r -d '' file; do
            node --check "$file"
          done < <(find public -type f -name '*.js' -print0)
''',
    )

    safety = WORKFLOWS / "phase-1-safety.yml"
    safety_text = safety.read_text(encoding="utf-8")
    safety_text = safety_text.replace("Prepare public frontend", "Prepare isolated public package")
    safety_text = safety_text.replace(
        "find frontend -type f -name '*.js'",
        "find public -type f -name '*.js'",
    )
    safety.write_text(safety_text, encoding="utf-8")

    visual = WORKFLOWS / "visual-regression.yml"
    visual_text = visual.read_text(encoding="utf-8")
    visual_text = visual_text.replace("Prepare public frontend", "Prepare isolated public package")
    visual_text = visual_text.replace("--directory frontend", "--directory public")
    visual.write_text(visual_text, encoding="utf-8")


def update_documentation() -> None:
    gitignore = ROOT / ".gitignore"
    ignore = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    if "/public/" not in ignore.splitlines():
        write(
            gitignore,
            ignore.rstrip() + "\n\n# Paquete generado para GitHub Pages\n/public/",
        )

    agents = ROOT / "AGENTS.md"
    agents_text = agents.read_text(encoding="utf-8")
    if "## Arquitectura oficial" not in agents_text:
        write(
            agents,
            agents_text.rstrip()
            + '''

## Arquitectura oficial

- La raíz del repositorio contiene la web institucional estática y sus recursos públicos.
- `frontend/app/` contiene el cliente dinámico Mi Casa Segura y el código reutilizable para la futura aplicación.
- `backend/` contiene FastAPI y las bases técnicas desplegadas en Render.
- `public/` es un paquete generado y no versionado; GitHub Pages publica exclusivamente ese paquete.
- Nunca publicar directamente la raíz completa ni exponer `backend/`, `scripts/`, `.github/` o archivos internos.
- Las funciones dinámicas deben consumir la API; la web institucional debe seguir siendo utilizable aunque Render no responda.
''',
        )

    write(
        ROOT / "README.md",
        '''# Construcción Segura

Sitio web de asesoría técnica para propietarios y familias que construyen, amplían o corrigen viviendas en el Perú.

## Responsable técnico

**Ing. Omar Oswaldo Alcantara Aquino · CIP N.° 364395**

## Arquitectura

- La web institucional estática vive en la raíz del repositorio.
- `frontend/app/` contiene Mi Casa Segura, el cliente dinámico que consume la API.
- `backend/` contiene FastAPI y las bases técnicas desplegadas en Render.
- `public/` se genera automáticamente y es el único contenido que GitHub Pages publica.

## Desarrollo local

```bash
python scripts/prepare_frontend.py
python -m http.server 8000 --directory public
```

Luego abre `http://localhost:8000`.

## Verificaciones

```bash
python scripts/prepare_frontend.py
python scripts/run_frontend_validator.py check_site
```

## Flujo de cambios

1. Crear una rama desde `main`.
2. Realizar cambios de contenido o código.
3. Ejecutar las verificaciones.
4. Abrir un pull request.
5. Fusionar solo después de revisar el resultado.

Las reglas permanentes están en `AGENTS.md`.
''',
    )

    write(
        ROOT / "docs" / "arquitectura.md",
        '''# Arquitectura de Construcción Segura

## Capas

1. **Web institucional estática:** archivos HTML, CSS, JavaScript y recursos ubicados en la raíz.
2. **Cliente dinámico:** `frontend/app/`, actualmente publicado como `/app/` y preparado para evolucionar hacia una aplicación independiente.
3. **Backend API First:** `backend/`, desplegado en Render y consumido por los clientes mediante HTTPS.
4. **Paquete de publicación:** `public/`, generado por `scripts/prepare_frontend.py` y excluido de Git.

## Flujo de publicación

- GitHub Pages ejecuta `scripts/prepare_frontend.py` y publica exclusivamente `public/`.
- Render despliega únicamente el backend y sus dependencias.
- La raíz completa del repositorio nunca se utiliza como artefacto de GitHub Pages.

## Regla para la futura aplicación

La lógica de interfaz reutilizable debe permanecer dentro de `frontend/app/`. La web institucional puede enlazar al aplicativo, pero no debe absorber su lógica de negocio.
''',
    )


def main() -> int:
    entries = move_public_sources()
    write_prepare_script()
    update_validator_scripts()
    update_workflows()
    update_documentation()
    print(f"Migración preparada con {len(entries)} entradas públicas en la raíz.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
