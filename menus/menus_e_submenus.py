''' --- MENUS E SUBMENUS --- '''

from modules.CadastroEleitorNEW import cadastrar_eleitor as cadastrar_eleitor_db
from database.conexao_SQL import criar_conexao
from modules.busca_edicao_remover import buscar_eleitor, editar_eleitor, remover_eleitor
from database.inserir_cand import inserir_candidatos
from database.busca_cand import buscar_candidato
from database.delete_cand import deletar_candidato
from database.atualizar_partido import atualizar_partido

# //// SUBMENU DE AUDITORIA ////
def menu_auditoria():
    opcao_auditoria = ""
    while opcao_auditoria != "3":
        print("\n--- [AUDITORIA] ---")
        print("1. Ver Logs")
        print("2. Ver Protocolos")
        print("3. Voltar")

        opcao_auditoria = input("\nEscolha uma opcao: ")

        match opcao_auditoria:
            case "1": print("Lendo arquivos de log...")
            case "2": print("Buscando protocolos de votacao no banco de dados...")
            case "3": print("Voltando ao menu Votacao...")
            case _: print("Opcao invalida, tente novamente.")

# //// SUBMENU DE RESULTADOS ////
def menu_resultados():
    opcao_resultado = ""
    while opcao_resultado != "5":
        print("\n--- [RESULTADOS] ---")
        print("1. Boletim da Urna")
        print("2. Votos por Partido")
        print("3. Estatisticas de Comparecimento")
        print("4. Validacao de Integridade")
        print("5. Voltar")

        opcao_resultado = input("\nEscolha uma opcao: ")

        match opcao_resultado:
            case "1": print("Gerando boletim da urna...")
            case "2": print("Buscando votos por partido no banco de dados...")
            case "3": print("Calculando estatisticas de comparecimento...")
            case "4": print("Validando integridade dos dados...")
            case "5": print("Voltando ao menu Votacao...")
            case _: print("Opcao invalida, tente novamente.")

# //// MENU DE CANDIDATOS ////
def menu_candidatos():
    opcao = ""
    while opcao != "5":
        print("\n--- [CANDIDATOS] ---")
        print("1. Inserir Candidato")
        print("2. Buscar Candidato")
        print("3. Deletar Candidato")
        print("4. Atualizar Partido")
        print("5. Voltar")

        opcao = input("\nEscolha uma opcao: ")

        match opcao:
            case "1":
                conexao, cursor = criar_conexao()
                nome   = input("Nome do candidato: ")
                numero = input("Numero: ")
                partido = input("Partido: ")
                inserir_candidatos(conexao, cursor, nome, numero, partido)
                cursor.close()    
                conexao.close()
            case "2":
                conexao, cursor = criar_conexao()
                nome = input("Nome do candidato: ")
                buscar_candidato(cursor, nome)
                cursor.close()    
                conexao.close()
            case "3":
                conexao, cursor = criar_conexao()
                numero = input("Numero do candidato: ")
                deletar_candidato(conexao, cursor, numero)
                cursor.close()    
                conexao.close()
            case "4":
                conexao, cursor = criar_conexao()
                numero     = input("Numero do candidato: ")
                novo_partido = input("Novo partido: ")
                atualizar_partido(conexao, cursor, numero, novo_partido)
                cursor.close()    
                conexao.close()
            case "5":
                print("Voltando...")
            case _:
                print("Opcao invalida, tente novamente.")

        

# //// FLUXO DE VOTO ////
def fluxo_voto():
    print("\n--- [VOTACAO] ---")

    titulo = ""
    while titulo == "":
        titulo = input("Informe o Titulo de Eleitor: ")
        if titulo == "":
            print("[ERRO] Titulo invalido. Tente novamente.")

    print("Validando eleitor no banco de dados...")
    print("Eleitor identificado com sucesso!")

    numero = input("Digite o numero do candidato: ")

    print("Candidato encontrado:")
    print("Numero : " + numero)
    print("Nome   : Candidato Ficticio")
    print("Partido: Partido Exemplo")

    confirma = ""
    while confirma not in ["S", "N"]:
        confirma = input("\nConfirmar voto? (S/N): ").upper()
        if confirma not in ["S", "N"]:
            print("Opcao invalida. Digite apenas S ou N.")

    if confirma == "S":
        print("Registrando voto no banco de dados...")
        print("Gerando protocolo de votacao...")
        print("Atualizando status do eleitor para Ja Votou...")
        print("[SUCESSO] Voto registrado com sucesso!")
    elif confirma == "N":
        print("Voto cancelado. Voltando ao Menu Urna...")

