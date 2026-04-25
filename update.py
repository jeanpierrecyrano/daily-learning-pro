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
Per Lingue, Chimica, Geografia, Storia, Corpo Umano, Sport, Rompicapi: scrivi la domanda e le opzioni nel theory-box usando <span class="quiz-option"> per ogni opzione (A), (B), (C)). Esempio:
Domanda del quiz?<br>
<span class="quiz-option">(A) Opzione A</span>
<span class="quiz-option">(B) Opzione B</span>
<span class="quiz-option">(C) Opzione C</span>

Soluzioni nel <div class="feedback-area"> associato.

REGOLE SPECIFICHE SEZIONI:
1. Lingue (id="quiz-languages", ans-1): Inglese e Spagnolo. Per ogni lingua: 1 parola di lessico, 1 tempo verbale con breve spiegazione, 1 quiz a completamento frase a scelta multipla (vedi FORMATO QUIZ). Soluzioni in ans-1.
2. Chimica (id="quiz-chemistry", ans-2): Spiegazione riassunta in 10 righe di un argomento (alterna tra analitica, organica o ambientale). Aggiungi 1 quiz a scelta multipla (vedi FORMATO QUIZ). Soluzione in ans-2.
3. Geografia (id="geography-content", ans-3): Località italiana da scoprire (5 righe), località nel mondo (5 righe). Inserisci il quiz bandiera ESATTAMENTE così: <img src="https://flagcdn.com/w160/XX.png" class="flag" alt="Bandiera"> (Sostituisci XX con il codice ISO nazione minuscolo). Risposta nazione in ans-3.
4. Storia (id="quiz-history", ans-4): Racconto storico di 10 righe + 1 quiz a scelta multipla (vedi FORMATO QUIZ). Soluzione in ans-4.
5. Corpo Umano (id="quiz-human", ans-5): Spiegazione di 10 righe + 1 quiz a scelta multipla (vedi FORMATO QUIZ). Soluzione in ans-5.
6. Sport (id="quiz-sport", ans-6): 3 domande a scelta multipla sugli sport in generale (vedi FORMATO QUIZ). Soluzioni in ans-6.
7. Cibo: 1 ricetta con ingredienti e piccola spiegazione sulla preparazione.
8. Cinema e Serie TV: Consiglio di 1 film e 1 serie tv (nuovi ogni giorno).
9. Profumi e Candele: Spiegazione di 10 righe sulla teoria dei profumi o candele.
10. Curiosità: Curiosità generale in 10 righe (tono rigoroso, NO barzellette).
11. Finanza Personale: Spiegazione in 5-10 righe su finanza, investimenti e come fare denaro.
12. Orto: Spiegazione in 10 righe su un argomento per l'orto.
13. Immobiliare: Spiegazioni, curiosità e consigli su come cercare/trovare casa.
14. Rompicapi (id="quiz-riddle", ans-14): 1 rompicapo (difficoltà media, vedi FORMATO QUIZ). Soluzione in ans-14.
15. Vestiti: Consigli di abbinamenti capi e colori **per un uomo di 30 anni** per fare bella figura in varie situazioni.
16. Soft Skill: Proponi 1 soft skill da imparare per oggi con breve spiegazione.
17. Progetti: Bozze di progetti fattibili da prendere in considerazione (presente o futuro).

Codice HTML attuale da aggiornare:
{current_html}
"""

response = model.generate_content(prompt)
new_html = response.text.strip()

if new_html.startswith("
http://googleusercontent.com/immersive_entry_chip/0
http://googleusercontent.com/immersive_entry_chip/1
http://googleusercontent.com/immersive_entry_chip/2
