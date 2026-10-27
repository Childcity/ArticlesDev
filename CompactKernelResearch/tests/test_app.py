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
    app.selectbox[0].set_value('sphere')
    next(b for b in app.button if b.label=='Обчислити').click().run()
    assert not app.exception
