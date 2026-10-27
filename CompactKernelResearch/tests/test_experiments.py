"""Математичні інваріанти та незалежні геометричні перевірки."""
import numpy as np
import pytest
import sympy as s
from core import kernel,lattice,matrix,fit,sdf,metrics,sampling
from experiment1 import run as run1
from experiment2 import run as run2
from experiment3 import configurations


@pytest.mark.parametrize('n',[1,2,3,4])
def test_exact_boundary_smoothness(n):
    x=s.symbols('x');p=(1-x*x)**(n+1)
    assert p.subs(x,0)==1
    for k in range(n+1):
        assert s.diff(p,x,k).subs(x,1)==0
    assert s.diff(p,x,n+1).subs(x,1)!=0
    assert kernel(np.array([0,1,2]),1,n).tolist()==[1,0,0]


def test_source_polynomials():
    # Коефіцієнти незалежно транскрибовані з рівнянь (2)-(5) DOCX.
    from math import comb
    expected=[[1,-2,1],[1,-3,3,-1],[1,-4,6,-4,1],[1,-5,10,-10,5,-1]]
    for n,c in enumerate(expected,1):
        assert [(-1)**j*comb(n+1,j) for j in range(n+2)]==c


def test_nodes_interpolated_but_constant_not_reproduced():
    stats,*_=run1(h=.3,rho=1.5,order=2)
    assert stats['node_residual']<1e-10
    assert stats['constant_max']>1e-3
    assert stats['uncovered_fraction']==0
    assert stats['rank']==stats['nodes']


def test_uncovered_counterexample_and_duplicate_rank():
    c=np.arange(-1,1.01,.2)[:,None]
    m=fit(c,lambda p:p[:,0],.08,2,h=.2)
    assert m.evaluate(np.array([[.5]]))[0]==0
    a=matrix(c,c,.4,2).toarray()
    a[1]=a[0]
    assert np.linalg.matrix_rank(a)<len(c)


@pytest.mark.parametrize('shape,points,expected',[
 ('circle',[[0,0],[.55,0],[1,0]],[-.55,0,.45]),
 ('square',[[0,0],[.48,.48],[.78,.88]],[-.48,0,.5]),
 ('two_circles',[[-.4,0],[0,0],[.72,0]],[-.32,.08,0]),
 ('neck',[[0,0],[0,.1],[0,.2],[.8,0]],[-.1,0,.1,-.05]),
 ('sphere',[[0,0,0],[0,0,.55]],[-.55,0]),
 ('torus',[[.52,0,0],[0,0,0],[.52,0,.2]],[-.2,.32,0]),
])
def test_analytic_sdf(shape,points,expected):
    assert np.allclose(sdf(np.array(points),shape),expected,atol=1e-12)


def test_rotation_translation_invariance():
    p=np.array([[.8,.3],[-.1,.6]])
    theta=np.pi/6
    rotation=np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]])
    moved=p@rotation.T+np.array([.1,0])
    assert np.allclose(sdf(p,'square'),sdf(moved,'square',30,.1))


def test_critical_topology_reference():
    _,p=sampling(resolution=201)
    d=sdf(p,'two_circles')
    assert metrics(d,d,201,offset=.06)['components_exact']==2
    assert metrics(d,d,201,offset=.10)['components_exact']==1
    d=sdf(p,'neck')
    assert metrics(d,d,201,offset=-.12)['components_exact']==2
    assert metrics(d,d,201,offset=-.08)['components_exact']==1


def test_offset_counterexample():
    # f=2d: координата нуля f-t відповідає істинній відстані t/2.
    t=.2;x=.55+t/2
    assert np.isclose(2*sdf(np.array([[x,0]]),'circle')[0],t)
    assert np.isclose(abs((x-.55)-t),.1)


@pytest.mark.parametrize('shape',['circle','sphere','torus'])
def test_experiment2_actual_solver(shape):
    stats,*_=run2(shape=shape,h=.4,resolution=17)
    assert stats['node_residual']<1e-8
    assert np.isfinite(stats['rmse'])


def test_factor_isolation_and_fixed_radius():
    baseline=dict(h=.25,rho=2.,order=2,jitter=0.,angle=20.,shift=.03,offset=0.)
    for factor,config in configurations():
        if factor=='fixed_r':assert np.isclose(config['h']*config['rho'],.5)
        elif factor!='critical_offset':
            assert all(config[k]==v for k,v in baseline.items() if k!=factor)


def test_displaced_collocation_rank_and_interpolation():
    c=lattice(.4,margin=.8)
    model=fit(c,lambda p:np.ones(len(p)),.8,2,jitter=.25,h=.4)
    a=matrix(model.nodes,c,.8,2).toarray()
    assert np.linalg.matrix_rank(a)==len(c)
    assert not np.allclose(a,a.T)
    assert model.residual<1e-9
    nodes=model.nodes.copy();nodes[1]=nodes[0]
    assert np.linalg.matrix_rank(matrix(nodes,c,.8,2).toarray())<len(c)


def test_experiment3_measured_sweep():
    from experiment3 import run_sweep
    rows=run_sweep()
    assert len(rows)==len(list(configurations()))
    assert all(r['status']=='ok' for r in rows)
    assert all(np.isfinite(r['band_rmse']) and r['node_residual']<1e-7 for r in rows)
    # Перевіряємо суттєвий результат на контрольній формі, а не точний час виконання.
    rhos={r['rho']:r for r in rows if r['factor']=='rho'}
    assert rhos[3.]['band_rmse']>rhos[1.5]['band_rmse']
