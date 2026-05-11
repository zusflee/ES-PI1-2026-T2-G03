import mysql.connector

from conexao_SQL import criar_conexao

conexao = criar_conexao()
cursor = conexao.cursor()


#Teste de leitura do banco    

cursor.execute("SELECT DATABASE();")
resultado = cursor.fetchone()
print("Banco atual:",resultado)

