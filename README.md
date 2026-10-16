# Big Data ELT Pipeline Project

## Description

A Big Data ELT pipeline for processing large mixed-quality order datasets using Python, PySpark, and MongoDB.

The system supports:
- File routing between Python Batch and PySpark
- Loading raw data into MongoDB
- Data quality validation and correction
- Quarantine of invalid records
- Metrics generation


## Technologies

- Python
- PySpark 4.2.0
- MongoDB
- PyMongo


## Pipeline Flow

CSV File

↓

File Router

↓

Python Batch / PySpark

↓

MongoDB Raw

↓

ELT Quality Processing

↓

Validated Data + Quarantine


## Execution Results

Total Records: 1,048,575

Validated Records: 985,991

Quarantine Records: 48,276

Inserted Records: 1,034,257

Updated Records: 14,318

Status: SUCCESS


## MongoDB Collections

- orders_raw
- orders_validated
- orders_quarantine


## Run Project

Install requirements:

pip install -r requirements.txt

Run:

python src/main.py


## Output

Results are stored in:

reports/results.json