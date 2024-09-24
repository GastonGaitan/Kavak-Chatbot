from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai

app = Flask(__name__)

client = openai.OpenAI(api_key="sk-svcacct-ixqcwWtpjxabp64J4csqUGSqAl_bEr6VuRx-fJjbZx5p46EQp8BJE5li9er7yitaiayk0_YBc8RiUT3BlbkFJ9aT6iWGDSFldCuId9u_VcVskvRTJfPuK4SkzN3pyjgIyAezc_s_CrgWmr4glg3R9_oe8mK-uyoTjAA")

model = "gpt-4o"

@app.route('/', methods=['GET', 'POST'])
def process_message():
    response = MessagingResponse()
    response.message('Hola mundo desde el server de Flask de twilio')
    return str(response)

if __name__ == '__main__':
    app.run(debug=True)