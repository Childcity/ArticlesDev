"""Градієнти, офсети й дискретна топологія з явними обмеженнями."""
import numpy as np
from scipy.ndimage import label,generate_binary_structure
from skimage.measure import euler_number
from scipy.stats import qmc
from core import sampling
from experiment2 import offset_metrics


def probes(dim,count=1024,seed=0,extent=1.):
    power=int(np.ceil(np.log2(count)))
    return (2*qmc.Sobol(dim,scramble=True,seed=seed).random_base2(power)[:count]-1)*extent


def reference_gradient(geometry,points):
    """Еталонні центральні різниці з двома кроками та маскою регулярності.

    Маска перевіряє збіжність різниць і одиничну норму. Вона не є
    глобальним аналітичним описом медіальної осі. Використано Sobol-точки,
    а не вузли/лінії симетрії; кількість виключених точок записується.
    """
    def finite(step):
        return np.column_stack([(geometry(points+np.eye(points.shape[1])[j]*step)-
                                 geometry(points-np.eye(points.shape[1])[j]*step))/(2*step)
                                for j in range(points.shape[1])])
    coarse=finite(2e-5);fine=finite(1e-5)
    regular=(np.linalg.norm(fine-coarse,axis=1)<1e-4)&(abs(np.linalg.norm(fine,axis=1)-1)<1e-4)
    return fine,regular


def gradient_quality(model,geometry,dim=2,seed=0):
    p=probes(dim,2048,seed)
    d=geometry(p);truth,regular=reference_gradient(geometry,p)
    mask=regular&(abs(d)<.25)
    g=model.gradient(p[mask]);gt=truth[mask]
    return dict(gradient_samples=int(mask.sum()),gradient_excluded=int((~regular).sum()),
                gradient_rmse=float(np.sqrt(np.mean(np.sum((g-gt)**2,axis=1)))),
                eikonal_rmse=float(np.sqrt(np.mean((np.linalg.norm(g,axis=1)-1)**2))),
                normal_alignment_mean=float(np.mean(np.sum(g*gt,axis=1)/(np.linalg.norm(g,axis=1)+1e-30))))


def topology(mask):
    """Betti для цифрового тіла: foreground 4/6, background 8/26.

    beta1=b0-chi (2D), beta1=b0+b2-chi (3D). При перетині межі
    області результат не інтерпретується як топологія повного тіла.
    """
    mask=np.asarray(mask,dtype=bool);dim=mask.ndim
    b0=int(label(mask,generate_binary_structure(dim,1))[1])
    chi=int(euler_number(mask,connectivity=1))
    touches=any(np.any(np.take(mask,i,axis=j)) for j in range(dim) for i in (0,-1))
    if dim==2:return dict(b0=b0,b1=b0-chi,b2=0,euler=chi,touches_boundary=touches)
    background,n=label(~mask,generate_binary_structure(dim,dim))
    exterior=set()
    for j in range(dim):
        for i in (0,-1):exterior.update(np.unique(np.take(background,i,axis=j)).tolist())
    b2=n-len(exterior-{0})
    return dict(b0=b0,b1=b0+b2-chi,b2=int(b2),euler=chi,touches_boundary=touches)


def measure(model,geometry,resolution=101,offsets=(-.1,0.,.1)):
    dim=3 if geometry.shape in ('sphere','torus') else 2
    axis,p=sampling(dim,resolution);exact=geometry(p);pred=model.evaluate(p)
    if not np.isfinite(pred).all():raise ValueError('nonfinite_field')
    shape=[resolution]*dim;truth=exact.reshape(shape);field=pred.reshape(shape)
    rows=[]
    for t in offsets:
        mask=abs(exact-t)<.2
        a=topology(truth<=t);b=topology(field<=t)
        row=dict(offset=t,resolution=resolution,band_rmse=float(np.sqrt(np.mean((exact[mask]-pred[mask])**2))),
                 sign_error=float(np.mean((exact<=t)!=(pred<=t))),sampled_max=float(np.max(abs(exact-pred))))
        row.update(offset_metrics(truth,field,axis,t,geometry))
        row.update({'reference_'+k:v for k,v in a.items()});row.update({'model_'+k:v for k,v in b.items()})
        row['topology_match']=all(a[k]==b[k] for k in ('b0','b1','b2'))
        row['surface_status']='both' if row['reference_surface_samples'] and row['model_surface_samples'] else 'empty_or_unresolved'
        rows.append(row)
    return rows


def pareto_mask(rows,keys):
    """Мінімізація усіх цілей; однакові точки не домінують одна одну."""
    values=np.array([[r[k] for k in keys] for r in rows])
    return np.array([not np.any(np.all(values<=v,axis=1)&np.any(values<v,axis=1)) for v in values])
