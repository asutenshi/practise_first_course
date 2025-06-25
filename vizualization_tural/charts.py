import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import json

DISTRICT_COLOR_MAP = {
    'р-н Правобережный': '#2EC4B6',
    'р-н Октябрьский': '#FF6B6B',
    'р-н Ленинский': '#3D5A80',
    'р-н Свердловский': '#FFCA3A',
}


def get_prop_type(title):
    t = str(title).lower()
    if 'офис' in t: return 'Офис'
    if 'склад' in t or 'кладовая' in t: return 'Склад'
    if 'торговая' in t or 'торговое' in t: return 'Торговая площадь'
    if 'общепит' in t: return 'Общепит'
    if 'здание' in t: return 'Здание'
    if 'универсальное' in t: return 'Универсальное помещение'
    if 'свободного' in t: return 'Свободного назначения'
    if 'гостиница' in t: return 'Гостиница'
    if 'парковка' in t: return 'Парковка'
    if 'производство' in t: return 'Производство'
    if 'автосервис' in t: return 'Автосервис'
    return 'Другое'

def extract_min_rent_months(term):
    if pd.isna(term): return None
    try:
        term_lower = str(term).lower()
        parts = term_lower.split()
        if 'мес' in term_lower: return int(parts[0])
        if 'год' in term_lower: return int(parts[0]) * 12
    except (ValueError, IndexError): return None
    return None



def load_marker_data(filepath):
    df = pd.read_csv(filepath)
    df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
    df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
    df.dropna(subset=['lat', 'lon'], inplace=True)
    df['property_type'] = df['Название здания']
    return df

def load_grid_data(filepath):
    df = pd.read_csv(filepath)
    def parse_polygon(p_str):
        if pd.isna(p_str): return None
        try:
            coords = [list(map(float, p.split(',')))[::-1] for p in p_str.split(';')]
            coords.append(coords[0])
            return {"type": "Polygon", "coordinates": [coords]}
        except (ValueError, IndexError):
            return None
    df['geometry'] = df['polygon_str'].apply(parse_polygon)
    df.dropna(subset=['geometry'], inplace=True)
    return df

def load_charts_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    df = pd.DataFrame.from_dict(data, orient='index')
    
    if 'district' in df.columns:
        df['district'] = df['district'].astype(str)
        df = df[df['district'].str.startswith('р-н')]

    df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
    df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
    df.dropna(subset=['lat', 'lon'], inplace=True)
    df['property_type'] = df['title'].apply(get_prop_type)
    if 'Минимальный срок аренды' in df.columns:
        df['min_rent_months'] = df['Минимальный срок аренды'].apply(extract_min_rent_months)
    df['street'] = df['address'].str.extract(r'(?:ул\.|улица)\s([^,]+)')[0].str.strip()
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)
    return df


def create_marker_map_fig(df, color_map):
    fig = px.scatter_mapbox(
        df, lat="lat", lon="lon", color="Название здания",
        color_discrete_map=color_map, hover_name="Название здания",
        mapbox_style="carto-positron", zoom=11, height=650,
        center={"lat": df.lat.mean(), "lon": df.lon.mean()},
        custom_data=['Полный адрес', 'Цена', 'Цена за квадратный метр', 'Площадь (м²)', 'Тип здания']
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{hovertext}</b><br><br>"
            "<b>Адрес:</b> %{customdata[0]}<br>"
            "<b>Цена:</b> %{customdata[1]:,} ₽<br>"
            "<b>Цена за м²:</b> %{customdata[2]:.2f} ₽<br>"
            "<b>Площадь:</b> %{customdata[3]} м²<br>"
            "<b>Тип здания:</b> %{customdata[4]}"
            "<extra></extra>"
        )
    )
    fig.update_layout(showlegend=False, margin={"r":0,"t":0,"l":0,"b":0})
    return fig

def create_grid_map_fig(df, metric_col, center_coords):
    geojson = {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": r.geometry, "id": r.h3_index} for _, r in df.iterrows()]}
    fig = go.Figure(go.Choroplethmapbox(
        geojson=geojson, locations=df['h3_index'], z=np.log1p(df[metric_col]),
        colorscale="RdYlGn_r",
        marker_opacity=0.7, marker_line_width=0,
        customdata=np.stack((df['count'], df['avg_price'].round(0), df['median_price'].round(0), df['min_price'], df['max_price'], df['landmark_count']), axis=-1),
        hovertemplate="<b>Шестиугольник H3</b><br><br>Кол-во объектов: %{customdata[0]}<br><b>Кол-во достопримечательностей: %{customdata[5]}</b><br>Средняя цена: %{customdata[1]:,} ₽<br>Медианная цена: %{customdata[2]:,} ₽<br>Мин. цена: %{customdata[3]:,} ₽<br>Макс. цена: %{customdata[4]:,} ₽<extra></extra>",
        colorbar=dict(title="")
    ))
    fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=10, mapbox_center=center_coords, margin={"r":0,"t":0,"l":0,"b":0}, height=650)
    return fig


