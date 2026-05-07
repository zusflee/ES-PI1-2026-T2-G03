def validar_titulo(titulo):
    titulo = ''.join(filter(str.isdigit, titulo))

    if len(titulo) != 12:#Vai efetuar a verifiação para ver se tem 12 digitos 
        return False

    if titulo == titulo[0] * 12:#Vai verificar se não são todos iguais
        return False

    # separa as partes
    sequencial = titulo[:8]
    uf = titulo[8:10]
    dvs = titulo[10:12]
    uf_num = int(uf)

        
    if uf_num == 0 or uf_num > 28: #vai ficar responsalver para verificar se a UF esta entre 0 e 28
        return False

    
    pesos1 = [2, 3, 4, 5, 6, 7, 8, 9] # primeiro dígito verificador, vai ultilizar os pesos 2 3 4 5 6 7 8 9
    soma1 = 0
    for i in range(8):
        soma1 += int(sequencial[i]) * pesos1[i]
    resto1 = soma1 % 11

    if resto1 == 10:
        dv1 = 0
    elif resto1 == 0:
        if uf_num in [1, 2]:  # SP e MG
            dv1 = 1
        else:
            dv1 = 0
    else:
        dv1 = resto1

    if dv1 != int(dvs[0]):
        return False

    
    soma2 = (int(uf[0]) * 7) + (int(uf[1]) * 8) + (dv1 * 9) # segundo dígito verificador vai utilizar os pesos 7 8 9
    resto2 = soma2 % 11

    if resto2 == 10:
        dv2 = 0
    elif resto2 == 0:
        if uf_num in [1, 2]:  # SP e MG
            dv2 = 1
        else:
            dv2 = 0
    else:
        dv2 = resto2

    if dv2 != int(dvs[1]):
        return False

    return True

if __name__ == "__main__":
    titulo = input("Digite o título de eleitor: ")
    if validar_titulo(titulo):
        print("Título válido!")
    else:
        print("Título inválido!")

