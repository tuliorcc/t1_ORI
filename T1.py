import os
import random


def main_menu():
    while (True):
        cls()
        print("MENU PRINCIPAL")
        print("  1 - Criar arquivo vazio")
        print("  2 - Inserir Registro")
        print("  3 - Buscar Registro")
        print("  4 - Remover Registro")
        print("  5 - Listar Registros")
        print("  6 - Manutenção do Arquivo")
        print("\n  0 - Sair\n")

        opcao = input("  > ")

        if (opcao == '1'):
            cria_arquivo()
        elif (opcao == '2'):
            insercao()
        elif (opcao == '3'):
            input_busca()
        elif (opcao == '4'):
            remove_registro()
        elif (opcao == '5'):
            lista_registros()
        elif (opcao == '6'):
            compacta_arquivo()
        elif (opcao == '0'):
            break
        else:
            input("\nOpção inválida. Pressione Enter para continuar.")


# Cria um arquivo vazio com 100 registros
def cria_arquivo():
    cls()
    with open('arqT1.dat', 'wb') as arquivo:

        for i in range(0, 101):     # 100 registros
            reg = gera_registro()
            arquivo.write(bytes(reg))

    print("Arquivo arqT1.dat criado, qualquer arquivo existente foi sobrescrito. 100 registros aleatórios foram "
          "adicionados.")
    input("Pressione Enter para continuar")


def insercao():
    opt = 0
    while (opt != '1' and opt != '2'):
        cls()
        print("### Inserção de Registros ###")
        print("\n(1) - Inserir 1 registro \n(2) - Inserção em lote \n\n   > ")
        opt = input()
    if (opt == '1'):
        insere_registro()
    else:
        num = input("\n Informe o número de registros a serem inseridos: ")
        for i in range(0,int(num)):
            insere_registro()



# Insere novo registro
def insere_registro():
    cls()
    print("### Inserir Registro ###")
    reg = gera_registro()
    print("\nRegistro aleatório gerado: ")      # gera registro aleatório reg a ser adicionado
    chave = bytes(reg[0:4]).decode('utf-8')
    print("    Chave [{}]".format(chave))
    for i in range(0,6):
        campo = bytes(reg[4+(i*10):14+(i*10)]).decode('utf-8')
        print("        Campo [{}]: {}".format(i, campo))

    with open('arqT1.dat', 'rb') as arq, open('temp.dat', 'wb') as temp:
        inserido = False
        num_bloco = 0
        fim_arquivo = False
        posicao = 0

        while (not fim_arquivo):

            # Lê bloco
            bloco_content = arq.read(512).decode('utf-8')  # Lê 1 bloco como uma string
            num_bloco += 1
            ponteiro = 0  # ponteiro que varre o bloco
            if (len(bloco_content) < 512):      # verifica se bloco tem menos de 8 registros
                fim_bloco = len(bloco_content)
                fim_arquivo = True
            else:
                fim_bloco = 512

            # Varre bloco
            while (ponteiro < fim_bloco):  # varre os 6 registros do bloco
                if (bloco_content[ponteiro] == '#' and inserido == False):  # registro vazio e ainda nao foi inserido o novo
                    inserido = True
                    temp.write(bytes(reg))  # insere o registro
                    print("Registro inserido na posição {} do arquivo.".format(posicao))
                else:                                   # registro ocupado
                    temp.write(bytes(bloco_content[ponteiro:ponteiro+64].encode('utf-8')))  # copia o registro existente
                ponteiro += 64  # próximo registro no bloco
                posicao += 64
        if (not inserido):
            temp.write(bytes(reg))  # insere no fim do arquivo se nao foi inserido até agora
            print("Registro inserido no fim do arquivo.")

    # Copia temp para arq
    with open('arqT1.dat', 'wb') as arq, open('temp.dat', 'rb') as temp:
        fim_arquivo = False         # copia temp para arq
        while (not fim_arquivo):
            bloco = temp.read(512)
            if (len(bloco) < 512):
                fim_arquivo = True
            arq.write(bloco)


# Busca um registro
def input_busca():
    cls()
    print("### Busca de registro ###\n")
    chave_b = input('Digite a chave a ser buscada (4 números): ')
    found = busca_registro(chave_b)
    if (found == -1):
        print("\nRegistro não encontrado.")
    else:
        imprime_registro(found)
    input("Pressione Enter para voltar ao menu principal.\n")


