import sys
from .CBot-API import *

class CardMessage(list):
  def __init__(self, *cards: Card):
      super().__init__()
      self.extend(cards)

  def __iter__(self):
      return iter([_get_repr(i) for i in self[:]])
