# Spielfunktionen: Ein-/Auszahlen, Runde spielen, Verlauf anzeigen.

import random
from module.eingaben import eingabe_auswahl, eingabe_zahl_float
from module.speichern_und_laden import runden_eintrag_speichern_csv

def bestimme_farbe(zahl: int) -> str:
    # Bestimmt die Farbe einer Zahl auf dem Roulette-Rad
    # 0 ist immer grün, bestimmte Zahlen sind rot, der Rest schwarz
    rote_zahlen = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}  # Alle roten Zahlen
    if zahl == 0:  # Spezialfall 0
        return "grün"
    return "rot" if zahl in rote_zahlen else "schwarz"  # Wenn in Liste rot, sonst schwarz


def gerade_ungerade(zahl: int) -> str:
    # Prüft, ob eine Zahl gerade oder ungerade ist
    if zahl == 0:  # 0 gilt als neutral (grün)
        return "keine"
    return "gerade" if (zahl % 2 == 0) else "ungerade"  


def einzahlen(guthaben: float) -> float:
    # Fragt nach einem Einzahlungsbetrag und erhöht das Guthaben
    betrag = eingabe_zahl_float("Einzahlungsbetrag (leer = abbrechen): ")  # Eingabe des Betrags
    if betrag is None or betrag <= 0:  # Abbruch oder ungültige Eingabe
        print("Keine Einzahlung durchgeführt.")
        return guthaben  # Guthaben bleibt gleich
    guthaben += betrag  # Betrag zum Guthaben addieren
    print(f"Eingezahlt: +{betrag:.2f} CHF") 
    return guthaben  # Neues Guthaben zurückgeben


def auszahlen(guthaben: float) -> float:
    # Fragt nach einem Auszahlungsbetrag und verringert das Guthaben
    betrag = eingabe_zahl_float("Auszahlungsbetrag (leer = abbrechen): ")
    if betrag is None or betrag <= 0:  # Keine Eingabe oder ungültiger Betrag
        print("Keine Auszahlung durchgeführt.")
        return guthaben
    if betrag > guthaben:  # Wenn zu wenig Geld vorhanden ist
        print("Nicht genügend Guthaben.")
        return guthaben
    guthaben -= betrag  # Betrag vom Guthaben abziehen
    print(f"Ausgezahlt: -{betrag:.2f} CHF") 
    return guthaben


