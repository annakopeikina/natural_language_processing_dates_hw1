import re
from datetime import datetime

# Шаблоны регулярных выражений для разных форматов дат
date_patterns = [
    r"(\d{1,2})/(\d{1,2})/(\d{2,4})",  # Форматы типа 12/05/89, 12/05/1999
    r"(\d{1,2})/(\d{2,4})",  # Форматы типа 12/1999, 12/05
    r"(\d{4})",  # Форматы типа 1999
    r"([a-zA-Z]+) (\d{1,2}) (\d{4})"  # Форматы типа сентябрь 12 1999
]

# Функция для преобразования даты в нужный формат
def normalize_date(date_str):
    # Проверим на формат MM/DD/YYYY или MM/DD/YY
    match = re.match(r"(\d{1,2})/(\d{1,2})/(\d{2,4})", date_str)
    if match:
        month, day, year = match.groups()
        year = int(year)
        # Если год двухзначный, считаем его за 21-й век
        if len(str(year)) == 2:
            year += 2000  # Для двухзначных годов предполагаем, что это 21-й век
        if 1900 <= year <= 2099:
            return f"{year}-{int(month):02d}-{int(day):02d}"
        else:
            return None  # Исключаем года, которые не входят в логичные диапазоны

    # Проверим на формат MM/YY
    match = re.match(r"(\d{1,2})/(\d{2,4})", date_str)
    if match:
        month, year = match.groups()
        year = int(year)
        # Для двухзначных годов снова добавляем 2000
        if len(str(year)) == 2:
            year += 2000
        if 1900 <= year <= 2099:
            return f"{year}-{int(month):02d}-01"
        else:
            return None  # Исключаем года, которые не входят в логичные диапазоны

    # Проверим на формат YYYY
    match = re.match(r"(\d{4})", date_str)
    if match:
        year = match.group(1)
        year = int(year)
        if 1900 <= year <= 2099:
            return f"{year}-01-01"
        else:
            return None  # Исключаем года, которые не входят в логичные диапазоны

    # Проверим на формат "месяц день год"
    match = re.match(r"([a-zA-Z]+) (\d{1,2}) (\d{4})", date_str)
    if match:
        month_str, day, year = match.groups()
        try:
            month = datetime.strptime(month_str, "%B").month
            return f"{year}-{int(month):02d}-{int(day):02d}"
        except ValueError:
            return None  # Исключаем неправильные месяцы

    return None

# Чтение файла и обработка строк
with open("hw1_NLP_dates.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

results = []
for line_number, line in enumerate(lines):
    # Поиск всех дат в строке
    dates = []
    for pattern in date_patterns:
        dates.extend(re.findall(pattern, line))
    
    # Преобразуем каждую найденную дату в нужный формат
    for date in dates:
        date_str = ''.join(date)  # Если дата была найдена через несколько групп
        formatted_date = normalize_date(date_str)
        if formatted_date:
            # Добавляем описание события, если оно есть рядом с датой
            event_description = line.strip().split(date_str)[-1] if date_str in line else "Описание события отсутствует"
            results.append(f"{line_number}\t{formatted_date}\t{event_description}")

# Запись результатов в файл
with open("assignment_akopeikina.txt", "w", encoding="utf-8") as out_file:
    for result in results:
        out_file.write(result + "\n")

print("Результаты записаны в файл.")
