import pandas as pd


def load_titles_from_excel(file_path):
    """
    Robust loader for legacy PRGI Excel files.
    Handles: real Excel, CSV disguised as XLS, HTML tables.
    """

    # 1️⃣ Try Excel (openpyxl / xlrd)
    try:
        df = pd.read_excel(file_path)
        print(f"[INFO] Loaded as Excel: {file_path}")
    except Exception:
        # 2️⃣ Try CSV
        try:
            df = pd.read_csv(file_path)
            print(f"[INFO] Loaded as CSV: {file_path}")
        except Exception:
            # 3️⃣ Try HTML
            try:
                tables = pd.read_html(file_path)
                df = tables[0]
                print(f"[INFO] Loaded as HTML table: {file_path}")
            except Exception as e:
                raise ValueError(
                    f"❌ Unsupported or corrupt file format: {file_path}"
                ) from e

    print("Columns detected:", df.columns)

    titles = []

    # Assume first column contains title
    first_col = df.columns[0]

    for val in df[first_col]:
        title = str(val).strip().lower()
        if title and title != "nan":
            titles.append(title)

    return titles
