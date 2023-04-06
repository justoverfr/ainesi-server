# import logging
from flask import Flask, request, jsonify
import os
# import requests
# from requests.structures import CaseInsensitiveDict

import modules.chatbot as chatbot

# from dotenv import load_dotenv

# load_dotenv()

# #! -------------------------------- A supprimer ------------------------------- #

# # Configure le niveau de journalisation
# logging.basicConfig(level=logging.DEBUG)
# #! ---------------------------------------------------------------------------- #

# default_response = "I don't understand."
# error_response = "An unknown error occurred. Please try again."


# app = Flask(__name__)


# @app.route('/dialogflow', methods=['POST'])
# def dialogflow():
#     """
#     Point d'entrée principal pour les requêtes Dialogflow.
#     Récupère le nom de l'intention et déclenche la fonction correspondante.

#     Returns:
#         str: La réponse de l'assistant virtuel.
#     """
#     req_data = request.get_json(force=True)
#     intent_name = req_data['queryResult']['intent']['displayName']

#     # Sélectionne la fonction à exécuter en fonction de l'intention
#     if intent_name == 'Default Welcome Intent':
#         response = welcome()
#     elif intent_name == 'Default Fallback Intent':
#         response = query_gpt(req_data['queryResult']['queryText'])
#     else:
#         response = default_response

#     # Renvoie la réponse au format JSON
#     return jsonify({'fulfillmentText': response})


# def welcome():
#     """
#     Gère l'intention "Default Welcome Intent".

#     Returns:
#         str: La réponse de l'assistant virtuel.
#     """
#     return "Hi, I am your virtual personal mental health assistant. How are you doing today?"


# def query_gpt(query):
#     """
#     Gère l'intention "Default Fallback Intent".
#     Interagit avec l'API GPT-3 pour obtenir une réponse adaptée à la requête de l'utilisateur.

#     Args:
#         query (str): La requête de l'utilisateur.

#     Returns:
#         str: La réponse générée par GPT-3.
#     """
#     # Configuration des en-têtes pour l'appel à l'API GPT-3
#     openai_api_key = os.environ.get("OPENAI_API_KEY")
#     headers = CaseInsensitiveDict()
#     headers["Content-Type"] = "application/json"
#     headers["Authorization"] = f"Bearer {openai_api_key}"

#     # Crée le dialogue pour l'API GPT-3
#     dialog = [
#         "The following is a conversation with an AI assistant that can have meaningful conversations with users. The assistant is helpful, empathic, and friendly. Its objective is to make the user feel better by feeling heard. With each response, the AI assisstant prompts the user to continue the conversation in a natural way.",
#         "AI: Hello, I am your personal mental health AI assistant. How are you doing today?",
#     ]
#     dialog.append(f"User: {query}")
#     dialog.append("AI:")

#     # Paramètres pour la requête à l'API GPT-3
#     completion_params = {
#         "prompt": "\n".join(dialog),
#         "max_tokens": 60,
#         "temperature": 0.7,
#         "n": 1,
#         "stream": False,
#         "logprobs": None,
#         "echo": False,
#         "stop": "\n",
#     }

#     # Effectue la requête à l'API GPT-3 et récupère la réponse
#     response = requests.post(
#         "https://api.openai.com/v1/engines/davinci/completions",
#         json=completion_params,
#         headers=headers,
#     )

#     #! -------------------------------- A SUPPRIMER ------------------------------- #
#     # Ajoute des instructions de journalisation pour afficher les informations sur la réponse de l'API GPT-3
#     logging.debug(f"Response status code: {response.status_code}")
#     logging.debug(f"Response content: {response.content}")
#     #! ---------------------------------------------------------------------------- #

#     # Traite la réponse de l'API GPT-3
#     if response.status_code == 200:
#         bot_response = response.json()["choices"][0]["text"].strip()
#     else:
#         bot_response = error_response

#     return bot_response


# from memory_search import MemorySearch
# import os
# from flask import Flask, request, jsonify


# @app.route('/', methods=['GET'])
# def home():
#     """
#     Affiche un message d'accueil sur la page d'accueil du serveur.

#     Returns:
#         str: Message d'accueil du serveur.
#     """
#     return "Bienvenue sur le serveur AINESI."


# # Lance l'application Flask
# if __name__ == '__main__':
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port)
app = Flask(__name__)


@app.route('/dialogflow', methods=['POST'])
def dialogflow():
    req_data = request.get_json(force=True)
    intent_name = req_data['queryResult']['intent']['displayName']

    if intent_name == 'Default Welcome Intent':
        response = welcome()
    elif intent_name == 'Default Fallback Intent':
        response = chatbot.get_response(
            req_data['queryResult']['queryText'])
    else:
        response = "I don't understand."

    return jsonify({'fulfillmentText': response})


def welcome():
    return "Hi, I am your virtual personal mental health assistant. How are you doing today?"


@app.route('/', methods=['GET'])
def home():
    """
    Affiche un message d'accueil sur la page d'accueil du serveur.

    Returns:
        str: Message d'accueil du serveur.
    """
    return "Bienvenue sur le serveur AINESI."


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
