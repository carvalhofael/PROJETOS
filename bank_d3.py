from typing import List
from abc import ABC, abstractmethod
from datetime import date

class Historico:
    def __init__(self) -> None:
        self.historico: List[str] = []

    def adicionar_transacao(self, descricao: str) -> None:
        self.historico.append(descricao)

class Cliente:
    def __init__(self, nome: str, endereco: str) -> None:
        self.nome = nome
        self.endereco = endereco
        self.contas: List['Conta'] = []

    def adicionar_conta(self, conta: 'Conta') -> None:
        self.contas.append(conta)

    def realizar_transacao(self, conta: 'Conta', transacao: 'Transacao') -> None:
        transacao.registrar(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome: str, endereco: str, cpf: str, data_nascimento: date) -> None:
        super().__init__(nome, endereco)
        self.cpf = cpf
        self.data_nascimento = data_nascimento

class Conta(ABC):
    def __init__(self, cliente: Cliente, numero: int, limite: float = 0.0) -> None:
        self.saldo: float = 0.0
        self.numero: int = numero
        self.cliente: Cliente = cliente
        self.limite: float = limite
        self.historico = Historico()
        cliente.adicionar_conta(self)

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self.saldo += valor
            self.historico.adicionar_transacao(f"Depósito de R$ {valor:.2f}")
            return True
        return False

    def sacar(self, valor: float) -> bool:
        if 0 < valor <= self.saldo + self.limite:
            self.saldo -= valor
            self.historico.adicionar_transacao(f"Saque de R$ {valor:.2f}")
            return True
        return False

class ContaCorrente(Conta):
    def __init__(self, cliente: Cliente, numero: int, limite: float = 0.0, limite_saque: float = 500.0) -> None:
        super().__init__(cliente, numero, limite)
        self.limite_saque = limite_saque

    def sacar(self, valor: float) -> bool:
        if valor > self.limite_saque:
            return False
        return super().sacar(valor)

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta: Conta) -> None:
        pass

class Deposito(Transacao):
    def __init__(self, valor: float) -> None:
        self.valor = valor

    def registrar(self, conta: Conta) -> None:
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(f"Depósito de R$ {self.valor:.2f}")

class Saque(Transacao):
    def __init__(self, valor: float) -> None:
        self.valor = valor

    def registrar(self, conta: Conta) -> None:
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(f"Saque de R$ {self.valor:.2f}")

def mostrar_menu():
    menu = """
==========================================
|         BANCO PYTHON - MENU            |
==========================================
| [1] Depositar                          |
| [2] Sacar                              |
| [3] Extrato                            |
| [4] Criar usuário                      |
| [5] Criar conta corrente               |
| [6] Listar contas                      |
| [7] Listar usuários                    |
| [0] Sair                               |
==========================================

=> """
    return menu

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("Depósito realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques
    saques_restantes = limite_saques - numero_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
        print(f"Saques restantes: 0")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        saques_restantes = limite_saques - numero_saques
        print(f"Saque realizado com sucesso! Saques restantes: {saques_restantes}")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato, numero_saques

def visualizar_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ").strip()
    cpf = ''.join(filter(str.isdigit, cpf))
    usuario = next((u for u in usuarios if u["cpf"] == cpf), None)
    if usuario:
        print("Já existe usuário com esse CPF!")
        return
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro, bairro, cidade/UF): ")
    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })
    print("Usuário cadastrado com sucesso!")

def criar_conta_corrente(usuarios, contas):
    cpf = input("Informe o CPF do usuário: ").strip()
    cpf = ''.join(filter(str.isdigit, cpf))
    usuario = next((u for u in usuarios if u["cpf"] == cpf), None)
    if not usuario:
        print("Usuário não encontrado!.")
        return
    numero_conta = len(contas) + 1
    conta = {
        "agencia": "0001",
        "numero_conta": numero_conta,
        "usuario": usuario
    }
    contas.append(conta)
    print(f"Conta criada com sucesso! Agência: {conta['agencia']} Número da conta: {conta['numero_conta']}")

def listar_contas(contas):
    print("\n====== CONTAS CADASTRADAS ======")
    if not contas:
        print("Nenhuma conta cadastrada.")
    for conta in contas:
        print(f"Agência: {conta['agencia']} | Conta: {conta['numero_conta']} | Titular: {conta['usuario']['nome']} (CPF: {conta['usuario']['cpf']})")
    print("================================")

def listar_usuarios(usuarios):
    print("\n====== USUÁRIOS CADASTRADOS ======")
    if not usuarios:
        print("Nenhum usuário cadastrado.")
    for usuario in usuarios:
        print(f"Nome: {usuario['nome']}")
        print(f"CPF: {usuario['cpf']}")
        print(f"Data de nascimento: {usuario['data_nascimento']}")
        print(f"Endereço: {usuario['endereco']}")
        print("----------------------------------")
    print("==================================")

def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    usuarios = []
    contas = []

    while True:
        opcao = input(mostrar_menu())

        if opcao == "1":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)
        elif opcao == "2":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )
        elif opcao == "3":
            visualizar_extrato(saldo, extrato=extrato)
        elif opcao == "4":
            criar_usuario(usuarios)
        elif opcao == "5":
            criar_conta_corrente(usuarios, contas)
        elif opcao == "6":
            listar_contas(contas)
        elif opcao == "7":
            listar_usuarios(usuarios)
        elif opcao == "0":
            break
        else:
            print("Operação inválida, por favor selecione novamente número da operação desejada.")

if __name__ == "__main__":
    cliente = PessoaFisica("João da Silva", "Rua A, 123, Centro, Cidade/UF", "12345678900", date(1990, 1, 1))
    conta = ContaCorrente(cliente, numero=1, limite=1000.0, limite_saque=500.0)
    cliente.realizar_transacao(conta, Deposito(200.0))
    cliente.realizar_transacao(conta, Saque(100.0))
    print(conta.historico.historico)
    main()