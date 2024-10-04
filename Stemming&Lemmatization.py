import pandas as pd
import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import string
import nltk

nltk.download('stopwords')


def remove_html_tags(input_file_path, output_file_path):
    stop_words = set(stopwords.words('english'))
    data = pd.read_csv(input_file_path)

    for column in data.columns:
        data[column] = data[column].apply(lambda x: clean_text(x, stop_words))

    data.to_csv(output_file_path, index=False)


def clean_text(text, stop_words):
    # Remove HTML tags using BeautifulSoup
    text = BeautifulSoup(text, "html.parser").get_text()
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Remove stop words
    text = ' '.join([word for word in text.split() if word.lower() not in stop_words])
    return text


# Main
input_file = "C:\\Users\\trear\\Downloads\\extracted_data.csv"
output_file = "C:\\Users\\trear\\Downloads\\Y2S2\\Modified_Data.csv"

remove_html_tags(input_file, output_file)

# Example to read the modified file
modified_data = pd.read_csv(output_file)
print(modified_data.head())









