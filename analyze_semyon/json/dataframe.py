import pandas as pd
import json

# Загрузка JSON данных из файла
with open("result.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Преобразование JSON в DataFrame
df_list = []

for url, property_info in data.items():
    # Создаем строку данных
    row = property_info.copy()
    row["url"] = url  # Добавляем URL как отдельную колонку
    df_list.append(row)

# Создание DataFrame
df = pd.DataFrame(df_list)

# Очистка данных - удаление лишних пробелов
for col in df.columns:
    if df[col].dtype == "object":
        df[col] = df[col].astype(str).str.strip()

# Преобразование цены в числовой формат
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# Преобразование координат в числовой формат
df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
df["lon"] = pd.to_numeric(df["lon"], errors="coerce")

# Информация о DataFrame
print("Структура данных:")
print(f"Количество записей: {len(df)}")
print(f"Количество столбцов: {len(df.columns)}")
print("\nПервые 5 записей:")
print(df.head())

# Сохранение в CSV
df.to_csv("irkutsk_commercial_properties.csv", index=False, encoding="utf-8")
print("\nДанные сохранены в файл: irkutsk_commercial_properties.csv")
