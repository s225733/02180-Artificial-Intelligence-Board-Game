"""Minimax AI agent for the Kalaha game.

This module implements the Minimax search algorithm with Alpha-Beta pruning
for selecting optimal actions in the Kalaha board game.

The algorithm explores possible future game states by recursively simulating
legal actions using the core game logic functions. Alpha-Beta pruning is used
to eliminate branches that cannot influence the final decision, improving
the efficiency of the search.

The main function for this module is:

`function(param)`

which returns the best action for the AI player given the current game state
and a search depth.
"""
import numpy as np

from game.logic import (
    legal_moves as actions, 
    apply_move as result, 
    is_terminal, 
    winner,
    score_diff,
)


def utility_eval(state, player):
    """Return the utility of a state from the AI player's perspective."""
    if is_terminal(state):
        w = winner(state)
        
        if w is None:
            return 0
        elif w == player:
            return 1
        else:
            return -1
        
    diff = score_diff(state)
    return diff if player == 0 else -diff


def alpha_beta_minmax(state, depth, alpha, beta, maximizing_player):
    """Run the minimax search with alpha-beta pruning."""
    if is_terminal(state) or depth == 0:
        return utility_eval(state, maximizing_player)

    if state.player == maximizing_player:
        max_eval = -np.inf
        for action in actions(state):
            new_state, _ = result(state, action)
            eval = alpha_beta_minmax(new_state, depth - 1, alpha, beta, maximizing_player)
            max_eval = max(max_eval, eval)
            
            alpha = max(alpha, eval)
            if beta <= alpha:
                break # Beta cut-off
        
        return max_eval
    
    else:
        min_eval = np.inf
        for action in actions(state):
            new_state, _ = result(state, action)
            
            eval = alpha_beta_minmax(new_state, depth - 1, alpha, beta, maximizing_player)
            min_eval = min(min_eval, eval)
            
            beta = min(beta, eval)
            if beta <= alpha:
                break # Alpha cut-off
            
        return min_eval
    

def choose_action(state, depth):
    """Return the best action for the current player."""
    maximizing_player = state.player
    best_action = None
    best_value = -np.inf
    
    for action in actions(state):
        new_state, _ = result(state, action)
        
        value = alpha_beta_minmax(
            new_state,
            depth-1,
            -np.inf,
            np.inf,
            maximizing_player
        )
        
        if value > best_value:
            best_value = value
            best_action = action
            
    return best_action