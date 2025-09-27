import sqlite3
import csv
import os

# Paths
data_dir = "FoodData_Central_branded_food_csv_2025-04-24"
db_path = "foods.db"

# Remove old DB if exists
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

def import_csv(csv_file, table_name):
    print(f"Importing {csv_file}...")
    file_path = os.path.join(data_dir, csv_file)
    with open(file_path, newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        placeholders = ",".join("?" * len(headers))
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
        cur.execute(f"CREATE TABLE {table_name} ({', '.join([h + ' TEXT' for h in headers])})")
        batch = []
        for i, row in enumerate(reader, 1):
            batch.append(row)
            if len(batch) >= 5000:  # insert in chunks
                cur.executemany(f"INSERT INTO {table_name} VALUES ({placeholders})", batch)
                batch.clear()
            if i % 50000 == 0:
                print(f"  {i} rows...")
        if batch:
            cur.executemany(f"INSERT INTO {table_name} VALUES ({placeholders})", batch)
    conn.commit()
    print(f"✅ Finished {table_name}")

# Import key tables
import_csv("food.csv", "food")
import_csv("branded_food.csv", "branded_food")
import_csv("food_nutrient.csv", "food_nutrient")
import_csv("nutrient.csv", "nutrient")

# Indexes for speed
cur.execute("CREATE INDEX idx_food_desc ON food(description)")
cur.execute("CREATE INDEX idx_foodnutr_foodid ON food_nutrient(fdc_id)")
cur.execute("CREATE INDEX idx_foodnutr_nutrientid ON food_nutrient(nutrient_id)")
conn.commit()
conn.close()

print("🎉 Database ready: foods.db")
