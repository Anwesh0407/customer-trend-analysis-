# Customer Shopping Behavior Analysis

An end-to-end data analytics project that analyzes customer shopping
behavior using **Python, PostgreSQL/SQL, and Power BI**.

The project follows a practical analytics workflow: understand the
business problem, clean and transform the data, answer business
questions with SQL, and present the findings through an interactive
Power BI dashboard.

------------------------------------------------------------------------

## Project Overview

Understanding customer purchasing behavior can help a business improve
its marketing strategy, customer engagement, product decisions, and
retention.

This project analyzes a customer shopping dataset to identify patterns
across:

-   Customer demographics
-   Product categories and products
-   Purchase amounts
-   Discounts and promotions
-   Subscription status
-   Shipping methods
-   Customer loyalty
-   Purchase frequency
-   Review ratings
-   Age groups

### Business Question

> **How can customer shopping data be used to identify purchasing
> trends, understand customer segments, and support better marketing and
> product decisions?**

------------------------------------------------------------------------

## Project Workflow

``` text
Raw Dataset
     ↓
Python / Pandas
     ↓
Data Exploration & Cleaning
     ↓
Feature Engineering
     ↓
PostgreSQL
     ↓
SQL Business Analysis
     ↓
Power BI
     ↓
Interactive Dashboard
     ↓
Business Insights
```

------------------------------------------------------------------------

## Dataset

The dataset contains **3,900 customer records** and **18 original
attributes**.

Each row represents a customer and their latest recorded purchase rather
than a complete transaction history.

### Main Attributes

  Column                   Description
  ------------------------ ------------------------------------
  Customer ID              Unique customer identifier
  Age                      Customer age
  Gender                   Customer gender
  Item Purchased           Product purchased
  Category                 Product category
  Purchase Amount (USD)    Amount spent on the purchase
  Location                 Customer/purchase location
  Size                     Product size
  Color                    Product color
  Season                   Purchase season
  Review Rating            Customer review rating
  Subscription Status      Whether the customer is subscribed
  Shipping Type            Shipping method
  Discount Applied         Whether a discount was applied
  Promo Code Used          Whether a promo code was used
  Previous Purchases       Number of previous purchases
  Payment Method           Payment method
  Frequency of Purchases   Purchase frequency

> **Dataset limitation:** The dataset does not contain complete
> historical transactions for every customer. It provides the latest
> purchase along with previous-purchase count and purchase-frequency
> information.

------------------------------------------------------------------------

# 1. Data Analysis with Python

Python was used for initial data exploration, cleaning, transformation,
and feature engineering.

### Libraries

-   Python
-   Pandas
-   Jupyter Notebook

### Exploratory Data Analysis

The dataset was examined using:

``` python
df.head()
df.info()
df.describe(include='all')
df.isnull().sum()
```

This was used to understand:

-   Dataset structure
-   Number of observations and columns
-   Data types
-   Summary statistics
-   Missing values

### Missing Value Treatment

The `Review Rating` column contained **37 missing values**.

Instead of replacing all missing values with the overall median, the
missing ratings were imputed using the **median rating within each
product category**.

``` python
df['Review Rating'] = (
    df.groupby('Category')['Review Rating']
      .transform(lambda x: x.fillna(x.median()))
)
```

This preserves differences in rating patterns between categories.

### Column Standardization

Column names were converted to lowercase and spaces were replaced with
underscores.

For example:

``` text
Customer ID
        ↓
customer_id
```

`Purchase Amount (USD)` was also renamed to:

``` text
purchase_amount
```

This makes the dataset easier to work with in both Python and SQL.

### Feature Engineering

#### Age Group

Customers were divided into four age groups using `pd.qcut()`:

-   Young Adult
-   Adult
-   Middle-aged
-   Senior

#### Purchase Frequency Days

The text-based purchase frequency was converted into a numerical
representation.

Examples:

``` text
Weekly          → 7 days
Fortnightly     → 14 days
Monthly         → 30 days
Quarterly       → 90 days
Annually        → 365 days
```

This creates the new feature:

``` text
purchase_frequency_days
```

### Redundant Column Removal

`discount_applied` and `promo_code_used` contained identical information
in this dataset.

After verifying their equality, `promo_code_used` was removed to avoid
redundancy.

