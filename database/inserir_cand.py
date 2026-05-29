from database.conexao_SQL import criar_conexao
import mysql.connector
from logs.sistemas_de_logs import registrar_log

# Inserir candidatos no banco de dados


def inserir_candidatos(conexao, cursor, nome, numero, partido):
    """
    Insere um novo candidato no banco de dados e registra o evento no log.
    Apos o INSERT, chamamos conexao.commit() para salvar no banco.
    Se der erro, fazemos rollback() para cancelar a operacao.

    Args:
        conexao: Objeto de conexao com o banco de dados.
        cursor: Cursor de conexao com o banco de dados para executar queries.
        nome (str): Nome do candidato.
        numero: Numero do candidato.
        partido (str): Partido do candidato.

    Returns:
        None: A funcao apenas exibe mensagens no terminal.
    """
    try:
        sql = "INSERT INTO candidatos (nome, numero, partido) VALUES (%s, %s, %s)"
        valores = [nome, numero, partido]

        cursor.execute(sql, valores)
        conexao.commit()  # Confirma a inserção no banco

        registrar_log(f"CADASTRO: Candidato cadastrado. Nome: {nome}. Numero: {numero}. Partido: {partido}")

        print("\n--- CANDIDATO CADASTRADO ---")
        print(f"  Nome   : {nome}")
        print(f"  Numero : {numero}")
        print(f"  Partido: {partido}")
        print("----------------------------\n")

    except mysql.connector.Error as erro:
        conexao.rollback()  # Desfaz a operação se der erro
        print(f"Erro ao inserir candidato: {erro}")