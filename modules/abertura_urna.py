from database.conexao_SQL import criar_conexao
def zerézima(cursor, conexao):
    print("\n--- INICIANDO ZERÉZIMA ---")

    cursor.execute("DELETE FROM votos") #Toda esta area esta responsavel por limpar e zerar os registros
    cursor.execute("UPDATE candidatos SET total_votos = 0")
    cursor.execute("UPDATE eleitores SET status_votos ='Não Votou'")
    conexao.commit()
    print("Registro de Votação limpos com sucesso!")

    cursor.execute("SELECT  * FROM candidatos")
    candidatos = cursor.fetchall()

    print("\n--- CANDIDATOS REGISTRADOS ---")
    
    for candidato in candidatos: #area responsavel por listar os candidatos
        print(f"Nome: {candidato[1]}")
        print(f"Numero:{candidato[2]}")
        print(f"Partido:{candidato[3]}")
        print(f"Votos: 0")

        print("\nZerézima concluida com sucesso! A urna esta vazia e pronta para a votação!")
        return True




def abertura_urna(cursor, conexao):
    print("\n--- ABERTURA DO SISTEMA DE VOTAÇÃO ---")
    titulo= input("Digite seu titulo de eleitor: ")#pede o titulo
    cmc_cpf= input("Digite os 4 primeiros digitos do CPF: ")#pede os 4 primeiros digitos do cpf
    chave_acesso= input("Digite sua chave de acesso: ")#pede a chave de acesso
    
    cursor.execute("SELECT * FROM eleitores WHERE titulo = %s", (titulo,) )#vai buscar no bd o eleitor pelo titulo
    eleitor = cursor.fetchone()

    if not eleitor: #vai verificar se o eleitor existe
        print("Dados incorretos. A validação falhou!")
        return False
    
    if eleitor[2] != titulo: #vai verificar se o titulo que consta no banco esta igual ao digitado
        print("Dados incorretos. A validaçãp falhou!")
        return False
    
    if eleitor[3][:4] != cmc_cpf: #vai verificar se os 4 primeiros digistos do cpf são iguais tanto no painel quanto no bd
        print("Dados incorretos. A validaçãp falhou!")
        return False

    if eleitor[4] !=chave_acesso: #vai verificar se a chave de acesso corresponde em ambos os lugares
        print("Dados incorretos. A validaçãp falhou!")
        return False
    
    if not eleitor[5]: #vai verificar se tem registro como mesario
        print("Erro. Este eleitor não possui perfil de mesario!")
        return False
     
    print(f"Bem vindo, {eleitor[1]}! Identidade validada com sucesso!")

    zerézima(cursor, conexao)
    return True

