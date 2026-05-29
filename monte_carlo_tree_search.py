class MCTSNode:
    """
    A single node in the MCTS search tree.
 
    Attributes
    ----------
    state        : GameState
    parent       : MCTSNode or None
    move         : the move that led to this node from its parent
    children     : list[MCTSNode]
    visits       : number of times this node has been visited
    wins         : total reward accumulated through this node
    untried_moves: moves not yet expanded from this node
    """
 
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.wins = 0.0
        self.untried_moves = state.get_legal_moves()
 
    def is_fully_expanded(self) -> bool:
        return len(self.untried_moves) == 0
 
    def is_terminal(self) -> bool:
        return self.state.is_terminal()
 
    def ucb1(self, exploration_constant: float) -> float:
        """
        Upper Confidence Bound 1 (Auer et al., 2002).
 
        UCB1 = wins/visits  +  C * sqrt(ln(parent.visits) / visits)
 
        The first term is exploitation (known good nodes); the second is
        exploration (nodes visited rarely).
        """
        if self.visits == 0:
            return math.inf     # unvisited nodes have infinite priority
        exploitation = self.wins / self.visits
        exploration = exploration_constant * math.sqrt(
            math.log(self.parent.visits) / self.visits
        )
        return exploitation + exploration
 
    def best_child(self, c: float):
        """Return the child with the highest UCB1 score."""
        return max(self.children, key=lambda child: child.ucb1(c))
 
    def expand(self):
        """
        Create a child node for one untried move (chosen randomly).
        Returns the new child node.
        """
        move = self.untried_moves.pop(random.randrange(len(self.untried_moves)))
        child_state = self.state.make_move(move)
        child = MCTSNode(child_state, parent=self, move=move)
        self.children.append(child)
        return child
 
    def rollout(self) -> float:
        """
        Random playout ("simulation") from this node to a terminal state.
        Returns the result from the perspective of the *root player*.
        """
        current = self.state
        while not current.is_terminal():
            moves = current.get_legal_moves()
            current = current.make_move(random.choice(moves))
        return current.get_result(1)   # always from player-1 perspective
 
    def backpropagate(self, result: float):
        """
        Walk back up the tree, updating visit counts and wins.
        The result alternates sign at each level (adversarial game).
        """
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.backpropagate(-result)   # flip sign for opponent
 
 
class MCTSSearch:
    """
    Monte-Carlo Tree Search with UCB1 selection (Coulom 2006; Kocsis & Szepesvári 2006).
 
    Four phases per iteration:
      1. Selection   – traverse tree with UCB1 until an expandable node
      2. Expansion   – add one new child to that node
      3. Simulation  – random rollout to a terminal state
      4. Backpropagation – update wins/visits back to root
 
    Parameters
    ----------
    iterations          : int   – number of MCTS iterations (more = stronger play)
    exploration_constant: float – C in UCB1; √2 is the theoretical default
    time_limit          : float – if set, run until this many seconds elapse
                          (iterations is ignored when time_limit is set)
    """
 
    def __init__(self, iterations: int = 1000, exploration_constant: float = math.sqrt(2),
                 time_limit: float = None):
        self.iterations = iterations
        self.c = exploration_constant
        self.time_limit = time_limit
        self.root = None
 
    def search(self, state):
        """
        Run MCTS from the given state.
 
        Returns
        -------
        (best_score_estimate, best_move)
        """
        self.root = MCTSNode(state)
 
        if self.time_limit:
            deadline = time.time() + self.time_limit
            while time.time() < deadline:
                self._iterate(self.root)
        else:
            for _ in range(self.iterations):
                self._iterate(self.root)
 
        best = self.root.best_child(c=0)   # c=0 → pure exploitation at root
        return best.wins / best.visits, best.move
 
    def _iterate(self, root: MCTSNode):
        """One full selection→expansion→simulation→backpropagation cycle."""
        # 1. Selection
        node = root
        while not node.is_terminal() and node.is_fully_expanded():
            node = node.best_child(self.c)
 
        # 2. Expansion
        if not node.is_terminal() and not node.is_fully_expanded():
            node = node.expand()
 
        # 3. Simulation (rollout)
        result = node.rollout()
 
        # 4. Backpropagation
        node.backpropagate(result)
 
    def get_stats(self) -> dict:
        """Return visit/win statistics for all root children."""
        if self.root is None:
            return {}
        return {
            child.move: {
                "visits": child.visits,
                "wins": round(child.wins, 3),
                "win_rate": round(child.wins / child.visits, 3) if child.visits else 0
            }
            for child in self.root.children
        }
 
