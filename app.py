from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os
from dotenv import load_dotenv  # Asegúrate de importar la librería
from twilio.rest import Client

# Cargar las variables desde el archivo .env
load_dotenv()

app = Flask(__name__)

client = openai.OpenAI(api_key="sk-svcacct-ixqcwWtpjxabp64J4csqUGSqAl_bEr6VuRx-fJjbZx5p46EQp8BJE5li9er7yitaiayk0_YBc8RiUT3BlbkFJ9aT6iWGDSFldCuId9u_VcVskvRTJfPuK4SkzN3pyjgIyAezc_s_CrgWmr4glg3R9_oe8mK-uyoTjAA")

model = "gpt-4o"

@app.route('/', methods=['GET', 'POST'])
def process_message():
    print(request)
    # Si es una petición POST, imprime los datos
    if request.method == 'POST':
        # Aquí puedes procesar el request
        print(f"Request data: {request.get_data(as_text=True)}")
        # Retornar una respuesta
        return 'POST request processed', 200
    # if request.method == 'POST':
    #     account_sid = os.environ['ACCOUNT_SID']
    #     auth_token = os.environ['AUTH_TOKEN']

    #     # agregar manejo de errores
    #     data = request.get_json()

    #     client = Client(account_sid, auth_token)
    #     msg_to = data['msg_to']
    #     msg_body = data['msg_body']
    #     from_whatsapp_number = 'whatsapp:' + os.environ["TWILIO_NUMBER"]

    #     message = client.messages.create(
    #         from_=from_whatsapp_number,
    #         body=msg_body,
    #         to=msg_to
    #     )

    #     print(message.sid)
    #     return 'Message sent to {}'.format(msg_to) 

if __name__ == '__main__':
    app.run(debug=True)