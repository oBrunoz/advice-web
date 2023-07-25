from flask import jsonify, request, session
from advice_web.modules.config import responseAPI_ID
import requests
from random import randint

def getNewAdvice(value:int=1):
    for _ in range(value):
        random_value = randint(1, 224)

    print(random_value)

    response = requests.get(f'{responseAPI_ID}{random_value}')

    if response.ok:
        advice = response.json()['slip']['advice']
        return {'advice': advice}
    else:
        return {'advice': 'Error: Unable to retrieve advice.'}

def getAdviceList(ids:list):
    advices = []

    for advice_id in ids:
        api_url = f'{responseAPI_ID}{advice_id}'
        response = requests.get(api_url)

        if response.ok:
            advice = response.json()
            advices.append(advice)

    return advices

def getAllAdvices():

    all_results = []

    for i in range(1, 6):
        response = requests.get(f'{responseAPI_ID}{i}')
        if response.ok:
            print('ok')
            advice_data = response.json()
            all_results.append(advice_data)

    return all_results