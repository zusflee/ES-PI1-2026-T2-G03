from datetime import datetime
import mysql.connector
 
#  Conexão com banco de dados
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sua_senha_aqui",  # ← altere
    database="ladpy_db"
)
cursor = conn.cursor(dictionary=True)
 
# Limpa os registros anteriores
cursor.execute("DELETE FROM votos")
cursor.execute("ALTER TABLE votos AUTO_INCREMENT = 1")
cursor.execute("UPDATE eleitores SET status_voto = 'Pendente'")
cursor.execute("UPDATE candidatos SET votos = 0")
conn.commit()
