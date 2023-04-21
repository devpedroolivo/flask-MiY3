from scipy.stats import norm
import requests
import json
import emoji
import time

#Informações do telegram
TOKEN = '5948587586:AAEcOOb5_BaFEHZmaabJuX0mK3yyOrHQZoo'
chat_id = '-930452902'

#Mensagens
message_alert = ''
message_gale_one = emoji.emojize('❗ Faça a 1º proteção❗')
message_gale_two = emoji.emojize('❗ Faça a 2º proteção❗')
message_green = emoji.emojize('✅✅✅')
message_lost = emoji.emojize('❌❌❌')

#Variáveis lógicas
isAlert = False
isGreen = False
isGaleOne = False
isGaleTwo = False

#String
data = ''
check_data = ''
last_id = ''

#URL'S
url_Telegram = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
url = "https://api.lavegas.bet/games/grau/history.php"

payload_status_code = ""
response_status_code = requests.request("GET", url, data=payload_status_code)
status_code = response_status_code.status_code

def get_api_data():
    payload = ""
    response = requests.request("GET", url, data=payload)
    data = json.loads(response.text)

    return data

def check_percent_data(data, values):
    global isAlert, isGaleOne, isGaleTwo ,isGreen, last_id, message_alert

    seq = values
    mean = sum(seq)/len(seq)
    std_dev = (sum([(i - mean)*2 for i in seq])/(len(seq)-1))*0.5
    prob = norm(mean, std_dev).sf(1.5)
    percent = prob * 100

    if (not isAlert and percent > 50):
        last_number = data[0]['final_multiplier']
        last_id = data[0]['id']
        message_alert = emoji.emojize(f'\n🚨OPORTUNIDADE ENCONTRADA EM {percent:.2f}%🚨\n\n🎰 Apostar após: {last_number}\n🚨 Sair em 1.50\n\n👩‍💻 ABRIR JOGO https://lavegas.bet/grau 👈🏻')

        params_Telegram = {'chat_id': chat_id, 'text': message_alert}
        response_Telegram = requests.post(url_Telegram, data=params_Telegram)

        isAlert = True
        isGreen = False

        time.sleep(10)

    if (isAlert and last_id != data[0]['id']):
        if (data[0]['final_multiplier'] > 1.50):
            params_Telegram = {'chat_id': chat_id, 'text': message_green}
            response_Telegram = requests.post(url_Telegram, data=params_Telegram)

            isGaleOne = False
            isGaleTwo = False
            isAlert = False
            isGreen = True

            time.sleep(30)
        elif (not isGreen and not isGaleOne):
            params_Telegram = {'chat_id': chat_id, 'text': message_gale_one}
            response_Telegram = requests.post(url_Telegram, data=params_Telegram)

            isGaleOne = True
        elif (not isGreen and isGaleOne and not isGaleTwo):
            params_Telegram = {'chat_id': chat_id, 'text': message_gale_two}
            response_Telegram = requests.post(url_Telegram, data=params_Telegram)

            isGaleTwo = True
        elif (not isGreen and isGaleOne and isGaleTwo):
            params_Telegram = {'chat_id': chat_id, 'text': message_lost}
            response_Telegram = requests.post(url_Telegram, data=params_Telegram)

            isGaleOne = False
            isGaleTwo = False
            isAlert = False

            time.sleep(30)

while True:
    payload_status_code = ""
    response_status_code = requests.request("GET", url, data=payload_status_code)
    status_code = response_status_code.status_code

    if (status_code == 200):
        data = get_api_data()
        values = [data['final_multiplier'] for data in data]

        if (data[0]['id'] != check_data):
            check_data = data[0]['id']
            check_percent_data(data, values)