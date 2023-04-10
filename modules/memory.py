import openai
import pinecone
import os

from uuid import uuid4
from time import time

import modules.util as util

from dotenv import load_dotenv
load_dotenv()

context_size = 30
memory_size = 10
pinecone_index_name = 'ainesi'

pinecone.init(os.environ.get("PINECONE_API_KEY"), environment='us-east4-gcp')
vector_database = pinecone.Index(pinecone_index_name)


def get_embeddings(text: str, engine='text-embedding-ada-002'):
    """
    Get the vector embedding of a text.

    Args:
        text (str): Text to vectorize.
        engine (str, optional): Engine to use. Defaults to 'text-embedding-ada-002'.

    Returns:
        list: Vector embedding of the text.
    """
    # * fix any UNICODE errors
    text = text.encode(encoding='ASCII', errors='ignore').decode()

    response = openai.Embedding.create(input=text, engine=engine)
    vector = response['data'][0]['embedding']
    return vector


def save_log(speaker, message, message_vector, logs_folder_path=''):
    """
    Save the log of a message.

    Args:
        speaker (str): Speaker of the message.
        message (str): Message.
        message_vector (list): Vector embedding of the message.
        logs_folder_path (str, optional): Path to the logs folder. Defaults to ''.
    """
    unix_time = time()
    timestring = util.get_time_string(unix_time)

    unique_id = str(uuid4())
    metadata = {'speaker': speaker, 'message': message, 'conversation_id': '1234',
                'time': unix_time, 'timestring': timestring, 'uuid': unique_id}

    util.save_json('%s.json' % unique_id,
                   data=metadata, folder_path=logs_folder_path)

    vector = [{
        "id": unique_id,
        "values": message_vector,
        "metadata": metadata
    }]

    vector_database.upsert(vector)


def load_context_logs(message_vector, logs_folder_path):
    """
    Load the logs related to the message vector.

    Args:
        message_vector (list): Vector embedding of the message.
        logs_folder_path (str): Path to the logs folder.

    Returns:
        list: List of related logs.
    """
    vector_results = vector_database.query(
        vector=message_vector,
        top_k=context_size,
        include_values=True,
        include_metadata=True,
        filter={"conversation_id": "1234"}
    )

    result = vector_results['matches']

    ordered = sorted(
        result, key=lambda d: d['metadata']['time'], reverse=False)
    return ordered


def load_previous_conversation():
    """
    Load the x most recent logs.
    """


def get_logs_messages(logs):
    """
    Convert logs to a list of messages readable by the chatbot.

    Args:
        logs (list): List of logs.

    Returns:
        list: List of messages in the following format: [{"role": "user", "content": "Hello!"}, ...]
    """
    logs_info = [i['metadata'] for i in logs]

    messages = [{"role": i['speaker'],
                 "content": i['message']} for i in logs_info]
    return messages
