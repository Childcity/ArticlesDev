"""Незалежні математичні та протокольні перевірки пунктів 4–6."""
import numpy as np
import pytest
from geometry import Geometry
from core import lattice
from comparators import build,basis,basis_derivative,METHODS,CountedGeometry
from quality import topology,reference_gradient,gradient_quality,pareto_mask,measure
from experiment4 import tune,TRAIN,HOLDOUT


@pytest.mark.parametrize('family',['pg','wendland_c2','wendland_c4'])
def test_basis_derivative_and_compact_support(family):
    q=np.linspace(.01,.99,31);eps=1e-6
    expected=(basis(q+eps,family)-basis(q-eps,family))/(2*eps)
    assert np.allclose(basis_derivative(q,family),expected,atol=2e-8)
    assert np.array_equal(basis(np.array([1.,2.]),family),[0.,0.])
    assert basis(np.array([0.]),family)[0]==1


@pytest.mark.parametrize('family',['wendland_c2_grid','wendland_c4_grid'])
def test_wendland_positive_definite_and_interpolation(family):
    from comparators import collocation
    centers=lattice(.4,margin=.4)
    a=collocation(centers,centers,.8,family.rsplit('_',1)[0],4).toarray()
    assert np.min(np.linalg.eigvalsh(a))>0
    g=CountedGeometry('circle');model,stats=build(family,g,h=.4)
    assert np.allclose(model.evaluate(model.centers),g(model.centers),atol=1e-10)
    assert stats['node_residual']<1e-10


@pytest.mark.parametrize('method',['pg_grid','pg_isolines','wendland_c2_grid','wendland_c4_isolines'])
def test_analytic_model_gradient_independent_differences(method):
    model,_=build(method,CountedGeometry('circle'),h=.3,rho=2,order=4)
    p=np.random.default_rng(6).uniform(-.8,.8,(25,2));eps=1e-6
    expected=np.column_stack([(model.evaluate(p+np.eye(2)[j]*eps)-model.evaluate(p-np.eye(2)[j]*eps))/(2*eps) for j in range(2)])
    assert np.allclose(model.gradient(p),expected,atol=1e-6)


@pytest.mark.parametrize('method',['linear','cubic'])
def test_grid_affine_reproduction(method):
    class Affine(Geometry):
        def __call__(self,p):return 1+.3*p[:,0]-.2*p[:,1]
    model,_=build(method,Affine(),h=.3)
    p=np.random.default_rng(2).uniform(-1,1,(32,2))
    assert np.allclose(model.evaluate(p),Affine()(p),atol=1e-10)
    assert np.allclose(model.gradient(p),[.3,-.2],atol=1e-8)


@pytest.mark.parametrize('shape,points,expected',[
    ('capsule',[[0,0],[.6,0],[0,.22]],[-.22,0.,0.]),
    ('rounded_box',[[0,0],[.47,0],[.35,.47]],[-.47,0.,0.])])
def test_new_heldout_sdf_and_nearest_projection(shape,points,expected):
    g=Geometry(shape)
    assert np.allclose(g(np.array(points)),expected,atol=1e-12)
    p=np.random.default_rng(11).uniform(-1,1,(40,2))
    for t in [-.1,0.,.1]:
        projected=g.project_level(p,t)
        assert np.max(abs(g(projected)-t))<1e-10
        assert np.allclose(np.linalg.norm(projected-p,axis=1),abs(g(p)-t),atol=1e-10)


def test_reference_gradient_and_medial_exclusion():
    g=Geometry('circle')
    p=np.array([[.4,.3],[.6,.2],[0.,0.]])
    gradient,mask=reference_gradient(g,p)
    assert np.allclose(gradient[:2],p[:2]/np.linalg.norm(p[:2],axis=1)[:,None],atol=1e-8)
    assert mask.tolist()==[True,True,False]


@pytest.mark.parametrize('shape,expected',[('sphere',(1,0,0)),('torus',(1,1,0))])
def test_3d_betti(shape,expected):
    axis=np.linspace(-1,1,65)
    p=np.stack(np.meshgrid(axis,axis,axis,indexing='ij'),-1).reshape(-1,3)
    result=topology((Geometry(shape)(p)<=0).reshape(65,65,65))
    assert tuple(result[k] for k in ('b0','b1','b2'))==expected
    assert not result['touches_boundary']


def test_cavity_and_2d_hole_topology():
    axis=np.linspace(-1,1,41)
    p=np.stack(np.meshgrid(axis,axis,axis,indexing='ij'),-1)
    radius=np.linalg.norm(p,axis=-1)
    shell=(radius<.7)&(radius>.3)
    t=topology(shell)
    assert (t['b0'],t['b1'],t['b2'])==(1,0,1)
    x,y=np.meshgrid(axis,axis,indexing='ij');r=np.hypot(x,y)
    t=topology((r<.7)&(r>.3))
    assert (t['b0'],t['b1'])==(1,1)


def test_exact_field_metrics_resolution():
    class Exact:
        def evaluate(self,p):return Geometry('circle')(p)
    for resolution in [41,81]:
        rows=measure(Exact(),Geometry('circle'),resolution)
        assert all(r['band_rmse']==0 and r['sampled_offset_hausdorff']==0 for r in rows)
        assert all(r['topology_match'] for r in rows)


def test_pareto_duplicates_and_dominance():
    rows=[dict(e=1,m=2,t=3),dict(e=1,m=2,t=3),dict(e=2,m=3,t=4),dict(e=.5,m=8,t=1)]
    assert pareto_mask(rows,['e','m','t']).tolist()==[True,True,False,True]


