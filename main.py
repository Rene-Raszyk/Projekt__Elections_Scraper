"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Rene Raszyk
email: 2004reno2004@gmail.com
"""


import csv
import sys
import requests
import bs4


def zapisovani_do_souboru(jmeno:str, radek:list):
    """
    Zapíše jeden řádek dat do CSV souboru.

    Funkce vytvoří nebo otevře CSV soubor s názvem `jmeno` v režimu append (a+),
    použije kódování UTF-8 a oddělovač středník (;).
    Na konec souboru přidá nový řádek se zadanými hodnotami.

    Parametry:
        jmeno (str): Název souboru (včetně cesty), do kterého se má zapisovat.
        radek (list): Seznam hodnot představující jeden řádek CSV souboru.

    Návratová hodnota:
        None
    """

    with open(jmeno, mode="a+", newline="", encoding="utf-8") as soubor_csv:
        csv.writer(soubor_csv, dialect="excel", delimiter=";").writerow(radek)
    return

def vytvoreni_hlavicky_souboru(obsah_html):
    """
    Vytvoří seznam názvů sloupců (hlavičku) pro CSV soubor na základě HTML obsahu.

    Funkce začíná pevně definovanými názvy sloupců:
    ["code", "location", "registered", "envelopes", "valid"]  
    Poté z HTML objektu `obsah_html` vyhledá všechny elementy s CSS třídou
    `.overflow_name` a jejich textový obsah přidá na konec seznamu.

    Parametry:
        obsah_html: Objekt typu BeautifulSoup umožňující metodu `.select()`
                    pro vyhledání elementů v HTML pomocí CSS selektoru.

    Návratová hodnota:
        list: Seznam řetězců představující názvy sloupců.
    """    
    
    hlavicka = ["code", "location", "registered", "envelopes", "valid"]
    radek_tabulky = obsah_html.select(".overflow_name")

    for nazev in radek_tabulky:
        hlavicka.append(nazev.text)
    return hlavicka

def vytvoreni_radku_pro_zapis(obsah_html, kod_obec, url_obec):
    """
    Vytvoří seznam hodnot představujících jeden řádek pro zápis do CSV souboru
    na základě dat z HTML stránky s výsledky voleb.

    Funkce:
    - extrahuje z HTML informace o obci, počtech voličů, vydaných obálek a platných hlasech,
    - název obce vybírá z různých míst HTML podle URL obce a délky kódu obce,
      protože struktura HTML se liší u některých stránek,
    - doplní další číselné hodnoty získané z části HTML identifikované jako <div id="inner">,
      vybírá každou třetí položku ze selektoru s třídou `.cislo`, počínaje druhou,
    - vrátí kompletní seznam dat pro zápis.

    Parametry:
        obsah_html: BeautifulSoup objekt obsahující HTML dané obce.
        kod_obec (str): Kód obce (číslo či text) používaný jako identifikátor.
        url_obec (str): URL adresa stránky obce, podle které se rozhoduje způsob extrakce názvu obce.

    Návratová hodnota:
        list: Seznam hodnot pro jeden řádek CSV ve formátu:
              [kod_obec, jmeno_obce, volici_v_seznamu, vydane_obalky, platne_hlasy, hlasy, ..., hlasy]
    """

    def vybirani_hodnot_ze_zbylych_tabulek(html):
        html_tabulek = html.find("div", id="inner")
        radek_tabulky = html_tabulek.select('.cislo')
        for radek in radek_tabulky[1::3]:
            seznam.append(radek.text)
        return
    
    seznam = []
    if url_obec == "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100":
        jmeno_obce = obsah_html.select_one("h3:nth-child(3)").text[7:-1]
    else:  
        if len(kod_obec) > 4:
            jmeno_obce = obsah_html.select_one("h3:nth-child(4)").text[7:-1]
        elif len(kod_obec) >= 3:
            jmeno_obce = obsah_html.select_one("h3:nth-child(4)").text[13:-1]
        elif len(kod_obec) >=2 :
            jmeno_obce = obsah_html.select_one("h3:nth-child(4)").text[12:-1]
        else:
            jmeno_obce = obsah_html.select_one("h3:nth-child(4)").text[11:-1]
        
    volici_v_seznamu = obsah_html.select_one('td[headers="sa2"][data-rel="L1"]').text
    vydane_obalky = obsah_html.select_one('td[headers="sa3"][data-rel="L1"]').text
    platne_hlasy = obsah_html.select_one('td[headers="sa6"][data-rel="L1"]').text
    
    seznam.append(kod_obec)
    seznam.append(jmeno_obce)
    seznam.append(volici_v_seznamu)
    seznam.append(vydane_obalky)
    seznam.append(platne_hlasy)
    vybirani_hodnot_ze_zbylych_tabulek(obsah_html)

    return seznam

def hlavni(url:str, jmeno_souboru:str):
    """
    Stáhne a zpracuje data z dané URL stránky s výsledky voleb, vytvoří CSV soubor
    s hlavičkou a datovými řádky pro jednotlivé obce.

    Funkce:
    - stáhne HTML obsah ze zadané `url`
    - najde všechny tabulkové buňky s třídou "cislo", které obsahují odkazy na obce
    - pro každou obec stáhne detailní stránku s výsledky
    - jednou na začátku vytvoří hlavičku CSV souboru pomocí `vytvoreni_hlavicky_soubrou`
    - postupně vytvoří data jednotlivých obcí pomocí `vytvoreni_radku_pro_zapis` a následné
      data pošle do `zapisovani_do_souboru`
    - pokud dojde k chybě při parsování konkrétní obce, chybu ignoruje a pokračuje dál

    Parametry:
        url (str): URL adresa stránky s přehledem obcí.
        jmeno_souboru (str): Název souboru CSV, do kterého se budou zapisovat data.

    Návratová hodnota:
        None
    """

    prvni = True
    zdrojak = requests.get(url, timeout=10)   
    obsah_souboru = bs4.BeautifulSoup(zdrojak.text, features="html.parser")
    radek_tabulky = obsah_souboru.select('td[class="cislo"]')

    for radek in radek_tabulky:
        try:
            cislo_obce = radek.select_one("a").text
            kousek_url_obce = radek.select_one("a").attrs["href"]
            url_obce = "https://www.volby.cz/pls/ps2017nss/" + kousek_url_obce
            zdroj_obce = requests.get(url_obce, timeout=10)
            obsah_html_obce = bs4.BeautifulSoup(zdroj_obce.text, features="html.parser")
            
            if prvni:
                hlavicka_souboru = vytvoreni_hlavicky_souboru(obsah_html_obce)
                zapisovani_do_souboru(jmeno_souboru, hlavicka_souboru)
                prvni = False
            
            radek_pro_zapis = vytvoreni_radku_pro_zapis(obsah_html_obce, cislo_obce, url)
            zapisovani_do_souboru(jmeno_souboru, radek_pro_zapis)

        except (AttributeError, IndexError):
            pass
    return

def kontrola_vstupu():
    """
    Zkontroluje platnost vstupních argumentů před spuštěním hlavního programu.

    Funkce:
    - načte první a druhý argument z příkazové řádky (`sys.argv`):
        1. URL odkaz (string)
        2. název výstupního souboru (string)
    - ověří, zda URL odkaz obsahuje platnou část URL ze seznamu platných odkazů
      stažených z webu "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ".
      Pokud není odkaz platný, program se ukončí.
    - ověří, zda má název výstupního souboru příponu ".csv".
      Pokud ne, program se ukončí.
    - pokud jsou obě kontroly úspěšné, vrátí tuple `(odkaz, jmeno_vystupniho_souboru)`.

    Návratová hodnota:
        tuple: (odkaz: str, jmeno_vystupniho_souboru: str) při platných vstupních datech.

    Výjimky:
        - Pokud jsou vstupy neplatné, funkce vypíše chybovou zprávu a ukončí program voláním `exit()`.
    """

    odkaz = sys.argv[1]
    hlavni_odkaz = requests.get("https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ")
    hlavni_obsah = bs4.BeautifulSoup(hlavni_odkaz.text, features="html.parser")
    radky_tabulky = hlavni_obsah.select("td.center")

    for radek in radky_tabulky:
        try:
            if radek.select_one("a").get("href") in odkaz:
                print("Správně zadaný odkaz.")
                break
        except:
            pass
    else:
        print("Nesprávný odkaz. Ukončuji program..")
        exit()
       
    jmeno_vystupniho_souboru = sys.argv[2]
    
    if jmeno_vystupniho_souboru[-4:] == ".csv":
        print("Správně zadaná přípona souboru.")
        return odkaz, jmeno_vystupniho_souboru
    else:
        print("Nesprávná přípona souboru. Ukončuji program..")
        exit()
    
    return

if __name__ == "__main__":

    url, jmeno_souboru = kontrola_vstupu()
    print("Zpracovávájí se výsledky, prosím neukončujte program...")
    hlavni(url, jmeno_souboru)
    print(f"Vysledky byly zapsany do {jmeno_souboru}.")