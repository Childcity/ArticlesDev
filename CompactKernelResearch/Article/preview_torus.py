"""Standalone torus previews from frozen PG configurations; no manuscript edits."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys

os.environ.setdefault('MPLCONFIGDIR', '/tmp/article-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
from skimage.measure import marching_cubes

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
from comparators import build, CountedGeometry
from core import sampling
from quality import measure

DATA = ROOT / 'results' / 'extended'
METHODS = ('pg_grid', 'pg_isolines')
BLUE = '#197a9b'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(fig, output, stem):
    for extension in ('png', 'pdf'):
        fig.savefig(output / f'{stem}.{extension}', dpi=180, bbox_inches='tight')
    plt.close(fig)


def surfaces(fields, axis, offset, title, output, stem):
    fig = plt.figure(figsize=(12, 4.5), layout='constrained')
    statuses = {}
    for i, (name, values) in enumerate(fields.items(), 1):
        ax = fig.add_subplot(1, 3, i, projection='3d')
        if values.min() < offset < values.max():
            vertices, faces, _, _ = marching_cubes(
                values, level=offset, spacing=(axis[1] - axis[0],) * 3)
            vertices += axis[0]
            ax.plot_trisurf(*vertices.T, triangles=faces, color=BLUE,
                           linewidth=0, antialiased=False, shade=True)
            statuses[name] = {'vertices': len(vertices), 'faces': len(faces)}
        else:
            ax.text2D(.5, .5, 'No surface at this level',
                      transform=ax.transAxes, ha='center')
            statuses[name] = {'vertices': 0, 'faces': 0}
        ax.set(xlim=(-1, 1), ylim=(-1, 1), zlim=(-1, 1),
               xlabel='x', ylabel='y', zlabel='z', title=name.replace('_', ' '))
        ax.set_box_aspect((1, 1, 1))
        ax.set_proj_type('ortho')
        ax.view_init(elev=28, azim=-58)
        for set_ticks in (ax.set_xticks, ax.set_yticks, ax.set_zticks):
            set_ticks([-.5, 0, .5])
    fig.suptitle(f'Torus surface | {title}\nExtraction grid: {len(axis)}³', fontsize=12)
    save(fig, output, stem + '_3d')
    return statuses


def sections(fields, axis, offset, title, output, stem):
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.6), layout='constrained')
    truth = fields['reference']
    for ax, (name, values) in zip(axes, fields.items()):
        if values.min() < offset < values.max():
            ax.contour(axis, axis, values.T, levels=[offset], colors=BLUE,
                       linewidths=1.6)
        else:
            ax.text(.5, .1, 'No contour at this level',
                    transform=ax.transAxes, ha='center')
        # Draw the exact contour last so it remains visible when they coincide.
        ax.contour(axis, axis, truth.T, levels=[offset], colors='black',
                   linestyles='dashed', linewidths=1)
        ax.set(xlim=(-1, 1), ylim=(-1, 1), xlabel='x', ylabel='z',
               title=name.replace('_', ' '))
        ax.set_aspect('equal')
    fig.suptitle(f'Torus cross-section: y = 0 | {title}', fontsize=12)
    fig.legend(handles=[Line2D([], [], color='black', linestyle='--', label='Reference'),
                        Line2D([], [], color=BLUE, label='Displayed field')],
               loc='outside lower center', ncol=2, frameon=False)
    save(fig, output, stem + '_section')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed', type=int, choices=(10, 11, 12), default=10)
    parser.add_argument('--h', type=float, nargs='+', choices=(.4, .5), default=[.4, .5])
    parser.add_argument('--offsets', type=float, nargs='+', choices=(-.1, 0., .1), default=[0.])
    parser.add_argument('--resolution', type=int, default=65, help='3D extraction grid size per axis')
    parser.add_argument('--slice-resolution', type=int, default=201)
    parser.add_argument('--output', type=Path, default=HERE / 'previews' / 'torus')
    args = parser.parse_args()
    if min(args.resolution, args.slice_resolution) < 3:
        parser.error('Both resolutions must be at least 3.')

    inputs = {name: json.loads((DATA / f'{name}.json').read_text())
              for name in ('protocol', 'selection', 'holdout')}
    protocol = inputs['protocol']
    if protocol['version'] != 'extended-4-6-n4-v1' or protocol['pg_order'] != 4:
        raise ValueError('Unexpected frozen protocol')
    for name, expected in protocol['source_hashes'].items():
        if digest(ROOT / name) != expected:
            raise ValueError(f'Research source differs from frozen protocol: {name}')
    args.output.mkdir(parents=True, exist_ok=True)
    manifest = dict(
        protocol=protocol['version'], source_hashes_verified=True,
        generator_sha256=digest(Path(__file__)),
        inputs={name: digest(DATA / f'{name}.json') for name in inputs},
        domain=[-1, 1], extraction_resolution=args.resolution,
        slice_resolution=args.slice_resolution, slice_plane='y=0',
        note='Preview only; frozen configurations, no retuning. Metrics checked on the archived grid, not the display grid.',
        examples=[])
    axis, points = sampling(3, args.resolution)
    slice_axis, points2 = sampling(2, args.slice_resolution)
    slice_points = np.column_stack((points2[:, 0], np.zeros(len(points2)), points2[:, 1]))
    for h in dict.fromkeys(args.h):
        rows = [r for r in inputs['holdout'] if r['shape'] == 'torus'
                and r['seed'] == args.seed and r['h'] == h and r['method'] in METHODS]
        pose = rows[0]
        geom = CountedGeometry('torus', pose['angle'], pose['shift'])
        fields = {'reference': geom(points).reshape((args.resolution,) * 3)}
        slices = {'reference': geom(slice_points).reshape((args.slice_resolution,) * 2)}
        configs, checks = {}, {}
        for method in METHODS:
            configs[method] = inputs['selection'][method]['config']
            model, _ = build(method, geom, h=h, **configs[method])
            archived = {r['offset']: r for r in rows if r['method'] == method}
            resolution = archived[args.offsets[0]]['resolution']
            checks[method] = []
            for measured in measure(model, geom, resolution, offsets=args.offsets):
                stored = archived[measured['offset']]
                if not np.isclose(measured['band_rmse'], stored['band_rmse'], rtol=1e-9, atol=1e-12):
                    raise ValueError(f'Archived band RMSE mismatch: {method}, h={h}')
                checks[method].append(dict(offset=measured['offset'], resolution=resolution,
                                           archived_band_rmse=stored['band_rmse'],
                                           recomputed_band_rmse=measured['band_rmse']))
            fields[method] = model.evaluate(points).reshape((args.resolution,) * 3)
            slices[method] = model.evaluate(slice_points).reshape((args.slice_resolution,) * 2)
        for offset in dict.fromkeys(args.offsets):
            stem = f'torus_seed{args.seed}_h{h:g}_t{offset:g}'
            settings = '; '.join(f'{m.replace("pg_", "")}: rho={c["rho"]:g}, n={c["order"]}'
                                 + (f', Delta/h={c["delta_ratio"]:g}' if m.endswith('isolines') else '')
                                 for m, c in configs.items())
            title = f'h={h:g}, t={offset:g}, seed={args.seed}\n{settings}'
            statuses = surfaces(fields, axis, offset, title, args.output, stem)
            sections(slices, slice_axis, offset, title, args.output, stem)
            manifest['examples'].append(dict(seed=args.seed, h=h, offset=offset,
                angle=pose['angle'], shift=pose['shift'], configs=configs,
                metric_checks={m: [c for c in checks[m] if c['offset'] == offset] for m in METHODS},
                surfaces=statuses,
                files=[f'{stem}_{kind}.{ext}' for kind in ('3d', 'section') for ext in ('png', 'pdf')]))
            print(f'Generated {stem}: 3D and cross-section (PNG/PDF)', flush=True)
    (args.output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')


if __name__ == '__main__':
    main()
