[app]
title = FPE Companion
package.name = fpecompanion
package.domain = org.dj
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.permissions = RECORD_AUDIO
android.api = 30
android.minapi = 30
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
