import os
import tempfile
import googletrans
import speech_recognition as sr
import gtts
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    translated_text = None
    audio_file = None

    if request.method == 'POST':
        input_lang = request.form['input_lang']
        output_lang = request.form['output_lang']

        recognizer = sr.Recognizer()
        translator = googletrans.Translator()
        text = ''

        try:
            with sr.Microphone() as source:
                print('Speak Now')
                voice = recognizer.listen(source)
                text = recognizer.recognize_google(voice, language=input_lang)
                print(text)
        except Exception as e:
            print("Error:", e)

        if text:
            translated = translator.translate(text, dest=output_lang)
            print(translated.text)
            converted_audio = gtts.gTTS(translated.text, lang=output_lang)
            with tempfile.NamedTemporaryFile(delete=True) as fp:
                temp_filename = fp.name + '.mp3'
                converted_audio.save(temp_filename)
                translated_text = translated.text
                audio_file = temp_filename

    return render_template('index.html', translated_text=translated_text, audio_file=audio_file)

@app.route('/get_audio/<path:filename>')
def get_audio(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
