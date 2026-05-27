from database.conexao_SQL import criar_conexao
from logs.sistemas_de_logs import registrar_abertura, registrar_alerta_acesso
from modules.utilidades import limpar_tela
from cripto.criptogafia_descripto import descriptografia_dados
def zerézima(cursor, conexao):
    

    print("\n--- INICIANDO ZERÉZIMA ---")

    cursor.execute("DELETE FROM votos") #Toda esta area esta responsavel por limpar e zerar os registros
    cursor.execute("UPDATE candidatos SET total_votos = 0")
    cursor.execute("UPDATE eleitores SET status_voto ='Não Votou'")
    cursor.execute("UPDATE eleitores SET status_voto = 'Pendente'")
    conexao.commit()
    print("Registro de Votação limpos com sucesso!")

    cursor.execute("SELECT  * FROM candidatos")
    candidatos = cursor.fetchall()
    
    total = len(candidatos)
    print(f"\n{'=' * 50}")
    print(f"  CANDIDATOS REGISTRADOS ({total} candidato(s))")
    print(f"{'=' * 50}")

    for candidato in candidatos:
        print(f"\n  Candidato:")
        print(f"  {'ID':<15}: {candidato[0]}")
        print(f"  {'Nome':<15}: {candidato[1]}")
        print(f"  {'Numero':<15}: {candidato[2]}")
        print(f"  {'Partido':<15}: {candidato[3]}")
        print(f"  {'Votos':<15}: {candidato[4]}")
        print("  " + "-" * 40)
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
    cpf_real = descriptografia_dados(eleitor[3])
    cmc_cpf = ""
    while cpf_real[:4] != cmc_cpf:
        cmc_cpf = input("Digite os 4 primeiros dígitos do CPF: ")
        if cpf_real[:4] != cmc_cpf:
                print("CPF incorreto. Tente novamente.")

    # Loop da chave de acesso]
    chave_real = descriptografia_dados(eleitor[4])
    chave_acesso = ""
    while chave_real != chave_acesso:
        chave_acesso = input("Digite sua chave de acesso: ")
        if chave_real != chave_acesso:
                print("Chave de acesso incorreta. Tente novamente.")

    # Verifica se é mesário
    if not eleitor[5]:
        registrar_alerta_acesso("Usuário sem perfil de mesário tentou abrir a urna.")
        print("Erro. Este eleitor não possui perfil de mesário!")
        return False

    print(f"Bem vindo, {eleitor[1]}! Identidade validada com sucesso!")
    zerézima(cursor, conexao)
    
    return True
    