# //// FLUXO DE ENCERRAR VOTACAO ////
def encerrar_votacao():
    print("\n--- [ENCERRAR VOTACAO] ---")

    confirma = ""
    while confirma not in ["S", "N"]:
        confirma = input("Deseja realmente encerrar a votacao? (S/N): ").upper()
        if confirma not in ["S", "N"]:
            print("Opcao invalida. Digite apenas S ou N.")

    if confirma == "N":
        print("Operacao cancelada. Voltando ao Menu Urna...")
        return

    chave = ""
    while chave == "":
        chave = input("Confirme a chave de encerramento: ")
        if chave == "":
            print("[ERRO] Chave invalida. Tente novamente.")

    print("Encerrando sistema de votacao...")
    print("[SUCESSO] Votacao encerrada!")
    menu_resultados()

# //// MENU DA URNA ////
def menu_urna():
    opcao_urna = ""
    while opcao_urna != "2":
        print("\n--- [MENU URNA] ---")
        print("1. Votar")
        print("2. Encerrar Votacao")

        opcao_urna = input("\nEscolha uma opcao: ")

        match opcao_urna:
            case "1": fluxo_voto()
            case "2": encerrar_votacao()
            case _: print("Opcao invalida, tente novamente.")

# //// LOGIN DO MESARIO ////
def login_mesario():
    print("\n--- [LOGIN DO MESARIO] ---")

    usuario = ""
    senha = ""
    while usuario == "" or senha == "":
        usuario = input("Usuario: ")
        senha = input("Senha: ")
        if usuario == "" or senha == "":
            print("[ERRO] Usuario ou senha invalidos. Tente novamente.")

    print("[SUCESSO] Login realizado com sucesso!")
    print("Executando Zeresima (zerando contadores)...")
    print("Urna zerada e pronta para uso.")

    menu_urna()

# //// MENU DE VOTACAO ////
def menu_votacao():
    opcao_voto = ""
    while opcao_voto != "4":
        print("\n--- [VOTACAO] ---")
        print("1. Abrir Sistema de Votacao")
        print("2. Auditoria")
        print("3. Resultados")
        print("4. Voltar")

        opcao_voto = input("\nEscolha uma opcao: ")

        match opcao_voto:
            case "1": login_mesario()
            case "2": menu_auditoria()
            case "3": menu_resultados()
            case "4": print("Voltando ao menu principal...")
            case _: print("Opcao invalida, tente novamente.")

# //// CADASTRAR ELEITOR ////
def cadastrar_eleitor():
    conexao, cursor = criar_conexao()
    if conexao and cursor:
        cadastrar_eleitor_db(cursor, conexao)
        cursor.close()
        conexao.close()

# //// MENU DE GERENCIAMENTO ////
def menu_gerenciamento():
    opcao_gerenciamento = ""
    while opcao_gerenciamento != "7":
        print("\n--- [GERENCIAMENTO] ---")
        print("1. Cadastrar Eleitor")
        print("2. Editar Eleitor")
        print("3. Remover Eleitor")
        print("4. Buscar Eleitor")
        print("5. Listar Eleitores")
        print("6. Gerenciar Candidatos")
        print("7. Voltar")

        opcao_gerenciamento = input("\nEscolha uma opcao: ")

        match opcao_gerenciamento:
            case "1": cadastrar_eleitor()
            case "2": editar_eleitor()
            case "3": remover_eleitor()
            case "4":
                termo = input("Digite o nome ou titulo: ")
                buscar_eleitor(termo)
            case "5": print("Listando todos os eleitores...")
            case "6": menu_candidatos()
            case "7": print("Voltando ao menu principal...")
            case _:   print("Opcao invalida, tente novamente.")

# //// INICIO DO SISTEMA ////
def iniciar_sistema():
    conexao, cursor = criar_conexao()
    print("Conectado ao MySQL com êxito!") 
    cursor.close()
    conexao.close()
    escolha = ""
    while escolha != "3":
        print("\n=== SISTEMA DE VOTACAO DIGITAL ===")
        print("1. Gerenciamento")
        print("2. Votacao")
        print("3. Sair")

        escolha = input("\nEscolha uma opcao: ")

        match escolha:
            case "1": menu_gerenciamento()
            case "2": menu_votacao()
            case "3": print("Encerrando o sistema...")
            case _: print("Opcao invalida, tente novamente.")

if __name__ == "__main__":
    iniciar_sistema()