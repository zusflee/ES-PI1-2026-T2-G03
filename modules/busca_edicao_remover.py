from database.conexao_SQL import criar_conexao
from logs.sistemas_de_logs import registrar_alteracao_usuario, registrar_exclusao_usuario
from cripto.criptogafia_descripto import descriptografia_dados, criptografia_dados
from modules.Validação_de_cpf import validação_de_cpf
from modules.ValidaçãoTituloNEW import validar_titulo

'''Função de exibir eleitor'''

def exibir_eleitor(eleitor):
    print(f"\nEleitor:")
    print(f"ID      : {eleitor[0]}")
    print(f"Nome    : {eleitor[1]}")
    print(f"Titulo  : {eleitor[2]}")
    print(f"CPF     : {descriptografia_dados(eleitor[3])}")
    print(f"Chave   : {descriptografia_dados(eleitor[4])}")
    print(f"Mesario : {'Sim' if eleitor[5] == 1 else 'Nao'}")
    print(f"Votou   : {eleitor[6]}")


'''Buscar eleitor por ID (uso interno)'''

def buscar_por_id(cursor, id_eleitor):
    cursor.execute("""
        SELECT id, nome, titulo, cpf, chave_acesso, is_mesario, status_voto
        FROM eleitores WHERE id = %s
        """, (id_eleitor,))
    return cursor.fetchone()


'''Buscar Eleitor por nome ou titulo'''

def buscar_eleitor(termo):
    conexao, cursor = criar_conexao()
    if conexao == None:
        return []

    try:
        # cifra o termo pra poder comparar com o cpf cifrado no banco
        termo_cifrado = criptografia_dados(termo)

        sql = """
            SELECT id, nome, titulo, cpf, chave_acesso, is_mesario, status_voto
            FROM eleitores WHERE cpf = %s OR titulo = %s
            """
        cursor.execute(sql, [termo_cifrado, termo])
        resultado = cursor.fetchall()

        if not resultado:
            print("Nenhum eleitor encontrado.")
            return []

        print(f"\n{len(resultado)} eleitor(es) encontrado(s):")
        for eleitor in resultado:
            print("\n----------------------")
            exibir_eleitor(eleitor)

        return resultado

    except Exception as e:
        print("Erro ao buscar eleitor:", e)
        return []

    finally:
        cursor.close()
        conexao.close()


'''Editar Eleitor'''

