import os
import google.generativeai as genai

# Configurazione API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Selezione modello automatica per trovare il più performante
modello_scelto = None
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        if 'flash' in m.name or 'pro' in m.name:
            modello_scelto = m.name
            break
if not modello_scelto:
    modello_scelto = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods][0]

model = genai.GenerativeModel(modello_scelto)

# Legge il file HTML esistente (deve chiamarsi index.html)
with open('index.html', 'r', encoding='utf-8') as file:
    current_html = file.read()

# ISTRUZIONI DI FERRO PER L'IA
prompt = f"""
Sei un docente universitario e formatore avanzato. Devi aggiornare un file HTML didattico composto da 17 sezioni.

REGOLA FONDAMENTALE STRUTTURALE:
Restituisci ESATTAMENTE l'intero file HTML da <!DOCTYPE html> a </html>. NON aggiungere formattazione markdown come ```html all'inizio o alla fine.
NON modificare assolutamente i tag <style>, <script>, le classi CSS, l'id degli elementi o i bottoni (<button>).
Modifica ESCLUSIVAMENTE il testo all'interno dei div con classe "theory-box" e "feedback-area".

REGOLE SUI CONTENUTI (TASSATIVE):
1. LUNGHEZZA E COMPLESSITÀ: I contenuti devono essere estremamente prolissi, ricchi di dettagli tecnici, linguaggio accademico e professionale. Scrivi testi lunghi e non sintetizzare nulla.
2. DIVIETO DI BARZELLETTE E IRONIA: È ASSOLUTAMENTE VIETATO usare barzellette, battute, freddure o ironia in QUALSIASI sezione (specialmente nella sezione 10 Curiosità). Il tono deve rimanere 100% formale, scientifico e divulgativo.
3. LINGUE (Sez 1): Testi molto lunghi in Inglese B1/B2 e Spagnolo A2 con vocabolario e teoria. Inserisci quiz finali. Le risposte ai quiz DEVONO essere scritte ESATTAMENTE nel <div id="ans-1" class="feedback-area">.
4. BANDIERE E GEOGRAFIA (Sez 3): Nel "theory-box" di questa sezione DEVI SEMPRE inserire l'immagine della bandiera usando ESATTAMENTE questo tag: <img src="[https://flagcdn.com/w160/XX.png](https://flagcdn.com/w160/XX.png)" style="display:block; margin: 10px auto; max-width: 120px; border: 1px solid #ccc; border-radius: 4px;" alt="Bandiera"> dove XX è il codice nazione ISO minuscolo a due lettere (es. it, no, jp). Metti la nazione e la capitale nel <div id="ans-3" class="feedback-area">.
5. FINANZA (Sez 11): Argomenti sempre DIVERSI e COMPLESSI (Macroeconomia, ETF, Titoli di Stato, Tassazione, Inflazione Sistemica, Bias comportamentali). VIETATO ripetere i banali concetti di "risparmio base".
6. QUIZ STORIA E SPORT: Per le sezioni 4 (Storia) e 6 (Sport), scrivi le domande nel "theory-box" e le relative risposte corrette nel "feedback-area" associato.

Codice HTML attuale da aggiornare:
{current_html}
"""

response = model.generate_content(prompt)
new_html = response.text.strip()

# Pulizia di sicurezza da markdown residuo
if new_html.startswith("```html"):
    new_html = new_html[7:]
elif new_html.startswith("```"):
    new_html = new_html[3:]
if new_html.endswith("```"):
    new_html = new_html[:-3]

# Sovrascrittura e salvataggio
with open('index.html', 'w', encoding='utf-8') as file:
    file.write(new_html.strip())
