import sys
sys.path.append('..')
from CBot-API import *

class CardMessage(list):
    """
    can be cast to a list, the most outside wrapper for card message
    """

    def __init__(self, *cards: Card):
        super().__init__()
        self.extend(cards)

    def __iter__(self):
        """hack for JSON serialization"""
        return iter([_get_repr(i) for i in self[:]])
