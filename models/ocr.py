from flask import Flask, request, jsonify
from apple_ocr.ocr import OCR
from PIL import Image
import io

app = Flask(__name__)

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
    app.run(debug=True)
