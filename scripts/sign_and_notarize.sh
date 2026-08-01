#!/usr/bin/env bash
#
# Signs, notarises and staples the BoardComposer Studio .app bundle.
#
# Gatekeeper only trusts certificates issued by Apple, so this needs a real
# Developer ID Application certificate — the one for distributing outside
# the App Store. A self-signed certificate changes nothing: the download
# still gets the "Apple cannot check it for malicious software" warning.
# Without the credentials below, CI skips this script and ships an unsigned
# build plus docs/INSTALL-macos.md (see DT-0011).
#
# Required environment:
#   APP_PATH            path to the .app bundle
#   SIGNING_IDENTITY    e.g. "Developer ID Application: Name (TEAMID)"
#   APPLE_ID            Apple account email
#   APPLE_TEAM_ID       10-character team identifier
#   APPLE_APP_PASSWORD  app-specific password, NOT the account password
#
# Usage: scripts/sign_and_notarize.sh

set -euo pipefail

: "${APP_PATH:?APP_PATH no definido}"
: "${SIGNING_IDENTITY:?SIGNING_IDENTITY no definido}"
: "${APPLE_ID:?APPLE_ID no definido}"
: "${APPLE_TEAM_ID:?APPLE_TEAM_ID no definido}"
: "${APPLE_APP_PASSWORD:?APPLE_APP_PASSWORD no definido}"

if [[ ! -d "$APP_PATH" ]]; then
  echo "No existe el bundle: $APP_PATH" >&2
  exit 1
fi

notarization_zip="$(dirname "$APP_PATH")/notarization-upload.zip"

echo "==> Limpiando atributos extendidos heredados"
# Defensa barata, aunque el diagnóstico de una vuelta anterior (ls -la@,
# file, codesign -dv sobre certifi/cacert.pem: 644, ASCII, sin xattrs) ya
# descartó que xattrs o el bit +x fueran la causa real del fallo de más
# abajo — se mantiene solo por si acaso, no hace daño.
xattr -cr "$APP_PATH"

echo "==> Moviendo a Resources/ los datos que Nuitka dejó sueltos en MacOS/"
# La causa real: codesign, al firmar el bundle exterior, exige que TODO
# fichero regular bajo Contents/MacOS/ sea código real (Mach-O) — cualquier
# dato plano ahí (p.ej. certifi/cacert.pem) falla con "code object is not
# signed at all" pase lo que pase con sus permisos o atributos, porque no
# es lo que codesign espera encontrar en esa carpeta. La convención de
# bundle de Apple ya sitúa los datos en Contents/Resources/, no junto al
# ejecutable — así que se mueven ahí y se deja un symlink relativo en el
# sitio original, para que el código Python que los localiza por ruta
# relativa a su propio paquete (certifi.where() resuelve cacert.pem junto a
# su __file__) los siga encontrando exactamente igual en tiempo de
# ejecución. Generalizado a cualquier fichero no-Mach-O bajo MacOS/, no
# solo a este caso concreto — si Nuitka deja otro dato suelto ahí en el
# futuro, queda cubierto igual.
macos_dir="$APP_PATH/Contents/MacOS"
resources_dir="$APP_PATH/Contents/Resources"
mkdir -p "$resources_dir"

while IFS= read -r -d '' f; do
  if file "$f" | grep -q "Mach-O"; then
    continue
  fi

  rel="${f#"$macos_dir"/}"
  dest="$resources_dir/$rel"
  mkdir -p "$(dirname "$dest")"
  mv "$f" "$dest"

  rel_dir="$(dirname "$rel")"
  up=""
  if [[ "$rel_dir" != "." ]]; then
    IFS='/' read -ra parts <<< "$rel_dir"
    for _ in "${parts[@]}"; do up="../$up"; done
  fi
  ln -s "${up}../Resources/$rel" "$f"
done < <(find "$macos_dir" -type f -print0)

echo "==> Firmando binarios internos"
# Inside-out, deliberately not --deep: Apple documents --deep as unsuitable
# for signing (it applies the same options to nested code that may need
# different ones, and silently skips some layouts). Every .so and .dylib is
# signed first, the bundle last — the outer signature seals hashes of what
# is inside, so anything signed afterwards would invalidate it.
while IFS= read -r binary; do
  codesign --force --timestamp --options runtime \
    --sign "$SIGNING_IDENTITY" "$binary"
done < <(find "$APP_PATH" -type f \( -name "*.dylib" -o -name "*.so" \))

cacert="$APP_PATH/Contents/MacOS/certifi/cacert.pem"
if [[ -e "$cacert" ]]; then
  echo "==> Diagnóstico de $cacert antes de firmar el bundle"
  ls -la@ "$cacert" || true
  file "$cacert" || true
  codesign -dv "$cacert" 2>&1 || true
fi

echo "==> Firmando el bundle"
# No entitlements on purpose: the app draws windows and makes outbound HTTPS
# calls, neither of which needs one outside the App Sandbox. If a future
# hardened-runtime failure demands one (allow-jit and friends), add it with
# the failing log in hand rather than pre-emptively — every entitlement
# widens what the app is allowed to do.
codesign --force --timestamp --options runtime \
  --sign "$SIGNING_IDENTITY" "$APP_PATH"

echo "==> Verificando la firma"
# Falla ruidosamente aquí antes que publicar un .app que Gatekeeper rechace
# en la máquina de quien lo descargue.
codesign --verify --strict --verbose=2 "$APP_PATH"

echo "==> Subiendo a notarizar (puede tardar varios minutos)"
# notarytool wants an archive, and ditto is the only archiver that preserves
# the bundle's symlinks and extended attributes intact.
ditto -c -k --keepParent "$APP_PATH" "$notarization_zip"

submit_output="$(xcrun notarytool submit "$notarization_zip" \
  --apple-id "$APPLE_ID" \
  --team-id "$APPLE_TEAM_ID" \
  --password "$APPLE_APP_PASSWORD" \
  --wait)"
echo "$submit_output"

rm -f "$notarization_zip"

# --wait blocks until Apple reaches a terminal state, but exits 0 either
# way — a rejected submission ("Invalid") still returns success, so without
# this check the script sails on into stapling and fails there instead,
# with a confusing "Record not found" instead of Apple's actual reason.
submission_id="$(awk '/^  id:/{print $2; exit}' <<< "$submit_output")"
status="$(awk '/^  status:/{print $2; exit}' <<< "$submit_output")"

if [[ "$status" != "Accepted" ]]; then
  echo "==> Notarización rechazada (status=$status) — log detallado de Apple:"
  xcrun notarytool log "$submission_id" \
    --apple-id "$APPLE_ID" \
    --team-id "$APPLE_TEAM_ID" \
    --password "$APPLE_APP_PASSWORD"
  exit 1
fi

echo "==> Grapando el ticket"
# Stapling embeds the notarisation ticket in the bundle, so a machine with
# no internet still opens it without a warning.
xcrun stapler staple "$APP_PATH"

echo "==> Comprobación final (lo que hará Gatekeeper en la máquina del usuario)"
xcrun stapler validate "$APP_PATH"
spctl --assess --type execute --verbose=2 "$APP_PATH"

echo "OK: firmado, notarizado y grapado."
