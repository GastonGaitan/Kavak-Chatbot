from flask import Flask
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def process_message():
    response = MessagingResponse()
    response.message('Hola mundo desde el server de Flask de twilio')
    return str(response)

if __name__ == '__main__':
    app.run(debug=True)