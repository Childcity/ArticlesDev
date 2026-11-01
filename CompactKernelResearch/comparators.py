"""Однакові центри та точність float64 для незалежних базових методів.

Основний алгоритм статті не змінено. Wendland — окремі конкуренти;
сіткова кубічна схема — конкретно RegularGridInterpolator not-a-knot.
"""
from dataclasses import dataclass
import time
import numpy as np
from scipy.spatial import cKDTree
from scipy.sparse.linalg import splu,spsolve
from scipy.interpolate import RegularGridInterpolator
from scipy.ndimage import distance_transform_edt
from core import lattice,select_isoline_nodes
from geometry import Geometry

METHODS=('pg_grid','pg_isolines','wendland_c2_grid','wendland_c2_isolines',
         'wendland_c4_grid','wendland_c4_isolines','linear','cubic','cubic_redistance')


class CountedGeometry(Geometry):
    """Лічильники API: аналітичні операції всередині проєктора не є SDF-викликами."""
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        object.__setattr__(self,'counts',dict(sdf_calls=0,sdf_points=0,projection_calls=0,projection_points=0))
    def __call__(self,p):
        self.counts['sdf_calls']+=1;self.counts['sdf_points']+=len(p)
        return super().__call__(p)
    def project_level(self,p,t):
        self.counts['projection_calls']+=1;self.counts['projection_points']+=len(p)
        return super().project_level(p,t)


def basis(q,family,order=4):
    q=np.asarray(q);u=np.maximum(1-q,0)
    if family=='pg':return np.maximum(1-q*q,0)**(order+1)
    if family=='wendland_c2':return u**4*(4*q+1)
    if family=='wendland_c4':return u**6*(35*q*q+18*q+3)/3
    raise ValueError(family)


def basis_derivative(q,family,order=4):
    q=np.asarray(q);u=np.maximum(1-q,0)
    if family=='pg':return -2*(order+1)*q*np.maximum(1-q*q,0)**order
    if family=='wendland_c2':return -20*q*u**3
    if family=='wendland_c4':return -(56/3)*q*(5*q+1)*u**5
    raise ValueError(family)


def collocation(points,centers,radius,family,order):
    a=cKDTree(points).sparse_distance_matrix(cKDTree(centers),radius,output_type='coo_matrix')
    a.data=basis(a.data/radius,family,order)
    a=a.tocsr();a.eliminate_zeros();return a


@dataclass
class RBFField:
    centers: np.ndarray
    coefficients: np.ndarray
    radius: float
    family: str
    order: int
    def evaluate(self,p):
        p=np.asarray(p);parts=[]
        for start in range(0,len(p),1024):
            parts.append(collocation(p[start:start+1024],self.centers,self.radius,self.family,self.order)@self.coefficients)
        return np.concatenate(parts) if parts else np.empty(0)
    def gradient(self,p):
        result=np.zeros_like(p,dtype=float)
        for start in range(0,len(p),1024):
            points=p[start:start+1024]
            a=cKDTree(points).sparse_distance_matrix(cKDTree(self.centers),self.radius,output_type='coo_matrix')
            factor=np.zeros_like(a.data);valid=a.data>1e-14
            factor[valid]=basis_derivative(a.data[valid]/self.radius,self.family,self.order)/(self.radius*a.data[valid])
            values=(points[a.row]-self.centers[a.col])*(factor*self.coefficients[a.col])[:,None]
            np.add.at(result[start:start+len(points)],a.row,values)
        return result
    @property
    def stored_bytes(self):
        # Координати регулярних центрів можна відновити з O(D) метаданих.
        return int(self.coefficients.nbytes)


@dataclass
class GridField:
    interpolator: object
    payload_bytes: int
    h: float
    def evaluate(self,p):return self.interpolator(p)
    def gradient(self,p):
        # Запити — неперервні Sobol-точки; на вузлових площинах linear похідна неєдина.
        step=self.h*1e-5
        return np.column_stack([(self.evaluate(p+np.eye(p.shape[1])[j]*step)-
                                 self.evaluate(p-np.eye(p.shape[1])[j]*step))/(2*step) for j in range(p.shape[1])])
    @property
    def stored_bytes(self):return self.payload_bytes


