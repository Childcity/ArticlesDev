"""Запуск інтерактивного застосунку без браузера через Streamlit AppTest."""
from pathlib import Path
from streamlit.testing.v1 import AppTest


def test_three_interactive_pages():
    app=AppTest.from_file(str(Path(__file__).parents[1]/'app.py'),default_timeout=60).run()
    assert not app.exception
    for page in ['1. Ядро та стійкість','2. Геометрія та офсети','3. Параметри']:
        app.radio[0].set_value(page).run()
        next(b for b in app.button if b.label=='Обчислити').click().run()
        assert not app.exception
        assert len(app.json)==1
    # Окремо проходимо об'ємну гілку й генерацію 3D-ізоповерхні.
    app.radio[0].set_value('2. Геометрія та офсети').run()
    next(x for x in app.selectbox if x.label=='Форма').set_value('sphere')
    next(b for b in app.button if b.label=='Обчислити').click().run()
    assert not app.exception


def test_grid_control_and_article_examples():
    app=AppTest.from_file(str(Path(__file__).parents[1]/'app.py'),default_timeout=60).run()
    app.radio[0].set_value('2. Геометрія та офсети').run()
    next(x for x in app.selectbox if x.label=='Точки інтерполяції').set_value('grid')
    next(b for b in app.button if b.label=='Обчислити').click().run()
    assert not app.exception
    assert len(app.json)==1
    next(b for b in app.button if b.label=='Приклади за схемою рисунків 4–6 та 8').click().run()
    assert not app.exception
    assert len(app.dataframe)==1


def test_optimizer_and_coefficient_download():
    app=AppTest.from_file(str(Path(__file__).parents[1]/'app.py'),default_timeout=60).run()
    app.radio[0].set_value('3. Параметри').run()
    next(b for b in app.button if b.label=='Добрати крок ізоліній: приклад за схемою рисунка 8').click().run()
    assert not app.exception
    assert len(app.json)==1
    assert len(app.dataframe)==1
    assert len(app.get('download_button'))==1


def test_slider_change_calculates_without_button():
    import json

    app=AppTest.from_file(str(Path(__file__).parents[1]/'app.py'),default_timeout=60).run()
    assert len(app.json)==0
    next(s for s in app.slider if s.label=='Крок h').set_value(.28).run()
    assert not app.exception
    assert len(app.json)==1
    assert json.loads(app.json[0].value)['h']==.28
    next(s for s in app.slider if s.label=='ρ = r/h').set_value(1.8).run()
    assert not app.exception
    assert json.loads(app.json[0].value)['rho']==1.8
    next(s for s in app.select_slider if s.label=='Роздільність оцінки 2D / 3D').set_value(31).run()
    assert not app.exception
    assert len(app.json)==1
    # A later rerun must not reuse the slider's calculation request.
    app.run()
    assert not app.exception
    assert len(app.json)==0


def test_extended_results_pages_and_quality_recalculation():
    app=AppTest.from_file(str(Path(__file__).parents[1]/'app.py'),default_timeout=60).run()
    for page in ['4. Незалежна перевірка','5. Градієнти та топологія','6. Парето та ресурси']:
        app.radio[0].set_value(page).run()
        assert not app.exception
    app.radio[0].set_value('5. Градієнти та топологія').run()
    next(b for b in app.button if b.label=='Перевірити градієнти й топологію').click().run()
    assert not app.exception
    assert len(app.json)==1
