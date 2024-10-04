def top_20_common(sorted_data):
    column_values = [row[1] for row in sorted_data]
    value_counts = Counter(column_values)
    top_20_common = value_counts.most_common(20)
    return top_20_common
