from models.concepts.CollectionOfRessources import CollectionOfRessources


class XMLCollection(CollectionOfRessources):

    def __init__(self, id:int, documents:dict):
        super().__init__(id, documents)