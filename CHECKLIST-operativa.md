# BoardComposer — Checklist operativa

**Versión revisada:** `0.3.36`
**Fecha de verificación:** 23/08/2026 (actualizada tras rehacer el build de la API en la VPS, `DT-0034`)
**Entorno de verificación:** sandbox Linux (Ubuntu 26.04, arm64) para el core/API/Studio local; runner autoalojado del Mac del usuario para CI y empaquetado — verificado vía `gh run watch`/logs, no solo asumido.

---

## ✅ Verificado automáticamente (entorno local)

| Check | Comando | Resultado |
|---|---|---|
| Entorno (`.venv`, Python 3.13.11) | `uv venv --python 3.13 .venv` | ✅ Recreado y funcional |
| Instalación | `pip install -e ".[dev]"` | ✅ Sin errores |
| Lint | `ruff check .` | ✅ "All checks passed!" |
| Tests | `pytest -q` | ✅ **1166 passed**, 0 fallos (336 s), repetido dos veces |
| CLI | `boardcomposer --csv data/samples/basic_boards.csv --max-length 3000 --max-width 600` | ✅ Genera solución real (3 tablas, score 70.3) |
| API — `/health` | `curl http://127.0.0.1:5050/health` | ✅ `{"status":"ok"}` |
| API — `/strategies` | `curl http://127.0.0.1:5050/strategies` | ✅ 3 estrategias listadas (`balanced`, `material`, `compact`) |
| Studio | `MainWindow(services=StudioServices())` (modo offscreen) | ✅ Instancia sin errores |
| Hook `git-secrets` | `git commit` | ✅ Binario instalado (faltaba), hook de pre-commit ya no lo bloquea |

**Nota:** el `.venv` original estaba roto (Python 3.14 en vez de 3.13, rutas absolutas de una ubicación anterior del repo). Se recreó desde cero con `uv` + Python 3.13.11 gestionado por `uv`. También se instalaron librerías de sistema faltantes para PySide6/Qt (`libglib2.0-0`, `libgl1`, `libegl1`, `libxkbcommon0`, etc.) vía `apt-get`.

---

## ✅ Verificado en real: CI/CD (21/08/2026)

