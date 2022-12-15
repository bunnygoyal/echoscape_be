import os
import openai
import whisper
from flask import Flask, request, request
from generation import get_dalle_prompt,generate_dalle_image, transcribe_audio
from flask_cors import CORS;

app = Flask(__name__)
CORS(app)
openai.api_key = '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' #my key

@app.route('/api/generate_image', methods=['POST'])
def generate_image():
    print(request.files['audio_path'])
    if 'audio_path' not in request.files:
        return {'message':'bad request'},401

    dirname = os.path.dirname("audios")
    save_path = os.path.join(dirname, "temp.wav")
    request.files['audio_path'].save(save_path)
    whisper_output = transcribe_audio(base_model,save_path)
    gpt_output = get_dalle_prompt(whisper_output)
    dalle_output = generate_dalle_image(gpt_output)
    print(gpt_output)
    return {'image_link':dalle_output,'transcribed_text':whisper_output},200

if __name__ == "__main__":
    base_model = whisper.load_model('base')
    app.run()


