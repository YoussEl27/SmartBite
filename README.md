# SmartBite
SmartBite ist eine moderne, KI-gestützte Webanwendung zur automatisierten Kalorien- und Nährwerterkennung von Mahlzeiten. Sie richtet sich speziell an Sportler:innen und gesundheitsbewusste Nutzer:innen, die ihren Ernährungsplan einfach und zeitsparend tracken möchten. Der Kern des Systems ist die Kombination eines Large Language Models (phi-4-multimodal) zur Bildbeschreibung und einer externen API zur Nährwertabfrage.

- Projektstatus: Funktionaler Prototyp (MVP)

- Letzte Aktualisierung: 05.09.2025

- Autor: Youssef Elkettani

## Funktionen
- Benutzer können Accounts erstellen und sich anmelden.
- Daten werden in einer Postgresql-Datenbank gespeichert.
- Bilder hochladen.
- Nährungswerte der Gerichte können gespeichert werden.

## Architekturübersicht
![img.png](img.png)

## Dienste

### Frontend (Streamlit):
   - Rolle: Stellt die nutzerzentrierte Weboberfläche bereit.
   - Funktionalität: Bild-Upload, Anzeige der analysierten Nährwerte, Interaktion mit dem Backend.
### KI-Service (phi-4-multimodal):
   - Rolle: Hochpräzise Bildanalyse und -beschreibung.
   - Funktionalität: Empfängt das hochgeladene Bild und generiert eine äußerst detaillierte und akkurate textuelle Beschreibung (z.B. "Spaghetti...").
### Externe API (OpenFoodFacts):
  - Rolle: Bereitstellung der Nährwertdaten.
### Backend-Service (FastAPI):
  - Rolle: Zentrale Geschäftslogik und Nutzerdatenverwaltung.
### Datenbank (PostgreSQL):
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
  │   │   ├── Architekturübersicht.png
  │   │   └── SmartSite.png
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
  │   │   ├── backend_dep.yaml
  │   │   └── backend_service.yaml
  │   ├── frontend/
  │   │   ├── app-dep.yaml
  │   │   ├── app-svc.yaml
  │   │   └── smartSite-ing.yaml
  │   └── storage/
  │       ├── db_deployment.yaml
  │       ├── db_service.yaml
  │       ├── pvc.yaml
  │       └── secret.yaml
  ├── .env
  ├── .gitignore
  ├── gitlab-ci.yml
  ├── docker-compose.yml
  └── README.md
