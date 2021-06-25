# House Rocket Streamlit
House Rocket dashboard using Streamlit, from Python ZERO ao DS course.

Project url: https://house-rocket-analytics-app.herokuapp.com/

## Business Problem
- **Company:** House Rocket;

- **Business Model:** Buy houses at the lowest price and review at the highest price;

- **Challenge:** Find good deals within the available portfolio, that is, find homes with a low price, in a great location and that have a great resale potential for a higher price.

The proposed challenge can be found [here](https://sejaumdatascientist.com/os-5-projetos-de-data-science-que-fara-o-recrutador-olhar-para-voce/). 

## CEO Requests
**I would like to arrive at my desk in the morning and have a unique place where I can look at House Rocket's portfolio. In this portfolio, I have interest:**

1. Filters of properties by one or several regions.
2. Choose one or more variables to view.
3. Look at the total number of properties, the average price, the average living room and also the average price per square meter in each of the zip codes.
4. Analyze each of the columns in a more described way.
5. A map with portfolio density by region and also price density.
6. Check the annual price variation.
7. Check the daily price variation.
8. Check the distribution of properties by:
- Price;
- Number of bedrooms;
- Number of bathrooms;
- Number of floors;
- Water view or not.

## Solution planning
**1. End product:**

A Link to access the dashboard.

**2. Tools:**
- Python 3.8.0;
- VS Code.

## Process
### 1. Filters properties by one or several regions.
- **Purpose:** View properties by zip code.
- **User Action:** Enter one or more desired codes.
- **The view:** A table with all attributes and filtered by zip code.

### 2. Choose one or more variables to view.
- **Objective:** View the characteristics of the property.
- **User Action:** Type the desired features.
- **The view:** A table with all selected attributes.

### 3. Observe the total number of properties, the average price, the average of the room be and also the average price per square meter in each of the postal codes.
- **Purpose:** View the averages of some metrics by region
- **User Action:** Enter the desired metrics.
- **The view:** A table with all selected attributes.

### 4. Analyze each of the columns in a more descriptive way.
- **Purpose:** View descriptive metrics for each of chosen attributes.
- **User Action:** Enter the desired metrics.
- **The view:** A table with descriptive metrics by attribute.

### 5. A map with the portfolio density by region and also the density of price.
- **Purpose:** View the portfolio density on the map (number of properties per region).
- **User Action:** No action.
- **Visualization:** A map with the density of properties by region.

### 6. Check the annual price variation.
- **Purpose:** Observe annual price variations.
- **User Action:** Filters data by year.
- **The visualization:** A line graph with years in x and average prices in y.

### 7. Check the daily price variation.
- **Purpose:** Observe daily price variations.
- **User Action:** Filters data by day.
- **The visualization:** A line graph with days in x and average prices in y.

### 8. Check the distribution of properties by:
- Price;
- Number of bedrooms;
- Number of bathrooms;
- Number of floors;
- Water view or not.

- **Purpose:** Observe the concentration of properties by price, bedrooms, bathrooms and floors.
- **User Action:** Price filter, room, bathroom and floor.
- **The visualization:** A histogram with each attribute defined.