------------------------------------------------------------------------

# 2. SQL Analysis with PostgreSQL

The cleaned dataset was loaded into a PostgreSQL database using
**SQLAlchemy**.

### Tools

-   PostgreSQL
-   pgAdmin
-   SQL
-   SQLAlchemy
-   psycopg2

The cleaned DataFrame was loaded into a table named:

``` text
customer
```

### Business Questions

The SQL analysis answers the following questions:

1.  **What is the total revenue generated by male vs. female
    customers?**

2.  **Which customers used a discount but still spent more than the
    average purchase amount?**

3.  **Which are the top 5 products with the highest average review
    rating?**

4.  **How does the average purchase amount compare between Standard and
    Express shipping?**

5.  **Do subscribed customers spend more?**

6.  **Which 5 products have the highest percentage of purchases with
    discounts applied?**

7.  **How many customers are New, Returning, and Loyal based on previous
    purchases?**

8.  **What are the top 3 most purchased products within each category?**

9.  **Are repeat buyers with more than 5 previous purchases more likely
    to subscribe?**

10. **What is the revenue contribution of each age group?**

### SQL Concepts Used

The project demonstrates:

-   `SELECT`
-   `WHERE`
-   `GROUP BY`
-   `ORDER BY`
-   Aggregate functions
-   `AVG()`
-   `SUM()`
-   `COUNT()`
-   Subqueries
-   `CASE`
-   CTEs
-   `ROW_NUMBER()`
-   Window functions
-   Conditional aggregation
-   Type casting
-   Filtering and segmentation

------------------------------------------------------------------------

# 3. Key Findings

Based on the cleaned dataset and SQL analysis:

### Revenue by Gender

  Gender     Revenue (USD)
  -------- ---------------
  Male           \$157,890
  Female          \$75,191

### Subscription Analysis

  Subscription     Customers   Avg. Spend (USD)   Revenue (USD)
  -------------- ----------- ------------------ ---------------
  No                   2,847            \$59.87       \$170,436
  Yes                  1,053            \$59.49        \$62,645

The average purchase amount is very similar between subscribers and
non-subscribers, while non-subscribers contribute substantially more
total revenue because they represent a larger customer base.

### Top-Rated Products

The five products with the highest average review ratings were:

1.  Gloves
2.  Sandals
3.  Boots
4.  Hat
5.  Skirt

### Shipping

  Shipping Type     Average Purchase (USD)
  --------------- ------------------------
  Express                          \$60.48
  Standard                         \$58.46

Express-shipping customers show a slightly higher average purchase
amount.

### Customer Segmentation

  Segment       Customers
  ----------- -----------
  Loyal             3,116
  Returning           701
  New                  83

The dataset is heavily concentrated toward customers with a high number
of previous purchases.

### Discount Dependence

The products with the highest proportion of discounted purchases
include:

-   Hat
-   Sneakers
-   Coat
-   Sweater
-   Pants

### Revenue by Age Group

  Age Group       Revenue (USD)
  ------------- ---------------
  Young Adult          \$62,143
  Middle-aged          \$59,197
  Adult                \$55,978
  Senior               \$55,763

Young Adults contribute the highest revenue among the four age groups in
this dataset.

------------------------------------------------------------------------

# 4. Power BI Dashboard

The cleaned and analyzed customer data was used to build an interactive
Power BI dashboard.

### Dashboard KPIs

The dashboard includes:

-   Number of Customers
-   Average Purchase Amount
-   Average Review Rating

### Visualizations

The dashboard explores:

-   Revenue by Category
-   Sales by Category
-   Revenue by Age Group
-   Sales by Age Group
-   Subscription Status
-   Customer demographics

### Interactive Filters

The dashboard includes slicers for:

-   Subscription Status
-   Gender
-   Category
-   Shipping Type

These filters allow users to interactively explore customer behavior and
see how the key metrics change across different segments.

------------------------------------------------------------------------

## Dashboard Preview

Add your dashboard screenshot here:

``` text
![Customer Behavior Dashboard](images/customer_behavior_dashboard.png)
```

If you do not have an image yet, export a screenshot from the Power BI
dashboard and save it inside an `images` folder.

------------------------------------------------------------------------

