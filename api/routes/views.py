from flask import jsonify, request, render_template, flash, redirect, session, url_for
from api import app
from api.modules.config import responseAPI_ID, responseAPI_SEARCH
from api.tools.functions import getNewAdvice, getAdviceList, getAllAdvices
import requests

@app.route('/get_new_advice', methods=['POST'])
def new_advice():
    advice = getNewAdvice()

    return jsonify(advice=advice['slip'])

@app.route('/checkFav/<int:id_advice>', methods=['POST'])
def favoriteAdvice(id_advice):
    if request.method == 'POST':
        checkedFav = request.form.get('checkFav')

        print(id_advice)
        try:
            if checkedFav:
                    # Adiciona o ID do "advice" ao array na sessão
                    if 'fav_advice_ids' not in session:
                        session['fav_advice_ids'] = [id_advice]
                    else:
                        session['fav_advice_ids'].append(id_advice)
                        print(session['fav_advice_ids'])
                    flash(f'Advice {id_advice} successfully added to favorite list', 'success')
            else:
                if 'fav_advice_ids' in session and id_advice in session['fav_advice_ids']:
                    session['fav_advice_ids'].remove(id_advice)
                    print(session['fav_advice_ids'])
                    flash(f'Advice {id_advice} removed from favorite list', 'warning')
                else:
                    flash('Sorry, we encountered an error while trying to add it to your favorites. Please try again later or contact an administrator for assistance.', 'info')
                    
        except KeyError as e:
            flash('An error occurred while accessing session data.', 'error')
            print(f"KeyError: {e}")
        except Exception as e:
            flash('An error ocurred, please try again.', 'error')
            print(f'Exception: {e}')
    
    return redirect(request.referrer or '/')

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        advice = getNewAdvice()
    except Exception as e:
        flash('An error ocurred, please try again or contat the administrator.', 'error')
        print(f'Exception: {e}')

    return render_template('index.html', advice=advice)

@app.route('/favorites')
def fav_advice():
    if 'fav_advice_ids' not in session:
        flash('Sorry, no favorited advices found. To favorite an advice, check out the methods below.', 'info')
        return render_template('favoritos.html')

    advices = getAdviceList(session['fav_advice_ids'])

    if not advices:
        print('FOi')
        flash('Sorry, no favorited advices found. To favorite an advice, check out the methods below.', 'info')

    return render_template('favoritos.html', advice=advices)

@app.route('/search', methods=['GET'])
def search_advice():
    inputSearch = request.args.get('tag', type=str)

    if inputSearch is None:
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
            if response.status_code == 404:
                print('bad request: 404')    
            else:
                flash(f'API request failed with status code: {response.status_code}.', 'error')
            search = None

    return render_template('pesquisar.html', response_search=search)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error_handler/404.html', error=error), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('505.html', error=error), 500

if __name__ == '__main__':
    app.run(debug=True)