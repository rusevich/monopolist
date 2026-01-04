from dataclasses import dataclass, field
from typing import Optional, Set, Dict, Tuple, Any

@dataclass
class Player:
    player_color: str
    turn_order: int
    money: int = 1500
    position: int = 0
    consecutive_doubles: int = 0 
    in_jail: bool = False
    got_sent_to_jail: bool = False
    is_bankrupt: bool = False

    properties: Set[int] = field(default_factory=set)
    houses: Dict[int, int] = field(default_factory=dict)
    mortgaged: Set[int] = field(default_factory=set)  
    get_out_of_jail_card: int = 0
    last_roll: Optional[Tuple[int, int]] = None
