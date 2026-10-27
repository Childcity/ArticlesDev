"""Пункт 1: гладкість, покриття, відтворення та чисельний ранг."""
import numpy as np
from core import kernel, lattice, matrix, fit, sampling


def run(h=.25, rho=2., order=2, jitter=0., margin=True):
    r = rho*h
    centers = lattice(h, margin=r if margin else 0)
    axis, points = sampling(resolution=61)
    query = matrix(points,centers,r,order)
    models = [fit(centers,f,r,order,jitter,h) for f in
              (lambda p: np.ones(len(p)), lambda p: 1+.3*p[:,0]-.2*p[:,1])]
    exact = [np.ones(len(points)),1+.3*points[:,0]-.2*points[:,1]]
    errors = [m.evaluate(points)-f for m,f in zip(models,exact)]
    a = matrix(models[0].nodes,centers,r,order)
    # Повна SVD лише на малих матрицях; великі не отримують вигаданого рангу.
    singular = np.linalg.svd(a.toarray(),compute_uv=False) if len(centers)<=900 else None
    threshold = singular[0]*len(centers)*np.finfo(float).eps if singular is not None else None
    stats = dict(h=h,rho=rho,order=order,jitter=jitter,margin=margin,nodes=len(centers),
                 uncovered_fraction=float(np.mean(np.diff(query.indptr)==0)),
                 constant_max=float(np.max(np.abs(errors[0]))),affine_max=float(np.max(np.abs(errors[1]))),
                 rank=int(np.sum(singular>threshold)) if singular is not None else None,
                 condition=float(singular[0]/singular[-1]) if singular is not None else None,
                 node_residual=models[0].residual)
    return stats,axis,errors,singular


def figure(result):
    import matplotlib.pyplot as plt
    stats,axis,errors,singular=result
    fig,ax=plt.subplots(1,3,figsize=(12,3.4),layout='constrained')
    x=np.linspace(-1.2,1.2,501)
    for n in (1,2,3,4):ax[0].plot(x,kernel(abs(x),1,n),label=f'n={n}')
    ax[0].legend();ax[0].set_title('Author kernel, r=1')
    im=ax[1].imshow(errors[0].reshape(len(axis),-1).T,origin='lower',extent=[-1,1,-1,1],cmap='coolwarm')
    fig.colorbar(im,ax=ax[1]);ax[1].set_title('Constant reproduction error')
    if singular is not None:ax[2].semilogy(singular,'.')
    ax[2].set_title('Singular values of collocation matrix')
    return fig

if __name__=='__main__':
    print(run()[0])
