import mysql.connector

def inserir_candidatos(conexao, cursor, nome, numero, partido):
    """
    Insere um novo candidato na tabela do banco de dados e confirma a transação.

    Args:
        conexao (mysql.connector.connection): O objeto de conexão ativa com o banco.
        cursor (mysql.connector.cursor): O cursor para execução de comandos SQL.
        nome (str): O nome completo do candidato.
        numero (int): O número eleitoral do candidato (chave de busca).
        partido (str): A sigla ou nome do partido do candidato.
    """
    try:
        sql = "INSERT INTO candidatos (nome, numero, partido) VALUES (%s, %s, %s)"
        valores = [nome, numero, partido]

        cursor.execute(sql, valores)
        conexao.commit()  

        print("\n--- CANDIDATO CADASTRADO ---")
        print(f"  Nome   : {nome}")
        print(f"  Numero : {numero}")
        print(f"  Partido: {partido}")
        print("----------------------------\n")

    except mysql.connector.Error as erro:
        conexao.rollback()  
        print(f"Erro ao inserir candidato: {erro}")