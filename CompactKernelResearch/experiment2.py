"""Пункт 2: точні SDF, критичні офсети й геометричні відмови."""
import numpy as np
from core import Geometry,lattice,fit,sampling,metrics
SHAPES=['circle','square','two_circles','neck','sphere','torus']


def offset_metrics(truth,field,axis,offset,geometry):
    """Відстані між хмарами вершин дискретних ізоповерхонь, не строгі межі."""
    from scipy.spatial import cKDTree
    from skimage.measure import find_contours,marching_cubes
    def extract(values):
        if not values.min()<offset<values.max():return np.empty((0,values.ndim))
        if values.ndim==2:
            contours=find_contours(values,offset)
            return np.concatenate(contours)*(axis[1]-axis[0])+axis[0] if contours else np.empty((0,2))
        vertices,*_=marching_cubes(values,offset,spacing=(axis[1]-axis[0],)*3)
        return vertices+axis[0]
    reference=extract(truth);predicted=extract(field)
    stats=dict(reference_surface_samples=len(reference),model_surface_samples=len(predicted))
    if len(reference) and len(predicted):
        stats['sampled_offset_hausdorff']=float(max(cKDTree(reference).query(predicted)[0].max(),
                                                       cKDTree(predicted).query(reference)[0].max()))
        stats['model_surface_sdf_error']=float(np.max(np.abs(geometry(predicted)-offset)))
    return stats


def run(shape='circle',h=.2,rho=2.,order=2,jitter=0.,angle=25.,shift=.03,offset=0.,
        resolution=None,strategy='isolines',level_step=None,square_half=.48,extent=1.,margin=True):
    dim=3 if shape in ('sphere','torus') else 2
    resolution=resolution or (35 if dim==3 else 151)
    radius=h*rho;delta=level_step if level_step is not None else h/2
    centers=lattice(h,dim,margin=radius if margin else 0,extent=extent)
    geometry=Geometry(shape,angle,shift,square_half)
    axis,points=sampling(dim,resolution,extent)
    exact=geometry(points)
    stats=dict(shape=shape,h=h,rho=rho,order=order,strategy=strategy,level_step=delta,
               angle=angle,shift=shift,offset=offset,resolution=resolution,nodes=len(centers),
               square_half=square_half,extent=extent,margin=margin)
    model=None;predicted=np.full_like(exact,np.nan)
    try:
        model=fit(centers,geometry,radius,order,jitter,h,strategy=strategy,level_step=delta)
        predicted=model.evaluate(points)
        stats.update(metrics(exact,predicted,resolution,dim,offset),status='ok',
                     fit_seconds=model.seconds,node_residual=model.residual,
                     active_entries=model.nnz,**model.node_info)
        stats.update(offset_metrics(exact.reshape([resolution]*dim),predicted.reshape([resolution]*dim),axis,offset,geometry))
    except (RuntimeError,ValueError) as error:
        stats.update(status='failed',error=str(error))
    return stats,axis,exact.reshape([resolution]*dim),predicted.reshape([resolution]*dim),model


def figure(result):
    import matplotlib.pyplot as plt
    stats,axis,truth,field,model=result
    if stats['status']!='ok':
        fig,ax=plt.subplots(figsize=(9,3));ax.axis('off');ax.text(.02,.5,stats['error'],wrap=True)
        return fig
    if truth.ndim==3:
        truth=truth[:,:,len(axis)//2];field=field[:,:,len(axis)//2]
    fig,ax=plt.subplots(1,2,figsize=(9,3.8),layout='constrained')
    im=ax[0].imshow((field-truth).T,origin='lower',extent=[axis[0],axis[-1],axis[0],axis[-1]],cmap='coolwarm')
    fig.colorbar(im,ax=ax[0]);ax[0].set_title('Field error (3D: z=0 slice)')
    if model is not None and truth.ndim==2 and model.nodes.shape[1]==2:
        ax[1].scatter(model.nodes[:,0],model.nodes[:,1],s=3,alpha=.4,color='blue')
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
    stats,axis,truth,field,model=result
    fig=plt.figure(figsize=(9,4),layout='constrained')
    for i,(values,title) in enumerate([(truth,'Exact'),(field,'Model')]):
        ax=fig.add_subplot(1,2,i+1,projection='3d')
        if stats['status']=='ok' and values.min()<stats['offset']<values.max():
            v,f,_,_=marching_cubes(values,stats['offset'],spacing=(axis[1]-axis[0],)*3)
            v+=axis[0]
            ax.plot_trisurf(v[:,0],v[:,1],v[:,2],triangles=f,linewidth=0,alpha=.8)
        ax.set_title(title);ax.set(xlim=(-1,1),ylim=(-1,1),zlim=(-1,1))
    return fig


def paper_cases():
    """Умови, подібні до рис. 4--6/8, без заяви про піксельне відтворення.

    Стаття задає 13x13, h=.25, Δ=.25 та .081384. r, n, точний розмір
    квадрата й другий кут не наведено чисельно: тут вони явно обрані.
    """
    # r=1,n=4 явно наведені для ілюстрації базису на рис.2;
    # r=.5 залишено як контроль чутливості до невстановленого параметра.
    for rho in (2.,4.):
        for angle in (45.,35.):
            for strategy,delta in [('grid',.25),('isolines',.25),('isolines',.081384)]:
                yield run(shape='square',h=.25,rho=rho,order=4,angle=angle,shift=0,
                          strategy=strategy,level_step=delta,square_half=.85,
                          extent=1.5,margin=False,resolution=151)


def comparison_figure(results):
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,len(results),figsize=(4*len(results),4),layout='constrained')
    # Спільна шкала SDF: автоматичне нормування кожної панелі приховує похибки.
    lo=min(float(r[2].min()) for r in results)
    hi=max(float(r[2].max()) for r in results)
    levels=np.linspace(lo,hi,16);filled=None
    for ax,result in zip(np.atleast_1d(axes),results):
        stats,axis,truth,field,model=result
        if stats['status']=='ok':
            filled=ax.contourf(axis,axis,field.T,levels=levels,cmap='Greys_r',extend='both')
            ax.contour(axis,axis,truth.T,levels=[0],colors='blue',linewidths=1)
            ax.contour(axis,axis,field.T,levels=[0],colors='red',linewidths=1)
            ax.scatter(model.nodes[:,0],model.nodes[:,1],s=5,color='black')
        else:ax.text(.05,.5,stats['error'][:100],wrap=True,transform=ax.transAxes)
        ax.set_aspect('equal')
        pad=.1*(axis[-1]-axis[0])
        ax.set(xlim=(axis[0]-pad,axis[-1]+pad),ylim=(axis[0]-pad,axis[-1]+pad))
        ax.set_title(f"{stats['strategy']}, Δ={stats['level_step']:.6g}, r={stats['h']*stats['rho']:g}")
    if filled is not None:
        fig.colorbar(filled,ax=np.atleast_1d(axes).tolist(),shrink=.8,label='Interpolated SDF')
    fig.suptitle('Blue: exact contour; red: model; black: interpolation nodes',fontsize=10)
    return fig
