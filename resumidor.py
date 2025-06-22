import google.generativeai as genai
import os
from pypdf import PdfReader

genai.configure(api_key=os.environ['GEMINI_API'])

model = genai.GenerativeModel("gemini-1.5-flash")

user_input = input("digite o caminho relativo do arquivo que você quer resumir: ")
print("procurando o arquivo:", user_input)

if os.path.exists(user_input):
    try:
        reader = PdfReader(user_input)
        number_of_pages = len(reader.pages)
        filename_without_extension = os.path.splitext(os.path.basename(user_input))[0]
        output_filename = f"{filename_without_extension}-completo.txt"
        directory = os.path.dirname(user_input)
        output_filepath = os.path.join(directory, output_filename)
        with open(output_filepath, "w", encoding="utf-8") as f:
            for page in reader.pages:
                f.write(page.extract_text())

        found_file = genai.upload_file(
            path=output_filepath,
            display_name="arquivo para ser resumido"
        )

        print("Arquivo encontrado e lido,  enviando para tradução.")


        prompt = "Por favor, faça um resumo conciso do seguinte artigo científico:"
        response = model.generate_content([found_file, prompt])
        print("traduzido! Salvando o arquivo")
        
        print("\nConteúdo resumido):\n")
        print(response.text)
        print(f"Conteúdo completo transcrito salvo em: {output_filepath}")


    except Exception as e: # Capture a exceção geral para problemas com a API ou upload
        print(f"Ocorreu um erro ao processar o arquivo: {e}")
else:
    print("Arquivo não encontrado. Verifique o caminho e tente novamente.")