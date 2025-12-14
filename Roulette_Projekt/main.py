# Hauptprogramm: Startet das Spiel und steuert das Menü.

from module.speichern_und_laden import nutzer_laden, nutzer_speichern
from module.auth import anmeldefluss
from module.roulette import einzahlen, auszahlen, spiele_runde, zeige_verlauf

def main():
    # Startpunkt des Programms (Menü & Ablauf)
    users = nutzer_laden() # Lädt alle gespeicherten Benutzer aus Datei
    benutzername = anmeldefluss(users) # Führt Anmeldung oder Registrierung durch
    if not benutzername:
        print("Programm wird beendet.")
        return

    zustand = users.get(benutzername, {})  # Holt gespeicherte Daten des Benutzers (falls vorhanden)
    guthaben = float(zustand.get("guthaben", 0.0))  # Startguthaben oder 0 CHF
    verlauf = list(zustand.get("verlauf", []))  # Vorherige Runden (falls vorhanden)

    while True:
        print("\n-----------------------------")
        print("         HAUPTMENÜ")
        print("-----------------------------")
        print(f"Angemeldet als: {benutzername}")
        print(f"Aktuelles Guthaben: {guthaben:.2f} CHF")
        print("1 - Einzahlen")
        print("2 - Auszahlen")
        print("3 - Runde starten")
        print("4 - Verlauf anzeigen")
        print("5 - Abmelden & Beenden")

        auswahl = input("Wahl (1–5): ").strip()
        if auswahl == "1":
            guthaben = einzahlen(guthaben)
        elif auswahl == "2":
            guthaben = auszahlen(guthaben)
        elif auswahl == "3":
            guthaben, verlauf = spiele_runde(benutzername, guthaben, verlauf)
        elif auswahl == "4":
            zeige_verlauf(verlauf)
        elif auswahl == "5":
            print("Danke fürs Spielen, bis bald ;).")
            break
        else:
            print("Die Eingabe ist ungültig, bitte wähle ein Menüpunkt zwischen 1-5 aus.")

        # Speichern nach jeder Aktion
        users[benutzername] = {"guthaben": guthaben, "verlauf": verlauf, **users.get(benutzername, {})} # Behält restliche Benutzerdaten (z. B. Passwort, Geburtsdatum)
        nutzer_speichern(users) # Daten in Datei speichern

    # Nach Beenden, Endstand speichern
    users[benutzername]["guthaben"] = guthaben
    users[benutzername]["verlauf"] = verlauf
    nutzer_speichern(users)
    print("Dein Spielverlauf wurde gespeichert.")

if __name__ == "__main__":
    main()
