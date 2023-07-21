from flask import jsonify, request, render_template
from advice_web import app
from random import randint
import requests
import ssl

@app.route('/get_new_advice', methods=['POST'])
def new_advice():

    for _ in range(1):
        random_value = randint(1, 224)

    response = requests.get(f'https://api.adviceslip.com/advice/{random_value}')

    advice = response.json()['slip']['advice']

    return jsonify({'advice': advice})

@app.route('/', methods=['GET', 'POST'])
def index():

    for _ in range(1):
        random_value = randint(1, 224)
        print(random_value)

    response = requests.get(f'https://api.adviceslip.com/advice/{random_value}')

    advice = response.json()['slip']['advice']

    return render_template('index.html', advice=advice)

@app.route('/favoritos')
def fav_advice():
    return render_template('favoritos.html')