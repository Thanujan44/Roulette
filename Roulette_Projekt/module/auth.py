# Anmeldung & Registrierung: Benutzer anlegen und anmelden.

from datetime import date  
from module.datum import geburtsdatum, ist_mindestens_18  
from module.eingaben import eingabe_auswahl 
from module.speichern_und_laden import nutzer_speichern  


def benutzer_registrieren(users: dict) -> str | None:  # Definiert eine Funktion zur Registrierung eines neuen Benutzers
    print("\n=== Registrierung ===")  

    while True:  
        name = input("Gewünschter Benutzername: ").strip()  # Strip = Leerzeichen am Anfang/Ende entfernen (Damit keine gleichen Benutzernamen entstehen)
        if not name:  # Wenn kein Name eingegeben wurde
            print("Benutzername darf nicht leer sein.") 
            continue  # Zurück zum Anfang der Schleife
        if name in users:  # Wenn der Benutzername schon existiert
            print("Benutzername bereits vergeben.") 
            continue  # Wieder zum Anfang der Schleife
        break  # Gültiger, neuer Name -> Schleife beenden

    while True:  
        pw1 = input("Passwort eingeben: ")  
        pw2 = input("Passwort wiederholen: ")  
        if not pw1:  # Wenn kein Passwort eingegeben wurde
            print("Passwort darf nicht leer sein.")  
            continue  # Wieder zum Anfang der Schleife
        if pw1 != pw2:  # Wenn Passwörter unterschiedlich sind
            print("Passwörter stimmen nicht überein.")  
            continue  # Wieder zum Anfang der Schleife
        break  # Beide Passwörter sind gleich -> Schleife beenden

    while True:  
        bd_str = input("Geburtsdatum (TT.MM.JJJJ, z. B. 19.04.2002): ").strip()  # Eingabe als Text
        bd = geburtsdatum(bd_str)  # Übergibt den Text an die Funktion, die ihn in ein Datum umwandelt
        if bd is None:  # Wenn ungültiges Datum
            continue  # Zurück zum Anfang der Schleife, neu versuchen
        if bd > date.today():  # Wenn Geburtsdatum in der Zukunft liegt
            print("Geburtsdatum liegt in der Zukunft, bitte erneut eingeben.") 
            continue  # Wieder neu eingeben
        ok, achtzehnter = ist_mindestens_18(bd)  # Prüft, ob Benutzer mindestens 18 Jahre alt ist
        if not ok:  # Wenn Benutzer unter 18 ist
            print("Du bist noch nicht 18.") 
            return None  # Registrierung abbrechen
        break  # Wenn Benutzer >= 18 -> Schleife beenden

    users[name] = {  # Neuen Benutzer in das Dictionary "users" einfügen
        "password": pw1,  # Passwort speichern
        "birthdate_iso": bd.isoformat(),  # Geburtsdatum im ISO-Format (JJJJ-MM-TT)
        "guthaben": 0.0,  # Startguthaben
        "verlauf": [],  # Leerer Verlauf
    }

    nutzer_speichern(users)  # Speichert das Dictionary mit allen Benutzern dauerhaft
    print(f"Registrierung erfolgreich. Willkommen, {name}!") 
    return name  # Gibt den neuen Benutzernamen zurück


def benutzer_anmelden(users: dict) -> str | None:  # Definiert Funktion zur Anmeldung eines Benutzers
    print("\n=== Anmeldung ===") 

    while True:  # Schleife für wiederholte Anmeldeversuche
        name = input("Benutzername: ").strip()  # Benutzername eingeben
        if name == "":  # Wenn leer
            return None  # Anmeldung abbrechen
        if name not in users:  # Wenn Benutzername unbekannt ist
            print("Unbekannter Benutzername.") 
            break  # Schleife beenden (zurück ins Hauptmenü)

        pw = input("Passwort eingeben: ")  # Passwort eingeben
        if pw == "":  # Wenn leer
            return None  # Anmeldung abbrechen

        if pw != users[name].get("password", ""):  # Passwort vergleichen
            print("Falsches Passwort.") 
            continue  # Noch einmal versuchen

        try:
            geburt = date.fromisoformat(users[name]["birthdate_iso"])  # Geburtsdatum aus gespeichertem ISO-String wiederherstellen
        except Exception:  # Falls das gespeicherte Datum fehlerhaft ist
            print("Gespeichertes Geburtsdatum fehlerhaft. Bitte neu registrieren.") 
            return None  # Anmeldung abbrechen

        ok, _ = ist_mindestens_18(geburt)  # Erneuter Alterscheck zur Sicherheit
        if not ok:  # Wenn Benutzer nicht 18 ist
            print("Du bist noch nicht 18.") 
            return None  # Anmeldung abbrechen

        print(f"Anmeldung erfolgreich. Willkommen zurück, {name}!") 
        return name  # Gibt den Benutzernamen zurück

def anmeldefluss(users: dict) -> str | None: # Definiert den Hauptablauf für Registrierung, Anmeldung und Beenden
    while True:
        print("\n--- Start ---")
        print("1 - Registrieren")
        print("2 - Anmelden")
        print("3 - Beenden")
        wahl = eingabe_auswahl("Bitte wählen (1/2/3): ", ["1","2","3"]) # Fragt den Benutzer nach einer Auswahl und überprüft, dass sie gültig ist
        if wahl == "1": # Wenn 1 gewählt -> Registrierung
            u = benutzer_registrieren(users); 
            if u: return u
        elif wahl == "2": # Wenn 2 gewählt -> Anmeldung
            u = benutzer_anmelden(users); 
            if u: return u
        elif wahl == "3": # Wenn 3 gewählt -> Beenden
            return None # Beendet das Programm
