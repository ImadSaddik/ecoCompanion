import os
from dotenv import load_dotenv

import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings

import chainlit as cl
from chainlit.input_widget import Slider

import google.generativeai as genai


class GeminiEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        model = 'models/embedding-001'
        title = "Custom query"
        return genai.embed_content(model=model,
                                   content=input,
                                   task_type="retrieval_document",
                                   title=title)["embedding"]


config = {
    'max_output_tokens': 128,
    'temperature': 0.9,
    'top_p': 0.9,
    'top_k': 50,
}

interface_started = False


@cl.on_chat_start
async def start():
    setUpGoogleAPI()
    loadVectorDataBase()

    settings = await cl.ChatSettings(
        [
            Slider(
                id="temperature",
                label="Temperature",
                initial=config['temperature'],
                min=0,
                max=1,
                step=0.1,
            ),
            Slider(
                id="top_p",
                label="Top P",
                initial=config['top_p'],
                min=0,
                max=1,
                step=0.1,
            ),
            Slider(
                id="top_k",
                label="Top K",
                initial=config['top_k'],
                min=0,
                max=100,
                step=1,
            ),
            Slider(
                id="max_output_tokens",
                label="Max output tokens",
                initial=config['max_output_tokens'],
                min=0,
                max=1024,
                step=1,
            )
        ]
    ).send()

    await setup_agent(settings)


def setUpGoogleAPI():
    load_dotenv()

    api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=api_key)


def loadVectorDataBase():
    chroma_client = chromadb.PersistentClient(path="./database/")

    db = chroma_client.get_or_create_collection(
        name="sme_db", embedding_function=GeminiEmbeddingFunction())

    cl.user_session.set('db', db)


@cl.on_settings_update
async def setup_agent(settings):
    global interface_started
    print("Setup agent with following settings: ", settings)

    config['temperature'] = float(settings['temperature'])
    config['top_p'] = float(settings['top_p'])
    config['top_k'] = int(settings['top_k'])
    config['max_output_tokens'] = int(settings['max_output_tokens'])

    model = genai.GenerativeModel(
        model_name="gemini-pro", generation_config=config)

    if cl.user_session.get('chat') is None:
        print("Creating new chat")
        chat = model.start_chat(history=[])
        cl.user_session.set('chat', chat)
    else:
        print("Using existing chat")
        model.start_chat(history=cl.user_session.get('chat').history)


@cl.on_message
async def main(message):
    chat = cl.user_session.get('chat')

    passages = get_relevant_passage(message.content, cl.user_session.get('db'))
    prompt = make_prompt(message.content, convert_pasages_to_list(passages))
    chat.send_message(prompt)

    await cl.Message(content=chat.last.text).send()


def get_relevant_passage(query, db):
    passages = db.query(query_texts=[query], n_results=10)['documents'][0]
    return passages


def make_prompt(query, relevant_passage):
    escaped = relevant_passage.replace(
        "'", "").replace('"', "").replace("\n", " ")

    prompt = ("""
              Vous êtes un expert utile et informatif qui répond aux questions liés à l'environnement. Assurez-vous de répondre par une phrase complète et comprenant toutes les informations générales pertinentes. Cependant, vous vous adressez à un public non spécialisé, alors assurez-vous de décomposer les concepts compliqués et adoptez un ton amical et conversationnel.
              
              QUESTION : '{query}'
              PASSAGE : '{relevant_passage}'
              
              ANSWER:
              """).format(query=query, relevant_passage=escaped)

    return prompt


def convert_pasages_to_list(passages):
    context = ""

    for passage in passages:
        context += passage + "\n"

    return context
