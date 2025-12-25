import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_existing_titles(file_path):
    full_path = os.path.join(BASE_DIR, file_path)

    titles = []
    with open(full_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            titles.append(row["title"].lower())

    return titles
