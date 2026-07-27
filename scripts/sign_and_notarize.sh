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

echo "==> Firmando el bundle"
# No entitlements on purpose: the app draws windows and makes outbound HTTPS
# calls, neither of which needs one outside the App Sandbox. If a future
# hardened-runtime failure demands one (allow-jit and friends), add it with
# the failing log in hand rather than pre-emptively — every entitlement
# widens what the app is allowed to do.
codesign --force --timestamp --options runtime \
  --sign "$SIGNING_IDENTITY" "$APP_PATH"

echo "==> Verificando la firma"
# Si esto falla, el sitio más probable es Contents/MacOS/certifi/cacert.pem:
# Nuitka deja ficheros de datos dentro de MacOS/, donde codesign espera solo
# código, y el bundle sin firmar de hoy ya falla ahí con "code object is not
# signed at all / In subcomponent: .../certifi/cacert.pem". Firmar el bundle
# entero debería sellarlos como recursos; si aun así se queja, moverlos a
# Contents/Resources/ es la salida (no se ha podido comprobar de verdad sin
# un certificado real). Falla ruidosamente aquí antes que publicar un .app
# que Gatekeeper rechace en la máquina de quien lo descargue.
codesign --verify --strict --verbose=2 "$APP_PATH"

echo "==> Subiendo a notarizar (puede tardar varios minutos)"
# notarytool wants an archive, and ditto is the only archiver that preserves
# the bundle's symlinks and extended attributes intact.
ditto -c -k --keepParent "$APP_PATH" "$notarization_zip"

xcrun notarytool submit "$notarization_zip" \
  --apple-id "$APPLE_ID" \
  --team-id "$APPLE_TEAM_ID" \
  --password "$APPLE_APP_PASSWORD" \
  --wait

rm -f "$notarization_zip"

echo "==> Grapando el ticket"
# Stapling embeds the notarisation ticket in the bundle, so a machine with
# no internet still opens it without a warning.
xcrun stapler staple "$APP_PATH"

echo "==> Comprobación final (lo que hará Gatekeeper en la máquina del usuario)"
xcrun stapler validate "$APP_PATH"
spctl --assess --type execute --verbose=2 "$APP_PATH"

echo "OK: firmado, notarizado y grapado."
