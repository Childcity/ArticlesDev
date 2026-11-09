"""Shared article comparison plotter and standalone fitting-point diagnostics."""
import csv
import json
from pathlib import Path

from preview_torus import (HERE, ROOT, DATA, BLUE, METHODS, digest, save,
                           np, plt, Line2D, build, CountedGeometry, sampling)
from core import select_isoline_nodes
from matplotlib.collections import LineCollection


def draw(fields, axis, geometry, locations, offset, title, output, stem, diagnostics):
    fig, axes = plt.subplots(1, 3, figsize=(13, 5.5), layout='constrained')
    truth = fields['reference']
    dim = next(iter(locations.values()))[0].shape[1]
    coords = [0, 2] if dim == 3 else [0, 1]
    for ax, (method, field) in zip(axes, fields.items()):
        if offset != 0:
            ax.contour(axis, axis, truth.T, levels=[0], colors='.6',
                       linestyles='dotted', linewidths=1)
        ax.contour(axis, axis, field.T, levels=[offset], colors=BLUE,
                   linestyles='solid', linewidths=1.5)
        ax.contour(axis, axis, truth.T, levels=[offset], colors='black',
                   linestyles='dashed', linewidths=1)
        subtitle = 'Analytical SDF'
        if method != 'reference':
            centers, nodes = locations[method]
            # A section is not a projection: never draw off-plane nodes as constraints.
            visible = np.all(np.abs(nodes[:, coords]) <= 1, axis=1)
            if dim == 3:
                visible &= (np.abs(nodes[:, 1]) < 1e-9) & (np.abs(centers[:, 1]) < 1e-9)
            c, y = centers[visible][:, coords], nodes[visible][:, coords]
            values = geometry(nodes[visible])
            zero = np.abs(values) < 1e-9
            ax.add_collection(LineCollection(np.stack([c, y], axis=1), colors='.7',
                                             linewidths=.7, zorder=2))
            ax.scatter(*c.T, marker='x', c='.5', s=26, linewidths=.9, zorder=3)
            ax.scatter(*y.T, c='#df8a24', s=22, edgecolors='white', linewidths=.4, zorder=4)
            ax.scatter(*y[zero].T, facecolors='none', edgecolors='#117c38',
                       s=90, linewidths=1.6, zorder=5)
            counts = diagnostics[method]
            subtitle = f'Nodes on d=0: {counts["zero_nodes"]} total, {sum(zero)} shown'
            if offset != 0:
                subtitle += f'\nNodes on d={offset:g}: {counts["displayed_level_nodes"]} total'
        ax.set(title=method.replace('_', ' ') + '\n' + subtitle,
               xlabel='x', ylabel='z' if dim == 3 else 'y', xlim=(-1, 1), ylim=(-1, 1))
        ax.set_aspect('equal')
        ax.set_xticks([-1, -.5, 0, .5, 1])
        ax.set_yticks([-1, -.5, 0, .5, 1])
    handles = [Line2D([], [], color='black', linestyle='--', label=f'Reference d={offset:g}'),
               Line2D([], [], color=BLUE, label=f'Displayed f={offset:g}'),
               Line2D([], [], color='.5', marker='x', linestyle='', label='Kernel centers'),
               Line2D([], [], color='#df8a24', marker='o', linestyle='', label='Fitting nodes'),
               Line2D([], [], color='#117c38', marker='o', markerfacecolor='none',
                      linestyle='', label='Fitting nodes on d=0')]
    if offset != 0:
        handles.append(Line2D([], [], color='.6', linestyle=':', label='Reference d=0'))
    fig.legend(handles=handles, loc='outside lower center', ncol=3, frameon=False)
    note = ('Only actual nodes and centers in y=0 are shown; off-plane nodes also affect the field.'
            if dim == 3 else 'Segments connect each fixed kernel center to its fitting node.')
    fig.suptitle(title + '\n' + note, fontsize=12)
    save(fig, output, stem)


