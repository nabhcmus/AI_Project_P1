# test_dfs.py - File test đánh giá thuật toán DFS
"""
File này dùng để test và so sánh hiệu suất của thuật toán DFS
với goal word được set sẵn, không ảnh hưởng đến code chính.
"""

import time
import sys
import os

# Thêm thư mục gốc vào path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from words_api import Words
from Search_Algorithm.dfs import DFSSolver


class TestWordAPI:
    """
    Wrapper class để set goal word cố định cho testing.
    """
    def __init__(self, word_size, fixed_goal=None):
        self.real_api = Words(word_size)
        self.words_list = self.real_api.words_list
        self.size = word_size
        
        # Set goal word cố định
        if fixed_goal:
            if fixed_goal.upper() in self.words_list:
                self.word = fixed_goal.upper()
            else:
                print(f"Warning: '{fixed_goal}' không có trong từ điển!")
                self.word = self.real_api.word
        else:
            self.word = self.real_api.word
        
        print(f"Goal word đã set: {self.word}")
    
    def is_at_right_position(self, i, char):
        if self.word[i] == char:
            return True
        return False
    
    def is_in_word(self, char):
        if char in self.word:
            return True
        return False
    
    def is_valid_guess(self, guess):
        if guess == self.word:
            return True
        return False
    
    def is_in_dictionary(self, word):
        return word in self.words_list


def run_single_test(goal_word, word_size=5, board_state=None, start_word=None):
    """
    Chạy test với một goal word cụ thể.
    
    Args:
        goal_word: Từ mục tiêu (goal) cần tìm
        word_size: Độ dài từ (3, 4, 5, hoặc 6)
        board_state: Trạng thái đã đoán trước (nếu có)
        start_word: Từ bắt đầu cố định (nếu có). Nếu None, DFS sẽ random từ MASTER_START_WORDS.
    
    Returns:
        dict: Kết quả test với các metrics
    """
    print("\n" + "="*60)
    print(f"Testing DFS với goal word: {goal_word.upper()}")
    if start_word:
        print(f"Start word: {start_word.upper()}")
    print("="*60)
    
    # Khởi tạo API với goal word cố định
    word_api = TestWordAPI(word_size, goal_word)
    
    # Tạo DFS solver
    solver = DFSSolver(word_api)
    
    # Nếu có start_word và không có board_state, tạo board_state với start_word
    if start_word and not board_state:
        # Tính feedback cho start_word
        feedback = solver._calculate_feedback(start_word.upper(), goal_word.upper())
        board_state = [(start_word.upper(), list(feedback))]
        print(f"Sử dụng start word: {start_word.upper()} → feedback: {feedback}")
    
    # Chạy solver
    start_time = time.time()
    solution = solver.solve(board_state if board_state else [])
    end_time = time.time()
    
    # Lấy statistics
    stats = solver.get_stats()
    
    # Thêm thông tin bổ sung
    result = {
        'goal_word': goal_word.upper(),
        'start_word': start_word.upper() if start_word else "Random",
        'solution_length': len(solution) + (1 if start_word else 0),  # +1 nếu có start_word
        'execution_time': round(end_time - start_time, 4),
        'solution_path': solution,
        'expanded_nodes': solver.expanded_nodes,
        'time': stats['Time']
    }
    
    if start_word:
        result['full_solution'] = [start_word.upper()] + solution
    else:
        result['full_solution'] = solution
    
    # In kết quả
    if start_word:
        print(f"\n✅ Full solution: {result['full_solution']}")
        print(f"   (Start: {start_word.upper()} + DFS: {solution})")
    else:
        print(f"\n✅ Solution found: {solution}")
    print(f"📊 Statistics:")
    print(f"  - Goal word: {result['goal_word']}")
    print(f"  - Start word: {result['start_word']}")
    print(f"  - Total steps: {result['solution_length']}")
    print(f"  - Expanded nodes: {result['expanded_nodes']}")
    print(f"  - Execution time: {result['execution_time']}s")
    
    return result


