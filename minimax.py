
class MinimaxSearch:
    """
    Classic minimax algorithm (Knuth & Moore, 1975).
 
    The maximizing player tries to maximise the score; the minimizing player
    tries to minimise it.  The algorithm recurses to terminal nodes (no moves
    left or an explicit depth limit) and backs up scores.
 
    Time complexity : O(b^d)   – b = branching factor, d = depth
    Space complexity: O(b*d)   – call-stack depth
    """
 
    def __init__(self, max_depth: int = None):
        """
        Parameters
        ----------
        max_depth : int or None
            Maximum search depth.  None means search until terminal nodes.
        """
        self.max_depth = max_depth
        self.nodes_explored = 0   # diagnostic counter
 
    def search(self, state, depth: int = 0) -> tuple:
        """
        Return (best_score, best_move) from the current state.
 
        Parameters
        ----------
        state : GameState
        depth : int  – current recursion depth (starts at 0)
 
        Returns
        -------
        (float, move)  – best score and the move that achieves it
        """
        self.nodes_explored += 1
 
        # ── base case ──────────────────────────────────────────────────────
        if state.is_terminal() or (self.max_depth is not None and depth >= self.max_depth):
            return state.get_result(1), None   # score from maximizer's view
 
        moves = state.get_legal_moves()
 
        if state.current_player == 1:      # MAXIMIZER
            best_score = -math.inf
            best_move = None
            for move in moves:
                child = state.make_move(move)
                score, _ = self.search(child, depth + 1)
                if score > best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move
 
        else:                              # MINIMIZER
            best_score = math.inf
            best_move = None
            for move in moves:
                child = state.make_move(move)
                score, _ = self.search(child, depth + 1)
                if score < best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move
 
    def reset_stats(self):
        self.nodes_explored = 0
