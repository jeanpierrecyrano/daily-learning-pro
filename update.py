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

1. REGOLE SUL CODICE (PER NON ROMPERE L'APP):
- DEVI restituire l'intero codice HTML da <!DOCTYPE html> fino a </html>.
- NON TOCCARE MAI, per nessun motivo, i tag <style> e <script>. Devono rimanere identici all'originale.
- NON MODIFICARE gli id, le classi CSS o i tag HTML strutturali.
- I bottoni interattivi (es. <button class="quiz-btn" onclick="...">) e il menu di navigazione DEVONO rimanere intatti.
- Cambia ESCLUSIVAMENTE il testo all'interno dei <div class="content-box"> e le soluzioni nei <div class="feedback-area">.

2. REGOLE SUI CONTENUTI (MASSIMA VARIETÀ):
- Livello lingue: Inglese B1/B2 (focus grammatica/lessico aziendale generico) e Spagnolo A2 (verbo del giorno e frasi utili).
- STILE: Accademico, informativo, diretto. NESSUNA barzelletta, nessuna battuta.
- ARGOMENTI: Scegli argomenti universali e generali. VARIAZIONE ESTREMA rispetto al giorno precedente. 
- DIVIETO ASSOLUTO: Non fare MAI riferimenti alla vita personale dell'utente. È vietato parlare di assorbenti, pannolini, laboratori, Crema, gatti, pianura padana o abbonamenti TV. Mantieni gli argomenti di chimica, geografia, storia, ecc., a un livello di cultura generale globale.

Restituisci SOLO il codice HTML puro. Non aggiungere "```html" all'inizio o alla fine.
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

