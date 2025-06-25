import pandas as pd
import h3

# === 1. Загрузка данных о помещениях ===
df = pd.read_csv("project/analiz_avito/tourism_properties.csv")

# === 2. Преобразование координат помещений в H3-индексы ===
resolution = 9
def get_h3_index(lat, lng, resolution=9):
    return h3.latlng_to_cell(lat, lng, resolution)

df["h3_index"] = [
    get_h3_index(lat, lng, resolution) for lat, lng in zip(df["lat"], df["lng"])
]

# === 3. Агрегирование статистик по H3-ячейкам для помещений ===
h3_stats = (
    df.groupby("h3_index")
    .agg(
        count=("price", "count"),
        avg_price=("price", "mean"),
        median_price=("price", "median"),
        min_price=("price", "min"),
        max_price=("price", "max"),
    )
    .reset_index()
)

# === 4. Получение полигональных координат шестиугольников ===
def h3_to_polygon(h3_idx):
    boundary = h3.cell_to_boundary(h3_idx)
    return [(lat, lng) for lat, lng in boundary]

h3_stats["polygon"] = h3_stats["h3_index"].apply(h3_to_polygon)
h3_stats["polygon_str"] = h3_stats["polygon"].apply(
    lambda coords: ";".join([f"{lat},{lng}" for lat, lng in coords])
)

# === 5. Загрузка и обработка достопримечательностей ===
df_landmarks = pd.read_csv("project/attractions/landmarks.csv")

# Фильтрация ненужных типов
types = [
    "питание",
    "услуги", 
    "спорт",
    "размещение",
    "индустриальные объекты",
    "транспорт",
]
df_landmarks = df_landmarks[~df_landmarks["agr_type"].isin(types)]

# Генерация H3-индексов для достопримечательностей
df_landmarks["h3_index"] = [
    get_h3_index(lat, lon, resolution)
    for lat, lon in zip(df_landmarks["lat"], df_landmarks["lon"])
]

# Подсчет количества достопримечательностей в каждом шестиугольнике
landmark_counts = df_landmarks["h3_index"].value_counts().rename("landmark_count")

# === 6. Объединение данных по H3-ячейкам ===
h3_stats = h3_stats.merge(
    landmark_counts, left_on="h3_index", right_index=True, how="left"
)
h3_stats["landmark_count"] = h3_stats["landmark_count"].fillna(0).astype(int)

# === 7. Экспорт итогового файла ===
export_path = "h3_grid_for_plotly_streamlit.csv"
h3_stats_export = h3_stats[
    [
        "h3_index",
        "count",
        "avg_price",
        "median_price",
        "min_price",
        "max_price",
        "polygon_str",
        "landmark_count",
    ]
]
h3_stats_export.to_csv(export_path, index=False)

print(f"H3 сетка экспортирована в файл: {export_path}")
print(f"Всего шестиугольников: {len(h3_stats_export)}")
print("\nПервые 5 записей:")
print(h3_stats_export.head())
