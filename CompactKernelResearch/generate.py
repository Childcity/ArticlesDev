"""Повний перезапуск виправлених дослідів, вимірювань, графіків і TeX."""
import csv,json,platform,sys,hashlib
from pathlib import Path
import importlib.metadata as metadata
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import experiment1 as e1
import experiment2 as e2
import experiment3 as e3
OUT=Path(__file__).parent/'results'


def savefig(fig,name):
    for extension in ('png','pdf'):fig.savefig(OUT/f'{name}.{extension}',dpi=160)
    plt.close(fig)


def run():
    OUT.mkdir(exist_ok=True)
    results=dict(protocol='article-isolines-v3',date='2026-10-31')
    rows=[]
    for rho in [1.,1.5,2.,3.]:
        for margin in [False,True]:
            for strategy in ['grid','isolines']:
                result=e1.run(h=.25,rho=rho,margin=margin,strategy=strategy)
                rows.append(result[0])
                if rho==2 and margin:
                    savefig(e1.figure(result),'experiment1' if strategy=='isolines' else 'experiment1_grid')
    results['experiment1']=rows
    results['experiment2']=[]
    for shape in e2.SHAPES:
        pair=[e2.run(shape=shape,strategy=strategy) for strategy in ['grid','isolines']]
        results['experiment2'].extend(r[0] for r in pair)
        savefig(e2.figure(pair[1]),f'experiment2_{shape}')
        if shape in ('sphere','torus'):
            savefig(e2.surface_figure(pair[1]),f'experiment2_{shape}_3d')
        else:savefig(e2.comparison_figure(pair),f'experiment2_{shape}_comparison')
        print(shape,[(r[0]['strategy'],r[0]['status']) for r in pair],flush=True)
    cases=list(e2.paper_cases())
    results['paper_cases']=[r[0] for r in cases]
    for start,name in [(0,'paper_45_r05'),(3,'paper_35_r05'),(6,'paper_45_r1'),(9,'paper_35_r1')]:
        savefig(e2.comparison_figure(cases[start:start+3]),name)
    print('Experiments 1/2 complete; starting paired sweep',flush=True)
    results['experiment3']=e3.run_sweep()
    savefig(e3.figure(results['experiment3']),'experiment3')
    optimization,trials,optimized=e3.optimize_level_step()
    results['optimization']=optimization
    results['optimization_trials']=trials
    savefig(e3.optimization_figure(optimization,trials),'optimization')
    savefig(e2.comparison_figure(optimized),'optimized_comparison')
    # Незалежне завантаження готового поля без вузлів та SDF.
    from storage import from_model,load
    field=from_model(optimized[-1][-1])
    field.save(OUT/'optimized_field.npz')
    restored=load(OUT/'optimized_field.npz')
    import numpy as np
    points=np.random.default_rng(8).uniform(-1.5,1.5,(128,2))
    results['storage']=dict(coefficients=int(field.coefficients.size),
        coefficient_bytes=int(field.coefficients.nbytes),
        voxel_value_bytes=int(field.coefficients.size*np.dtype(float).itemsize),
        archive_bytes=(OUT/'optimized_field.npz').stat().st_size,
        max_roundtrip_error=float(np.max(np.abs(restored.evaluate(points)-optimized[-1][-1].evaluate(points)))))
    source=Path(__file__).parents[1]/'papers/2025_Pseudo_Gaussian_Modeling/pseudo_gaussian_grid_ric_formatted (2).docx'
    results['source_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
    results['environment']=dict(python=sys.version,platform=platform.platform(),
        packages={p:metadata.version(p) for p in ['numpy','scipy','matplotlib','streamlit','pytest','sympy','scikit-image']})
    (OUT/'results.json').write_text(json.dumps(results,indent=2,ensure_ascii=False,allow_nan=False))
    for key in ['experiment1','experiment2','experiment3','paper_cases','optimization_trials']:
        rows=results[key];fields=sorted(set().union(*(r.keys() for r in rows)))
        with (OUT/f'{key}.csv').open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');writer.writeheader();writer.writerows(rows)
    from reports import write_reports
    write_reports(results)
    print('All results and TeX reports written',flush=True)

if __name__=='__main__':run()
