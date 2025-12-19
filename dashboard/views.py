from django.shortcuts import render
import requests
from datetime import datetime

COE_API = "https://data.gov.sg/api/action/datastore_search?resource_id=d_69b3380ad7e51aff3a7dcc84eba52b8a&limit=5000"

def to_int(value):
    try:
        return int(str(value).replace(',', ''))
    except:
        return 0

def index(request):
    res = requests.get(COE_API).json()
    records = res.get("result", {}).get("records", [])

    # Filter Category D only
    cat_d_records = [
        {
            "date": datetime.strptime(r["month"], "%Y-%m"),
            "premium": to_int(r.get("premium", 0)),
            "quota": to_int(r.get("quota", 0)),
            "bids": to_int(r.get("bids_received", 0)),
        }
        for r in records
        if r.get("vehicle_class") == "Category D" and "month" in r
    ]
    cat_d_records.sort(key=lambda x: x["date"])

    # Compute PQP (3-month moving average)
    for i, r in enumerate(cat_d_records):
        if i >= 2:
            r["pqp"] = round(
                (cat_d_records[i]["premium"] +
                 cat_d_records[i-1]["premium"] +
                 cat_d_records[i-2]["premium"]) / 3
            )
        else:
            r["pqp"] = 0

    data = [
        {
            "date": r["date"].strftime("%Y-%m"),
            "premium": r["premium"],
            "quota": r["quota"],
            "bids": r["bids"],
            "pqp": r["pqp"],
        }
        for r in cat_d_records
    ]

    context = {"records": data}
    return render(request, "dashboard/index.html", context)
