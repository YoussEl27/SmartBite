# SmartBite
SmartBite ist eine moderne, KI-gestützte Webanwendung zur automatisierten Kalorien- und Nährwerterkennung von Mahlzeiten. Sie richtet sich speziell an Sportler:innen und gesundheitsbewusste Nutzer:innen, die ihren Ernährungsplan einfach und zeitsparend tracken möchten. Der Kern des Systems ist die Kombination eines Large Language Models (LLM) zur Bildbeschreibung und einer externen API zur Nährwertabfrage.

- Projektstatus: Funktionaler Prototyp (MVP)

- Letzte Aktualisierung: 05.09.2025

- Autor: Youssef Elkettani

## Architekturübersicht
![img.png](img.png)

## Dienste

### Frontend (Streamlit):
   - Rolle: Stellt die nutzerzentrierte Weboberfläche bereit.
   - Funktionalität: Bild-Upload, Anzeige der analysierten Nährwerte, Interaktion mit dem Backend.

### KI-Service (phi-4-multimodal):
   - Rolle: Hochpräzise Bildanalyse und -beschreibung.
   - Funktionalität: Empfängt das hochgeladene Bild und generiert eine äußerst detaillierte und akkurate textuelle Beschreibung (z.B. "Eine Portion Spaghetti Bolognese mit frischem Basilikum und Parmesan auf einem weißen Teller").
### Externe API (OpenFoodFacts):
  - Rolle: Bereitstellung der Nährwertdaten.
### Backend-Service (FastAPI):
  - Rolle: Zentrale Geschäftslogik und Nutzerdatenverwaltung.
### Datenbank (PostgresSQL):
  - Rolle: Persistente Speicherung von Anwendungsdaten.
### Deployment (Kubernetes & GitLab CI/CD):
  - Rolle: Automatisierte Bereitstellung und Skalierung der Anwendung.

## ProjektStruktur
```
   youssef-elkettani/
   ├── .devcontainer/
   ├── app/
   │   ├── pages/
   │   ├── app.py
   │   ├── Pics/
   │   ├── Dockerfile
   │   ├── requirements.txt
   │   └── uber-raw-data-sep14.csv
   ├── Backend/
   │   ├── __init__.py
   │   ├── auth.py
   │   ├── crud.py
   │   ├── database.py
   │   ├── Dockerfile
   │   ├── main.py
   │   ├── models.py
   │   ├── requirements.txt
   │   └── schemas.py
   ├── deploy/
   │   ├── backend/
   │   ├── frontend/
   │   └── storage/
   ├── tests/
   │   ├── test_backend.py
   │   └── test_frontend.py
   ├── .env
   ├── .gitignore
   ├── gitlab-ci.yml
   ├── docker-compose.yml
   ├── img.png
   ├── README.md
   └── visualization.png
```

## Docker Compose
- Die Datei docker-compose.yml definiert alle Services:
  - frontend: Streamlit
  - backend : FastAPI
  - db: PostgresSQL Datenbank

##GitLab CI/CD
- Die .gitlab-ci.yml Datei beschreibt die CI/CD-Pipeline, mit der das Projekt gebaut und getestet wird. Docker-Images werden automatisch erstellt und in die GitLab Registry geladen und deploy-Dateien ausführen.

##Anwendung lokal ausführen
   ### Voraussetzungen
- Docker und Docker Compose installiert
   ### Starten
- ```sh
    docker-compose up --build
    ```
   ### Zugriff
- --------------------------------------------

## Hinweise zur KI-Unterstützung
Zur Qualitätssicherung und sprachlichen Korrektur wurde KI eingesetzt. Die KI hat insbesondere bei der Verbesserung von Dokumentationsabschnitten geholfen, wurde aber nicht zur Codegenerierung verwendet.

## Lizenz
Dieses Projekt dient ausschließlich Studien- und Lernzwecken. Eine kommerzielle Nutzung ist nicht vorgesehen.
