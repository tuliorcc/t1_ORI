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
        print("\n  0 - Sair\n\n")

        opcao = input("> ")

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

    print("Arquivo arqT1.dat criado, qualquer arquivo existente foi sobrescrito. 100 registros aleatórios foram adicionados.")
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

def lista_registros():
    cls()
    # Lista Registros

def compacta_arquivo():
    cls()
    # Compacta Arquivo


def cls():  # Função que limpa o console
    os.system('cls' if os.name == 'nt' else 'clear')

# PROGRAMA PRINCIPAL
    main_menu()
