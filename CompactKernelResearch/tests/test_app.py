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
