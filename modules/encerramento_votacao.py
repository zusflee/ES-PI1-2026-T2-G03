from database.conexao_SQL import criar_conexao

def encerramento_votacao(cursor, conexao):
    titulo = input("Digite seu titulo de eleitor: ")        # pede o titulo
    cmc_cpf = input("Digite os 4 primeiros digitos do CPF: ")  # pede os 4 primeiros digitos do cpf
    chave_acesso = input("Digite sua chave de acesso: ")    # pede a chave de acesso

    cursor.execute("SELECT * FROM eleitores WHERE titulo = %s", (titulo,))  # vai realizar a busca no banco pelo titulo
    eleitor = cursor.fetchone() 


    if not eleitor: #vai verificar se o eleitor existe
        print("Dados incorretos. A validação falhou!")
        return False


    if eleitor[3][:4] != cmc_cpf: #vai verificar se os 4 primeiros numeros do cpf estao corretos
        print("Dados incorretos. A validação falhou!")
        return False


    if eleitor[4] != chave_acesso: #vai verificar se a chave de acesso esta correta
        print("Dados incorretos. A validação falhou!")
        return False


    if not eleitor[5]: #vai verificar se tem cadastro de mesario
        print("Erro. Este eleitor não possui perfil de mesário!")
        return False


    confirmacao = ""  #pergunta de confirmação com validação
    respostas_validas = ["sim", "não", "nao"]

    while confirmacao.lower() not in respostas_validas:
        confirmacao = input("\nDeseja realmente encerrar a votação? (Sim/Não): ")
        if confirmacao.lower() not in respostas_validas:
            print("Resposta inválida! Digite apenas Sim ou Não.")


    
    if confirmacao.lower() != "sim":
        print("Encerramento cancelado. Retornando ao menu anterior.")
        return False

   
    chave_confirmacao = input("Digite sua chave de acesso novamente para confirmar: ")

    
    if chave_confirmacao != eleitor[4]:
        print("Chave de acesso incorreta. Encerramento cancelado!")
        return False

    print("\nVotação encerrada com sucesso!")
    return True