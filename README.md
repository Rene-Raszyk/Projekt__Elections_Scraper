# Elections Scraper

Třetí projekt do Engeto Online Python Akademie 
Autor: Rene Raszyk 
Email: 2004reno2004@gmail.com

## Popis

Tento nástroj slouží k automatickému stahování a analýze výsledků parlamentních voleb konaných v roce 2017.
Detailní výsledky najdete [zde](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ)

## Požadavky

- Python 3.8 nebo novější
- `pip` pro správu Python balíčků

## Instalace

**Naklonování repozitáře**

   ```bash
   git clone https://github.com/Rene-Raszyk/Projekt__Elections_Scraper.git
   cd Projekt__Election_Scraper
   ```

**Instalace knihoven**

   ```bash
   pip install -r requirements.txt
   ```

## Spuštění projektu

Pro spuštění souboru main.py z příkazového řádku je nutné zadat dva povinné argumenty.

   ```bash
   python main.py <odkaz_uzemního_celku> <jméno_souboru>
   ```

Výsledky se uloží jako soubor ve formátu .csv.

## Ukázka projektu

**Výsledky hlasování pro okres Karviná:**

1. argument: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8103
2. argument: vysledky_karvina.csv

**Spuštění programu:**

python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8103" "vysledky_karvina.csv"

**Průběh stahování:**

Správně zadaný odkaz.
Správně zadaná přípona souboru.
Zpracovávájí se výsledky, prosím neukončujte program...
Vysledky byly zapsany do vysledky_karvina.csv.

**Částečný výstup:**

code;location;registered;envelopes;valid;Občanská demokratická strana;...
598925;Albrechtice;3 173;1 957;1 944;109;4;2;181;2;131;211;15;22;12;1;3;139;0;5;25;635;1;1;174;0;10;1;0;255;5
599051;Bohumín;17 613;9 040;8 973;579;12;4;1 241;9;133;821;85;91;87;7;6;641;0;12;119;3 157;18;33;305;3;55;14;25;1 478;38
...

## Autor

- **Jméno:** Rene Raszyk  
- **Email:** 2004reno2004@gmail.com 