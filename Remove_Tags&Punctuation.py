import pandas as pd
import csv
import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import string
import nltk

nltk.download('stopwords')


def remove_html_tags(input_file_path, output_file_path):
    # Open the original CSV file for reading
    stop_words = set(stopwords.words('english'))
    with open(input_file_path, 'r', newline='', encoding="utf-8") as input_file:
        # Open the new CSV file for writing
        with open(output_file_path, 'w', newline='', encoding="utf-8") as output_file:
            # Create CSV reader and writer objects
            csv_reader = csv.reader(input_file)
            csv_writer = csv.writer(output_file)

            # Iterate through the rows in the original file
            for row in csv_reader:
                # Apply replacements and remove HTML tags to each cell in the row
                modified_row = []

                for cell in row:
                    # Remove HTML tags using regular expression
                    cell = re.sub('<[^<]+?>', '', cell)
                    # Remove punctuation
                    cell = cell.translate(str.maketrans('', '', string.punctuation))
                    # Remove stop words
                    cell = ' '.join([word for word in cell.split() if word.lower() not in stop_words])

                    # Apply other replacements
                    modified_row.append(cell)

                # Write the modified row to the new CSV file
                csv_writer.writerow(modified_row)


# Everthing below this is for testing purposes and must be deleted after testing completed

# Path to your CSV file
input_file = "C:\\Users\\trear\\Downloads\\extracted_data.csv"
output_file = "C:\\Users\\trear\\Downloads\\Y2S2\\Modified_Data.csv"

remove_html_tags(input_file, output_file)
# Open the modified CSV file for reading
with open(output_file, 'r', newline='', encoding="utf-8") as modified_file:
    # Create a CSV reader object
    csv_reader = csv.reader(modified_file)

    # Print each row in the modified CSV file
    for row in csv_reader:
        print(row)
