import sys
sys.path.append('.')
sys.path.append('./Testing')
from test_bfs_detailed import TestWordAPI
from Search_Algorithm.bfs import BFSSolver

# Test với 3 words
test_words = ['SLATE', 'CRANE', 'RAISE']

for word in test_words:
    print(f"\n{'='*50}")
    print(f"Testing: {word}")
    print('='*50)
    
    api = TestWordAPI(5, word)
    solver = BFSSolver(api)
    result = solver.solve(board_state=[])
    
    stats = solver.get_stats()
    print(f"\n📊 Results:")
    print(f"  Success: {result}")
    print(f"  Expanded Nodes: {solver.expanded_nodes}")
    print(f"  Memory Usage: {stats['Memory Usage']}")
    print(f"  Time: {stats['Time']}")

