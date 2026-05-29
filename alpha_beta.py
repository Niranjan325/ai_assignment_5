import math

def alphabeta(depth, nodeIndex, maximizingPlayer,
              values, alpha, beta, maxDepth):

    if depth == maxDepth:
        return values[nodeIndex]

    if maximizingPlayer:

        best = -math.inf

        for i in range(2):

            val = alphabeta(
                depth + 1,
                nodeIndex * 2 + i,
                False,
                values,
                alpha,
                beta,
                maxDepth
            )

            best = max(best, val)
            alpha = max(alpha, best)

            if beta <= alpha:
                break

        return best

    else:

        best = math.inf

        for i in range(2):

            val = alphabeta(
                depth + 1,
                nodeIndex * 2 + i,
                True,
                values,
                alpha,
                beta,
                maxDepth
            )

            best = min(best, val)
            beta = min(beta, best)

            if beta <= alpha:
                break

        return best

values = [3,5,6,9,1,2,0,-1]

result = alphabeta(
    0,
    0,
    True,
    values,
    -math.inf,
    math.inf,
    3
)

print("Optimal Value =", result)
