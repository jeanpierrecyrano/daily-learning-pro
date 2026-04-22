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
Sei un sistema automatizzato di aggiornamento per una Web-App didattica avanzata.
Ecco il codice HTML attuale:
{current_html}

COMPITO:
Aggiorna i contenuti didattici per la giornata di oggi seguendo QUESTE REGOLE TASSATIVE:

1. REGOLE SUL CODICE (STRUTTURA):
- Restituisci l'intero codice HTML. Non aggiungere "```html" all'inizio o alla fine.
- NON TOCCARE MAI i tag <style>, <script>, o i bottoni <button>. La logica deve rimanere intatta.
- Inserisci la soluzione dei quiz ESATTAMENTE all'interno dei tag <div class="feedback-area"> già presenti.

2. REGOLE SUI CONTENUTI (LUNGHEZZA, COMPLESSITÀ E SPECIFICITÀ):
- LUNGHEZZA MASSIMA: I contenuti DEVONO essere lunghi, strutturati e complessi. Usa paragrafi ampi, elenchi puntati, spiegazioni dettagliate e sviscera ogni argomento a livello universitario/professionale. NON ESSERE SINTETICO.
- LINGUE (Inglese B1/B2 e Spagnolo A2): Inserisci letture lunghe e articolate (almeno 150 parole), spiegazioni grammaticali approfondite, lessico avanzato e frasi contestualizzate. Inserisci il quiz finale e metti la risposta nel div nascosto.
- CHIMICA: Scendi nel dettaglio tecnico, molecolare e industriale. Spiega i meccanismi di reazione, l'impatto ambientale o le applicazioni pratiche con linguaggio scientifico rigoroso.
- GEOGRAFIA (BANDIERE): Mostra SEMPRE l'immagine della bandiera usando ESATTAMENTE questo tag HTML: <img src="[https://flagcdn.com/w160/XX.png](https://flagcdn.com/w160/XX.png)" alt="Bandiera" style="display:block; margin: 10px auto; max-width: 120px; border: 1px solid #ccc; border-radius: 4px;"> (Sostituisci "XX" con il codice ISO a 2 lettere minuscolo della nazione).
- FINANZA PERSONALE: Tratta argomenti complessi e specifici (es. analisi macroeconomica, funzionamento degli ETF, bias cognitivi negli investimenti, tassazione). Nessuna ovvietà sul risparmio base.
- CIBO/RICETTA: Scrivi la ricetta in modo estremamente dettagliato: dosi precise, procedimenti passo-passo lunghi, tempi di cottura e magari il principio chimico/fisico dietro la preparazione.
- DIVIETO ASSOLUTO DI BARZELLETTE: Niente ironia, battute o freddure in nessuna sezione. Mantenere un tono 100% serio, accademico e divulgativo.

Cambia solo il testo dentro i <div class="content-box"> e le soluzioni nei <div class="feedback-area">, riempiendoli con contenuti lunghi e di altissima qualità.

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

