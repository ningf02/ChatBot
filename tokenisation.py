import pandas as pd


def tokenize_stackoverflow_text(text):
    words = text.split()

    df = pd.DataFrame({'Token': words})

    return df
