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
        message_id = request_object['message']['message_id']
        result = {}

        message = ''

        if '/start' in text:
            message = (
                'Olá\n\nSou um bot programado para rolar dados, o que é muito útil para jogar RPG 😄\n\n'
                'Basta usar o comando /roll xdy para rolar os dados. Só substituir o <strong>x</strong> pela quantidade e o <strong>y</strong> pelo tipo de dado.\n\n'
                'Por exemplo: <code>/roll 1d20</code>\n\n'
                'Também posso rolar dados para o Sistema Storyteller, usado na série World of Darkness. Pra isso, basta usar o comando /wod numero_de_dados dificuldade\n\n'
                'Por exemplo: <code>/wod 6</code> para rolar 6d10 com dificuldade 6!'
            )

        if '/help' in text:
            message = (
                'Os comandos disponíveis são:\n\n'
                '<strong>/roll</strong>: Faz rolagem de qualquer tipo de dado. É possível adicionar modificadores às rolagens.\n'
                '<strong>Exemplos de uso:</strong>\n'
                '<code>/roll 1d20</code>: joga 1d20 normal\n'
                '<code>/roll 1d12+1d4</code>: joga 1d12 e soma o resultado a 1d4\n'
                '<code>/roll 1d8-1</code>: joga 1d8 e remove -1 do resultado\n\n'
                '<strong>/wod</strong>: Faz rolagens para o Sistema Storyteller (d10) e conta os sucessos com base na dificuldade, que, por padrão, é 6.\n'
                '<strong>Exemplos de uso:</strong>\n'
                '<code>/wod 6</code>: joga 6d10 e conta os sucessos\n'
                '<code>/roll 6 8</code>: joga 6d10 com dificuldade 8\n\n'
                '<strong>IMPORTANTE</strong>\n'
                'O uso de modificadores é exclusivo do comando /roll. Não é recomendado utilizar modificadores com qualquer outro comando, como /wod.\n\n'
                'Acertos críticos a todos!'
            )
        
        elif '/roll' in text or '/wod' in text and len(text.split()) > 1 and len(text.split()) < 4:
            if '/roll' in text:
                result = utils.parse_dice(text)

            elif '/wod' in text:
                result = utils.parse_wod(text)

            if 'status' in result.keys() and result['status'] != 'fail':
                message = 'Teve algo de errado nesse comando aí. Se tiver com dúvidas, use o comando /help!'

            else:
                message = utils.assemble_message(result)

        else:
            message = 'Foi mal, mas não entendi esse comando!'

        if len(message) > 0:
            payload = {
                'reply_to_message_id': message_id,
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }

            post = requests.post(SUBMIT_URL, data=payload)

            return {
                'status': post.status_code
            } 

if __name__ == '__main__':
    app.run(debug=True)
