# speichern_und_laden

import csv
from config import DATEI_USERS_CSV, DATEI_RUNDEN_CSV  # Pfade zu den CSV-Dateien

def nutzer_laden():
    """Lädt alle Benutzer aus der Datei users.csv."""
    benutzer = {}  
    try:
        with open(DATEI_USERS_CSV, newline="", encoding="utf-8") as datei:
            for name, passwort, geburtsdatum, guthaben in csv.reader(datei):
                benutzer[name] = {
                    "password": passwort,                   # Passwort
                    "birthdate_iso": geburtsdatum,          # Geburtsdatum im ISO-Format
                    "guthaben": float(guthaben),            # Guthaben als Zahl
                    "verlauf": [],                          # Spielverlauf 
                }
    except FileNotFoundError:
        pass  # Wenn Datei nicht existiert
    return benutzer

def nutzer_speichern(benutzer):
    """Speichert alle Benutzer in die Datei users.csv."""
    with open(DATEI_USERS_CSV, "w", newline="", encoding="utf-8") as datei:
        schreiber = csv.writer(datei)
        for name, daten in benutzer.items():
            schreiber.writerow([
                name,
                daten["password"],
                daten["birthdate_iso"],
                daten["guthaben"]
            ])

def runden_eintrag_speichern_csv(name, zahl, farbe, gerade_oder_ungerade):
    """Speichert eine gespielte Runde in die Datei roulette_verlauf.csv."""
    with open(DATEI_RUNDEN_CSV, "a", newline="", encoding="utf-8") as datei:
        csv.writer(datei).writerow([name, zahl, farbe, gerade_oder_ungerade])

def letzte_runden_aus_csv(name, anzahl=10):
    """Liest die letzten 'anzahl' Runden eines bestimmten Spielers aus."""
    try:
        with open(DATEI_RUNDEN_CSV, newline="", encoding="utf-8") as datei:
            zeilen = [zeile for zeile in csv.reader(datei) if zeile and zeile[0] == name]
        return zeilen[-anzahl:]  # Nur die letzten  Einträge zurückgeben
    except FileNotFoundError:
        return []  # Falls Datei fehlt → leere Liste zurückgeben
