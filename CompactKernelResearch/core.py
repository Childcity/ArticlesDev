"""Авторське компактне ядро та аналітичні геометричні еталони."""
from dataclasses import dataclass
import time
import numpy as np
from scipy.spatial import cKDTree
from scipy.sparse.linalg import splu
from scipy.ndimage import label
from matplotlib.path import Path


def kernel(distance, radius, order):
    """pg_n,r(s) = (1 - (s/r)^2)_+^(n+1), n >= 1."""
    if radius <= 0 or int(order) != order or order < 1:
        raise ValueError('radius > 0 and integer order >= 1 required')
    return np.maximum(1 - (np.asarray(distance) / radius)**2, 0)**(order + 1)


def lattice(h, dim=2, margin=0.0):
    """Область оцінки [-1,1]^D; центри продовжено на margin."""
    if h <= 0 or margin < 0:
        raise ValueError('invalid grid')
    k = int(np.ceil((1 + margin) / h))
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

    def evaluate(self, points):
        # Пакети обмежують пікову пам'ять для об'ємної 3D-сітки.
        return np.concatenate([matrix(p, self.centers, self.radius, self.order)
                               @ self.coefficients for p in np.array_split(points, max(1, len(points)//8000+1))])


def fit(centers, function, radius, order=2, jitter=0.0, h=.25, seed=0):
    if not 0 <= jitter < radius/h:
        raise ValueError('node displacement must be smaller than support radius')
    rng = np.random.default_rng(seed)
    direction = rng.normal(size=centers.shape)
    direction /= np.maximum(np.linalg.norm(direction, axis=1, keepdims=True), 1e-15)
    nodes = centers + direction * (jitter*h)
    start = time.perf_counter()
    a = matrix(nodes, centers, radius, order)
    values = function(nodes)
    # Жодної прихованої регуляризації: сингулярні випадки є відмовами досліду.
    coefficients = splu(a.tocsc()).solve(values)
    residual = np.max(np.abs(a @ coefficients - values))
    return Model(centers, nodes, radius, order, coefficients, float(residual),
                 time.perf_counter()-start, a.nnz)


POLYGON = np.array([[-.85,-.4],[-.3,-.4],[-.3,-.10],[.3,-.10],
                    [.3,-.4],[.85,-.4],[.85,.4],[.3,.4],[.3,.10],
                    [-.3,.10],[-.3,.4],[-.85,.4]])


def polygon_sdf(p, vertices=POLYGON):
    """Точна евклідова відстань до сегментів простого багатокутника."""
    a = vertices
    b = np.roll(vertices, -1, axis=0)
    v = b-a
    w = p[:,None,:]-a
    t = np.clip(np.sum(w*v, axis=-1)/np.sum(v*v, axis=-1), 0, 1)
    distance = np.min(np.linalg.norm(w-t[:,:,None]*v, axis=-1), axis=1)
    inside = Path(np.vstack([vertices, vertices[0]])).contains_points(p)
    return np.where(inside, -distance, distance)


def sdf(points, shape='circle', angle=0.0, shift=0.0):
    p = np.asarray(points, dtype=float).copy()
    p[:,0] -= shift
    theta = np.deg2rad(angle)
    rot = np.array([[np.cos(theta),-np.sin(theta)], [np.sin(theta),np.cos(theta)]])
    p[:,:2] = p[:,:2] @ rot
    if shape in ('circle','sphere'):
        return np.linalg.norm(p,axis=1)-.55
    if shape == 'square':
        q = np.abs(p)-.48
        return np.linalg.norm(np.maximum(q,0),axis=1)+np.minimum(np.max(q,axis=1),0)
    if shape == 'two_circles':
        # Диски не перетинаються, тому min їх SDF є точною SDF об'єднання.
        return np.minimum(np.linalg.norm(p-[-.4,0],axis=1),
                          np.linalg.norm(p-[.4,0],axis=1))-.32
    if shape == 'neck':
        return polygon_sdf(p)
    if shape == 'torus':
        return np.hypot(np.linalg.norm(p[:,:2],axis=1)-.52,p[:,2])-.20
    raise ValueError(shape)


def sampling(dim=2, resolution=101):
    axes = np.linspace(-1,1,resolution)
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
