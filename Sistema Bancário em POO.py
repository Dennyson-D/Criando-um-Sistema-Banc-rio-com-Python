from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
import textwrap

   
class Cliente: 
    def __init__(self,endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self,conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self,conta):
         self.contas.append(conta)

class Pessoa_fisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
          
class Conta:
    def __init__(self,numero,cliente):
          self._saldo = 0
          self._numero = numero
          self._agencia = '0001'
          self._cliente = cliente
          self._historico = Historico()

    @classmethod
    def nova_conta(cls,cliente,numero):
         return cls(numero,cliente)

    @property
    def saldo(self):
          return self._saldo
    
    @property
    def numero(self):
         return self._numero
    
    @property
    def agencia(self):
         return self._agencia

    @property
    def cliente(self):
         return self._cliente
    
    @property
    def historico(self):
         return self._historico
    
    def sacar(self,valor):
        saldo = self.saldo 

        if valor > saldo:
            print(' @Operação falhou: Saldo insuficiente!')
        
        elif valor > 0:
            print(f'Valor de saque R$ {valor:.2f}, saldo disponivel R$ {saldo-valor:.2f}')
            self._saldo -= valor 
            #extrato += f'Valor sacado R$  {valor:.2f}\n'  
            return True
        
        else:
             print('@Operação falhou: Valor inválido!')
        return False
        
    def depositar(self,valor):
        if valor > 0:
            print(f'Valor de depósito R$ {valor:.2f}')
            self._saldo += valor 

        else:
            print('@Operação falhou: Valor inválido') 
            return False
        
        return True

class ContaCorrente(Conta):
    def __init__(self, numero,cliente, limite = 500, limite_saques = 3):
          super().__init__(numero, cliente)
          self._limite = limite
          self._limite_saques = limite_saques

    def sacar(self,valor):
        num_saques = len([transacao for transacao in self.historico.transacoes 
                      if transacao['tipo'] == Saque.__name__])
         
        if valor > self._limite:
            print('@Operação falhou: valor do saque excedeu limite!')

        elif num_saques >= self._limite_saques:
             print('@Operação falhou: Número de saques excedido!')  

        else:
             return super().sacar(valor)

        return False    

    def __str__(self):
         return f"""
            \n Agência: {self.agencia}
            \n C/C: {self.numero}
            \n Titular: {self.cliente.nome}   
         """  
class Historico:
    def __init__(self):
          self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes      

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            } 
        )

class Transacao(ABC):

     @property
     @abstractproperty
     def valor(self):
          pass
     
     @abstractclassmethod
     def registrar(self,conta):
          pass
     
class Saque(Transacao):
    def __init__(self,valor):
          self._valor = valor
    
    @property
    def valor(self):
         return self._valor
    
    def registrar(self,conta):
         sucesso_transacao = conta.sacar(self.valor)

         if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self,valor):
          self._valor = valor

    @property
    def valor(self):
         return self._valor     

    def registrar(self, conta):
         sucesso_transacao = conta.depositar(self.valor)

         if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


'''
--------------------------------------------------------------------------------------------------------
Acima = classes / Abaixo funções
--------------------------------------------------------------------------------------------------------                       
'''

def criar_cliente(clientes):
    cpf = input('Digite CPF: ')
    cliente = filtrar_cliente(cpf,clientes)

    if cliente:
         print('@ Usuário já existe!')
         return

    nome =  input("Digite nome completo: ")
    data_nascimento = input("Digite data de nascimento (dd-mm-aaaa): ")
    endereco = input("Digite endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    
    cliente = Pessoa_fisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print('!!! Cliente criado com sucesso !!!')


# def filtro_usuarios(cpf,usuarios):
#     usuario_fil = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
#     return usuario_fil[0] if usuario_fil else None

def criar_conta(num_conta,clientes, contas):
     cpf = input('Informe CPF:')
     cliente = filtrar_cliente(cpf, clientes)

     if not cliente:
          print('@@@ Usuário não encontrado, deve ser criado um usuário antes! @@@')
          return

     conta = ContaCorrente.nova_conta(cliente=cliente, numero=num_conta)
     contas.append(conta)
     cliente.contas.append(conta)
     print('!!! Conta criada com sucesso !!!')    
            

def listar_contas(contas):
     if len(contas) > 0:
          for conta in contas:       
               print('*' * 100)
               print(textwrap.dedent(str(conta)))
     else:
        print('@ Não existem contas cadastradas!')            

def filtrar_cliente(cpf, clientes):
     clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf ]         
     return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
     if not cliente.contas:
          print("@@ Cliente não possui conta! @@")
          return
     
     return cliente.contas[0]

def depositar(clientes):
     cpf = input('Informe o cpf: ')
     cliente = filtrar_cliente(cpf, clientes)

     if not cliente:
          print(f'@@ Cliente não encontrado! @@')         
          return
     
     valor = float(input('Digite o valor de deposito: '))
     transacao = Deposito(valor)

     conta = recuperar_conta_cliente(cliente)
     if not conta:
          return
     
     cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
     cpf = input('Informe CPF: ')
     cliente = filtrar_cliente(cpf,clientes)  

     if not cliente:
          print('@ Cliente não encontrado!')
          return
     
     valor = float(input('Digite o valor do saque: '))
     transacao = Saque(valor)      

     conta = recuperar_conta_cliente(cliente)
     if not conta:
          return  
     
     cliente.realizar_transacao(conta, transacao)

def mostrar_extrato(clientes):
     cpf = input('Digite CPF: ')
     cliente = filtrar_cliente(cpf,clientes)

     if not cliente:
          print('@ CLiente não encontrado!')
          return

     conta = recuperar_conta_cliente(cliente)
     if not conta:
          return

     print('**************** EXTRATO ****************')
     transacoes = conta.historico.transacoes

     extrato = ""
     if not transacoes:
          extrato  = '@ Não existe histórico nessa conta'
     else:
          for transacao in transacoes:
               extrato += f" {transacao['tipo']}:\n R$ {transacao['valor']:.2f}"

     print(extrato)
     print(f'Saldo: R$ {conta.saldo:.2f}')
     print('*****************************************')                


def menu():
    menu =  '''
    ------------------MENU------------------

    Digite uma das opções abaixo:

    [0] - Depósito
    [1] - Saque
    [2] - Extrato
    [3] - Criar conta
    [4] - Listar contas
    [5] - Criar Cliente
    [6] - Sair

    ----------------------------------------
    '''
    return input(textwrap.dedent(menu))


def main():
    contas = []
    clientes = []

    while True:
        opcao = menu()
        if opcao == '0':
            depositar(clientes)

        elif  opcao == '1':          
            sacar(clientes)

        elif opcao == '2':
            mostrar_extrato(clientes)

        elif opcao == '3':
             numero_conta = len(contas)+1
             criar_conta(numero_conta, clientes, contas)

        elif opcao == '4':
             listar_contas(contas)    

        elif opcao == '5':
             criar_cliente(clientes)    
        
        elif opcao == '6':
            break    
    else:
        print('@@ Operação inválida @@')

main()