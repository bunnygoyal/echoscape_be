import openai
import whisper
from flask import Flask, request, request
from generation import get_dalle_prompt,generate_dalle_image, transcribe_audio

app = Flask(__name__)
openai.api_key = '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' #my key

@app.route('/api/generate_image', methods=['POST'])
def generate_image():
    print(request.form.keys())
    if 'audio_path' not in request.form:
        return {'message':'bad request'},401
    whisper_output = transcribe_audio(base_model,request.form['audio_path'])
    gpt_output = get_dalle_prompt(whisper_output)
    dalle_output = generate_dalle_image(gpt_output)
    print(gpt_output)
    return {'image_link':dalle_output},200

if __name__ == "__main__":
    base_model = whisper.load_model('base')
    app.run()


