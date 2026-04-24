def validar_titulo(titulo):
    titulo = ''.join(filter(str.isdigit, titulo))
    
    if len(titulo) != 12: # verifica se tem 12 dígitos
        return False
    
    if titulo == titulo[0] * 12:# verifica se não são todos iguais
        return False
    
    estado = int(titulo[8:10])# verifica se o estado é válido (01 a 28)
    if estado == 0 or estado > 28:
        return False
    
    return True

titulo = input("Digite o título de eleitor: ")
if validar_titulo(titulo):
    print("Título válido!") 
else:
    print("Título inválido!")