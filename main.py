import os
import io

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vision', methods=['POST'])
def vision():
    from google.cloud import vision
    from google.cloud.vision import types

    client = vision.ImageAnnotatorClient()

    ing_file = request.files['imageupload']
    content = ing_file.read()
    image = types.Image(content=content)
    
    response = client.text_detection(image=image)
    texts = response.text_annotations
    ingredients = []
    for i in range(len(texts)):
        if('INGREDIENTS:' == texts[i].description):
            for x in range(i, len(texts)):
                ingredients.append(texts[x].description)
            break

    return render_template('index.html', ing=ingredients)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 3000)
