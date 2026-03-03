from dataclasses import dataclass
from typing import Optional, FrozenSet, Tuple

@dataclass(frozen=True)
class PitProps:
    owner: Optional[int]          # 0, 1, or None
    is_scoring: bool              # store-like
    skip_for_player: FrozenSet[int]
    grants_extra_turn_for: FrozenSet[int]  # for option (1), usually same as {owner}