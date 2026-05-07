from conexao_SQL import criar_conexao   

import mysql.connector

from datetime import datetime
 

ARQUIVO_LOG = "log_ocorrencias.txt"
 
 
def registrar_log(mensagem):
 
    
    agora = datetime.now()
 
   
    linha = f"[{agora}] {mensagem}\n"
 
  
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha)
 
 

def registrar_abertura():
    registrar_log("ABERTURA: Votação iniciada com sucesso. Total de votos zerado.")
 
 

def registrar_alerta_acesso():
    registrar_log("ALERTA: Tentativa de acesso negado")
 
 

def registrar_alerta_voto_duplo():
    registrar_log("ALERTA: Tentativa de voto duplo")
 
 

def registrar_voto_sucesso():
    registrar_log("SUCESSO: Voto realizado com sucesso")
 
 

def registrar_encerramento():
    registrar_log("ENCERRAMENTO: Votação finalizada com sucesso.")
 
 

def exibir_logs():
    print("=" * 55)
    print("         REGISTRO DE OCORRÊNCIAS")
    print("=" * 55)
 
    try:
        
        with open(ARQUIVO_LOG, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
 
        
        if not linhas:
            print("Nenhum registro encontrado.")
        else:
            for linha in linhas:
                print(linha, end="")  
 
    except FileNotFoundError:
        
        print("Arquivo de log não encontrado. Nenhum evento foi registrado ainda.")
 
    print("=" * 55)
 
 

if __name__ == "__main__":
 
    
    registrar_abertura()
    registrar_alerta_acesso()
    registrar_voto_sucesso()
    registrar_alerta_voto_duplo()
    registrar_voto_sucesso()
    registrar_encerramento()
 
    
    exibir_logs()
