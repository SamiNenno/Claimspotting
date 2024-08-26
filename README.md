# Claimspotting

## Über das Projekt

Claimspotting ist ein Teil der [Public Interest AI](https://publicinterest.ai/) Forschungsgruppe am Humboldt Institut für Internet und Gesellschaft (HIIG). Das Claimspotting-Tool soll Faktenchecker:innen dabei unterstützen, Telegram-Kanäle zu überwachen und Inhalte nach Kriterien zu analysieren, die im Kontext von Desinformation relevant sind. Alle maschinellen Lernmodelle können auf Huggingface abgerufen werden: [Huggingface - Sami92](https://huggingface.co/Sami92).

## Projektstruktur

Das Projekt besteht aus vier Hauptkomponenten, die jeweils in einem separaten Ordner organisiert sind:

### [Django_Interface](./Django_Interface)

Dieses Modul dient der Erstellung einer API mit Django. Die API ermöglicht es, auf die Datenbank zuzugreifen, Abfragen zu stellen und Statistiken über die gesammelten Daten zu erhalten.

### [ML_Interface](./ML_Interface)

Dieses Modul dient der Kennzeichnung und Annotation von Telegram-Beiträgen mit maschinellen Lernklassifikatoren und Einbettungsmodellen. Es wird verwendet, um die Beiträge nach relevanten Kriterien zu analysieren.

### [Tele_Crawler](./Tele_Crawler)

Dieses Modul crawlt regelmäßig Daten von Telegram-Kanälen, die für die Verbreitung von Desinformation bekannt sind. Die gesammelten Daten werden in der Datenbank gespeichert und zur weiteren Analyse bereitgestellt.

### [Tele_Stats](./Tele_Stats)

Dieses Modul aktualisiert die statistischen Aspekte der Datenbank, indem es die gesammelten Daten analysiert und aggregierte Statistiken erstellt. Diese Statistiken können über die API abgefragt werden.

---

# Claimspotting

## About the Project

Claimspotting is part of the [Public Interest AI](https://publicinterest.ai/) research group at the Humboldt Institute for Internet and Society (HIIG). The Claimspotting tool is designed to assist fact-checkers by monitoring Telegram channels and analysing content according to criteria that are relevant in the context of misinformation. All machine learning models can be accessed on Huggingface: [Huggingface - Sami92](https://huggingface.co/Sami92).

## Project Structure

The project is organised into four main components, each contained within its own directory:

### [Django_Interface](./Django_Interface)

This module is responsible for creating an API using Django. The API allows access to the database, querying of data, and retrieval of statistics about the collected data.

### [ML_Interface](./ML_Interface)

This module is used for tagging and annotating Telegram posts with machine learning classifiers and embedding models. It is used to analyse posts according to relevant criteria.

### [Tele_Crawler](./Tele_Crawler)

This module regularly scrapes data from Telegram channels known for spreading misinformation. The collected data is stored in the database and made available for further analysis.

### [Tele_Stats](./Tele_Stats)

This module updates the statistical aspects of the database by analysing the collected data and creating aggregated statistics. These statistics can be queried through the API.
