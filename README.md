# napari-ome-tiff-reader

A minimal napari plugin that reads OME-TIFF files with correct physical scale and automatic channel splitting.

- Reads `PhysicalSizeX/Y/Z` from OME-XML metadata and sets layer scale accordingly
- Splits multi-channel data into separate layers with green/red colormaps and additive blending
- Falls back to napari's builtin reader for non-OME TIFFs

## Installation

```bash
cd napari-ome-tiff-reader
pip install -e .
```

## napari reader preference

napari caches which plugin to use for each file extension. If `.tif` files are already mapped to a different reader (e.g. `napari` builtins), you need to update the config.

Find your settings file:

```
~/.config/napari/<env_name>/settings.yaml
```

Look for the `extension2reader` section under `plugins:` and set (or add):

```yaml
plugins:
  extension2reader:
    '*.tif': napari-ome-tiff-reader
```

If you'd rather be prompted to choose each time, delete the `'*.tif'` line entirely.
