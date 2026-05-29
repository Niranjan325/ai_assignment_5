class AlphaBetaSearch:
    """
    Alpha-Beta Pruning (Knuth & Moore, 1975; Hart & Edwards, 1961).
 
    Improves Minimax by maintaining two bounds:
      alpha – the best score the maximizer is *guaranteed* so far
      beta  – the best score the minimizer is *guaranteed* so far
 
    When alpha >= beta the remaining siblings cannot influence the result and
    are skipped ("pruned").
 
    In the best case this reduces the effective branching factor from b to √b,
    making it twice as deep for the same computation budget.
 
    Time complexity (best) : O(b^(d/2))
    Time complexity (worst): O(b^d)      – same as minimax if no pruning occurs
    """
 
    def __init__(self, max_depth: int = None):
        self.max_depth = max_depth
        self.nodes_explored = 0
        self.nodes_pruned = 0
 
    def search(self, state, alpha=-math.inf, beta=math.inf, depth=0):
        """
        Return (best_score, best_move) with alpha-beta pruning.
 
        Parameters
        ----------
        state            : GameState
        alpha            : float – lower bound (maximizer's guarantee)
        beta             : float – upper bound (minimizer's guarantee)
        depth            : int   – current depth
        """
        self.nodes_explored += 1
 
        if state.is_terminal() or (self.max_depth is not None and depth >= self.max_depth):
            return state.get_result(1), None
 
        moves = state.get_legal_moves()
        best_move = None
 
        if state.current_player == 1:      # MAXIMIZER
            best_score = -math.inf
            for move in moves:
                child = state.make_move(move)
                score, _ = self.search(child, alpha, beta, depth + 1)
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, best_score)
                if alpha >= beta:          # ── β cutoff (prune)
                    self.nodes_pruned += 1
                    break
            return best_score, best_move
 
        else:                              # MINIMIZER
            best_score = math.inf
            for move in moves:
                child = state.make_move(move)
                score, _ = self.search(child, alpha, beta, depth + 1)
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)
                if alpha >= beta:          # ── α cutoff (prune)
                    self.nodes_pruned += 1
                    break
            return best_score, best_move
 
    def reset_stats(self):
        self.nodes_explored = 0
        self.nodes_pruned = 0
