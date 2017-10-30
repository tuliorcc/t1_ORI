# t1_ORI
Trabalho 1 da disciplina Organização e Recuperação da Informação, do Prof. Jander.

#### **Grupo:**
    - Leonardo Henrique Tozzatto Volpe
    - Miguel Gonçalves Vieira
    - Túlio Ribeiro Cesar de Campos


## Estrutura do arquivo:

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
  
### insere_registro()
Gera um registro aleatório com gera_registro(). Em seguida, lê o arquivo bloco por bloco, procurando
um espaço vazio, enquanto copia o arquivo para um arquivo temporário.   
Caso um espaço seja encontrado,o registro é escrito no lugar do espaço vazio. 
Caso contrário, é escrito no fim do arquivo.  
No fim, o arquivo temporário é copiado para o arquivo principal.  
  
### input_busca() e busca_registros(chave) 
input_busca() pede a chave a ser buscada pelo usuário e passa para busca_registros(chave).
Abre o arquivo e lê um bloco por vez, salvando o bloco em uma string.  
Varre o arquivo (bloco por bloco) procurando a chave.  
Caso encontrada, retorna a posição do registro no arquivo. Caso contrário, retorna -1.
  
### remove_registro()
Pergunta a chave do registro a ser removido e a busca no arquivo.
Se encontrado, calcula em que bloco o registro se encontra.  
Cria um arquivo novo (temp.dat) vazio e copia bloco por bloco do arquivo original neste arquivo.
Quando chega no bloco em que o registro a ser removido se encontra, troca o primeiro caracter do registro
por um #. Então, ele copia o resto dos blocos para o arquivo temp.
Reescreve o arquivo original com o conteúdo de temp. 
  
### lista_registros()
Lista os registros do arquivo. Existem as opções de listagem por bloco ou por arquivo completo.  
Abre o arquivo e lê um bloco por vez, salvando o bloco em uma string de caracteres.  
Imprime os oito registros do bloco (chave e campos)  
No caso da listagem por bloco, para a execução no fim de cada bloco, perguntando ao usuário se quer imprimir o próximo bloco, o arquivo inteiro ou voltar ao menu.

### imprime_registro(pos)
Recebe a posição do registro no arquivo e imprime sua chave e campos formatados.

### gera_registro
Gera um registro aleatório e retorna uma lista com os caracteres.


*Obs.: Para a inserção e remoção de registros, um arquivo temporário auxiliar foi usado. A solução
não é ótima em termos de uso de memória e tempo, mas foi a solução encontrada, visto que o python não
consegue alterar bytes no meio do arquivo.*  
*Seria melhor renomear o arquivo temporário ao invés de copiá-lo para o arquivo principal, mas resolvemos
manter esta solução para não ser necessário o uso de bibliotecas extras.*


## To Do:

Implementar:
- [x] Criação de novo arquivo
- [ ] Inserir novo registro
- [x] Buscar registro, dada uma chave
- [x] Remoção de um registro, dada uma chave
- [x] Listagem de registros
- [ ] Compactação do arquivo