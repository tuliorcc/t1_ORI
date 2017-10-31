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
            insere_registro()
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


# Cria um arquivo arqT1.dat contendo 100 registros aleatórios
def cria_arquivo():
    cls()
    with open('arqT1.dat', 'wb') as arquivo: # Cria/Abre o arquivo arqT1.dat em modo escrita binária

        for i in range(0, 100):            # 100 registros gerados aleatoriamente por gera_registro()
            reg = gera_registro()
            arquivo.write(bytes(reg))

    print("Arquivo arqT1.dat com 100 registros aleatórios criado. "
          "Qualquer arquivo arqT1.dat existente foi sobrescrito.")
    input("Pressione Enter para continuar")


# Insere um novo registro aleatório no arquivo arqT1.dat
def insere_registro():
    cls()
    print("### Inserir Registro ###")
    num = input("\n Informe o número de registros a serem inseridos ou -1 para retornar: ")
    if(num != '-1'):
        for i in range(0,int(num)):
            reg = gera_registro()                   # Gera um registro aleatório de 64 bytes
            print("\nRegistro aleatório gerado: ")
            chave = bytes(reg[0:4]).decode('utf-8') # chave recebe os primeiros 4 bytes gerados
            print("    Chave [{}]".format(chave))
            for i in range(0,6):
                campo = bytes(reg[4+(i*10):14+(i*10)]).decode('utf-8') # campo recebe os últimos 60 bytes gerados
                print("        Campo [{}]: {}".format(i, campo))

            # Abre o arquivo arqT1.dat em modo leitura binária e cria o arquivo temp.dat em modo escrita binária.
            # temp.dat será utilizado para copiar os registros atuais de arqT1.dat e inserir um novo
            with open('arqT1.dat', 'rb') as arq, open('temp.dat', 'wb') as temp:
                inserido = False        # Indica se o novo registro foi inserido
                fim_arquivo = False     # Indica se a leitura chegou ao final do arquivo
                num_bloco = 0           # Indica o número do bloco lido
                posicao = 0             # Indica a posição do registro relativa ao início do arquivo

                while (not fim_arquivo):

                    # Lê um bloco de 512 bytes (até 8 registros de 64 bytes) como uma string em utf-8
                    bloco_content = arq.read(512).decode('utf-8')
                    num_bloco += 1                      # Incrementa o número do bloco lido
                    ponteiro = 0                        # Ponteiro para varredura do bloco
                    if (len(bloco_content) < 512):      # Verifica se o bloco possui menos de 8 registros
                        fim_bloco = len(bloco_content)  # Indica o número de bytes ocupados no bloco
                        fim_arquivo = True
                    else:
                        fim_bloco = 512                 # Indica que o bloco está cheio, com 512 bytes

                    # Varre o bloco lido um registro por vez, copiando os registros para um arquivo temporário
                    # e inclui o registro novo no primeiro espaço vazio encontrado (pode ser no final)
                    while (ponteiro < fim_bloco):   # Enquanto o ponteiro não chegar ao fim do bloco
                        if (bloco_content[ponteiro] == '#' and inserido == False):  # Encontrou registro vazio e o novo não foi inserido ainda
                            inserido = True
                            temp.write(bytes(reg))  # Insere o novo registro no espaço encontrado
                            print("Registro inserido na posição {} do arquivo, referente ao bloco {}.".format(posicao, num_bloco))
                        else:           # Registro encontrado (vazio ou não) será copiado para o arquivo temporário                                   
                            temp.write(bytes(bloco_content[ponteiro:ponteiro+64].encode('utf-8')))  # Copia o registro existente
                        ponteiro += 64  # Pula 64 bytes até o próximo registro no bloco
                        posicao += 64
                if (not inserido):      # Insere o novo registro no final do arquivo caso nenhum registro vazio seja encontrado
                    temp.write(bytes(reg))
                    print("Registro inserido no final do arquivo.")

            # Abre o arquivo arqT1.dat em modo escrita binária e o arquivo temporário temp.dat em modo leitura binária.
            # O conteúdo de temp.dat será copiado para arqT1.dat e temp.dat será removido
            with open('arqT1.dat', 'wb') as arq, open('temp.dat', 'rb') as temp:
                fim_arquivo = False
                while (not fim_arquivo):    # Lê todos os blocos do arquivo, copiando-os
                    bloco = temp.read(512)
                    if (len(bloco) < 512):  # Um bloco incompleto (menos de 8 registros) indica o final do arquivo
                        fim_arquivo = True
                    arq.write(bloco)
            os.remove('temp.dat')           # Remove o arquivo temporário
        input("\nPressione Enter para continuar.")


