import random

def heuristic(state):
    return state

def alpha_beta(depth, value, alpha, beta, maximizing):

    if depth == 0:
        return heuristic(value)

    if maximizing:

        best = -9999

        for _ in range(2):

            score = alpha_beta(
                depth-1,
                value + random.randint(-5,5),
                alpha,
                beta,
                False
            )

            best = max(best, score)

            alpha = max(alpha, best)

            if beta <= alpha:
                break

        return best

    else:

        best = 9999

        for _ in range(2):

            score = alpha_beta(
                depth-1,
                value + random.randint(-5,5),
                alpha,
                beta,
                True
            )

            best = min(best, score)

            beta = min(beta, best)

            if beta <= alpha:
                break

        return best

print(alpha_beta(4, 10, -9999, 9999, True))
