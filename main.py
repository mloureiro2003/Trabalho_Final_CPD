"""
Importa os modulos e classes necessarios para o funcionamento do programa:

- `defaultdict` da biblioteca `collections`: Utilizado para criar dicionarios 
com valores padrao, facilitando a manipulacao de dados.
- `csv`: Módulo utilizado para manipulação de arquivos CSV, facilitando a 
leitura e escrita de dados no formato CSV.
- Tipos `Tuple`, `Union`, `Dict` do módulo `typing`: Usados para a documentacao
de tipos nas funcoes, facilitando a compreensao do codigo.
- Estruturas de dados `Monster`, `Monster_Name`, `Monster_Attribute` do arquivo 
`monsters.py`: Utilizadas para armazenar informacoes relacionadas aos monstros, 
como nome, atributos e outras caracteristicas.
- Estruturas de dados `TrieNode`, `Trie`, `BSTNode`, `BST` do arquivo `trees.py`: 
Utilizadas para criacao de arvores de busca e estrutura de dados para atributos 
dos monstros, como índice e tipos.
"""
from collections import defaultdict
import csv
from typing import Tuple, Union, Dict
from monsters import Monster, Monster_Name, Monster_Attribute
from trees import TrieNode, Trie, BSTNode, BST

def menu() -> int:
    """
    Exibe as opcoes de funcionalidades do programa e retorna a escolha do usuario.

    Exibe um menu com as seguintes opções:
    1. Carregar o arquivo "Monsters_D&D5e.csv" novamente.
    2. Inserir um novo monstro.
    3. Fazer uma pesquisa.
    4. Sair do programa.

    Valida a entrada do usuario para garantir que a escolha seja válida.

    Returns:
        int: A opção escolhida pelo usuario (1, 2, 3 ou 4).
    """
    print('1 - Carregar "Monsters_D&D5e.csv" novamente')
    print('2 - Inserir novo monstro')
    print('3 - Fazer pesquisa')
    print('4 - Sair')
    ans = (int(input('Favor escolha uma das alternativas: ')))
    # loop de validacao
    while ans not in [1, 2, 3, 4]:
        ans = int(input('Entrada inválida. Favor escolha um número válido: '))
    return ans

