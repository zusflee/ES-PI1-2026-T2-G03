''' --- MENUS E SUBMENUS --- '''

# Gera protocolo com título do eleitor + número do candidato + hora atual
from datetime import datetime
from modules.CadastroEleitorNEW import cadastrar_eleitor as cadastrar_eleitor_db
from database.conexao_SQL import criar_conexao
from modules.busca_edicao_remover import buscar_eleitor, editar_eleitor, remover_eleitor
from database.inserir_cand import inserir_candidatos
from database.busca_cand import buscar_candidato
from database.delete_cand import deletar_candidato
from database.atualizar_partido import atualizar_partido
from modules.busca_edicao_remover import listar_eleitores
from modules.abertura_urna import abertura_urna

from logs.sistemas_de_logs import (
    exibir_logs,
    registrar_alerta_voto_duplo,
    registrar_voto_sucesso,
    registrar_encerramento
)

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
            case "1": print("Lendo arquivos de log..."),exibir_logs()
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
    conexao, cursor = criar_conexao()
    if not conexao or not cursor:
        print("[ERRO] Sem conexão com o banco.")
        return

    #---------------eleitor-------------

    # validação titulo
    titulo = input("Digite seu título eleitoral: ")
    cursor.execute("SELECT * FROM eleitores WHERE titulo = %s", (titulo,))
    eleitor = cursor.fetchone()
    if eleitor is None:
        print("Credenciais inválidas. Acesso negado.")
        cursor.close()
        conexao.close()
        return

    #validação cpf
    cmc_cpf = input("Digite os 4 primeiros dígitos do CPF: ")
    if eleitor[3][:4] != cmc_cpf:
        print("Credenciais inválidas. Acesso negado.")
        cursor.close()
        conexao.close()
        return

    #validar chave de acesso
    chave_acesso = input("Digite sua chave de acesso: ")
    if eleitor[4] != chave_acesso:
        print("Credenciais inválidas. Acesso negado.")
        cursor.close()
        conexao.close()
        return


    # Verificar se já votou
    if eleitor[6] == "Já Votou": 
            registrar_alerta_voto_duplo(titulo)
            print("Eleitor já realizou a votação.")
            cursor.close()
            conexao.close()
            return

#-------------candidato--------------
    voto_finalizado = False
    while not voto_finalizado:
        numero = input("Digite o numero do candidato: ")

        # Buscar candidato
        cursor.execute("SELECT * FROM candidatos WHERE numero = %s", (numero,))
        candidato = cursor.fetchone()

        if not candidato:
            print("Candidato não encontrado. Tente outro número.")
            continue

        print(f"\nCandidato encontrado:")
        print(f"Numero  : {candidato[2]}")
        print(f"Nome    : {candidato[1]}")
        print(f"Partido : {candidato[3]}")

        confirma = ""
        while confirma not in ["S", "N"]:
            confirma = input("\nConfirmar voto? (S/N): ").upper()
            if confirma not in ["S", "N"]:
                print("Opcao invalida. Digite apenas S ou N.")

        if confirma == "S":
            voto_finalizado = True
            # Gerar protocolo único
            protocolo = f"{titulo}{candidato[2]}{eleitor[0]}"

            # Registrar voto
            cursor.execute(
                "INSERT INTO votos (id_candidato, data_hora, protocolo) VALUES (%s, NOW(), %s)",
                (candidato[0], protocolo)
            )
            # Atualizar contagem do candidato
            cursor.execute(
                "UPDATE candidatos SET total_votos = total_votos + 1 WHERE id = %s",
                (candidato[0],)
            )
            # Marcar eleitor como já votou
            cursor.execute(
                "UPDATE eleitores SET status_voto = 'Já Votou' WHERE titulo = %s",
                (titulo,)
            )
            conexao.commit()
            registrar_voto_sucesso(protocolo)
            print("[SUCESSO] Voto registrado com sucesso!")
        # Se confirma == "N", o while volta a rodar (pede número de novo)

    cursor.close()
    conexao.close()


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
    registrar_encerramento()
    menu_resultados()

# //// MENU DA URNA ////
def menu_urna():
    opcao_urna = ""
    while opcao_urna != "3":
        print("\n--- [MENU URNA] ---")
        print("1. Votar")
        print("2. Encerrar Votacao")
        print("3. Voltar")

        opcao_urna = input("\nEscolha uma opcao: ")

        match opcao_urna:
            case "1": fluxo_voto()
            case "2": encerrar_votacao()
            case "3": print("Voltando ao menu anterior...")
            case _: print("Opcao invalida, tente novamente.")

# //// LOGIN DO MESARIO ////
def login_mesario():
    print("\n--- [LOGIN DO MESARIO] ---")

    conexao, cursor = criar_conexao()

    if not conexao or not cursor:
        print("[ERRO] Falha na conexão com o banco de dados.")
        return

    autenticado = abertura_urna(cursor, conexao)

    cursor.close()
    conexao.close()

    if autenticado:
        print("[SUCESSO] Login realizado com sucesso!")
        menu_urna()
    else:
        print("[ERRO] Autenticação falhou. Voltando ao menu...")


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
            case "1":
                login_mesario()
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
                    print("----------------------")
                    termo = input("Digite o CPF ou Título: ")
                    buscar_eleitor(termo)
            case "5":
                print("Listando todos os eleitores...")
                listar_eleitores()
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
