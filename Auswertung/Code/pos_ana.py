import sqlite3
import pandas as pd
import nltk
from nltk import pos_tag
from collections import Counter
import matplotlib.pyplot as plt

# Stellen Sie sicher, dass die NLTK-Pakete heruntergeladen sind
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

def get_pos_statistics(texts):
    # Tokenisierung und POS-Tagging für jeden Text
    pos_statistics = []
    for text in texts:
        tokens = nltk.word_tokenize(text)
        pos_tags = pos_tag(tokens)
        pos_statistics.extend([tag for word, tag in pos_tags])

    # Zählen der Häufigkeit der POS-Tags
    pos_counts = Counter(pos_statistics)
    return pos_counts

def plot_pos_statistics(pos_counts, group_name):
    # Sortieren der POS-Tags nach Häufigkeit
    sorted_pos_counts = dict(sorted(pos_counts.items(), key=lambda item: item[1], reverse=True))

    # Extrahieren der POS-Tags und ihrer Häufigkeiten
    pos_tags = list(sorted_pos_counts.keys())
    frequencies = list(sorted_pos_counts.values())

    # Balkendiagramm erstellen
    plt.figure(figsize=(12, 6))
    plt.barh(pos_tags, frequencies)
    plt.xlabel('Häufigkeit')
    plt.ylabel('POS-Tag')
    plt.title(f'POS-Statistik für {group_name}')
    plt.gca().invert_yaxis()  # Umgekehrte Reihenfolge für bessere Lesbarkeit
    plt.show()

def main():
    # Datenbankverbindung herstellen
    conn = sqlite3.connect('C:/Users/Alexa/Documents/MA/Masterarbeit-Alexander-Vikete/Auswertung/Code/Datenbank.db')  # Pfad zur Datenbank anpassen

    # Liste der ChatIDs für LC und NC
    lc_chat_ids = [35653198, 874105911, 2144953432, 6382250267, 6622741485, 6659747133, 
                   6673501390, 6688206975, 6711193461, 6714094450, 6872463735, 6872950062, 
                   6913598906, 6920468126, 6663633720]
    
    nc_chat_ids = [494632552, 784733263, 909202635, 1273781158, 1470949664, 5843421327, 
                   6133516300, 6170880041, 6536374262, 6699389447, 6718145485, 6749559140, 
                   6754172146, 6877146415, 6965940833]

    # Daten abfragen für LC und NC
    lc_query = f"SELECT * FROM Master_Test WHERE ChatID IN ({','.join(['?']*len(lc_chat_ids))})"
    nc_query = f"SELECT * FROM Master_Test WHERE ChatID IN ({','.join(['?']*len(nc_chat_ids))})"
    
    df_lc = pd.read_sql_query(lc_query, conn, params=lc_chat_ids)
    df_nc = pd.read_sql_query(nc_query, conn, params=nc_chat_ids)

    # Schließen der Datenbankverbindung
    conn.close()

    # POS-Statistik für LC und NC
    lc_pos_statistics = get_pos_statistics(df_lc['Human'])
    nc_pos_statistics = get_pos_statistics(df_nc['Human'])

    # Visualisierung der POS-Statistik
    plot_pos_statistics(lc_pos_statistics, 'LC')
    plot_pos_statistics(nc_pos_statistics, 'NC')

if __name__ == '__main__':
    main()
