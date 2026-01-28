# Sales Data Cleaner

## 1. Project Title & Goal
A local Flask-based application that cleans messy sales CSV data by standardizing prices, removing duplicates, converting currency from USD to INR, and exporting the result as a downloadable JSON file.

---

## 2. Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip installed

### Installation & Run
```bash
pip install -r requirements.txt
python main.py
```

### Access the Application
Open your browser and go to:
```
http://127.0.0.1:5000
```

---

## 3. The Logic (How I Thought)

### Why did I choose this approach?
I chose a Flask-based approach to keep the solution lightweight, easy to run locally, and user-friendly. I added a simple UI that allows users to upload CSV files directly from their system, process them in memory, and download the cleaned JSON output without storing unnecessary files on disk. This mirrors real-world ETL workflows while staying within the problem constraints.

### Core Processing Steps
- Read uploaded CSV data in memory
- Clean inconsistent formatting (quotes, dollar signs)
- Convert price values from string to float
- Deduplicate records using a composite key
- Convert USD prices to INR
- Generate a clean JSON file dynamically named after the uploaded CSV

### Code Snippets (Key Requirements)

#### Convert prices to Float
```python
price_raw = row[2].replace('$', '').strip()
price_usd = float(price_raw)
```

#### Convert all USD prices to INR (1 USD = 83 INR)
```python
price_inr = round(price_usd * 83, 2)
```

#### Remove duplicate rows (same Product, Price, and Country)
```python
dedup_key = (product_name, price_usd, country)
if dedup_key in seen:
    continue
seen.add(dedup_key)
```

### What was the hardest bug you faced, and how did you fix it?
The most challenging part was handling deduplication correctly. Initially, records were removed even when the same product and price appeared in different countries. To fix this, I refined the deduplication logic to include the country field as part of the composite key. This ensured that only truly identical records were removed while preserving valid regional variations. 

---

## 4. Output Screenshots

The following screenshots demonstrate that the application works as expected:
<img width="1920" height="1080" alt="Screenshot (797)" src="https://github.com/user-attachments/assets/b267f2f9-201f-4025-aec0-263cbb56e162" /> The UI

<img width="1920" height="1080" alt="Screenshot (798)" src="https://github.com/user-attachments/assets/d4d883b4-fdab-4c59-b955-2f8c8f2513a1" /> Processing the JSON Creation

<img width="861" height="932" alt="Screenshot 2026-01-28 123029" src="https://github.com/user-attachments/assets/fd0e8c11-2962-4fb0-905d-b712489927c8" /> Cleaned JSON of sales







---

## 5. Future Improvements

If I had two more days, I would add the following enhancements:
- Export cleaned data in CSV and Excel formats in addition to JSON.
- Compare uploaded CSV with the newly created files.
- Support multiple international currency conversions.
- Maintain a processing history to track all uploaded and generated files.

---