def open_file(file_name: str) -> list[Monster]:
    """
    Le um arquivo .csv e converte cada linha em um objeto do tipo `Monster`.

    Esta funçaoo abre o arquivo especificado, extrai os dados necessarios de cada linha 
    com base em colunas predefinidas, e utiliza esses dados para criar uma lista de 
    objetos `Monster`.

    Args:
        file_name (str): O nome do arquivo .csv a ser aberto.

    Returns:
        list[Monster]: Uma lista contendo instancias do tipo `Monster`, 
        com cada instancia representando uma linha do arquivo.

    Notas:
        - As colunas selecionadas do arquivo .csv são baseadas no indice definido em `desired_info`.
        - As colunas consideradas sao:
            0. Nome do monstro
            1. Tamanho
            2. Tipo
            3. Alinhamento
            4. Classe de Armadura (AC)
            5. Pontos de Vida (HP)
            18. Nivel de Desafio (CR)
            20. Fonte
        - Caso alguma coluna especificada nao exista em uma linha, será substituida por uma string vazia.
    """
    # inicia uma lista para guardar os monstros
    monsters = []
    # abre o arquivo para leitura
    with open(file_name, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        # faz uma lista com o numero das colunas que contem as informacoes a serem coletadas
        desired_info = [0, 1, 2, 3, 4, 5, 18, 20] 

        # para cada linha do arquivo
        for row in csvreader:
            # ate terminar a linha, se a coluna tiver um dos numeros apontados anteriormente, guarda em uma lista
            selected_data = [row[i] if i < len(row) else "" for i in desired_info]
            # coloca cada dado na sua devida categoria
            name, size, type, aligment, AC, HP, CR, source = selected_data
            # agrupa os dados em um item do tipo Monstro
            monster = Monster(name, size, type, aligment, AC, HP, CR, source)
            # adiciona o item na lista de monstros
            monsters.append(monster)
    return monsters

def load_to_file(monsters: list[Monster]) -> None:
    """
    Esta funcao recebe uma lista de instancias do tipo `Monster` e escreve 
    seus atributos no arquivo "monsters.txt", onde cada linha do arquivo 
    representa um monstro.

    Args:
        monsters (list[Monster]): Lista de objetos do tipo `Monster` a serem salvos no arquivo.

    Notas:
        - Cada linha do arquivo resultante contém os atributos de um monstro, separados por virgulas.
        - Os atributos escritos no arquivo sao:
            - name: Nome do monstro
            - size: Tamanho
            - type: Tipo
            - alignment: Alinhamento
            - AC: Classe de Armadura
            - HP: Pontos de Vida
            - CR: Nivel de Desafio
            - source: Fonte
    """
    # abre o arquivo para escrita
    with open('monsters.txt', 'w', encoding='utf-8') as txt_file:
        # para cada Monster da lista
        for monster in monsters:
            # escreve seus dados em uma mesma linha
            txt_file.write(f"{monster.name},{monster.size},{monster.type},{monster.alignment},{monster.AC},{monster.HP},{monster.CR},{monster.source}\n")

def choose_attribute(attributes: list[str], message: str) -> str:
    """
    Esta funcao apresenta uma lista de opções de atributos para o usuario, exibe uma mensagem
    personalizada e valida a escolha do usuário até que uma entrada valida seja fornecida.

    Args:
        attributes (list[str]): Lista de opcoes de atributos disponiveis para o usuário escolher.
        message (str): Mensagem personalizada pedindo ao usuario para fazer uma escolha.

    Returns:
        str: A opção de atributo escolhida pelo usuario.

    Raises:
        ValueError: Se o numero inserido pelo usuario nao estiver entre as opções validas.
    """
    # impressao de linha vazia para facilitar leitura do usuario
    print('\n')
    # coloca variavel como numero maior que quantidades de opcoes para possibilitar validacao posterior
    ans = len(attributes) + 1
    # para cada opcao de atributo
    for number, attribute in enumerate(attributes, start=1):
        # printa numero que o usuario pode escolher e a opcao correspondente
        print(f"{number} - {attribute.attribute}")
    # ans recebe input do usuario
    ans = int(input(message))
    # enquanto ans for 0 ou um numero maior do que o numero de opcoes (ou seja, entradas validas)
    while 0<ans>len(attributes):
        # ans recebe input so usuario
        ans = int(input('Entrada invalida. Favor escolha um numero valido: '))
    # retorna opcao de atributo correspondente a escolha do usuario-1(para corrigir enumeracao de
    # alternativas de atributo comecadas em 1, mas lista comeca em 0)
    return attributes[ans-1].attribute

def choose_size() -> str:
    """
    Solicita ao usuario que escolha o tamanho de um monstro entre varias opcoes predefinidas.

    A funcao cria uma lista de opcoes de tamanhos de monstros e passa essa lista para a funcao 
    `choose_attribute`, onde o escolhido usuario uma das opcoes. A funcao retorna o tamanho escolhido.

    Returns:
        str: O tamanho do monstro escolhido pelo usuario.
    """
    sizes = [
        Monster_Attribute('Tiny', 1),
        Monster_Attribute('Small', 2),
        Monster_Attribute('Medium', 3),
        Monster_Attribute('Large', 4),
        Monster_Attribute('Huge', 5),
        Monster_Attribute('Gargantuan', 6)
    ]
    return choose_attribute(sizes, 'Qual o tamanho do monstro? ')

def choose_type() -> str:
    """
    Solicita ao usuario que escolha o tipo de um monstro entre varias opcoes predefinidas.

    A funcao cria uma lista de opcoes de tamanhos de monstros e passa essa lista para a funcao 
    `choose_attribute`, onde o usuario escolhe uma das opcoes. Se o tipo escolhido for "Fiend",
    a funcao solicita uma escolha adicional para a categoria de "Fiend" entre tres opcoes. A funcao 
    retorna o tipo ou a categoria de "Fiend" escolhida.

    Returns:
        str: O tipo ou a categoria de "Fiend" do monstro escolhido pelo usuario.
    """
    types = [
        Monster_Attribute('Aberration', 1),
        Monster_Attribute('Beast', 2),
        Monster_Attribute('Celestial', 3),
        Monster_Attribute('Construct', 4),
        Monster_Attribute('Dragon', 5),
        Monster_Attribute('Elemental', 6),
        Monster_Attribute('Fey', 7),
        Monster_Attribute('Fiend', 8),
        Monster_Attribute('Giant', 9),
        Monster_Attribute('Humanoid', 10),
        Monster_Attribute('Monstrosity', 11),
        Monster_Attribute('Ooze', 12),
        Monster_Attribute('Plant', 13),
        Monster_Attribute('Undead', 14)
    ]
    ans = choose_attribute(types, 'Qual o tipo do monstro? ')
    if ans == 'Fiend':
        fiend_types = [
            Monster_Attribute('Fiend (Devil)', 1),
            Monster_Attribute('Fiend (Demon)', 2),
            Monster_Attribute('Nao Especifo', 3)
        ]
        fiend_type = choose_attribute(fiend_types, 'Qual a categoria de fiend? Escolha 3 se nao tiver especificado: ')
        return fiend_type
    return ans

def choose_alignment() -> str:
    """
    Solicita ao usuario que escolha o alinhamento de um monstro entre varias opcoes predefinidas.

    A funcao cria uma lista de opções de alinhamento para o monstro e passa essa lista para a 
    funacao `choose_attribute`, onde o usuario escolhe o alinhamento do monstro. O alinhamento pode 
    ser um dos valores tradicionais de D&D ou "ANY" para qualquer alinhamento.

    Returns:
        str: O alinhamento do monstro escolhido pelo usuario.
    """
    alignments = [
        Monster_Attribute('LG', 1),
        Monster_Attribute('NG', 2),
        Monster_Attribute('CG', 3),
        Monster_Attribute('LN', 4),
        Monster_Attribute('TN', 5),
        Monster_Attribute('CN', 6),
        Monster_Attribute('LE', 7),
        Monster_Attribute('NE', 8),
        Monster_Attribute('CE', 9),
        Monster_Attribute('ANY', 10)
    ]
    return choose_attribute(alignments, 'Qual o alinhamento do monstro? ')

def choose_source() -> str:
    """
    Solicita ao usuario que escolha a fonte de um monstro entre varias opcoes predefinidas.

    A funacao cria uma lista de fontes de onde o monstro pode ter vindo, incluindo livros oficiais de 
    Dungeons & Dragons, como "Monster Manual" e "Tales from the Yawning Portal", e também a opção "Homebrew" 
    para monstros criados pelo usuário ou fora dos livros oficiais. A lista de fontes é passada para a funcao 
    `choose_attribute`, onde o usuário faz a escolha.

    Returns:
        str: O nome da fonte de onde o monstro foi originado, conforme escolhido pelo usuario.
    """
    sources = [
        Monster_Attribute('Monster Manual', 1),
        Monster_Attribute('Tomb of Annihilation', 2),
        Monster_Attribute('Mordenkainen\'s Tome of Foes', 3),
        Monster_Attribute('Hoard of the Dragon Queen', 4),
        Monster_Attribute('Curse of Strahd', 5),
        Monster_Attribute('Tales from the Yawning Portal', 6),
        Monster_Attribute('Volo\'s Guide to Monsters', 7),
        Monster_Attribute('Dungeon Master\'s Guide', 8),
        Monster_Attribute('Out of the Abyss', 9),
        Monster_Attribute('Princes of the Apocalypse', 10),
        Monster_Attribute('Rise of Tiamat', 11),
        Monster_Attribute('Storm King\'s Thunder', 12),
        Monster_Attribute('Xanathar\'s Guide to Everything', 13),
        Monster_Attribute('The Tortle Package', 14),
        Monster_Attribute('Homebrew', 15)
    ]
    return choose_attribute(sources, 'De qual livro veio esse monstro? ')

def new_monster(monsters) -> list[Monster]:
    """
    Solicita ao usuario informacoes sobre um novo monstro, cria um objeto Monster e o adiciona a uma lista existente.

    A funaoo pede ao usuario o nome, tamanho, tipo, alinhamento, CA (Classe de Armadura), HP (Pontos de Vida),
    CR (Nivel de Desafio) e a fonte de onde o monstro foi originado. Antes de adicionar o monstro a lista, a funcao verifica
    se o nome já está presente na lista de monstros. Se o nome ja existir, a função informa o usuario e retorna a 
    lista original.

    Args:
        monsters (list[Monster]): A lista de monstros a qual o novo monstro sera adicionado.

    Returns:
        list[Monster]: A lista de monstros atualizada, incluindo o novo monstro, caso o nome nao esteja duplicado.
    """
    name = input('Digite o nome do monstro que deseja inserir: ')
    # validacao de nome
    if any(monster.name == name for monster in monsters):
        print('Esse mosnstro ja esta na lista.')
        return monsters
    size = choose_size()
    type = choose_type()
    alignment = choose_alignment()
    AC = (input('Digite o CA do monstro: '))
    HP = (input('Digite o HP do monstro: '))
    CR = (input('Digite o CR do monstro: '))
    source = choose_source()
    # coloca informacoes coletadas em suas respectivas categorias
    monster = Monster(name, size, type, alignment, AC, HP, CR, source)
    # adiciona novo Monster a lista recebida
    monsters.append(monster)
    # retorna lista
    return monsters

def more_mosters(monsters) -> None:
    """
    Oferece opcoes ao usuario para adicionar mais monstros a lista, seja carregando mais monstros de uma planilha CSV ou 
    inserindo manualmente novos monstros. 
    Apos a interacao do usuario, atualiza o arquivo "monsters.txt" com a lista final de monstros.

    A funcao permite adicionar monstros manualmente, solicitando informacoes do usuario sobre o novo monstro.
    Parar de adicionar monstros.

    Quando o usuario decide parar, o arquivo "monsters.txt" e sobrescrito com a lista final de monstros.

    Args: monsters (list[Monster]): A lista de monstros que sera modificada durante a execucao da funcao.
    """
    # inciacao de variavel com valor fora das opcoes para iniciar loop
    ans = 0 
    # enquanto resposta for invalida
    while ans != 2:
            print('\n1 - adicionar mais monstros')
            print('2 - parar de adicionar monstros')
            ans = int(input('Digite numero correspondente a opcao desejada: '))
            if ans not in [1, 2]:
                print('Favor entre com uma resposta valida: ')
            if ans == 1:
                # chama funcao new_monster
                monsters = new_monster(monsters)
            
    print('\n')

    # sobrescreve arquivo "monsters.txt"
    load_to_file(monsters)

def index_file_tree(tree, file_name) -> None:
    """
    A funcao percorre a arvore de forma ordenada e para cada valor de atributo presente nos nos,
    ela escreve em uma linha do arquivo o valor do atributo seguido dos indices dos monstros que possuem 
    esse valor de atributo no arquivo "monsters.txt". Caso um valor de atributo tenha multiplos indices associados, todos os indices 
    sao listados separados por virgulas.

    Args: tree (BST): A arvore binaria de busca que contem os valores dos atributos e os indices dos monstros. 
    file_name (str): O nome do arquivo onde os indices serao gravados. 
    """
    # abre o arquivo para escrita
    with open(file_name, 'w', encoding='utf-8') as txt_file:
        # para cada valor de atributo presente nos nodos da arvores
        for value, indexes in tree.in_order():
            # se tiver mais de um indice, formando uma lista
            if isinstance(indexes, list):
                # escreve no arquivo o valor seguidos dos indices correspondentes
                txt_file.write(f"{value}, {','.join(map(str, indexes))}\n")
            else:
                # escreve no arquivo o valor seguidos do indice correspondente
                txt_file.write(f"{value}, {indexes}\n")

def index_file(names) -> None:
    """
    Recebe uma lista de objetos `Monster_Attribute` e escreve o nome e o Andice de acesso de cada objeto em um arquivo de Andices.

    A funcao percorre a lista de `Monster_Attribute`, extraindo o atributo `attribute` (nome) e o `index`, e grava essas informacoes
    no arquivo de texto "index_names.txt", onde cada linha contem o nome e o índice correspondente.

    Args:
        names (list of Monster_Attribute): A lista de objetos `Monster_Attribute` que contem o nome (atributo `attribute`)
                                           e o indice (atributo `index`) a ser gravado no arquivo.
    """
    # abre o arquivo para escrita
    with open ('index_names.txt', 'w', encoding='utf-8') as txt_file:
        # para cada nome na lista de Monster_Attribute
        for name in names:
            # escreve o nome e o indice de acesso no arquivo
            txt_file.write(f"{name.attribute}, {name.index}\n")

def to_number(value) -> Union[float, str]:
    """
    A função tenta converter o valor passado para um numero de ponto flutuante. Se a conversao for bem-sucedida,
    o valor convertido e retornado. Caso contrário, o valor original (como string) e retornado.

    Args:
        value (str): O valor a ser convertido para número.

    Returns:
        Union[float, str]: O valor convertido para `float` se possivel, ou o valor original caso contrário.
    """
    # caso seja possivel transformar em float
    try:
        # converte
        return float(value)
    # se houver erro (nao e possivel)
    except ValueError:
        # retorna nao convertido
        return value

def index() -> None:
    """
    Abre o arquivo "monsters.txt", que contem um monstro por linha, coleta os dados de cada atributo,
    os organiza em uma arvore (ou lista no caso dos nomes) e cria arquivos de indices que contem os 
    diferentes valores de cada atributo e o numero da linha dos monstros correspondentes no arquivo original.

    Os indices gerados são:
        - `index_names.txt`: Contem os nomes dos monstros e os indices das linhas.
        - `index_sizes.txt`: Contem os tamanhos dos monstros e os indices das linhas.
        - `index_types.txt`: Contem os tipos dos monstros e os indices das linhas.
        - `index_alignments.txt`: Contem os alinhamentos dos monstros e os indices das linhas.
        - `index_ACs.txt`: Contem os valores de AC (Classe de Armadura) dos monstros e os indices das linhas.
        - `index_HPs.txt`: Contem os valores de HP (Pontos de Vida) dos monstros e os indices das linhas.
        - `index_CRs.txt`: Contem os valores de CR (Nivel de Desafio) dos monstros e os indices das linhas.
        - `index_sources.txt`: Contem as fontes dos monstros e os indices das linhas.
    """
    # inicia a arvore ou lista de cada atributo
    names = []
    sizes = Trie()
    types = Trie()
    alignments = Trie()
    ACs = BST()
    HPs = BST()
    CRs = BST()
    sources = Trie()

    # abre arquivo para leitura
    with open ('monsters.txt', 'r') as source_file:
        # inicia variavel que guarda o valor da linha sendo lida
        offset = 0
        # ate terminar o arquivo
        while True:
            # le cada linha individualmente
            line = source_file.readline()
            # caso haja erro da um break
            if not line:
                break
            # pega a linha, limpa os espaços em branco antes e depois dos caracteres 
            # das pontas, e divide em 8 pelas virgulas, contando a partir da direita
            monster = line.strip().rsplit(',', 7)
            # cada atributo recebe dado correspondente
            name = monster[0].strip()[:32]
            size = monster[1].strip()[:10]
            type = monster[2].strip()[:40]
            alignment = monster[3].strip()[:11]
            # como AC, HP e CR sao em sua maioria numeros, tenta converter para float 
            # com funcao to_number
            AC = to_number(monster[4].strip())
            HP = to_number(monster[5].strip())
            CR = to_number(monster[6].strip())
            source = monster[7].strip()[:30]

            # adiciona atributos do Monster lido nas suas respectivas estruturas 
            # de dados, seguido do numero da linha para facilitar acesso
            names.append(Monster_Name(monster[0], offset))
            sizes.insert(Monster_Attribute(monster[1], offset))
            types.insert(Monster_Attribute(monster[2], offset))
            alignments.insert(Monster_Attribute(monster[3], offset))
            ACs.insert(Monster_Attribute(AC, offset))
            HPs.insert(Monster_Attribute(HP, offset))
            CRs.insert(Monster_Attribute(CR, offset))
            sources.insert(Monster_Attribute(monster[7], offset))
            # soma um a variavel que fala qual linha foi lida
            offset += 1

    # organiza os nomes em ordem alfabetica
    names = sorted(names, key=lambda x: x.attribute)
    # passa lista de nomes para funcao index_file
    index_file(names)
    # passa demais listas de atributos para index_file_tree, acompanhado
    # do nome do arquivo de indices correspondente
    index_file_tree(sizes, 'index_sizes.txt')
    index_file_tree(types, 'index_types.txt')
    index_file_tree(alignments, 'index_alignments.txt')
    index_file_tree(ACs, 'index_ACs.txt')
    index_file_tree(HPs, 'index_HPs.txt')
    index_file_tree(CRs, 'index_CRs.txt')
    index_file_tree(sources, 'index_sources.txt')

def number_then_string(value, order) -> Tuple[int, Union[float, str]]:
    """
    A funcao tenta converter o valor passado para float. Se a conversao for bem-sucedida,
    a funcao retorna uma tupla com a flag `0` e o valor convertido para float. Se a conversao
    falhar, a funcao retorna uma tupla com a flag `1` e o valor original como string.

    Args:
        value (Union[str, float]): O valor a ser processado. Pode ser uma string ou um numero.
        order (int): flag que indica se os numeros devem ser ordenados em ordem crescente ou descrecente

    Returns:
        Tuple[int, Union[float, str]]:
            - Se a conversao para float for bem-sucedida, retorna uma tupla `(0, float)`.
            - Se a conversao falhar, retorna uma tupla `(1, str)`, mantendo o valor original como string.
    """
    try:
        if isinstance(value, str):
            num = float(value)
            return (0, num * order)
    except ValueError:
        pass
    return (1, str(value))

def print_monster(monster_data) -> None:
    """
    Recebe um dado de monstro no formato de string, cria um objeto `Monster` 
    com os atributos correspondentes e imprime suas informações na tela.

    A funcao divide os dados do monstro em 8 atributos e os imprime de forma legivel, 
    incluindo nome, tamanho, tipo, alinhamento, CA, HP, CR e fonte.

    Args:
        monster_data (str): Uma string contendo os dados de um monstro, separados por virgulas.
            Espera-se que a string tenha a seguinte estrutura:
            'nome,tamanho,tipo,alinhamento,CA,HP,CR,fonte'.
    """
    # pega os atributos do mosnstro, limpa os espaços em branco antes e depois dos caracteres 
    # das pontas, e divide em 8 pelas virgulas, contando a partir da direita
    monster_data = monster_data.strip().rsplit(',', 7)
    monster = Monster(
        # liga cada atributo a categoria correspondente
        name=monster_data[0].strip(),
        size=monster_data[1].strip(),
        type=monster_data[2].strip(),
        alignment=monster_data[3].strip(),
        AC=monster_data[4].strip(),
        HP=monster_data[5].strip(),
        CR=monster_data[6].strip(),
        source=monster_data[7].strip()
    )

    # linha em branco para faciltar leitura dos dados
    print('\n')
    # impressao dos atributos do Monster
    print(f'Nome: {monster.name}')
    print(f'Tamanho: {monster.size}')
    print(f'Tipo: {monster.type}')
    print(f'Alinhamento: {monster.alignment}')
    print(f'CA: {monster.AC}')
    print(f'HP: {monster.HP}')
    print(f'CR: {monster.CR}')
    print(f'Fonte: {monster.source}')

def load_index(file) -> Tuple[list[str], defaultdict[str, list[int]]]:
    """
    Abre um arquivo de indice que contém linhas no formato 'atributo, lista de indices', onde a 
    lista de indices indica as linhas do arquivo 'monsters.txt' que possuem o valor de 
    atributo correspondente. Cria um dicionario onde cada valor de atributo 
    esta relacionado aos numeros das linhas dos monstros correspondentes no arquivo 
    'monsters.txt'.

    Args:
        file (str): O nome do arquivo de indice a ser carregado. O arquivo deve ter o 
                    formato de "atributo, lista de indices", onde os indices são separados 
                    por vírgulas.

    Returns:
        Tuple[list[str], defaultdict[str, list[int]]]:
            - A lista de categorias de atributos encontradas no arquivo.
            - Um dicionario onde cada chave é um valor de atributo e o valor é uma lista 
              de indices das linhas de monstros no arquivo 'monsters.txt' que possuem esse 
              valor de atributo.
    """
    # inicia uma lista para armazenar os diferentes valores do atributo
    categories = []
    # inicia um dicionario para ligar cada valor aos indexes correspondentes
    categories_dic = defaultdict(list)

    # abre arquivo para leitura
    with open(file, 'r') as file:
        # para cada linha(valor de atributo) do arquivo
        for line in file:
            # separa em dois a partir da virgula
            data = line.split(',', 1)
            # primeira parte e a categoria do atributo
            attribute = data[0].strip()[:30]
            # segunda e os valores do index, tira os escacos em branco desnecessarios,
            # divide pelas virgulas e anexa na lista index
            index = [int(num.strip()) for num in data[1].split(',')] 
            # liga a lista index a categoria por meio do dicionario
            categories_dic[attribute].extend(index)
            # se categoria ainda nao tiver na lista de categorias
            if attribute not in categories:
                # adiciona na lista de categorias
                categories.append(attribute)
    # retorna lista de categorias e dicionario
    return categories_dic

def search_number(file, string, dictionary) -> None:
    """
    Pesquisa por monstros em um arquivo de monstros ('monsters.txt') com base em uma categoria de atributo 
    escolhida pelo usuário. Para cada categoria, exibe os monstros que correspondem a categoria 
    de atributo selecionada, usando os indices fornecidos no dicionário. Exibe tambem a porcentagem de monstros 
    que se encaixam na categoria em relacao ao total de monstros.

    Args:
        file (str): O nome do arquivo que contem os dados dos monstros (deve estar no formato 'monsters.txt').
        string (str): A string que descreve o tipo de atributo (por exemplo, "tamanho", "tipo", etc.).
        dictionary (dict): Um dicionario onde as chaves são as categorias de atributos (como "Tamanho", "Tipo", etc.) 
                           e os valores sao listas de indices correspondentes as linhas dos monstros no arquivo 'monsters.txt'.
    """
    # inicia lista para guardar as categorias de atributo
    keys = []
    # inicia lista para organizar as categorias de atributo
    categories = list(dictionary.keys())  

    # criacao de variavel para controle do loop de validacao
    ans = 3
    # loop de validacao
    while ans not in [1,2]:
        # ans e o input do usuario. {string} utilizada para informar por qual atributo
        # esta sendo realizada a pesquisa.
        ans = int(input(f'Aperte 1 para visualizar as opcoes em orderm crescente e 2 para descrescente: '))
        # se input do usuario for valido 
        if ans not in [1,2]:
            # pede novo input
            print('Entrada inválida. Favor escolha um número válido.')
        else:
            break
    
    # se escolha for 1 (ordem crescente)
    if ans == 1:
        # organiza itens da lista numbers colocando primeiro os numeros em ordem 
        # crescente depois as strings
        order = 1
        categories.sort(key=lambda x: number_then_string(x, order))
    
    # se escolha for 2 (ordem descrescente)
    if ans == 2:
        # organiza itens da lista numbers colocando primeiro os numeros em ordem 
        # descrescente depois as strings
        order = -1
        categories.sort(key=lambda x: number_then_string(x, order))

    # linha em branco para facilitar leitura
    print ('\n')
    # para cada item da lista numbers (categorias de atributo organizadas)
    for number, cr in enumerate(categories, start=1):
        # printa o numero que o usuario deve escolher para procurar por 
        # monstros nessa categoria e a categoria em si 
        print(f"{number} - {cr}")

    # loop de validacao
    while True:
        try:
            # ans e o input do usuario. {string} utilizada para informar por qual atributo
            # esta sendo realizada a pesquisa. input-1 para corrigir fato do dicionario 
            # comecar a contar do 0 e escolhas serem mostradas a partir do 1
            ans = int(input(f'Escolha o numero do lado do {string} do monstro desejado: ')) - 1
            # se input do usuario for valido (resposta entre 1 e o numero de categorias de atributo
            if 0 <= ans < len(categories):
                # da um break
                break
        # caso input tenha sido invalido
        except ValueError:
            # pede input novo do usuario
            print('Entrada inválida. Favor escolha um número válido.')

    # categoria escolhida e o item de categorias correspondente a ans
    category = categories[ans]
    # total de monstros e o comprimento da lista de valores anexados pelo dicionario
    # conta os indexes de todas as categorias
    total_items = sum(len(values) for values in dictionary.values())
    # contagem de itens impresssos 
    items_printed = 0
    # abre arquivo para leitura
    with open('monsters.txt', 'r') as file_monsters:
        # para cada index ligado a categoria pelo dicionario
        for index in dictionary[category]: 
            # vai pra primeira linha do documento
            file_monsters.seek(0) 
            # para cada linha do arquivo 'monsters.txt'
            for current_line_number , line in enumerate(file_monsters):
                # se numero da linha for igual ao index
                if current_line_number == index:
                    # tira espaços em branco das extremidades
                    monster_data = line.strip()
                    # passa dados do monstro para a funcao print_monster
                    print_monster(monster_data)
                    # incrementa contagem de itens impressos
                    items_printed += 1
    
    # mostra quantos monstros se enxaixam na categoria
    print(f"\nTotal de monstros com {string} '{categories[ans]}': {items_printed}")
    if total_items > 0:
        percentage_printed = (items_printed / total_items) * 100
        # e porcentagem dos monstros pertencentes a essa categoria
        print(f"Porcentagem de monstros com {string} '{number}': {percentage_printed:.2f}% ")

def search_string(file, string, dictionary) -> None:
    """
    Pesquisa por monstros em um arquivo de monstros ('monsters.txt') com base em uma categoria de atributo 
    escolhida pelo usuário. Para cada categoria, exibe os monstros que correspondem a categoria 
    de atributo selecionada, usando os indices fornecidos no dicionário. Exibe tambem a porcentagem de monstros 
    que se encaixam na categoria em relacao ao total de monstros.

    Args:
        file (str): O nome do arquivo que contém os dados dos monstros (deve estar no formato 'monsters.txt').
        string (str): A string que descreve o tipo de atributo (por exemplo, "AC", "HP", etc.).
        dictionary (dict): Um dicionario onde as chaves são as categorias de atributos (como AC", "HP", etc.) 
                           e os valores são listas de indices correspondentes as linhas dos monstros no arquivo 'monsters.txt'.
    """
    # define ordem para atributo tamanho
    order = ['Tiny', 'Small', 'Medium', 'Large', 'Huge', 'Gargantuan']
    # cria ordena lista para organizaras categorias de atributo
    categories = sorted(dictionary.keys(), key=lambda x: (x not in order, order.index(x) if x in order else len(order)))
    
    # linha em branco para facilitar leitura
    print ('\n')
    # para cada item da lista numbers (categorias de atributo organizadas)
    for number, category in enumerate(categories, start=1):
        # printa o numero que o usuario deve escolher para procurar por 
        # monstros nessa categoria e a categoria em si 
        print(f"{number} - {category}")

    # loop de validacao
    while True:
        try:
            # ans e o input do usuario. {string} utilizada para informar por qual atributo
            # esta sendo realizada a pesquisa. input-1 para corrigir fato do dicionario 
            # comecar a contar do 0 e escolhas serem mostradas a partir do 1
            ans = int(input(f'Escolha qual {string} do monstro desejado: ')) - 1
            # se input do usuario for valido (resposta entre 1 e o numero de categorias de atributo
            if 0<=ans<len(categories):
                # da um break
                break
        # caso input tenha sido invalido
        except ValueError:
            # pede input novo do usuario
            print('Entrada invalida. Favor escolha um numero valido: ')

    # categoria escolhida e o item de categorias correspondente a ans
    category_name = categories[ans]
    # total de monstros e o comprimento da lista de valores anexados pelo dicionario
    # conta os indexes de todas as categorias
    total_items = sum(len(values) for values in dictionary.values()) 
    # contagem de itens impresssos 
    items_printed = 0
    # abre arquivo para leitura
    with open('monsters.txt', 'r') as file_monsters:
        # para cada index ligado a categoria pelo dicionario
        for index in dictionary[category_name]:
            # vai pra primeira linha do documento
            file_monsters.seek(0)
            # para cada linha do arquivo 'monsters.txt'
            for current_line_number, line in enumerate(file_monsters):
                # se numero da linha for igual ao index
                if current_line_number == index:
                    # tira espaços em branco das extremidades
                    monster_data = line.strip()
                    # passa dados do monstro para a funcao print_monster
                    print_monster(monster_data)
                    # incrementa contagem de itens impressos
                    items_printed += 1

    # mostra quantos monstros se enxaixam na categoria
    print(f"\nTotal de monstros com {string} {category_name.lower()}: {items_printed}")
    if total_items > 0:
        percentage_printed = (items_printed / total_items) * 100
        # e porcentagem dos monstros pertencentes a essa categoria
        print(f"Porcentagem de monstros com {string} {category_name.lower()}: {percentage_printed:.2f}%")

def search_name() -> None:
    """
    Solicita ao usuário o nome de um monstro, divide o nome em palavras-chave e 
    pesquisa essas palavras no indice de nomes para encontrar monstros correspondentes. 
    Em seguida, exibe os monstros encontrados no arquivo de monstros ('monsters.txt').

    A pesquisa e feita de forma que todos os termos fornecidos pelo usuário devem 
    estar presentes no nome do monstro para que ele seja considerado uma correspondência.

    Se um ou mais monstros corresponderem a pesquisa, eles serao exibidos. Caso contrario, 
    uma mensagem informando que o monstro nao foi encontrado sera mostrada.

    Também e exibido o total de monstros encontrados e a porcentagem desses monstros 
    em relacao ao total de monstros no arquivo.
    """
    # pede nome ao usuario
    name = input('Digite o nome do monstro desejado: ').strip().lower()
    # inicia lista para guardar nomes de monstros que tem todas as 
    # palavras pesquisas
    monsters_list = []

    # inicia lista com todos os termos da pesquisa separados de acordo 
    # com os espacos em branco
    search_terms = set(name.split())

    # abre arquivo de indice de nomes para leitura
    with open('index_names.txt', 'r') as file:
        # para cada linha
        for line in file:
            # divide pela primeira virgula
            data = line.rsplit(',', 1)
            # nome e a parte antes da virgula
            monster_name = data[0].strip().lower()
            # index e a parte depois
            index = int(data[1].strip())

            # se todos os termos em monster_name estiverem na lista de 
            # termos de pesquisa
            if all(term in monster_name for term in search_terms):
                # lista de nomes recebe o item Monster_Name correspondente
                # a linha lida
                monsters_list.append(Monster_Name(monster_name, index))
    
    # se nao tiver nenhum monstro na lista com todos os termos correspondentes
    if not monsters_list:
        # printa que monstro nao foi achado
        print(f'Monstro "{name}" não encontrado.')
        # da um break
        return

    # contagem de itens impresssos 
    items_printed = 0
    # contagem de monstros
    monsters_counter = 0
    # abre arquivo 'monster.txt" para leitura
    with open('monsters.txt', 'r') as file_monsters:
        # para cada linha do arquivo
        for current_line_number, line in enumerate(file_monsters):
            # incrementa contagem de monstros
            monsters_counter += 1
            # para cada monstro em monsters_list
            for monster in monsters_list:
                # se a linha lida tem o mesmo numero do index do monstro
                if current_line_number == monster.index:
                    # tira espaços em branco das extremidades
                    monster_data = line.strip()
                    # passa dados do monstro para a funcao print_monster
                    print_monster(monster_data)
                    # incrementa contagem de itens impressos
                    items_printed += 1

    # mostra quantos monstros se enxaixam com o nome pesquisado
    print(f"\nTotal de monstros com nome {name}: {items_printed}")
    percentage_printed = (items_printed / monsters_counter) * 100
    # e porcentagem dos monstros pertencentes a essa categoria
    print(f"Porcentagem de monstros com nome {name}: {percentage_printed:.2f}%")

def menu_search() -> int:
    """
    Exibe um menu com opcoes de atributos para pesquisa e solicita ao usuario
    que escolha um tipo de pesquisa a ser realizada. O menu inclui as opcoes de 
    pesquisa por nome, tamanho, tipo, alinhamento, CA, HP, CR e fonte.

    Apos exibir as opcoes, a função aguarda a escolha do usuario e valida a entrada
    para garantir que ela esteja entre as opções validas (1 a 8). Caso a entrada
    seja invalida, o usuario sera solicitado a inserir novamente.

    Returns:
        int: O numero correspondente a opcao escolhida pelo usuario (1 a 8).
    """
    print('\n1 - Nome')
    print('2 - Tamanho')
    print('3 - Tipo')
    print('4 - Alinhamento')
    print('5 - CA')
    print('6 - HP')
    print('7 - CR')
    print('8 - Fonte')

    ans = int(input('Digite o numero do tipo de pesquisa que deseja realizar: '))
    # loop de validacao
    while ans not in [1, 2, 3, 4, 5, 6, 7, 8]:
        ans = int(input('Entrada invalida. Favor escolha um numero valido: '))

    return ans

def search() -> None:
    """
    Permite ao usuário realizar pesquisas de monstros com base em diferentes atributos.
    O usuario escolhe o tipo de pesquisa atraves de um menu interativo, e a funcao
    chama a funcao correspondente para realizar a pesquisa de acordo com a escolha.

    O processo e repetido enquanto o usuario desejar realizar mais pesquisas. 
    O menu oferece as opcoes de pesquisa por nome, tamanho, tipo, alinhamento, CA, HP, CR e fonte.

    O fluxo da funçao é o seguinte:
        1. Exibe um menu de opcoes de pesquisa e coleta a escolha do usuario.
        2. Dependendo da escolha do usuario, a funcao chama a funcao apropriada 
           (como `search_name`, `search_string`, `search_number`).
        3. Após cada pesquisa, a funcao pergunta ao usuario se ele deseja realizar outra pesquisa.
        4. Se o usuario desejar continuar, o loop é reiniciado. Caso contrario, a pesquisa termina.
    """
    # enquanto usuario quiser seguir pesquisando
    while True:
        # pega atributo para pesquisa com menu_search()
        ans = menu_search()

        # se escolha for 1
        if ans == 1:
            # chama search_name()
            search_name()

        # se escolha for 2
        elif ans == 2:
            # passa arquivo de index para load_index, 
            # criando dicionario de index do atributo
            index_sizes = load_index('index_sizes.txt')
            # passa arquivo de index, string para pesquisa e dicionario 
            # para funcao search_string
            search_string('index_sizes.txt', 'tamanho', index_sizes)
        
        # se escolha for 3
        elif ans == 3:
            # passa arquivo de index para load_index, 
            # criando dicionario de index do atributo
            index_types = load_index('index_types.txt')
            # passa arquivo de index, string para pesquisa e dicionario 
            # para funcao search_string
            search_string('index_types.txt', 'tipos', index_types)
        
        # se escolha for 4
        elif ans == 4:
            # passa arquivo de index para load_index, 
            # criando dicionario de index do atributo
            index_alignments = load_index('index_alignments.txt')
            # passa arquivo de index, string para pesquisa e dicionario 
            # para funcao search_string
            search_string('index_alignments.txt', 'alinhamento', index_alignments)
        
        # se escolha for 5
        elif ans == 5:
            # passa arquivo de index para load_index, 
            # criando dicionario de index do atributo
            index_ACs = load_index('index_ACs.txt')
            # passa arquivo de index, string para pesquisa e dicionario 
            # para funcao search_number
            search_number('index_ACs.txt', 'CA', index_ACs)
        
        # se escolha for 6
        elif ans == 6:
            # passa arquivo de index para load_index, 
            # criando dicionario de index do atributo
            index_HPs = load_index('index_HPs.txt')
            # passa arquivo de index, string para pesquisa e dicionario 
            # para funcao search_number
            search_number('index_HPs.txt', 'HP', index_HPs)
        
        # se escolha for 7
        elif ans == 7:
            # passa arquivo de index para load_index, 
            # criando dicionario de index do atributo
            index_CRs = load_index('index_CRs.txt')
            # passa arquivo de index, string para pesquisa e dicionario 
            # para funcao search_number
            search_number('index_CRs.txt', 'CR', index_CRs)
        
        # se escolha for 8
        else:
            # passa arquivo de index para load_index, 
            # criando dicionario de index do atributo
            index_sources = load_index('index_sources.txt')
            # passa arquivo de index, string para pesquisa e dicionario 
            # para funcao search_string
            search_string('index_sources.txt', 'fontes', index_sources)

        # inicia variavel de controle para loop
        continue_search = ''
        # enquanto variavel de controle nao for uma resposta valida
        while continue_search not in ['s', 'n']:
            # pega input do usuario
            continue_search = input('\nDeseja realizar outra pesquisa? (s/n): ').strip().lower()
            # se variavel de controle nao for uma resposta valida
            if continue_search not in ['s', 'n']:
                # pede input ao usuario novamente
                print('Entrada inválida. Digite "s" para continuar ou "n" para parar.')

        # se usuario nao quiser continuar pesquisa
        if continue_search == 'n':
            # da um break
            break

        # imprime linha em branco para facilitar leitura
        print('\n')

def main():
    """
    Controla o fluxo principal do programa, interagindo com o usuario para executar 
    acoes como carregar dados, adicionar monstros, realizar pesquisas ou sair do programa.

    O programa oferece as seguintes opcoes para o usuario:
        1. Recarregar o arquivo 'Monsters_D&D5e.csv', carregando os dados e criando indices.
        2. Carregar mais monstros, adicionando-os ao arquivo e criando novos indices.
        3. Realizar uma pesquisa de monstros com base em atributos especificos.
        4. Sair do programa.

    O fluxo de operacao depende da escolha do usuario, e a função continua a executar 
    ate que o usuário escolha sair.
    """
    # inicia variavel de controle para loop
    ans = 0
    # enquanto usuario quiser seguir usando o programa
    while ans != 4:
        # resposta do usuario e resultado da funcao menu()
        ans = menu()
    
        # se escolha for 1 (recarregar 'Monsters_D&D5e.csv')
        if ans == 1:
            # lista de monstros recebe resultado da funcao open_file()
            # aplicada ao arquivo 'Monsters_D&D5e.csv'
            monsters = open_file('Monsters_D&D5e.csv')
            # passa lista monsters para load_to_file()
            load_to_file(monsters)
            # chama funcao index() para criar lista de indexes
            index()
            # imprime mensagem
            print ('Arquivo carregado com sucesso!\n')

        # se escolha for 2 (carregar mais monstros)
        elif ans == 2:
            # lista de monstros recebe resultado da funcao open_file()
            # aplicada ao arquivo 'Monsters_D&D5e.csv'
            monsters = open_file('Monsters_D&D5e.csv')
            # passa lista monsters para load_to_file()
            load_to_file(monsters)
            # # passa lista monsters para more_monsters
            more_mosters(monsters)
            # chama funcao index() para criar lista de indexes
            index()

        # se escolha for 3 (pesquisar monstro)
        elif ans == 3:
            # chama funcao search(), que controla todo fluxo de pesquisa
            search()

        # se escolha for 4 (sair)
        else:
            # da um break
            break

if __name__ == "__main__":
    main()