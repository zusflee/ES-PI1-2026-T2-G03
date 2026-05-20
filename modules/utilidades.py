import os

def limpar_tela():
    """
    Limpa o terminal de acordo com o sistema operacional.
    """
    os.system('cls' if os.name == 'nt' else 'clear')