```

## Docker Compose
- Die Datei docker-compose.yml definiert alle Services:
  - Frontend: Streamlit
  - Backend : FastAPI
  - DB: PostgresSQL Datenbank

## GitLab CI/CD
- Die .gitlab-ci.yml Datei beschreibt die CI/CD-Pipeline.
- Docker-Images werden automatisch erstellt und in die GitLab Registry geladen.
- Deploy-Dateien werden automatisch ausgeführt.

## Anwendung lokal ausführen
   ### Voraussetzungen
- Docker und Docker Compose installiert
   ### Starten
- ```sh
    docker-compose up --build
    ```
   ### Zugriff
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- Backend API Dokumentation: http://localhost:8000/docs
- Datenbank: lokal erreichbar auf Port 5432

## Anwendung ausführen/Deployment

 ### Automatisches Deployment (CI/CD)

Das Deployment auf den Kubernetes-Cluster wird automatisch von der GitLab CI/CD-Pipeline gesteuert.

**Voraussetzung:** Die Pipeline wird nur ausgelöst, wenn die Variable `DEPLOY` auf `"yes"` gesetzt ist.

**So wird's gemacht:**
1.  **Variable setzen:** In der `.gitlab-ci.yml`-Datei den Wert der Variable `DEPLOY` von `"no"` auf `"yes"` ändern.
    ```yaml
    variables:
      APP_NAME: "SmartBite"
      DEPLOY: "yes"  # hier ändern
    ```
2.  **Änderung pushen:** Committe die geänderte Datei und pushe sie in den `main`-Branch.
3.  **Pipeline startet:** Der Push trigger automatisch die Pipeline in GitLab, die die Anwendung nun baut und deployt.

Der Status des Deployments kann unter **CI/CD > Pipelines** in GitLab verfolgt werden.
  
### Zugriff auf die live Anwendung

Nach einem erfolgreichen Deployment ist die Anwendung unter dieser URL erreichbar:
**https://smartbite.edu.k8s.th-luebeck.dev**

## Verwendete Technologien/Bibliotheken
  ### Backend
- FastAPI - Web Framework für APIs
- uvicorn - ASGI-Server für Python
- sqlalchemy - ORM für Datenbankzugriff
- requests - HTTP Client für API-Anfragen
- passlib - Password Hashing
- python-jose - JWT Token Handling
- httpx - Asynchroner HTTP Client

### Frontend
- streamlit - Web Framework für Data Apps
- requests - HTTP Client für Backend-Kommunikation
- pandas - Datenanalyse und -manipulation
- streamlit-option-menu - UI Komponenten für Streamlit
- openai - OpenAI API Client
- Pillow - Bildverarbeitung
- httpx - HTTP Client

  ### Infrastruktur und Tools
- Docker - Containerisierung
- Docker Compose - Container Orchestrierung
- PostgreSQL - Datenbank
- Kubernetes - Container Orchestrierung (Production)
- GitLab CI/CD - Continuous Integration/Deployment
- OpenFoodFacts API - Nährwertdaten
- phi-4-multimodal - KI-Modell für Bilderkennung 

## Aufgetretene Probleme
#### Kamera-Funktionalität im Production-Deployment
  - Problem:
    - Ursprünglich war die Nutzung der camera_input-Komponente von Streamlit geplant. Diese Komponente funktionierte in der lokalen Entwicklungsumgebung einwandfrei, scheiterte jedoch im Kubernetes-Deployment. Die Ursache hierfür liegt in den Sicherheitseinschränkungen moderner Browser, die den Kamerazugriff nur über eine sichere HTTPS-Verbindung und oft nur in bestimmten Kontexten erlauben. Im Production-Setup wurde dieser Zugriff blockiert.
  - Lösung:
    - Als zuverlässige Alternative wurde auf die file_uploader-Komponente von Streamlit umgestellt. Wichtig: Diese Lösung bietet praktisch den gleichen Funktionsumfang, da Nutzer auf Mobilgeräten beim Upload-Dialog die Option haben, direkt ein neues Foto mit der Kamera aufzunehmen, anstatt ein bestehendes Bild auszuwählen.
  - Bekanntes Restproblem:
        - Beim Upload sehr großer Bilder (insbesondere von modernen Smartphone-Kameras) kann folgender Fehler auftreten:
          - ```
            AxiosError: Request failed with status code 413
            ```
  - Lösungsansatz und Zeitmangel:
    - Es wurde versucht, die Bilder clientseitig vor dem Hochladen zu komprimieren und zu verkleinern, um die Dateigröße zu reduzieren. Aufgrund der zeitlichen Komplexität einer stabilen Implementierung dieser Komprimierung in Streamlit konnte dieser Ansatz jedoch nicht finalisiert werden.
  - Aktueller Status:
    - Das Hochladen von Bildern von einem Desktop-Computer oder kleineren Bilddateien von Mobilgeräten funktioniert zuverlässig. Der Upload sehr großer, direkt mit der Handykamera aufgenommener Bilder kann weiterhin zu einem 413-Fehler führen.
#### Streamlit Multipage-Handling
- Am Anfang hatte ich Probleme mit switching_page in Streamlit, da dabei viele Fehler auftraten. Deshalb habe ich alle Seiten in einer Datei (app.py) zusammengefasst, was jedoch unpraktisch ist.
#### Erweiterte Account-Funktionen
- Aufgrund von Zeitmangel und der Komplexität der Funktion „Passwort vergessen“ wurde diese leider nicht implementiert.

## Hinweise zur KI-Unterstützung
Zur Qualitätssicherung und sprachlichen Korrektur wurde KI eingesetzt. Die KI hat insbesondere bei der Verbesserung von Dokumentationsabschnitten geholfen, wurde aber nicht zur Codegenerierung verwendet.

## Lizenz
Dieses Projekt dient ausschließlich Studien- und Lernzwecken. Eine kommerzielle Nutzung ist nicht vorgesehen.
