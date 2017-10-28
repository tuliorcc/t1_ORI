import os
import random

def main_menu():
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
        arquivo_vazio()


# Cria um arquivo vazio com 100 registros
def arquivo_vazio():
    cls()
    with open('arqT1.dat', 'wb') as arquivo:

        for i in range(0, 101):     # 100 registros
            reg = []
            for j in range(0, 4):
                reg.append(random.randrange(48, 58))   #chave numérica
            for j in range(0, 60):
                reg.append(random.randrange(65, 90))  #conteúdo
            arquivo.write(bytes(reg))


def cls():  # Função que limpa o console
    os.system('cls' if os.name == 'nt' else 'clear')

# PROGRAMA PRINCIPAL
while(True):
    main_menu()
