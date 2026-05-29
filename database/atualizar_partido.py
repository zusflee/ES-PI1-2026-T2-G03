import mysql.connector

def atualizar_partido(conexao, cursor, numero_candidato, novo_partido):
    """
    Modifica a sigla do partido de um candidato com base no seu número eleitoral.

    Args:
        conexao (mysql.connector.connection): O objeto de conexão ativa com o banco.
        cursor (mysql.connector.cursor): O cursor para execução de comandos SQL.
        numero_candidato (int): O número correspondente ao candidato que será atualizado.
        novo_partido (str): O novo nome ou sigla do partido político.
    """
    try:
        sql = "UPDATE candidatos SET partido = %s WHERE numero = %s"
        valores = [novo_partido, numero_candidato]

        cursor.execute(sql, valores)
        conexao.commit()

        if cursor.rowcount > 0:
            print("\n--- PARTIDO ATUALIZADO ---")
            print(f"  Numero    : {numero_candidato}")
            print(f"  Novo Partido: {novo_partido}")
            print("--------------------------\n")
        else:
            print(f"Nenhum candidato encontrado com o número {numero_candidato}.")

    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"Erro ao atualizar partido: {erro}")