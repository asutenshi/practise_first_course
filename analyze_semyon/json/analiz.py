import pandas as pd

# Загрузка данных
df = pd.read_csv("irkutsk_commercial_properties.csv")

# Словарь для классификации типов по легенде
legend_types = {
    "гостиница": "Гостиница",
    "свободного назначения": "Свободного назначения",
    "здание": "Здание",
    "общепит": "Общепит",
    "офис": "Офис",
    "склад": "Склад",
    "торговая площадь": "Торговая площадь",
    "универсальное помещение": "Универсальное помещение",
}


# Функция для классификации типа помещения
def classify_title(title):
    title = str(title).lower()
    for key, val in legend_types.items():
        if key in title:
            return val
    # Если ничего не найдено — Другое
    return "Другое"


# Очищаем названия: оставляем только тип из легенды или "Другое"
df["Название здания"] = df["title"].apply(classify_title)

# Преобразуем площадь в число
df["Площадь (м²)"] = (
    df["Общая площадь"]
    .astype(str)
    .str.replace(" ", "")
    .str.replace("м²", "")
    .str.replace(",", ".")
    .str.extract(r"([\d.]+)")
    .astype(float)
)

# Цена за квадратный метр
df["Цена за квадратный метр"] = df.apply(
    lambda row: row["price"] / row["Площадь (м²)"]
    if row["Площадь (м²)"] and row["price"] > 0
    else None,
    axis=1,
)


# Формируем итоговый датафрейм с координатами
result = df[
    [
        "Название здания",
        "address",  # Полный адрес
        "price",  # Цена
        "Цена за квадратный метр",
        "Площадь (м²)",  # Площадь
        "Тип здания",  # Тип здания
        "lat",  # Широта
        "lon",  # Долгота
    ]
].rename(
    columns={"address": "Полный адрес", "price": "Цена", "Тип здания": "Тип здания"}
)

# Сохраняем в CSV
result.to_csv("irkutsk_commercial_properties_clean.csv", index=False, encoding="utf-8")
print("Файл irkutsk_commercial_properties_clean.csv создан.")
