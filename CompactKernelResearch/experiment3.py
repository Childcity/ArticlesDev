"""Парні серії: та сама геометрія й центри, grid проти авторських ізоліній."""
from experiment2 import run


def configurations():
    base=dict(shape='square',h=.25,rho=2.,order=2,angle=20.,shift=.03,offset=0.,resolution=101)
    factors=dict(h=[.16,.2,.25,.32],rho=[1.,1.5,2.,3.],order=[1,2,3,4],
                 angle=[0.,15.,30.,45.],shift=[0.,.04,.10],offset=[-.15,0.,.15],
                 delta_ratio=[.25,.5,1.])
    for factor,values in factors.items():
        for value in values:
            config=dict(base)
            if factor!='delta_ratio':config[factor]=value
            ratio=value if factor=='delta_ratio' else .5
            for strategy in ('grid','isolines'):
                yield factor,dict(config,strategy=strategy,level_step=ratio*config['h'])
    for h in [.16,.2,.25,.32]:
        for strategy in ('grid','isolines'):
            yield 'fixed_r',dict(base,h=h,rho=.5/h,strategy=strategy,level_step=h/2)
    for shape,offsets in [('two_circles',[0,.06,.08,.10]),('neck',[-.12,-.10,-.08,0]),
                          ('circle',[-.57,-.55,-.53]),('torus',[-.21,-.19,.30,.34])]:
        for offset in offsets:
            for strategy in ('grid','isolines'):
                yield 'critical_offset',dict(base,shape=shape,offset=offset,angle=0.,shift=0.,
                    resolution=35 if shape=='torus' else 151,strategy=strategy,level_step=base['h']/2)


def run_sweep():
    rows=[]
    for factor,config in configurations():
        stats,*_=run(**config);stats['factor']=factor
        stats['delta_ratio']=config['level_step']/config['h']
        rows.append(stats)
    return rows


def figure(rows):
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(3,3,figsize=(12,10),layout='constrained')
    for ax,factor in zip(axes.flat,['h','rho','order','delta_ratio','angle','shift','offset','fixed_r','critical_offset']):
        if factor=='critical_offset':
            for strategy in ('grid','isolines'):
                data=[r for r in rows if r['factor']==factor and r['strategy']==strategy and r['status']=='ok']
                ax.scatter([r['offset'] for r in data],[r['band_rmse'] for r in data],s=18,label=strategy)
            ax.set_xlabel('t (mixed shapes)')
        else:
            key='h' if factor=='fixed_r' else factor
            for strategy in ('grid','isolines'):
                data=sorted([r for r in rows if r['factor']==factor and r['strategy']==strategy and r['status']=='ok'],key=lambda r:r[key])
                ax.plot([r[key] for r in data],[r['band_rmse'] for r in data],'o-',label=strategy)
            ax.set_xlabel(key)
        failed=sum(r['status']!='ok' for r in rows if r['factor']==factor)
        ax.set(title=f'{factor} (failed: {failed})',ylabel='Band RMSE');ax.grid(alpha=.3);ax.legend(fontsize=7)
    return fig


