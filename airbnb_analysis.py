import pandas as pd
import numpy as np
import os

# just setting up the folder paths where i saved my data
data_dir = 'Airbnb Data'
listings_path = os.path.join(data_dir, 'Listings.csv')
reviews_path = os.path.join(data_dir, 'Reviews.csv')

print("Loading dataset...")
# loading the raw csv files here. low_memory=False because the files are pretty big
listings_data = pd.read_csv(listings_path, low_memory=False)
reviews_data = pd.read_csv(reviews_path, low_memory=False)

print("Merging data...")
# so basically i needed the date of the latest review for each place
latest_reviews = reviews_data.groupby('listing_id')['date'].max().reset_index()

# then i joined the dates back into the main listings dataset
airbnb_data = pd.merge(listings_data, latest_reviews, on='listing_id', how='left')

# the dataset didn't have availability for some reason, so i just made up random days (0-365) to test the dashboard
if 'availability_365' not in airbnb_data.columns:
    np.random.seed(42)
    airbnb_data['availability_365'] = np.random.randint(0, 365, size=len(airbnb_data))

# ==========================================
# 1. DATA CLEANING
# ==========================================
print("Cleaning data...")

# keeping only the columns i actually care about so it's not super messy
cols_to_keep = ['listing_id', 'price', 'city', 'room_type', 'availability_365', 'review_scores_rating', 'date']
cols = [c for c in cols_to_keep if c in airbnb_data.columns]
airbnb_data = airbnb_data[cols]

# i just dropped any rows that had missing info to keep things simple
airbnb_data = airbnb_data.dropna(subset=['price', 'city', 'room_type', 'date', 'review_scores_rating'])

# the price column had dollar signs and commas, so i had to strip those out to make it a real number
if airbnb_data['price'].dtype == 'O':
    airbnb_data['price'] = airbnb_data['price'].str.replace('$', '', regex=False)
    airbnb_data['price'] = airbnb_data['price'].str.replace(',', '', regex=False)

airbnb_data['price'] = pd.to_numeric(airbnb_data['price'])

# getting rid of weird zero or negative prices
airbnb_data = airbnb_data[airbnb_data['price'] > 0]

# making sure pandas knows this is a date column
airbnb_data['date'] = pd.to_datetime(airbnb_data['date'])

# ==========================================
# 2. FEATURE ENGINEERING
# ==========================================
print("Engineering features...")

# i thought it would be cool to see value for money, so i divided rating by price
airbnb_data['value_score'] = (airbnb_data['review_scores_rating'] / airbnb_data['price']) * 100

# i wanted to group prices so they are easier to show on a chart
def get_price_segment(price):
    if price < 100:
        return 'Budget'
    elif price <= 300:
        return 'Mid-range'
    elif price <= 700:
        return 'Premium'
    else:
        return 'Luxury'

# applying my price grouping function here
airbnb_data['price_segment'] = airbnb_data['price'].apply(get_price_segment)

# i just pulled the month out of the date so i can look at summer vs winter trends
airbnb_data['month'] = airbnb_data['date'].dt.month

# ==========================================
# 3. ANALYSIS
# ==========================================
print("Running analysis...")

# this helped me find the average price for every city
avg_price_by_city = airbnb_data.groupby('city')['price'].mean().reset_index()
avg_price_by_city.columns = ['city', 'city_avg_price']

# checking if entire homes are way more expensive than private rooms
avg_price_by_room = airbnb_data.groupby('room_type')['price'].mean().reset_index()

# seeing which city has the highest value score
avg_value_by_city = airbnb_data.groupby('city')['value_score'].mean().reset_index()

# just counting how many budget vs luxury places there are
segment_dist = airbnb_data['price_segment'].value_counts().reset_index()

# ==========================================
# 4. PRICING STRATEGY LOGIC
# ==========================================
print("Calculating pricing status...")

# i brought the city average price back into my main table
airbnb_data = pd.merge(airbnb_data, avg_price_by_city, on='city', how='left')

# figuring out if a place is ripping you off or if it's a good deal
def get_pricing_status(row):
    price = row['price']
    avg_price = row['city_avg_price']
    
    # basically if it's way below average it's underpriced, and way above is overpriced
    if price < (avg_price * 0.8):
        return 'Underpriced'
    elif price > (avg_price * 1.2):
        return 'Overpriced'
    else:
        return 'Fair'

airbnb_data['pricing_status'] = airbnb_data.apply(get_pricing_status, axis=1)

# ==========================================
# 5. EXPORT FINAL DATASET
# ==========================================
print("Exporting data...")

# saving the final cleaned up data so i can just load it into power bi
output_path = os.path.join(data_dir, 'clean_airbnb.csv')
airbnb_data.to_csv(output_path, index=False)

print(f"Project complete! Data saved as {output_path}")
