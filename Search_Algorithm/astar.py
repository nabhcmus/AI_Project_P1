import time
import os
import pickle
import sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class AStarSolver:
    DATA_FILE = "static_entropy.pkl"
    TREE_FILE = "full_turn2_tree.pkl"
    
    _cache_data = None
    _cache_tree = None

    def __init__(self, api):
        self.api = api
        self.target = getattr(api, 'word', None)
        if self.target: self.target = self.target.upper()
        
        if AStarSolver._cache_data is None:
            paths = [self.DATA_FILE, os.path.join("Search_Algorithm", self.DATA_FILE), os.path.join("..", self.DATA_FILE), os.path.join(".", self.DATA_FILE)]
            found = next((p for p in paths if os.path.exists(p)), None)
            if found:
                with open(found, 'rb') as f:
                    AStarSolver._cache_data = pickle.load(f)
            else:
                raise FileNotFoundError("Thiếu static_entropy.pkl")

        if AStarSolver._cache_tree is None:
            paths = [self.TREE_FILE, os.path.join("Search_Algorithm", self.TREE_FILE), os.path.join("..", self.TREE_FILE), os.path.join(".", self.TREE_FILE)]
            found_tree = next((p for p in paths if os.path.exists(p)), None)
            
            if found_tree:
                print(f"⚡ [A* Full Tree] Loading Tree from: {found_tree}")
                t0 = time.time()
                with open(found_tree, 'rb') as f:
                    AStarSolver._cache_tree = pickle.load(f)
                print(f"   Done loading tree in {time.time()-t0:.2f}s")
            else:
                print("⚠️ Không thấy 'full_turn2_tree.pkl'. Sẽ tính toán thủ công (chậm).")

        self.data = AStarSolver._cache_data
        self.full_tree = AStarSolver._cache_tree
        
        self.full_dictionary = self.data["full_dictionary"]
        self.table = self.data["pattern_table"]
        self.w2i = self.data["word_to_idx"]
        self.guesses_history = []
        self.search_time = 0
        self.expanded_nodes = 0
        self.memory_usage = 0

        self.candidates_indices = np.arange(len(self.full_dictionary))

    def calculate_dynamic_entropy(self, guess_idx, candidate_indices):
        patterns = self.table[guess_idx, candidate_indices]
        _, counts = np.unique(patterns, return_counts=True)
        total = len(candidate_indices)
        if total == 0: return 0
        probs = counts / total
        return -np.sum(probs * np.log2(probs))

    def solve(self, board_state=None, max_turns=None):
        start_time = time.time()
        self.guesses_history = []
        self.expanded_nodes = 0
        self.candidates_indices = np.arange(len(self.full_dictionary))

        last_guess_idx = -1
        last_pid = -1
        
        if board_state:
            for guess, feedback_chars in board_state:
                guess = guess.upper()
                if guess not in self.w2i: continue

                p_map = {'G': 2, 'Y': 1, 'X': 0}
                pid = sum(p_map[c] * (3**i) for i, c in enumerate(feedback_chars))
                
                g_idx = self.w2i[guess]
                last_guess_idx = g_idx
                last_pid = pid
                
                row = self.table[g_idx, self.candidates_indices]
                self.candidates_indices = self.candidates_indices[row == pid]

        current_turn = len(board_state) if board_state else 0
        print(f"\n[A* Tree] Candidates left: {len(self.candidates_indices)} | max_turns={max_turns}")

        while True:
            if max_turns is not None and current_turn >= max_turns:
                break
            current_turn += 1
            best_word = ""

            if current_turn == 1:
                best_word = "SALET"

            elif current_turn == 2 and self.full_tree is not None:
                if last_guess_idx in self.full_tree:
                    turn2_options = self.full_tree[last_guess_idx]
                    
                    if last_pid in turn2_options:
                        next_idx = turn2_options[last_pid]
                        best_word = self.full_dictionary[next_idx]
                        print(f"🚀 Tree Lookup: Sau '{self.full_dictionary[last_guess_idx]}' -> Đi '{best_word}'")
            
            if best_word == "":
                if len(self.candidates_indices) <= 2:
                    best_word = self.full_dictionary[self.candidates_indices[0]]
                else:
                    search_space = self.candidates_indices
                    if len(search_space) > 300:
                         import random
                         search_space = np.random.choice(search_space, 300, replace=False)

                    best_score = -1.0
                    best_word_idx = -1
                    
                    for idx in search_space:
                        self.expanded_nodes += 1
                        entropy = self.calculate_dynamic_entropy(idx, self.candidates_indices)
                        if entropy > best_score:
                            best_score = entropy
                            best_word_idx = idx
                    
                    best_word = self.full_dictionary[best_word_idx]

            self.guesses_history.append(best_word)

            if self.target and best_word == self.target: break
            if not self.target: break 

            try:
                t_idx = self.w2i[self.target]
                g_idx = self.w2i[best_word]
                real_pid = self.table[g_idx, t_idx]
                
                last_guess_idx = g_idx
                last_pid = real_pid
                
                row = self.table[g_idx, self.candidates_indices]
                self.candidates_indices = self.candidates_indices[row == real_pid]
            except: break
            if len(self.candidates_indices) == 0: break

        self.search_time = time.time() - start_time
        
        # Calculate memory from data structures
        mem_candidates = self.candidates_indices.nbytes  # NumPy array
        mem_history = sys.getsizeof(self.guesses_history) + sum(sys.getsizeof(w) for w in self.guesses_history)
        self.memory_usage = mem_candidates + mem_history
        
        return self.guesses_history

    def _calculate_feedback(self, guess, secret):
        feedback = [''] * 5
        s_list = list(secret); g_list = list(guess)
        for i in range(5):
            if g_list[i] == s_list[i]: feedback[i] = 'G'; s_list[i] = '#'; g_list[i] = '$'
        for i in range(5):
            if g_list[i] == '$': continue
            if g_list[i] in s_list: feedback[i] = 'Y'; s_list[s_list.index(g_list[i])] = '#'
            else: feedback[i] = 'X'
        return tuple([f if f else 'X' for f in feedback])

    def get_stats(self):
        # Format memory intelligently
        if self.memory_usage < 1024:
            mem_str = f"{self.memory_usage} bytes"
        elif self.memory_usage < 1024 * 1024:
            mem_str = f"{self.memory_usage / 1024:.2f} KB"
        else:
            mem_str = f"{self.memory_usage / (1024 * 1024):.2f} MB"
        
        return {
            "target": self.target,
            "steps": len(self.guesses_history),
            "search_time": round(self.search_time, 4),
            "Memory Usage": mem_str,
            "Expanded Nodes": self.expanded_nodes
        }