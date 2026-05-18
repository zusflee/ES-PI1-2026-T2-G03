from database.conexao_SQL import criar_conexao
def boletim_urna(cursor):
    print("\n--- BOLETIM DE URNA ---")

    ## lista candidatos em ordem alfabética com votos
    cursor.execute("SELECT * FROM candidatos ORDER BY nome ASC")
    candidatos = cursor.fetchall()

    if not candidatos:
        print("Nenhum candidato cadastrado!")
        return

    print("\nCandidatos:")
    for candidato in candidatos:
        print(f"Nome: {candidato[1]} | Número: {candidato[2]} | Partido: {candidato[3]} | Votos: {candidato[4]}")

    #Responsavel por mostrar o vencedor
    cursor.execute("SELECT * FROM candidatos ORDER BY total_votos DESC LIMIT 1")
    vencedor = cursor.fetchone()

    print(f"\n--- VENCEDOR ---")
    print(f"Nome: {vencedor[1]} | Número: {vencedor[2]} | Partido: {vencedor[3]} | Votos: {vencedor[4]}")


def votos_por_partido(cursor):
    print("\n--- VOTOS POR PARTIDO ---")

    # realiza a soma de votos por partido
    cursor.execute("SELECT partido, SUM(total_votos) FROM candidatos GROUP BY partido ORDER BY partido ASC")
    partidos = cursor.fetchall()

    if not partidos:
        print("Nenhum partido encontrado!")
        return

    for partido in partidos:
        print(f"Partido: {partido[0]} | Total de Votos: {partido[1]}")


def estatistica_comparecimento(cursor):
    print("\n--- ESTATÍSTICA DE COMPARECIMENTO ---")

    #  quantas pessoas votaram e percentual
    cursor.execute("SELECT COUNT(*) FROM eleitores")
    total_eleitores = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM eleitores WHERE status_voto = 'Já Votou'")
    total_votaram = cursor.fetchone()[0]

    if total_eleitores == 0:
        print("Nenhum eleitor cadastrado!")
        return

    percentual = (total_votaram / total_eleitores) * 100

    print(f"Total de eleitores aptos: {total_eleitores}")
    print(f"Total que votaram: {total_votaram}")
    print(f"Percentual de comparecimento: {percentual:.2f}%")


def validacao_integridade(cursor):
    print("\n--- VALIDAÇÃO DE INTEGRIDADE ---")

    # compara votos na urna com eleitores que já votaram
    cursor.execute("SELECT COUNT(*) FROM votos")
    total_votos_urna = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM eleitores WHERE status_voto = 'Já Votou'")
    total_ja_votou = cursor.fetchone()[0]

    print(f"Total de votos na urna: {total_votos_urna}")
    print(f"Total de eleitores com status 'Já Votou': {total_ja_votou}")

    if total_votos_urna == total_ja_votou:
        print("Eleição integra! Os números coincidem.")
    else:
        print("ATENÇÃO! Os números não coincidem. Possível inconsistência!")
             
    



