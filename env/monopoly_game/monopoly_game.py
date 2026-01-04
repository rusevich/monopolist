from models.game_state import GameState
from models.player import Player
from monopoly_spec import MonopolySpec

import random
import operator

JAIL_POSITION = 10
GO_TO_JAIL_POSITION = 30
CONSECUTIVE_DOUBLE_LIMIT = 2
BOARD_SIZE = 40

class MonopolyGame:
    """
    This class represents a full game of monopoly. 
    """

    def __init__(self, players_count=2) -> None:
        assert 1 <= players_count <= 8
        self.state = GameState()
        colors = ["red", "blue", "green", "yellow", "purple", "black", "brown", "pink"]
        random.shuffle(colors)
        for pid in range(players_count):
            self.state.players.append(Player(player_color=colors[pid], turn_order=pid))

    def start_game(self) -> None:
        self.state.current_player_idx = 0
        self.state.turn_number = 0

    def prepare_turn(self) -> None:
        if self.is_game_over():
            return

        current_player = self.state.players[self.state.current_player_idx]
        
        if current_player.in_jail:
            return

        # player updates
        die1, die2 = self._roll_dice()
        if die1 == die2:
            current_player.consecutive_doubles += 1
        else:
            current_player.consecutive_doubles = 0

        is_double_limit = current_player.consecutive_doubles >= CONSECUTIVE_DOUBLE_LIMIT
        is_go_jail_position = (current_player.position + die1 + die2) == GO_TO_JAIL_POSITION

        if is_go_jail_position or is_double_limit: 
            self._send_to_jail(self.state.current_player_idx)
        else:
            current_player.position = (current_player.position + die1 + die2) % BOARD_SIZE  

        # game state updates
        self.state.turn_number += 1
        self.state.last_roll = (die1, die2)

        # TODO pay for entrance, other automatic action  

    def apply_action(self, action=None) -> None:
        current_player = self.state.players[self.state.current_player_idx]
        
        if current_player.got_sent_to_jail:
            current_player.got_sent_to_jail = False
            self._set_next_current_player_idx()
            return

        # TODO applying action

        self._set_next_current_player_idx()

    def is_game_over(self) -> bool:
        return all(p.is_bankrupt for p in self.state.players)

    def _roll_dice(self) -> tuple[int, int]:
        return random.randint(1, 6), random.randint(1, 6)

    def _set_next_current_player_idx(self) -> None:
        pidx = self.state.current_player_idx
        is_double = self.state.last_roll and (self.state.last_roll[0] == self.state.last_roll[1])
        if is_double and self.state.players[pidx].is_bankrupt is False:
            return

        for idx in list(range(pidx + 1, len(self.state.players))) + list(range(pidx)):
            if self.state.players[idx].is_bankrupt is False:
                self.state.current_player_idx = idx
                return

    def _send_to_jail(self, pid) -> None:
        player = self.state.players[pid]
        player.in_jail = True
        player.got_sent_to_jail = True

    def p_print(self):
        print("===============================")
        print(f"{self.state.turn_number}. turn")
        print(f"{self.state.players[self.state.current_player_idx].player_color} last roll: {self.state.last_roll}")
        print(f"{self.state.players[0].player_color} - {self.state.players[0].position}")
        print(f"{self.state.players[1].player_color} - {self.state.players[1].position}")
        print()


if __name__ == '__main__':
    m = MonopolyGame(2)
    m.start_game()
    while True:
        input()
        m.prepare_turn()
        m.p_print()
        m.apply_action()