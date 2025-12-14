# Saubere Abfragen für Zahlen und Auswahlen.

def eingabe_zahl_float(prompt: str, leere_eingabe_erlaubt: bool = True) -> float | None:
    # Fragt eine Zahl ab und prüft die Eingabe
    while True:
        s = input(prompt).strip()  # Benutzer-Eingabe lesen und Leerzeichen entfernen
        if leere_eingabe_erlaubt and s == "":  # Leere Eingabe ist erlaubt
            return None
        s = s.replace(",", ".")  # Kommas durch Punkte ersetzen (z. B. 1,5 → 1.5)
        try:
            return float(s)  # Versuch, Eingabe in eine Zahl umzuwandeln
        except ValueError:  # Falls Umwandlung nicht möglich ist
            print("Ungültige Zahl. Bitte erneut eingeben.")

def eingabe_auswahl(prompt: str, optionen: list[str]) -> str:
    # Fragt eine Auswahl ab und prüft, ob die Eingabe gültig ist
    opts = [o.lower() for o in optionen]  # Erlaubte Optionen in Kleinbuchstaben umwandeln
    while True:
        s = input(prompt).strip().lower()  # Eingabe lesen und in Kleinbuchstaben umwandeln
        if s in opts:  # Wenn Eingabe gültig ist
            return s
        print(f"Ungültige Eingabe. Erlaubt: {', '.join(optionen)}")  # Fehlermeldung bei ungültiger Auswahl
