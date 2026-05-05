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
 
 
'''Buscar Eleitor'''

def buscar_eleitor(termo):
    conexao, cursor = criar_conexao()
    if not conexao:
        return []

    try:
        sql = "SELECT id, nome, titulo, cpf, is_mesario, status_voto FROM eleitores WHERE nome = %s OR titulo = %s"
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
 
def editar_eleitor(id_eleitor, novo_nome, novo_cpf, novo_titulo, novo_mesario):
    conexao, cursor = criar_conexao()
    if not conexao:
        return False

    try:
        # Buscar dados atuais
        cursor.execute("""
            SELECT id, nome, titulo, cpf, is_mesario, status_voto 
            FROM eleitores WHERE id = %s
        """, (id_eleitor,))
        
        eleitor = cursor.fetchone()

        if not eleitor:
            print("Nenhum eleitor encontrado com esse ID.")
            return False

        print("\n--- Dados atuais ---")
        exibir_eleitor(eleitor)

        # Atualizar
        sql = """
            UPDATE eleitores 
            SET nome = %s, cpf = %s, titulo = %s, is_mesario = %s 
            WHERE id = %s
        """
        cursor.execute(sql, (novo_nome, novo_cpf, novo_titulo, novo_mesario, id_eleitor))
        conexao.commit()

        # Buscar dados atualizados
        cursor.execute("""
            SELECT id, nome, titulo, cpf, is_mesario, status_voto 
            FROM eleitores WHERE id = %s
        """, (id_eleitor,))
        
        eleitor_atualizado = cursor.fetchone()

        print("\n--- Dados atualizados ---")
        exibir_eleitor(eleitor_atualizado)

        return True

    except Exception as e:
        print("Erro ao editar eleitor:", e)
        return False

    finally:
        cursor.close()
        conexao.close()

'''Remover Eleitor'''
 
def confirmar_remocao(cursor, conexao, id_eleitor):
    confirma = input("\nConfirmar remocao? (S/N): ").upper()
    if confirma == "S":
        cursor.execute("DELETE FROM eleitores WHERE id = %s", (id_eleitor,))
        conexao.commit()
        print("Eleitor removido com sucesso!")
        return True
    elif confirma == "N":
        print("Remocao cancelada.")
        return False
    else:
        print("Opcao invalida. Digite apenas S ou N.")
        return confirmar_remocao(cursor, conexao, id_eleitor)


def remover_eleitor(id_eleitor):
    conexao, cursor = criar_conexao()
    if not conexao:
        return False

    try:
        cursor.execute("SELECT nome, titulo, cpf, is_mesario FROM eleitores WHERE id = %s", (id_eleitor,))
        eleitor = cursor.fetchone()

        if not eleitor:
            print("Nenhum eleitor encontrado com esse ID.")
            return False

        print(f"\nEleitor encontrado:")
        exibir_eleitor(eleitor)

        return confirmar_remocao(cursor, conexao, id_eleitor)

    except Exception as e:
        print("Erro ao remover eleitor:", e)
        return False

    finally:
        cursor.close()
        conexao.close()