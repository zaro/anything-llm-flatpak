# Flatpak packaging for AnythingLLM

## Quick start

### Install pre-built

1. Go to [Latest Release ](https://github.com/zaro/anything-llm-flatpak/releases/latest)
2. Download AnythingLLM.flatpak asset.
3. Install either by double clicking or by running `flatpak install AnythingLLM.flatpak`


### Build it yourself

1. Clone this repo
2. Run

```sh
flatpak-builder build  flatpak.yaml --install-deps-from=flathub --force-clean --user --install
```

This will build a flatpak from AnythingLLM AppImage and will install it in your user installed apps.
