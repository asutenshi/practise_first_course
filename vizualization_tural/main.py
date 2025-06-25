import streamlit as st
from charts import (
    load_marker_data,
    load_grid_data,
    load_charts_data,
    create_marker_map_fig,
    create_grid_map_fig,
    create_district_pie_chart,
    create_top_streets_bar_chart,
    create_rent_dist_bar_chart,
    create_building_types_bar_chart,
    create_avg_price_bar_chart
)

st.set_page_config(layout="wide", page_title="Анализ недвижимости Иркутска")

@st.cache_data
def get_data():
    marker_df = load_marker_data('irkutsk_commercial_properties_clean.csv')
    grid_df = load_grid_data('h3_grid_for_plotly_streamlit.csv') 
    charts_df = load_charts_data('result.json')
    return marker_df, grid_df, charts_df

marker_df, grid_df, charts_df = get_data()

COLOR_MAP = {
    'Офис': '#EF553B', 'Склад': '#636EFA', 'Торговая площадь': '#00CC96',
    'Свободного назначения': '#AB63FA', 'Здание': '#FFA15A', 'Универсальное помещение': '#19D3F3',
    'Общепит': '#FF6692', 'Гостиница': '#B6E880', 'Парковка': '#FECB52', 'Другое': '#8C8C8C'
}
METRIC_CHOICES = {
    "Количество объектов": "count",
    "Количество достопримечательностей": "landmark_count",
    "Средняя цена": "avg_price",
    "Медианная цена": "median_price",
    "Максимальная цена": "max_price"
}

tab_maps, tab_charts = st.tabs(["Карты", "Графики"])

with tab_maps:
    col_map, col_settings = st.columns([3, 1])
    
    with col_settings:
        st.subheader("Настройки")
        map_choice = st.radio("Выберите тип карты:", ["Карта с маркерами", "Сетчатая карта"])
        st.markdown("---")

        if map_choice == "Карта с маркерами":
            st.markdown("**Легенда**")
            
            type_counts = marker_df['Название здания'].value_counts()

            for prop_type in sorted(marker_df['Название здания'].unique()):
                if prop_type in COLOR_MAP:
                    count = type_counts.get(prop_type, 0)
                    st.markdown(
                        f'<div style="display: flex; align-items: center; margin-bottom: 4px; font-size: 14px;">'
                        f'<span style="height: 15px; width: 15px; background-color: {COLOR_MAP.get(prop_type, "#8C8C8C")}; '
                        f'border-radius: 50%; display: inline-block; margin-right: 8px; border: 1px solid #555;"></span>'
                        f'<span>{prop_type} ({count})</span></div>',
                        unsafe_allow_html=True
                    )
        else:
            selected_metric_name = st.selectbox("Выберите показатель для цвета:", options=list(METRIC_CHOICES.keys()))
            selected_metric_col = METRIC_CHOICES[selected_metric_name]

    with col_map:
        if map_choice == "Карта с маркерами":
            fig_marker = create_marker_map_fig(marker_df, COLOR_MAP)
            st.plotly_chart(fig_marker, use_container_width=True)
        else:
            center_coords = {"lat": marker_df.lat.mean(), "lon": marker_df.lon.mean()}
            fig_grid = create_grid_map_fig(grid_df, selected_metric_col, center_coords)
            st.plotly_chart(fig_grid, use_container_width=True)

with tab_charts:
    st.subheader("Графики анализа данных")
    

    fig1 = create_district_pie_chart(charts_df)
    fig2 = create_top_streets_bar_chart(charts_df)
    fig3 = create_rent_dist_bar_chart(charts_df)
    fig4 = create_building_types_bar_chart(charts_df)
    fig5 = create_avg_price_bar_chart(charts_df)

    col1, col2 = st.columns(2)
    with col1:
        if fig1: st.plotly_chart(fig1, use_container_width=True)
        if fig2: st.plotly_chart(fig2, use_container_width=True)
    with col2:
        if fig3: st.plotly_chart(fig3, use_container_width=True)
        if fig4: st.plotly_chart(fig4, use_container_width=True)
        if fig5: st.plotly_chart(fig5, use_container_width=True)