from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from PIL import Image
import numpy as np

app = Flask(__name__)
CORS(app)

def load_model():
    # Ensure this path is correct relative to where app.py is executed
    model = tf.keras.models.load_model('model.h5')
    return model

model = load_model()

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        try:
            image = Image.open(file).convert('L')
            image = image.resize((28, 28))
            image = np.array(image)
            image = image / 255.0
            image = np.expand_dims(image, axis=0)
            image = np.expand_dims(image, axis=-1)
            prediction = model.predict(image)
            result = 'AI-generated' if prediction[0][0] > 0.5 else 'Human-generated'
            return jsonify({'prediction': result})
        except Exception as e:
            return jsonify({'error': str(e)})
    return jsonify({'error': 'Invalid file format'})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
