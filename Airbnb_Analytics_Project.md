# Airbnb Data Analytics Project - Complete Guide

This document contains everything you need for your end-to-end Airbnb analytics project, including the step-by-step Power BI guide, color design rules, business insights, and a resume bullet point.

---

## PART 2: POWER BI DASHBOARD (FULL DESIGN)

Create exactly 5 pages in your Power BI dashboard. Here is the layout and content for each:

### 1. OVERVIEW (The Big Picture)
* **What it shows:** High-level metrics and the overall breakdown of the market.
* **Layout:** KPIs at the top, a donut chart in the center, and a bar chart at the bottom.
* **Visuals:**
  - **KPI Cards (Top):** `Average of price`, `Count of listing_id` (Total Listings), `Average of review_scores_rating`.
  - **Donut Chart (Center):** Legend = `price_segment`, Values = `Count of listing_id`. (Shows the distribution of Budget vs. Luxury listings).
  - **Clustered Bar Chart (Bottom):** X-axis = `room_type`, Y-axis = `Average of price`.

### 2. CITY ANALYSIS (Geographic View)
* **What it shows:** Where listings are concentrated and which cities are the most expensive.
* **Layout:** Map visual taking up the left side, with a bar chart on the right side.
* **Visuals:**
  - **Map Visual (Left):** Location = `city`, Bubble Size = `Count of listing_id`.
  - **Clustered Bar Chart (Right):** X-axis = `city`, Y-axis = `Average of price`. Sort descending to show the most expensive cities first.

### 3. PRICING ANALYSIS (Strategy View)
* **What it shows:** Identifying which listings are overpriced, underpriced, or fair compared to their local market.
* **Layout:** Table at the bottom, stacked column chart at the top.
* **Visuals:**
  - **Stacked Column Chart (Top):** X-axis = `city`, Legend = `pricing_status`, Y-axis = `Count of listing_id`. (Shows how many listings in each city are underpriced/overpriced).
  - **Table (Bottom):** Columns = `listing_id`, `city`, `price`, `city_avg_price`, `pricing_status`.

### 4. DEMAND TRENDS (Time-Series View)
* **What it shows:** How pricing and availability fluctuate throughout the year.
* **Layout:** Two line charts stacked vertically. Add a Slicer for `city` on the left pane.
* **Visuals:**
  - **Slicer (Left Pane):** Field = `city`.
  - **Line Chart (Top Right):** X-axis = `month`, Y-axis = `Average of price`.
  - **Line Chart (Bottom Right):** X-axis = `month`, Y-axis = `Average of availability_365`.

### 5. VALUE INSIGHTS (Customer Perspective)
* **What it shows:** Finding the best "bang for your buck" across the market.
* **Layout:** Table taking up most of the space, with a KPI highlighting the #1 city.
* **Visuals:**
  - **KPI Card (Top):** First `city` (filtered to show the city with the highest `value_score`).
  - **Table (Center):** Columns = `city`, `Average of price`, `Average of value_score`. *Sort this table by `value_score` descending.*
  - **Scatter Plot (Optional, Bottom):** X-axis = `price`, Y-axis = `review_scores_rating`.

---

## PART 3: AIRBNB COLOR PALETTE DESIGN

To make your dashboard look professional and cohesive, use this Airbnb-inspired design system. Go to the **View** tab in Power BI, click the drop-down arrow in the Themes section, and select **Customize Current Theme** to apply these hex codes.

* **Primary Red:** `#FF5A5F` (Use for major accents, primary KPIs, and highlighting important data points like "Underpriced").
* **Dark Text:** `#222222` (Use for all chart titles, axis labels, and regular text).
* **Gray:** `#767676` (Use for secondary text, gridlines, and subtle UI borders).
* **Light Background:** `#F7F7F7` (Use as the main canvas background color to make visuals pop).
* **White:** `#FFFFFF` (Use for the background of individual visual cards to create a "card" effect over the light gray canvas).

**Design Rules for a Clean Look:**
1. **Remove Clutter:** Turn off gridlines in your charts and remove background colors from your slicers.
2. **Card Effect:** Set the background of every visual to White (`#FFFFFF`) with a subtle shadow. Place them on the Light Background (`#F7F7F7`) canvas.
3. **Consistent Fonts:** Use `Segoe UI` or `DIN` (built into Power BI) for a modern, clean look. Make all chart titles 12pt, bold, and Dark Text (`#222222`).

---

## PART 4: BUSINESS INSIGHTS

*Use these simple, human-like insights when explaining your project:*

1. **Market Saturation:** The vast majority of our listings fall into the "Mid-range" ($100-$300) and "Budget" (<$100) segments. True "Luxury" listings are rare, meaning hosts in that segment face far less direct competition.
2. **The "Entire Home" Premium:** Entire homes and apartments command significantly higher average prices compared to private rooms, proving that guests are willing to pay a heavy premium for privacy.
3. **Hidden Value Markets:** While major tourist hubs naturally have the highest average prices, some secondary cities actually score higher on our `value_score` metric. These are prime locations to promote to budget-conscious travelers.
4. **Seasonal Fluctuations:** We see a clear spike in average prices during peak months, accompanied by a drop in average availability. This indicates strong seasonal demand where hosts can safely increase their rates.
5. **Pricing Strategy Inefficiencies:** A surprising percentage of listings are flagged as "Underpriced" (priced 20%+ below their city's average). This indicates that many hosts are leaving money on the table and could likely raise rates without sacrificing bookings.

---

## PART 5: RESUME LINE

*Add this bullet point to your resume under a "Projects" or "Experience" section:*

**Data Analyst | Airbnb Market & Pricing Analysis**
* Engineered a clean dataset using Python (Pandas) to extract pricing segments and calculate value metrics.
* Designed a 5-page interactive Power BI dashboard utilizing a custom Airbnb UI color palette (#FF5A5F), enabling the identification of seasonal demand trends and over/underpriced listings.
