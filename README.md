# t1_ORI
Trabalho 1 da disciplina Organização e Recuperação da Informação, do Prof. Jander.

#### **Grupo:**
    - Leonardo Henrique Tozzatto Volpe
    - Miguel Gonçalves Vieira
    - Túlio Ribeiro Cesar de Campos


### Estrutura do arquivo:

**Nome:** arqT1.dat

Registros de 64 bytes
Blocos de 512 bytes (8 registros)

**Estrutura dos registros:**
4 bytes - Chave (numérica, aleatória)
60 bytes - Conteúdo (letras aleatórias)
         - 6 campos de 10 bytes

Registros inválidos se iniciam com o caracter #

## Funções:

### cria_arquivo()
Cria um novo arquivo arqT1.dat, sobrescrevendo caso já exista. O novo arquivo possui 100 registros gerados aleatoriamente.  
  
### lista_registros()
Lista os registros do arquivo. Existem as opções de listagem por bloco ou por arquivo completo.  
Abre o arquivo e lê um bloco por vez, salvando o bloco em uma string de caracteres.  
Imprime os oito registros do bloco (chave e campos)  
No caso da listagem por bloco, para a execução no fim de cada bloco, perguntando ao usuário se quer imprimir o próximo bloco, o arquivo inteiro ou voltar ao menu.



## To Do:

Implementar:
- [x] Criação de novo arquivo
- [ ] Inserir novo registro
- [ ] Buscar registro, dada uma chave
- [ ] Remoção de um registro, dada uma chave
- [x] Listagem de registros
- [ ] Compactação do arquivo