# 5. Project Structure

``` text
customer-shopping-behavior-analysis/
│
├── data/
│   └── customer_shopping_behavior.csv
│
├── notebooks/
│   └── Customer_Shopping_Behavior_Analysis.ipynb
│
├── sql/
│   └── customer_behavior_sql_queries.sql
│
├── dashboard/
│   └── customer_behavior_dashboard.pbix
│
├── images/
│   └── customer_behavior_dashboard.png
│
└── README.md
```

------------------------------------------------------------------------

# 6. How to Run the Project

## Step 1 --- Clone the Repository

``` bash
git clone <your-repository-url>
cd customer-shopping-behavior-analysis
```

## Step 2 --- Install Python Dependencies

``` bash
pip install pandas sqlalchemy psycopg2-binary jupyter
```

## Step 3 --- Run the Notebook

Open:

``` text
Customer_Shopping_Behavior_Analysis.ipynb
```

Run the notebook to:

-   Load the dataset
-   Explore the data
-   Clean missing values
-   Standardize column names
-   Create engineered features
-   Prepare the dataset for SQL analysis

## Step 4 --- Set Up PostgreSQL

Create a PostgreSQL database named:

``` text
customer_behavior
```

Create/load the cleaned dataset into the:

``` text
customer
```

table.

Update the database connection credentials in the notebook before
running the PostgreSQL loading section.

## Step 5 --- Run SQL Analysis

Open:

``` text
customer_behavior_sql_queries.sql
```

Run the queries in PostgreSQL/pgAdmin to reproduce the business
analysis.

## Step 6 --- Open the Power BI Dashboard

Open:

``` text
customer_behavior_dashboard.pbix
```

If required, update the database connection to your local PostgreSQL
instance.

------------------------------------------------------------------------

# 7. Skills Demonstrated

This project demonstrates practical experience with:

**Data Analytics** - Data cleaning - Exploratory data analysis - Feature
engineering - Customer segmentation - Business-oriented analysis

**Python** - Pandas - Data transformation - Missing-value handling -
Categorical feature engineering

**SQL** - Aggregations - Subqueries - CTEs - CASE statements - Window
functions - Conditional aggregation - Business problem solving

**Data Visualization** - Power BI - KPI cards - Interactive charts -
Slicers - Dashboard design

**Database** - PostgreSQL - pgAdmin - SQLAlchemy

------------------------------------------------------------------------

# 8. Business Takeaways

The analysis provides several useful business perspectives:

-   Male customers contribute a larger share of revenue in this dataset.
-   Subscription status does not correspond to a higher average purchase
    amount in the available data.
-   Express-shipping customers have a slightly higher average purchase
    amount than Standard-shipping customers.
-   The customer base is dominated by loyal customers based on
    previous-purchase count.
-   Some products have a much higher dependence on discounts than
    others.
-   Young Adults generate the highest revenue among the defined age
    groups.
-   Highly rated products can be identified for potential marketing and
    merchandising decisions.

These findings can be further investigated with additional
transaction-level and customer-history data.

------------------------------------------------------------------------

# 9. Limitations

This project is based on a customer-behavior snapshot rather than a
complete transactional database.

Important limitations include:

-   No complete transaction history for individual customers
-   Previous purchases are represented as a count rather than individual
    transactions
-   Purchase frequency is categorical in the original dataset
-   The analysis does not establish causation between customer behavior
    and business outcomes
-   The dataset does not provide enough historical information for true
    customer lifetime value or retention analysis

------------------------------------------------------------------------

# 10. Future Improvements

The project can be extended by adding:

-   Customer Lifetime Value (CLV)
-   RFM customer segmentation
-   Cohort analysis
-   Customer retention analysis
-   Churn prediction
-   Purchase prediction
-   Recommendation systems
-   Time-series sales analysis
-   Advanced ML-based customer segmentation

------------------------------------------------------------------------

## Author

**Anwesh Bindhani**

A data analytics portfolio project focused on transforming raw customer
data into actionable business insights using Python, SQL, and Power BI.

------------------------------------------------------------------------

## Disclaimer

This project is intended for educational and portfolio purposes. The
insights are based on the available dataset and should not be
interpreted as definitive business conclusions without additional
transactional and customer-level data.
