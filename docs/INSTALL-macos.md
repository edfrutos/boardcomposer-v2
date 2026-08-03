# Instalar BoardComposer Studio en macOS

> Esta guía solo aplica a releases sin firmar. Desde `v0.3.3` (`DT-0011`
> resuelta el 01/08/2026), `package-studio.yml` firma y notariza cada
> release cuando los secrets de Apple están cargados — si la tuya lo está,
> este fichero ni siquiera se publica junto al `.dmg` (compruébalo en los
> *assets* de la release). Sigue existiendo para builds antiguas o para el
> caso en que los secrets falten en el futuro.

Esta build **no está firmada con un certificado de Apple**, así que macOS
avisará la primera vez. No es un fallo de la aplicación ni una señal de que
algo vaya mal: es el comportamiento normal de Gatekeeper con cualquier
programa descargado que no venga de la App Store ni de un desarrollador
registrado en Apple.

## Instalación

1. Descarga `BoardComposerStudio-macos.dmg` desde la release y ábrelo (monta un volumen con la app y un acceso directo a `Aplicaciones`).
2. Arrastra `BoardComposerStudio.app` sobre el icono de `Aplicaciones` dentro del propio volumen montado, luego expúlsalo.
3. Abre el Terminal y ejecuta:

       xattr -dr com.apple.quarantine /Applications/BoardComposerStudio.app

4. Abre la aplicación con normalidad.

Sin el paso 3 verás *"No se puede abrir porque Apple no puede comprobar que
no contiene software malicioso"*.

### Alternativa sin Terminal

Si prefieres no usar comandos: **clic derecho** sobre la aplicación →
**Abrir** → **Abrir** en el diálogo. Hay que hacerlo solo la primera vez.

## Qué hace ese comando, exactamente

Al descargar un fichero, macOS le pone una marca llamada
`com.apple.quarantine`. Cuando abres algo que la lleva, Gatekeeper comprueba
si está firmado por un desarrollador identificado por Apple y notarizado; si
no lo está, bloquea la apertura. `xattr -dr` quita esa marca, y con ella la
comprobación.

Es la razón de que una build compilada por ti en tu propio Mac
(`make package`) se abra sin ningún aviso: nunca pasó por una descarga, así
que nunca llevó la marca. El binario es exactamente el mismo.

## Lo que esto no arregla

Quitar la cuarentena desactiva la verificación **para este fichero
concreto**. Hazlo solo con aplicaciones cuyo origen conozcas — en este caso,
una build generada por GitHub Actions a partir del código de este
repositorio, cuyo registro completo es público en la pestaña *Actions*.

La solución de verdad es firmar con un certificado **Developer ID
Application** y notarizar — ya en marcha desde `v0.3.3` (`DT-0011`,
`docs/masterplan/DOC-006-DeudaTecnica.md`, `scripts/sign_and_notarize.sh`).
Si estás leyendo esto es porque tu release concreta no llevaba los secrets
de firma cargados al publicarse (build antigua, o un fallo puntual de
configuración) — no porque la firma no exista todavía.

## Requisitos

- macOS con Apple Silicon (arm64). No hay build para Intel ni para
  Windows/Linux.
