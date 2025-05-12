# Trezor Case Study - Inventory Analysis

This project implements an ELT (Extract, Load, Transform) pipeline to process and analyze inventory data from Keboola. The solution focuses on transforming raw data into business-ready insights, with a particular emphasis on inventory management and stock level analysis.

## Project Structure

```
trezor-case-study/
├── lib/                    # Core library code
├── sql_scripts/           # SQL transformation scripts
├── elt_jobs.json         # Job configuration
├── elt_run_job.py       # Job execution script
├── elt_daily_load.py    # Daily load orchestration
└── main.py             # Main entry point
```

## Features

- Data extraction from Keboola API
- Secure credential management using keyring
- PostgreSQL-based data transformations
- Daily automated data loads
- Inventory analysis including:
  - Total stock per product across locations
  - Stock level monitoring
  - Product status tracking

## Prerequisites

- Python
- PostgreSQL
- Keboola API access
- keyring package for secure credential storage
- black (for code formatting)

## Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure credentials:
   ```PYTHON
   # Set Keboola API token
   import keyring
   
   keyring.set_password('KEBOOLA', 'keboola', 'your-token')
   keyring.set_password('POSTGRES', 'postgres', 'password')
   ```

## Usage

### Running Individual Jobs

To run a specific ELT job:

etl_run_job.py:
```python
if __name__ == '__main__':
    run_job(['choose_your_desired_job'])
```
All the jobs need to be specified in elt_jobs.json

### Running Daily Load

To execute the complete daily load process:
```bash
python elt_daily_load.py
```

### Data Analysis

After loading the data, you can analyze it using the gold layer views:
```sql
-- View total stock per product
SELECT * FROM gold.product_status_summary;

-- Check low stock products
SELECT * FROM gold.product_status_summary 
WHERE stock_status = 'Low Stock';
```

## Data Flow

1. **Extract**: Data is pulled from Keboola API
2. **Load**: Raw data is loaded into bronze layer tables
3. **Transform**: SQL scripts transform the data into gold layer views
4. **Analyze**: Business-ready views provide insights on inventory status

## Data Quality
- I noticed some data quality issues
  - first was that quantity_on_hand was higher than quantity_available which I dont think is correct, so if that was the case I set the column to quantity_available
  - there are also missing dimensions but I do not think it has an impact on the data because the main information is that if we have that product in stock or not

## Future Improvements
- Create star schema in gold layer - dimension and fact tables
- support for more data sources - not only Keboola
- create custom exceptions for better error handling