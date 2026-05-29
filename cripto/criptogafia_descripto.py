from database.conexao_SQL import criar_conexao

"""Modulo de criptografia de dados usando a Cifra de Hill (blocos de 2).

Atende ao requisito RNF006: criptografar CPF, chave de acesso e protocolo
de votacao antes de gravar no banco, e descriptografar ao consultar.

A chave da cifra e uma matriz 2x2. Para a cifra ser reversivel, a matriz
precisa ser invertivel modulo 36 (tamanho do alfabeto):
    - Matriz de criptografia    : [[5, 8], [17, 3]]   (determinante 23 mod 36)
    - Matriz de descriptografia : [[33, 20], [29, 19]] (a inversa mod 36)
"""

# Alfabeto: cada caractere ocupa uma posicao, ex A=0...
ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
N = len(ALFABETO) 

# Caractere usado para completar o par quando o texto tem tamanho impar.
PADDING = "X"

# Matrizes da cifra (a de descriptografia e a inversa da de criptografia mod 36).
MATRIZ_CRIPTO = ([5, 8], [17, 3])
MATRIZ_DECRIPTO = ([33, 20], [29, 19])


def _normalizar(texto):
    """Padroniza o texto para entrar na cifra.

    Coloca em maiusculas e remove pontos e tracos (formatacao de CPF).

    Args:
        texto (str): Texto em claro, podendo conter formatacao (ex.: CPF).

    Returns:
        str: Texto somente com caracteres aceitos pela cifra, em maiusculas.
    """
    return texto.upper().replace("-", "").replace(".", "")


def _posicao(caractere):
    """Devolve a posicao de um caractere no alfabeto da cifra.

    Args:
        caractere (str): Um unico caractere a ser localizado no alfabeto.

    Returns:
        int: Indice do caractere no alfabeto (0 a 35).

    Raises:
        ValueError: Se o caractere nao pertencer ao alfabeto (A-Z, 0-9).
    """
    indice = ALFABETO.find(caractere)
    if indice == -1:
        raise ValueError(
            "Caractere invalido para a cifra: '%s'. "
            "So sao aceitos A-Z e 0-9." % caractere
        )
    return indice


def _aplicar_cifra(texto, matriz):
    """Aplica a multiplicacao da Cifra de Hill em blocos de 2 caracteres.

    Args:
        texto (str): Texto de tamanho par, com caracteres do alfabeto.
        matriz (list): Matriz 2x2 da cifra, no formato [[a, b], [c, d]].

    Returns:
        str: Texto resultante apos aplicar a cifra bloco a bloco.
    """
    (a, b), (c, d) = matriz
    resultado = ""
    for i in range(0, len(texto), 2):
        p1 = _posicao(texto[i])
        p2 = _posicao(texto[i + 1])
        n1 = (a * p1 + b * p2) % N
        n2 = (c * p1 + d * p2) % N
        resultado += ALFABETO[n1] + ALFABETO[n2]
    return resultado


def criptografia_dados(texto):
    """Criptografa um dado em claro para ser gravado no banco.

    Usada antes de qualquer INSERT/UPDATE de CPF, chave de acesso ou
    protocolo de votacao. Se o texto tiver tamanho impar, um
    caractere de padding e adicionado para fechar o ultimo bloco.

    Args:
        texto (str): Dado em claro (ex.: '123.456.789-01' ou 'ANS4821').

    Returns:
        str: Texto cifrado, pronto para ser persistido no banco.

    Raises:
        ValueError: Se o texto for vazio ou contiver caractere fora do
            alfabeto aceito (A-Z, 0-9).
    """
    texto = _normalizar(texto)

    if texto == "":
        raise ValueError("Texto vazio: nada para criptografar.")

    # A cifra trabalha de 2 em 2. Se for impar, completa o ultimo par.
    if len(texto) % 2 != 0:
        texto += PADDING

    return _aplicar_cifra(texto, MATRIZ_CRIPTO)


def descriptografia_dados(cifrado):
    """Descriptografa um dado lido do banco, devolvendo o valor original.

    Usada ao consultar/exibir um eleitor ou ao recuperar um protocolo.
    Remove o caractere de padding ao final, caso ele tenha sido
    adicionado durante a criptografia.

    Args:
        cifrado (str): Texto cifrado exatamente como esta no banco.

    Returns:
        str: Texto original em claro, sem o padding.

    Raises:
        ValueError: Se o texto cifrado tiver tamanho impar (corrompido ou
            incompleto) ou contiver caractere fora do alfabeto.
    """
    cifrado = cifrado.upper()

    if len(cifrado) % 2 != 0:
        raise ValueError(
            "Texto cifrado invalido: o tamanho deveria ser par. "
            "Pode estar corrompido ou incompleto."
        )

    texto = _aplicar_cifra(cifrado, MATRIZ_DECRIPTO)

    # Remove o padding 'X' do final, se houver (era so para fechar o par).
    if texto.endswith(PADDING):
        texto = texto[:-1]

    return texto

