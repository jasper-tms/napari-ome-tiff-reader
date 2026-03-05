#!/usr/bin/env python3

import tifffile
from xml.etree import ElementTree as ET


def napari_get_reader(path):
    if isinstance(path, list):
        path = path[0]
    if isinstance(path, str) and path.lower().endswith('.tif'):
        return reader
    return None


def reader(path):
    if isinstance(path, list):
        path = path[0]
    with tifffile.TiffFile(path) as tif:
        if not tif.is_ome:
            from napari_builtins.io import magic_imread
            return [(magic_imread(path),)]
        data = tif.asarray()
        axes = tif.series[0].axes  # e.g. 'ZCYX'

        root = ET.fromstring(tif.pages[0].tags[270].value)
        pixels = root.find('.//{*}Pixels')
        pz = float(pixels.get('PhysicalSizeZ', 1))
        py = float(pixels.get('PhysicalSizeY', 1))
        px = float(pixels.get('PhysicalSizeX', 1))

        sizes = {'Z': pz, 'Y': py, 'X': px}
        scale = [sizes.get(ax, 1.0) for ax in axes]

    if 'C' not in axes:
        return [(data, {'scale': scale}, 'image')]

    c_idx = axes.index('C')
    channel_scale = [s for i, s in enumerate(scale) if i != c_idx]
    colors = ['green', 'red', 'blue', 'cyan']

    return [
        (
            data.take(c, axis=c_idx),
            {
                'scale': channel_scale,
                'colormap': colors[c],
                'blending': 'additive',
                'name': f'Channel {c}' + (f' ({colors[c]})' if c < len(colors) else ''),
            },
            'image'
        )
        for c in range(data.shape[c_idx])
    ]
