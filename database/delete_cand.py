import mysql.connector

import mysql.connector

def deletar_candidato(conexao, cursor, numero_candidato):
    """
    Remove o registro de um candidato do banco de dados após confirmação manual do usuário.
    Busca e exibe os dados do candidato antes de solicitar a confirmação de exclusão.

    Args:
        conexao (mysql.connector.connection): O objeto de conexão ativa com o banco.
        cursor (mysql.connector.cursor): O cursor para execução de comandos SQL.
        numero_candidato (int): O número do candidato que será excluído do sistema.
    """
    try:
        # Busca o candidato antes de deletar para exibir os dados
        cursor.execute("SELECT * FROM candidatos WHERE numero = %s", (numero_candidato,))
        candidato = cursor.fetchone()

        if not candidato:   # Verifica se o candidato existe no banco
            print(f"Nenhum candidato encontrado com o número {numero_candidato}.")
            return

        # Exibe os dados encontrados
        print("\n--- CANDIDATO ENCONTRADO ---")
        print(f"  ID      : {candidato[0]}")
        print(f"  Nome    : {candidato[1]}")
        print(f"  Número  : {candidato[2]}")
        print(f"  Partido : {candidato[3]}")
        print(f"  Votos   : {candidato[4]}")
        print("----------------------------")

        confirmacao = input(f"\nTem certeza que deseja deletar este candidato? (s/n): ")

        if confirmacao.lower() != "s":   # lower --> Converte todos os caracteres alfabéticos maiúsculos em uma string para minúscula.
            print("Operação cancelada.")
            return  # Sai da função sem fazer nada

        sql = "DELETE FROM candidatos WHERE numero = %s"
        valor = (numero_candidato,)  # Vírgula obrigatória — tupla com 1 elemento

        cursor.execute(sql, valor)
        conexao.commit()

        print("\n--- CANDIDATO REMOVIDO ---")
        print(f"  Nome    : {candidato[1]}")
        print(f"  Número  : {candidato[2]}")
        print(f"  Partido : {candidato[3]}")
        print("--------------------------\n")

    except mysql.connector.Error as erro:
            conexao.rollback()
            print(f"Erro ao deletar candidato: {erro}")