# Big Data ELT Pipeline Project

## Description

A Big Data ELT pipeline for processing large mixed-quality order datasets using Python, PySpark, MongoDB, and FastAPI.

The system supports:

- File routing between Python Batch and PySpark
- Loading raw data into MongoDB
- Data quality validation and correction
- Quarantine of invalid records
- Metrics generation
- CSV ingestion through REST API

## Technologies

- Python
- PySpark 4.2.0
- MongoDB
- PyMongo
- FastAPI
- Uvicorn

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

## File Routing

Files are automatically routed according to file size:

- Small files: Python Batch
- Large files: PySpark

The current routing threshold is 200 MB.

## Latest Execution Results

Total Records: 1,048,581

Valid/Corrected Records: 1,000,299

Corrected Records: 23,398

Quarantine Records: 48,282

Inserted Records: 7,344

Updated Records: 1,041,237

Status: SUCCESS

## MongoDB Collections

- orders_raw
- orders_validated
- orders_quarantine

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt