# STEP 1: IMPORT LIBRARIES
# i imported pandas for data cleaning, numpy for math, and matplotlib for drawing charts
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # use this to save charts without opening windows
import matplotlib.pyplot as plt

# STEP 2: LOAD THE DATA
# i am now going to load the CSV file from my computer
print('loading dataset...')
file_path = r'C:\Users\Admin\Desktop\Retail_sales_Analysis\dataset.csv'
df = pd.read_csv(file_path, encoding='cp1252', low_memory=False, on_bad_lines='skip')

# STEP 3: CLEAN THE DATA
# i removed all $ signs and commas from numbers because they are text, not numbers
print('cleaning data...')
for col in ['Sales', 'Profit', 'Shipping Cost']:
    if col in df.columns and df[col].dtype == 'object':
        df[col] = (
            df[col].astype(str)
                 .str.replace('$', '', regex=False)
                 .str.replace(',', '', regex=False)
        )
        df[col] = pd.to_numeric(df[col], errors='coerce')

# i converted date to proper date format and extracted year and month from it
if 'Order Date' in df.columns:
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.month

# STEP 4: REMOVE BAD ROWS
# i removed rows with missing values because they break our analysis
print('making sure rows are clean...')
df = df.dropna(subset=['Sales', 'Profit', 'Order Date'])

# STEP 5: CREATE NEW COLUMNS FOR ANALYSIS
# i created profit margin column to understand which products are most profitable
print('creating new features...')
df['Profit Margin %'] = df['Profit'] / df['Sales'].replace(0, np.nan) * 100

# STEP 6: CALCULATE TOTAL NUMBERS
# i calculated total sales and profit for the entire business
print('calculating totals...')
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
print('Total Sales:', f'${total_sales:,.2f}')
print('Total Profit:', f'${total_profit:,.2f}')

# CHART 1: SALES VS PROFIT BY CATEGORY
# i used a side-by-side bar chart to compare sales and profit for each product category
# this helps us see which category makes the most money and which is most profitable
plt.style.use('seaborn-v0_8-darkgrid')

category_analysis = df.groupby('Category').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
plt.figure(figsize=(10, 6))
x = np.arange(len(category_analysis['Category']))
width = 0.35
plt.bar(x - width/2, category_analysis['Sales'], width, label='Sales', color='#1976d2', edgecolor='black')
plt.bar(x + width/2, category_analysis['Profit'], width, label='Profit', color='#ffb300', edgecolor='black')
plt.xticks(x, category_analysis['Category'])
plt.ylabel('Amount ($)')
plt.title(f'Sales vs Profit by Category\n(Total Sales: ${total_sales:,.0f})')
plt.legend(frameon=True, edgecolor='black')
plt.tight_layout()
plt.gcf().savefig('category_analysis.png')
plt.close()

# CHART 2: TOP 10 CITIES BY SALES
# i used a colorful bar chart to show which cities are selling the most products
# each bar has a different color to make it easy to read and attractive
city_analysis = df.groupby('City')['Sales'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(12, 6))
colors = plt.cm.viridis(np.linspace(0.25, 0.75, len(city_analysis)))
bars = plt.bar(city_analysis.index, city_analysis.values, color=colors, edgecolor='black')
plt.title('Top 10 Cities by Sales')
plt.xticks(rotation=45, ha='right')
for bar in bars:
    y = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, y + total_sales * 0.003, f'${y:,.0f}', ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.gcf().savefig('top_cities.png')
plt.close()

# CHART 3: TOP 5 COUNTRIES BY PROFIT
# i used a horizontal bar chart to show which countries make the most profit
# horizontal bars make it easier to read country names
country_analysis = df.groupby('Country')['Profit'].sum().sort_values(ascending=False).head(5)
plt.figure(figsize=(10, 6))
colors = plt.cm.PuRd(np.linspace(0.4, 0.9, len(country_analysis)))
plt.barh(country_analysis.index, country_analysis.values, color=colors, edgecolor='black')
plt.gca().invert_yaxis()
plt.xlabel('Total Profit ($)')
plt.title('Top 5 Countries by Profit')
plt.tight_layout()
plt.gcf().savefig('top_countries.png')
plt.close()


# CHART 4: INDIA SALES VS GLOBAL SALES GAUGE
# i created a donut chart to show what percentage of total sales comes from India
india_sales = df[df['Country'] == 'India']
india_total = india_sales['Sales'].sum()
print('India total sales:', f'${india_total:,.2f}')
india_share = (india_total / total_sales * 100) if total_sales else 0

plt.figure(figsize=(6, 6))
values = [india_total, max(total_sales - india_total, 0)]
colors = ['#1e88e5', '#cfd8dc']
plt.pie(values, labels=['India', 'Rest of World'], colors=colors, startangle=90,
        autopct=lambda pct: f'{pct:.1f}%' if pct > 0 else '', pctdistance=0.75,
        wedgeprops=dict(width=0.35, edgecolor='white'))
