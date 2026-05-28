import random

LETRAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def gerar_protocolo(numero_candidato):
    """
    Gera um protocolo de votacao no padrao do escopo:
    "V" + 2 letras aleatorias + Ano (26) + Numero do Candidato (2 digitos)
    + 5 digitos aleatorios. Ex: VRT269950134.
    Para voto nulo, passar 0 (vira "00" no protocolo).

    Args:
        numero_candidato (int): Numero do candidato. Use 0 para voto nulo.

    Returns:
        str: Protocolo no formato VAB26NN12345 (12 caracteres).
    """
    # 2 letras aleatorias
    letras = ""
    for _ in range(2):
        posicao = random.randint(0, 25)   # sorteia um indice de 0 a 25
        letras += LETRAS[posicao]         # pega a letra naquela posicao

    # Ano fixo
    ano = "26"

    # Numero do candidato com 2 digitos
    num_str = str(numero_candidato)
    if len(num_str) < 2:
        num_str = "0" + num_str           # ex: "5" vira "05"
    elif len(num_str) > 2:
        num_str = num_str[-2:]            # ex: "133" vira "33"

    # 5 digitos aleatorios
    digitos = ""
    for _ in range(5):
        digitos += str(random.randint(0, 9))   # sorteia um numero de 0 a 9

    return f"V{letras}{ano}{num_str}{digitos}"