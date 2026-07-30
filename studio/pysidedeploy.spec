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

# application icon = the project's own icon, committed in-repo (source
# artwork in assets/icon-source.jpg, converted with sips + iconutil).
# relative to this file's directory (project_dir = ., builds run from
# studio/). before this existed the field was left blank so pyside6-deploy
# would fall back to the default pyside6 icon — if a build run ever
# rewrites this to an absolute path into a .venv, restore this relative
# path before committing.
icon = ./assets/icon.icns

[python]

# python path. left blank on purpose, same reasoning as icon = pyside6-deploy
# overwrites this with the currently active venv's interpreter on every run
# (see config.set_or_fetch), so committing an absolute path here would only
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
#
# --macos-signed-app-name sets the bundle identifier. without it nuitka
# derives it from the entry point's filename, so every build so far shipped
# with cfbundleidentifier = "app": not unique to anything, shared with any
# other app built the same careless way, and rejected by notarisation. it
# has to stay in reverse-dns form and must never change once a release is
# out — macos keys per-app settings and permissions off this string.
# --macos-app-version must match the version in pyproject.toml.
# scripts/check_project.py fails the build if the two drift apart.
extra_args = --quiet --noinclude-qt-translations --macos-signed-app-name=com.efjdefrutos.boardcomposer.studio --macos-app-version=0.3.2

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

