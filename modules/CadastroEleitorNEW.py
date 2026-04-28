from ValidaçãoTituloNEW import validar_titulo
from Validação_de_cpf import validação_de_cpf
from conexao_SQL import criar_conexao
import random
import mysql.connector


def gerar_chave():  ##Vai gerar a chave obrigatoria 
    return ''.join([str(random.randint(0, 9)) for _ in range(8)])


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

    chave = gerar_chave()
    
    sql = "INSERT INTO eleitores (nome, titulo, cpf, is_mesario, chave_acesso) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (nome, titulo, cpf, mesario, chave))
    
    # Salva as alterações no banco.'
    conexao.commit()

    print(f"Eleitor cadastrado com sucesso!")
    print(f"Sua chave de acesso é: {chave}")


conexao, cursor = criar_conexao()

if conexao and cursor:
    cadastrar_eleitor(cursor, conexao)
    
    # Fecha as portas após terminar
    cursor.close()
    conexao.close()
else:
    # Se 'conexao' ou 'cursor' forem None (erro na conexao_SQL.py)
    print("Erro ao conectar ao banco de dados. Verifique seu arquivo conexao_SQL.py")
