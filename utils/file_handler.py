import csv
import os
from config.settings import DATA_DIR

# =========================
# DIRECTORY SETUP
# =========================
def ensure_data_directory():
    os.makedirs(DATA_DIR, exist_ok=True)


# =========================
# FILE CHECK
# =========================
def ensure_file(file_path, fieldnames=None):
    """
    Ensures file exists. If missing and fieldnames provided,
    creates file with header row.
    """
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            if fieldnames:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()


# =========================
# READ CSV
# =========================
def read_csv(file_path):
    ensure_file(file_path)

    with open(file_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        # Handle empty file safely
        if reader.fieldnames is None:
            return []

        return list(reader)


# =========================
# WRITE CSV (overwrite mode)
# =========================
def write_csv(file_path, data, fieldnames):
    ensure_file(file_path, fieldnames)

    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        if data:
            writer.writerows(data)


# =========================
# APPEND SINGLE ROW (IMPORTANT ADDITION)
# =========================
def append_csv(file_path, row, fieldnames):
    ensure_file(file_path, fieldnames)

    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(row)