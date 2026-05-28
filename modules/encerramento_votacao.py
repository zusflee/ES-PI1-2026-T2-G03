from database.conexao_SQL import criar_conexao
from cripto.criptogafia_descripto import descriptografia_dados

def encerramento_votacao(cursor, conexao):
    titulo = input("Digite seu titulo de eleitor: ")        # pede o titulo
    cmc_cpf = input("Digite os 4 primeiros digitos do CPF: ")  # pede os 4 primeiros digitos do cpf
    chave_acesso = input("Digite sua chave de acesso: ")    # pede a chave de acesso

    cursor.execute("SELECT * FROM eleitores WHERE titulo = %s", (titulo,))  # vai realizar a busca no banco pelo titulo
    eleitor = cursor.fetchone() 


    if not eleitor: #vai verificar se o eleitor existe
        print("Dados incorretos. A validação falhou!")
        return False


    cpf_real = descriptografia_dados(eleitor[3])
    while cpf_real[:4] != cmc_cpf:
        print("CPF incorreto. Tente novamente.")
        cmc_cpf = input("Digite os 4 primeiros dígitos do CPF: ")

        
    chave_real = descriptografia_dados(eleitor[4])
    while chave_real != chave_acesso:
        print("Chave de acesso incorreta. Tente novamente.")
        chave_acesso = input("Digite sua chave de acesso: ")

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

    
    if chave_confirmacao != chave_real:
        print("Chave de acesso incorreta. Encerramento cancelado!")
        return False
    print("\nVotação encerrada com sucesso!")
    return True