import datetime
import mysql.connector

def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="senha", #mudar a senha
        database="sistema_eleitoral"
    )

def registrar_log_db(evento):
    if not evento:
        return
    else:
        conn = conectar_db()
        cursor = conn.cursor()
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') #serve para registrar a data
        query = "INSERT INTO logs (timestamp, evento) VALUES (%s, %s)" 
        cursor.execute(query, (timestamp, evento))
        conn.commit() #confirma e salva os dados
        for recurso in [cursor, conn]:
            recurso.close()  #nao deixa a conexao aberta

def registrar_abertura(): #comeco da votacao
    registrar_log_db("ABERTURA: Votação iniciada com sucesso. Total de votos zerado.")

def registrar_acesso_negado(): #dados errados
    registrar_log_db("ALERTA: Tentativa de acesso negado por dados inválidos no login do mesário.")

#voto_info depende do modulo principal
def registrar_voto_realizado(voto_info):
    registrar_log_db(f"SUCESSO: Voto realizado com sucesso. Detalhes: {voto_info}")

def registrar_encerramento(): 
    registrar_log_db("ENCERRAMENTO: Votação finalizada com sucesso.")
