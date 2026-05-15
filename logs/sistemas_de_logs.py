import os
from datetime import datetime

ARQUIVO_LOG = os.path.join(os.path.dirname(__file__), "log_ocorrencias.txt")
with open(ARQUIVO_LOG, "w", encoding="utf-8") as arquivo:
    arquivo.write("INICIO DA VOTAÇÃO\n")    

def registrar_log(mensagem):
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"[{agora}] {mensagem}\n"

    with open(ARQUIVO_LOG, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha)

def registrar_abertura():
    registrar_log("ABERTURA: Votação iniciada com sucesso.")

def registrar_exclusao_usuario(tipo, nome, titulo):
    registrar_log(f"EXCLUSAO: {tipo} removido com sucesso. Nome: {nome}. Título: {titulo}")

def registrar_exclusao_candidato(nome, numero):
    registrar_log(f"EXCLUSAO: Candidato removido com sucesso. Nome: {nome}. Número: {numero}")


def registrar_alteracao_candidato(nome, numero, campo, valor_antigo, valor_novo):
    registrar_log(
        f"ALTERACAO: Candidato alterado com sucesso. "
        f"Nome: {nome}. Número: {numero}. "
        f"Campo: {campo}. De: {valor_antigo}. Para: {valor_novo}"
    )

def registrar_alteracao_usuario(tipo, nome, titulo, campo, valor_antigo, valor_novo):
    registrar_log(
        f"ALTERACAO: {tipo} alterado com sucesso. "
        f"Nome: {nome}. Título: {titulo}. "
        f"Campo: {campo}. De: {valor_antigo}. Para: {valor_novo}"
    )


def registrar_cadastro_eleitor(nome, titulo):
    registrar_log(f"CADASTRO: Eleitor cadastrado com sucesso. Nome: {nome}. Título: {titulo}")


def registrar_cadastro_mesario(nome, titulo):
    registrar_log(f"CADASTRO: Mesário cadastrado com sucesso. Nome: {nome}. Título: {titulo}")


def registrar_abertura():
    registrar_log("ABERTURA: Votação iniciada com sucesso. Total de votos zerado.")


def registrar_alerta_acesso(motivo="Tentativa de acesso negado."):
    registrar_log(f"ALERTA: {motivo}")


def registrar_alerta_voto_duplo(titulo=None):
    if titulo:
        registrar_log(f"ALERTA: Tentativa de voto duplo. Título: {titulo}")
    else:
        registrar_log("ALERTA: Tentativa de voto duplo.")


def registrar_voto_sucesso(protocolo=None):
    if protocolo:
        registrar_log(f"SUCESSO: Voto realizado com sucesso. Protocolo: {protocolo}")
    else:
        registrar_log("SUCESSO: Voto realizado com sucesso.")


def registrar_encerramento():
    registrar_log("ENCERRAMENTO: Votação encerrada com sucesso.")


def exibir_logs():
    if not os.path.exists(ARQUIVO_LOG):
        print("\nNenhum log encontrado.\n")
        return

    print("\n===== LOGS DE OCORRÊNCIAS =====\n")
    with open(ARQUIVO_LOG, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read().strip()

    if conteudo:
        print(conteudo)
    else:
        print("Arquivo de log vazio.")

    print("\n===============================\n")