centre_circle = plt.Circle((0, 0), 0.55, fc='white')
plt.gca().add_artist(centre_circle)
plt.text(0, 0, f'India\n{india_share:.1f}%\nof Global Sales', ha='center', va='center', fontsize=13, fontweight='bold')
plt.title('India Sales vs Global Sales')
plt.tight_layout()
plt.gcf().savefig('india_vs_global_gauge.png')
plt.close()

# CHART 5: TOP INDIA STATES BY SALES
# i analyzed India sales broken down by state to see which states are most important
if not india_sales.empty:
    india_state_sales = india_sales.groupby('State')['Sales'].sum().sort_values(ascending=False)
    print('India sales by state:')
    for state, sales in india_state_sales.head(10).items():
        print('-', state, f'${sales:,.2f}')
    plt.figure(figsize=(10, 6))
    colors = plt.cm.Reds(np.linspace(0.4, 0.85, min(10, len(india_state_sales))))
    plt.bar(india_state_sales.head(10).index, india_state_sales.head(10).values, color=colors, edgecolor='black')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Total Sales ($)')
    plt.title('Top India States by Sales')
    plt.tight_layout()
    plt.gcf().savefig('india_state_sales.png')
    plt.close()

    # CHART 6: TOP INDIA CITIES BY SALES
    # i analyzed India sales broken down by city to see which cities sell the most
    india_city_sales = india_sales.groupby('City')['Sales'].sum().sort_values(ascending=False).head(10)
    print('Top 10 India cities by sales:')
    for city, sales in india_city_sales.items():
        print('-', city, f'${sales:,.2f}')
    plt.figure(figsize=(12, 6))
    colors = plt.cm.cividis(np.linspace(0.2, 0.8, len(india_city_sales)))
    bars = plt.bar(india_city_sales.index, india_city_sales.values, color=colors, edgecolor='black')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Total Sales ($)')
    plt.title('Top India Cities by Sales')
    for bar in bars:
        y = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, y + total_sales * 0.002, f'${y:,.0f}', ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plt.gcf().savefig('india_top_cities.png')
    plt.close()
else:
    print('No India rows found.')

# CHART 7: SALES BY REGION
# i used a line chart with filled area to show sales across all regions in the world
region_analysis = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
print('sales by region:')
for region, sales in region_analysis.items():
    print('-', region, f'${sales:,.2f}')
plt.figure(figsize=(12, 6))
plt.plot(region_analysis.index, region_analysis.values, marker='o', linestyle='-', color='#6a1b9a')
plt.fill_between(region_analysis.index, region_analysis.values, color='#ce93d8', alpha=0.3)
plt.xticks(rotation=45, ha='right')
plt.ylabel('Total Sales ($)')
plt.title('Sales by Region')
plt.tight_layout()
plt.gcf().savefig('sales_by_region.png')
plt.close()

# CHART 8: YEARLY SALES TREND
# i plotted sales data over months for the last 3 years to see the trend over time
sales_trend = df.groupby(['Year', 'Month'])['Sales'].sum().reset_index()
plt.figure(figsize=(12, 6))
years = sorted(df['Year'].dropna().unique())
colors = ['#1e88e5', '#43a047', '#f4511e']
for index, year in enumerate(years[-3:]):
    year_data = sales_trend[sales_trend['Year'] == year]
    plt.plot(year_data['Month'], year_data['Sales'], marker='o', label=str(int(year)), color=colors[index])
plt.title('Yearly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Sales')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.gcf().savefig('sales_trend.png')
plt.close()

# CHART 9: YEAR ON YEAR GROWTH
# i calculated the percentage change in sales from 2014 to 2015 to see if business is growing
sales_2014 = df[df['Year'] == 2014]['Sales'].sum()
sales_2015 = df[df['Year'] == 2015]['Sales'].sum()
if sales_2014 != 0:
    yoy_growth = (sales_2015 - sales_2014) / sales_2014 * 100
else:
    yoy_growth = 0

plt.figure(figsize=(8, 4))
bar_color = '#2e7d32' if yoy_growth >= 0 else '#c62828'
plt.barh(['YoY Growth'], [yoy_growth], color=bar_color)
plt.xlim(min(-100, yoy_growth - 10), max(100, yoy_growth + 10))
plt.xlabel('Growth (%)')
plt.title('2015 vs 2014 Sales Growth')
for i, v in enumerate([yoy_growth]):
    plt.text(v + (2 if v >= 0 else -2), i, f'{v:.1f}%', va='center', ha='left' if v >= 0 else 'right', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.gcf().savefig('yoy_growth.png')
plt.close()

print('charts saved: category_analysis.png, top_cities.png, top_countries.png, india_vs_global_gauge.png, india_state_sales.png, india_top_cities.png, sales_by_region.png, sales_trend.png, yoy_growth.png')
