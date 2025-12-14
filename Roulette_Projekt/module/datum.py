# Datum & Alter: Geburtsdatum prüfen und 18+ Kontrolle.

from datetime import date, datetime

def geburtsdatum(s: str) -> date | None:  
    # Wandelt Text im Format TT.MM.JJJJ in ein Datum um
    s = s.strip()  # Entfernt Leerzeichen
    try:
        return datetime.strptime(s, "%d.%m.%Y").date()  # Text -> Datum
    except ValueError:  # Falsches Format oder ungültiges Datum
        print("Ungültiges Datum! Bitte im Format TT.MM.JJJJ angeben (z. B. 19.04.2002).")
        return None

def jahre_addieren(d: date, jahre: int) -> date:
    # Addiert Jahre zu einem Datum (beachtet Schaltjahre)
    try:
        return d.replace(year=d.year + jahre)
    except ValueError:  # Falls 29. Feb. und kein Schaltjahr
        return d.replace(month=2, day=28, year=d.year + jahre)
    
def ist_mindestens_18(geburt: date) -> tuple[bool, date]:
    # Prüft, ob jemand heute mindestens 18 Jahre alt ist
    heute = date.today()
    achtzehnter = jahre_addieren(geburt, 18)
    return (heute >= achtzehnter, achtzehnter)  # True/False + Datum des 18. Geburtstags