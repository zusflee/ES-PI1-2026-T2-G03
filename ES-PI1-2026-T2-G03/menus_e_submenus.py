# SISTEMA DE VOTACAO DIGITAL - Projeto Integrador

# --- SUBMENU DE AUDITORIA ---
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

# --- SUBMENU DE RESULTADOS ---
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

# --- FLUXO DE VOTO ---
def fluxo_voto():
    print("\n--- [VOTACAO] ---")
    titulo = input("Informe o Titulo de Eleitor: ")

    print("Validando eleitor no banco de dados...")

    if titulo == "":
        print("[ERRO] Titulo invalido. Retornando ao Menu Urna.")
        return

    print("Eleitor identificado com sucesso!")

    numero = input("Digite o numero do candidato: ")

    print("Candidato encontrado:")
    print("Numero : " + numero)
    print("Nome   : Candidato Ficticio")
    print("Partido: Partido Exemplo")

    confirma = input("\nConfirmar voto? (S/N): ").upper()

    if confirma == "S":
        print("Registrando voto no banco de dados...")
        print("Gerando protocolo de votacao...")
        print("Atualizando status do eleitor para Ja Votou...")
        print("[SUCESSO] Voto registrado com sucesso!")
    else:
        print("Voto cancelado. Voltando ao Menu Urna...")

# --- FLUXO DE ENCERRAR VOTACAO ---
def encerrar_votacao():
    print("\n--- [ENCERRAR VOTACAO] ---")
    confirma = input("Deseja realmente encerrar a votacao? (S/N): ").upper()

    if confirma != "S":
        print("Operacao cancelada. Voltando ao Menu Urna...")
        return

    chave = input("Confirme a chave de encerramento: ")

    if chave == "":
        print("[ERRO] Chave invalida. Operacao cancelada.")
        return

    print("Encerrando sistema de votacao...")
    print("[SUCESSO] Votacao encerrada!")
    menu_resultados()

# --- MENU DA URNA ---
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

# --- LOGIN DO MESARIO ---
def login_mesario():
    print("\n--- [LOGIN DO MESARIO] ---")
    usuario = input("Usuario: ")
    senha = input("Senha: ")

    if usuario == "" or senha == "":
        print("[ERRO] Usuario ou senha invalidos.")
        return

    print("[SUCESSO] Login realizado com sucesso!")
    print("Executando Zeresima (zerando contadores)...")
    print("Urna zerada e pronta para uso.")

    menu_urna()

# --- MENU DE VOTACAO ---
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

# --- CADASTRAR ELEITOR ---
def cadastrar_eleitor():
    print("\n--- [CADASTRAR ELEITOR] ---")
    nome = input("Nome: ")
    cpf = input("CPF: ")
    titulo = input("Titulo de Eleitor: ")
    mesario = input("E mesario? (S/N): ").upper()

    print("Validando dados...")

    if nome == "" or cpf == "" or titulo == "":
        print("[ERRO] Preencha todos os campos.")
        return

    print("Verificando duplicidade no banco de dados...")
    print("[SUCESSO] Eleitor " + nome + " cadastrado com sucesso!")

# --- MENU DE GERENCIAMENTO ---
def menu_gerenciamento():
    opcao_gerenciamento = ""
    while opcao_gerenciamento != "6":
        print("\n--- [GERENCIAMENTO] ---")
        print("1. Cadastrar Eleitor")
        print("2. Editar Eleitor")
        print("3. Remover Eleitor")
        print("4. Buscar Eleitor")
        print("5. Listar Eleitores")
        print("6. Voltar")

        opcao_gerenciamento = input("\nEscolha uma opcao: ")

        match opcao_gerenciamento:
            case "1": cadastrar_eleitor()
            case "2": print("Buscando eleitor para edicao...")
            case "3": print("Removendo eleitor do banco de dados...")
            case "4": print("Buscando eleitor...")
            case "5": print("Listando todos os eleitores...")
            case "6": print("Voltando ao menu principal...")
            case _: print("Opcao invalida, tente novamente.")

# --- INICIO DO SISTEMA ---
def iniciar_sistema():
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