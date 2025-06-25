import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных
df = pd.read_csv("../json/irkutsk_commercial_properties.csv")

# 1. Распределение по районам (круговая диаграмма)
plt.figure(figsize=(10, 8))
district_counts = df["district"].value_counts()
plt.pie(district_counts, labels=district_counts.index, autopct="%1.1f%%", startangle=90)
plt.title("Распределение объектов по районам Иркутска")
plt.axis("equal")
plt.savefig("district_distribution.png")
plt.show()

# 2. Топ-10 самых загруженных улиц (столбчатая)
plt.figure(figsize=(12, 6))
street_counts = df["address"].str.extract(r"ул\. ([^,]+)")[0].value_counts().head(10)
street_counts.plot(kind="bar", color="#ff7f0e")
plt.title("Топ-10 улиц по количеству объектов")
plt.xlabel("Улица")
plt.ylabel("Количество объектов")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("top_streets.png")
plt.show()


# 3. Распределение минимального срока аренды (столбчатая)
def extract_min_rent(term):
    if pd.isna(term):
        return 0
    if "мес" in term:
        return int(term.split()[0])
    if "год" in term:
        return int(term.split()[0]) * 12
    return 0


df["min_rent_months"] = df["Минимальный срок аренды"].apply(extract_min_rent)
rent_counts = df["min_rent_months"].value_counts().sort_index()

plt.figure(figsize=(10, 6))
rent_counts.plot(kind="bar", color="#2ca02c")
plt.title("Распределение минимального срока аренды")
plt.xlabel("Срок (месяцы)")
plt.ylabel("Количество объектов")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.savefig("rent_distribution.png")
plt.show()

# 4. Распределение по типам зданий (столбчатая)
plt.figure(figsize=(12, 6))
building_counts = df["Тип здания"].value_counts().head(10)
building_counts.plot(kind="bar", color="#1f77b4")
plt.title("Распределение по типам зданий")
plt.xlabel("Тип здания")
plt.ylabel("Количество объектов")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("building_types.png")
plt.show()

# 5. Средняя стоимость по районам (столбчатая)
plt.figure(figsize=(12, 6))
district_prices = df.groupby("district")["price"].mean().sort_values(ascending=False)
district_prices.plot(kind="bar", color="#d62728")
plt.title("Средняя стоимость аренды по районам")
plt.xlabel("Район")
plt.ylabel("Средняя цена (₽)")
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig("district_prices.png")
plt.show()
