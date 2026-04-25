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
Modifica SOLO il testo dentro i <div class="theory-box"> e i <div class="feedback-area">. I quiz a scelta multipla DEVONO essere scritti come testo semplice (A) ... B) ... C) ...) nel theory-box, e le soluzioni vanno nei feedback-area.

REGOLE CONTENUTI (Rispetta ESATTAMENTE le lunghezze e le richieste):
1. Lingue (ans-1): Inglese e Spagnolo. Per ogni lingua: 1 parola di lessico, 1 tempo verbale con breve spiegazione, 1 quiz a completamento frase a scelta multipla. Soluzioni in ans-1.
2. Chimica (ans-2): Spiegazione riassunta in 10 righe di un argomento (alterna tra analitica, organica o ambientale). Aggiungi 1 quiz a scelta multipla. Soluzione in ans-2.
3. Geografia (ans-3): Località italiana da scoprire (5 righe), località nel mondo (5 righe). Inserisci il quiz bandiera ESATTAMENTE così nel theory-box: <img src="https://flagcdn.com/w160/XX.png" style="max-width:120px;" alt="Bandiera"> (XX = codice ISO nazione). Risposta nazione in ans-3.
4. Storia (ans-4): Racconto storico di 10 righe + 1 quiz a scelta multipla. Soluzione in ans-4.
5. Corpo Umano (ans-5): Spiegazione di 10 righe + 1 quiz a scelta multipla. Soluzione in ans-5.
6. Sport (ans-6): 3 domande a scelta multipla sugli sport in generale. Soluzioni in ans-6.
7. Cibo: 1 ricetta con ingredienti e piccola spiegazione sulla preparazione.
8. Cinema e Serie TV: Consiglio di 1 film e 1 serie tv (nuovi ogni giorno).
9. Profumi e Candele: Spiegazione di 10 righe sulla teoria dei profumi o candele.
10. Curiosità: Curiosità generale in 10 righe.
11. Finanza Personale: Spiegazione in 5-10 righe su finanza, investimenti e come fare denaro.
12. Orto: Spiegazione in 10 righe su un argomento per l'orto.
13. Immobiliare: Spiegazioni, curiosità e consigli su come cercare/trovare casa.
14. Rompicapi (ans-14): 1 rompicapo (difficoltà media). Soluzione in ans-14.
15. Vestiti: Consigli di abbinamenti capi e colori per fare bella figura a 30 anni in varie situazioni.
16. Soft Skill: Proponi 1 soft skill da imparare per oggi con breve spiegazione.
17. Progetti: Bozze di progetti fattibili da prendere in considerazione (presente o futuro).

Codice HTML attuale:
{current_html}
"""

response = model.generate_content(prompt)
new_html = response.text.strip()

if new_html.startswith("
http://googleusercontent.com/immersive_entry_chip/0
http://googleusercontent.com/immersive_entry_chip/1
http://googleusercontent.com/immersive_entry_chip/2
