import os
import openai
import re
from time import time, sleep
from uuid import uuid4
import pinecone
import requests
from requests.structures import CaseInsensitiveDict

import modules.utils as utils

from dotenv import load_dotenv

load_dotenv()


# ---------------------------------------------------------------------------- #
#                                   Variables                                  #
# ---------------------------------------------------------------------------- #
convo_length = 30
# --------------------------------- api keys --------------------------------- #
openai.api_key = os.environ.get("OPENAI_API_KEY")
pinecone.init(os.environ.get("PINECONE_API_KEY"), environment='us-east4-gcp')


pinecone_index_name = 'ainesi'
vector_database = pinecone.Index(pinecone_index_name)

logs_folder_path = "logs"

response_cache = []
cache_size = 5

#! Supprime tous les vecteurs de Pinecone
# pinecone_index = pinecone.Index(pinecone_index_name)

# pinecone_index.delete(delete_all=True)
# print("finito")


def gpt3_embedding(content: str, engine='text-embedding-ada-002'):
    # fix any UNICODE errors
    content = content.encode(encoding='ASCII', errors='ignore').decode()
    response = openai.Embedding.create(input=content, engine=engine)
    vector = response['data'][0]['embedding']  # this is a normal list
    return vector


def load_conversation(results):
    result = list()
    for m in results['matches']:
        info = utils.load_json(logs_folder_path + '/%s.json' % m['id'])
        if info is not None:
            result.append(info)

    if not result:
        return None

    # sort them all chronologically
    # ordered = sorted(result, key=lambda d: d['time'], reverse=False)
    # messages = [i['message'] for i in ordered]
    # return '\n'.join(messages).strip()

    ordered = sorted(result, key=lambda d: d['time'], reverse=False)
    messages = [f"{i['speaker']}: {i['message']}" for i in ordered]
    return '\n'.join(messages).strip()


def generate_response(message: str):
    max_retry = 5
    retry = 0
    message = message.encode(encoding='ASCII', errors='ignore').decode()

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {openai.api_key}"

    temp = 0.0

    while True:
        try:
            # Paramètres pour la requête à l'API GPT-3
            completion_params = {
                "prompt": message,
                "max_tokens": 400,
                "temperature": temp,
                "top_p": 1.0,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0,
                # "n": 1,
                # "stream": False,
                # "logprobs": None,
                # "echo": False,
                "stop": ['USER:', 'AInesi:'],
            }

            # Effectue la requête à l'API GPT-3 et récupère la réponse
            response = requests.post(
                "https://api.openai.com/v1/engines/davinci/completions",
                json=completion_params,
                headers=headers,
            )

            ai_response = response.json()['choices'][0]['text'].strip()
            ai_response = re.sub('[\r\n]+', '\n', ai_response)
            ai_response = re.sub('[\t ]+', ' ', ai_response)

            # Vérifiez si la réponse est déjà dans le cache
            if ai_response not in response_cache:
                # Ajoutez la réponse au cache et supprimez la réponse la plus ancienne si nécessaire
                response_cache.append(ai_response)
                if len(response_cache) > cache_size:
                    response_cache.pop(0)

                # Enregistre la conversation dans les logs du bot
                filename = '%s_gpt.txt' % time()
                if not os.path.exists('gpt_logs'):
                    os.makedirs('gpt_logs')
                utils.save_file('gpt_logs/%s' % filename, message +
                                '\n\n==========\n\n' + ai_response)

                # Retourne la réponse de GPT-3
                return ai_response

            else:
                print(
                    "La réponse est déjà dans le cache, génération d'une nouvelle réponse...")
                # Augmentation de la température pour générer une nouvelle réponse
                # completion_params["temperature"] += 0.1
                temp += 0.1

        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)


def get_response(user_input):
    # get user input, save it, vectorize it, save to pinecone
    payload = list()

    timestamp = time()
    timestring = utils.timestamp_to_datetime(timestamp)
    # message = '%s: %s - %s' % ('USER', timestring, a)
    message = user_input
    vector = gpt3_embedding(message)

    unique_id = str(uuid4())
    metadata = {'speaker': 'USER', 'time': timestamp,
                'message': message, 'timestring': timestring, 'uuid': unique_id}
    utils.save_json(logs_folder_path + '/%s.json' % unique_id, metadata)
    payload.append((unique_id, vector))
    # search for relevant messages, and generate a response
    results = vector_database.query(vector=vector, top_k=convo_length)
    # results should be a DICT with 'matches' which is a LIST of DICTS, with 'id'
    conversation = load_conversation(results)
    if conversation is None:
        conversation = ""

    prompt = utils.open_file('prompt_response.txt').replace(
        '<<CONVERSATION>>', conversation).replace('<<MESSAGE>>', user_input)
    # generate response, vectorize, save, etc
    output = generate_response(prompt)

    timestamp = time()
    timestring = utils.timestamp_to_datetime(timestamp)
    # message = '%s: %s - %s' % ('AInesi', timestring, output)

    message = output
    vector = gpt3_embedding(message)
    unique_id = str(uuid4())
    metadata = {'speaker': 'AInesi', 'time': timestamp,
                'message': message, 'timestring': timestring, 'uuid': unique_id}
    utils.save_json(logs_folder_path + '/%s.json' % unique_id, metadata)
    payload.append((unique_id, vector))
    vector_database.upsert(payload)
    # print('\n\AInesi: %s' % output)
    return output
