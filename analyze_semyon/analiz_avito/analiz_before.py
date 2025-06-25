import pandas as pd

# Загрузка исходного CSV файла
input_file = 'output.csv'
df = pd.read_csv(input_file)

# Функция для определения типа помещения из его названия
def extract_property_type(title):
    title = str(title).lower()
    
    # Словарь типов помещений
    property_types = {
        'свободного назначения': 'Свободного назначения',
        'здание': 'Здание',
        'помещение': 'Помещение',
        'офис': 'Офис',
        'торговая площадь': 'Торговая площадь',
        'торговые площади': 'Торговая площадь',
        'склад': 'Склад',
        'общепит': 'Общепит',
        'универсальное': 'Универсальное',
        'гостиница': 'Гостиница',
        'ресторан': 'Ресторан',
        'павильон': 'Павильон',
        'автосервис': 'Автосервис',
        'производство': 'Производство',
        'йога': 'Йога',
        'маникюр': 'Маникюр',
        'бьюти': 'Бьюти',
        'массаж': 'Массаж',
        'косметология': 'Косметология',
        'коворкинг': 'Коворкинг',
        'нежилое': 'Нежилое'
    }
    
    for key, value in property_types.items():
        if key in title:
            return value
    
    return 'Прочее'

# Анализируем типы помещений
df['property_type'] = df['title'].apply(extract_property_type)

# Получаем статистику
property_type_counts = df['property_type'].value_counts()

# Выводим результаты
print("Анализ исходного файла:")
print(f"Общее количество помещений: {len(df)}")
print("\nРаспределение по типам:")
for property_type, count in property_type_counts.items():
    print(f"{property_type}: {count} ({count/len(df)*100:.1f}%)")