def editar_eleitor():
    conexao, cursor = criar_conexao()
    if conexao == None:
        return 0

    try:
        id_eleitor = int(input("\nDigite o ID do eleitor: "))

        eleitor = buscar_por_id(cursor, id_eleitor)
        while eleitor is None:
            print("Nenhum eleitor encontrado com esse ID.")
            id_eleitor = int(input("Digite o ID do eleitor: "))
            eleitor = buscar_por_id(cursor, id_eleitor)

        print("\n--- Dados atuais ---")
        exibir_eleitor(eleitor)

        confirma = ""
        while confirma not in ["S", "N"]:
            confirma = input("\nDeseja editar este eleitor? (S/N): ").upper()
            if confirma not in ["S", "N"]:
                print("[ERRO] Digite apenas S ou N.")

        if confirma == "N":
            print("Edicao cancelada.")
            return 0

        print("\n--- O que deseja editar? ---")
        print("1 - Nome")
        print("2 - Titulo")
        print("3 - CPF")
        print("4 - Mesario")
        print("0 - Cancelar")

        opcao_campo = input("\nEscolha uma opcao: ").strip()

        if opcao_campo == "0":
            print("Edicao cancelada.")
            return 0

        campos = {
            "1": ("nome",       "Novo nome: "),
            "2": ("titulo",     "Novo titulo: "),
            "3": ("cpf",        "Novo CPF: "),
            "4": ("is_mesario", "E mesario? (S/N): "),
        }

        if opcao_campo not in campos:
            print("[ERRO] Opcao invalida.")
            return 0

        coluna, pergunta = campos[opcao_campo]

        nome_atual = eleitor[1]
        titulo_atual = eleitor[2]
        tipo = "Mesário" if eleitor[5] == 1 else "Eleitor"

        campo_log = ""
        valor_antigo_log = ""
        valor_novo_log = ""

        if opcao_campo == "4":
            novo_valor = ""
            while novo_valor not in ["S", "N"]:
                novo_valor = input(pergunta).upper()
                if novo_valor not in ["S", "N"]:
                    print("[ERRO] Digite apenas S ou N.")
            valor_antigo_log = "Sim" if eleitor[5] == 1 else "Nao"
            novo_valor = 1 if novo_valor == "S" else 0
            valor_novo_log = "Sim" if novo_valor == 1 else "Nao"
            campo_log = "mesario"
        else:
            novo_valor = input(pergunta).strip()
            if not novo_valor:
                print("[ERRO] Valor invalido.")
                return 0

            if coluna == "nome":
                valor_antigo_log = eleitor[1]
                campo_log = "nome"

            elif coluna == "titulo":
                # valida o titulo com a funcao oficial (RF001.05)
                if not validar_titulo(novo_valor):
                    print("[ERRO] Titulo invalido.")
                    return 0

                # verifica duplicidade: nao pode existir outro eleitor com o mesmo titulo
                cursor.execute(
                    "SELECT id FROM eleitores WHERE titulo = %s AND id != %s",
                    [novo_valor, id_eleitor]
                )
                if cursor.fetchone() is not None:
                    print("[ERRO] Ja existe outro eleitor com esse titulo.")
                    return 0

                valor_antigo_log = eleitor[2]
                campo_log = "titulo"

            elif coluna == "cpf":
                # valida o cpf com a funcao oficial (RF001.05)
                if not validação_de_cpf(novo_valor):
                    print("[ERRO] CPF invalido.")
                    return 0

                # cifra o CPF antes de salvar (mantem consistencia com o resto do banco)
                novo_valor_cifrado = criptografia_dados(novo_valor)

                # verifica duplicidade comparando cifrado com cifrado
                cursor.execute(
                    "SELECT id FROM eleitores WHERE cpf = %s AND id != %s",
                    [novo_valor_cifrado, id_eleitor]
                )
                if cursor.fetchone() is not None:
                    print("[ERRO] Ja existe outro eleitor com esse CPF.")
                    return 0

                valor_antigo_log = eleitor[3]
                campo_log = "cpf"
                novo_valor = novo_valor_cifrado   # o UPDATE depois vai usar o valor cifrado
                
        valor_novo_log = novo_valor

        sql = f"UPDATE eleitores SET {coluna} = %s WHERE id = %s"
        cursor.execute(sql, [novo_valor, id_eleitor])
        conexao.commit()

        if cursor.rowcount > 0:
            registrar_alteracao_usuario(
                tipo,
                nome_atual,
                titulo_atual,
                campo_log,
                valor_antigo_log,
                valor_novo_log
            )
        print("\n--- Dados atualizados ---")
        exibir_eleitor(buscar_por_id(cursor, id_eleitor))

        return 1

    except Exception as e:
        print("Erro ao editar eleitor:", e)
        return 0

    finally:
        cursor.close()
        conexao.close()


'''Remover Eleitor'''

def remover_eleitor():
    conexao, cursor = criar_conexao()
    if conexao == None:
        return 0

    try:
        id_eleitor = int(input("\nDigite o ID do eleitor: "))

        eleitor = buscar_por_id(cursor, id_eleitor)
        while eleitor is None:
            print("Nenhum eleitor encontrado com esse ID.")
            id_eleitor = int(input("Digite o ID do eleitor: "))
            eleitor = buscar_por_id(cursor, id_eleitor)

        print("\n--- Eleitor encontrado ---")
        exibir_eleitor(eleitor)

        confirma = ""
        while confirma not in ["S", "N"]:
            confirma = input("\nConfirmar remocao? (S/N): ").upper()
            id_eleitor


        if confirma == "S":
            nome = eleitor[1]
            titulo_eleitor = eleitor[2]
            tipo = "Mesário" if eleitor[5] == 1 else "Eleitor"
            cursor.execute("DELETE FROM eleitores WHERE id = %s", [id_eleitor])
            conexao.commit()
            registrar_exclusao_usuario(tipo, nome, titulo_eleitor)
            print("Eleitor removido com sucesso!")
            return 1
        
        print("Remocao cancelada.")
        return 0

    except Exception as e:
        print("Erro ao remover eleitor:", e)
        return 0

    finally:
        cursor.close()
        conexao.close()

'''Listar Eleitores'''

def listar_eleitores():
    conexao, cursor = criar_conexao()
    if conexao == None:
        return

    try:
        cursor.execute("""
            SELECT id, nome, titulo, cpf, chave_acesso, is_mesario, status_voto
            FROM eleitores ORDER BY nome
            """)
        eleitores = cursor.fetchall()

        # Verifica se existe pelo menos um eleitor cadastrado
        if not eleitores:
            print("\nNenhum eleitor cadastrado no sistema.")
            return

        print(f"\n{'='*50}")
        print(f"  LISTA DE ELEITORES ({len(eleitores)} cadastrado(s))")
        print(f"{'='*50}")  

        for eleitor in eleitores:
            exibir_eleitor(eleitor)
            print("-" * 50)  # Separador visual entre eleitores

    except Exception as e:
        print(f"\nErro ao listar eleitores: {e}")

    finally:
        cursor.close()
        conexao.close()