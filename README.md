# Flatpak packaging for AnythingLLM

## Quick start

1. Clone this repo
2. Run

```sh
flatpak-builder build  flatpak.yaml --install-deps-from=flathub --force-clean --user --install
```

This will build a flatpak from AnythingLLM AppImage and will install it in your user installed apps.