def spiele_runde(benutzername: str, guthaben: float, verlauf: list) -> tuple[float, list]:
    # Führt eine vollständige Spielrunde durch
    print("\n=== Neue Runde ===")
    wetten = []  # Liste für alle gesetzten Wetten

    # Wetten erfassen
    while True:
        print("\nWette hinzufügen:")
        print("1 - Auf Zahl (0-36)")
        print("2 - Auf Farbe (rot/schwarz)")
        print("3 - Auf Parität (gerade/ungerade)")
        print("4 - Keine weitere Wette (Runde starten)")
        auswahl = eingabe_auswahl("Auswahl: ", ["1","2","3","4"])  # Benutzer wählt Wettart

        if auswahl == "4":  # Wenn keine weiteren Wetten
            break

        # Wette auf Zahl
        if auswahl == "1":
            try:
                wert = int(eingabe_zahl_float("Welche Zahl (0-36)? "))  # Zahl einlesen
            except (TypeError, ValueError):  # Wenn keine gültige Zahl eingegeben wurde
                print("Ungültige Zahl.")
                continue
            if wert < 0 or wert > 36:  # Zahl außerhalb des erlaubten Bereichs
                print("Zahl außerhalb des Bereichs.")
                continue
            einsatz = eingabe_zahl_float("Einsatz in CHF: ", leere_eingabe_erlaubt=False)  # Einsatz einlesen
            if einsatz is None or einsatz <= 0:  # Ungültiger Einsatz
                print("Ungültiger Einsatz.")
                continue
            # Wette als Dictionary speichern
            wetten.append({"art": "zahl", "wert": wert, "einsatz": einsatz})

        # Wette auf Farbe
        elif auswahl == "2":
            farbe = input("Farbe (rot/schwarz): ").strip().lower()
            if farbe not in {"rot", "schwarz"}:  # Nur rot oder schwarz erlaubt
                print("Ungültige Farbe.")
                continue
            einsatz = eingabe_zahl_float("Einsatz in CHF: ", leere_eingabe_erlaubt=False)
            if einsatz is None or einsatz <= 0:
                print("Ungültiger Einsatz.")
                continue
            # Wette als Dictionary speichern
            wetten.append({"art": "farbe", "wert": farbe, "einsatz": einsatz})

        # Wette auf gerade/ungerade
        elif auswahl == "3":
            par = input("Parität (gerade/ungerade): ").strip().lower()
            if par not in {"gerade", "ungerade"}:  # Eingabe prüfen
                print("Ungültige Parität.")
                continue
            einsatz = eingabe_zahl_float("Einsatz in CHF: ", leere_eingabe_erlaubt=False)
            if einsatz is None or einsatz <= 0:
                print("Ungültiger Einsatz.")
                continue
            # Wette als Dictionary speichern
            wetten.append({"art": "paritaet", "wert": par, "einsatz": einsatz})

    # Wenn keine Wetten gesetzt
    if not wetten:
        print("Keine Wetten – Runde abgebrochen.")
        return guthaben, verlauf

    # Prüfen, ob genug Guthaben vorhanden ist
    gesamt_einsatz = sum(w["einsatz"] for w in wetten)
    if gesamt_einsatz > guthaben:
        print("Nicht genügend Guthaben für diese Wetten.")
        return guthaben, verlauf

    # Zufallszahl ziehen
    gezogene_zahl = random.randint(0, 36)  # Zufallszahl zwischen 0 und 36
    gezogene_farbe = bestimme_farbe(gezogene_zahl)  # Farbe bestimmen
    verlauf.append([gezogene_zahl, gezogene_farbe])  # Ergebnis im Verlauf speichern
    print(f"\nDie Kugel fällt auf: {gezogene_zahl} ({gezogene_farbe})")

    # Runde in CSV-Datei protokollieren 
    runden_eintrag_speichern_csv(benutzername, gezogene_zahl, gezogene_farbe, gerade_ungerade(gezogene_zahl))

    # Gewinne berechnen
    gesamter_auszahlungsbetrag = 0.0  # Summe aller Gewinne
    for wette in wetten:
        art, wert, einsatz = wette["art"], wette["wert"], wette["einsatz"]
        auszahlung = 0.0
        if art == "zahl":  # Treffer auf exakte Zahl -> 36x Einsatz
            if gezogene_zahl == wert:
                auszahlung = einsatz * 36
        elif art == "farbe":  # Treffer auf Farbe -> 2x Einsatz
            if wert == gezogene_farbe:
                auszahlung = einsatz * 2
        elif art == "paritaet":  # Treffer auf gerade/ungerade -> 2x Einsatz
            if wert == gerade_ungerade(gezogene_zahl):
                auszahlung = einsatz * 2
        gesamter_auszahlungsbetrag += auszahlung  # Gewinne summieren

    # Guthaben aktualisieren
    guthaben -= gesamt_einsatz  # Gesamteinsätze abziehen
    guthaben += gesamter_auszahlungsbetrag  # Gewinne hinzufügen
    netto = gesamter_auszahlungsbetrag - gesamt_einsatz  # Nettogewinn/-verlust berechnen

    # Ergebnis anzeigen
    if netto > 0:
        print(f"\nRunde GEWONNEN: +{netto:.2f} CHF")
    elif netto < 0:
        print(f"\nRunde VERLOREN: {netto:.2f} CHF")
    else:
        print("\nRunde: +/- 0 CHF (Break-even)")

    print(f"Aktuelles Guthaben: {guthaben:.2f} CHF")  # Aktueller Kontostand
    return guthaben, verlauf  # Neues Guthaben + aktualisierter Verlauf zurückgeben


def zeige_verlauf(verlauf: list) -> None:
    # Zeigt die letzten gezogenen Zahlen und Farben an
    if not verlauf:  # Wenn noch keine Ergebnisse existieren
        print("Kein Verlauf vorhanden.")
        return
    print("\nLetzte Ergebnisse:")
    for i, (zahl, farbe) in enumerate(verlauf[-10:], start=1):  # Zeigt die letzten 10 Runden
        print(f"{i:2d}. Zahl: {zahl:2d} | Farbe: {farbe:7s}")  # Formatierte Ausgabe jeder Runde

