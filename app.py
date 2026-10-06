from fastapi import FastAPI, Form
from data_base_sqlite import salvar_despesa
from parser_mensagem import processar_mensagem
from datetime import datetime

# Inicializa o servidor FastAPI
app = FastAPI()

#Cria a rota do tipo POST

@app.post("/webhook")
def receber_mensagem_whatsapp(Body: str = Form(...)):
    """
    :param Body: texto digitado no whatsapp
    :return: Mensagem no formato XML
    """
    texto_recebido = Body.strip()

    try:
        #Faz o unpacking do texto recebido
        valor, descricao = processar_mensagem(texto_recebido)

        #Armazena a data atual do lançamento
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #Salva a despesa usando o metodo
        salvar_despesa(data_atual,descricao,valor, "Geral")

        #Mensagem de sucesso
        resposta = f" 📝*Registrado com sucesso!*\n 💰Valor: {valor}"

    except ValueError as erro:
        #Se o rise lançar ValueError
        resposta = f" ❌ *Erro de formato:*  {str(erro)}"

    #Retorna a resposta no formato XML exigito pelo Twilio
    return {
        "Response": f"<Message><Body>{resposta}</Body></Message>"
    }


