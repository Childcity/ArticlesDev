"""Пункт 1: вся конструкція статті, вибір вузлів і діагностика СЛАР."""
import numpy as np
from scipy.sparse.linalg import splu
from core import Geometry,lattice,matrix,fit,sampling,select_isoline_nodes


def run(h=.25,rho=2.,order=2,jitter=0.,margin=True,strategy='isolines',level_step=None):
    r=rho*h;delta=level_step if level_step is not None else h/2
    centers=lattice(h,margin=r if margin else 0)
    geometry=Geometry('circle')
    if strategy=='isolines':nodes,info=select_isoline_nodes(centers,geometry,r,h,delta)
    else:nodes=centers.copy();info=dict(unique_nodes=len(nodes),max_displacement=0.)
    axis,points=sampling(resolution=61);query=matrix(points,centers,r,order)
    a=matrix(nodes,centers,r,order)
    singular=np.linalg.svd(a.toarray(),compute_uv=False) if len(centers)<=900 else None
    threshold=singular[0]*len(centers)*np.finfo(float).eps if singular is not None else None
    stats=dict(h=h,rho=rho,order=order,strategy=strategy,level_step=delta,margin=margin,nodes=len(centers),
               uncovered_fraction=float(np.mean(np.diff(query.indptr)==0)),
               rank=int(np.sum(singular>threshold)) if singular is not None else None,
               condition=float(singular[0]/singular[-1]) if singular is not None else None)
    stats.update(info)
    errors=[]
    try:
        model=fit(centers,geometry,r,order,h=h,strategy=strategy,level_step=delta)
        lu=splu(a.tocsc())
        # Це окремі діагностичні праві частини на вузлах, вибраних за SDF кола.
        # Константа не є SDF; не застосовуємо до неї геометричну проєкцію.
        for values,truth in [(np.ones(len(nodes)),np.ones(len(points))),
                              (1+.3*nodes[:,0]-.2*nodes[:,1],1+.3*points[:,0]-.2*points[:,1])]:
            errors.append(query@lu.solve(values)-truth)
        errors.append(model.evaluate(points)-geometry(points))
        stats.update(status='ok',constant_max=float(np.max(abs(errors[0]))),
                     affine_max=float(np.max(abs(errors[1]))),node_residual=model.residual,
                     sdf_rmse=float(np.sqrt(np.mean(errors[2]**2))))
    except (ValueError,RuntimeError) as error:
        stats.update(status='failed',error=str(error))
    return stats,axis,errors,singular,centers,nodes


def figure(result):
    import matplotlib.pyplot as plt
    stats,axis,errors,singular,centers,nodes=result
    fig,ax=plt.subplots(1,3,figsize=(12,3.6),layout='constrained')
    ax[0].scatter(centers[:,0],centers[:,1],s=10,marker='+',label='Fixed centers')
    ax[0].scatter(nodes[:,0],nodes[:,1],s=8,label='Interpolation nodes')
    ax[0].legend(fontsize=8);ax[0].set_aspect('equal');ax[0].set_title(stats['strategy'])
    if errors:
        im=ax[1].imshow(errors[2].reshape(len(axis),-1).T,origin='lower',extent=[-1,1,-1,1],cmap='coolwarm')
        fig.colorbar(im,ax=ax[1]);ax[1].set_title('SDF error on independent grid')
    else:ax[1].text(.05,.5,stats['error'][:80],wrap=True,transform=ax[1].transAxes)
    if singular is not None:ax[2].semilogy(singular,'.')
    ax[2].set_title('Singular values')
    return fig
