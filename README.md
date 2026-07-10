# 🛒 E-Commerce Order Analytics System

## 📌 Project Overview

This project is an end-to-end E-Commerce Order Analytics System developed using **Python**, **SQLite**, and **SQL**.

The system performs the complete analytics pipeline:

- Generate realistic e-commerce datasets
- Clean and validate raw data
- Load cleaned data into SQLite
- Execute analytical SQL queries
- Generate CLI reports
- Run automated test cases

---

# 🛠️ Technologies Used

- Python 3.x
- Pandas (v2.1.0)
- SQLite
- SQL
- Faker
- Tabulate

---

# 📂 Project Structure

```
ecommerce-analytics-system
│
├── data
│   ├── raw
│   └── cleaned
│
├── database
│   └── ecommerce.db
│
├── output
│   ├── cli_report_output.txt
│   └── sample_reports
│
├── scripts
│   ├── generate_data.py
│   ├── clean_data.py
│   ├── load_database.py
│   ├── run_queries.py
│   ├── report_cli.py
│   └── run_tests.py
│
├── sql
│   ├── schema.sql
│   ├── aggregations.sql
│   ├── window_functions.sql
│   └── cohort_analysis.sql
│
├── README.md
├── requirements.txt
└── .gitignore
```

> **Note:** The files inside the `data/raw/`, `data/cleaned/`, `database/`, and `output/` directories are not present initially. They will be automatically generated and populated once you execute the pipeline scripts.

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/itskeshavsharma/Celebal-Internship-Week8.git
```

Move into project directory

```bash
cd Celebal-Internship-Week8
```

Install dependencies

```bash
pip install -r requirements.txt
```

# ▶️ Execution Flow

There are **2 methods** to run the project:

---

## ⚡ Method 1: Automated Pipeline (Run All in One Command)

If you want to run the entire pipeline (generate, clean, load, and query) automatically in one go, execute this script in the root directory:

```bash
python run_all.py
```

This script will run all steps sequentially and display the validation results at the end.

---

## 🛠️ Method 2: Step-by-Step Manual Execution

If you prefer to execute the steps manually one by one, run the following commands in this sequence:

### Step 1 : Generate Raw Dataset
```bash
python scripts/generate_data.py
```
* **Output**: `data/raw/` (customers.csv, products.csv, orders.csv, order_items.csv)

### Step 2 : Clean Raw Data
```bash
python scripts/clean_data.py
```
* **Tasks**: Duplicates removal, missing values handling, email validation, future orders cleaning.
* **Output**: `data/cleaned/` (customers_clean.csv, products_clean.csv, orders_clean.csv, order_items_clean.csv)

### Step 3 : Load Database
```bash
python scripts/load_database.py
```
* **Tasks**: Create SQLite tables, set foreign keys & indices, load cleaned data.
* **Output**: `database/ecommerce.db`

### Step 4 : Execute SQL Queries
```bash
python scripts/run_queries.py
```
* **Tasks**: Runs analytical SQL scripts.
* **Output**: `output/sample_reports/` (aggregations_report.txt, window_functions_report.txt, cohort_analysis_report.txt)

### Step 5 : Generate CLI Analytics Report
```bash
python scripts/report_cli.py
```
* **Tasks**: Interactive report menu (Daily, Weekly, Monthly).
* **Output**: `output/cli_report_output.txt`

### Step 6 : Run Test Cases
```bash
python scripts/run_tests.py
```
* **Tasks**: Runs data integrity test cases and validations.

---

# 📊 SQL Features

The project includes

- Aggregations
- GROUP BY
- ORDER BY
- Window Functions
- ROW_NUMBER()
- RANK()
- DENSE_RANK()
- LAG()
- LEAD()
- Running Total
- Moving Average
- Cohort Analysis
- Customer Segmentation
- Revenue Analysis

---

# 📈 Reports Generated

- Revenue Report
- Monthly Revenue
- Top Customers
- Top Products
- Cohort Analysis
- Customer Segmentation
- Window Function Reports
- CLI Analytics Dashboard

---

# ✅ Output Folders

```
data/raw/
```

Generated raw datasets.

```
data/cleaned/
```

Validated and cleaned datasets.

```
database/
```

SQLite database.

```
output/sample_reports/
```

SQL query outputs.

```
output/
```

CLI generated reports.

---

# 📌 Author

Keshav kumar Sharma

Celebal Technologies Internship Project

2026