import os
import google.generativeai as genai
from datetime import datetime

# Connessione al sistema
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# RICERCA AUTOMATICA DEL MODELLO (Addio Errore 404)
modello_scelto = None
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        # Cerca preferibilmente il modello Flash o Pro disponibile per il tuo account
        if 'flash' in m.name or 'pro' in m.name:
            modello_scelto = m.name
            break

# Se non trova nomi specifici, prende il primo modello di testo valido in assoluto
if not modello_scelto:
    modello_scelto = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods][0]

model = genai.GenerativeModel(modello_scelto)

# Legge il sito attuale
with open('index.html', 'r', encoding='utf-8') as file:
    current_html = file.read()

# Istruzioni per la generazione
prompt = f"""
Oggi è il {datetime.now().strftime('%d/%m/%Y')}.
Ecco il codice HTML del Daily Learning Pro attuale:
{current_html}

COMPITO:
1. Sposta tutta la teoria di oggi delle 17 sezioni nell'Archivio Storico Integrale, mantenendo rigorosamente la divisione per materie e copiando parola per parola.
2. Genera contenuti completamente nuovi e approfonditi per le 17 sezioni di oggi.
3. Restituisci SOLO il nuovo codice HTML completo e aggiornato. Non aggiungere "```html" all'inizio o alla fine, fornisci solo il codice puro.
"""

response = model.generate_content(prompt)
new_html = response.text.strip()

# Pulisce eventuali tag di formattazione
if new_html.startswith("```html"):
    new_html = new_html[7:]
if new_html.endswith("```"):
    new_html = new_html[:-3]

# Salva e sovrascrive il sito web
with open('index.html', 'w', encoding='utf-8') as file:
    file.write(new_html.strip())
