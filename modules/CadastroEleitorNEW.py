from modules.ValidaçãoTituloNEW import validar_titulo
from modules.Validação_de_cpf import validação_de_cpf
from database.conexao_SQL import criar_conexao
import random
from logs.sistemas_de_logs import (
    registrar_cadastro_eleitor,
    registrar_cadastro_mesario,
    registrar_tentativa_cadastro_duplicado
)
import mysql.connector
from cripto.criptogafia_descripto import criptografia_dados, descriptografia_dados              



def gerar_chave(nome):
    """
    Gera uma chave de acesso única para o eleitor baseada no seu nome.
    A chave é composta pelas 2 primeiras letras do primeiro nome,
    a primeira letra do segundo nome e 4 dígitos aleatórios.
    Exemplo: "André Silva" gera "ANS" + "4821" = "ANS4821".

    Args:
        nome (str): Nome completo do eleitor com pelo menos dois nomes.

    Returns:
        str: Chave de acesso gerada com 7 caracteres no formato
             (2 letras + 1 letra + 4 dígitos). Exemplo: "ANS4821".
    """

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
    """
    Realiza o cadastro de um novo eleitor no banco de dados.
    Valida nome, título e CPF antes de salvar. Criptografa o CPF
    e a chave de acesso antes de armazenar no banco. Verifica
    duplicidade de CPF e título, gera a chave de acesso e registra
    o cadastro no log diferenciando entre eleitor comum e mesário.

    Args:
        cursor: Cursor de conexão com o banco de dados para executar queries.
        conexao: Objeto de conexão com o banco de dados para confirmar alterações.

    Returns:
        None: A função apenas exibe os dados cadastrados no terminal.
              Retorna None antecipadamente se já existir um eleitor
              cadastrado com o mesmo CPF ou título.
    """
    print("\n--- CADASTRO DE ELEITOR ---")
    nome = input("Nome completo: ").strip()
    while len(nome.split()) < 2 or not nome.replace(" ", "").isalpha():
        print("Erro: Digite nome e sobrenome (apenas letras).")
        nome = input("Nome completo: ").strip()
    
    titulo = input("Titulo de eleitor: ")  #Pede e verifica se o titulo é valido.
    while not validar_titulo(titulo):
        print("Título inválido!")
        titulo = input("Titulo de eleitor: ")

    cpf = input("CPF (apenas números): ")
    while not validação_de_cpf(cpf):
        print("CPF inválido!")
        cpf = input("CPF (apenas números): ")

    # CRIPTO: cifra o CPF validado antes de usar no banco, para manter a segurança dos dados sensíveis
    cpf_cifrado = criptografia_dados(cpf)   

    pergunta = input("Voce atuará como mesario? (S/N): ")   # corrigi "atuára" tbm
    pergunta = pergunta.lower()
    if pergunta == 's':
        mesario = True
    else:
        mesario = False

    # Verificação se já existe no banco
    cursor.execute(
        "SELECT * FROM eleitores WHERE cpf = %s OR titulo = %s",
        [cpf_cifrado, titulo]
    )
    if cursor.fetchone():
        registrar_tentativa_cadastro_duplicado(titulo)
        print("Eleitor já cadastrado com este CPF ou título!")
        return

    chave = gerar_chave(nome)
    chave_cifrada = criptografia_dados(chave)

    sql = "INSERT INTO eleitores (nome, titulo, cpf, is_mesario, chave_acesso) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, [nome, titulo, cpf_cifrado, mesario, chave_cifrada])

    conexao.commit()

    # LOG AGORA — só registra DEPOIS que o cadastro deu certo de verdade
    if mesario:
        registrar_cadastro_mesario(nome, titulo)
    else:
        registrar_cadastro_eleitor(nome, titulo)

    print("\n--- CADASTRO REALIZADO ---")
    print(f"  Nome  : {nome}")
    print(f"  Título: {titulo}")
    print(f"  CPF   : {cpf}")
    print(f"  Chave : {chave}")
    print("--------------------------\n")



