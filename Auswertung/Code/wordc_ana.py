import sqlite3
import pandas as pd
from wordcloud import WordCloud
import gensim
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk
import re

# Stellen Sie sicher, dass die NLTK-Pakete heruntergeladen sind
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('stopwords')

# Initialisieren des Lemmatizers
lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def preprocess(text):
    """Entfernen von Sonderzeichen und Satzzeichen, Lemmatisierung und Entfernung von Stopwörtern."""
    
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in stopwords.words('german'):
            lemmatized_token = lemmatizer.lemmatize(token, get_wordnet_pos(token))
            result.append(lemmatized_token)
    return result

def generate_wordcloud(text, title, file_path):
    """Erzeugt eine Wortwolke aus den Textdaten."""
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(text))
    
    # Anzeigen der Wortwolke
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(title)
    plt.axis("off")
    
    # Speichern der Wortwolke als Bild
    plt.savefig(file_path)
    plt.close()

def main():
    # Datenbankverbindung herstellen
    conn = sqlite3.connect('C:/Users/Alexa/Documents/MA/Masterarbeit-Alexander-Vikete/Auswertung/Code/Datenbank.db')

    # Liste der ChatIDs
    chat_ids_lc = [  # ChatIDs für Gruppe LC
        35653198, 874105911, 2144953432, 6382250267, 6622741485, 6659747133, 
        6673501390, 6688206975, 6711193461, 6714094450, 6872463735, 6872950062, 
        6913598906, 6920468126, 6663633720
    ]
    
    chat_ids_nc = [  # ChatIDs für Gruppe NC
        494632552, 784733263, 909202635, 1273781158, 1470949664, 5843421327, 
        6133516300, 6170880041, 6536374262, 6699389447, 6718145485, 6749559140, 
        6754172146, 6877146415, 6965940833
    ]

    # Daten abfragen für Gruppe LC
    query_lc = f"SELECT * FROM Master_Test WHERE ChatID IN ({','.join(['?']*len(chat_ids_lc))})"
    df_lc = pd.read_sql_query(query_lc, conn, params=chat_ids_lc)

    # Daten abfragen für Gruppe NC
    query_nc = f"SELECT * FROM Master_Test WHERE ChatID IN ({','.join(['?']*len(chat_ids_nc))})"
    df_nc = pd.read_sql_query(query_nc, conn, params=chat_ids_nc)

    # Schließen der Datenbankverbindung
    conn.close()

    # Vorverarbeitung der Nachrichten für Gruppe LC
    df_lc['processed_msgs'] = df_lc['Human'].apply(preprocess)

    # Vorverarbeitung der Nachrichten für Gruppe NC
    df_nc['processed_msgs'] = df_nc['Human'].apply(preprocess)

    # Erzeugung der Word Cloud für Gruppe LC
    all_text_lc = df_lc['processed_msgs'].sum()
    generate_wordcloud(all_text_lc, 'Word Cloud for LC', 'wordcloud_lc.png')

    # Erzeugung der Word Cloud für Gruppe NC
    all_text_nc = df_nc['processed_msgs'].sum()
    generate_wordcloud(all_text_nc, 'Word Cloud for NC', 'wordcloud_nc.png')

if __name__ == '__main__':
    main()