def test_train_holdout_disjoint_and_seeded_selection():
    assert not ({r['shape'] for r in TRAIN}&set(HOLDOUT))
    a,rows=tune(methods=['pg_grid','linear'],seeds=(0,),budget=2)
    b,_=tune(methods=['pg_grid','linear'],seeds=(0,),budget=2)
    assert a['pg_grid']['config']==b['pg_grid']['config']
    assert all(r['sdf_points']>0 for r in rows)
    assert all(r['projection_points']==0 for r in rows)


def test_additional_redistance_storage_accounted():
    direct,a=build('cubic',CountedGeometry('circle'),h=.3)
    redistance,b=build('cubic_redistance',CountedGeometry('circle'),h=.3)
    assert b['stored_bytes']>a['stored_bytes']


@pytest.mark.parametrize('method',['linear','cubic','cubic_redistance','pg_grid','wendland_c2_grid'])
def test_cached_edit_matches_full_rebuild_for_fixed_grid(method):
    from editing import prepare
    initial=Geometry('capsule',angle=37.)
    target=Geometry('capsule',angle=37.,shift=.02)
    config=dict(rho=2.,order=4,delta_ratio=.5)
    update,info=prepare(method,initial,.3,config)
    cached=update(target);fresh,_=build(method,target,h=.3,**config)
    points=np.random.default_rng(99).uniform(-1,1,(60,2))
    assert np.allclose(cached.evaluate(points),fresh.evaluate(points),atol=1e-9)
    assert info['retained_factor_bytes']>=0


def test_isolated_worker_reports_native_memory_and_editing():
    import json,os,subprocess,sys
    from pathlib import Path
    config=dict(method='linear',dim=2,h=.3,config=dict(rho=2.,order=4,delta_ratio=.5))
    env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
    r=subprocess.run([sys.executable,str(Path(__file__).parents[1]/'resource_worker.py'),json.dumps(config)],
                     env=env,capture_output=True,text=True,check=True)
    row=json.loads(r.stdout)
    assert row['status']=='ok'
    assert row['peak_rss_bytes']>=row['import_peak_rss_bytes']>0
    assert len(row['build_samples'])==3
    assert len(row['cached_update_samples'])==3
    assert len(row['full_rebuild_samples'])==3
    assert row['total_edit_seconds']['10']>row['cached_update_seconds']


def test_pg_default_matches_quartic_smoothness_kernel():
    from comparators import PG_ORDER
    assert PG_ORDER==4
    q=np.array([0.,.2,.5,.9,1.])
    assert np.allclose(basis(q,'pg'),np.maximum(1-q*q,0)**5)
    assert np.allclose(basis_derivative(q,'pg'),-10*q*np.maximum(1-q*q,0)**4)
    field,stats=build('pg_grid',CountedGeometry('circle'),h=.3)
    assert field.order==stats['order']==PG_ORDER


def test_fixed_smoothness_tuning_budget_has_distinct_candidates():
    from comparators import candidates,PG_ORDER
    for method in METHODS:
        configs=candidates(method)
        assert len(configs)==(1 if method in ('linear','cubic','cubic_redistance') else 6)
        assert all(c['order']==PG_ORDER for c in configs)
        assert len({tuple(sorted(c.items())) for c in configs})==len(configs)
    assert candidates('pg_grid')==candidates('wendland_c2_grid')==candidates('wendland_c4_grid')
    assert candidates('pg_isolines')==candidates('wendland_c2_isolines')==candidates('wendland_c4_isolines')


def test_failure_design_covers_fixed_smoothness_cartesian_product():
    from experiment6 import failure_configurations
    configs=list(failure_configurations())
    assert len(configs)==40
    assert {c['order'] for c in configs}=={4}
    assert {c['h'] for c in configs}=={.2,.3}
    assert {c['rho'] for c in configs}=={.5,1.,1.5,2.,3.}
    assert len({tuple(sorted(c.items())) for c in configs})==40


def test_report_guard_requires_consistent_pg_smoothness():
    from comparators import PG_ORDER
    from extended_reports import validate_pg_order
    protocol=dict(pg_order=PG_ORDER)
    selection=dict(pg_grid=dict(config=dict(order=PG_ORDER)))
    tables=dict(training=[dict(method='pg_grid',order=PG_ORDER)],
                resources=[dict(method='pg_grid',config=dict(order=PG_ORDER))])
    validate_pg_order(protocol,selection,tables)
    tables['resources'][0]['config']['order']=PG_ORDER+1
    with pytest.raises(ValueError,match='order'):
        validate_pg_order(protocol,selection,tables)


def test_published_extended_protocol_and_measurements_use_order_four():
    import json
    from pathlib import Path
    from comparators import PG_ORDER
    from extended_reports import validate_pg_order
    out=Path(__file__).parents[1]/'results'/'extended'
    protocol=json.loads((out/'protocol.json').read_text())
    selected=json.loads((out/'selection.json').read_text())
    tables={name:json.loads((out/(name+'.json')).read_text())
            for name in ('training','holdout','resolution','failure_map','resources')}
    assert protocol['pg_order']==PG_ORDER==4
    assert protocol['version']=='extended-4-6-n4-v1'
    for configs in protocol['candidates'].values():
        assert all(config['order']==PG_ORDER for config in configs)
    validate_pg_order(protocol,selected,tables)
    assert len(tables['failure_map'])==len(protocol['failure_configurations'])==40
    assert {tuple(row[k] for k in ('h','rho','order','strategy','delta_ratio'))
            for row in tables['failure_map']}=={
                tuple(config[k] for k in ('h','rho','order','strategy','delta_ratio'))
                for config in protocol['failure_configurations']}
