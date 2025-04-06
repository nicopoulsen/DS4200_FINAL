import altair as alt
import pandas as pd
import os

os.makedirs("../visualizations", exist_ok=True)

df = pd.read_csv("../data/car_price_dataset.csv").reset_index() 

alt.data_transformers.disable_max_rows()

brands = list(df.Brand.unique())
brands.insert(0, None)
labels = list(df.Brand.unique())
labels.insert(0, 'All')

brand_dropdown = alt.binding_select(
    options=brands,
    labels=labels,
    name='Brand: '
)
brand_select = alt.selection_point(fields=['Brand'], bind=brand_dropdown)

price_slider = alt.binding_range(min=2000, max=20000, step=1000, name='Max Price: ')
price_param = alt.param(bind=price_slider, name='MaxPrice')

chart = alt.Chart(df).mark_point().encode(
    x=alt.X('Year:Q', scale=alt.Scale(domain=[2000, 2024]), axis=alt.Axis(format='d')),
    y='Price:Q',
    color=alt.condition(brand_select, alt.Color('Brand:N'), alt.value('lightgrey')),
    tooltip=['index', 'Brand:N', 'Model:N', 'Year:Q', 'Price:Q']
).add_params(
    brand_select,
    price_param
).transform_filter(
    brand_select
).transform_filter(
    alt.datum.Price < price_param
)

chart = chart.configure_view(
    stroke=None
).interactive().properties(
    autosize='pad',
    title='Year vs Price Among Car Brands (Interactive)',
    width=700,
    height=400,
    bounds="flush",
    padding={"left": 60, "right": 120, "top": 30, "bottom": 40}  
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).configure_legend(
    orient='right',
    labelFontSize=12,
    titleFontSize=14,
    padding=10
)

chart.save("../visualizations/charts_altair.html")

df.to_json("../visualizations/car_data.json", orient="records")

print("✅ Altair interactive chart + car data JSON saved!")
