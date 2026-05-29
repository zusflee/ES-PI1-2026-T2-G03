def buscar_candidato(cursor, nome):
    """
    Busca candidatos no banco de dados através de uma correspondência parcial de nome.

    Args:
        cursor (mysql.connector.cursor): O cursor para execução de comandos SQL.
        nome (str): O termo ou trecho do nome para realizar a busca (utiliza LIKE).

    Returns:
        list: Uma lista de tuplas contendo todos os registros encontrados.
              Retorna uma lista vazia se nenhum candidato corresponder ao critério.
    """
    sql = "SELECT * FROM candidatos WHERE nome LIKE %s"  
    valor = [f"%{nome}%"]
    
    cursor.execute(sql, valor)
    resultados = cursor.fetchall()  

    if resultados:
        for candidato in resultados:
            print("\n--- CANDIDATO ENCONTRADO ---")
            print(f"  ID     : {candidato[0]}")
            print(f"  Nome   : {candidato[1]}")
            print(f"  Numero : {candidato[2]}")
            print(f"  Partido: {candidato[3]}")
            print("----------------------------")
    else:
        print("Nenhum candidato encontrado com esse nome.")
        
    return resultados