from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Import functions from textClassifier.py
from textClassifier import predict_tag, load_classifier_and_vectorizer
vivado = False
# Import the UserQueryProcessor class
from user_query import UserQueryProcessor
from languageDetection import langD


# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS

app.secret_key = 'your_secret_key'

try:
    output_df = pd.read_csv('output3.csv', encoding='utf-8')  # Try reading with UTF-8 first
except UnicodeDecodeError:
    output_df = pd.read_csv('output3.csv', encoding='ISO-8859-1')  # Fallback to ISO-8859-1

# Load the classifier and vectorizer for text classification
classifier_path = 'classifier.joblib'
vectorizer_path = 'vectorizer.joblib'
trained_classifier, trained_vectorizer = load_classifier_and_vectorizer(classifier_path, vectorizer_path)

# Initialize the TF-IDF Vectorizer for comparing user query against answers
answer_vectorizer = TfidfVectorizer()


def find_most_similar_answer(user_query, output_df, trained_vectorizer, trained_classifier, answer_vectorizer):
    """
    Finds the most similar answer for a user query based on TF-IDF cosine similarity.

    :param user_query: The user's query as a string.
    :param output_df: DataFrame containing possible answers, indexed by tags.
    :param trained_vectorizer: The trained TF-IDF vectorizer for transforming queries.
    :param trained_classifier: The trained classifier for predicting the tag of a query.
    :param answer_vectorizer: The TF-IDF vectorizer for comparing user query against answers.
    :return: The most similar answer as a string.
    """
    # Predict the tag for the user query
    predicted_tag = predict_tag(user_query, trained_vectorizer, trained_classifier)

    # Select the column corresponding to the predicted tag
    answers_column = output_df[predicted_tag].dropna()  # Drop any missing values

    # Transform all answers under the tag to the same vector space
    answers_tfidf = answer_vectorizer.fit_transform(answers_column)

    # Transform the user query to the same vector space
    query_tfidf = answer_vectorizer.transform([user_query])
    print(query_tfidf)
    # Compute cosine similarity between query and all answers under the tag
    cosine_similarities = cosine_similarity(query_tfidf, answers_tfidf).flatten()

    # Find the index of the answer with the highest similarity
    most_similar_index = cosine_similarities.argmax()

    # Get the most similar answer
    most_similar_answer = answers_column.iloc[most_similar_index]

    return most_similar_answer

# Modify the existing route to use the new function
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        word1 = "vivado"
        data = request.get_json()
        user_query = data['userMessage']

        lang = langD.find_language(user_query)
        if lang == 'null':
            print("Language not detected")
        elif lang != "en":
            user_query = langD.translate_arr(user_query, 0, 'null')

        # Call the new function to find the most similar answer
        most_similar_answer = find_most_similar_answer(user_query, output_df, trained_vectorizer, trained_classifier, answer_vectorizer)
        if(lang != 'en'):
            most_similar_answer = langD.translate_arr(most_similar_answer, 1, lang)
        # Return the most similar answer
        if word1 in user_query:
            response_message = f"We think that you may be using inappropriate language, please try again"
        else:
            response_message = f"{most_similar_answer}"
        return jsonify({"responseMessage": response_message})

    # This part is for handling GET requests or other purposes. Adjust as needed.
    return '''
        <form method="post" autocomplete="off">
            Query: <input type="text" name="query" autocomplete="off"><br>
            <input type="submit" value="Submit">
        </form>
    '''


if __name__ == '__main__':
    app.run(debug=True)
