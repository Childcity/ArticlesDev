"""Translate table headers into Ukrainian without changing numeric data.

Run after prepare.py whenever the English generated tables change.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
HEADERS = {
    'selection': ['Метод', r'$\rho$', r'$\Delta/h$', 'Кандидати', 'Добір (с)'],
    'errors': ['Метод', '$D$', 'RMSE у смузі', 'Діапазон медіан за seed', '$H$', 'RMSE градієнта'],
    'resources': ['Метод', '$h$', 'Дані (байт)', 'Побудова (с)', 'Запити (с)', '$H$'],
    'editing': ['Метод', 'Підгот. кешу (с)', 'Оновлення (с)', 'Перебудова (с)', 'RMSE кеш.', 'RMSE перебуд.'],
    'topology': ['Метод', 'Роздільність', r'Еталон $(b_0,b_1,b_2)$', r'Модель $(b_0,b_1,b_2)$'],
}

def main():
    target = HERE / 'tables' / 'uk'
    target.mkdir(exist_ok=True)
    for name, headers in HEADERS.items():
        source = (HERE / 'tables' / f'{name}.tex').read_text()
        lines = source.splitlines(keepends=True)
        if len(lines[1].split(' & ')) != len(headers):
            raise ValueError(f'Table column count changed: {name}')
        lines[1] = ' & '.join(headers) + r' \\ \midrule' + '\n'
        translated = ''.join(lines)
        # Only the header is replaced. Body and numeric formatting are preserved.
        if translated.splitlines()[2:] != source.splitlines()[2:]:
            raise ValueError(f'Table body changed: {name}')
        (target / f'{name}.tex').write_text(translated)

if __name__ == '__main__':
    main()
