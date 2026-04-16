import os
import google.generativeai as genai
from datetime import datetime

# Connessione al modello
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-pro')

# Legge il sito attuale
with open('index.html', 'r', encoding='utf-8') as file:
    current_html = file.read()

# Istruzioni per Gemini
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
