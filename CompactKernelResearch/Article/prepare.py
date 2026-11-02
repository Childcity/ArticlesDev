"""Regenerate article tables/figures; verify frozen results without retuning."""
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/article-mpl')
import sys,json,hashlib
from pathlib import Path
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(ROOT))
from comparators import build,CountedGeometry,basis
from core import sampling
from quality import measure
DATA=ROOT/'results/extended'
def read(name): return json.loads((DATA/(name+'.json')).read_text())
for d in ['tables','figures']: (HERE/d).mkdir(exist_ok=True)
def table(name,header,rows):
    text='\\begin{tabular}{'+'l'+'r'*(len(header)-1)+'}\\toprule\n'+' & '.join(header)+r' \\ \midrule'+'\n'
    text+='\n'.join(' & '.join(str(v).replace('_',r'\_') for v in row)+r' \\' for row in rows)
    (HERE/'tables'/f'{name}.tex').write_text(text+'\n\\bottomrule\\end{tabular}\n')
p=read('protocol'); assert p['version']=='extended-4-6-n4-v1' and p['pg_order']==4
for f,h in p['source_hashes'].items(): assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
h=read('holdout');res=read('resolution');resources=read('resources');fm=read('failure_map');sel=read('selection');summary=read('summary')
assert [len(read(n)) for n in ['training','holdout','resolution','failure_map','resources']]==[234,972,432,40,36]
assert Counter(r['flag'] for r in fm)=={'within_threshold':13,'quality_threshold':19,'uncovered_support':8}
rows=[]
for dim in [2,3]:
 for s in summary[f'holdout_{dim}d']:
  a=[r for r in h if r['dim']==dim and r['method']==s['method'] and r['status']=='ok']
  med=float(np.median([r['band_rmse'] for r in a]));assert np.isclose(med,s['band_rmse'],rtol=1e-12)
  seeds=[np.median([r['band_rmse'] for r in a if r['seed']==seed]) for seed in [10,11,12]]
  assert np.isclose(min(seeds),s['band_rmse_seed_min']) and np.isclose(max(seeds),s['band_rmse_seed_max'])
  rows.append([s['method'],dim,f'{med:.6f}',f'{min(seeds):.6f}--{max(seeds):.6f}',f"{np.median([r['sampled_offset_hausdorff'] for r in a if r.get('sampled_offset_hausdorff') is not None]):.6f}",f"{np.median([r['gradient_rmse'] for r in a]):.5f}"])
table('errors',['Method','$D$','Band RMSE','Seed median range','$H$','Gradient RMSE'],rows)
table('selection',['Method',r'$\rho$',r'$\Delta/h$','Candidates','Tuning (s)'],[[m,s['config']['rho'] if 'grid' in m or 'isolines' in m else '--',s['config']['delta_ratio'] if 'isolines' in m else '--',s['candidates'],f"{s['tuning_seconds']:.4f}"] for m,s in sel.items()])
table('resources',['Method','$h$','Payload (B)','Build (s)','Query (s)','$H$'],[[r['method'],r['h'],r['stored_bytes'],f"{r['build_seconds']:.4f}",f"{r['query_seconds']:.4f}",f"{r['mean_offset_error']:.5f}"] for r in resources if r['dim']==3 and r['h']==.4])
table('editing',['Method','Cache prep (s)','Update (s)','Rebuild (s)','Cached RMSE','Rebuilt RMSE'],[[r['method'],f"{r['cache_prepare_seconds']:.4f}",f"{r['cached_update_seconds']:.5f}",f"{r['full_rebuild_seconds']:.4f}",f"{np.median(r['cached_update_rmse']):.5f}",f"{np.median(r['full_rebuild_rmse']):.5f}"] for r in resources if r['dim']==3 and r['h']==.4])
table('topology',['Method','Resolution',r'Ref. $(b_0,b_1,b_2)$',r'Model $(b_0,b_1,b_2)$'],[[r['method'],r['resolution'],str(tuple(r['reference_'+k] for k in ['b0','b1','b2'])),str(tuple(r['model_'+k] for k in ['b0','b1','b2']))] for r in res if r['shape']=='torus' and r['offset']==-.19 and r['method'] in ['pg_grid','pg_isolines','cubic']])
q=np.linspace(0,1.2,400);fig,ax=plt.subplots(figsize=(6,3))
for f in ['pg','wendland_c2','wendland_c4']: ax.plot(q,basis(q,f,4),label=f.replace('_',' '))
ax.set(xlabel='Normalized radius s/r',ylabel='Basis value');ax.legend();fig.tight_layout();fig.savefig(HERE/'figures/kernel.pdf');plt.close(fig)
# Illustrate the largest and smallest paired PG isoline/grid error ratios in 2D.
pairs=[]
for r in h:
 if r['dim']==2 and r['method']=='pg_isolines':
  g=next(a for a in h if a['method']=='pg_grid' and all(a[k]==r[k] for k in ['shape','seed','h','offset']))
  pairs.append((r['band_rmse']/g['band_rmse'],r,g))
