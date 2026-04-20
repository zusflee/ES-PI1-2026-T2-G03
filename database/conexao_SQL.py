# Conexão com o banco
import mysql.connector
''' import traz uma biblioteca externa para dentro do nosso código.
    "mysql.connector" é o pacote que permite ligar o Python com MySQL.
    Para instalar: pip install mysql-connector-python'''

def criar_conexao():
    try:
        conexao = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='fleezus',
        database='sistema_eleitoral'
    )
        if conexao.is_connected():
        print("Conectado ao MySQL com êxito!")

        cursor = conexao.cursor()
        return conexao  
    except mysql.connector.Error as erro:
        print(f"Erro ao conectar{erro}:")

'''"try" significa: "tenta fazer isso; se der errado, vai pro except"
    Usamos try/except aqui porque conexão com banco pode falhar'''
 
#Teste de leitura do banco
cursor.execute("SELECT DATABASE();")
resultado = cursor.fetchone()
print("Banco atual:",resultado)

#Criar def buscar_candidato_por_nome
#Criar def inserir_candidato
#Criar def buscar_candidato_por_nome
#Criar def atualizar_partido
#Criar def deletar_candidato