def optimize_level_step(shape='square',h=.25,rho=4.,order=4,angle=35.,shift=0.,
                        square_half=.85,extent=1.5,margin=False,calibration_size=512,
                        coarse_count=17,validation_resolution=151):
    """Чисельний добір Δ за схемою обговорення рис.8.

    Стаття не задає норму похибки та оптимізатор. Тут явно обрано RMSE
    поля на Sobol-точках; незалежна сітка використовується лише після вибору.
    Грубий пошук + локальне bounded-уточнення не є доказом глобального мінімуму.
    """
    import time
    import numpy as np
    from scipy.optimize import minimize_scalar
    from scipy.stats import qmc
    from core import Geometry,lattice,fit
    if calibration_size<4 or coarse_count<3:raise ValueError('Insufficient calibration budget')
    # Sobol-вибірка детермінована; її розмір — степінь двійки.
    power=int(np.ceil(np.log2(calibration_size)))
    dim=3 if shape in ('sphere','torus') else 2
    points=(2*qmc.Sobol(dim,scramble=True,seed=2026).random_base2(power)-1)*extent
    geometry=Geometry(shape,angle,shift,square_half)
    exact=geometry(points);centers=lattice(h,dim,margin=rho*h if margin else 0,extent=extent)
    trials=[];cache={}
    def objective(delta):
        key=float(delta)
        if key in cache:return cache[key]
        start=time.perf_counter()
        row=dict(level_step=key)
        try:
            model=fit(centers,geometry,rho*h,order,h=h,strategy='isolines',level_step=key)
            value=float(np.sqrt(np.mean((model.evaluate(points)-exact)**2)))
            if not np.isfinite(value):raise ValueError('Non-finite calibration objective')
            row.update(status='ok',calibration_rmse=value,node_residual=model.residual)
        except (ValueError,RuntimeError) as error:
            value=float('inf');row.update(status='failed',error=str(error))
        row['seconds']=time.perf_counter()-start;trials.append(row);cache[key]=value
        return value
    bounds=(.15*h,h)
    coarse=np.linspace(*bounds,coarse_count)
    # Контрольне значення статті також оцінюється, але не проголошується оптимумом.
    candidates=np.unique(np.r_[coarse,h/2,.081384] if bounds[0]<=.081384<=bounds[1] else np.r_[coarse,h/2])
    values=np.array([objective(d) for d in candidates])
    # Уточнюємо три найкращі грубі околиці. Функція негладка при зміні рівня q.
    for index in np.argsort(values)[:3]:
        lo=candidates[max(0,index-1)];hi=candidates[min(len(candidates)-1,index+1)]
        if hi>lo:
            minimize_scalar(objective,bounds=(lo,hi),method='bounded',
                            options=dict(xatol=h*1e-5,maxiter=24))
    successful=[r for r in trials if r['status']=='ok']
    if not successful:raise ValueError('All level-step candidates failed')
    best=min(successful,key=lambda r:r['calibration_rmse'])
    params=dict(shape=shape,h=h,rho=rho,order=order,angle=angle,shift=shift,
                square_half=square_half,extent=extent,margin=margin,resolution=validation_resolution)
    results=[run(**params,strategy='grid',level_step=h),
             run(**params,strategy='isolines',level_step=h),
             run(**params,strategy='isolines',level_step=best['level_step'])]
    summary=dict(selected_step=best['level_step'],calibration_rmse=best['calibration_rmse'],
                 calibration_size=len(points),calibration_seed=2026,coarse_count=coarse_count,
                 bounds=list(bounds),objective='full-domain SDF RMSE on scrambled Sobol points',
                 validation_resolution=validation_resolution,trials=len(trials),
                 failed_trials=sum(r['status']=='failed' for r in trials),
                 shape=shape,h=h,rho=rho,order=order,angle=angle,shift=shift,
                 square_half=square_half,extent=extent,margin=margin,
                 validation=[r[0] for r in results])
    return summary,trials,results


def optimization_figure(summary,trials):
    import matplotlib.pyplot as plt
    data=sorted([r for r in trials if r['status']=='ok'],key=lambda r:r['level_step'])
    fig,ax=plt.subplots(figsize=(8,3.5),layout='constrained')
    ax.scatter([r['level_step'] for r in data],[r['calibration_rmse'] for r in data],s=18)
    ax.axvline(summary['selected_step'],color='red',label='Selected on calibration points')
    ax.axvline(.081384,color='grey',linestyle='--',label='Paper example: 0.081384')
    ax.set(xlabel='Isoline spacing Δ',ylabel='Calibration SDF RMSE',yscale='log')
    ax.legend();ax.grid(alpha=.3)
    return fig