# Busca um registro pela chave digitada e o imprime
def input_busca():
    cls()
    print("### Busca de registro ###\n")
    chave_b = input('Digite a chave a ser buscada (4 números): ')
    found = busca_registro(chave_b)
    if (found == -1):   # Registro não encontrado
        print("\nRegistro não encontrado.")
    else:               # Registro encontrado será imprimido
        imprime_registro(found)
    input("Pressione Enter para voltar ao menu principal.\n")


# Busca um registro pela chave e retorna sua posição no arquivo ou -1 se não o encontrar
def busca_registro(chave_b):
    with open('arqT1.dat', 'rb') as arquivo:    # Abre o arquivo arqT1.dat em modo leitura binária
        fim_arquivo = False                     # Indica se a leitura chegou ao final do arquivo
        num_bloco = 0                           # Indica o número do bloco lido
        posicao = 0                             # Indica a posição do registro relativa ao início do arquivo
        while(not fim_arquivo):
            ponteiro = 0                        # Ponteiro para varredura do bloco
            # Lê um bloco de 512 bytes (até 8 registros de 64 bytes) como uma string em utf-8
            bloco_content = arquivo.read(512).decode('utf-8')
            num_bloco += 1                      # Incrementa o número do bloco lido
            if (len(bloco_content) < 512):      # Verifica se bloco possui menos de 8 registros
                fim_bloco = len(bloco_content)  # Indica o número de bytes ocupados no bloco
                fim_arquivo = True              # Bloco incompleto encontrado indica final do arquivo
            else:
                fim_bloco = 512                 # Indica que o bloco está cheio, com 512 bytes

            while (ponteiro < fim_bloco):
                if(chave_b == bloco_content[ponteiro:ponteiro+4]):  # Verifica se é a chave buscada
                    print("Registro {} encontrado na posição {} do arquivo, referente ao bloco {}.".format(chave_b,posicao,num_bloco))
                    return posicao
                else:
                    ponteiro += 64 # Não é a chave buscada: Pula 64 bytes até o próximo registro no bloco
                    posicao += 64
        return -1                  # Registro não foi encontrado: Retorna -1


