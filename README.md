# Simulation ebener Mechanismen

## Einleitung
- **Projektname:** Ebene_Mechanismen
- **Projekttyp:** Simulation
- **Autor(en):** Fabian Augschöll, Manuel Hofer
- **Datum:** 05.02.2025
- **Kurzbeschreibung:** Simulation ebener Mechanismen zur Berechnung von Längenfehlern und Visualisierung der kinematischen Bewegung.
- **Mindestzielsetzung:** 
    - Implementierung einer Python-Anwendung mit Streamlit-Web-UI
    - Definition und Simulation ebener Mechanismen
    - Berechnung der Positions-Kinematik für einen Drehwinkelbereich
    - Visualisierung des Mechanismus und seiner Bahnkurven
    - Speicherung und Laden des Mechanismus
    - Fehleroptimierung durch Minimierung der Längenabweichungen
    - Validierung der Mechanismen anhand vorgegebener Testfälle
    - Bereitstellung der Anwendung über Streamlit

## Projektbeschreibung
Dieses Projekt befasst sich mit der Simulation ebener Mechanismen. Die methodische Grundlage zur Berechnung der Längenfehler wurde durch den betreuenden Professor vorgegeben. Anstelle der empfohlenen Matrixrechnung wurde jedoch ein objektorientierter Ansatz gewählt, um eine strukturierte und modulare Implementierung zu gewährleisten. Diese Vorgehensweise erleichtert die Wartung und Erweiterung des Codes, wodurch zukünftige Anpassungen effizienter umgesetzt werden können. Zudem trägt dieser Ansatz zur besseren Lesbarkeit bei und ermöglicht eine klare Trennung der einzelnen funktionalen Komponenten der Simulation.



## Technologien und Werkzeuge
- **Programmiersprache:** Python
- **Web-UI:** Streamlit (für eine interaktive Benutzeroberfläche)
- **Mathematische Bibliotheken:** NumPy, SciPy (für numerische Berechnungen und Optimierung)
- **3D-Modellierung:** OpenSCAD (zur Erstellung eines 3D-Volumenmodells des Mechanismus)


## Installation und Ausführung

1. **Repository klonen:**  
   ```bash
   git clone <repository-url>
   ```
2. **Abhängigkeiten installieren:**  
   ```bash
   pip install -r requirements.txt
   ```
3. **Projekt starten:**  
   ```bash
   streamlit run ui.py
   ```

## UML-Diagramme
*Platzhalter für UML-Diagramme,  die Klassenstruktur und die Beziehungen*


## Proof of Concept: Berechnung
  Die Simulation ebener Mechanismen wurde erfolgreich implementiert und erfüllt die gestellten Minimalanforderungen. Hier gezeigt mit dem Viergelenk bzw. einem Bein des "Strandbeest" von Theo Jansen:
  ![Viergelenk](doc/Viergelenk.gif)
  ![Viergelenk](doc/strandbeest.gif)





## Erweiterungen
Bisher wurden folgende Erweiterungen implementiert:
- **Animation als GIF speichern:**  
  Die Simulation kann als animierte GIF exportiert werden, um Bewegungsabläufe und Fehlerverläufe zu dokumentieren.
  
- **Stückliste als PDF:**  
  Eine automatische Generierung einer Stückliste im PDF-Format, die alle relevanten Komponenten des Mechanismus (Gestänge, Antriebe, Gelenke) auflistet. 
  
- **3D-Volumenmodell mittels OpenSCAD:**  
  Erstellung eines 3D-Modells des Mechanismus, das in OpenSCAD weiterverarbeitet werden kann, um volumetrische Analysen und Visualisierungen zu ermöglichen.

- **Erweiterung auf mehrere Fixpunkte:**
  Die Simulation unterstützt nun mehrere Fixpunkte, um die Bewegung des Mechanismus in verschiedenen Konfigurationen zu analysieren. Beispiel: two-legged-Strandbeest

- **Auszeichnungssprache mittels JSON-Datenbank**
  Implementierung einer JSON-Datenbank mittels TinyDB zur Speicherung und zum Laden von Mechanismen. Zusätzlich können externe Mechanismen importiert und in der Simulation verwendet werden. Bereits erstellte Mechanismen können heruntergeladen werden. 

## Walkthrough
- Variante A: Punkte und Verbindungen im build-Tab händisch erstellen
  - Mechanismus definieren (bild)
  - live-preview wird autoamtisch erstellt (bild)
  - Freiheitsgrade können, müssen aber nicht, händisch überprüft werden 
  - der erstellte Mechanismus muss für die Berechnung gespeichert werden (entwerder Temporär oder als eigene Datenbank)
  - in den plot-Tab wechseln und als data source den erstellten Mechanismus auswählen (temporäre Datei bzw. eigene Datenbank)
  - Punkt auswählen dessen Bahnkurve zusätzlich zum Bewegungsablauf geplottet werden soll
  - mit *calculate* die Berechnung starten (Berechnung und erstellen der Simulation kann einige Sekunden dauern)
  - im Download-Bereich unter der Visulaisierung können alle erstellen Dateien (Stückliste, CSV-Bahnkurve, CAD-Modell, Animation, Datenbank) heruntergeladen werden

- Variante B: Mechanismus importieren
  - plot-Tab öffnen
  - bei der Auswahl der data source eine vorhandene Datenbank auswählen bzw. eine eigene hochladen



## Projektstruktur
```
├── README.md
├── requirements.txt
├── main.py

```

## Weiterführende Informationen
*Hier können weiterführende Links, Literaturhinweise und zusätzliche Dokumentationen ergänzt werden, um einen tieferen Einblick in die Methodik und die zugrunde liegenden mathematischen Modelle zu geben.*



