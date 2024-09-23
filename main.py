import os
from dotenv import load_dotenv  # Asegúrate de importar la librería
from twilio.rest import Client

# Cargar las variables desde el archivo .env
load_dotenv()

# Acceder a las variables de entorno
account_sid = os.environ['ACCOUNT_SID']
auth_token = os.environ['AUTH_TOKEN']
client = Client(account_sid, auth_token)

from_whatsapp_number = 'whatsapp:' + os.environ["TWILIO_NUMBER"]

print(from_whatsapp_number)

message = client.messages.create(
    from_=from_whatsapp_number,
    body='Hola mundo desde Twilio probando probando',
    to='whatsapp:+5493487235569'
)

print(message.sid)