# Remove o primeiro registro encontrado com a chave buscada
def remove_registro():
    cls()
    print("### Remoção de registro ###")
    chave = input("Informe a chave do registro que deseja remover: ")
    pos = busca_registro(chave) # busca_registro retorna a posição ddo primeiro registro encontrado ou -1
    if (pos == -1):             # O registro com a chave informada não foi encontrado
        print("Registro não encontrado.")
    else:                       # O registro foi encontrado e será removido
        bloco = int(abs(pos/512))             # Indica o número do bloco onde o registro foi encontrado
        pos_bloco  = int(pos - (512*(bloco))) # Indica a posição do registro em seu bloco
        num_bloco = 0                         # Indica o bloco atual na varredura
        fim_arquivo = False                   # Indica se a leitura chegou ao final do arquivo

        # Abre o arquivo arqT1.dat em modo leitura binária e cria o arquivo temp.dat em modo escrita binária.
        # temp.dat será utilizado para copiar os registros atuais de arqT1.dat e remover o necessário
        with open('arqT1.dat', 'rb') as arq, open('temp.dat','wb') as temp:
            while (not fim_arquivo):
                # Lê um bloco de 512 bytes (até 8 registros de 64 bytes) como uma string em utf-8
                bloco_content = arq.read(512).decode('utf-8')
                if (len(bloco_content) < 512):  # Verifica se o bloco possui menos de 8 registros
                    fim_arquivo = True          # Bloco incompleto encontrado indica final do arquivo

                if (bloco == num_bloco):   # Se o bloco varrido for o mesmo do registro encontrado
                    lista = list(bloco_content)     # Lista os registros do bloco
                    lista[pos_bloco] = '#'          # Invalida o registro a remover na lista
                    bloco_content = ''.join(lista)  # Retorna a lista ao formato correto com o registro removido
                    temp.write(bloco_content.encode('utf-8')) # Copia o bloco alterado para o arquivo temporário
                else:
                    temp.write(bloco_content.encode('utf-8')) # Copia o bloco para o arquivo temporário normalmente
                num_bloco += 1

        # Abre o arquivo arqT1.dat em modo escrita binária e o arquivo temporário temp.dat em modo leitura binária.
        # O conteúdo de temp.dat será copiado para arqT1.dat e temp.dat será removido
        with open('arqT1.dat', 'wb') as arq, open('temp.dat', 'rb') as temp:
            fim_arquivo = False
            while (not fim_arquivo):    # Lê todos os blocos do arquivo, copiando-os
                bloco = temp.read(512)
                if (len(bloco) < 512):  # Um bloco incompleto (menos de 8 registros) indica o final do arquivo
                    fim_arquivo = True
                arq.write(bloco)
        os.remove('temp.dat')           # Remove o arquivo temporário
        input("Registro apagado. Pressione Enter para continuar.")


# Lista os registros do arquivo inteiro ou um bloco por vez
def lista_registros():
    cls()
    print("### Lista de registros ###\n")
    opt = input("(1) - Por bloco \n(2) - Arquivo completo \n(Outro) - Voltar ao menu \n  >")

    with open('arqT1.dat', 'rb') as arquivo:    # Abre o arquivo arqT1.dat em modo leitura binária
        num_bloco = 0           # Indica o número do bloco lido
        fim_arquivo = False     # Indica se a leitura chegou ao final do arquivo
        posicao = 0             # Indica a posição do registro relativa ao início do arquivo

        while (opt == '1' or opt == '2' and fim_arquivo == False): # **
            # Lê um bloco de 512 bytes (até 8 registros de 64 bytes) como uma string em utf-8
            bloco_content = arquivo.read(512).decode('utf-8')
            num_bloco += 1      # Incrementa o número do bloco lido
            print("> Bloco {}:".format(num_bloco)) # Imprime o número do bloco atual
            ponteiro = 0        # Ponteiro para varredura do bloco
            if (len(bloco_content) < 512):         # Verifica se o bloco possui menos de 8 registros
                fim_bloco = len(bloco_content)     # Indica o número de bytes ocupados no bloco
                fim_arquivo = True
            else:
                fim_bloco = 512                    # Indica que o bloco está cheio, com 512 bytes

            while (ponteiro < fim_bloco):          # Varre o bloco inteiro, um registro por vez
                if (bloco_content[ponteiro] == '#'):    # Registro inválido (vazio) encontrado
                    print("## Espaço vazio")
                else:                                   # Registro válido encontrado
                    imprime_registro(posicao)
                print("\n")
                ponteiro += 64  # Incrementa o ponteiro para varrer o próximo registro
                posicao += 64

            if (opt == '1'):   # Varredura de um bloco finalizado conforme opção 1
                next = input("(1) - Mostrar arquivo completo. (2) - Voltar ao menu. (Outro) - Próximo bloco\n")
                if (next == '1'):
                    opt = '2'  # Força mudança da opção anterior para 2, retornando ao while (indicado por **) para varrer o arquivo todo
                elif (next == '2'):
                    opt = '3'  # Força saída do while (indicado por **)

        input("\nPressione Enter para voltar ao menu principal.\n")


