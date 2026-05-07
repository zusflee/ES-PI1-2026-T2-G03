from database.conexao_SQL import criar_conexao


'''Função de exibir eleitor'''

def exibir_eleitor(eleitor):
    print(f"\nEleitor:")
    print(f"ID      : {eleitor[0]}")
    print(f"Nome    : {eleitor[1]}")
    print(f"Titulo  : {eleitor[2]}")
    print(f"CPF     : {eleitor[3]}")
    print(f"Mesario : {'Sim' if eleitor[4] == 1 else 'Nao'}")
    print(f"Votou   : {'Sim' if eleitor[5] == 1 else 'Nao'}")


'''Buscar eleitor por ID (uso interno)'''

def buscar_por_id(cursor, id_eleitor):
    cursor.execute("""
        SELECT id, nome, titulo, cpf, is_mesario, status_voto
        FROM eleitores WHERE id = %s
    """, (id_eleitor,))
    return cursor.fetchone()


'''Buscar Eleitor por nome ou titulo'''

def buscar_eleitor(termo):
    conexao, cursor = criar_conexao()
    if conexao == None:
        return []

    try:
        sql = """
            SELECT id, nome, titulo, cpf, is_mesario, status_voto
            FROM eleitores WHERE nome = %s OR titulo = %s
        """
        cursor.execute(sql, (termo, termo))
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
        if eleitor == None:
            print("Nenhum eleitor encontrado com esse ID.")
            return 0

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

        print("\n--- Digite os novos dados ---")
        novo_nome   = input("Novo nome: ")
        novo_titulo = input("Novo titulo: ")
        novo_cpf    = input("Novo CPF: ")

        novo_mesario = ""
        while novo_mesario not in ["S", "N"]:
            novo_mesario = input("E mesario? (S/N): ").upper()
            if novo_mesario not in ["S", "N"]:
                print("[ERRO] Digite apenas S ou N.")

        novo_mesario = 1 if novo_mesario == "S" else 0

        sql = """
            UPDATE eleitores
            SET nome = %s, cpf = %s, titulo = %s, is_mesario = %s
            WHERE id = %s
        """
        cursor.execute(sql, (novo_nome, novo_cpf, novo_titulo, novo_mesario, id_eleitor))
        conexao.commit()

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
        if eleitor == None:
            print("Nenhum eleitor encontrado com esse ID.")
            return 0

        print("\n--- Eleitor encontrado ---")
        exibir_eleitor(eleitor)

        confirma = ""
        while confirma not in ["S", "N"]:
            confirma = input("\nConfirmar remocao? (S/N): ").upper()
            if confirma not in ["S", "N"]:
                print("[ERRO] Digite apenas S ou N.")

        if confirma == "S":
            cursor.execute("DELETE FROM eleitores WHERE id = %s", (id_eleitor,))
            conexao.commit()
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