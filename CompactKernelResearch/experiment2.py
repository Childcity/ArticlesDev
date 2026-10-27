"""Пункт 2: точні SDF, критичні офсети й геометричні відмови."""
import numpy as np
from core import lattice,fit,sdf,sampling,metrics
SHAPES=['circle','square','two_circles','neck','sphere','torus']


def run(shape='circle',h=.2,rho=2.,order=2,jitter=0.,angle=25.,shift=.03,offset=0.,resolution=None):
    dim=3 if shape in ('sphere','torus') else 2
    resolution=resolution or (35 if dim==3 else 151)
    radius=h*rho
    centers=lattice(h,dim,margin=radius)
    function=lambda p:sdf(p,shape,angle,shift)
    model=fit(centers,function,radius,order,jitter,h)
    axis,points=sampling(dim,resolution)
    exact=function(points);predicted=model.evaluate(points)
    stats=metrics(exact,predicted,resolution,dim,offset)
    stats.update(shape=shape,h=h,rho=rho,order=order,jitter=jitter,angle=angle,shift=shift,offset=offset,
                 resolution=resolution,nodes=len(centers),fit_seconds=model.seconds,node_residual=model.residual,
                 active_entries=model.nnz)
    return stats,axis,exact.reshape([resolution]*dim),predicted.reshape([resolution]*dim)


def figure(result):
    import matplotlib.pyplot as plt
    stats,axis,truth,field=result
    if truth.ndim==3:
        truth=truth[:,:,len(axis)//2];field=field[:,:,len(axis)//2]
    fig,ax=plt.subplots(1,2,figsize=(9,3.8),layout='constrained')
    im=ax[0].imshow((field-truth).T,origin='lower',extent=[-1,1,-1,1],cmap='coolwarm')
    fig.colorbar(im,ax=ax[0]);ax[0].set_title('Field error (3D: z=0 slice)')
    level=stats['offset']
    for values,color,style in [(truth,'black','solid'),(field,'red','dashed')]:
        if values.min()<level<values.max():
            ax[1].contour(axis,axis,values.T,levels=[level],colors=color,linestyles=style)
    ax[1].set_aspect('equal');ax[1].set_title(f"{stats['shape']}, t={level:g}: exact black / model red")
    return fig


def surface_figure(result):
    """Об'ємні дані дають справжні 3D-ізоповерхні, а не лише зріз."""
    import matplotlib.pyplot as plt
    from skimage.measure import marching_cubes
    stats,axis,truth,field=result
    fig=plt.figure(figsize=(9,4),layout='constrained')
    for i,(values,title) in enumerate([(truth,'Exact'),(field,'Model')]):
        ax=fig.add_subplot(1,2,i+1,projection='3d')
        if values.min()<stats['offset']<values.max():
            v,f,_,_=marching_cubes(values,stats['offset'],spacing=(axis[1]-axis[0],)*3)
            v-=1
            ax.plot_trisurf(v[:,0],v[:,1],v[:,2],triangles=f,linewidth=0,alpha=.8)
        ax.set_title(title);ax.set(xlim=(-1,1),ylim=(-1,1),zlim=(-1,1))
    return fig
