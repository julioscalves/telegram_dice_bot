import os
import random
import requests

import utils

from flask import Flask
from flask.globals import request


TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
SUBMIT_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'


app = Flask(__name__)


@app.route('/updates', methods=['GET', 'POST'])
def updates() -> dict:
    if request.is_json:
        request_object = request.json

        text = request_object['message']['text']
        chat_id = request_object['message']['from']['id']
        result = {}

        message = ''

        if '/start' in text:
            message = (
                'Olá\n\nSou um bot programado para rolar dados, o que é muito útil para jogar RPG 😄\n\n'
                'Basta usar o comando /roll xdy para rolar os dados. Só substituir o <strong>x</strong> pela quantidade e o <strong>y</strong> pelo tipo de dado.\n\n'
                'Por exemplo: /roll 1d20\n\n'
                'Também posso rolar dados para o Sistema Storyteller, usado na série World of Darkness. Pra isso, basta usar o comando /wod numero_de_dados dificuldade\n\n'
                'Por exemplo: /wod 6 6 para rolar 6d10 com dificuldade 6!'
            )
        
        elif '/roll' in text or '/wod' in text:
            if '/roll' in text:
                result = utils.parse_dice(text)

            elif '/wod' in text:
                result = utils.parse_wod(text)

            message = utils.assemble_message(result)

        else:
            message = 'Foi mal, mas não entendi esse comando!'

        if len(message) > 0:
            payload = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }

            post = requests.post(SUBMIT_URL, data=payload)

            return post

if __name__ == '__main__':
    app.run(debug=False)
