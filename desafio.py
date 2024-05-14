"""
Sistema Bancário -  Bootcamp DIO Backend IA com Python
"""
from __future__ import annotations
import time
import os
import abc

class Historico:
    """
    Representa o histórico de transacões.
    """
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao: Transacao):
        """
        Adiciona uma nova transação.
        """
        self._transacoes.append(transacao)

    @property
    def transacoes(self):
        """
        Retorna todas as transações já realizadas.
        """
        return self._transacoes

class Conta:
    """
    Uma conta genérica com operações de depósito e de saque.
    Poderia representar uma conta salário básica.
    """
    def __init__(self, cliente, numero):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
        self._ativa = True
  
    @property
    def ativa(self):
        return self._ativa

    @property
    def agencia(self):
        return self._agencia

    @property
    def historico(self):
        return self._historico

    @property
    def saldo(self) -> float:
        """
        O saldo da conta.
        """
        return self._saldo
    
    @property
    def cliente(self):
        """
        Retorna o cliente dono da conta.
        """
        return self._cliente
    
    @property
    def numero(self):
        return self._numero

    @classmethod
    def nova_conta(cls, cliente : Cliente, numero : int):
        """
        Cria uma determinada conta com para o cliente em 'cliente' e com o número em 'numero'.
        """
        nova_conta = Conta(cliente, numero)
        return nova_conta

    def sacar(self, valor: float):
        """
        Retira o saldo conforme valor.
        """
        if valor <= self._saldo:
            self._saldo = self._saldo - valor
            return True
        else:
            return False

    def depositar(self, valor: float):
        """
        Adiciona no saldo conforme valor.
        """
        self._saldo += valor
        return True

class Transacao(abc.ABC):
    """
    Representa uma operação bancária.
    """
    def __init__(self):
        super().__init__()

    @abc.abstractmethod
    def registrar(self,  conta: Conta) -> bool:
        """
        Registrar a operação a ser realizada na conta representa pelo objeto em 'conta'.
        """

    @property
    @abc.abstractmethod
    def valor(self) -> float:
        """
        Retorna o valor da operação.
        """