def create_district_pie_chart(df):
    if 'district' not in df.columns or df['district'].empty: return None
    
    district_counts = df['district'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=district_counts.index,
        values=district_counts.values,
        marker=dict(colors=[DISTRICT_COLOR_MAP.get(d, '#888888') for d in district_counts.index]),
        hoverinfo='label+percent',
        textinfo='percent+label',
        textfont_size=12,
        sort=False,
        direction='clockwise',
        rotation=90
    )])
    fig.update_layout(
        title_text='Распределение объектов по районам',
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

def create_top_streets_bar_chart(df):
    if 'street' not in df.columns or 'district' not in df.columns or df['street'].isnull().all():
        return None

    top_10_streets_list = df['street'].value_counts().nlargest(10).index.tolist()
    df_top10 = df[df['street'].isin(top_10_streets_list)].copy()
    street_district_counts = df_top10.groupby(['street', 'district']).size().reset_index(name='count')
    total_counts = df_top10['street'].value_counts().reset_index()
    total_counts.columns = ['street', 'total_count']
    final_df = pd.merge(street_district_counts, total_counts, on='street')
    
    fig = px.bar(
        final_df, x='street', y='count', color='district',
        color_discrete_map=DISTRICT_COLOR_MAP,
        title='Топ-10 улиц по количеству объектов',
        labels={'street': 'Улица', 'count': 'Количество объектов', 'district': 'Район'},
        text_auto=True,
        category_orders={'street': final_df.sort_values('total_count', ascending=False)['street'].unique().tolist()}
    )
    fig.for_each_trace(lambda t: t.update(name=t.name.split("=")[-1]))
    fig.update_layout(xaxis_title="", yaxis_title="Кол-во объектов", legend_title_text='Район')
    return fig

def create_rent_dist_bar_chart(df):
    if 'min_rent_months' not in df.columns or df['min_rent_months'].isnull().all(): 
        return None

    df_filtered = df[(df['min_rent_months'] > 0) & (df['min_rent_months'] <= 12)]
    if df_filtered.empty: return None

    rent_counts = df_filtered['min_rent_months'].value_counts().sort_index().reset_index()
    rent_counts.columns = ['min_rent_months', 'count']
    rent_counts['min_rent_months_str'] = rent_counts['min_rent_months'].astype(int).astype(str) + ' мес.'

    fig = px.bar(
        rent_counts, x='count', y='min_rent_months_str', orientation='h',
        title='Распределение минимального срока аренды', text='count'
    )
    fig.update_layout(
        xaxis_title="Количество объектов", yaxis_title="Минимальный срок аренды",
        yaxis={'categoryorder':'total descending'}
    )
    fig.update_yaxes(showgrid=False)
    return fig

def create_building_types_bar_chart(df):
    if 'Тип здания' not in df.columns or df['Тип здания'].isnull().all(): return None
    building_counts = df['Тип здания'].value_counts().nlargest(10).reset_index()
    building_counts.columns = ['building_type', 'count']
    fig = px.bar(building_counts, x='building_type', y='count', title='Распределение по типам зданий', labels={'building_type': 'Тип здания', 'count': 'Количество объектов'}, text_auto=True)
    fig.update_layout(xaxis_title="", yaxis_title="Кол-во объектов")
    return fig

def create_avg_price_bar_chart(df):
    if 'district' not in df.columns or 'price' not in df.columns or df['district'].empty: return None
    q_low = df["price"].quantile(0.01)
    q_hi  = df["price"].quantile(0.99)
    df_filtered = df[(df["price"] < q_hi) & (df["price"] > q_low)]
    if df_filtered.empty: return None

    district_prices = df_filtered.groupby('district')['price'].mean().sort_values(ascending=False).reset_index()
    district_prices.columns = ['district', 'avg_price']
    
    fig = px.bar(
        district_prices, x='district', y='avg_price', color='district',
        color_discrete_map=DISTRICT_COLOR_MAP,
        title='Средняя стоимость аренды по районам (без выбросов)', 
        labels={'district': 'Район', 'avg_price': 'Средняя цена (₽)'}, 
        text_auto='.2s'
    )
    fig.update_layout(xaxis_title="", yaxis_title="Средняя цена (₽)", showlegend=False)
    return fig