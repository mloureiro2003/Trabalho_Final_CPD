"""
Importa os módulos e classes necessários para o funcionamento do programa:
- Tipos `Tuple`, `Union`, `Dict` do módulo `typing`: Usados para a documentao
de tipos nas funcoes, facilitando a compreensao do codigo.
- Estruturas de dados `Monster`, `Monster_Name`, `Monster_Attribute` do arquivo
 `monsters.py`: Utilizadas para armazenar informacoes relacionadas aos monstros, como nome, atributos e outras caracteristicas.
"""
from monsters import Monster, Monster_Name, Monster_Attribute
from typing import Tuple, Union, Dict

# definicao da classe TrieNode, representando um no de uma Trie (arvore de prefixos)
class TrieNode:
    def __init__(self) -> None:
        """
        Inicializa um no de Trie.
        - `children`: dicionario de filhos do no, onde a chave e o caractere e o valor e o próximo no.
        - `is_end_of_word`: booleano que indica se este no e o fim de uma palavra.
        - `indexes`: uma string que armazena os indices dos monstros associados ao atributo.
        """
        # filhos do no
        self.children = {}
         # indica se e o fim de uma palavra
        self.is_end_of_word = False
        # indices dos monstros
        self.indexes = ""

# definicao da classe Trie, que representa a estrutura da arvore Trie para busca eficiente
class Trie:
    def __init__(self) -> None:
        """
        Inicializa a Trie com a raiz como um TrieNode vazio.
        """
        self.root = TrieNode()

    def insert(self, monster: Monster_Attribute) -> None:
        """
        Insere um atributo de monstro na Trie.
        
        Para cada caractere no atributo do monstro, insere um no correspondente na Trie.
        Se o nó já existir, move para ele, caso contrário, cria um novo no.
        Quando o fim da palavra é alcançado, marca o no como `is_end_of_word` e armazena o indice.
        
        Args:
            monster (Monster_Attribute): O objeto Monster_Attribute que contem o atributo a ser inserido.
        """
        node = self.root
        for char in monster.attribute:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

        # adiciona o índice do monstro no no
        # se nodo ja tem indices
        if node.indexes:
            # adiciona mais índices
            node.indexes += "," + monster.get_index_string()
        # se nao
        else:
            # primeira vez adicionando índice
            node.indexes = monster.get_index_string()


    def in_order(self) -> list[Tuple[Union[str], int]]:
        """
        Realiza uma busca em ordem (in-order traversal) na Trie e retorna todos os atributos com seus índices.
        
        Returns:
            list: Lista de tuplas (atributo, índices), em ordem alfabética.
        """
        attributes = []
        # chama DFS para preencher a lista
        self._dfs(self.root, "", attributes)
        # retorna lista de atributos
        return attributes

    def _dfs(self, node: TrieNode, prefix: str, attributes: list):
        """
        Função auxiliar para realizar uma busca em profundidade (DFS) na Trie.
        
        Args:
            node (TrieNode): O nó atual da Trie.
            prefix (str): O prefixo formado até o momento.
            attributes (list): A lista que será preenchida com os resultados.
        """
        # se nodo for final de uma palavra
        if node.is_end_of_word:
            # adiciona o atributo e os indices encontrados
            attributes.append((prefix, node.indexes)) 
        # se nao, para cada letra do atributo do nodo chave
        for char in sorted(node.children.keys()):
            # passa recursivamente cada filho para dfs
            self._dfs(node.children[char], prefix + char, attributes)

# Definição da classe BSTNode, representando um no de uma Árvore de Busca Binária (BST).
class BSTNode:
    def __init__(self, key) -> None:
        """
        Inicializa um no de árvore binária com um chave (atributo).
        
        Args:
            key (Monster_Attribute): O atributo que será armazenado no nó.
        """
        self.key = key # o atributo do monstro
        self.left = None # no filho a esquerda
        self.right = None # no filho a direita

# Definicao da classe BST, representando uma arvore de Busca Binária (Binary Search Tree).
class BST:
    def __init__(self) -> None:
        """
        Inicializa a arvore binaria com a raiz como `None`.
        """
        self.root = None

    def insert(self, monster: Monster_Attribute) -> None:
        """
        Insere um novo atributo de monstro na árvore binária.
        
        A inserção segue a logica de arvore binária de busca, comparando o atributo e colocando-o a esquerda ou a direita.
        Se o atributo ja existir, os indices são adicionados ao no correspondente.

        Args:
            monster (Monster_Attribute): O objeto Monster_Attribute a ser inserido na árvore.
        """
        new_attribute = monster
        # se nao tiver raiz
        if self.root is None:
            # cria o no raiz
            self.root = BSTNode(new_attribute)
        # se não
        else:
            # chama a funcao recursiva de insercao
            self._insert(self.root, new_attribute)

    def _insert(self, node, new_attribute) -> None:
        """
        Funcao recursiva que realiza a inseraoo do novo atributo na arvore binaria.

        Args:
            node (BSTNode): O na atual da arvore.
            new_attribute (Monster_Attribute): O novo atributo a ser inserido.
        """
        if new_attribute.attribute == node.key.attribute:
           # se o atributo ja existe, adiciona o indice a lista de indices
           node.key.indexes.append(new_attribute.indexes[0])
        # se o atributo for menor, vai para o no a esquerda
        elif str(new_attribute.attribute) < str(node.key.attribute):
            # se nodo da esquerda esta vazio
            if node.left is None:
                # adiciona novo nodo
                node.left = BSTNode(new_attribute)
            # se nao
            else:
                # passa nodo da esquerda e novo nodo de forma recursiva para a funcao
                self._insert(node.left, new_attribute)
        # ae o atributo for maior, vai para o no a direita
        else:  
            # se nodo da direita esta vazio
            if node.right is None:
                # adiciona novo nodo
                node.right = BSTNode(new_attribute)
            # se nao
            else:
                # passa nodo da direita e novo nodo de forma recursiva para a funcao
                self._insert(node.right, new_attribute)

    def in_order(self) -> list[Tuple[Union[float, str], int]]:
        """
        Realiza a busca em ordem (in-order traversal) na arvore binaria e retorna os atributos com seus indices.
        
        Returns:
            list: Lista de tuplas (atributo, indices), em ordem crescente.
        """
        
        result = []
        # chama o metodo recursivo de in-order
        self._in_order(self.root, result)
        return result

    def _in_order(self, node, result):
        """
        Funcao auxiliar para realizar a busca em ordem na arvore binaria.

        Args:
            node (BSTNode): O na atual da arvore.
            result (list): A lista que será preenchida com os resultados.
        """
        if node:
            # chama recursivamente para o filho a esquerda
            self._in_order(node.left, result) 
            # Adiciona o atributo e os índices ao nodo recebido
            result.append((node.key.attribute, node.key.indexes)) 
            # Chama recursivamente para o filho a direita
            self._in_order(node.right, result) 