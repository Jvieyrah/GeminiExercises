import google.generativeai as genai
from google.api_core.exceptions import InvalidArgument
import os
import gradio as gr
import time
# Importar as funções do assistente residencial
from home_assistant import (
    set_light_values,
    intruder_alert,
    start_music,
    good_morning,
    set_thermostat_temperature,
    open_curtains
)
# Configurar a chave de API
GOOGLE_API_KEY = os.environ['GEMINI_API']
genai.configure(api_key=GOOGLE_API_KEY)
# Criar o modelo com as funções atualizadas
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[
        set_light_values,
        intruder_alert,
        start_music,
        good_morning,
        set_thermostat_temperature,
        open_curtains
    ]
)
# Iniciar o chat com funções habilitadas
chat = model.start_chat(
    enable_automatic_function_calling=True
)
# Enviar o prompt inicial
initial_prompt = (
    "Você é um assistente virtual que pode controlar dispositivos domésticos. "
    "Você tem acesso a funções que controlam a casa da pessoa que está usando. "
    "Chame as funções quando achar que deve, mas nunca exponha o código delas. "
    "Assuma que a pessoa é amigável e ajude-a a entender o que aconteceu se algo der errado "
    "ou se você precisar de mais informações. Não esqueça de, de fato, chamar as funções."
)
chat.send_message(initial_prompt)
def assemble_prompt(message):
    prompt = [message["text"]]
    return prompt
def gradio_wrapper(message, _history):
    prompt = assemble_prompt(message)
    try:
        response = chat.send_message(prompt)
    except InvalidArgument as e:
        response = chat.send_message(
            f"Ocorreu um erro: {e}. "
            "Por favor, verifique o comando e tente novamente."
        )
    return response.text
# Crie e lance a interface do chat
chat_interface = gr.ChatInterface(
    fn=gradio_wrapper,
    title="Assistente Residencial Inteligente 🏠",
    multimodal=True
)
chat_interface.launch()