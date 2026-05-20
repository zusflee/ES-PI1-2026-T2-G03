from database.conexao_SQL import criar_conexao
from logs.sistemas_de_logs import registrar_abertura, registrar_alerta_acesso
from modules.utilidades import limpar_tela
def zerézima(cursor, conexao):
    

    print("\n--- INICIANDO ZERÉZIMA ---")

    cursor.execute("DELETE FROM votos") #Toda esta area esta responsavel por limpar e zerar os registros
    cursor.execute("UPDATE candidatos SET total_votos = 0")
    cursor.execute("UPDATE eleitores SET status_voto ='Não Votou'")
    conexao.commit()
    print("Registro de Votação limpos com sucesso!")

    cursor.execute("SELECT  * FROM candidatos")
    candidatos = cursor.fetchall()

    print("\n--- CANDIDATOS REGISTRADOS ---")
    
    for candidato in candidatos: #area responsavel por listar os candidatos
        print(f"Nome: {candidato[1]}")
        print(f"Numero:{candidato[2]}")
        print(f"Partido:{candidato[3]}")
        print(f"Votos: 0")

    print("\nZerézima concluida com sucesso! A urna esta vazia e pronta para a votação!")
    return True




def abertura_urna(cursor, conexao):
    print("\n--- ABERTURA DO SISTEMA DE VOTAÇÃO ---")
    registrar_abertura()
    # Loop do título
    eleitor = None
    while eleitor is None:
        titulo = input("Digite seu título eleitoral: ")
        cursor.execute("SELECT * FROM eleitores WHERE titulo = %s", (titulo,))
        eleitor = cursor.fetchone()
        if eleitor is None:
            registrar_alerta_acesso("Título de eleitor não encontrado.")
            print("Título não encontrado. Tente novamente.")

    # Loop dos 4 primeiros dígitos do CPF
    cmc_cpf = ""
    while eleitor[3][:4] != cmc_cpf:
        cmc_cpf = input("Digite os 4 primeiros dígitos do CPF: ")
        if eleitor[3][:4] != cmc_cpf:
            registrar_alerta_acesso("CPF incorreto na abertura da urna.")
            print("CPF incorreto. Tente novamente.")

    # Loop da chave de acesso
    chave_acesso = ""
    while eleitor[4] != chave_acesso:
        chave_acesso = input("Digite sua chave de acesso: ")
        if eleitor[4] != chave_acesso:
            registrar_alerta_acesso("Chave de acesso incorreta na abertura da urna.")
            print("Chave de acesso incorreta. Tente novamente.")

    # Verifica se é mesário
    if not eleitor[5]:
        registrar_alerta_acesso("Usuário sem perfil de mesário tentou abrir a urna.")
        print("Erro. Este eleitor não possui perfil de mesário!")
        return False

    print(f"Bem vindo, {eleitor[1]}! Identidade validada com sucesso!")
    zerézima(cursor, conexao)
    
    return True
    
