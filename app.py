from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os
from dotenv import load_dotenv  # Asegúrate de importar la librería
from twilio.rest import Client
from openai_interaction import use_openai

# Cargar las variables desde el archivo .env
load_dotenv()

app = Flask(__name__)

openai_client = openai.OpenAI(api_key="sk-svcacct-ixqcwWtpjxabp64J4csqUGSqAl_bEr6VuRx-fJjbZx5p46EQp8BJE5li9er7yitaiayk0_YBc8RiUT3BlbkFJ9aT6iWGDSFldCuId9u_VcVskvRTJfPuK4SkzN3pyjgIyAezc_s_CrgWmr4glg3R9_oe8mK-uyoTjAA")

model = "gpt-4o"

@app.route('/', methods=['GET', 'POST'])
def process_message():
    # twilio procesa content-type -> application/x-www-form-urlencoded
    print(request)
    # Si es una petición POST, imprime los datos
    if request.method == 'POST':
        # Aquí puedes procesar el request
        print(f"Request data: {request.get_data(as_text=True)}")
        # Obtener datos del formulario
        message_body = request.form.get('Body')
        from_number = request.form.get('From')
        to_number = request.form.get('To')

        print(f"Message Body: {message_body}")
        print(f"From: {from_number}")
        print(f"To: {to_number}")
        # Retornar una respuesta
        
        kavak_assistant_response = use_openai(from_number, message_body)

        account_sid = os.environ['ACCOUNT_SID']
        auth_token = os.environ['AUTH_TOKEN']

        twilio_client = Client(account_sid, auth_token)

        message = twilio_client.messages.create(
            from_=to_number,
            body=kavak_assistant_response,
            to=from_number
        )

        print(message.sid)
        return 'Message sent to {}'.format(to_number) 

if __name__ == '__main__':
    app.run(debug=True)