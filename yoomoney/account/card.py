class Card:
    def __init__(self,
                 pan_fragment: str = None,
                 type: str = None,
                 id: int = None
                 ):
        self.pan_fragment = pan_fragment
        self.type = type
        self.id = id
