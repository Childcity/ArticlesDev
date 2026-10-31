"""Добір кроку та незалежне оцінювання поля після передачі коефіцієнтів."""
from dataclasses import replace
import numpy as np
import pytest
from core import Geometry,lattice,fit
from storage import from_model,load
from experiment3 import optimize_level_step


@pytest.mark.parametrize('shape,dim',[('circle',2),('square',2),('sphere',3)])
def test_coefficient_archive_without_nodes_or_sdf(tmp_path,shape,dim):
    centers=lattice(.4,dim,margin=.4)
    model=fit(centers,Geometry(shape),.8,order=4,h=.4,level_step=.2)
    archive=tmp_path/'field.npz'
    from_model(model).save(archive)
    with np.load(archive) as saved:
        assert set(saved.files)=={'version','origin','spacing','coefficients','radius','order'}
        assert saved['coefficients'].size==len(centers)
        assert saved['coefficients'].nbytes==len(centers)*8
    restored=load(archive)
    points=np.random.default_rng(5).uniform(-1,1,(80,dim))
    assert not hasattr(restored,'nodes')
    assert np.allclose(restored.evaluate(points),model.evaluate(points),atol=1e-10)
    assert restored.evaluate(np.empty((0,dim))).shape==(0,)


def test_nonregular_storage_rejected():
    model=fit(lattice(.4,margin=.4),Geometry(),.8,order=4,h=.4,level_step=.2)
    wrong=model.centers.copy();wrong[0,0]+=.01
    with pytest.raises(ValueError,match='lattice'):
        from_model(replace(model,centers=wrong))


def test_optimized_step_selected_without_validation_leakage():
    a,trials,_=optimize_level_step(calibration_size=128,coarse_count=7,validation_resolution=61)
    b,other,_=optimize_level_step(calibration_size=128,coarse_count=7,validation_resolution=91)
    assert a['selected_step']==b['selected_step']
    assert a['calibration_rmse']==b['calibration_rmse']
    assert a['bounds'][0]<=a['selected_step']<=a['bounds'][1]
    # Лише збережені калібрувальні оцінки визначають вибір, не перевірочна сітка.
    assert a['calibration_rmse']==min(t['calibration_rmse'] for t in trials if t['status']=='ok')
    assert a['validation'][2]['status']=='ok'
    assert all(t['status'] in ('ok','failed') for t in trials)
    assert any(np.isclose(t['level_step'],.081384) for t in trials)
