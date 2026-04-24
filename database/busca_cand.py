from conexão_banco import criar_conexao

# Buscar candidato pelo nome

def buscar_candidato(cursor, nome):
    '''O % antes do nome adiciona busca parcial (ex: "Jo" encontra "João").'''
    '''O %s protege contra SQL injection (interfiram nas consultas)'''
    sql = "SELECT * FROM candidatos WHERE nome LIKE %s"  # LIKE encontra: "João", "João Silva","João Carlos"
    valor = (f"{nome}",)
    cursor.execute(sql, valor)
    resultados = cursor.fetchall()  # Pega todas as linhas encontradas

    if resultados:
        for candidato in resultados:
            print(candidato)
    else:
        print("Nenhume candidato encontrado com esse nome.")
    return resultados


# Bloco de teste

if __name__ == "__main__":
    conexao = criar_conexao()
    cursor = conexao.cursor()

    buscar_candidato(cursor, "Gabriel")

    cursor.close()
    conexao.close()