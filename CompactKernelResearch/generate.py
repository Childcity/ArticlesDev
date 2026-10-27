"""Запускає всі три досліди; звіти містять лише збережені вимірювання."""
import csv,json,platform,sys,time
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
    results={}
    rows=[]
    for rho in [1.,1.5,2.,3.]:
        for margin in [False,True]:
            result=e1.run(h=.25,rho=rho,margin=margin)
            rows.append(result[0])
            if rho==2 and margin:savefig(e1.figure(result),'experiment1')
    results['experiment1']=rows
    results['experiment2']=[]
    for shape in e2.SHAPES:
        result=e2.run(shape=shape)
        results['experiment2'].append(result[0]);savefig(e2.figure(result),f'experiment2_{shape}')
        if shape in ('sphere','torus'):savefig(e2.surface_figure(result),f'experiment2_{shape}_3d')
    print('Experiments 1 and 2 complete',flush=True)
    results['experiment3']=e3.run_sweep()
    savefig(e3.figure(results['experiment3']),'experiment3')
    results['environment']=dict(python=sys.version,platform=platform.platform(),
        packages={p:metadata.version(p) for p in ['numpy','scipy','matplotlib','streamlit','pytest','sympy','scikit-image']},seed=0)
    (OUT/'results.json').write_text(json.dumps(results,indent=2,ensure_ascii=False))
    for key in ['experiment1','experiment2','experiment3']:
        rows=results[key];fields=sorted(set().union(*(r.keys() for r in rows)))
        with (OUT/f'{key}.csv').open('w') as f:
            writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
    from reports import write_reports
    write_reports(results)
    print('All results and TeX reports written',flush=True)

if __name__=='__main__':run()
