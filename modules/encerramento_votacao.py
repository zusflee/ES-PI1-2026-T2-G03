from database.conexao_SQL import criar_conexao
from cripto.criptogafia_descripto import descriptografia_dados
from logs.sistemas_de_logs import registrar_alerta_acesso


def encerramento_votacao(cursor, conexao):
    """
    Encerra a votacao apos validacao completa do mesario. Pede titulo, CPF
    e chave de acesso, verifica se o usuario possui perfil de mesario,
    pede confirmacao e uma segunda inserção da chave como dupla verificação.

    Args:
        cursor (mysql.connector.cursor): Cursor da conexao com o banco.
        conexao (mysql.connector.connection): Conexao ativa com o MySQL.

    Returns:
        bool: True se o encerramento foi confirmado, False caso contrario.
    """
    titulo = input("Digite seu titulo de eleitor: ")
    cmc_cpf = input("Digite os 4 primeiros digitos do CPF: ")
    chave_acesso = input("Digite sua chave de acesso: ")

    cursor.execute("SELECT * FROM eleitores WHERE titulo = %s", [titulo])
    eleitor = cursor.fetchone()

    if not eleitor:
        registrar_alerta_acesso("Titulo invalido no encerramento da urna.")
        print("Dados incorretos. A validacao falhou!")
        return False

    if not eleitor[5]:
        registrar_alerta_acesso("Tentativa de encerramento por nao-mesario.")
        print("Erro. Este eleitor nao possui perfil de mesario!")
        return False

    cpf_real = descriptografia_dados(eleitor[3])
    chave_real = descriptografia_dados(eleitor[4])

    while cpf_real[:4] != cmc_cpf:
        registrar_alerta_acesso("CPF incorreto no encerramento da urna.")
        print("CPF incorreto. Tente novamente.")
        cmc_cpf = input("Digite os 4 primeiros digitos do CPF: ")

    while chave_real != chave_acesso:
        registrar_alerta_acesso("Chave de acesso incorreta no encerramento da urna.")
        print("Chave de acesso incorreta. Tente novamente.")
        chave_acesso = input("Digite sua chave de acesso: ")

    confirmacao = ""
    respostas_validas = ["sim", "não", "nao"]
    while confirmacao.lower() not in respostas_validas:
        confirmacao = input("\nDeseja realmente encerrar a votacao? (Sim/Nao): ")
        if confirmacao.lower() not in respostas_validas:
            print("Resposta invalida! Digite apenas Sim ou Nao.")

    if confirmacao.lower() != "sim":
        print("Encerramento cancelado. Retornando ao menu anterior.")
        return False

    chave_confirmacao = input("Digite sua chave de acesso novamente para confirmar: ")
    if chave_confirmacao != chave_real:
        registrar_alerta_acesso("Segunda chave incorreta no encerramento da urna.")
        print("Chave de acesso incorreta. Encerramento cancelado!")
        return False

    print("\nVotacao encerrada com sucesso!")
    return True