"""Пункт 6: діагностична карта відмов та ізольовані виміри ресурсів."""
import os,json,subprocess,sys
from pathlib import Path
from itertools import product
import numpy as np
from comparators import CountedGeometry,build,collocation
from quality import probes,measure,pareto_mask


def failure_map():
    rows=[]
    # Повний добуток взаємодій, на відміну від однофакторної серії пункту 3.
    for h,rho,order,strategy,ratio in product((.2,.3),(.5,1.,1.5,2.,3.),(1,2,4),('grid','isolines'),(.5,1.)):
        geometry=CountedGeometry('square',angle=33.,shift=.037)
        row=dict(h=h,rho=rho,order=order,strategy=strategy,delta_ratio=ratio)
        try:
            model,info=build('pg_'+strategy,geometry,h=h,rho=rho,order=order,delta_ratio=ratio,
                             margin=3*h,diagnostics=True)
            p=probes(2,1024,21)
            coverage=collocation(p,model.centers,rho*h,'pg',order)
            uncovered=float(np.mean(np.diff(coverage.indptr)==0))
            q=measure(model,geometry,101,offsets=(0.,))[0]
            # Пороги визначені до досліду; це інженерні прапорці, не теорема допустимості.
            geometry_flag=(q.get('sampled_offset_hausdorff',10)>.1 or not q['topology_match'])
            flag='quality_threshold' if geometry_flag else 'within_threshold'
            if info.get('rank',len(model.centers))<len(model.centers):flag='rank_deficient'
            if uncovered>0:flag='uncovered_support'
            row.update(status='ok',flag=flag,uncovered_fraction=uncovered,**info,**q)
        except (ValueError,RuntimeError) as error:
            row.update(status='failed',flag='algebraic_failure',error=str(error))
        rows.append(row)
    return rows


def resources(selection):
    rows=[];worker=Path(__file__).with_name('resource_worker.py')
    env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
    for dim in (2,3):
        for h in ((.2,.3) if dim==2 else (.4,.5)):
            for method,chosen in selection.items():
                if chosen['status']!='ok':continue
                config=dict(method=method,dim=dim,h=h,config=chosen['config'])
                try:
                    completed=subprocess.run([sys.executable,str(worker),json.dumps(config)],
                                             capture_output=True,text=True,env=env,timeout=180)
                    if completed.returncode:raise RuntimeError(completed.stderr[-600:])
                    row=json.loads(completed.stdout)
                    row.update(method=method,dim=dim,h=h)
                except (RuntimeError,ValueError,subprocess.TimeoutExpired) as error:
                    row=dict(config,status='failed',error=str(error))
                rows.append(row)
        print('Resource study dimension',dim,'complete',flush=True)
    for dim in (2,3):
        group=[r for r in rows if r['status']=='ok' and r['dim']==dim]
        mask=pareto_mask(group,['mean_offset_error','stored_bytes','query_seconds'])
        for r,front in zip(group,mask):r['pareto']=bool(front)
    return rows
