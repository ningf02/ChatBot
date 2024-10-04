def sort_by_name(csv_file):
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)
        sorted_rows = sorted(rows, key=lambda row: row[1])
        return sorted_rows
