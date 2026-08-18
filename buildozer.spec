[app]
title = WS Alimentação
package.name = wsalimentacao
package.domain = br.com.dracss
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,ttf,html,js,css,webmanifest,ico,svg
source.include_patterns = webapp/*,webapp/**/*
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/icon.png

# Android build configuration
android.api = 34
android.minapi = 21
android.archs = arm64-v8a
android.accept_sdk_license = True
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 0
