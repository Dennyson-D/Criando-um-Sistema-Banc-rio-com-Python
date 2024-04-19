import textwrap

def depositar(saldo, valor, extrato, /): 
    
    if valor > 0:
            print(f'Valor de depósito R$ {valor:.2f}')
            saldo += valor 
            extrato += f'Depósito R$ {valor:.2f} \n'
    else:
            print('Valor inválido')
    return saldo,extrato        

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
        if numero_saques < limite_saques:    
                if valor > saldo:
                    print('Valor de saque é maior que o saldo')
                else:
                    print(f'Valor de saque R$ {valor:.2f}, saldo disponivel R$ {saldo-valor:.2f}')
                    numero_saques += 1 
                    saldo -= valor 
                    extrato += f'Valor sacado R$  {valor:.2f}\n'    
        else:
            print('Limite de 3 saques excedido') 
        return saldo,extrato,numero_saques       

def extrato(saldo, /,*, extrato):           
    print('---------Extrato---------\n')
    print('Não existem movimentos nesta conta') if not extrato else extrato
    print(extrato)
    print(f'\nSaldo R$ {saldo:.2f}')
    print('-------------------------')

def criar_usuario(usuarios):
    cpf = input('Digite CPF: ')
    usuario = filtro_usuarios(cpf,usuarios)

    if usuario:
         print('*** Usuário já existe ***')
         return

    nome =  input('Digite nome compelto: ')
    dt_nasc = input('Digite data de nascimento (dd-mm-aaaa): ')
    endereco = input('Digite endereço (logradouro, nro - bairro - cidade/sigla estado): ')
    
    usuarios.append({'cpf':cpf, 'nome':nome, 'data_nascimento':dt_nasc, 'endereco':endereco})

    print('!!! Usuário criado com sucesso !!!')


def filtro_usuarios(cpf,usuarios):
    usuario_fil = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuario_fil[0] if usuario_fil else None

def criar_conta(agencia,numero_conta,usuarios):
     cpf = input('Informe CPF:')
     usuario = filtro_usuarios(cpf,usuarios)

     if usuario:
          print('!!! Conta criada com sucesso !!!')
          return {'agencia':agencia,'numero_conta':numero_conta, 'usuario':usuario}
     
     print('@@@ Usuário não encontrado, deve ser criado um usuário antes! @@@')

def listar_contas(contas):
     for conta in contas:
         mostrar = f'''
            \n Agência: {['agencia']}
            \n C/C: {conta['numero_conta']}
            \n Titular: {conta['usuario']['nome']}      
         ''' 
         print('*' * 100)
         print(textwrap.dedent(mostrar))

def menu():
    menu =  '''
    ------------------MENU------------------

    Digite uma das opções abaixo:

    [0] - Depósito
    [1] - Saque
    [2] - Extrato
    [3] - Criar conta
    [4] - Listar contas
    [5] - Criar Usuário
    [6] - Sair

    ----------------------------------------
    '''
    return input(textwrap.dedent(menu))

def main():
    depositos = 0
    extrato = ''
    n_saques = 0
    LIMITE_SAQUE = 3
    LIMITE_VALOR_SAQUE = 500
    AGENCIA = '0001'
    saldo = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()
        if opcao == '0':
            valor = float(input('Digite valor do depósito:R$ ')) 
            saldo, extrato  = depositar(saldo,valor,extrato)

        elif  opcao == '1':          
            valor = float(input('Digite valor de saque R$ '))
            saldo,extrato,n_saques = sacar(saldo = saldo,
                                  valor = valor,
                                  extrato= extrato,
                                  limite = LIMITE_VALOR_SAQUE,
                                  numero_saques = n_saques,
                                  limite_saques = LIMITE_SAQUE
                                 )
              

        elif opcao == '2':
            extrato(saldo, extrato = extrato)

        elif opcao == '3':
             numero_conta = len(contas) + 1
             conta = criar_conta(AGENCIA,numero_conta,usuarios)    
             
             if conta:
                  contas.append(conta)
        elif opcao == '4':
             listar_contas(contas)    

        elif opcao == '5':
             criar_usuario(usuarios)    
        
        elif opcao == '6':
            break    
    else:
        print('Operação inválida')



main()