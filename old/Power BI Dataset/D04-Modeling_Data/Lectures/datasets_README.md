# Brew & Bean — Power BI training datasets

## Overview

These datasets support Day 2 of the Power BI training program (Modeling the Data). They represent **Brew & Bean**, a fictional coffee shop chain with 12 locations across Seattle, Portland, and San Francisco. The data covers January 2022 through December 2024.

## Star schema

```
                    ┌──────────────┐
                    │  DimProducts │
                    │  (24 rows)   │
                    └──────┬───────┘
                           │ ProductKey
┌──────────────┐    ┌──────┴───────┐    ┌──────────────┐
│  DimStores   │────│  FactSales   │────│ DimCustomers │
│  (12 rows)   │    │ (280K rows)  │    │  (500 rows)  │
└──────────────┘    └──────┬───────┘    └──────────────┘
     StoreKey              │ DateKey         CustomerKey
                    ┌──────┴───────┐
                    │   DimDate    │
                    │ (1,826 rows) │
                    └──────────────┘
```

Additional tables: **MonthlyTargets** (409 rows), **CustomerFeedback** (1,200 rows), **Inventory** (12,580 rows).

## Files and columns

### DimProducts.csv — 24 rows

The product catalog. 22 active items and 2 seasonal (inactive) products.

| Column | Type | Description |
|---|---|---|
| ProductKey | Integer | Primary key (1–24) |
| ProductName | Text | Product name (e.g., "Latte", "Croissant") |
| Category | Text | Coffee, Tea, Pastry, Food |
| Size | Text | Single, Small, Medium, Large, Regular |
| BasePrice | Decimal | Selling price in USD |
| Cost | Decimal | Cost of goods in USD |
| IsActive | Boolean | True = currently sold, False = seasonal/retired |

### DimStores.csv — 12 rows

Store locations with manager information. Includes ManagerEmail for Row-Level Security exercises (Course 01).

| Column | Type | Description |
|---|---|---|
| StoreKey | Integer | Primary key (1–12) |
| StoreName | Text | Location name (e.g., "Downtown Flagship") |
| City | Text | Seattle, Portland, or San Francisco |
| Region | Text | All "West" (single region for this dataset) |
| OpenDate | Date | Store opening date |
| SquareFootage | Integer | Store size in square feet |
| Manager | Text | Store manager full name |
| ManagerEmail | Text | Manager's email — used for dynamic RLS |

### DimCustomers.csv — 500 rows

Loyalty program members. ~15% have missing email, ~10% have missing phone.

| Column | Type | Description |
|---|---|---|
| CustomerKey | Integer | Primary key (1–500) |
| FirstName | Text | Customer first name |
| LastName | Text | Customer last name |
| Email | Text | Email address (blank for ~15% of rows) |
| Phone | Text | Phone number (blank for ~10% of rows) |
| City | Text | Customer's city |
| LoyaltyTier | Text | Bronze, Silver, Gold, or Platinum |
| SignupDate | Date | Loyalty program enrollment date |

### DimDate.csv — 1,826 rows

Complete date dimension covering January 1, 2021 through December 31, 2025. No gaps.

| Column | Type | Description |
|---|---|---|
| DateKey | Integer | Primary key in YYYYMMDD format |
| Date | Date | ISO date (YYYY-MM-DD) |
| Year | Integer | Calendar year |
| Quarter | Text | "Q1" through "Q4" |
| QuarterNumber | Integer | 1–4 |
| MonthNumber | Integer | 1–12 |
| MonthName | Text | Full month name ("January") |
| MonthYear | Text | "Jan 2022" format |
| WeekNumber | Integer | ISO week number |
| Day | Integer | Day of month |
| DayName | Text | Full day name ("Monday") |
| DayOfWeek | Integer | 1=Monday through 7=Sunday |
| IsWeekend | Boolean | True for Saturday/Sunday |
| FiscalYear | Text | "FY2022" (July–June fiscal year) |
| FiscalQuarter | Text | "FQ1" through "FQ4" |

### FactSales.csv — 280,077 rows

Point-of-sale transactions across all stores. ~46% of transactions have no CustomerKey (non-loyalty purchases).

