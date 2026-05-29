import os
from datetime import datetime

ARQUIVO_LOG = os.path.join(os.path.dirname(__file__), "log_ocorrencias.txt")
with open(ARQUIVO_LOG, "w", encoding="utf-8") as arquivo:
    arquivo.write("--LOG DE OCORRÊNCIAS--\n")    

def registrar_log(mensagem):
    """
    Grava uma linha no arquivo de log de ocorrencias com timestamp.
    A funcao adiciona a data e hora atual no formato [YYYY-MM-DD HH:MM:SS]
    antes da mensagem, atendendo ao RF002.02.01.02 do escopo.

    Args:
        mensagem (str): Texto descritivo do evento a ser registrado.

    Returns:
        None: Apenas grava a linha no arquivo de log.
    """
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"[{agora}] {mensagem}\n"

    with open(ARQUIVO_LOG, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha)

def registrar_exclusao_usuario(tipo, nome, titulo):
    """
    Registra no log a exclusao de um eleitor ou mesario do sistema.

    Args:
        tipo (str): Tipo do usuario removido ("Eleitor" ou "Mesario").
        nome (str): Nome do usuario removido.
        titulo (str): Titulo eleitoral do usuario removido.

    Returns:
        None: Apenas grava a linha no arquivo de log.
    """
    registrar_log(f"EXCLUSAO: {tipo} removido com sucesso. Nome: {nome}. Título: {titulo}")

def registrar_exclusao_candidato(nome, numero):
    """
    Registra no log a exclusao de um candidato do sistema.

    Args:
        nome (str): Nome do candidato removido.
        numero (int): Numero de votacao do candidato removido.

    Returns:
        None: Apenas grava a linha no arquivo de log.
    """
    registrar_log(f"EXCLUSAO: Candidato removido com sucesso. Nome: {nome}. Número: {numero}")


def registrar_alteracao_candidato(nome, numero, campo, valor_antigo, valor_novo):
    """
    Registra no log a alteracao de um campo de um candidato.

    Args:
        nome (str): Nome do candidato alterado.
        numero (int): Numero de votacao do candidato.
        campo (str): Nome do campo alterado (ex: "partido").
        valor_antigo (str): Valor anterior do campo.
        valor_novo (str): Novo valor do campo.

    Returns:
        None: Apenas grava a linha no arquivo de log.
    """
    registrar_log(
        f"ALTERACAO: Candidato alterado com sucesso. "
        f"Nome: {nome}. Número: {numero}. "
        f"Campo: {campo}. De: {valor_antigo}. Para: {valor_novo}"
    )

def registrar_alteracao_usuario(tipo, nome, titulo, campo, valor_antigo, valor_novo):
    """
    Registra no log a alteracao de um campo de um eleitor ou mesario.

    Args:
        tipo (str): Tipo do usuario alterado ("Eleitor" ou "Mesario").
        nome (str): Nome do usuario alterado.
        titulo (str): Titulo eleitoral do usuario.
        campo (str): Nome do campo alterado (ex: "nome", "cpf", "titulo").
        valor_antigo (str): Valor anterior do campo.
        valor_novo (str): Novo valor do campo.

    Returns:
        None: Apenas grava a linha no arquivo de log.
    """
    registrar_log(
        f"ALTERACAO: {tipo} alterado com sucesso. "
        f"Nome: {nome}. Título: {titulo}. "
        f"Campo: {campo}. De: {valor_antigo}. Para: {valor_novo}"
    )


def registrar_cadastro_eleitor(nome, titulo):
    """
    Registra no log o cadastro bem-sucedido de um eleitor comum.

    Args:
        nome (str): Nome do eleitor cadastrado.
        titulo (str): Titulo eleitoral do eleitor cadastrado.

    Returns:
        None: Apenas grava a linha no arquivo de log.
    """
    registrar_log(f"CADASTRO: Eleitor cadastrado com sucesso. Nome: {nome}. Título: {titulo}")


