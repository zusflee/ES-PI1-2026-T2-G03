def cadastro_eleitor():
    print("CADASTRO DE ELEITOR")
    nome=input("Digite o nome completo: ")
    
    titulo=input("Diigite seu titulo: ")#Cadastro de titulo
    if not validar_titulo(titulo):
        print("Titulo Invalido, deve contar 12 digitos")
        return
    
    cpf=input("Digite o seu CPF(somente numeros): ")#Cadastro de cpf
    if not validação_de_cpf(cpf):
        print("CPF invalido")
        return
    
    pergunta=input("Voce atuára como mesario? (S/N): ")
    pergunta= pergunta.lower()
    if pergunta == 's':
      mesario=True
    else:
      mesario=False
 