class Deposito(Transacao):
    """
    Representa a operação de depósito.
    """
    def __init__(self, valor : float):
        super().__init__()
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta: Conta) -> bool:
        sucesso = conta.depositar(self._valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
            return True
        else:
            return False

class Saque(Transacao):
    """
    Representa a operação de saque.
    """
    def __init__(self, valor : float):
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor
    
    def registrar(self, conta: Conta) -> bool:
        sucesso = conta.sacar(self._valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
            return True
        else:
            return False


class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        pass

    def adicionar_conta(self, conta: Conta):
        self._contas.append(conta)
    
    def tem_conta(self):
        return len(self._contas) > 0
    
    @property
    def contas(self):
        return self._contas

class ContaCorrente(Conta):
    def __init__(self, cliente: Cliente, numero: int, limite: float, limite_saques: float):
        super().__init__(cliente, numero)
        self._limite = limite
        self._limite_saques = limite_saques
        self._qtd_saques = 0

    def sacar(self, valor: float):
        """
        Realiza um saque, se tiver saldo e limite suficientes.
        """
        if valor <= self._saldo + self._limite and self._qtd_saques < self._limite_saques:
            self._saldo -= valor
            self._qtd_saques += 1
            return True
        else:
            return False

    def depositar(self, valor: float):
        """
        Deposita novos valores se o limite de depósito não foi alcançado.
        """
        if valor > 0:
            return super().depositar(valor)
        else:
            return False


class PessoaFisica(Cliente):
    """
    Cliente Pessoa Física
    """
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def nome(self):
        """
        Retorna o nome do cliente.
        """
        return self._nome
    
    @property
    def cpf(self):
        """
        Retorna o CPF do cliente.
        """
        return self._cpf

    @property
    def data_nascimento(self):
        """
        Retorna a data de nascimento.
        """
        return self._data_nascimento

def limpar_terminal():
    """
    Limpa o terminal verificando qual sistema operacional está sendo utilizado.
    """
    if os.name == 'posix':  # Unix/Linux/MacOS
        os.system('clear')
    elif os.name == 'nt':  # Windows
        os.system('cls')

def exibir_extrato(conta):
    extrato = []
    for transaco in conta.historico.transacoes:
        extrato.append(f"Operação de {transaco.__class__.__name__} no valor de {transaco.valor}")

    extrato = "\n".join(extrato)

    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    #nome, dt_nascimento, cpf, endereco
    cpf = input("CPF do novo usuário (somente números): ")
    usuario = [usuario for usuario in usuarios if usuario.cpf == cpf]
    if usuario:
        print(f"\n@@@ Já existe usuário com esse CPF: {cpf} @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    usuarios.append(PessoaFisica(endereco=endereco, cpf=cpf, nome=nome, data_nascimento=data_nascimento))
    print("@@@ Usuário criado com sucesso! @@@")

def criar_conta(usuarios):
    cpf = input("Informe o CPF do usuário para o qual a conta será criada: ")
    usuario = [u for u in usuarios if u.cpf == cpf]
    if usuario:
        numero = len(usuario[0].contas) + 1
        limite = float(input("Limite da conta: "))
        novaconta = ContaCorrente(usuario[0], numero, limite, 2)
        usuario[0].adicionar_conta(novaconta)
        print("\n@@@ Conta criada com sucesso! @@@")
    else:
        print("\n@@@ Usuário não encontrado, fluxo de criação da conta encerrado! @@@")

def listar_contas(usuario):
    print(''.center(50, '*'))
    print('LISTA DE CONTAS ATIVAS'.center(50, '*'))
    print(''.center(50, '*'))
    if usuario.tem_conta():
        for conta in usuario.contas:
            print("NÚMERO: ", conta.numero)
            print("AGÊNCIA: ", conta.agencia)
            print("USUARIO: ", conta.cliente.nome, '(CPF: ', conta.cliente.cpf, ')')
            print("STATUS: ", 'ATIVA' if conta.ativa else 'INATIVA')
    else:
        print(f"O usuário identificado com o CPF {usuario.cpf} não tem contas")
    print(''.center(50, '*'))

def realizar_transacao(operacao, nome_operacao):
        cpf = input("CPF da Conta: ")
        usuario = [cliente for cliente in usuarios if cliente.cpf == cpf]
        if usuario:
            usuario = usuario[0]
            if usuario.tem_conta():
                num_conta = int(input("Informe o número da conta: "))
                contas = [conta for conta in usuario.contas if conta.numero == num_conta]
                if contas:
                    conta = contas[0]
                    valor = float(input(f"Informe o valor da operação de {nome_operacao}: "))
                    transacao = operacao(valor)
                    if not transacao.registrar(conta):
                       print("Não possível realizar esta transação! Entre em contato com o setor financeiro!")
                    else:
                        print("Operação realizada com sucesso!!!")
                else:
                    print(f"Conta {num_conta} não existe para o CPF {cpf}!")
            else:
                print(f"Nenhuma conta registrada no CPF {cpf}!")
        else:
            print(f"Usuário não encontrado: {cpf}")

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

while True:
    limpar_terminal()
    print("".center(50, '*'))
    print("BANCO BRAGESCO".center(50, '*'))
    print("".center(50, '*'))
    opcao = input(menu)
    if opcao == "d":
        realizar_transacao(Deposito, "depósito")
    elif opcao == "s":
        realizar_transacao(Saque, "saque")
    elif opcao == "e":
        cpf = input("CPF do usuário: ")
        usuarioscomcpf = [usuario for usuario in usuarios if usuario.cpf == cpf]
        if usuarioscomcpf and usuarioscomcpf[0].tem_conta():
            for conta in usuarioscomcpf[0].contas:
                exibir_extrato(conta)
        else:
            print("Não existe uma conta com o CPF informado ", cpf)
    elif opcao == "a":
        criar_usuario(usuarios)
    elif opcao == "c":
        criar_conta(usuarios)
    elif opcao == "l":
        if usuarios:
            for usuario in usuarios:
                if usuario.tem_conta():
                    listar_contas(usuario)
        else:
            print("NENHUM USUÁRIO CADASTRADO!")
    elif opcao == "q":
        break
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
    for i in range(5):
        print("\rProcessando", "."*i, end="")
        time.sleep(1)