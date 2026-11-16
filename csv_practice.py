"""
Reflection Answers:
1. Complete ETL pipeline vs Excel: Python allows for automated, repeatable 
processing of large datasets without manual formula dragging or formatting risks. 
Excel excels at quick ad-hoc analysis, visual charting, and human-in-the-loop 
data entry, whereas Python is superior for robust batch processing, complex 
conditional logic, and pipeline scalability.
2. Real business process for append-mode logs: An e-commerce transaction or 
API request logger. Append mode is the right tool because every new event 
must be recorded chronologically without overwriting historical logs, maintaining 
an immutable audit trail of system activity over time.
"""

import csv
from datetime import datetime

file_path = "data/sales.csv"

# EXERCISE 1 & 2: Read and print raw rows
print("=== EXERCISE 2: Raw Rows ===")
with open(file_path, mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# EXERCISE 3: Skip the header
print("\n=== EXERCISE 3: Skip Header ===")
with open(file_path, mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    print(f"Header: {header}")
    for row in reader:
        print(row)

# EXERCISE 4: Compute totals
print("\n=== EXERCISE 4: Compute Totals ===")
overall_total = 0.0
with open(file_path, mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        product = row[0]
        price = float(row[1])
        quantity = int(row[2])
        line_total = price * quantity
        overall_total += line_total
        print(f"{product}: {quantity} units × ${price:.2f} = ${line_total:.2f}")

print(f"Overall Total Revenue: ${overall_total:.2f}")

# EXERCISE 5: Filter and write cleaned report
print("\n=== EXERCISE 5: Filter and Write ===")
original_count = 0
written_count = 0

with open(file_path, mode="r", encoding="utf-8") as infile, \
     open("data/cleaned.csv", mode="w", newline="", encoding="utf-8") as outfile:
    
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    # Write new header
    writer.writerow(["Product", "Price", "Qty", "Total"])
    
    next(reader)  # skip input header
    for row in reader:
        original_count += 1
        product = row[0]
        price = float(row[1])
        quantity = int(row[2])
        line_total = price * quantity
        
        if line_total > 100:
            writer.writerow([product, f"{price:.2f}", quantity, f"{line_total:.2f}"])
            written_count += 1

print(f"Original rows: {original_count}, Written rows (> $100): {written_count}")

# EXERCISE 6: csv.DictReader
print("\n=== EXERCISE 6: DictReader ===")
# csv.reader accesses columns by integer index (e.g., row[0]), which is concise 
# but fragile if column positions change. csv.DictReader maps columns to dictionary keys 
# (e.g., row["product"]), making code self-documenting and resilient to column reordering.

with open(file_path, mode="r", encoding="utf-8") as f:
    dict_reader = csv.DictReader(f)
    dict_total = 0.0
    for row in dict_reader:
        p = row["product"]
        pr = float(row["price"])
        qty = int(row["quantity"])
        dict_total += pr * qty
print(f"DictReader Computed Total Revenue: ${dict_total:.2f}")

# EXERCISE 7: Sales summary by product
print("\n=== EXERCISE 7: Sales Summary by Product ===")
summary = {}
with open(file_path, mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        prod = row["product"]
        rev = float(row["price"]) * int(row["quantity"])
        summary[prod] = summary.get(prod, 0.0) + rev

for prod in sorted(summary.keys()):
    print(f"{prod}: ${summary[prod]:.2f}")

# EXERCISE 8: Append mode log
print("\n=== EXERCISE 8: Append Mode Log ===")
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_line = f"[{current_time}] Run completed. Total Revenue: ${overall_total:.2f}\n"

with open("data/run_log.txt", mode="a", encoding="utf-8") as log_file:
    log_file.write(log_line)

print("Log entry appended to data/run_log.txt successfully.")