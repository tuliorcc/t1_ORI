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
        print("  6 - Compactar Arquivo")
        print("\n  0 - Sair\n")

        opcao = input("  > ")

        if (opcao == '1'):
            cria_arquivo()
        elif (opcao == '2'):
            insere_registro()
        elif (opcao == '3'):
            busca_registro()
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
            reg = []
            for j in range(0, 4):
                reg.append(random.randrange(48, 58))   #chave numérica
            for j in range(0, 60):
                reg.append(random.randrange(65, 90))  #conteúdo
            arquivo.write(bytes(reg))

    print("Arquivo arqT1.dat criado, qualquer arquivo existente foi sobrescrito. 100 registros aleatórios foram "
          "adicionados.")
    input("Pressione Enter para continuar")


def insere_registro():
    cls()
    # Insere Registro


def busca_registro():
    cls()
    # Busca Registro


def remove_registro():
    cls()
    # Remove Registro


# Lista os registros do arquivo
def lista_registros():
    cls()
    print("### Lista de registros do arquivo arqT1.dat ###\n")
    opt = input("(1) - Por bloco \n(2) - Arquivo completo \n(Outro) - Voltar ao menu \n  >")

    with open('arqT1.dat', 'rb') as arquivo:
        num_bloco = 0

        while (opt == '1' or opt == '2'):
            bloco_content = arquivo.read(512).decode('utf-8')  # Lê 1 bloco como uma string
            num_bloco += 1
            print("> Bloco {}:".format(num_bloco))
            ponteiro = 0  # ponteiro que varre o bloco

            while (ponteiro < 512):  # varre os 6 registros do bloco

                if (bloco_content[ponteiro] == '#'):    # registro vazio
                    print("## Espaço vazio")
                else:                                   # registro válido
                    chave = bloco_content[ponteiro:ponteiro+4]
                    print("Registro [{}] - ".format(chave))     # Imprime chave
                    for i in range(0, 6):                       # imprime os 6 campos
                        inicio_campo = (ponteiro+4)+(i*10)
                        conteudo_campo = bloco_content[inicio_campo:inicio_campo+10]
                        print("   Campo [{}]: {}".format(i+1, conteudo_campo))
                print("\n")

                ponteiro += 64  #próximo registro no bloco


            if (opt == '1'):   # fim do bloco
                next = input("(1) - Mostrar arquivo completo. (2) - Voltar ao menu. (Outro) - Próximo\n")
                if (next == '1'):
                    opt = '2'  # volta pro while, mas imprime arquivo inteiro
                elif (next == '2'):
                    opt = '3'  # sai do while, volta ao menu


def compacta_arquivo():
    cls()
    # Compacta Arquivo


def cls():  # Função que limpa o console
    os.system('cls' if os.name == 'nt' else 'clear')

# PROGRAMA PRINCIPAL
main_menu()
