"""Математичні інваріанти та незалежні геометричні перевірки."""
import numpy as np
import pytest
import sympy as s
from core import kernel,lattice,matrix,fit,sdf,metrics,sampling,Geometry,select_isoline_nodes
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
    stats,*_=run1(h=.3,rho=1.5,order=2,strategy='grid')
    assert stats['node_residual']<1e-10
    assert stats['constant_max']>1e-3
    assert stats['uncovered_fraction']==0
    assert stats['rank']==stats['nodes']


def test_uncovered_counterexample_and_duplicate_rank():
    c=np.arange(-1,1.01,.2)[:,None]
    m=fit(c,lambda p:p[:,0],.08,2,h=.2,strategy='grid')
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
    assert stats['status']=='ok'
    assert stats['node_residual']<1e-8
    assert np.isfinite(stats['rmse'])


def test_factor_isolation_and_fixed_radius():
    baseline=dict(h=.25,rho=2.,order=2,angle=20.,shift=.03,offset=0.)
    pairs=list(configurations())
    for i in range(0,len(pairs),2):
        factor,a=pairs[i];_,b=pairs[i+1]
        assert {k:v for k,v in a.items() if k!='strategy'}=={k:v for k,v in b.items() if k!='strategy'}
        if factor=='fixed_r':assert np.isclose(a['h']*a['rho'],.5)
        elif factor!='critical_offset':
            assert all(a[k]==v for k,v in baseline.items() if k!=factor)
        assert 0<a['level_step']<=a['h']


def test_displaced_collocation_rank_and_interpolation():
    c=lattice(.4,margin=.8)
    model=fit(c,lambda p:np.ones(len(p)),.8,2,jitter=.25,h=.4,strategy='random')
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
    for r in rows:
        assert r['status'] in ('ok','failed')
        if r['status']=='ok':
            assert np.isfinite(r['band_rmse']) and r['node_residual']<1e-6
        else:assert r['error']
    assert sum(r['status']=='ok' and r['strategy']=='isolines' for r in rows)>10


@pytest.mark.parametrize('shape',['circle','square','two_circles','neck'])
@pytest.mark.parametrize('level',[-.15,0.,.1,.35])
def test_nearest_level_projection_against_independent_contours(shape,level):
    # Еталон незалежний від проєктора: marching squares по точній SDF.
    from skimage.measure import find_contours
    from scipy.spatial import cKDTree
    g=Geometry(shape,angle=17,shift=.03)
    axis,p=sampling(resolution=501,extent=1.5)
    curves=find_contours(g(p).reshape(501,501),level)
    reference=np.concatenate(curves)*(axis[1]-axis[0])+axis[0]
    queries=np.random.default_rng(4).uniform(-1,1,(15,2))
    projected=g.project_level(queries,level)
    assert np.isfinite(projected).all()
    assert np.max(abs(g(projected)-level))<5e-8
    sampled=cKDTree(reference).query(queries)[0]
    distances=np.linalg.norm(projected-queries,axis=1)
    assert np.max(abs(sampled-distances))<.012


@pytest.mark.parametrize('shape',['sphere','torus'])
@pytest.mark.parametrize('level',[-.15,0.,.35])
def test_3d_level_projection(shape,level):
    g=Geometry(shape,shift=.02)
    queries=np.random.default_rng(2).uniform(-1,1,(25,3))
    projected=g.project_level(queries,level)
    assert np.isfinite(projected).all()
    assert np.max(abs(g(projected)-level))<1e-10
    # Незалежні густі параметричні поверхні для перевірки мінімальності.
    from scipy.spatial import cKDTree
    a,b=np.meshgrid(np.linspace(0,2*np.pi,401),np.linspace(0,2*np.pi,401))
    if shape=='sphere':
        radius=.55+level
        reference=radius*np.stack([np.sin(a)*np.cos(b),np.sin(a)*np.sin(b),np.cos(a)],-1).reshape(-1,3)
    else:
        radius=.2+level;u=.52+radius*np.cos(a)
        reference=np.stack([u*np.cos(b),u*np.sin(b),radius*np.sin(a)],-1).reshape(-1,3)
        reference=reference[(u>=0).ravel()]
    reference[:,0]+=.02
    sampled=cKDTree(reference).query(queries)[0]
    assert np.max(abs(sampled-np.linalg.norm(projected-queries,axis=1)))<.015


def test_nearest_isoline_is_not_rounding_sdf():
    # У проміжку дисків d(0)=.08. Найближчий рівень — 0, не round(.08/.1)*.1.
    c=np.array([[0.,0.]])
    g=Geometry('two_circles')
    nodes,info=select_isoline_nodes(c,g,radius=.4,h=.2,level_step=.1)
    assert np.allclose(g(nodes),0.,atol=1e-12)
    assert np.isclose(np.linalg.norm(nodes[0]),.08)
    assert info['unique_nodes']==1


@pytest.mark.parametrize('shape',['circle','square','two_circles','neck','sphere','torus'])
def test_article_nodes_invariants(shape):
    dim=3 if shape in ('sphere','torus') else 2
    g=Geometry(shape,angle=23,shift=.02)
    centers=lattice(.4,dim,margin=.4)
    original=centers.copy()
    nodes,info=select_isoline_nodes(centers,g,.8,.4,.2)
    assert np.array_equal(centers,original)
    assert len(nodes)==len(centers)
    assert info['max_displacement']<.8
    assert np.max(abs(g(nodes)/.2-np.round(g(nodes)/.2)))<1e-6


def test_empty_levels_and_invalid_step():
    assert np.isnan(Geometry('circle').project_level(np.array([[0.,0.]]),-.6)).all()
    with pytest.raises(ValueError,match='level_step'):
        select_isoline_nodes(np.array([[0.,0.]]),Geometry(),.5,.25,.3)


def test_determinism_and_no_hidden_perturbation():
    g=Geometry('square');c=lattice(.4,margin=.8)
    first=fit(c,g,.8,order=4,h=.4,strategy='isolines',level_step=.2)
    second=fit(c,g,.8,order=4,h=.4,strategy='isolines',level_step=.2)
    assert np.array_equal(first.nodes,second.nodes)
    assert np.allclose(first.evaluate(first.nodes),g(first.nodes),atol=1e-8)
    duplicated=np.vstack([c[0],c[0]])
    with pytest.raises(ValueError,match='Coincident'):
        fit(duplicated,g,.8,h=.4,strategy='isolines',level_step=.2)


def test_paper_cases_and_surface_metrics():
    from experiment2 import paper_cases
    rows=[r[0] for r in paper_cases()]
    assert len(rows)==12
    assert all(r['nodes']==169 for r in rows)
    assert all(r['strategy'] in ('grid','isolines') for r in rows)
    assert {r['level_step'] for r in rows}=={.25,.081384}
    assert all(r['status']=='ok' and r['sampled_offset_hausdorff']>=0 for r in rows)
