import pandas as pd

# Загрузка отфильтрованного CSV файла
input_file = "tourism_properties.csv"
df = pd.read_csv(input_file)


# Функция для определения типа помещения из его названия
def extract_property_type(title):
    title = str(title).lower()

    # Словарь типов помещений (только для туризма)
    property_types = {
        "свободного назначения": "Свободного назначения",
        "здание": "Здание",
        "помещение": "Помещение",
        "офис": "Офис",
        "торговая площадь": "Торговая площадь",
        "торговые площади": "Торговая площадь",
        "склад": "Склад",
        "общепит": "Общепит",
        "универсальное": "Универсальное",
        "гостиница": "Гостиница",
        "ресторан": "Общепит",
        "павильон": "Павильон",
        "нежилое": "Нежилое",
    }

    for key, value in property_types.items():
        if key in title:
            return value

    return "Прочее"


# Анализируем типы помещений
df["property_type"] = df["title"].apply(extract_property_type)

# Получаем статистику
property_type_counts = df["property_type"].value_counts()

# Выводим результаты
print("Анализ отфильтрованного файла (для туризма):")
print(f"Общее количество помещений для туризма: {len(df)}")
print("\nРаспределение по типам:")
for property_type, count in property_type_counts.items():
    print(f"{property_type}: {count} ({count / len(df) * 100:.1f}%)")

# Дополнительно: анализ цен и площадей
if "price" in df.columns:
    print(f"\nСредняя цена: {df['price'].mean():.0f} ₽")
    print(f"Медианная цена: {df['price'].median():.0f} ₽")
