import requests
from bs4 import BeautifulSoup
import re
import random

def estrai_risultati():
    url = "https://www.parlamento.it/1063"
    list_partiti = []

    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        partiti = soup.find_all(class_="partito")
        partiti_list = [e.get_text(strip=True) for e in partiti]

        for partito in partiti_list:
            list_partiti.append(partito)
    except:
        return "Errore nella richiesta al sito."
    
        # URL della pagina Wikipedia (Partiti politici italiani)
    # Useremo sempre lo stesso URL di esempio
    URL = "https://it.wikipedia.org/wiki/Partiti_politici_italiani"
    # Il nuovo selettore CSS
    CSS_SELECTOR_1 = "td:nth-of-type(2) > a"
    CSS_SELECTOR_2 = ".mw-content-ltr > ul li"

    # --- 1. Ottenere il contenuto della pagina ---
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(URL, headers=headers)
        response.raise_for_status() 

        html_content = response.text

    except requests.exceptions.RequestException as e:
        print(f"Errore nella richiesta: {e}")
        exit()

    # --- 2. Analizzare il contenuto e trovare gli elementi ---
    soup = BeautifulSoup(html_content, 'html.parser')

    def estrai_risultati(CSS_SELECTOR):
        # Utilizza il metodo .select() con il nuovo selettore
        anchors = soup.select(CSS_SELECTOR)

        # --- 3. Estrarre e stampare testo ---
        for i, anchor in enumerate(anchors):
            # Estrai il testo visibile
            text = anchor.get_text(strip=True)
            list_partiti.append(text)

    estrai_risultati(CSS_SELECTOR_1)
    estrai_risultati(CSS_SELECTOR_2)
    print(list_partiti)


    list_partiti = [p for p in list_partiti if p.strip() != ""]

    preposizioni_articoli = {
        "di","a","da","in","con","su","per","tra","fra",
        "il","lo","la","i","gli","le","l","un","uno","una",
        "del","dello","della","dei","degli","delle",
        "al","allo","alla","ai","agli","alle",
        "dal","dallo","dalla","dai","dagli","dalle",
        "nel","nello","nella","nei","negli","nelle",
        "sul","sullo","sulla","sui","sugli","sulle",
        "col","coi"
    }

    preposizioni_articoli_per_partito = []

    for partito in list_partiti:
        tokens = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ']+", partito)
        trovati = []

        for tok in tokens:
            t = tok.lower()
            if t in preposizioni_articoli:
                trovati.append(t)
            elif t.startswith(("d'", "l'", "all'")):
                prefix = t.split("'")[0] + "'"
                trovati.append(prefix)

        filtered = []
        for item in trovati:
            idx = partito.lower().find(item.lower())
            if idx > 0 and idx + len(item) < len(partito):
                if partito[idx - 1] == " " and partito[idx + len(item)] == " ":
                    filtered.append(item)

        if filtered:
            preposizioni_articoli_per_partito.append(" ".join(filtered))

    risultati = []
    for mid in preposizioni_articoli_per_partito:
        for partito in list_partiti:
            if mid in partito:
                idx = partito.lower().find(mid.lower())
                if idx != -1:
                    estratto = partito[idx:].strip()
                    risultati.append(estratto)

    if not risultati:
        return "Nessun risultato disponibile."

    def restituisci_partito():
        first_word = random.choice(list_partiti)
        second_word = random.choice(risultati)
        while True:
            third_word = random.choice(risultati)
            if third_word != second_word:
                break
        third_word = random.choice(risultati)

        # ⚠️ RESTITUISCE SOLO LA STRINGA RICHIESTA
        return first_word + " " + second_word + " " + third_word

    restituisci_partito()
