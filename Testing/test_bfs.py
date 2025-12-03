# test_bfs.py - File test đánh giá hiệu suất thuật toán BFS
"""
File test chạy BFS 100 lần và thống kê:
- Average search time, expanded nodes, guesses, max memory nodes
- Chia thống kê theo 2 nhóm:
  + Nhóm 1: Tìm ra kết quả trong ≤6 lượt đoán
  + Nhóm 2: Tìm ra kết quả sau >6 lượt đoán
"""

import time
import sys
import os
import random

# Thêm thư mục gốc vào path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from words_api import Words
from Search_Algorithm.bfs import BFSSolver


class TestWordAPI:
    """Wrapper cho Words API để test với target word cụ thể"""
    def __init__(self, word_size, target_word=None):
        self.real_api = Words(word_size)
        self.words_list = self.real_api.words_list
        self.size = word_size
        
        # Set target word
        if target_word:
            if target_word.upper() in self.words_list:
                self.word = target_word.upper()
            else:
                print(f"Warning: '{target_word}' không có trong từ điển!")
                self.word = self.real_api.word
        else:
            self.word = random.choice(self.words_list).upper()
    
    def is_at_right_position(self, i, char):
        return self.word[i] == char
    
    def is_in_word(self, char):
        return char in self.word
    
    def is_valid_guess(self, guess):
        return guess == self.word
    
    def is_in_dictionary(self, word):
        return word.upper() in self.words_list


def run_single_bfs_test(target_word=None, word_size=5, verbose=False):
    """
    Chạy 1 lần test BFS với target word cụ thể hoặc random
    
    Returns:
        dict: Thống kê bao gồm search_time, expanded_nodes, guesses, target
    """
    # Khởi tạo API
    word_api = TestWordAPI(word_size, target_word)
    
    # Tạo BFS solver
    solver = BFSSolver(word_api)
    
    # Chạy solver với board_state rỗng
    start_time = time.time()
    solution = solver.solve(board_state=[])
    end_time = time.time()
    
    # Lấy statistics
    stats = solver.get_stats()
    
    # Tính toán các metrics
    total_guesses = len(solution)
    execution_time = round(end_time - start_time, 4)
    
    result = {
        'target': word_api.word,
        'total_guesses': total_guesses,
        'expanded_nodes': stats['Expanded Nodes'],
        'execution_time': execution_time,
        'solution': solution
    }
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"Target: {result['target']}")
        print(f"Solution: {solution}")
        print(f"Guesses: {result['total_guesses']}")
        print(f"Expanded nodes: {result['expanded_nodes']}")
        print(f"Time: {result['execution_time']}s")
        print(f"{'='*60}")
    
    return result


