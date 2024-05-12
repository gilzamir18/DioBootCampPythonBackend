import time
import os

def limpar_terminal():
    """
    Limpa o terminal verificando qual sistema operacional está sendo utilizado.
    """
    if os.name == 'posix':  # Unix/Linux/MacOS
        os.system('clear')
    elif os.name == 'nt':  # Windows
        os.system('cls')

def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    #return saldo e extrato
    excedeu_saldo = valor > saldo

    excedeu_limite = valor > limite

    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1

    else:
        print("Operação falhou! O valor informado é inválido.")
    
    return saldo, extrato

def deposito(saldo, valor, extrato, /):
    #return saldo e extrato
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    #nome, dt_nascimento, cpf, endereco
    cpf = input("CPF do novo usuário (somente números): ")
    usuario = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    if usuario:
        print(f"\n@@@ Já existe usuário com esse CPF: {cpf} @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, 
                            endereco: endereco})
    print("@@@ Usuário criado com sucesso! @@@")

def criar_conta(contas, usuarios):
    cpf = input("Informe o CPF do usuário para o qual a conta será criada: ")
    usuario = [u for u in usuarios if u['cpf'] == cpf]
    if usuario:
        numero = str(len(contas) + 1)
        agencia = "0001"
        contas.append({'agencia': agencia, 'numero_conta': numero, 'usuario': usuario[0], 'ativo': True})
        print("\n@@@ Conta criada com sucesso! @@@")
    else:
        print("\n@@@ Usuário não encontrado, fluxo de criação da conta encerrado! @@@")

def listar_contas(contas):
    print(''.center(50, '*'))
    print('LISTA DE CONTAS ATIVAS'.center(50, '*'))
    print(''.center(50, '*'))
    if contas:
        for conta in contas:
            print("NÚMERO: ", conta['numero_conta'])
            print("AGÊNCIA: ", conta['agencia'])
            print("USUARIO: ", conta['usuario']['nome'], '(CPF: ', conta['usuario']['cpf'], ')')
            print("STATUS: ", 'ATIVA' if conta['ativo'] else 'INATIVA')
    else:
        print("NENHUMA CONTA CADASTRADA!")
    print(''.center(50, '*'))


menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[a] Adicionar usuário
[c] Criar conta
[l] Exibir todas as contas
[q] Sair
=> """


usuarios = []
contas = []

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 2

while True:
    limpar_terminal()
    print("".center(50, '*'))
    print("BANCO BRAGESCO".center(50, '*'))
    print("".center(50, '*'))
    opcao = input(menu)
    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))
        saldo, extrato = deposito(saldo, valor, extrato)
    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))
        saldo, extrato = saque(saldo=saldo, valor=valor, limite=limite,
                               numero_saques=numero_saques, extrato=extrato, limite_saques=LIMITE_SAQUES)
    elif opcao == "e":
        exibir_extrato(saldo, extrato=extrato)
    elif opcao == "a":
        criar_usuario(usuarios)
    elif opcao == "c":
        criar_conta(contas, usuarios)
    elif opcao == "l":
        listar_contas(contas)
    elif opcao == "q":
        break
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
    for i in range(5):
        print("\rProcessando", "."*i, end="")
        time.sleep(1)