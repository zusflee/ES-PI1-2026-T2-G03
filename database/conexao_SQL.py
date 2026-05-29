import mysql.connector

def criar_conexao():
    """
    Estabelece a conexão com o banco de dados MySQL local 'sistema_eleitoral'.

    Returns:
        tuple: Uma tupla contendo (conexao, cursor). 
               Retorna (None, None) caso ocorra uma falha na conexão.
    """
    try:
        conexao = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='Cabo2015@',
            database='sistema_eleitoral'
        )
        cursor = conexao.cursor()
        return conexao, cursor
    except mysql.connector.Error as erro:
        print(f"Erro ao conectar: {erro}")
        return None, None

if __name__ == "__main__":
    conexao, cursor = criar_conexao()
