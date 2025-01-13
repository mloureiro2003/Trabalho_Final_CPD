class Monster:
    
    def __init__(self, name, size, type, alignment, AC, HP, CR, source)  -> None:
        """
        Inicializa um monstro com diversos atributos.

        Atributos:
        name (str): O nome do monstro, truncado para 32 caracteres.
        size (str): O tamanho do monstro, truncado para 10 caracteres.
        type (str): O tipo do monstro, truncado para 40 caracteres.
        alignment (str): O alinhamento do monstro, truncado para 11 caracteres.
        AC: A classe de armadura (Armor Class) do monstro (pode ser str ou int).
        HP: Os pontos de vida (Hit Points) do monstro (pode ser str ou int).
        CR: O nível de desafio (Challenge Rating) do monstro (pode ser str ou int).
        source (str): A fonte onde o monstro é encontrado, truncada para 30 caracteres.
        """
        self.name = name[:32]
        self.size = size[:10]
        self.type = type[:40]
        self.alignment = alignment[:11]
        self.AC = AC
        self.HP = HP
        self.CR = CR
        self.source = source[:30]

class Monster_Name:
    def __init__(self, attribute, index) -> None:
        """
        Inicialza o nome de um monstro e seu índice associado.

        Atributos:
        attribute (str): O nome do monstro, truncado para 32 caracteres.
        index (int): O índice associado ao monstro.
        """
        self.attribute = attribute[:32]
        self.index = index

class Monster_Attribute:
    def __init__(self, attribute, index) -> None:
        """
        Inicializa  um atributo de monstro e uma lista de índices associados a ele.

        Atributos:
        attribute: O valor do atributo (o tipo pode variar).
        indexes (list): Uma lista de índices (int) associados a este atributo.
        """
        self.attribute = attribute
        self.indexes = [index]

    def get_index_string(self) -> str:
        """
        Converte a lista de índices em uma string separada por vírgulas.

        Retorna:
            str: Uma string contendo todos os índices separados por vírgulas.
        """
        return ",".join(map(str, self.indexes))