import openai
from dotenv import load_dotenv
import os
import time
import logging
from datetime import datetime
import json

load_dotenv()

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)  # Carga el contenido del archivo JSON en un diccionario
        return data

def read_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()  # Carga el contenido del archivo de texto
        return data

kavak_cars_data = read_json("kavak_data/sample_caso_ai_engineer.json")
kavak_business_data = read_txt("kavak_data/informacion_de_kavak.txt")

client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Updating the assistant with the vector storage
assistant = client.beta.assistants.update(
    assistant_id=os.environ["KAVAK_ASSISTANT_ID"], 
    name="Asistente de IA de Kavak",
    instructions=f'''
    Asistente de IA de Kavak para ayudar con atención al cliente.
    Esta es informacion de la empresa y el modelo de negocio de Kavak: {kavak_business_data}
    No puedes involucrarte en ninguna convesarción que no tenga que ver con autos y el negocio de Kavak.
    Dependiendo del auto por el que la persona se sienta interesada, seras capaz de otorgar 
    planes de financiamiento tomando como base el enganche, el precio
    del auto, una tasa de interés del 10% y plazos de financiamiento de entre 3 y 6 años.
    Informacion de nuestros vehiculos disponibles de los cuales deberas proporcionar informacion y buscar cerrar ventas: ꐕ{kavak_cars_data}ꐕ
    Importante, solamente brindaras informacion de los autos que se encuentran en el json delimitado entre los simbolos ꐕ.
    ''',
    model="gpt-4o",
)