def compacta_arquivo():
    cls()
    print("### Manutenção do arquivo ###")
    print("\n ")

    # Abre o arquivo arqT1.dat em modo leitura  binária e o arquivo temporário temp.dat em modo escrita binária.
    # Os blocos de arqT1.dat serão varridos e os registros inválidos serão removidos do arquivo
    with open('arqT1.dat', 'rb') as arq, open('temp.dat', 'wb') as temp:
        num_bloco = 0           # Indica o número do bloco lido
        fim_arquivo = False     # Indica se a leitura chegou ao final do arquivo
        vazios = 0              # Indica o número de registros vazios encontrados

        while (not fim_arquivo):
            # Lê um bloco de 512 bytes (até 8 registros de 64 bytes) como uma string em utf-8
            bloco_content = arq.read(512).decode('utf-8')
            num_bloco += 1                      # Incrementa o número do bloco lido
            ponteiro = 0                        # Ponteiro para varredura do bloco
            bloco_escrita = []                  # Bloco de escrita vazio
            if (len(bloco_content) < 512):      # Verifica se bloco possui menos de 8 registros
                fim_bloco = len(bloco_content)  # Indica o número de bytes ocupados no bloco
                fim_arquivo = True              # Bloco incompleto encontrado indica final do arquivo
            else:
                fim_bloco = 512                 # Indica que o bloco está cheio, com 512 bytes

            while (ponteiro < fim_bloco):       # Varre o bloco inteiro, um registro por vez
                if (bloco_content[ponteiro] != '#'):   # Caso não esteja vazio, o registro será copiado para o bloco de escrita
                    bloco_escrita.append(bloco_content[ponteiro:ponteiro+64])
                else:
                    vazios += 1                        # Caso esteja vazio, o registro será ignorado e o contador de vazios incrementado
                ponteiro += 64                         # Incrementa o ponteiro para varrer o próximo registro
            bloco_escrita = ''.join(bloco_escrita)     # Une os registros do bloco de escrita no formato correto
            temp.write(bloco_escrita.encode('utf-8'))  # Escreve o bloco de escrita no arquivo temporário

    # Abre o arquivo arqT1.dat em modo escrita binária e o arquivo temporário temp.dat em modo leitura binária.
    # O conteúdo de temp.dat será copiado para arqT1.dat e temp.dat será removido
    with open('arqT1.dat', 'wb') as arq, open('temp.dat', 'rb') as temp:
        fim_arquivo = False
        while (not fim_arquivo):    # Lê todos os blocos do arquivo, copiando-os
            bloco = temp.read(512)
            if (len(bloco) < 512):  # Um bloco incompleto (menos de 8 registros) indica o final do arquivo
                fim_arquivo = True
            arq.write(bloco)
    os.remove('temp.dat')           # Remove o arquivo temporário

    print("\n Foram apagados {} registros inválidos. O tamanho do arquivo foi reduzido em {} bytes.".format(vazios, vazios*64))
    input("\nPressione Enter para continuar.")

## FUNÇÕES AUXILIARES ##
# Imprime o registro encontrado na posição pos relativa ao arquivo
def imprime_registro(pos):
    with open('arqT1.dat', 'rb') as arquivo:     # Abre o arquivo arqT1.dat em modo leitura binária
        arquivo.seek(pos)                        # Posiciona o ponteiro de leitura de acordo com o argumento pos
        chave = arquivo.read(4).decode('utf-8')  # Lê os primeiros 4 bytes do registro como sua chave
        print("Registro [{}] - ".format(chave))  # Imprime a chave lida
        for i in range(0, 6):                    # Lê e imprime os 6 campos de 10 bytes do registro
            campo = arquivo.read(10).decode('utf-8')
            print("   Campo [{}]: {}".format(i,campo))


# Gera um registro aleatório de 64 bytes
def gera_registro():
    reg = []
    for j in range(0, 4):
        reg.append(random.randrange(48, 58))  # Primeiros 04 bytes: Chave numérica
    for j in range(0, 60):
        reg.append(random.randrange(65, 90))  # Últimos 60 bytes: Conteúdo
    return reg


def cls():  # Limpa o console utilizando a função padrão do SO atual
    os.system('cls' if os.name == 'nt' else 'clear')


## PROGRAMA PRINCIPAL ##
# Inicia mostrando o menu principal
main_menu()
