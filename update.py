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

REGOLA STRUTTURALE: Restituisci l'intero HTML da <!DOCTYPE html> a </html>. NON aggiungere formattazione markdown. NON toccare i <button>, le classi, gli id o il tag <script>.
Modifica SOLO il testo dentro i <div class="theory-box"> e i <div class="feedback-area">.

FORMATO QUIZ A SCELTA MULTIPLA (TASSATIVO E FONDAMENTALE):
Per Lingue, Chimica, Geografia, Storia, Corpo Umano, Sport e Rompicapi: OGNI singola domanda deve avere le sue opzioni avvolte in un <div class="options-group">.
Devi OBBLIGATORIAMENTE aggiungere data-correct="true" SOLO all'opzione esatta.
Esempio esatto:
Domanda del quiz?<br>
<div class="options-group">
    <span class="quiz-option">(A) Opzione Sbagliata</span>
    <span class="quiz-option" data-correct="true">(B) Opzione Esatta</span>
    <span class="quiz-option">(C) Opzione Sbagliata</span>
</div>

La breve spiegazione del perché la risposta è corretta va scritta nel <div class="feedback-area"> associato.

REGOLE SPECIFICHE SEZIONI:
1. Lingue (ans-1): Inglese e Spagnolo. Per ogni lingua: 1 parola di lessico, 1 tempo verbale spiegato, 1 quiz a scelta multipla (vedi FORMATO QUIZ). Soluzioni in ans-1.
2. Chimica (ans-2): Spiegazione in 10 righe di un argomento analitica/organica/ambientale. 1 quiz a scelta multipla. Soluzione/Spiegazione in ans-2.
3. Geografia (ans-3): Località italiana (5 righe), località mondo (5 righe). Inserisci il quiz bandiera ESATTAMENTE così nel theory-box: <img src="https://flagcdn.com/w160/XX.png" class="flag" alt="Bandiera"> (XX = codice ISO nazione minuscolo). Poi le 3 opzioni quiz sulla nazione in options-group. Soluzione in ans-3.
4. Storia (ans-4): Racconto storico di 10 righe + 1 quiz a scelta multipla. Soluzione in ans-4.
5. Corpo Umano (ans-5): Spiegazione di 10 righe + 1 quiz a scelta multipla. Soluzione in ans-5.
6. Sport (ans-6): 3 domande a scelta multipla sugli sport in generale. Usa un <div class="options-group"> separato per ogni domanda. Soluzioni in ans-6.
7. Cibo: 1 ricetta con ingredienti e piccola spiegazione sulla preparazione.
8. Cinema e Serie TV: Consiglio di 1 film e 1 serie tv.
9. Profumi e Candele: Spiegazione di 10 righe sulla teoria dei profumi o candele.
10. Curiosità: Curiosità generale in 10 righe (tono serio, NO barzellette).
11. Finanza Personale: Spiegazione in 5-10 righe su finanza, investimenti e come fare denaro.
12. Orto: Spiegazione in 10 righe su un argomento per l'orto.
13. Immobiliare: Spiegazioni, curiosità e consigli su come cercare casa.
14. Rompicapi (ans-14): 1 rompicapo. Sotto inserisci le 3 opzioni in options-group. Soluzione in ans-14.
15. Vestiti: Consigli di abbinamenti capi e colori **per un uomo di 30 anni** per fare bella figura in varie situazioni.
16. Soft Skill: Proponi 1 soft skill da imparare oggi con breve spiegazione.
17. Progetti: Bozze di progetti fattibili.

Codice HTML attuale da aggiornare:
{current_html}
"""

response = model.generate_content(prompt)
new_html = response.text.strip()

# Pulizia di sicurezza sicura per l'editor di GitHub
new_html = new_html.replace("```html", "")
new_html = new_html.replace("```", "")
new_html = new_html.strip()

with open('index.html', 'w', encoding='utf-8') as file:
    file.write(new_html)
