from dataclasses import dataclass, field
from models.player import Player
from typing import List, Optional

@dataclass
class GameState:
    players: List[Player] = field(default_factory=list)
    current_player_idx: int = 0
    turn_number: int = 0
    last_roll: Optional[tuple] = None