def main():
    output = HERE / 'previews' / 'fitting_points'
    output.mkdir(parents=True, exist_ok=True)
    protocol, selection, holdout = [json.loads((DATA / f'{name}.json').read_text())
                                    for name in ('protocol', 'selection', 'holdout')]
    for name, expected in protocol['source_hashes'].items():
        if digest(ROOT / name) != expected:
            raise ValueError(f'Research source differs from frozen protocol: {name}')
    manifest = dict(generator_sha256=digest(Path(__file__)),
                    plot_helpers_sha256=digest(HERE / 'preview_torus.py'),
                    inputs={name: digest(DATA / f'{name}.json')
                            for name in ('protocol', 'selection', 'holdout')},
                    source_hashes_verified=True, slice_resolution=401, examples=[])
    for shape, seed, h, offsets in [('two_circles', 12, .3, [-.1, 0.]),
                                    ('torus', 10, .4, [0.])]:
        row = next(r for r in holdout if r['shape'] == shape and r['seed'] == seed and r['h'] == h)
        geom = CountedGeometry(shape, row['angle'], row['shift'])
        axis, p2 = sampling(2, 401)
        points = np.column_stack((p2[:, 0], np.zeros(len(p2)), p2[:, 1])) if shape == 'torus' else p2
        fields = {'reference': geom(points).reshape(401, 401)}
        locations, checks = {}, {}
        stem = f'{shape}_seed{seed}_h{h:g}'
        for method in METHODS:
            config = selection[method]['config']
            model, _ = build(method, geom, h=h, **config)
            centers = model.centers
            nodes = centers.copy()
            if method == 'pg_isolines':
                nodes, _ = select_isoline_nodes(centers, geom, config['rho'] * h,
                                                h, config['delta_ratio'] * h)
            values, prediction = geom(nodes), model.evaluate(nodes)
            residual = float(np.max(np.abs(prediction - values)))
            if residual > 1e-7 * max(1., float(np.max(np.abs(values)))):
                raise ValueError(f'Fitting-node residual failed for {shape}/{method}')
            if method == 'pg_isolines':
                delta = config['delta_ratio'] * h
                level_error = float(np.max(np.abs(values - np.rint(values / delta) * delta)))
                if level_error > 1e-9:
                    raise ValueError('Fitting nodes do not lie on the selected levels')
            else:
                level_error = None
            locations[method] = centers, nodes
            fields[method] = model.evaluate(points).reshape(401, 401)
            filename = f'{stem}_{method}_nodes.csv'
            with (output / filename).open('w', newline='') as stream:
                writer = csv.writer(stream)
                dims = 'xyz'[:nodes.shape[1]]
                writer.writerow([f'center_{d}' for d in dims] + [f'node_{d}' for d in dims]
                                + ['reference_value', 'fitted_value'])
                writer.writerows(np.column_stack((centers, nodes, values, prediction)))
            checks[method] = dict(config=config, total_nodes=len(nodes),
                                  zero_nodes=int(np.sum(np.abs(values) < 1e-9)),
                                  max_nodal_residual=residual, max_level_residual=level_error,
                                  nodes_file=filename)
        for offset in offsets:
            diagnostics = {m: dict(checks[m], displayed_level_nodes=int(np.sum(
                np.abs(geom(locations[m][1]) - offset) < 1e-9))) for m in METHODS}
            name = f'{stem}_t{offset:g}_points'
            delta = selection['pg_isolines']['config']['delta_ratio'] * h
            title = (f'{shape.replace("_", " ")} | h={h:g}, t={offset:g}, seed={seed}, '
                     f'PG n=4, rho=2, isoline levels k * {delta:g}')
            draw(fields, axis, geom, locations, offset, title, output, name, diagnostics)
            manifest['examples'].append(dict(shape=shape, seed=seed, h=h, offset=offset,
                angle=row['angle'], shift=row['shift'], diagnostics=diagnostics,
                files=[name + '.png', name + '.pdf']))
            print(name, json.dumps(diagnostics), flush=True)
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')


if __name__ == '__main__':
    main()
