from app import app
from datetime import datetime
import csv
import os


def export_csv(ok):
    d = os.path.join(app.root_path, "data.csv")
    with open(d, "w", encoding="utf-8")as f:
        writer = csv.DictWriter(f, fieldnames=["id", "customer_name", "address", "created_date", "money", "phone",
                                               "id_number", "passbook_type_id", "active"])
        writer.writeheader()
        for x in ok:
            writer.writerow(x)
    return d
