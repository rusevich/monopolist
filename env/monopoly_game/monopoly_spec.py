from utils import SingletonMeta
from typing import Set, Dict
import json

with open("data/board.json", "r") as f:
    board_json = json.load(f)

class MonopolySpec(metaclass=SingletonMeta):
    pass
