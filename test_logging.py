"""
Script test logging thống nhất cho các thuật toán
"""
import words_api
from Search_Algorithm.bfs import BFSSolver
from Search_Algorithm.dfs import DFSSolver
from Search_Algorithm.astar import AStarSolver
from Search_Algorithm.entropy_best_first import EntropySolver
from Search_Algorithm.stats_logger import StatsLogger

def test_algorithm(algo_name, solver_class, word_api):
    """Test một thuật toán và log kết quả"""
    print(f"\n{'='*60}")
    print(f"Testing {algo_name}")
    print(f"{'='*60}")
    
    try:
        solver = solver_class(word_api)
        
        # Solve với board_state rỗng
        if algo_name == "Entropy":
            # Entropy cần pattern matrix
            try:
                solution = solver.solve(board_state=None, hard_mode=True)
            except FileNotFoundError as e:
                print(f"⚠️  Entropy requires pattern_matrix.npy: {e}")
                return
        else:
            solution = solver.solve(board_state=[])
        
        # Get stats
        stats = solver.get_stats()
        
        # Print stats
        StatsLogger.print_stats(algo_name, stats)
        
        # Get solution path
        if hasattr(solver, 'winning_path'):
            path = solver.winning_path
        elif hasattr(solver, 'full_solution_path'):
            path = solver.full_solution_path
        elif hasattr(solver, 'guesses_history'):
            path = solver.guesses_history
        elif hasattr(solver, 'solution_path'):
            path = solver.solution_path
        else:
            path = solution
        
        # Save to Excel
        StatsLogger.save_run(
            algorithm_name=algo_name,
            stats_dict=stats,
            solution_path=path,
            target_word=word_api.word.upper(),
            word_length=5
        )
        
        print(f"✅ {algo_name} completed successfully")
        
    except Exception as e:
        print(f"❌ Error in {algo_name}: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Test tất cả 4 thuật toán"""
    # Khởi tạo word API với từ 5 chữ cái
    word_api = words_api.Words(5)
    
    print(f"\n🎯 Target Word: {word_api.word.upper()}")
    print(f"📊 Testing all algorithms and logging to Excel...")
    
    # Test từng thuật toán
    test_algorithm("BFS", BFSSolver, word_api)
    test_algorithm("DFS", DFSSolver, word_api)
    test_algorithm("A*", AStarSolver, word_api)
    test_algorithm("Entropy", EntropySolver, word_api)
    
    print(f"\n{'='*60}")
    print("✅ All tests completed!")
    print(f"📁 Results saved to: Experiments_History.xlsx")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
