from flask import jsonify, request, render_template, flash, redirect, session
from advice_web import app
from advice_web.modules.config import responseAPI_ID, responseAPI_SEARCH
from advice_web.tools.functions import getNewAdvice, getAdviceList, getAllAdvices
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

            flash('Advice removed from favorite list', 'success')

    return redirect(request.referrer or '/')

@app.route('/', methods=['GET', 'POST'])
def index():
    for _ in range(1):
        random_value = randint(1, 224)

    response = requests.get(f'{responseAPI_ID}{random_value}')
    if response.ok:
        try:
            advice = response.json()
        except ValueError:
            flash('Invalid API response format.', 'error')

    return render_template('index.html', advice=advice)

@app.route('/favoritos')
def fav_advice():
    if 'fav_advice_ids' not in session:

        return render_template('favoritos.html')

    advices = getAdviceList(session['fav_advice_ids'])
    if not advices:
        flash('Sorry, no favorited advices found. To favorite an advice, check out the methods below.', 'info')

    return render_template('favoritos.html', advice=advices)

@app.route('/search', methods=['GET'])
def search_advice():
    inputSearch = request.args.get('tag', type=str)

    if inputSearch == None:
        all_results = getAllAdvices()

        return render_template('pesquisar.html', getAll=all_results)
    else:
        response = requests.get(f'{responseAPI_SEARCH}{inputSearch}')

        if response.ok:
            try:
                search = response.json()
                total_results = search.get('total_results')
                if total_results is None:
                    flash(f'Not found any advice with \"{inputSearch}\", please try another.', 'error')
                    return redirect('/search' or request.referrer)
            except ValueError:
                flash('Invalid API response format.', 'error')
        else:
            flash(f'API request failed with status code: {response.status_code}.', 'error')
            search = None

    return render_template('pesquisar.html', response_search=search)