# Busca o registro e retorna sua posição no arquivo
def busca_registro(chave_b):

    with open('arqT1.dat', 'rb') as arquivo:
        fim_arquivo = False

        posicao = 0
        while(not fim_arquivo):
            ponteiro = 0
            bloco_content = arquivo.read(512).decode('utf-8')  # Lê 1 bloco como uma string
            if (len(bloco_content) < 512):      # verifica se bloco tem menos de 8 registros
                fim_bloco = len(bloco_content)
                fim_arquivo = True
            else:
                fim_bloco = 512

            while (ponteiro < fim_bloco):
                if(chave_b == bloco_content[ponteiro:ponteiro+4]):  # verifica se chave é a chave buscada
                    print("Registro {} encontrado (offset = {}).".format(chave_b,posicao))
                    return posicao
                else:
                    ponteiro += 64 # se não encontrar, vai para o próximo registro
                    posicao += 64
        return -1  # retorna -1 caso não encontrado


# Remove o primeiro registro encontrado com a chave buscada.
def remove_registro():
    cls()
    print("### Remoção de registro ###")
    chave = input("Informe a chave do registro que deseja remover: ")
    pos = busca_registro(chave)
    if (pos == -1):
        print("Registro não encontrado.")
    else:
        bloco = int(abs(pos/512))
        pos_bloco  = int(pos - (512*(bloco)))
        num_bloco = 0
        fim_arquivo = False

        with open('arqT1.dat', 'rb') as arq, open('temp.dat','wb') as temp:
            while (not fim_arquivo):
                bloco_content = arq.read(512).decode('utf-8')  # lê o bloco como string
                if (len(bloco_content) < 512):
                    fim_arquivo = True

                if (bloco == num_bloco):   # se o registro está no bloco
                    lista = list(bloco_content)
                    lista[pos_bloco] = '#'          # invalida o registro na lista
                    bloco_content = ''.join(lista)      # transforma de volta
                    temp.write(bloco_content.encode('utf-8'))
                else:
                    temp.write(bloco_content.encode('utf-8'))  # senão só escreve o bloco
                num_bloco += 1

        with open('arqT1.dat', 'wb') as arq, open('temp.dat', 'rb') as temp:
            fim_arquivo = False         # copia temp para arq
            while (not fim_arquivo):
                bloco = temp.read(512)
                if (len(bloco) < 512):
                    fim_arquivo = True
                arq.write(bloco)
        input("Registro apagado. Pressione Enter para continuar.")


# Lista os registros do arquivo
def lista_registros():
    cls()
    print("### Lista de registros ###\n")
    opt = input("(1) - Por bloco \n(2) - Arquivo completo \n(Outro) - Voltar ao menu \n  >")

    with open('arqT1.dat', 'rb') as arquivo:
        num_bloco = 0
        fim_arquivo = False
        posicao = 0

        while (opt == '1' or opt == '2' and fim_arquivo == False):
            bloco_content = arquivo.read(512).decode('utf-8')  # Lê 1 bloco como uma string
            num_bloco += 1
            print("> Bloco {}:".format(num_bloco))
            ponteiro = 0  # ponteiro que varre o bloco
            if (len(bloco_content) < 512):      # verifica se bloco tem menos de 8 registros
                fim_bloco = len(bloco_content)
                fim_arquivo = True
            else:
                fim_bloco = 512

            while (ponteiro < fim_bloco):  # varre os 6 registros do bloco
                if (bloco_content[ponteiro] == '#'):    # registro vazio
                    print("## Espaço vazio")
                else:                                   # registro válido
                    imprime_registro(posicao)
                print("\n")
                ponteiro += 64  # próximo registro no bloco
                posicao += 64

            if (opt == '1'):   # fim do bloco
                next = input("(1) - Mostrar arquivo completo. (2) - Voltar ao menu. (Outro) - Próximo\n")
                if (next == '1'):
                    opt = '2'  # volta pro while, mas imprime arquivo inteiro
                elif (next == '2'):
                    opt = '3'  # sai do while, volta ao menu

        input("\nPressione Enter para voltar ao menu principal.\n")


def compacta_arquivo():
    cls()
    # Compacta Arquivo


# FUNÇÕES AUXILIARES
def imprime_registro(pos):
    with open('arqT1.dat', 'rb') as arquivo:
        arquivo.seek(pos)      #seta ponteiro na posicao recebida
        chave = arquivo.read(4).decode('utf-8')
        print("Registro [{}] - ".format(chave))  # Imprime chave
        for i in range(0, 6):  # imprime os 6 campos
            campo = arquivo.read(10).decode('utf-8')
            print("   Campo [{}]: {}".format(i,campo))


# Gera um registro aleatório
def gera_registro():
    reg = []
    for j in range(0, 4):
        reg.append(random.randrange(48, 58))  # chave numérica
    for j in range(0, 60):
        reg.append(random.randrange(65, 90))  # conteúdo
    return reg


def cls():  # Função que limpa o console
    os.system('cls' if os.name == 'nt' else 'clear')


# PROGRAMA PRINCIPAL
main_menu()
