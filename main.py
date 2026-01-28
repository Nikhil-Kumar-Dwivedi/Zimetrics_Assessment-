from flask import Flask, render_template, request, send_file, jsonify
import csv
import json
import io
import os

app = Flask(__name__)

USD_TO_INR = 83  # Conversion rate


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process_csv():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    
    original_filename = os.path.splitext(file.filename)[0]
    output_filename = f"{original_filename}_clean_sales.json"

    
    stream = io.StringIO(file.stream.read().decode("utf-8"))
    reader = csv.reader(stream)

    cleaned_data = []
    seen = set()  # Track (product_name, price, country)

    for row in reader:
        if len(row) != 4:
            continue  

        product_id = row[0].strip()

        
        product_name = row[1].replace('"', '').strip()

        
        country = row[3].strip()

        
        price_raw = row[2].replace('$', '').strip()
        try:
            price_usd = float(price_raw)
        except ValueError:
            continue

        # Deduplication key (product + price + country)
        dedup_key = (product_name, price_usd, country)
        if dedup_key in seen:
            continue

        seen.add(dedup_key)

        
        price_inr = round(price_usd * USD_TO_INR, 2)

        cleaned_data.append({
            "product_id": int(product_id),
            "product_name": product_name,
            "price_in_inr": price_inr,
            "country": country
        })

    # Write JSON file in memory
    json_buffer = io.BytesIO()
    json_buffer.write(json.dumps(cleaned_data, indent=4).encode("utf-8"))
    json_buffer.seek(0)

    return send_file(
        json_buffer,
        as_attachment=True,
        download_name=output_filename,
        mimetype="application/json"
    )


if __name__ == "__main__":
    app.run(debug=True)

