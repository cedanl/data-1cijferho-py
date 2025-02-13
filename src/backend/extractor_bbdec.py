import pandas as pd
import re
from pathlib import Path
from typing import List, Dict

def lees_bestand(bestandsnaam: str) -> List[str]:
    """Leest een tekstbestand en retourneert de inhoud als lijst van regels."""
    try:
        with open(bestandsnaam, encoding='latin1') as f:
            inhoud = f.readlines()
        if len(inhoud) == 0:
            raise Exception("Bestand is leeg of kan niet worden gelezen")
        return inhoud
    except Exception as e:
        raise Exception(f"Fout bij het lezen van bestand: {str(e)}")

def vind_decoderingssecties(inhoud: List[str]) -> List[Dict]:
    """Vindt alle decoderingssecties in de bestandsinhoud."""
    secties = []
    huidige_sectienaam = ""
    
    # Zoek eerst naar sectienamen die beginnen met "Dec"
    for i, regel in enumerate(inhoud):
        if regel.strip().startswith("Dec"):
            huidige_sectienaam = regel.strip()
            continue
            
        if regel.strip().endswith('='):
            # Als we een sectienaam hebben gevonden, verwerk de sectie
            if huidige_sectienaam:
                # Vind begin van sectie inhoud (eerste regel met data)
                start_inhoud = i + 1
                while start_inhoud < len(inhoud) and not inhoud[start_inhoud].strip():
                    start_inhoud += 1
                
                # Vind einde van sectie (volgende sectie kop of einde bestand)
                volgende_sectie = next((j for j in range(start_inhoud, len(inhoud)) 
                                    if inhoud[j].strip().startswith("Dec")), len(inhoud))
                
                secties.append({
                    'titel': huidige_sectienaam,
                    'inhoud': inhoud[start_inhoud:volgende_sectie],
                    'start_regel': start_inhoud,
                    'eind_regel': volgende_sectie
                })
    
    print("\nGevonden secties:")
    for sectie in secties:
        print(f"- {sectie['titel']} (regels {sectie['start_regel']} tot {sectie['eind_regel']})")
        if sectie['inhoud']:
            print("Voorbeeld inhoud:")
            for regel in sectie['inhoud'][:3]:
                print(f"  {regel.strip()}")
        else:
            print("  (geen inhoud)")
    
    return secties
    

def verwerk_sectie(sectie: Dict) -> pd.DataFrame:
    """Verwerkt een decoderingssectie naar een DataFrame."""
    data_list = []
    
    for regel in sectie['inhoud']:
        if len(regel.strip()) == 0:
            continue
            
        delen = [deel for deel in re.split(r'\s{2,}', regel.strip()) if deel]
        
        if len(delen) >= 3:
            data_list.append({
                'ID': len(data_list) + 1,
                'Naam': delen[0],
                'Start_Positie': int(delen[1]),
                'Aantal_Posities': int(delen[2])
            })
    
    df = pd.DataFrame(data_list)
    if not df.empty:
        df['ID'] = df['ID'].apply(lambda x: f"{sectie['titel']}_{x}")
        df = df.sort_values('Start_Positie')
    else:
        print(f"Waarschuwing: Sectie '{sectie['titel']}' bevat geen data")
    
    return df

def verwerk_bestanden(bestandsnaam: str) -> Dict[str, pd.DataFrame]:
    """Verwerkt een bestand met decoderingssecties."""
    inhoud = lees_bestand(bestandsnaam)
    secties = vind_decoderingssecties(inhoud)
    dataframes = {}
    
    for sectie in secties:
        df = verwerk_sectie(sectie)
        dataframes[sectie['titel']] = df
        
    return dataframes

def exporteer_dataframes(dataframes: Dict[str, pd.DataFrame], uitvoermap: str):
    """Exporteert de DataFrames naar CSV-bestanden."""
    Path(uitvoermap).mkdir(parents=True, exist_ok=True)

    print(dataframes.items())
    
    for tabel_naam, df in dataframes.items():
        print(tabel_naam)
        # Verwijder speciale tekens en spaties uit de tabelnaam
        bestandsnaam = Path(uitvoermap) / f"{tabel_naam.replace('=', '').replace(' ', '_')}.csv"
        df.to_csv(bestandsnaam, index=False)
        print(f"Exporteerde {bestandsnaam}")

if __name__ == "__main__":
    bestandsnaam = "Bestandsbeschrijving_Dec-bestanden.txt"
    uitvoermap = "data/"
    
    dataframes = verwerk_bestanden(bestandsnaam)
    exporteer_dataframes(dataframes, uitvoermap)