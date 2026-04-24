from conexão_banco import criar_conexao
import mysql.connector

# Inserir candidatos no banco de dados

def inserir_candidatos(conexao, cursor, nome, numero, partido):
    '''Após o INSERT, chamamos conexao.commit() para salvar no banco.
        Se der erro, fazemos rollback() para cancelar a operação.'''
    
    try:
        sql = "INSERT INTO candidatos (nome, numero, partido) VALUES (%s, %s, %s)"
        valores = (nome, numero, partido)  

        cursor.execute(sql, valores)
        conexao.commit()  # Confirma a inserção no banco

        print(f"Candidato '{nome}' inserido com sucesso!")

    except mysql.connector.Error as erro:
        conexao.rollback()  # Desfaz a operação se der erro
        print(f"Erro ao inserir candidato: {erro}")

        
# Bloco de teste

if __name__ == "__main__":
    conexao = criar_conexao()
    cursor = conexao.cursor()

    inserir_candidatos(conexao, cursor, 'Leonardo', 22, 'PSDB')

    cursor.close()
    conexao.close()