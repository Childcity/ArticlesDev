"""Псевдогаусове ядро зі статті та інтерполянт із вибором точок на ізолініях."""
from dataclasses import dataclass
import time
import numpy as np
from scipy.spatial import cKDTree
from scipy.sparse.linalg import splu
from scipy.ndimage import label
from geometry import Geometry, sdf, polygon_sdf, POLYGON


def kernel(distance, radius, order):
    """pg_n,r(s) = (1 - (s/r)^2)_+^(n+1), n >= 1."""
    if radius <= 0 or int(order) != order or order < 1:
        raise ValueError('radius > 0 and integer order >= 1 required')
    return np.maximum(1 - (np.asarray(distance) / radius)**2, 0)**(order + 1)


def lattice(h, dim=2, margin=0.0, extent=1.0):
    """Область оцінки [-extent,extent]^D; центри продовжено на margin."""
    if h <= 0 or margin < 0:
        raise ValueError('invalid grid')
    k = int(np.ceil((extent + margin) / h))
    axis = np.arange(-k, k + 1) * h
    return np.stack(np.meshgrid(*([axis]*dim), indexing='ij'), -1).reshape(-1, dim)


def matrix(points, centers, radius, order):
    # Просторовий індекс відкидає центри поза підтримкою без щільної матриці.
    m = cKDTree(points).sparse_distance_matrix(cKDTree(centers), radius,
                                               output_type='coo_matrix')
    m.data = kernel(m.data, radius, order)
    m = m.tocsr()
    m.eliminate_zeros()
    return m


@dataclass
class Model:
    centers: np.ndarray
    nodes: np.ndarray
    radius: float
    order: int
    coefficients: np.ndarray
    residual: float
    seconds: float
    nnz: int
    node_info: dict

    def evaluate(self, points):
        # Пакети обмежують пікову пам'ять для об'ємної 3D-сітки.
        return np.concatenate([matrix(p, self.centers, self.radius, self.order)
                               @ self.coefficients for p in np.array_split(points, max(1, len(points)//8000+1))])


def select_isoline_nodes(centers, geometry, radius, h, level_step):
    """Стратегія статті: найближча точка об'єднання рівнів d=q*Δ.

    Перебираємо всі q, для яких |d(c)-qΔ|<r. Через 1-ліпшицевість
    точної SDF жодний інший рівень не може дати допустимий вузол.
    Не замінюємо найближчу проєкцію округленням d і кроком за градієнтом.
    При рівних відстанях вибираємо менший q, а в проєкторі — сталий напрям.
    """
    if not 0 < level_step <= h*(1+1e-12):
        raise ValueError('Article requires 0 < level_step <= h')
    values=geometry(centers)
    lower=np.ceil((values-radius)/level_step).astype(int)
    upper=np.floor((values+radius)/level_step).astype(int)
    nodes=np.full_like(centers,np.nan);best=np.full(len(centers),np.inf)
    selected_levels=np.full(len(centers),np.nan)
    for q in range(int(lower.min()),int(upper.max())+1):
        indices=np.where((lower<=q)&(upper>=q))[0]
        if not len(indices):continue
        projected=geometry.project_level(centers[indices],q*level_step)
        distance=np.linalg.norm(projected-centers[indices],axis=1)
        valid=np.isfinite(distance)&(distance<radius*(1-1e-12))
        take=valid & (distance<best[indices]-1e-12)
        chosen=indices[take];nodes[chosen]=projected[take];best[chosen]=distance[take]
        selected_levels[chosen]=q*level_step
    if not np.all(np.isfinite(best)):
        raise ValueError('No admissible isoline node within support for some centers')
    return nodes,dict(level_step=float(level_step),max_displacement=float(best.max()),
                      level_residual=float(np.max(np.abs(geometry(nodes)-selected_levels))),
                      unique_nodes=int(len(np.unique(np.round(nodes,11),axis=0))))


def fit(centers, function, radius, order=2, jitter=0.0, h=.25, seed=0,
        strategy='isolines', level_step=None):
    """Рівняння (7)--(13) DOCX; центри не рухаються при виборі вузлів.

    Немає прихованої регуляризації чи випадкового виправлення дубльованих
    вузлів. Такі випадки фіксуються як відмова, а не підміна методу.
    """
    start=time.perf_counter()
    if strategy=='isolines':
        if not isinstance(function,Geometry):
            raise ValueError('Isoline strategy requires Geometry with nearest-level projection')
        nodes,info=select_isoline_nodes(centers,function,radius,h,level_step if level_step is not None else h)
    elif strategy=='grid':
        nodes=centers.copy();info=dict(max_displacement=0.,unique_nodes=len(centers))
    elif strategy=='random':
        if not 0<=jitter<radius/h:raise ValueError('invalid random displacement')
        rng=np.random.default_rng(seed);direction=rng.normal(size=centers.shape)
        direction/=np.maximum(np.linalg.norm(direction,axis=1,keepdims=True),1e-15)
        nodes=centers+direction*jitter*h
        info=dict(max_displacement=jitter*h,unique_nodes=len(centers))
    else:raise ValueError('Unknown node strategy')
    a=matrix(nodes,centers,radius,order)
    info['strategy']=strategy
    if info['unique_nodes']!=len(nodes):
        raise ValueError(f"Coincident interpolation nodes: {info['unique_nodes']}/{len(nodes)}; no silent perturbation")
    values=function(nodes)
    coefficients=splu(a.tocsc()).solve(values)
    residual=float(np.max(np.abs(a@coefficients-values)))
    if not np.isfinite(coefficients).all() or residual>1e-7*max(1,float(np.max(np.abs(values)))):
        raise ValueError('Unstable collocation solve: residual exceeds 1e-7 relative scale')
    return Model(centers,nodes,radius,order,coefficients,residual,time.perf_counter()-start,a.nnz,info)


def sampling(dim=2, resolution=101, extent=1.0):
    axes = np.linspace(-extent,extent,resolution)
    points = np.stack(np.meshgrid(*([axes]*dim),indexing='ij'),-1).reshape(-1,dim)
    return axes, points


def metrics(exact, predicted, resolution, dim=2, offset=0.0):
    band = np.abs(exact-offset)<.2
    truth = (exact<=offset).reshape([resolution]*dim)
    result = (predicted<=offset).reshape([resolution]*dim)
    # Зв'язність уздовж осей; результат залежить від роздільності оцінки.
    return dict(rmse=float(np.sqrt(np.mean((predicted-exact)**2))),
                band_rmse=float(np.sqrt(np.mean((predicted[band]-exact[band])**2))),
                sampled_max=float(np.max(np.abs(predicted-exact))),
                sign_error=float(np.mean(truth!=result)),
                components_exact=int(label(truth)[1]), components_model=int(label(result)[1]))
