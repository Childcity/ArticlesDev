"""Пункт 3: контрольовані серії з незалежною зміною одного фактора."""
from experiment2 import run


def configurations():
    baseline=dict(shape='square',h=.25,rho=2.,order=2,jitter=0.,angle=20.,shift=.03,offset=0.,resolution=101)
    # Однакові контрольні умови дозволяють відділити ефекти параметрів.
    factors=dict(h=[.16,.2,.25,.32],rho=[1.,1.5,2.,3.],order=[1,2,3,4],
                 jitter=[0.,.1,.25],angle=[0.,15.,30.,45.],shift=[0.,.04,.10],offset=[-.15,0.,.15])
    for factor,values in factors.items():
        for value in values:yield factor,dict(baseline,**{factor:value})
    for h in [.16,.2,.25,.32]:
        yield 'fixed_r',dict(baseline,h=h,rho=.5/h)
    # Зміни топології очікувані також у точного еталона, а не лише при відмові методу.
    for shape,offsets in [('two_circles',[0,.06,.08,.10]),('neck',[-.12,-.10,-.08,0]),
                           ('circle',[-.57,-.55,-.53]),('torus',[-.21,-.19,.30,.34])]:
        for offset in offsets:
            yield 'critical_offset',dict(baseline,shape=shape,offset=offset,h=.25,
                                         resolution=35 if shape=='torus' else 151,angle=0.,shift=0.)


def run_sweep():
    rows=[]
    for factor,config in configurations():
        try:
            stats,*_=run(**config);stats.update(factor=factor,status='ok');rows.append(stats)
        except (RuntimeError,ValueError) as error:
            rows.append(dict(config,factor=factor,status='failed',error=str(error)))
    return rows


def figure(rows):
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(2,3,figsize=(12,7),layout='constrained')
    for ax,factor in zip(axes.flat,['h','rho','order','jitter','angle','fixed_r']):
        data=[r for r in rows if r['factor']==factor and r['status']=='ok']
        key='h' if factor=='fixed_r' else factor
        data=sorted(data,key=lambda r:r[key])
        ax.plot([r[key] for r in data],[r['band_rmse'] for r in data],'o-')
        ax.set(xlabel=key,ylabel='Band RMSE',title=factor);ax.grid(alpha=.3)
    return fig
