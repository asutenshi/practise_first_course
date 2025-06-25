import pandas as pd

# Загрузка исходного CSV файла
input_file = 'output.csv'
df = pd.read_csv(input_file)

# Функция для определения, относится ли помещение к сфере туризма
def is_tourism_property(title):
    title = str(title).lower()
    
    # Типы помещений для туристической сферы (на основе изображения)
    tourism_types = [
        'свободного назначения', 'здание', 'помещение', 'офис', 
        'торговая площадь', 'прочее', 'склад', 'общепит',
        'универсальное', 'гостиница', 'ресторан', 'павильон', 'нежилое'
    ]
    
    # Типы помещений, которые НЕ относятся к туристической сфере
    non_tourism_types = [
        'автосервис', 'производство', 'йога', 'маникюр', 'педикюр', 
        'бьюти', 'массаж', 'косметология', 'автомойка', 'хореографический',
        'коворкинг'
    ]
    
    # Проверяем, есть ли в названии явное указание на НЕтуристический тип
    for non_type in non_tourism_types:
        if non_type in title:
            return False
    
    # Проверяем, есть ли в названии указание на туристический тип
    for tourism_type in tourism_types:
        if tourism_type in title:
            return True
    
    # По умолчанию считаем, что помещение не относится к туризму
    return False

# Фильтруем данные
filtered_df = df[df['title'].apply(is_tourism_property)]

# Сохраняем результат в новый CSV файл
output_file = 'tourism_properties.csv'
filtered_df.to_csv(output_file, index=False)

print(f"Исходное количество записей: {len(df)}")
print(f"Количество записей после фильтрации: {len(filtered_df)}")
print(f"Удалено записей: {len(df) - len(filtered_df)}")
print(f"Результат сохранен в файл: {output_file}")
