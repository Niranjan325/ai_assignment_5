class HeuristicAlphaBetaSearch:
    """
    Depth-limited Alpha-Beta with a domain-specific heuristic evaluation.
 
    When the search reaches max_depth without hitting a terminal node, the
    heuristic function estimates the value of the position instead of
    returning an exact result.
 
    The heuristic is passed in as a callable:
        heuristic(state, player) -> float
 
    Move ordering (also supplied by the caller) tries "promising" moves first,
    which dramatically increases the number of α-β cutoffs.
    """
 
    def __init__(self, max_depth: int, heuristic_fn, move_ordering_fn=None):
        """
        Parameters
        ----------
        max_depth       : int      – hard depth limit (required)
        heuristic_fn    : callable – heuristic(state, maximizing_player) → float
        move_ordering_fn: callable – order_moves(moves, state) → sorted list
                          If None, moves are used in their natural order.
        """
        if max_depth <= 0:
            raise ValueError("max_depth must be a positive integer")
        self.max_depth = max_depth
        self.heuristic = heuristic_fn
        self.move_ordering = move_ordering_fn or (lambda moves, _: moves)
        self.nodes_explored = 0
        self.nodes_pruned = 0
        self.heuristic_calls = 0
 
    def search(self, state, alpha=-math.inf, beta=math.inf, depth=0):
        """Return (score, move)."""
        self.nodes_explored += 1
 
        # ── terminal or depth-limit: evaluate position ─────────────────────
        if state.is_terminal():
            return state.get_result(1), None
        if depth >= self.max_depth:
            self.heuristic_calls += 1
            return self.heuristic(state, 1), None
 
        moves = self.move_ordering(state.get_legal_moves(), state)
        best_move = None
 
        if state.current_player == 1:
            best_score = -math.inf
            for move in moves:
                child = state.make_move(move)
                score, _ = self.search(child, alpha, beta, depth + 1)
                if score > best_score:
                    best_score, best_move = score, move
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    self.nodes_pruned += 1
                    break
            return best_score, best_move
        else:
            best_score = math.inf
            for move in moves:
                child = state.make_move(move)
                score, _ = self.search(child, alpha, beta, depth + 1)
                if score < best_score:
                    best_score, best_move = score, move
                beta = min(beta, best_score)
                if alpha >= beta:
                    self.nodes_pruned += 1
                    break
            return best_score, best_move
 
    def reset_stats(self):
        self.nodes_explored = 0
        self.nodes_pruned = 0
        self.heuristic_calls = 0
