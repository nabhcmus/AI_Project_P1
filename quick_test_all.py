import sys
sys.path.append('.')
sys.path.append('./Testing')
from test_dfs_detailed import TestWordAPI
from Search_Algorithm.dfs import DFSSolver
from Search_Algorithm.astar import AStarSolver
from Search_Algorithm.entropy_best_first import EntropySolver

test_words = ['SLATE', 'CRANE']

print("\n" + "="*60)
print("DFS MEMORY TEST")
print("="*60)
for word in test_words:
    api = TestWordAPI(5, word)
    solver = DFSSolver(api)
    result = solver.solve(board_state=[])
    stats = solver.get_stats()
    print(f"{word}: Memory={stats['Memory Usage']}, Nodes={stats['Expanded Nodes']}")

print("\n" + "="*60)
print("A* MEMORY TEST")
print("="*60)
for word in test_words:
    api = TestWordAPI(5, word)
    solver = AStarSolver(api)
    result = solver.solve(board_state=[], max_turns=6)
    stats = solver.get_stats()
    print(f"{word}: Memory={stats['Memory Usage']}, Nodes={stats['Expanded Nodes']}")

print("\n" + "="*60)
print("ENTROPY MEMORY TEST")
print("="*60)
for word in test_words:
    api = TestWordAPI(5, word)
    solver = EntropySolver(api)
    result = solver.solve(board_state=[], hard_mode=True)
    stats = solver.get_stats()
    print(f"{word}: Memory={stats['Memory Usage']}, Nodes={stats['Expanded Nodes']}")
