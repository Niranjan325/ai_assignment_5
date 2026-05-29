import math

def minimax(depth, nodeIndex, maximizingPlayer, values, maxDepth):

    if depth == maxDepth:
        return values[nodeIndex]

    if maximizingPlayer:
        return max(
            minimax(depth + 1, nodeIndex * 2, False, values, maxDepth),
            minimax(depth + 1, nodeIndex * 2 + 1, False, values, maxDepth)
        )
    else:
        return min(
            minimax(depth + 1, nodeIndex * 2, True, values, maxDepth),
            minimax(depth + 1, nodeIndex * 2 + 1, True, values, maxDepth)
        )

values = [3, 5, 6, 9, 1, 2, 0, -1]

result = minimax(0, 0, True, values, 3)

print("Optimal Value =", result)
