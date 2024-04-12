depositos = 0
saques = 0
LIMITE_SAQUE = 3
LIMITE_VALOR_SAQUE = 500
extrato = ''''''
saldo = 0


menu =  '''
    ------------------MENU------------------

    Digite uma das opções abaixo:

    [0] - Depósito
    [1] - Saque
    [2] - Extrato
    [3] - Sair

    ----------------------------------------
    '''

while True:
    opcao = input(menu)
    if opcao == '0':
        deposito = float(input('Digite valor do depósito:R$ '))
        
        if (deposito) > 0:
            print(f'Valor de depósito R$ {deposito:.2f}')
            saldo += deposito 
            extrato += f'Depósito = R$ {deposito:.2f} \n'
        else:
            print('Valor inválido')

    elif  opcao == '1':
        if saques < LIMITE_SAQUE:
            saque = float(input('Digite valor de saque R$ '))
            if saque > saldo:
                print('Valor de saque é maior que o saldo')
            else:
                print(f'Valor de saque R$ {saque:.2f}, saldo disponivel R$ {saldo-saque:.2f}')
                saques += 1 
                saldo -= saque 
                extrato += f'Valor sacado R$ {saque:.2f}\n'    
        else:
            print('Limite de 3 saques excedido')  
            continue   

    elif opcao == '2':
          print('---------Extrato---------\n')
          print('Não existem movimentos nesta conta') if not extrato else extrato
          print(extrato)
          print(f'\nSaldo R$ {saldo:.2f}')
          print('-------------------------')
    elif opcao == '3':
        break    
    else:
        print('Operação inválida')