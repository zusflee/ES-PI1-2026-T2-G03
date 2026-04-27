# Conexão com o banco
import mysql.connector
''' import traz uma biblioteca externa para dentro do nosso código.
    "mysql.connector" é o pacote que permite ligar o Python com MySQL.
    Para instalar: pip install mysql-connector-python'''

def criar_conexao():
    try:
        conexao = mysql.connector.connect(
        host='BD-ACD',
        user='BD25022616',
        password='Rzsty4',
        database='BD25022616'
    )
        if conexao.is_connected():
            print("Conectado ao MySQL com êxito!")

        cursor = conexao.cursor()
        return conexao, cursor
    except mysql.connector.Error as erro:
        print(f"Erro ao conectar{erro}:")
        return None, None

'''"try" significa: "tenta fazer isso; se der errado, vai pro except"
    Usamos try/except aqui porque conexão com banco pode falhar'''
 
#Teste de leitura do banco
def teste_conexao():
    conexao, cursor = criar_conexao()
    if cursor:
        cursor.execute("SELECT DATABASE();")
        resultado = cursor.fetchone()
        print("Banco atual:",resultado)
        cursor.close()
        conexao.close()

# Chama a função de teste ao rodar o arquivo
if __name__ == "__main__":
    teste_conexao()