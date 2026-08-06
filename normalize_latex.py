import pandas as pd
import re


def has_latex_markup(text: str) -> bool:
    """Проверяет, есть ли в тексте LaTeX-разметка (хотя бы одна пара $...$)."""
    if not isinstance(text, str):
        return False
    return bool(re.search(r'\$[^$]*\$', text))


def wrap_math_fragments(text: str) -> str:
    """Оборачивает в $...$ фрагменты, которые выглядят как формулы."""
    if not isinstance(text, str):
        return text

    marker_pattern = r'\\vec|\\frac|\\sqrt|\\sin|\\cos|\\tan|\\cot|\\log|\\ln|\\int|\\sum|\\prod|\\left|\\right|\^|\_|\d+\s*/\s*\d+'

    result = []
    i = 0
    n = len(text)

    while i < n:
        match = re.search(marker_pattern, text[i:])
        if not match:
            result.append(text[i:])
            break

        pos = i + match.start()
        result.append(text[i:pos])

        j = pos
        math_char_pattern = r'[A-Za-z0-9\^_\{\}\[\]\(\)\+\-\*\/\=\\\.\,\s]'
        while j < n and re.match(math_char_pattern, text[j]):
            j += 1

        candidate = text[pos:j].strip()

        if re.search(marker_pattern, candidate):
            clean_candidate = re.sub(r'\s+', ' ', candidate)
            result.append('$' + clean_candidate + '$')
        else:
            result.append(candidate)

        i = j

    return ''.join(result)


def normalize_condition(text):
    if has_latex_markup(text):
        # Уже размечено — ничего не меняем
        return text
    else:
        # Нет разметки — оборачиваем формулы
        return wrap_math_fragments(text)


if __name__ == '__main__':
    # Укажите здесь имя вашего Excel-файла
    input_file = 'tasks.xlsx'
    output_file = 'tasks_normalized.xlsx'

    print(f'Читаем файл: {input_file}')
    df = pd.read_excel(input_file)

    if 'condition' not in df.columns:
        raise ValueError('В файле нет колонки "condition"')

    print('Обрабатываем колонку condition...')
    df['condition_latex'] = df['condition'].apply(normalize_condition)

    print(f'Сохраняем результат в: {output_file}')
    df.to_excel(output_file, index=False)
    print('Готово!')
