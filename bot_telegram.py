import json
import re
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Substitua pelo seu token
TOKEN = '7847334522:AAEOVibI03bEkfKG3vrDTfPqBaNYfLKl0F0'

# Caminho do arquivo JSON onde os problemas serão armazenados
ARQUIVO_PROBLEMAS = 'problemas.json'

# Carregar os problemas salvos de um arquivo JSON
def carregar_problemas():
    try:
        with open(ARQUIVO_PROBLEMAS, 'r') as arquivo:
            # Tenta carregar o conteúdo do arquivo JSON
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existir ou estiver malformado, retorna um dicionário vazio
        return {}

# Salvar os problemas no arquivo JSON
def salvar_problemas(problemas):
    with open(ARQUIVO_PROBLEMAS, 'w') as arquivo:
        # Salva os dados em formato JSON no arquivo
        json.dump(problemas, arquivo, indent=4)

# Dicionário para armazenar problemas não resolvidos
problemas_nao_resolvidos = carregar_problemas()

# Função para processar a mensagem de problema
def processar_mensagem_problema(texto):
    padrao = r"Nome:\s*(?P<nome>.*?)\s*Descrição:\s*(?P<descricao>.*?)\s*Original problem ID:\s*(?P<id_problema>\d+)"
    match = re.search(padrao, texto, re.DOTALL)

    if match:
        nome = match.group("nome").strip()
        descricao = match.group("descricao").strip()
        id_problema = match.group("id_problema").strip()

        local_padroes = r"Local:\s*(?P<local>.*?)\s*-"
        local_match = re.search(local_padroes, descricao)

        data_hora_padroes = r"(\d{2}:\d{2}:\d{2} \d{4}/\d{2}/\d{2})"
        data_hora_match = re.search(data_hora_padroes, descricao)

        local = local_match.group("local").strip() if local_match else "Desconhecido"
        data_hora = data_hora_match.group(0) if data_hora_match else "Desconhecido"

        # Armazenar o problema no dicionário
        problemas_nao_resolvidos[id_problema] = {
            "nome": nome,
            "descricao": descricao,
            "local": local,
            "data_hora": data_hora
        }

        # Salvar os problemas no arquivo
        salvar_problemas(problemas_nao_resolvidos)

        return True
    return False

# Função para processar a mensagem de resolução
def processar_mensagem_resolucao(texto):
    padrao_resolucao = r"Problem has been resolved at (\d{2}:\d{2}:\d{2}) on (\d{4}.\d{2}.\d{2})\s*Problem name:\s*(?P<nome>.*?)\s*Original problem ID:\s*(?P<id_problema>\d+)"
    match = re.search(padrao_resolucao, texto, re.DOTALL)

    if match:
        id_problema = match.group("id_problema").strip()

        # Remover o problema resolvido do dicionário
        if id_problema in problemas_nao_resolvidos:
            del problemas_nao_resolvidos[id_problema]
            # Salvar os problemas após a remoção
            salvar_problemas(problemas_nao_resolvidos)
            return True
    return False

# Função que será chamada quando uma nova mensagem for recebida
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text

    # Verificar se é um problema elétrico não resolvido
    if "⚡️PROBLEMA ELÉTRICO⚡️" in texto:
        if processar_mensagem_problema(texto):
            print(f"Problema novo registrado: {texto}")

    # Verificar se é uma mensagem de resolução de problema
    elif "✅RESOLVIDO✅" in texto:
        if processar_mensagem_resolucao(texto):
            print(f"Problema resolvido: {texto}")

    # Exibir o estado atual dos problemas não resolvidos
    exibir_problemas_nao_resolvidos()

# Função para exibir problemas não resolvidos
def exibir_problemas_nao_resolvidos():
    print("\n--- Problemas Elétricos Não Resolvidos ---")
    for id_problema, info in problemas_nao_resolvidos.items():
        print(f"ID: {id_problema}")
        print(f"Nome: {info['nome']}")
        print(f"Local: {info['local']}")
        print(f"Descrição: {info['descricao']}")
        print(f"Data/Hora: {info['data_hora']}\n")

# Função principal para iniciar o bot
def main():
    # Usando Application.builder() para criar a instância do bot
    application = Application.builder().token(TOKEN).build()

    # Cria um handler para capturar todas as mensagens de texto
    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    application.add_handler(message_handler)

    # Inicia o bot
    application.run_polling()

if __name__ == '__main__':
    main()