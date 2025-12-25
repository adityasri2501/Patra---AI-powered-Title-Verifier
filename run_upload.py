from core.upload_titles_firestore import upload_titles

files = [
    ("data/TestExcel.xls", "TEST_1"),
    ("data/TestExcel(1).xls", "TEST_2"),
    ("data/TestExcel(2).xls", "TEST_3"),
    ("data/TestExcel(3).xls", "TEST_4"),
    ("data/TestExcel(4).xls", "TEST_5"),
    ("data/TestExcel(5).xls", "TEST_6"),
]

for file, name in files:
    print(f"Uploading {file}")
    upload_titles(file, name)
