# bot_code_telegram
Python para monitorar bot

Este código implementa um bot do Telegram que gerencia problemas elétricos reportados pelos usuários. Ele usa a biblioteca python-telegram-bot para interagir com o Telegram e o arquivo JSON para armazenar os problemas e suas resoluções.

Resumo simples:
Armazenamento de problemas: O bot salva informações sobre problemas elétricos em um arquivo JSON (problemas.json). Ele carrega e salva dados sempre que um problema é registrado ou resolvido.

Processamento de mensagens:

Problemas não resolvidos: Quando um usuário envia uma mensagem com a tag "⚡️PROBLEMA ELÉTRICO⚡️", o bot extrai informações do texto (como nome, descrição e ID do problema) e as armazena em um dicionário.
Problemas resolvidos: Quando uma mensagem contém "✅RESOLVIDO✅", o bot remove o problema correspondente do arquivo JSON.
Exibição de problemas: Após processar uma mensagem, o bot imprime no console uma lista dos problemas elétricos não resolvidos.

Bot do Telegram:

O bot utiliza o token fornecido para se conectar à API do Telegram e fica aguardando mensagens.
Sempre que uma nova mensagem de texto é recebida, a função handle_message é chamada, que processa o conteúdo da mensagem e executa as ações apropriadas (registrar um novo problema ou resolver um problema existente).
Funções principais:
carregar_problemas(): Carrega os problemas armazenados no arquivo JSON.
salvar_problemas(problemas): Salva os problemas no arquivo JSON.
processar_mensagem_problema(texto): Processa a mensagem de um problema elétrico e armazena os dados.
processar_mensagem_resolucao(texto): Processa a mensagem de resolução de um problema.
handle_message(update, context): Função que lida com as mensagens recebidas no Telegram.
exibir_problemas_nao_resolvidos(): Exibe no console a lista dos problemas não resolvidos.
Como funciona:
O bot lê mensagens dos usuários no Telegram.
Quando recebe uma mensagem sobre um problema elétrico, ele armazena as informações em um arquivo JSON.
Quando recebe uma mensagem de resolução, ele remove o problema correspondente.
O bot imprime todos os problemas não resolvidos no console.
Iniciação:
A função main() configura e executa o bot, começando a escutar as mensagens enviadas para ele.