| Column | Type | Description |
|---|---|---|
| TransactionID | Integer | Primary key (unique per transaction) |
| StoreKey | Integer | Foreign key → DimStores |
| ProductKey | Integer | Foreign key → DimProducts |
| CustomerKey | Integer | Foreign key → DimCustomers (blank for ~46%) |
| DateKey | Integer | Foreign key → DimDate (YYYYMMDD) |
| Quantity | Integer | Items purchased (1–3) |
| UnitPrice | Decimal | Price per item (may differ from BasePrice due to discounts) |
| TotalAmount | Decimal | Quantity × UnitPrice |
| TransactionDateTime | DateTime | Full timestamp of transaction |
| PaymentMethod | Text | Card, Cash, Mobile, or Gift Card |

### MonthlyTargets.csv — 409 rows

Sales targets set by store by month. Only includes months after each store's opening date.

| Column | Type | Description |
|---|---|---|
| StoreKey | Integer | Foreign key → DimStores |
| DateKey | Integer | Foreign key → DimDate (first day of month, YYYYMMDD) |
| Month | Text | "YYYY-MM" format |
| SalesTarget | Integer | Revenue target in USD |
| TransactionTarget | Integer | Transaction count target |

### CustomerFeedback.csv — 1,200 rows

Customer satisfaction surveys. ~60% linked to a loyalty member, ~40% anonymous. ~10% have blank comments.

| Column | Type | Description |
|---|---|---|
| FeedbackID | Text | Primary key ("F-10001" format) |
| StoreKey | Integer | Foreign key → DimStores |
| CustomerKey | Integer | Foreign key → DimCustomers (blank for ~40%) |
| DateKey | Integer | Foreign key → DimDate |
| FeedbackDate | Date | Survey submission date |
| OverallScore | Integer | 1–5 overall rating |
| ServiceScore | Integer | 1–5 service rating |
| QualityScore | Integer | 1–5 quality rating |
| Comments | Text | Free-text feedback (blank for ~10%) |

### Inventory.csv — 12,580 rows

Weekly stock count snapshots (every Monday) for 10 key products across all stores. Used for semi-additive measure exercises (Course 03).

| Column | Type | Description |
|---|---|---|
| StoreKey | Integer | Foreign key → DimStores |
| ProductKey | Integer | Foreign key → DimProducts |
| DateKey | Integer | Foreign key → DimDate |
| SnapshotDate | Date | Monday snapshot date |
| StockCount | Integer | Units in stock at count time |

## Course mapping

| Dataset | Course 01 | Course 02 | Course 03 | Course 04 |
|---|---|---|---|---|
| DimProducts | Relationships, hierarchies | CALCULATE, iterators | — | Cardinality reduction |
| DimStores | RLS (ManagerEmail), hierarchies | SWITCH, SELECTEDVALUE | — | Q&A synonyms |
| DimCustomers | Properties, hide keys | DISTINCTCOUNT, COALESCE | — | Remove unused columns |
| DimDate | Date table, Sort by Column | — | YTD, QTD, MTD, DATEADD | Data type optimization |
| FactSales | Star schema center | All measures | Time intelligence | Performance Analyzer |
| MonthlyTargets | Composite keys | IF (target comparison) | YTD target vs actual | — |
| CustomerFeedback | Properties, data categories | AVERAGE, conditional | — | Filter unnecessary rows |
| Inventory | — | — | Semi-additive (LASTDATE) | — |

## Data characteristics

These features are intentional for teaching purposes:

**46% null CustomerKey** in FactSales teaches NULL handling, ISBLANK, and the difference between COUNTROWS and DISTINCTCOUNT.

**~5% discounted transactions** where UnitPrice differs from BasePrice teaches why SUMX is needed (row-level Quantity × UnitPrice) versus using a pre-calculated column.

**Year-over-year growth** (~8% annually) makes YoY comparison measures produce meaningful positive results that students can verify.

**Seasonal patterns** (summer and holiday peaks) make moving averages visually demonstrate smoothing of genuine fluctuations.

**Store opening dates** vary, so some stores have no data for early months. This teaches students to handle partial data ranges and explains why some comparisons return BLANK.

**Weekly inventory snapshots** (Mondays only) demonstrate why LASTNONBLANK is needed — most dates have no inventory data, so LASTDATE alone returns BLANK for Tuesday through Sunday.
