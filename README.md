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

## Hauptfunktionen
- **Mechanismensimulation:**  
  Darstellung und Berechnung von ebenen Mechanismen unter Verwendung von definierten Gelenken (Punkten) und Gliedern (Stangen). Dabei wird für einen konstanten Drehwinkel die Konfiguration des gesamten Mechanismus ermittelt.

- **Fehlerberechnung:**  
  Ermittlung der Differenz zwischen den berechneten (Soll-) und den tatsächlich gemessenen (Ist-) Längen der Glieder. Diese Abweichungen werden anschließend mittels Optimierungsalgorithmen (z.B. aus dem `scipy.optimize`-Modul) minimiert.

- **Objektorientierte Architektur:**  
  Der Einsatz von objektorientierten Konzepten bei der Fehlerberechnung und Simulation ermöglicht eine klare Trennung der einzelnen Funktionalitäten, was den Code nicht nur wartbar, sondern auch einfach erweiterbar macht.

- **Visualisierung:**  
  Graphische Darstellung der Mechanismen, inklusive Animationen, um die kinematische Bewegung und die Fehlerverläufe der Glieder über verschiedene Drehwinkel hinweg zu veranschaulichen.

## Technologien und Werkzeuge
- **Programmiersprache:** Python
- **Web-UI:** Streamlit (für eine interaktive Benutzeroberfläche)
- **Mathematische Bibliotheken:** NumPy, SciPy (für numerische Berechnungen und Optimierung)
- **3D-Modellierung:** OpenSCAD (zur Erstellung eines 3D-Volumenmodells des Mechanismus)
- **Dokumentation:** UML-Diagramme zur Darstellung der Klassenstruktur (Platzhalter für weitere Details)

## Installation und Ausführung
*Platzhalter für die detaillierte Anleitung zur Installation und Ausführung:*
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
   streamlit run main.py
   ```

## UML-Diagramme
*Platzhalter für UML-Diagramme,  die Klassenstruktur und die Beziehungen  *

## Erweiterungen
Bisher wurden folgende Erweiterungen implementiert:
- **Animation als GIF speichern:**  
  Die Simulation kann als animierte GIF exportiert werden, um Bewegungsabläufe und Fehlerverläufe zu dokumentieren.
  
- **Stückliste als PDF:**  
  Eine automatische Generierung einer Stückliste im PDF-Format, die alle relevanten Komponenten des Mechanismus (Gestänge, Antriebe, Gelenke) auflistet.
  
- **3D-Volumenmodell mittels OpenSCAD:**  
  Erstellung eines 3D-Modells des Mechanismus, das in OpenSCAD weiterverarbeitet werden kann, um volumetrische Analysen und Visualisierungen zu ermöglichen.

## Projektstruktur
```
├── README.md
├── requirements.txt
├── main.py

```

## Weiterführende Informationen
*Hier können weiterführende Links, Literaturhinweise und zusätzliche Dokumentationen ergänzt werden, um einen tieferen Einblick in die Methodik und die zugrunde liegenden mathematischen Modelle zu geben.*