def build(method,geometry,h=.25,rho=2.,order=4,delta_ratio=.5,extent=1.,margin=None,diagnostics=False):
    if method not in METHODS:raise ValueError(method)
    start=time.perf_counter();dim=3 if geometry.shape in ('sphere','torus') else 2
    # Однаковий запас усіх методів у парній задачі; незалежний від обраного rho.
    margin=4*h if margin is None else margin
    centers=lattice(h,dim,margin=margin,extent=extent)
    stats=dict(method=method,h=h,rho=rho,order=order,delta_ratio=delta_ratio,nodes=len(centers),
               projection_seconds=0.,solve_seconds=0.,node_residual=0.)
    if method in ('linear','cubic','cubic_redistance'):
        axes=[np.unique(centers[:,i]) for i in range(dim)]
        values=geometry(centers).reshape([len(a) for a in axes])
        cubic=method!='linear'
        kwargs=dict(method='cubic' if cubic else 'linear',bounds_error=True)
        if cubic:kwargs['solver']=spsolve
        interpolation=RegularGridInterpolator(axes,values,**kwargs)
        if method=='cubic_redistance':
            # Явна сіткова baseline: оцінюємо cubic на вдвічі густішій сітці й EDT.
            fine=[np.linspace(a[0],a[-1],2*len(a)-1) for a in axes]
            points=np.stack(np.meshgrid(*fine,indexing='ij'),-1).reshape(-1,dim)
            mask=interpolation(points).reshape([len(a) for a in fine])<=0
            signed=(distance_transform_edt(~mask,sampling=h/2)-distance_transform_edt(mask,sampling=h/2))
            # Повна додаткова пам'ять записується: не порівнюємо EDT як безкоштовну.
            interpolation=RegularGridInterpolator(fine,signed,method='linear',bounds_error=True)
            model=GridField(interpolation,int(signed.nbytes),h/2)
        else:
            payload=interpolation._spline.c.nbytes if cubic else values.nbytes
            model=GridField(interpolation,int(payload),h)
    else:
        family=method.rsplit('_',1)[0];strategy=method.rsplit('_',1)[1]
        nodes=centers
        if strategy=='isolines':
            t=time.perf_counter();nodes,info=select_isoline_nodes(centers,geometry,rho*h,h,delta_ratio*h)
            stats['projection_seconds']=time.perf_counter()-t;stats.update(info)
            if info['unique_nodes']!=len(nodes):raise ValueError('coincident_nodes')
        t=time.perf_counter();a=collocation(nodes,centers,rho*h,family,order);b=geometry(nodes)
        coeff=splu(a.tocsc()).solve(b);stats['solve_seconds']=time.perf_counter()-t
        residual=float(np.max(abs(a@coeff-b)));stats['node_residual']=residual
        if not np.isfinite(coeff).all() or residual>1e-7*max(1,float(np.max(abs(b)))):
            raise ValueError('unstable_solve')
        model=RBFField(centers,coeff,rho*h,family,order)
        stats['matrix_nnz']=a.nnz
        if diagnostics and len(centers)<=600:
            singular=np.linalg.svd(a.toarray(),compute_uv=False)
            stats['rank']=int(np.sum(singular>len(centers)*np.finfo(float).eps*singular[0]))
            stats['condition']=float(singular[0]/singular[-1]) if singular[-1]>0 else None
    stats.update(build_seconds=time.perf_counter()-start,stored_bytes=model.stored_bytes)
    return model,stats


def candidates(method):
    """До шести кандидатів на метод; скінченний зафіксований бюджет, не повний оптимум."""
    if method in ('linear','cubic','cubic_redistance'):return [dict(rho=2.,order=4,delta_ratio=.5)]
    if method=='pg_grid':return [dict(rho=r,order=n,delta_ratio=.5) for r in (1.5,2.,3.) for n in (2,4)]
    if method=='pg_isolines':
        return [dict(rho=r,order=n,delta_ratio=d) for r,n,d in
                [(1.5,2,.5),(1.5,4,1.),(2.,2,.25),(2.,4,.5),(3.,2,1.),(3.,4,.25)]]
    if method.endswith('_grid'):return [dict(rho=r,order=4,delta_ratio=.5) for r in (1.25,1.5,2.,2.5,3.,4.)]
    return [dict(rho=r,order=4,delta_ratio=d) for r in (1.5,2.,3.) for d in (.5,1.)]
