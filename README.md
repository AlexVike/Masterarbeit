# Masterarbeit

- [00-Auswertung](https://github.com/AlexVike/Masterarbeit/tree/main/Auswertung)
- [01-Masterarbeit Code](https://github.com/AlexVike/Masterarbeit/tree/main/Masterarbeit%20Code)
- [02-Vorstudie](https://github.com/AlexVike/Masterarbeit/tree/main/Vorstudie)


## 00-Auswertung
Der vorliegende Ordner enthält die statistische Analyse, die in der Masterarbeit verwendet wurde. Die detaillierten Ergebnisse und die dazugehörige Diskussion sind in den entsprechenden Abschnitten 'Ergebnisse' und 'Diskussion' der Arbeit zu finden.

- Ordner 1-6: Aufteilung der Datensätze der Subskalen des ```motivated strategies for learning questionnaire```. Deskreptive Statistiken der Subskalen.
- Ordner 7. Gesamtauswertung: Auswertung des abhängigen und unabhängigen t-Tests. Zusammenfassende deskreptive Statistik.
- Code: Programmatische Lösung der statistischen Analyse.
- POS LC NC: Visuelle Analyse des ```part-of-speech tagging```.
- Topic Modelling: Visuelle Analyse des ```Topic Modelling```.
- Wordcloud LC NC: Visuelle Analyse der ```Wordcloud```.

## 01-Masterarbeit Code
Dieser Ordner enthält alle notwendigen Dateien zur Implementierung und zum Betrieb des Chatbots, der im Rahmen der Masterarbeit entwickelt wurde. Er bietet zudem Zugriff auf die Datenbank.

- Datenbank.db: Datenbank des Projektes.
- chatbot_tel_erste_session.py: Mit dieser Datei kann der Chatbot initialisiert werden.
- gpt_lerncoach_neutral.py: Funktionen auf denen die Chatbots zugreifen. OpenAI API Key muss eingesetzt werden bevor es gestartet wird.
- messages.py: Vorgefertigte Antworten im Chatverlauf.

  Die SQLite-Datenbank besteht aus sechs Tabellen, die speziell für die Verwaltung von Chat-Sitzungen und Benutzerinteraktionen konzipiert sind. Hier ist eine detaillierte Beschreibung jeder Tabelle:
  
  - **Zweite_S**: 
    - **Zweck**: Speicherung von Daten der zweiten Session.
    - **Felder**: Chat-ID, Informationen über Teilnehmende, Phase der Interaktion, Gruppeninformationen, Zeitstempel.
  
  - **Chat_end**: 
    - **Zweck**: Erfassung von vorzeitigen Chat-Abbrüchen.
    - **Felder**: Chat-ID, Zeitstempel des Abbruchs.
  
  - **Fortschritte**: 
    - **Zweck**: Nachverfolgung von Fortschritten in der zweiten Sitzung.
    - **Felder**: Chat-ID, Beschreibung des Fortschritts, Zeitstempel.
  
  - **Master_Test**: 
    - **Zweck**: Speicherung der normalen Chatverläufe.
    - **Felder**: Chat-ID, Nutzername (Human), Chatbot-Name, Phase der Interaktion, Gruppenzugehörigkeit, Zeitstempel.
  
  - **Zusammenfassung_chat**: 
    - **Zweck**: Bereitstellung von Zusammenfassungen von GPT-3.5.
    - **Felder**: Chat-ID, Zusammenfassungstext, Bewertung der Phase, Zeitstempel.
  
  - **Anmeldung_zweite_S**: 
    - **Zweck**: Speicherung der Chatverläufe der zweiten Session.
    - **Felder**: Anmeldedetails, Chat-ID, Zeitstempel.


## 02-Vorstudie
Dieser Ordner enthält die Wizard-of-Oz Vorstudie.

- Auswertung: Auswertung der Vorstudie.
- Vorstudie 1-5: Chatverläufe der Vorstudie.
- Vorstudie_Manual.docx: Manual der Vorstudie für den Wizard.

# Installationsanleitung für die Studie

Befolgen Sie diese Schritte, um die Chatbots für das Masterarbeitsprojekt einzurichten und zu betreiben.

## Voraussetzungen

- Stellen Sie sicher, dass Python 3.x auf Ihrem System installiert ist.

## Installation

### Schritt 1: OpenAI API-Schlüssel besorgen

- Registrieren Sie sich bei [OpenAI](https://openai.com/) und generieren Sie einen API-Schlüssel.

### Schritt 2: Erforderliche Python-Bibliotheken installieren

Öffnen Sie Ihre Kommandozeile und führen Sie folgende Befehle aus:

```bash
pip install openai
pip install sqlite3
pip install aiohttp
pip install aiogram
```
### Schritt 3: Telegram-Bot erstellen
Schreiben Sie mit dem [BotFather](https://telegram.me/BotFather) auf Telegram, um einen neuen Bot zu erstellen und erhalten Sie den Token.

### Schritt 4: API-Schlüssel und Token
Fügen Sie Ihren OpenAI API-Schlüssel im Code bei `openai.api_key = "IHR_API_SCHLÜSSEL"` ein.
Fügen Sie Ihren Telegram Token im Code bei `TOKEN = "IHR_Token"` ein.

### Schritt 5: Datenbank vorbereiten
Stellen Sie sicher, dass die Datei `Datenbank.db` existiert und das erforderliche Schema aufweist.

### Schritt 6: Chatbot ausführen
Führen Sie das Hauptskript aus, um den Chatbot zu starten:

```bash
python chatbot_tel_erste_session.py
```
