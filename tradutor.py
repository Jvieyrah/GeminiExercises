import google.generativeai as genai
import os

genai.configure(api_key=os.environ['GEMINI_API'])

model = genai.GenerativeModel("gemini-1.5-flash")

user_input = input("digite o caminho relativo do arquivo que você quer traduzir: ")
print("procurando o arquivo:", user_input)

if os.path.exists(user_input):
    try:
        found_file = genai.upload_file(
            path=user_input,
            display_name="file to be translated to english"
        )

        print("Arquivo encontrado e enviado para tradução.")


        prompt = "traduza o texto do arquivo para inglês"
        response = model.generate_content([found_file, prompt])
        print("traduzido! Salvando o arquivo")
        directory = os.path.dirname(user_input)
        filename_without_extension = os.path.splitext(os.path.basename(user_input))[0]
        output_filename = f"{filename_without_extension}-translated.txt"
        output_filepath = os.path.join(directory, output_filename)
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Conteúdo traduzido salvo em: {output_filepath}")
        print("\nConteúdo da resposta (apenas para visualização rápida):\n")
        print(response.text) # Continua exibindo no terminal para feedback imediato


    except Exception as e: # Capture a exceção geral para problemas com a API ou upload
        print(f"Ocorreu um erro ao processar o arquivo: {e}")
else:
    print("Arquivo não encontrado. Verifique o caminho e tente novamente.")