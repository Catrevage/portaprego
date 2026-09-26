def processar_mensagem (texto: str):
    """Recebe um texo, no formato "25.90 Almoço", separa o valor inteiro,
    e retorna o valor interiro e uma string com a descrição
    :param texto: '25.90 Almoço'
    :return: valor inteiro, descrição
    """
    #Recebe o texto sem espaços no fim e no início
    texto_limpo = texto.strip()

    #Corta o texto no primeiro spaço que encontrar;
    #o número 1 informa que será cortado aplenas 1 vez
    partes = texto_limpo.split(" ",1)

    #Armazena o valor
    valor_texto = partes[0]


    #transforma o . em vírgula
    valor_texto = valor_texto.replace(",",".")

    try:
        #Transforma a string em float
        valor_num = float(valor_texto)
    except ValueError:
        #Lança o erro caso seja informado o formato errado
        raise ValueError("O texto deve começar com um valor numérico válido tipo 25,90")

    # Armazena a descrição
    if len(partes)> 1:
        descricao = partes[1]
    else:
        descricao = "Gasto não especificado"

    return valor_num, descricao





