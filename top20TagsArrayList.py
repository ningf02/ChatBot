from sortTagsByName import sort_by_name
from top_20_common_tags import top_20_common

csv_file = 'Tags5+.csv'
sorted_data = sort_by_name(csv_file)
if sorted_data:
    print("Sorted data based on the second column:")
    for row in sorted_data:
        print(row)
    top_20 = top_20_common(sorted_data)
    if top_20:
        print("Top 20 most common tags:")
        for tag, count in top_20:
            Top_20_list.append(tag)
            print(f"{tag}: {count}")
else:
    print("No data found.")
print(Top_20_list)
