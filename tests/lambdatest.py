

def foo(x, heuristic):
    return heuristic(x)

def heur_lambda(y):
    return lambda x: x - y

print(foo(3, heur_lambda(2)))
