
def validar_titulo(titulo):
    titulo= ''.join(filter(str.isdigit, titulo))
    if len(titulo)==12:
        return True
    else:
        return False

titulo=input("Digite o titulo de eleitor: ")
if validar_titulo(titulo):
    print("Titulo validado")
else:
    print("Titulo Invalido")
