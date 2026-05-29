import mysql.connector

def deletar_candidato(conexao, cursor, numero_candidato):
    """
    Remove o registro de um candidato do banco de dados após confirmação manual do usuário.

    Args:
        conexao (mysql.connector.connection): O objeto de conexão ativa com o banco.
        cursor (mysql.connector.cursor): O cursor para execução de comandos SQL.
        numero_candidato (int): O número do candidato que será excluído do sistema.
    """
    try:
        confirmacao = input(f"Tem certeza que deseja deletar o candidato nº {numero_candidato}? (s/n): ")

        if confirmacao.lower() != "s":   
            print("Operação cancelada.")
            return  

        sql = "DELETE FROM candidatos WHERE numero = %s"
        valor = [numero_candidato]  

        cursor.execute(sql, valor)
        conexao.commit()

        if cursor.rowcount > 0:
            print("\n--- CANDIDATO REMOVIDO ---")
            print(f"  Numero: {numero_candidato}")
            print("--------------------------\n")
        else:
            print(f"Nenhum candidato encontrado com o número {numero_candidato}.")

    except mysql.connector.Error as erro:
            conexao.rollback()
            print(f"Erro ao deletar candidato: {erro}")