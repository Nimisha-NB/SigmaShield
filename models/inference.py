from numpy import ndarray
from typing import Tuple, List, Dict, Union
from flask import Flask, request, jsonify
from typing import List
import re
from huggingface_hub import hf_hub_download
import fasttext

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


if __name__ == '__main__':
    app.run(port=4000)
