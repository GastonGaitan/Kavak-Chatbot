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

model = "gpt-4o"

@app.route('/', methods=['POST'])
def process_message():
    # twilio procesa content-type -> application/x-www-form-urlencoded
    print(request)
    if request.method == 'POST':
        print(f"Request data: {request.get_data(as_text=True)}")
        # Get data from requests
        message_body = request.form.get('Body')
        from_number = request.form.get('From')
        to_number = request.form.get('To')

        print(f"Message Body: {message_body}")
        print(f"From: {from_number}")
        print(f"To: {to_number}")
        
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
        return f'Message sent to {to_number}' 

if __name__ == '__main__':
    app.run(debug=True)