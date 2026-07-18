[app]

# title of your application
title = BoardComposerStudio

# project root directory. default = The parent directory of input_file
project_dir = .

# source file entry point path. default = main.py
input_file = app.py

# directory where the executable output is generated
exec_directory = ./dist

# path to the project file relative to project_dir
project_file = 

# application icon. left blank on purpose: this path is machine-specific
# (points into whichever .venv generated it), so it's resolved fresh on
# every run instead of committing an absolute path. Falls back to the
# default PySide6 icon bundled with the venv actually running the build.
# NOTE: once a build writes a resolved value here, it "sticks" (pyside6-deploy
# only re-detects it if this field reads back blank) — re-blank it before
# committing if a local build run dirtied this file.
icon =

[python]

# python path. left blank on purpose, same reasoning as icon: pyside6-deploy
# overwrites this with the currently active venv's interpreter on every run
# (see Config.set_or_fetch), so committing an absolute path here would only
# be misleading, not authoritative.
python_path =

# python packages to install
packages = Nuitka==4.0

# buildozer = for deploying Android application
android_packages = buildozer==1.5.0,cython==0.29.33

[qt]

# paths to required qml files. comma separated
# normally all the qml files required by the project are added automatically
# design studio projects include the qml files using qt resources
qml_files = 

# excluded qml plugin binaries
excluded_qml_plugins = 

# qt modules used. comma separated
modules = Core,DBus,Gui,Svg,Widgets

# qt plugins used by the application. only relevant for desktop deployment
# for qt plugins used in android application see [android][plugins]
plugins = accessiblebridge,egldeviceintegrations,generic,iconengines,imageformats,platforminputcontexts,platforms,platforms/darwin,platformthemes,styles,wayland-decoration-client,wayland-graphics-integration-client,wayland-shell-integration,xcbglintegrations

[android]

# path to pyside wheel
wheel_pyside = 

# path to shiboken wheel
wheel_shiboken = 

# plugins to be copied to libs folder of the packaged application. comma separated
plugins = 

[nuitka]

# usage description for permissions requested by the app as found in the info.plist file
# of the app bundle. comma separated
# eg = extra_args = --show-modules --follow-stdlib
macos.permissions = 

# mode of using nuitka. accepts standalone or onefile. default = onefile
mode = onefile

# specify any extra nuitka arguments
extra_args = --quiet --noinclude-qt-translations

[buildozer]

# build mode
# possible values = ["aarch64", "armv7a", "i686", "x86_64"]
# release creates a .aab, while debug creates a .apk
mode = debug

# path to pyside6 and shiboken6 recipe dir
recipe_dir = 

# path to extra qt android .jar files to be loaded by the application
jars_dir = 

# if empty, uses default ndk path downloaded by buildozer
ndk_path = 

# if empty, uses default sdk path downloaded by buildozer
sdk_path = 

# other libraries to be loaded at app startup. comma separated.
local_libs = 

# architecture of deployed platform
arch = 

