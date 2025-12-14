# Pfade 
import os

DATEN_ORDNER = "daten"
os.makedirs(DATEN_ORDNER, exist_ok=True)

# CSV: Benutzer (Name, Passwort, Geburtsdatum, Guthaben)
DATEI_USERS_CSV = os.path.join(DATEN_ORDNER, "users.csv")

# CSV: Runden (Benutzername, Zahl, Farbe, Gerade/Ungerade)
DATEI_RUNDEN_CSV = os.path.join(DATEN_ORDNER, "roulette_verlauf.csv")
