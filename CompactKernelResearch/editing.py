"""Одне редагування після підготовки: нова SDF, фіксовані центри/вузли.

Для isolines збережені вузли відповідають вихідній геометрії. Перевибір
вузлів — окреме повне rebuild, яке вже вимірюється build_seconds.
"""
import time
import numpy as np
from scipy.sparse.linalg import splu
from scipy.interpolate import RegularGridInterpolator
from scipy.interpolate._ndbspline import NdBSpline
from scipy.interpolate._bsplines import _not_a_knot
from scipy.ndimage import distance_transform_edt
from core import lattice,select_isoline_nodes
from geometry import Geometry
from comparators import collocation,RBFField,GridField


def prepare(method,geometry,h,config,extent=1.):
    dim=3 if geometry.shape in ('sphere','torus') else 2
    centers=lattice(h,dim,margin=4*h,extent=extent)
    axes=[np.unique(centers[:,j]) for j in range(dim)]
    start=time.perf_counter();factor_bytes=0
    if method in ('linear','cubic','cubic_redistance'):
        shape=tuple(len(a) for a in axes)
        if method=='linear':
            def update(g):return GridField(RegularGridInterpolator(axes,g(centers).reshape(shape),method='linear'),len(centers)*8,h)
        else:
            # Геометрично стала not-a-knot матриця; факторизація оплачується один раз.
            knots=tuple(_not_a_knot(a,3) for a in axes);degrees=(3,)*dim
            a=NdBSpline.design_matrix(centers,knots,degrees);lu=splu(a.tocsc())
            def update(g):
                coeff=lu.solve(g(centers)).reshape(shape)
                spline=NdBSpline(knots,coeff,degrees)
                if method=='cubic':return GridField(spline,int(coeff.nbytes),h)
                fine=[np.linspace(v[0],v[-1],2*len(v)-1) for v in axes]
                points=np.stack(np.meshgrid(*fine,indexing='ij'),-1).reshape(-1,dim)
                mask=spline(points).reshape(tuple(len(v) for v in fine))<=0
                signed=distance_transform_edt(~mask,sampling=h/2)-distance_transform_edt(mask,sampling=h/2)
                return GridField(RegularGridInterpolator(fine,signed,method='linear'),int(signed.nbytes),h/2)
    else:
        family,strategy=method.rsplit('_',1);nodes=centers
        if strategy=='isolines':nodes,_=select_isoline_nodes(centers,geometry,h*config['rho'],h,h*config['delta_ratio'])
        a=collocation(nodes,centers,h*config['rho'],family,config['order']);lu=splu(a.tocsc())
        def update(g):
            return RBFField(centers,lu.solve(g(nodes)),h*config['rho'],family,config['order'])
    if method!='linear':
        lower,upper=lu.L,lu.U
        factor_bytes=sum(a.nbytes for a in [lower.data,lower.indices,lower.indptr,upper.data,upper.indices,upper.indptr,lu.perm_r,lu.perm_c])
    return update,dict(cache_prepare_seconds=time.perf_counter()-start,retained_factor_bytes=int(factor_bytes))


def benchmark(method,geometry,h,config,query_points):
    update,info=prepare(method,geometry,h,config)
    samples=[];errors=[];fresh_samples=[];fresh_errors=[]
    for delta in (.01,-.01,.02):
        target=Geometry(geometry.shape,geometry.angle,geometry.shift+delta,geometry.square_half)
        start=time.perf_counter();field=update(target);samples.append(time.perf_counter()-start)
        errors.append(float(np.sqrt(np.mean((field.evaluate(query_points)-target(query_points))**2))))
        from comparators import build
        start=time.perf_counter();fresh,_=build(method,target,h=h,**config);fresh_samples.append(time.perf_counter()-start)
        fresh_errors.append(float(np.sqrt(np.mean((fresh.evaluate(query_points)-target(query_points))**2))))
    return dict(info,cached_update_samples=samples,cached_update_seconds=float(np.median(samples)),
                cached_update_rmse=errors,full_rebuild_samples=fresh_samples,full_rebuild_seconds=float(np.median(fresh_samples)),
                full_rebuild_rmse=fresh_errors,editing_rule='shifted SDF, original interpolation nodes fixed')
