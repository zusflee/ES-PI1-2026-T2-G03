from database.conexao_SQL import criar_conexao

# Buscar candidato pelo nome

def buscar_candidato(cursor, nome):
    '''O % antes do nome adiciona busca parcial (ex: "Jo" encontra "João").'''
    '''O %s protege contra SQL injection (interfiram nas consultas)'''
    sql = "SELECT * FROM candidatos WHERE nome LIKE %s"  # LIKE encontra: "João", "João Silva","João Carlos"
    valor = [f"%{nome}%"]
    cursor.execute(sql, valor)
    resultados = cursor.fetchall()  # Pega todas as linhas encontradas

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

