from flask import jsonify, request, render_template, flash, redirect, session
from advice_web import app
from advice_web.modules.config import responseAPI_ID, responseAPI_SEARCH
from advice_web.tools.functions import getNewAdvice, getAdviceList
from random import randint
import requests
import ssl

advice = getNewAdvice()

@app.route('/get_new_advice', methods=['POST'])
def new_advice():
    adviceValue = getNewAdvice()

    return adviceValue

@app.route('/checkFav/<int:id_advice>', methods=['POST'])
def favoriteAdvice(id_advice):
    if request.method == 'POST':
        checkedFav = request.form.get('checkFav')

        if checkedFav:
            # Adiciona o ID do "advice" ao array na sessão
            if 'fav_advice_ids' not in session:
                session['fav_advice_ids'] = [id_advice]
            else:
                session['fav_advice_ids'].append(id_advice)
                print(session['fav_advice_ids'])
            flash('Advice successfully added to favorite list', 'success')
        else:
            if 'fav_advice_ids' in session and id_advice in session['fav_advice_ids']:
                session['fav_advice_ids'].remove(id_advice)
                print(session['fav_advice_ids'])

            flash('Advice removed from favorite list', 'error')

    return redirect('/')

@app.route('/', methods=['GET', 'POST'])
def index():
    for _ in range(1):
        random_value = randint(1, 224)

    response = requests.get(f'{responseAPI_ID}{random_value}')
    advice = response.json()

    return render_template('index.html', advice=advice)

@app.route('/favoritos')
def fav_advice():
    if 'fav_advice_ids' not in session:
        return render_template('favoritos.html')
    
    sessionValue = session['fav_advice_ids']

    advices = getAdviceList(session['fav_advice_ids'])

    return render_template('favoritos.html', advice=advices)

@app.route('/pesquisar', methods=['GET'])
def search_advice():
    inputSearch = request.args.get('search', type=str).strip()

    if inputSearch != None:
        print(inputSearch)

        response = requests.get(f'{responseAPI_SEARCH}{inputSearch}')

        if response.ok:
            search = response.json()
            print('NUMERO DE VALORES: ', search['slips'])
    else:
        print('Valor de input veio como None')

    return render_template('pesquisar.html', response_search=search)