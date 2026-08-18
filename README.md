# WS Alimentação

Kivy Android app scaffolded by the android-app-builder skill.

## Files
- `main.py` — the app. Edit this to implement your logic. Test on desktop with `python main.py`.
- `buildozer.spec` — build configuration (dependencies, permissions, API levels).
- `.github/workflows/android-build.yml` — builds the APK on GitHub's servers.

## Build the APK

### Option A — GitHub Actions (no local setup)
1. Create a GitHub repo and push this folder.
2. The workflow runs on push (or trigger it from the Actions tab).
3. Download the **apk** artifact from the finished run.

### Option B — Local (Linux)
```bash
pip install --user buildozer "cython<3.1"
sudo apt-get install -y openjdk-17-jdk git zip unzip autoconf libtool pkg-config \
  zlib1g-dev libffi-dev libssl-dev build-essential ccache
buildozer android debug
# APK appears in bin/
```

## Install on a phone
Transfer the `.apk` to the phone, enable "Install unknown apps" for the app opening it,
tap the APK, and install.
