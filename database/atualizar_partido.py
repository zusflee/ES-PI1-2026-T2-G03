def atualizar_partido(conexao, cursor, numero_candidato, novo_partido):
    try:
        sql = "UPDATE candidatos SET partido = %s WHERE numero = %s"
        valores = (novo_partido, numero_candidato)

        cursor.execute(sql, valores)
        conexao.commit()

        if cursor.rowcount > 0:
            # rowcount = quantas linhas foram afetadas pelo UPDATE
            print(f"Partido do candidato nº {numero_candidato} atualizado para '{novo_partido}'.")
        else:
            print(f"Nenhum candidato encontrado com o número {numero_candidato}.")

    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"Erro ao atualizar partido: {erro}")