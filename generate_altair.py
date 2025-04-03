import altair as alt
import pandas as pd

# Load your data
prediction = pd.read_csv("data/car_price_dataset.csv")

# Dropdown options
options = list(prediction.Brand.unique())
four_door = prediction.query('`Doors` == 4')
options.insert(0, None)
labels = list(prediction.Brand.unique())
labels.insert(0, 'All')
input_dropdown = alt.binding_select(
    options=options,
    labels=labels,
    name='Make:'
)

# Set up interactivity
selection = alt.selection_point(fields=['Brand'], bind=input_dropdown)
alt.data_transformers.disable_max_rows()

# Chart 1: Mileage vs Price
miles = alt.Chart(prediction).mark_point().encode(
    x='Mileage:Q',
    y='Price:Q',
    color=alt.condition(selection, alt.Color('Brand:N'), alt.value('lightgrey'))
).add_params(
    selection
).transform_filter(
    selection
).properties(
    title='Mileage vs Price Among Different Car Brands'
)

# Chart 2: Year vs Price
year_price = miles.encode(
    x=alt.X('Year:Q', scale=alt.Scale(domain=[2000, 2024]))
).properties(
    title='Year vs Price Among Different Car Brands'
)

# Chart 3: Price Distribution
prices = alt.Chart(prediction).mark_bar().encode(
    alt.X('Price:Q', bin=alt.Bin(extent=[2000, 20000], step=2000)),
    y='count()',
    color=alt.condition(selection, alt.Color('Brand:N'), alt.value('lightgrey'))
).add_params(
    selection
).transform_filter(
    selection
).properties(
    title='Distribution of Car Price Among Different Brands'
)

# Chart 4: Cars for Sale by Brand
top_brands = alt.Chart(prediction).mark_bar().encode(
    alt.X('Brand:N').sort('-y'),
    y='count()',
    color=alt.condition(selection, alt.Color('Brand:N'), alt.value('lightgrey'))
).properties(
    title='Number of Cars For Sale by Brand'
)

# Combine all charts
top_row = miles | year_price
bottom_row = top_brands | prices
final_chart = top_row & bottom_row

# Export to HTML
final_chart.save("charts_altair.html")