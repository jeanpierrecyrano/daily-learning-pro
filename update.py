import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

modello_scelto = None
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        if 'flash' in m.name or 'pro' in m.name:
            modello_scelto = m.name
            break
if not modello_scelto:
    modello_scelto = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods][0]

model = genai.GenerativeModel(modello_scelto)

with open('index.html', 'r', encoding='utf-8') as file:
    current_html = file.read()

prompt = f"""
Sei un generatore di contenuti rigoroso. Devi aggiornare un file HTML di 17 sezioni.

REGOLA STRUTTURALE: Restituisci l'intero HTML da <!DOCTYPE html> a </html>. NON toccare i <button>, le classi, gli id o il tag <script>.
Modifica SOLO il testo dentro i <div class="theory-box"> (e i suoi id specifici) e i <div class="feedback-area">.

REGOLE CONTENUTI (Rispetta ESATTAMENTE le lunghezze e le richieste):

FORMATO QUIZ A SCELTA MULTIPLA (TASSATIVO):
Per Lingue, Chimica, Geografia, Storia, Corpo Umano, Sport, Rompicapi: scrivi la domanda e le opzioni nel theory-

