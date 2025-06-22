import time
import google.generativeai as genai
from google.api_core.exceptions import InvalidArgument
import os
import gradio as gr
genai.configure(api_key=os.environ["GEMINI_API"])
initial_prompt = (
    "Você é um assistente culinário inteligente e amigável. Seu papel é ajudar usuários a encontrar receitas com base nos ingredientes que eles têm disponíveis, fornecer instruções passo a passo para o preparo dos pratos, dar dicas de culinária e responder a dúvidas sobre técnicas, substituições de ingredientes, tempo de cozimento e armazenamento de alimentos."

"Seja sempre claro, objetivo e cordial. Quando sugerir uma receita, inclua os seguintes itens:"

"Nome do prato"

"Ingredientes com quantidades"

"Modo de preparo passo a passo"

"Tempo de preparo e rendimento"

"Se o usuário fornecer ingredientes, sugira receitas possíveis com o que ele tem. Caso não haja ingredientes, pergunte o que a pessoa tem na despensa."

"Também ofereça dicas de cozinha quando solicitado, como técnicas de corte, formas de conservar alimentos, dicas de tempero, ou substituições comuns."

"Sempre que possível, adapte suas sugestões ao contexto do usuário (por exemplo, refeições rápidas, pratos vegetarianos, sem glúten, etc.)."


)
model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=initial_prompt)
chat = model.start_chat()

def assemble_prompt(message):
   prompt = [message["text"]]
   uploaded_files = upload_files(message)
   prompt.extend(uploaded_files)
   return prompt

def upload_files(message):
    uploaded_files = []
    if message["files"]:
        for file_gradio_data in message["files"]:
            uploaded_file = genai.upload_file(file_gradio_data["path"])
            while uploaded_file.state.name == "PROCESSING":
                time.sleep(5)
                uploaded_file = genai.get_file(uploaded_file.name)
            uploaded_files.append(uploaded_file)
    return uploaded_files
def gradio_wrapper(message, _history):
   prompt = assemble_prompt(message)
   try:
       response = chat.send_message(prompt)
   except InvalidArgument as e:
       response = chat.send_message(
           f"O usuário te enviou um arquivo para você ler e obteve o erro: {e}. "
           "Pode explicar o que houve e dizer quais tipos de arquivos você "
           "dá suporte? Assuma que a pessoa não sabe programação e "
           "não quer ver o erro original. Explique de forma simples e concisa."
       )
   return response.text
# Crie e lance a interface do chat com suporte a arquivos
chat_interface = gr.ChatInterface(
   fn=gradio_wrapper,
   title="Assistente culinário",
   multimodal=True
)
# Inicie a interface
chat_interface.launch()