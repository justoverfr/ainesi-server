from flask import Flask, request, jsonify
from flask_cors import CORS
import os

import openai
import pinecone

import modules.chatbot as chatbot

from dotenv import load_dotenv
load_dotenv()

# --------------------------------- api keys --------------------------------- #
openai.api_key = os.environ.get("OPENAI_API_KEY")
pinecone.init(os.environ.get("PINECONE_API_KEY"), environment='us-east4-gcp')

PORT = 5000

app = Flask(__name__)
CORS(app)


@app.route('/chatbot', methods=['POST'])
def converse():
    """
    Receive a message from the user and send a response.

    Returns:
        str: Response.
    """
    # receive the message from the user
    req_data = request.get_json(force=True)
    user_message = req_data['queryResult']['queryText']

    # send the message to the chatbot and get the response
    response = chatbot.get_response(user_message)

    # send the response to the user
    return jsonify({'fulfillmentText': response})


@app.route('/', methods=['GET'])
def home():
    """
    Display a message.

    Returns:
        str: Message.
    """
    return "AINESI Server"


if __name__ == '__main__':
    port = int(os.environ.get("PORT", PORT))
    app.run(host='0.0.0.0', port=port)
