import mysql.connector

def deletar_candidato(conexao, cursor, numero_candidato):
    try:
        confirmacao = input(f"Tem certeza que deseja deletar o candidato nº {numero_candidato}? (s/n): ")

        if confirmacao.lower() != "s":   # lower --> Converte todos os caracteres alfabéticos maiúsculos em uma string para minúscula. 
            print("Operação cancelada.")
            return  # Sai da função sem fazer nada

        sql = "DELETE FROM candidatos WHERE numero = %s"
        valor = (numero_candidato,)  # Vírgula obrigatória — tupla com 1 elemento

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