def listar_candidatos(cursor):
    """
    Lista todos os candidatos cadastrados no banco de dados em ordem alfabética.
    Exibe os dados de cada candidato formatados no terminal com separadores
    visuais entre cada registro.

    Args:
        cursor: Cursor de conexão com o banco de dados para executar queries.

    Returns:
        None: A função apenas exibe os dados no terminal.
              Retorna None antecipadamente se nenhum candidato estiver cadastrado.
    """
    cursor.execute("SELECT * FROM candidatos ORDER BY nome ASC")
    candidatos = cursor.fetchall()

    if not candidatos:
        print("\nNenhum candidato cadastrado no sistema.")
        return

    print(f"\n{'='*50}")
    print(f"  LISTA DE CANDIDATOS ({len(candidatos)} cadastrado(s))")
    print(f"{'='*50}")

    for candidato in candidatos:
        print(f"\n  Candidato:")
        print(f"  {'ID':<15}: {candidato[0]}")
        print(f"  {'Nome':<15}: {candidato[1]}")
        print(f"  {'Número':<15}: {candidato[2]}")
        print(f"  {'Partido':<15}: {candidato[3]}")
        print(f"  {'Votos':<15}: {candidato[4]}")
        print("  " + "-" * 40)