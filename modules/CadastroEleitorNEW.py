from modules.ValidaçãoTituloNEW import validar_titulo
from modules.Validação_de_cpf import validação_de_cpf
from database.conexao_SQL import criar_conexao
import random
import mysql.connector


def gerar_chave(nome):
    partes = nome.strip().split()

    resultado= ""
    contador= 0

    for letra in partes[0]:
        if contador < 2:
            resultado += letra.upper()
            contador += 1

    resultado += partes[1][0].upper()

    for _ in range(4):
        resultado +=str(random.randint(0,9))

    return resultado

def cadastrar_eleitor(cursor, conexao): ## onde se inicia o cadastro do eleitor.
    print("\n--- CADASTRO DE ELEITOR ---")
    nome = input("Nome completo: ")
    
    titulo = input("Titulo de eleitor: ")  #Pede e verifica se o titulo é valido.
    if not validar_titulo(titulo):
        print("Título inválido!")
        return

    cpf = input("CPF (apenas números): ") #Pede e verifica se o cpf é valido.
    if not validação_de_cpf(cpf):
        print("CPF inválido!")
        return

    pergunta=input("Voce atuára como mesario? (S/N): ") #Verifica se vai ser mesariou ou não.
    pergunta= pergunta.lower()
    if pergunta == 's':
      mesario=True
    else:
      mesario=False

    # Verificação se já existe no banco.
    cursor.execute("SELECT * FROM eleitores WHERE cpf = %s OR titulo = %s", (cpf, titulo))
    if cursor.fetchone():
        print("Eleitor já cadastrado com este CPF ou título!")
        return

    chave = gerar_chave(nome)
    
    sql = "INSERT INTO eleitores (nome, titulo, cpf, is_mesario, chave_acesso) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (nome, titulo, cpf, mesario, chave))
    
    # Salva as alterações no banco.'
    conexao.commit()

    print("\n--- CADASTRO REALIZADO ---")
    print(f"  Nome  : {nome}")
    print(f"  Título: {titulo}")
    print(f"  CPF   : {cpf}")
    print(f"  Chave : {chave}")
    print("--------------------------\n")


conexao, cursor = criar_conexao()

