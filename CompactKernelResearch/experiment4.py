"""Пункт 4: зафіксований бюджет добору на train та заморожені holdout-оцінки."""
import time
import numpy as np
from comparators import METHODS,CountedGeometry,build,candidates
from quality import probes,measure,gradient_quality

TRAIN=[dict(shape='circle',angle=11.,shift=-.03),dict(shape='square',angle=23.,shift=.02)]
HOLDOUT=['capsule','rounded_box','neck','two_circles','sphere','torus']


def case(shape,seed):
    # Фінальні seeds не використовуються в жодному калібрувальному критерію.
    rng=np.random.default_rng(seed)
    return dict(shape=shape,angle=float(rng.uniform(31,68)),shift=float(rng.uniform(-.08,.08)))


def tune(methods=METHODS,seeds=(0,1,2),budget=6):
    rows=[];selection={}
    for method in methods:
        choices=candidates(method)[:budget];scores=[]
        for index,config in enumerate(choices):
            losses=[];failed=False
            for shape in TRAIN:
                for seed in seeds:
                    geometry=CountedGeometry(**shape);start=time.perf_counter()
                    row=dict(method=method,candidate=index,train_shape=shape['shape'],angle=shape['angle'],shift=shape['shift'],seed=seed,**config)
                    try:
                        model,info=build(method,geometry,h=.25,**config)
                        points=probes(2,512,seed);exact=geometry(points);mask=abs(exact)<.25
                        error=model.evaluate(points)-exact
                        loss=float(np.sqrt(np.mean(error[mask]**2)))
                        if not np.isfinite(loss):raise ValueError('nonfinite_loss')
                        losses.append(loss);row.update(status='ok',calibration_rmse=loss,**info)
                    except (ValueError,RuntimeError) as error:
                        failed=True;row.update(status='failed',error=str(error))
                    row.update(geometry.counts);row['total_seconds']=time.perf_counter()-start;rows.append(row)
            scores.append(float(np.mean(losses)) if not failed and losses else np.inf)
        valid=np.flatnonzero(np.isfinite(scores))
        if not len(valid):selection[method]=dict(status='failed',reason='all_training_candidates_failed')
        else:
            best=int(valid[np.argmin(np.array(scores)[valid])])
            selection[method]=dict(status='ok',config=choices[best],candidate=best,train_score=scores[best],
                                   candidates=len(choices),tuning_seconds=sum(r['total_seconds'] for r in rows if r['method']==method),
                                   tuning_sdf_points=sum(r['sdf_points'] for r in rows if r['method']==method),
                                   tuning_projection_points=sum(r['projection_points'] for r in rows if r['method']==method))
    return selection,rows


def evaluate_holdout(selection,seeds=(10,11,12),shapes=HOLDOUT):
    results=[]
    for shape in shapes:
        dim=3 if shape in ('sphere','torus') else 2
        hs=(.4,.5) if dim==3 else (.2,.3)
        for seed in seeds:
            for h in hs:
                for method,chosen in selection.items():
                    pose=case(shape,seed)
                    row=dict(shape=shape,seed=seed,h=h,method=method,dim=dim,angle=pose['angle'],shift=pose['shift'])
                    if chosen['status']!='ok':
                        results.append(dict(row,status='failed',error='no_training_selection'));continue
                    geometry=CountedGeometry(**pose)
                    try:
                        model,info=build(method,geometry,h=h,**chosen['config'])
                        counts=geometry.counts.copy()
                        quality=measure(model,geometry,81 if dim==2 else 31)
                        gradients=gradient_quality(model,geometry,dim,seed)
                        for q in quality:results.append(dict(row,status='ok',**info,**q,**gradients,**counts))
                    except (ValueError,RuntimeError) as error:
                        results.append(dict(row,status='failed',error=str(error)))
        print('Holdout',shape,'complete',flush=True)
    return results
