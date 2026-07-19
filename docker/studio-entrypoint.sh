#!/bin/bash
# Boots BoardComposer Studio (the same PySide6 desktop app used locally,
# unmodified) inside a virtual X11 display, exposes it over VNC, and serves
# that VNC session to a browser via noVNC/websockify. No UI rewrite — this
# is a remote desktop for the existing app, not a web port of it.
set -e

: "${VNC_PASSWORD:?VNC_PASSWORD es obligatoria — sin valor por defecto a propósito}"

mkdir -p "$HOME/.vnc"
x11vnc -storepasswd "$VNC_PASSWORD" "$HOME/.vnc/passwd"

Xvfb "$DISPLAY" -screen 0 1920x1080x24 &
XVFB_PID=$!
sleep 1

# Minimal window manager so the Studio window has decorations and can be
# moved/resized inside the virtual display — Qt apps run without one, but
# a bare undecorated window is awkward to use over VNC.
fluxbox &

boardcomposer-studio &
STUDIO_PID=$!

# fluxbox places new windows at their requested size/position, not filled
# to the screen — left alone, Studio's 1400x900 window floats in a corner
# with a lot of black void around it. Force it to fill the display once it
# appears (retried: the window can take a few seconds to map while Studio
# boots and loads the demo project).
(
    for _ in $(seq 1 20); do
        if wmctrl -r "BoardComposer Studio" -b add,maximized_vert,maximized_horz 2>/dev/null; then
            break
        fi
        sleep 0.5
    done
) &

x11vnc -display "$DISPLAY" -forever -shared -rfbauth "$HOME/.vnc/passwd" &

websockify --web=/usr/share/novnc/ 6080 localhost:5900 &
NOVNC_PID=$!

# If any of these three dies, the container should exit (and, with
# --restart unless-stopped, come back up) rather than limp along with a
# half-working session.
wait -n "$XVFB_PID" "$STUDIO_PID" "$NOVNC_PID"