def compare_multiple_goals(goal_words, word_size=5, start_word=None):
    """
    So sánh DFS trên nhiều goal words khác nhau.
    
    Args:
        goal_words: Danh sách các goal words cần test
        word_size: Độ dài từ
        start_word: Từ bắt đầu cố định cho tất cả tests (nếu có)
    
    Returns:
        list: Danh sách kết quả cho từng goal
    """
    results = []
    
    print("\n" + "█"*60)
    print("🔬 BẮT ĐẦU SO SÁNH NHIỀU GOAL WORDS")
    if start_word:
        print(f"Start word cố định: {start_word.upper()}")
    print("█"*60)
    
    for goal in goal_words:
        result = run_single_test(goal, word_size, start_word=start_word)
        results.append(result)
    
    # Tổng kết so sánh
    print("\n" + "█"*60)
    print("📊 TỔNG KẾT SO SÁNH")
    print("█"*60)
    print(f"{'Goal':<10} {'Steps':<8} {'Nodes':<10} {'Time':<10}")
    print("-"*60)
    
    for r in results:
        print(f"{r['goal_word']:<10} {r['solution_length']:<8} "
              f"{r['expanded_nodes']:<10} {r['execution_time']:<10}s")
    
    # Tính trung bình
    avg_steps = sum(r['solution_length'] for r in results) / len(results)
    avg_nodes = sum(r['expanded_nodes'] for r in results) / len(results)
    avg_time = sum(r['execution_time'] for r in results) / len(results)
    
    print("-"*60)
    print(f"{'AVERAGE':<10} {avg_steps:<8.2f} {avg_nodes:<10.2f} "
          f"{avg_time:<10.4f}s")
    
    return results


def test_with_board_state(goal_word, board_state):
    """
    Test DFS với board_state có sẵn (user đã đoán trước).
    
    Args:
        goal_word: Từ mục tiêu
        board_state: Danh sách [(guess, feedback), ...]
    
    Example:
        board_state = [
            ("SLATE", ['G', 'X', 'A', 'X', 'E']),
            ("STALE", ['G', 'X', 'A', 'X', 'E'])
        ]
    """
    print("\n" + "="*60)
    print(f"Testing DFS với board_state có sẵn")
    print(f"Goal: {goal_word.upper()}")
    print(f"Board state: {len(board_state)} guesses")
    print("="*60)
    
    for i, (guess, feedback) in enumerate(board_state, 1):
        print(f"  {i}. {guess} → {feedback}")
    
    result = run_single_test(goal_word, board_state=board_state)
    return result


def compare_dfs_vs_ucs(goal_word, word_size=5):
    """
    So sánh DFS với UCS trên cùng một goal word.
    
    Args:
        goal_word: Từ mục tiêu
        word_size: Độ dài từ
    """
    from Search_Algorithm.ucs import UCSSolver
    
    print("\n" + "⚔️"*30)
    print(f"SO SÁNH DFS vs UCS - Goal: {goal_word.upper()}")
    print("⚔️"*60)
    
    # Test DFS
    print("\n🔵 Testing DFS...")
    word_api_dfs = TestWordAPI(word_size, goal_word)
    solver_dfs = DFSSolver(word_api_dfs)
    
    start_dfs = time.time()
    solution_dfs = solver_dfs.solve([])
    time_dfs = time.time() - start_dfs
    
    # Test UCS
    print("\n🟢 Testing UCS...")
    word_api_ucs = TestWordAPI(word_size, goal_word)
    solver_ucs = UCSSolver(word_api_ucs)
    
    start_ucs = time.time()
    solution_ucs = solver_ucs.solve(None)
    time_ucs = time.time() - start_ucs
    
    # So sánh kết quả
    print("\n" + "="*60)
    print("📊 KẾT QUẢ SO SÁNH")
    print("="*60)
    
    print(f"\n{'Metric':<25} {'DFS':<20} {'UCS':<20}")
    print("-"*60)
    print(f"{'Solution length':<25} {len(solution_dfs):<20} {len(solution_ucs):<20}")
    print(f"{'Expanded nodes':<25} {solver_dfs.expanded_nodes:<20} {len(solver_ucs.expanded_nodes_list):<20}")
    print(f"{'Execution time':<25} {time_dfs:<20.4f} {time_ucs:<20.4f}")
    
    print(f"\n🔵 DFS Solution: {solution_dfs}")
    print(f"🟢 UCS Solution: {solution_ucs}")
    
    # Tìm thuật toán tốt hơn
    print("\n" + "="*60)
    if len(solution_dfs) < len(solution_ucs):
        print("🏆 Winner: DFS (ít bước hơn)")
    elif len(solution_dfs) > len(solution_ucs):
        print("🏆 Winner: UCS (ít bước hơn)")
    else:
        if time_dfs < time_ucs:
            print("🏆 Winner: DFS (cùng số bước nhưng nhanh hơn)")
        elif time_dfs > time_ucs:
            print("🏆 Winner: UCS (cùng số bước nhưng nhanh hơn)")
        else:
            print("🤝 Hòa: Cả hai đều cho kết quả tương đương")
    print("="*60)
    
    return {
        'dfs': {'solution': solution_dfs, 'nodes': solver_dfs.expanded_nodes, 'time': time_dfs},
        'ucs': {'solution': solution_ucs, 'nodes': len(solver_ucs.expanded_nodes_list), 'time': time_ucs}
    }


