from database.conexao_SQL import criar_conexao
 
 
'''Buscar Eleitor'''

def buscar_eleitor(termo):
    conexao, cursor = criar_conexao()
    if not conexao:
        return []
 
    try:
        sql = "SELECT id, nome, titulo, cpf, is_mesario, status_voto FROM eleitores WHERE nome = %s OR titulo = %s"
        cursor.execute(sql, (termo, termo))
 
        resultado = cursor.fetchall()
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
        sql = "UPDATE eleitores SET nome = %s, cpf = %s, titulo = %s, is_mesario = %s WHERE id = %s"
        cursor.execute(sql, (novo_nome, novo_cpf, novo_titulo, novo_mesario, id_eleitor))
        conexao.commit()

        if cursor.rowcount == 0:
            print("Nenhum eleitor encontrado com esse ID.")
            return False

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
        print(f"Nome    : {eleitor[0]}")
        print(f"Titulo  : {eleitor[1]}")
        print(f"CPF     : {eleitor[2]}")
        print(f"Mesario : {'Sim' if eleitor[3] == 1 else 'Nao'}")

        return confirmar_remocao(cursor, conexao, id_eleitor)

    except Exception as e:
        print("Erro ao remover eleitor:", e)
        return False

    finally:
        cursor.close()
        conexao.close()