def registrar_cadastro_mesario(nome, titulo):
    """
    Registra no log o cadastro bem-sucedido de um eleitor com perfil de mesario.

    Args:
        nome (str): Nome do mesario cadastrado.
        titulo (str): Titulo eleitoral do mesario cadastrado.

    Returns:
        None: Apenas grava a linha no arquivo de log.
    """
    registrar_log(f"CADASTRO: Mesário cadastrado com sucesso. Nome: {nome}. Título: {titulo}")

def registrar_tentativa_cadastro_duplicado(titulo):
    """
    Registra no log uma tentativa de cadastro de eleitor com CPF ou
    titulo ja existente no banco. Util para auditoria administrativa.

    Args:
        titulo (str): Titulo de eleitor informado na tentativa duplicada.

    Returns:
        None: Apenas grava a linha no arquivo de log.
    """
    registrar_log(f"ALERTA: Tentativa de cadastro duplicado. Titulo: {titulo}")


def registrar_abertura():
    """
    Registra no log o evento de abertura da urna (RF002.02.01.03).
    Chamada apenas apos validacao bem-sucedida do mesario e realizacao
    da zerezima.

    Returns:
        None: Apenas grava a linha no arquivo de log.
    """
    registrar_log("ABERTURA: Votação iniciada com sucesso. Total de votos zerado.")


def registrar_alerta_acesso(motivo=None):
    """
    Registra no log o evento de tentativa de acesso negado (RF002.02.01.04).
    A mensagem literal exigida pelo escopo e sempre registrada, podendo
    ser complementada com um motivo descritivo opcional para fins de
    auditoria detalhada.

    Args:
        motivo (str): Descricao adicional da falha (opcional). Ex: "CPF
            incorreto na abertura da urna." Se omitido, registra apenas
            a mensagem literal do escopo.

    Returns:
        None: Apenas grava a linha no arquivo de log.
    """
    if motivo:
        registrar_log(f"ALERTA: Tentativa de acesso negado. ({motivo})")
    else:
        registrar_log("ALERTA: Tentativa de acesso negado.")


def registrar_alerta_voto_duplo(titulo=None):
    """
    Registra no log uma tentativa de voto duplo (RF002.02.01.05).
    Acionada quando um eleitor com status 'Já Votou' tenta votar novamente.

    Args:
        titulo (str): Titulo eleitoral do eleitor que tentou votar
            duas vezes (opcional). Se omitido, registra apenas o alerta
            generico.

    Returns:
        None: Apenas grava a linha no arquivo de log.
    """
    if titulo:
        registrar_log(f"ALERTA: Tentativa de voto duplo. Título: {titulo}")
    else:
        registrar_log("ALERTA: Tentativa de voto duplo.")


def registrar_voto_sucesso():
    """
    Registra no log o evento de voto realizado com sucesso (RF002.02.01.06).
    O protocolo nao e registrado no log para proteger o sigilo do voto -
    ele fica disponivel apenas no banco de dados, acessivel via menu de
    Auditoria > Ver Protocolos.

    Returns:
        None: Apenas grava a linha no arquivo de log.
    """
    registrar_log("SUCESSO: Voto realizado com sucesso.")


def registrar_encerramento():
    """
    Registra no log o evento de encerramento da votacao (RF002.02.01.07).
    Chamada apenas apos validacao bem-sucedida do mesario e confirmacao
    da dupla checagem da chave de acesso.

    Returns:
        None: Apenas grava a linha no arquivo de log.
    """
    registrar_log("ENCERRAMENTO: Votação finalizada com sucesso.")


def exibir_logs():
    """
    Le e exibe no terminal todo o conteudo do arquivo de log de ocorrencias
    (RF002.02.01.08). Mostra mensagem apropriada se o arquivo nao existir
    ou estiver vazio.

    Returns:
        None: A funcao apenas exibe os logs no terminal.
              Retorna None antecipadamente se o arquivo de log nao existir.
    """
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