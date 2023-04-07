# import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
# import requests
# from requests.structures import CaseInsensitiveDict

import modules.chatbot as chatbot

from dotenv import load_dotenv


app = Flask(__name__)
CORS(app)


@app.route('/dialogflow', methods=['POST'])
def dialogflow():
    req_data = request.get_json(force=True)
    intent_name = req_data['queryResult']['intent']['displayName']

    if intent_name == 'Default Welcome Intent':
        response = welcome()
    elif intent_name == 'CustomIntent' or intent_name == 'Default Fallback Intent':
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
    # load_dotenv()

    # openai_api_key = os.environ.get("OPENAI_API_KEY")
    # pinecone_api_key = os.environ.get("PINECONE_API_KEY")

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