# ============================================================================
# EXAMPLES - Các ví dụ sử dụng
# ============================================================================

if __name__ == "__main__":
    print("\n🎮 WORDLE DFS TESTING FRAMEWORK\n")
    
    # -------------------------------------------------------------------------
    # Example 1: Test với goal word CÓ start word cố định
    # -------------------------------------------------------------------------
    print("📝 Example 1: Test với goal và start word cố định")
    result1 = run_single_test("HUSOS", start_word="SLATE")
    
    # # -------------------------------------------------------------------------
    # # Example 2: Test với goal word KHÔNG có start word (random)
    # # -------------------------------------------------------------------------
    # print("\n📝 Example 2: Test với goal word, start word random")
    # result2 = run_single_test("CRANE")
    
    # # -------------------------------------------------------------------------
    # # Example 3: So sánh nhiều goal words với CÙNG start word
    # # -------------------------------------------------------------------------
    # print("\n📝 Example 3: So sánh nhiều goals với start word cố định")
    # test_goals = ["SHAKE", "CRANE", "STALE", "BREAD", "SWIMS"]
    # results = compare_multiple_goals(test_goals, start_word="SLATE")
    
    # # -------------------------------------------------------------------------
    # # Example 4: So sánh nhiều goal words với start word RANDOM
    # # -------------------------------------------------------------------------
    # print("\n📝 Example 4: So sánh nhiều goals với start word random")
    # results2 = compare_multiple_goals(test_goals)
    
    # # -------------------------------------------------------------------------
    # # Example 5: Test với board_state (user đã đoán trước)
    # # -------------------------------------------------------------------------
    # print("\n📝 Example 5: Test với board_state có sẵn")
    
    # # Giả sử user đã đoán SLATE
    # # Goal là SHAKE → feedback sẽ là:
    # # S-Green, L-Gray, A-Green, T-Gray, E-Green
    # board_state_example = [
    #     ("SLATE", ['G', 'X', 'G', 'X', 'G'])
    # ]
    # result5 = test_with_board_state("SHAKE", board_state_example)
    
    # # -------------------------------------------------------------------------
    # # Example 6: So sánh DFS vs UCS với cùng start word
    # # -------------------------------------------------------------------------
    # print("\n📝 Example 6: So sánh DFS vs UCS")
    # comparison = compare_dfs_vs_ucs("BRAIN")
    
    # # -------------------------------------------------------------------------
    # # Example 7: Tự tạo test case của bạn
    # # -------------------------------------------------------------------------
    # print("\n📝 Example 7: Custom test case")
    
    # # Test với goal và start word tùy chỉnh
    # my_goal = "AUDIO"
    # my_start = "ADIEU"
    # my_result = run_single_test(my_goal, start_word=my_start)
    
    print("\n✅ Testing hoàn tất!")
