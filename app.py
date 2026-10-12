from fastapi import FastAPI, Request, Response, status
from data_base import salvar_despesa, conectar_banco, inicializar_banco
from parser_mensagem import processar_mensagem
from datetime import datetime

# Inicializa o servidor FastAPI
app = FastAPI()

#Inicializado o banco e cria a tabela se ela não existir

inicializar_banco()

#Cria a rota do tipo POST

@app.post("/webhook")
async def receber_mensagem_whatsapp(request: Request):
    """
    :param Body: texto digitado no whatsapp
    :return: Mensagem no formato XML
    """
    try:
        #transforma a requisição em um dict
        dados = await request.json()

        #Navea pelas chaves d JSON e captura o texto digitado
        mensagem_objeto = dados.get("data", {}).get("message", {})
        texto_recebido = mensagem_objeto.get("conversation","").strip()


        #se a mensagem iver vazia ou diferente de texto
        if not texto_recebido:
            return Response(status_code=status.HTTP_200_OK)

        #Faz o unpacking do texto recebido
        valor, descricao = processar_mensagem(texto_recebido)

        #Armazena a data atual do lançamento
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #Salva a despesa usando o metodo
        salvar_despesa(data_atual,descricao,valor, "Geral")

        #Mensagem de sucesso
        resposta = f" 📝*Registrado com sucesso!*\n 💰Valor: {valor}"

        return {
            "status": "sucesso",
            "reply": resposta
        }

    except ValueError as erro:

        #Retorna a resposta no formato XML exigito pelo Twilio
        return {
            "status": "erro",
            "reply": f"❌ *Erro de formato:* {str(erro)}"
        }

    except Exception as erro_generico:
        #Proteção para outros tipos de erro
        print(f"Erro inesperado no servidor: {erro_generico}")
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
