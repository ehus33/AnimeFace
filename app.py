from flask import Flask, render_template, send_file
import os
import tensorflow as tf
from PIL import Image
import numpy as np

app = Flask(__name__)

generator = tf.keras.models.load_model('DCGEN.h5')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate')
def generate_image():
    noise = tf.random.normal([1, 300])
    
    generated_image = generator(noise, training=False)
    
    generated_image = (generated_image * 255).numpy().astype(np.uint8)
    generated_image = Image.fromarray(generated_image[0])
    
    image_path = os.path.join('static', 'generated_image.png')
    generated_image.save(image_path)
    
    return send_file(image_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
