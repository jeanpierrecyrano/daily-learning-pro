import os
import google.generativeai as genai

# Connessione al sistema
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Ricerca automatica del modello migliore
modello_scelto = None
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        if 'flash' in m.name or 'pro' in m.name:
            modello_scelto = m.name
            break

if not modello_scelto:
    modello_scelto = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods][0]

model = genai.GenerativeModel(modello_scelto)

# Legge il sito attuale
with open('index.html', 'r', encoding='utf-8') as file:
    current_html = file.read()

# ISTRUZIONI BLINDATE PER L'INTELLIGENZA ARTIFICIALE
prompt = f"""
Sei un sistema automatizzato di aggiornamento per una Web-App didattica.
Ecco il codice HTML attuale:
{current_html}

COMPITO:
Aggiorna i contenuti didattici per la giornata di oggi seguendo QUESTE REGOLE TASSATIVE:

1. REGOLE SUL CODICE:
- Restituisci l'intero codice HTML. Non aggiungere "```html" all'inizio o alla fine.
- NON TOCCARE MAI i tag <style>, <script>, o i bottoni <button>.

2. REGOLE SUI CONTENUTI (DA RISPETTARE TASSATIVAMENTE):
- LINGUE: Inserisci la teoria e aggiungi un piccolo quiz. La soluzione del quiz DEVE andare dentro i tag <div id="eng-ans" class="feedback-area"> e <div id="spa-ans" class="feedback-area">.
- GEOGRAFIA: Mostra l'immagine della bandiera usando ESATTAMENTE questo tag HTML: <img src="[https://flagcdn.com/w160/XX.png](https://flagcdn.com/w160/XX.png)" alt="Bandiera" style="display:block; margin: 10px auto; max-width: 120px; border: 1px solid #ccc; border-radius: 4px;"> (Sostituisci "XX" con il codice ISO a 2 lettere minuscolo della nazione, es. "it" per Italia, "mx" per Messico). Metti il nome della nazione dentro il <div id="geo-ans" class="feedback-area">.
- FINANZA PERSONALE: ESTREMA VARIETÀ. Ogni giorno devi trattare un micro-argomento completamente diverso: mercati azionari, obbligazioni storiche, tassi d'interesse BCE, criptovalute, ETF, tassazione, bias comportamentali. VIETATO ripetere i concetti di risparmio base.
- DIVIETO DI BARZELLETTE E BATTUTE: È severamente vietato generare ironia, barzellette o freddure nella sezione curiosità o altrove. Mantieni un tono 100% accademico e divulgativo. Sezione 10 è per le curiosità storiche/scientifiche universali.

Cambia solo il testo dentro i <div class="content-box"> e le soluzioni nei <div class="feedback-area">.
"""

response = model.generate_content(prompt)
new_html = response.text.strip()

# Pulizia di sicurezza nel caso l'AI inserisca tag markdown
if new_html.startswith("```html"):
    new_html = new_html[7:]
if new_html.endswith("```"):
    new_html = new_html[:-3]
if new_html.startswith("```"):
    new_html = new_html[3:]

# Salva e sovrascrive il sito web
with open('index.html', 'w', encoding='utf-8') as file:
    file.write(new_html.strip())