examples=[]
for name,item in [('improvement',min(pairs,key=lambda x:x[0])),('failure',max(pairs,key=lambda x:x[0]))]:
 ratio,r,g=item;fig,axes=plt.subplots(1,3,figsize=(10,3.4));axis,points=sampling(2,81)
 geom=CountedGeometry(r['shape'],r['angle'],r['shift']);truth=geom(points).reshape(81,81)
 for ax,method in zip(axes,['reference','pg_grid','pg_isolines']):
  if method=='reference':z=truth
  else:
   model,_=build(method,geom,h=r['h'],**sel[method]['config']);z=model.evaluate(points).reshape(81,81)
   measured=next(x for x in measure(model,geom,81) if x['offset']==r['offset'])
   stored=g if method=='pg_grid' else r
   assert np.isclose(measured['band_rmse'],stored['band_rmse'],rtol=1e-9)
  ax.contour(axis,axis,truth.T,levels=[r['offset']],colors='black',linestyles='dashed')
  ax.contour(axis,axis,z.T,levels=[r['offset']],colors='#197a9b');ax.set_aspect('equal');ax.set_title(method.replace('_',' '));ax.set(xlabel='x',ylabel='y')
 fig.tight_layout();fig.savefig(HERE/'figures'/f'{name}.pdf');plt.close(fig)
 example={k:r[k] for k in ['shape','seed','h','angle','shift','offset','resolution','rho','delta_ratio']};example.update(grid_rmse=g['band_rmse'],isoline_rmse=r['band_rmse'],ratio=ratio);examples.append(example)
 caption=f"{r['shape'].replace('_',' ')}; seed {r['seed']}, h={r['h']}, rho={r['rho']}, Delta/h={r['delta_ratio']}, offset={r['offset']}, resolution 81 squared. Grid/isoline band RMSE {g['band_rmse']:.6f}/{r['band_rmse']:.6f}. Dashed: reference; blue: displayed field."
 (HERE/'tables'/f'{name}_caption.tex').write_text(caption)
(HERE/'provenance.json').write_text(json.dumps({'protocol':p['version'],'unresolved_offsets':{str(dim)+'D/'+m:sum(r.get('sampled_offset_hausdorff') is None for r in h if r['dim']==dim and r['method']==m) for dim in [2,3] for m in sel},'source_hashes_verified':True,'inputs':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in DATA.glob('*.json')},'examples':examples,'aggregation':'Median of all successful rows by method/dimension; seed range of three seed medians. Resource and editing table: torus h=.4, recorded medians; editing error median over three shifts.','note':'Only two stored 2D configurations reconstructed for figures. No tuning or benchmark timings rerun.'},indent=2))
print('Verified counts, code hashes, aggregate RMSE/seed ranges, and figure reconstructions.');print(json.dumps(examples,indent=2))
