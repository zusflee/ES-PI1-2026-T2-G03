import mysql.connector

from conexao_SQL import criar_conexao

conexao, cursor = criar_conexao()


#Teste de leitura do banco    

cursor.execute("SELECT DATABASE();")
resultado = cursor.fetchone()
print("Banco atual:",resultado)

