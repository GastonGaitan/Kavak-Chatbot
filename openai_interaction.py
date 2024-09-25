import openai
from dotenv import load_dotenv
import os
import time
import logging
from datetime import datetime
import json

load_dotenv()

client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

kavak_assistant_id = os.environ["KAVAK_ASSISTANT_ID"]

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)  # Carga el contenido del archivo JSON en un diccionario
        return data

def write_json(file_path, data):
    """Escribir el diccionario actualizado en el archivo JSON."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def add_number_and_thread_if_not_exists(file_path, number, message):
    # Leer el archivo JSON
    data = read_json(file_path)
    # Verificar si el número ya está en el diccionario
    if number not in data:
        thread = openai_create_thread(client, number, message)
        # Si no está, agregar el número y el thread
        data[number] = thread
        # Escribir los cambios de vuelta al archivo JSON
        write_json(file_path, data)
        print(f'Se agregó {number}: {thread} al archivo JSON.')
    else:
        print(f'El número {number} ya existe en el archivo JSON con el thread {data[number]}.')

def get_thread_id(file_path, number):
    json_data = read_json(file_path)
    thread_id = json_data.get(number)
    return thread_id

def openai_create_thread(client, number, message):
    thread = client.beta.threads.create(
        messages=[{"role": "user", "content": message}],
    )
    thread_id = thread.id
    print(f"thread_id = {thread_id}")
    return thread_id

def openai_wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    #print("entered wait_for_run_completion")
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                return response  # Ensure the response is returned
        except Exception as e:
            print(f"An error occurred while retrieving the run: {e}")
            break
        print("waiting for run to complete...")
        time.sleep(sleep_interval)

def openai_send_message(client, thread_id, assistant_id, message):
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message,
    )
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )
    response = openai_wait_for_run_completion(client, thread_id, run.id)
    return response

def use_openai(number, message):
    add_number_and_thread_if_not_exists("conversation_data/numbers_thread.json", number, message)
    thread = get_thread_id("conversation_data/numbers_thread.json", number)
    response = openai_send_message(client, thread, kavak_assistant_id, message)
    print(f"Response: {response}")
    return response

