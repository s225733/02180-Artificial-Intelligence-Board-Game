"""Configuration for the Kalaha board layout.

This file defines the static structure of the board, such as the number of pits,
the store positions, and helper methods for locating pits and stores.
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class GameConfig:
    """Configuration describing the Kalaha board layout.
    
    Attributes:
        pits_per_side: Number of pits each player has.
    """
    pits_per_side: int

    @property
    def board_size(self) -> int:
        """Return the total number of positions on the board.
        
        Includes:
        - pits for player 0
        - pits for player 1
        - both stores
        """
        return 2 * self.pits_per_side + 2

    @property
    def p0_store(self) -> int:
        """Return the board index of player 0's store."""
        return self.pits_per_side

    @property
    def p1_store(self) -> int:
        """Return the board index of player 1's store."""
        return 2 * self.pits_per_side + 1

    def pits_range(self, player: int) -> range:
        """Return the index range of pits belonging to a player.
        
        Args:
            player: Player number (0 or 1).
            
        Returns:
            Range of indices representing that player's pits.
        """
        if player == 0:
            return range(0, self.pits_per_side)
        return range(self.pits_per_side + 1, 2 * self.pits_per_side + 1)

    def opponent_store(self, player: int) -> int:
        """Return the store index belonging to the opponent."""
        return self.p1_store if player == 0 else self.p0_store

    def store_index(self, player: int) -> int:
        """Return the store index belonging to the given player."""
        return self.p0_store if player == 0 else self.p1_store

    def is_own_pit(self, player: int, idx: int) -> bool:
        """Check whether a board index belongs to the player's pits."""
        return idx in self.pits_range(player)

    def opposite_pit(self, idx: int) -> int:
        """Return the index of the pit opposite to the given pit.
        
        Used in the capture rule of Kalaha.
        """
        return 2 * self.pits_per_side - idx