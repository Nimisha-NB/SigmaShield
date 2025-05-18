import re
import io
import fasttext
from PIL import Image
from numpy import ndarray
from apple_ocr.ocr import OCR
from flask import Flask, request, jsonify
from typing import Tuple, List, Dict, Union
from huggingface_hub import hf_hub_download

app = Flask(__name__)

model = fasttext.load_model(hf_hub_download(
    "kenhktsui/code-natural-language-fasttext-classifier", "model_quantized.bin"))

def replace_newlines(text: str) -> str:
    return re.sub("\n+", " ", text)

def parse_labels_probs(
    data: Tuple[List[List[str]], List[ndarray]],
    remove_prefix: str = '__label__'
) -> Dict[str, Union[List[Dict[str, float]], Dict[str, float]]]:
    labels, probs = data

    parsed_dict = {
        label[0].replace(remove_prefix, ''): float(prob[0])
        for label, prob in zip(labels, probs)
    }

    return {
        'dict': parsed_dict
    }

def prediction(text_list: List[str]) -> List[dict]:
    text_list = [replace_newlines(text) for text in text_list]
    pred = model.predict(text_list)
    ans = parse_labels_probs(pred)
    return ans['dict']

@app.route('/predict', methods=['POST'])
def predict_route():
    data = request.json
    text = data["text"]
    if not text:
        return jsonify({"error": "No texts provided"}), 400
    predictions = prediction([text])
    return jsonify(predictions)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    image = Image.open(io.BytesIO(file.read()))
    
    ocr_instance = OCR(image=image)
    text = ocr_instance.recognize()

    content_lines = []
    current_line = []

    for i in range(len(text['Content'])):
        if i == 0:
            current_line.append(text['Content'][i])
        else:
            if abs(text['y'][i] - text['y'][i - 1]) < 0.0025:
                current_line.append(text['Content'][i])
            else:
                content_lines.append(" ".join(current_line))
                current_line = [text['Content'][i]]

    if current_line:
        content_lines.append(" ".join(current_line))

    return jsonify({'text': "\n".join(content_lines)})

if __name__ == '__main__':
    app.run(port=4000)
