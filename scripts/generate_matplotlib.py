import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

data_path = "../data/car_price_dataset.csv"
output_dir = "../visualizations"
img_dir = os.path.join(output_dir, "images")

# ensuring folders are present 
os.makedirs(output_dir, exist_ok=True)
os.makedirs(img_dir, exist_ok=True)

df = pd.read_csv(data_path)

# 1. Scatter + KDE 
plt.figure(figsize=(10,6))
plt.scatter(df['Mileage'], df['Price'], alpha=0.2)
sns.kdeplot(x=df['Mileage'], y=df['Price'], cmap="Reds", fill=True, alpha=0.5)
plt.xlabel('Mileage')
plt.ylabel('Price')
plt.title('Scatter Plot of Mileage vs Price with KDE')
plt.tight_layout()
plt.savefig(f"{img_dir}/plot1.png")
plt.close()

# Lineplot
plt.figure(figsize=(12,6))
sns.lineplot(data=df, x='Year', y='Price', hue='Brand')
plt.title('Brand Price Depreciation Over Time')
plt.xlabel('Year of Manufacture')
plt.ylabel('Average Price')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(f"{img_dir}/plot2.png")
plt.close()

# heatmap
plt.figure(figsize=(10, 8))
pred = df[['Price','Mileage','Doors','Year','Owner_Count','Engine_Size']]
corr = pred.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Heatmap Depicting Correlation Matrix for Car Features')
plt.tight_layout()
plt.savefig(f"{img_dir}/plot3.png")
plt.close()

html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Matplotlib Static Visualizations</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
            background-color: #fefefe;
        }}

        h2 {{
            margin-top: 40px;
            color: #333;
        }}

        img {{
            width: 100%;
            max-height: 450px;
            object-fit: contain;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
    </style>
</head>
<body>

    <h2>Scatter + KDE: Mileage vs Price</h2>
    <img src="images/plot1.png" alt="Scatter KDE">

    <h2>Lineplot: Brand Depreciation Over Time</h2>
    <img src="images/plot2.png" alt="Lineplot Brand">

    <h2>Heatmap: Feature Correlations</h2>
    <img src="images/plot3.png" alt="Correlation Heatmap">

</body>
</html>
"""

with open(f"{output_dir}/matplotlib_static.html", "w") as f:
    f.write(html)

print("✅ Static matplotlib visuals and HTML saved.")
