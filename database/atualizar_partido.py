import mysql.connector

def atualizar_partido(conexao, cursor, numero_candidato, novo_partido):
    try:
        sql = "UPDATE candidatos SET partido = %s WHERE numero = %s"
        valores = (novo_partido, numero_candidato)

        cursor.execute(sql, valores)
        conexao.commit()

        if cursor.rowcount > 0:
            # rowcount = quantas linhas foram afetadas pelo UPDATE
            print("\n--- PARTIDO ATUALIZADO ---")
            print(f"  Numero    : {numero_candidato}")
            print(f"  Novo Partido: {novo_partido}")
            print("--------------------------\n")
        else:
            print(f"Nenhum candidato encontrado com o número {numero_candidato}.")

    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"Erro ao atualizar partido: {erro}")