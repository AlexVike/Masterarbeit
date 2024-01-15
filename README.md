# Masterarbeit

- [00-Auswertung](https://github.com/AlexVike/Masterarbeit/tree/main/Auswertung)
- [01-Masterarbeit Code](https://github.com/AlexVike/Masterarbeit/tree/main/Masterarbeit%20Code)
- [02-Vorstudie](https://github.com/AlexVike/Masterarbeit/tree/main/Vorstudie)

Die Ordner und die Deliverables werden nun einzeln beschrieben:

## 00-Auswertung
Der vorliegende Ordner enthält die statistische Analyse, die in der Masterarbeit verwendet wurde. Die detaillierten Ergebnisse und die dazugehörige Diskussion sind in den entsprechenden Abschnitten 'Ergebnisse' und 'Diskussion' der Arbeit zu finden.

- Ordner 1-6: Aufteilung der Datensätze der Subskalen des ```motivated strategies for learning questionnaire```. Deskreptive Statistiken der Subskalen.
- 7. Gesamtauswertung: Auswertung des abhängigen und unabhängigen t-Tests. Zusammenfassende deskreptive Statistik.
- Code: Programmatische Lösung der statistischen Analyse.
- POS LC NC: Visuelle Analyse des ```part-of-speech tagging```.
- Topic Modelling: Visuelle Analyse des ```Topic Modelling```.
- Wordcloud LC NC: Visuelle Analyse der ```Wordcloud```.

## 01-Masterarbeit Code
In diesem Ordner ist die Umsetzung der Chatbots zu finden. Zusätzlich kann die Datenbank beobachtet werden die in diesem Projekt verwendet wurde.

- Datenbank.db: Datenbank des Projektes.
- chatbot_tel_erste_session.py: Mit dieser Datei kann der Chatbot initialisiert werden.
- gpt_lerncoach_neutral.py: Funktionen auf denen die Chatbots zugreifen. OpenAI API Key muss eingesetzt werden bevor es gestartet wird.
- messages.py: Vorgefertigte Antworten im Chatverlauf.
-  SQLite Datenbanktabellen Beschreibung

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


## 02-Anforderungsspezifizierung
In diesem Ordner sind die Deliverables des Anforderungsdokument, der Hierarchischen Task Analyse und der Personas, User stories, Use-cases zu finden. In diesem Teil der Arbeit ist die Basis der Anforderungserhebung spezifiziert worden.
- Personas, User stories, Use-cases: Beinhaltet eine PDF-Datei mit allen Personas, User stories und Use-cases.
- Hierarchische Taskanalye: Beihnaltet die Schlüsseltasks und die Taskanalyse.
- Anforderungsdokument: Beinhaltet das Anforderungsdokument welches auf der Anforderungserhebung und der restlichen Anforderungsspezifizierung basiert. Aus diesem wird ersichtlich, welche Features die App beinhalten sollte. Jedoch sind nicht alle Anforderungen des Dokumentes übernommen worden. Die Gründe dafür sind im Bericht zu finden.

## 03-Iterativer Designprozess
In diesem Ordner sind drei Videos zu den unterschiedlichen Prototypen zu finden. In diesem Projekt wurden ein Paper-Prototype, ein Medium-Fidelity-Prototype und ein High-Fidelity-Prototype erstellt. Zusätzlich ist der High-Fidelity-Prototype anhand der UE-Tests verbessert worden. Genaue Erklärungen und Bilder der Prototypen sind im Bericht zu finden.
- Low-Fidelity-Prototype: Beinhaltet das Video des Prototypen.
- Medium-Fidelity-Prototype: Beinhaltet das Video des Prototypen.
- High-Fidelity-Prototype: Beinhaltet das Video des Prototypen.

## 04-Summative Evaluation
In diesem Ordner ist die Evaluation des High-Fidelity-Prototype zu finden. Mithilfe dieser Auswertung ist der High-Fidelity-Prototype verbessert worden. Mehr dazu in dem Bericht in 00-General.
- Evaluation des Prototypen: Beinhaltet die Vorabfragebögen der Teilnehmer der UE-Tests. Daneben ist exemplarisch eine Einverständniserklärung hochgeladen worden, die die Teilnehmer unterschrieben haben. Beobachter, Notizen und die Testunterlagen der UE-Tests sind hier zu finden. Diese zeigen die Vorbereitung auf die Tests und welche Notizen dabei entstanden sind. Mit diesen Notizen und den gesammelten Daten ist die Auswertung entstanden, die hier hochgeladen wurde.
