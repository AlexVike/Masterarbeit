import sqlite3
import pandas as pd
import gensim
from gensim import corpora
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

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

def analyze_topics_for_group(df, group_name):
    """Themenanalyse für eine bestimmte Gruppe und Erzeugung von Wortwolken."""
    df_group = df[df['Gruppe'] == group_name]
    processed_msgs = df_group['processed_msgs'].tolist()
    dictionary = corpora.Dictionary(processed_msgs)
    corpus = [dictionary.doc2bow(text) for text in processed_msgs]
    lda_model = gensim.models.LdaMulticore(corpus, num_topics=5, id2word=dictionary, passes=10, workers=2)

    for idx, topic in lda_model.print_topics(-1):
        print(f"\nGroup {group_name} - Topic: {idx}")
        print(f"Words: {topic}")
        topic_words = process_topic(topic)
        file_path = f'wordcloud_{group_name}_topic_{idx}.png'  # Dateipfad anpassen
        generate_wordcloud(topic_words, f"Group {group_name} - Topic {idx}", file_path)
        
def process_topic(topic):
    """Verarbeitet die Topic-Strings und extrahiert Wörter mit ihren Gewichtungen."""
    words = {}
    for part in topic.split(" + "):
        weight, word = part.split("*")
        words[word.strip(' "')] = float(weight)
    return words


def generate_wordcloud(topic_words, title, file_path):
    """Erzeugt eine Wortwolke aus den Topic-Wörtern."""
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(topic_words)
    
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
    chat_ids = [
        35653198, 874105911, 2144953432, 6382250267, 6622741485, 6659747133, 
        6673501390, 6688206975, 6711193461, 6714094450, 6872463735, 6872950062, 
        6913598906, 6920468126, 6663633720, 494632552, 784733263, 909202635, 
        1273781158, 1470949664, 5843421327, 6133516300, 6170880041, 6536374262, 
        6699389447, 6718145485, 6749559140, 6754172146, 6877146415, 6965940833
    ]

    # Daten abfragen
    query = f"SELECT * FROM Master_Test WHERE ChatID IN ({','.join(['?']*len(chat_ids))})"
    df = pd.read_sql_query(query, conn, params=chat_ids)

    # Schließen der Datenbankverbindung
    conn.close()

    # Vorverarbeitung der Nachrichten
    df['processed_msgs'] = df['Human'].apply(preprocess)

    # Durchführen der Themenanalyse für jede Gruppe
    analyze_topics_for_group(df, 'LC')
    analyze_topics_for_group(df, 'NC')

if __name__ == '__main__':
    main()