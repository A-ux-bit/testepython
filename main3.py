SALARIO = float(input("informe o salário: "))

if SALARIO <= 3000:
    print("Programador junior")
elif SALARIO > 3000 and SALARIO <= 6000:
    print("Programador pleno")
elif SALARIO >6000 and SALARIO <= 15000:
    print("programador senior")
else:
    print("gerente de projetos")