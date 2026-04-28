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
 
def remover_eleitor(id_eleitor):
    conexao, cursor = criar_conexao()
    if not conexao:
        return False
 
    try:
        sql = "DELETE FROM eleitores WHERE id = %s"
        cursor.execute(sql, (id_eleitor,))
        conexao.commit()
 
        if cursor.rowcount == 0:
            print("Nenhum eleitor encontrado com esse ID.")
            return False
 
        return True
 
    except Exception as e:
        print("Erro ao remover eleitor:", e)
        return False
 
    finally:
        cursor.close()
        conexao.close()