| Check | Resultado |
|---|---|
| `ci.yml` migrado de `ubuntu-latest` a `[self-hosted, macOS]` | ✅ Commit `0732192`, release `v0.3.35` |
| `ci.yml` en el push a `main` | ✅ Verde, `5m25s` — venv, ruff format, ruff lint, 1166 tests, `check_project.py` |
| `package-studio.yml` en el tag `v0.3.35` | ✅ Verde, `42m14s` — build Nuitka, firma, notarización, staple, `.dmg`, release |
| Firma del `.app` sin el error de `v0.3.33` (`errSecInternalComponent` / cadena al certificado intermedio de Apple) | ✅ Confirmado en el log: `Timestamp=21 Aug 2026 at 13:27:34`, sin el error |
| Release publicada | ✅ [`v0.3.35`](https://github.com/edfrutos/boardcomposer-v2/releases/tag/v0.3.35), asset `BoardComposerStudio-macos.dmg` (firmado — no acompaña `INSTALL-macos.md`) |
| `.dmg` replicado en `edfrutos/boardcomposer-releases` (repo público) | ✅ Paso "Publish .dmg to the public releases repo" en verde |
| Gist público de versión actualizado | ✅ Paso "Update the public version Gist" en verde |
| Duplicado de run en el mismo push de tag (mismo patrón que `v0.3.31`) | ⚠️ Sigue ocurriendo — se canceló el run duplicado a mano (`gh run cancel`); no bloquea pero desperdicia ~40 min de Mac si no se detecta |
| Sincronización `main` ↔ `origin/main` | ✅ Sin commits de diferencia en ningún sentido, sin PRs abiertos |

El bloqueo original (*"recent account payments have failed or your spending limit needs to be increased"* en `ubuntu-latest`) queda resuelto: `ci.yml` ya no depende de minutos de pago de GitHub.

---

## 🖥️ App de escritorio (macOS)

- [x] El `.app` compila sin errores en el Mac real — verificado indirectamente vía CI (`package-studio.yml` en verde, `v0.3.35`), no con `make package` a mano
- [x] Firma y notarización vigentes — confirmado en el log (`Timestamp=21 Aug 2026...`, sin `errSecInternalComponent`)
- [x] El `.app` arranca con doble clic (no solo desde Terminal) — confirmado por el usuario contra `v0.3.35`; `DT-0023` sigue cerrado
- [x] Descargar el `.dmg` real de la release `v0.3.35` y comprobar que Gatekeeper no bloquea al abrirlo — confirmado por el usuario
- [ ] "Buscar actualizaciones" detecta, descarga y relanza correctamente desde una versión anterior instalada (`IDE-0043`/`IDE-0045`) — pendiente: se publica `v0.3.36` (solo número de versión) para que `v0.3.35` ya instalada tenga algo que ofrecer

## ☁️ Despliegue en producción

- [x] `bc.efjdefrutos.com` responde (`/health`) desde fuera de la VPS — confirmado 23/08/2026, `{"status":"ok"}`
- [x] `studio.efjdefrutos.com` (noVNC) carga y permite operar Studio desde el navegador, con paridad completa respecto a la app local — confirmado 23/08/2026 tras reconstruir el contenedor (`DT-0035`); estaba tan desfasado como la API (`DT-0034`), le faltaban `IDE-0039`/`IDE-0041`
- [x] Los contenedores de la VPS corren la versión actual (`v0.3.36`) — confirmado 23/08/2026 tras rehacer el build por SSH; estaba en `v0.3.9` (27 versiones de desfase, `DT-0034`)
- [x] `BOARDCOMPOSER_API_KEY` / auth básica de nginx siguen activas — confirmado 23/08/2026 (`/strategies` con clave devuelve `200`); `VNC_PASSWORD` (Studio/noVNC) sin comprobar en esta sesión

## 💳 Billing / Stripe

- [ ] Confirmar si `STRIPE_SECRET_KEY` / `STRIPE_PRICE_BASICO` / `STRIPE_PRICE_PRO` ya están configuradas en la VPS (según `MASTERPLAN.md`, seguían pendientes a fecha 08/08/2026)
- [ ] Probar un alta de cliente real con `scripts/manage_keys.py`

## 🤖 Proveedores de IA

- [ ] Al menos una clave real (Anthropic/OpenAI/Gemini) probada en producción reciente — Gemini y Ollama constaban como "sin verificar con credenciales/servidor reales" en el masterplan

## 📄 Repo / higiene

- [x] Decidir qué hacer con `CLAUDE.md` y `studio/STOP Por limite de gasto.png` (sin trackear en git) — `CLAUDE.md` trackeado en `8a786be`; la captura ya no existe en el árbol, nada que decidir
- [x] Investigar el duplicado de run en `package-studio.yml` al empujar un tag (`v0.3.31` y `v0.3.35`) — mismo `head_sha`, segundos de diferencia: síntoma típico de empujar rama+tag en el mismo `git push` (`--follow-tags`/`--atomic`), que GitHub a veces entrega como dos eventos `push` distintos para el mismo ref. Mitigado con `concurrency: {group: package-studio-${{ github.ref }}, cancel-in-progress: true}` — cancela el run duplicado más viejo en vez de dejar que corra la build firmada dos veces. **Pendiente de confirmar en el próximo tag empujado con rama+tag juntos.**

---

## Referencias

- Estado vivo funcionalidad por funcionalidad: `docs/masterplan/DOC-004-Backlog.md`
- Deuda técnica: `docs/masterplan/DOC-006-DeudaTecnica.md`
- Resumen y próxima decisión: `docs/masterplan/MASTERPLAN.md`
