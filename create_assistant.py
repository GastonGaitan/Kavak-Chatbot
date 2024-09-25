import openai
from dotenv import load_dotenv
import os
import time
import logging
from datetime import datetime
import json

load_dotenv()

client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)  # Carga el contenido del archivo JSON en un diccionario
        return data

kavak_data = read_json("kavak_data/sample_caso_ai_engineer.json")

print(kavak_data)

# Assistant creation
kavak_ai_assistant = client.beta.assistants.create(
    name="Asistente de IA de Kavak",
    instructions=f'''
    Asistente de IA de Kavak para ayudar con atención al cliente.
    Kavak es una empresa de venta de autos usados en línea de la más alta calidad.
    No puedes involucrarte en ninguna convesarción que no tenga que ver con autos y el negocio de Kavak.
    Estas entrenado con información de los autos  de Kavak.
    Debes buscar cerrar ventas de autos y dar información sobre los autos de Kavak.
    Dependiendo del auto por el que la persona se sienta interesada, seras capaz de otorgar 
    planes de financiamiento tomando como base el enganche, el precio
    del auto, una tasa de interés del 10% y plazos de financiamiento de entre 3 y 6 años.
    Informacion de nuestros vehiculos disponibles de los cuales deberas proporcionar informacion: ꐕ{kavak_data}ꐕ
    Importante, solamente brindaras informacion de los autos que se encuentran en el json delimitado entre los simbolos ꐕ.
    ''',
    model="gpt-4o",
    tools=[{"type":"file_search"}]
)

kavak_assistant_id = kavak_ai_assistant.id
print(f"kavak_ai_assistant.id = {kavak_ai_assistant.id}")
