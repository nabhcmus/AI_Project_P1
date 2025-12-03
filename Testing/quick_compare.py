import sys
sys.path.append('.')
from Testing.test_full_algorithm import test_bfs_single, test_dfs_single, test_astar_single, test_entropy_single

# Test all 5 algorithms with the same word
word = 'CRANE'
print(f"\n=== Testing all algorithms with word: {word} ===\n")

bfs = test_bfs_single(word)
dfs = test_dfs_single(word)
astar = test_astar_single(word)
ent_h = test_entropy_single(word, hard_mode=True)
ent_n = test_entropy_single(word, hard_mode=False)

print(f"\n{'='*60}")
print(f"{'Algorithm':<15} {'Guesses':<12} {'Expanded Nodes':<15}")
print(f"{'='*60}")
print(f"{'BFS':<15} {bfs['total_guesses']:<12} {bfs['expanded_nodes']:<15}")
print(f"{'DFS':<15} {dfs['total_guesses']:<12} {dfs['expanded_nodes']:<15}")
print(f"{'A*':<15} {astar['total_guesses']:<12} {astar['expanded_nodes']:<15}")
print(f"{'Entropy-Hard':<15} {ent_h['total_guesses']:<12} {ent_h['expanded_nodes']:<15}")
print(f"{'Entropy-Normal':<15} {ent_n['total_guesses']:<12} {ent_n['expanded_nodes']:<15}")
print(f"{'='*60}\n")
