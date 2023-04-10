import openai
import re
from time import time, sleep
import requests
from requests.structures import CaseInsensitiveDict

import modules.util as util
import modules.memory as memory

gpt_logs_folder_path = "gpt_logs"
logs_folder_path = "logs"


def generate_response(message_vector):
    max_retry = 5
    retry = 0

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {openai.api_key}"

    context = memory.load_context_logs(message_vector, logs_folder_path)
    messages = memory.get_logs_messages(context)

    prompt = util.open_file('prompt.txt')
    prompt = prompt.replace('<<LANGUAGE>>', 'french')
    prompt = prompt.replace('<<OPENNESS>>', '10')
    prompt = prompt.replace('<<CONSCIENTIOUSNESS>>', '10')
    prompt = prompt.replace('<<EXTRAVERSION>>', '10')
    prompt = prompt.replace('<<AGREEABLENESS>>', '10')
    prompt = prompt.replace('<<NEUROTICISM>>', '10')
    prompt = prompt.replace('<<COUNTRY>>', "France")

    prompt_message = {"role": "system", "content": prompt}
    messages.insert(0, prompt_message)
    print(messages)

    while True:
        try:
            # Paramètres pour la requête à l'API GPT-3
            completion_params = {
                "model": "gpt-3.5-turbo",
                "messages": messages,
                "max_tokens": 256,
                "temperature": 0.1,
                "top_p": 1.0,
                "frequency_penalty": 0.5,
                "presence_penalty": 1.0,
                "n": 1,
                "stream": False,
                "stop": ['USER:', 'ASSISTANT:'],
            }

            # Effectue la requête à l'API GPT-3 et récupère la réponse
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                json=completion_params,
                headers=headers,
            )

            ai_response = response.json(
            )['choices'][0]['message']['content'].strip()

            ai_response = re.sub('[\r\n]+', '\n', ai_response)
            ai_response = re.sub('[\t ]+', ' ', ai_response)

            # Enregistre la conversation dans les logs du bot
            filename = '%s_gpt.txt' % time()
            messages_string = "\n".join(
                [f"{message['role']}: {message['content']}" for message in messages])
            util.save_file(filename, messages_string + "\nassistant: " + ai_response,
                           gpt_logs_folder_path)

            # Retourne la réponse de GPT-3
            return ai_response

        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)


def get_response(user_input):
    input_vector = memory.get_embeddings(user_input)
    memory.save_log("user", user_input, input_vector, logs_folder_path)

    response = generate_response(input_vector)

    response_vector = memory.get_embeddings(response)
    memory.save_log("assistant", response, response_vector, logs_folder_path)

    return response
