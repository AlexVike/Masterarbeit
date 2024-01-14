from textblob_de import TextBlobDE as TextBlob
import sqlite3
import pandas as pd

def sentiment_analysis(df, group_name):
    df_group = df[df['Gruppe'] == group_name].copy()  # Erstellen einer Kopie des gefilterten DataFrames
    df_group['Sentiment'] = df_group['Human'].apply(lambda text: TextBlob(text).sentiment.polarity)
    avg_sentiment = df_group['Sentiment'].mean()
    print(f"Average sentiment for group {group_name}: {avg_sentiment}")


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

    # Sentimentanalyse für jede Gruppe durchführen
    sentiment_analysis(df, 'LC')
    sentiment_analysis(df, 'NC')

if __name__ == '__main__':
    main()
