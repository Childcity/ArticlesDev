"""Зберігання готового інтерполянта: один коефіцієнт на вузол сітки.

NPZ — наша технічна реалізація ідеї статті, не запропонований авторами
новий стандарт. Положення точок інтерполяції та оригінальна SDF не потрібні.
"""
from dataclasses import dataclass
from functools import cached_property
import numpy as np
from core import matrix


@dataclass
class StoredField:
    origin: np.ndarray
    spacing: np.ndarray
    coefficients: np.ndarray
    radius: float
    order: int

    @cached_property
    def centers(self):
        axes=[a+h*np.arange(n) for a,h,n in zip(self.origin,self.spacing,self.coefficients.shape)]
        return np.stack(np.meshgrid(*axes,indexing='ij'),-1).reshape(-1,len(axes))

    def evaluate(self,points):
        points=np.asarray(points,dtype=float)
        if len(points)==0:return np.empty(0)
        result=[]
        for p in np.array_split(points,max(1,len(points)//8000+1)):
            result.append(matrix(p,self.centers,self.radius,self.order)@self.coefficients.ravel())
        return np.concatenate(result)

    def save(self,path):
        # Додаткові дані мають сталий розмір O(D), без масиву центрів чи вузлів.
        np.savez_compressed(path,version=np.array(1),origin=self.origin,spacing=self.spacing,
                            coefficients=self.coefficients,radius=np.array(self.radius),order=np.array(self.order))


def from_model(model):
    axes=[np.unique(model.centers[:,j]) for j in range(model.centers.shape[1])]
    if any(len(a)<2 for a in axes):raise ValueError('At least two centers per axis required')
    spacing=np.array([a[1]-a[0] for a in axes])
    if not all(np.allclose(np.diff(a),h,rtol=1e-10,atol=1e-12) for a,h in zip(axes,spacing)):
        raise ValueError('Regular lattice required')
    centers=np.stack(np.meshgrid(*axes,indexing='ij'),-1).reshape(-1,len(axes))
    if centers.shape!=model.centers.shape or not np.allclose(centers,model.centers,atol=1e-12):
        raise ValueError('Canonical complete regular lattice required')
    return StoredField(np.array([a[0] for a in axes]),spacing,
                       model.coefficients.reshape([len(a) for a in axes]).copy(),model.radius,model.order)


def load(path):
    with np.load(path,allow_pickle=False) as data:
        if set(data.files)!={'version','origin','spacing','coefficients','radius','order'} or int(data['version'])!=1:
            raise ValueError('Unsupported field archive')
        field=StoredField(data['origin'].copy(),data['spacing'].copy(),data['coefficients'].copy(),
                          float(data['radius']),int(data['order']))
    dim=field.coefficients.ndim
    if (dim not in (1,2,3) or field.origin.shape!=(dim,) or field.spacing.shape!=(dim,)
            or np.any(field.spacing<=0) or not np.isfinite(field.radius) or field.radius<=0 or field.order<1
            or not all(np.isfinite(a).all() for a in [field.origin,field.spacing,field.coefficients])):
        raise ValueError('Invalid field metadata')
    return field