def run_100_tests(word_size=5):
    """
    Chạy BFS 100 lần với random target words và thống kê kết quả
    Chia thành 2 nhóm: ≤6 guesses và >6 guesses
    """
    print("\n" + "█"*70)
    print("🔬 BẮT ĐẦU TEST BFS - 100 LẦN CHẠY")
    print("█"*70)
    
    results_within_6 = []  # Nhóm tìm ra trong ≤6 lượt
    results_beyond_6 = []  # Nhóm tìm ra sau >6 lượt
    
    for i in range(1, 101):
        print(f"\rĐang chạy test {i}/100...", end='', flush=True)
        
        stats = run_single_bfs_test(target_word=None, word_size=word_size, verbose=False)
        
        # Phân loại kết quả
        if stats['total_guesses'] <= 6:
            results_within_6.append(stats)
        else:
            results_beyond_6.append(stats)
    
    print("\n\n✅ Hoàn thành 100 lần test!")
    
    # Tính toán thống kê cho nhóm ≤6 guesses
    print("\n" + "="*70)
    print(f"📊 NHÓM 1: TÌM RA KẾT QUẢ TRONG ≤6 LƯỢT ĐOÁN ({len(results_within_6)} cases)")
    print("="*70)
    
    if results_within_6:
        avg_time_6 = sum(r['execution_time'] for r in results_within_6) / len(results_within_6)
        avg_expanded_6 = sum(r['expanded_nodes'] for r in results_within_6) / len(results_within_6)
        avg_guesses_6 = sum(r['total_guesses'] for r in results_within_6) / len(results_within_6)
        
        print(f"Số lượng cases: {len(results_within_6)}")
        print(f"Tỷ lệ: {len(results_within_6)/100*100:.1f}%")
        print(f"Average search time: {avg_time_6:.4f}s")
        print(f"Average expanded nodes: {avg_expanded_6:.2f}")
        print(f"Average guesses: {avg_guesses_6:.2f}")
        
        # Phân bố số lượt đoán
        guess_distribution_6 = {}
        for r in results_within_6:
            g = r['total_guesses']
            guess_distribution_6[g] = guess_distribution_6.get(g, 0) + 1
        
        print("\nPhân bố số lượt đoán:")
        for g in sorted(guess_distribution_6.keys()):
            count = guess_distribution_6[g]
            bar = "█" * (count // 2)
            print(f"  {g} lượt: {count:3d} cases {bar}")
    else:
        print("Không có case nào trong nhóm này!")
    
    # Tính toán thống kê cho nhóm >6 guesses
    print("\n" + "="*70)
    print(f"📊 NHÓM 2: TÌM RA KẾT QUẢ SAU >6 LƯỢT ĐOÁN ({len(results_beyond_6)} cases)")
    print("="*70)
    
    if results_beyond_6:
        avg_time_beyond = sum(r['execution_time'] for r in results_beyond_6) / len(results_beyond_6)
        avg_expanded_beyond = sum(r['expanded_nodes'] for r in results_beyond_6) / len(results_beyond_6)
        avg_guesses_beyond = sum(r['total_guesses'] for r in results_beyond_6) / len(results_beyond_6)
        
        print(f"Số lượng cases: {len(results_beyond_6)}")
        print(f"Tỷ lệ: {len(results_beyond_6)/100*100:.1f}%")
        print(f"Average search time: {avg_time_beyond:.4f}s")
        print(f"Average expanded nodes: {avg_expanded_beyond:.2f}")
        print(f"Average guesses: {avg_guesses_beyond:.2f}")
        
        # Phân bố số lượt đoán
        guess_distribution_beyond = {}
        for r in results_beyond_6:
            g = r['total_guesses']
            guess_distribution_beyond[g] = guess_distribution_beyond.get(g, 0) + 1
        
        print("\nPhân bố số lượt đoán:")
        for g in sorted(guess_distribution_beyond.keys()):
            count = guess_distribution_beyond[g]
            bar = "█" * count
            print(f"  {g} lượt: {count:3d} cases {bar}")
        
        # Hiển thị một số ví dụ từ khó
        print("\n🔴 Top 5 từ khó nhất (nhiều lượt đoán nhất):")
        sorted_beyond = sorted(results_beyond_6, key=lambda x: x['total_guesses'], reverse=True)
        for i, r in enumerate(sorted_beyond[:5], 1):
            print(f"  {i}. {r['target']:6s} - {r['total_guesses']} lượt - "
                  f"{r['expanded_nodes']} nodes - {r['execution_time']:.4f}s")
    else:
        print("Không có case nào trong nhóm này!")
    
    # Tổng kết chung
    print("\n" + "="*70)
    print("📊 TỔNG KẾT CHUNG (100 CASES)")
    print("="*70)
    
    all_results = results_within_6 + results_beyond_6
    
    avg_time_all = sum(r['execution_time'] for r in all_results) / len(all_results)
    avg_expanded_all = sum(r['expanded_nodes'] for r in all_results) / len(all_results)
    avg_guesses_all = sum(r['total_guesses'] for r in all_results) / len(all_results)
    
    print(f"Average search time: {avg_time_all:.4f}s")
    print(f"Average expanded nodes: {avg_expanded_all:.2f}")
    print(f"Average guesses: {avg_guesses_all:.2f}")
    
    min_guesses = min(r['total_guesses'] for r in all_results)
    max_guesses = max(r['total_guesses'] for r in all_results)
    print(f"\nMin guesses: {min_guesses}")
    print(f"Max guesses: {max_guesses}")
    
    return {
        'within_6': results_within_6,
        'beyond_6': results_beyond_6,
        'all': all_results
    }


def test_specific_word(target_word, word_size=5):
    """Test BFS với 1 từ cụ thể"""
    print("\n" + "="*70)
    print(f"🎯 TEST BFS VỚI TỪ CỤ THỂ: {target_word.upper()}")
    print("="*70)
    
    stats = run_single_bfs_test(target_word=target_word, word_size=word_size, verbose=True)
    
    return stats


# ============================================================================
# MAIN - Chạy test
# ============================================================================

if __name__ == "__main__":
    print("\n🎮 BFS ALGORITHM TESTING FRAMEWORK\n")
    
    # Chọn chế độ test
    print("Chọn chế độ test:")
    print("1. Test 100 lần với random words (thống kê đầy đủ)")
    print("2. Test với 1 từ cụ thể")
    print("3. Test nhanh 10 lần")
    
    choice = input("\nNhập lựa chọn (1/2/3): ").strip()
    
    if choice == "1":
        results = run_100_tests(word_size=5)
        
        # Lưu kết quả ra file nếu muốn
        save = input("\nLưu kết quả ra file? (y/n): ").strip().lower()
        if save == 'y':
            import json
            filename = f"bfs_test_results_{int(time.time())}.json"
            
            # Chuyển đổi để có thể serialize
            export_data = {
                'within_6': [
                    {
                        'target': r['target'],
                        'guesses': r['total_guesses'],
                        'expanded_nodes': r['expanded_nodes'],
                        'time': r['execution_time'],
                        'solution': r['solution']
                    } for r in results['within_6']
                ],
                'beyond_6': [
                    {
                        'target': r['target'],
                        'guesses': r['total_guesses'],
                        'expanded_nodes': r['expanded_nodes'],
                        'time': r['execution_time'],
                        'solution': r['solution']
                    } for r in results['beyond_6']
                ]
            }
            
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            print(f"✅ Đã lưu kết quả vào {filename}")
    
    elif choice == "2":
        word = input("Nhập từ cần test (5 chữ cái): ").strip()
        if len(word) == 5:
            test_specific_word(word, word_size=5)
        else:
            print("❌ Từ phải có 5 chữ cái!")
    
    elif choice == "3":
        print("\n🚀 Chạy test nhanh 10 lần...")
        results = []
        for i in range(1, 11):
            print(f"\nTest {i}/10:")
            stats = run_single_bfs_test(verbose=True)
            results.append(stats)
        
        # Thống kê nhanh
        print("\n" + "="*70)
        print("📊 KẾT QUẢ 10 LẦN TEST")
        print("="*70)
        avg_time = sum(r['execution_time'] for r in results) / len(results)
        avg_guesses = sum(r['total_guesses'] for r in results) / len(results)
        print(f"Average time: {avg_time:.4f}s")
        print(f"Average guesses: {avg_guesses:.2f}")
    
    else:
        print("❌ Lựa chọn không hợp lệ!")
    
    print("\n✅ Testing hoàn tất!\n")
