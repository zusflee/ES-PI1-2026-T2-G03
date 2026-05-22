from modules.ValidaçãoTituloNEW import validar_titulo
from modules.Validação_de_cpf import validação_de_cpf
from database.conexao_SQL import criar_conexao
import random
from logs.sistemas_de_logs import registrar_cadastro_eleitor, registrar_cadastro_mesario
import mysql.connector
from cripto.criptogafia_descripto import criptografia_dados, descriptografia_dados              



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

    pergunta = input("Voce atuára como mesario? (S/N): ")
    pergunta = pergunta.lower()
    if pergunta == 's':
        mesario = True
        registrar_cadastro_mesario(nome, titulo)
    else:
        mesario = False
        registrar_cadastro_eleitor(nome, titulo)

    # Verificação se já existe no banco (compara o CPF JÁ CIFRADO)
    cursor.execute(
        "SELECT * FROM eleitores WHERE cpf = %s OR titulo = %s",
        (cpf_cifrado, titulo)                    # <-- CRIPTO: usa o CPF cifrado, não o puro
    )
    if cursor.fetchone():
        print("Eleitor já cadastrado com este CPF ou título!")
        return

    chave = gerar_chave(nome)
    chave_cifrada = criptografia_dados(chave)  # cifra a chave de acesso antes de guardar no banco, para manter a segurança

    sql = "INSERT INTO eleitores (nome, titulo, cpf, is_mesario, chave_acesso) VALUES (%s, %s, %s, %s, %s)"
    # aqui o CPF e a chave de acesso são inseridos já cifrados, garantindo que dados sensíveis não fiquem expostos no banco
    cursor.execute(sql, (nome, titulo, cpf_cifrado, mesario, chave_cifrada))

    conexao.commit()

    print("\n--- CADASTRO REALIZADO ---")
    print(f"  Nome  : {nome}")
    print(f"  Título: {titulo}")
    print(f"  CPF   : {cpf}")      # cpf será exibido em texto puro para o eleitor, mas armazenado cifrado no banco
    print(f"  Chave : {chave}")    # chave será exibida em texto puro para o eleitor, mas armazenada cifrada no banco
    print("--------------------------\n")


conexao, cursor = criar_conexao()

