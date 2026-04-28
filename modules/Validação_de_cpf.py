def validação_de_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))#Vai limpar os pontos e traços contidos no cpf

    if len(cpf) !=11: #Verificação para ver se tem os 11 digistos necessarios
        return False 
    if cpf == cpf[0] *11: #Verificação para ver se os numeros não são iguais
        return False
    
    soma= 0 #primeiro digito verificador
    for i in range(9):
       soma+= int(cpf[i])*(10-i)
    resto= soma % 11
    if resto <2:
        digito1 = 0
    else:
        digito1= 11 - resto
    if digito1 != int(cpf[9]):
      return False 
    
    soma=0
    for i in range(10):
       soma+= int(cpf[i])*(11-i)
    resto= soma % 11
    if resto <2:
        digito2 = 0
    else:
       digito2= 11 - resto
    if digito2 != int(cpf[10]):
       return False
       

    return True
