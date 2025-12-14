# Roulette-Spiel 

Ein Roulette-Spiel bei dem sich die Benutzer registrieren, anmelden und anschliessend Roulette spielen können.  
Das Projekt nutzt **CSV-Dateien** zur Speicherung von Benutzerdaten und Spielverläufen und bildet so ein vollständiges Spielsystem mit Benutzerverwaltung, Guthabenhandling und Spielrunden ab.
Das Roulette-Spiel läuft komplett im **Terminal** und simuliert eine vereinfachte Form des europäischen Roulettes.  

---

## Inhaltsverzeichnis
1. Projektbeschreibung  
2. Hauptfunktionen – Technische Umsetzung  
3. Projektstruktur  
4. Installation & Start  
5. Benutzung & Ablauf  
6. Dateispeicherung  

## 1. Hauptfunktionen – Technische Umsetzung

### Benutzerverwaltung (`auth.py`, `datum.py`, `speichern_und_laden.py`)
- **Registrierung (`benutzer_registrieren`)**  
  Fragt Benutzername, Passwort und Geburtsdatum ab.  
  Das Geburtsdatum wird durch `geburtsdatum()` geprüft und in ein `datetime.date`-Objekt umgewandelt.  
  Die Funktion `ist_mindestens_18()` stellt sicher, dass der Spieler volljährig ist.  
  Erfolgreich registrierte Benutzer werden mit Passwort, Geburtsdatum und Startguthaben in der Datei `users.csv` gespeichert.

- **Anmeldung (`benutzer_anmelden`)**  
  Vergleicht Benutzername und Passwort mit den gespeicherten Werten in `users.csv`.  
  Nur volljährige und korrekt registrierte Benutzer können sich anmelden.

- **Speicherung**  
  `nutzer_laden()` und `nutzer_speichern()` laden und speichern alle Benutzer in einer CSV-Datei.

---

### Guthabenverwaltung (`roulette.py`)
- **Einzahlen (`einzahlen`)**  
  Fragt über `eingabe_zahl_float()` den Betrag ab und erhöht das Guthaben, sofern der Betrag positiv ist.  

- **Auszahlen (`auszahlen`)**  
  Funktioniert analog, prüft jedoch, ob der Betrag nicht höher als das aktuelle Guthaben ist.

---

### Spielmechanik (`roulette.py`)
- **Rundenstart (`spiele_runde`)**  
  Spieler können mehrere Wetten gleichzeitig platzieren:
  - Zahl (0–36) → Auszahlung 35:1  
  - Farbe (rot/schwarz) → Auszahlung 1:1  
  - Gerade/Ungerade → Auszahlung 1:1  

  Das Programm nutzt:
  - `bestimme_farbe(zahl)` – gibt die Farbe einer Zahl zurück  
  - `gerade_ungerade(zahl)` – prüft, ob die gezogene Zahl gerade oder ungerade ist

  Nach Eingabe der Wetten wird eine Zufallszahl (0–36) über `random.randint()` gezogen, das Ergebnis ausgegeben und Gewinne bzw. Verluste berechnet.  
  Anschließend werden die Ergebnisse in der Datei `roulette_verlauf.csv` gespeichert.

---

### Spielverlauf (`roulette.py`)
- **Verlauf anzeigen (`zeige_verlauf`)**  
  Gibt die letzten zehn gezogenen Zahlen und deren Farben aus.  
  Der Verlauf wird im Speicher sowie in der CSV-Datei gespeichert.

---

## 2. Projektstruktur

```
projektordner/
│
├── main.py                    # Hauptprogramm: Menü und Spielfluss
├── config.py                  # Definition der Datenpfade und Ordner
│
└── module/
    ├── auth.py                # Registrierung und Anmeldung der Benutzer
    ├── datum.py               # Datumseingabe und Altersprüfung
    ├── eingaben.py            # Eingabevalidierung für Zahlen und Auswahlen
    ├── roulette.py            # Spiellogik: Ein-/Auszahlen, Wetten, Runden
    └── speichern_und_laden.py # Laden und Speichern der Benutzerdaten (CSV)
```

Beim ersten Start wird automatisch der Ordner `daten/` erstellt, in dem die CSV-Dateien gespeichert werden.

---

## 3. Installation & Start

### Voraussetzungen
- Python 3.10 oder neuer  

### Startanleitung
1. Projekt herunterladen
2. Im Projektordner öffnen  
3. Im Terminal ausführen:  
   ```bash
   python main.py
   ```
4. Es erscheint das Startmenü, in dem sich Benutzer registrieren oder anmelden können.

---

## 4. Benutzung & Ablauf

### Hauptmenü
Nach der Anmeldung erscheint:
```
-----------------------------
         HAUPTMENÜ
-----------------------------
1 - Einzahlen
2 - Auszahlen
3 - Runde starten
4 - Verlauf anzeigen
5 - Abmelden & Beenden
```

### Menüoptionen
1. **Einzahlen:** Betrag eingeben, Guthaben erhöhen  
2. **Auszahlen:** Betrag abheben, sofern Guthaben ausreicht  
3. **Runde starten:** Wetten platzieren, Zahl wird gezogen, Gewinn/Verlust wird berechnet  
4. **Verlauf anzeigen:** Zeigt die letzten 10 gezogenen Zahlen  
5. **Abmelden & Beenden:** Programm beendet sich, alle Daten werden gespeichert  

---

## 5. Dateispeicherung

| Datei | Inhalt | Format |
|--------|---------|--------|
| `daten/users.csv` | Benutzername, Passwort, Geburtsdatum, Guthaben | CSV |
| `daten/roulette_verlauf.csv` | Benutzername, Zahl, Farbe, Gerade/Ungerade | CSV |

Die Dateien werden automatisch beim ersten Start erstellt und nach jeder Änderung aktualisiert.  
Alle gespeicherten Informationen sind im Klartext einsehbar, was der Lern- und Demonstrationszweck dieses Projekts ist.  
