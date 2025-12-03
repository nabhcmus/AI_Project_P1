import numpy as np
import math
import time
import os
import sys

class EntropySolver:
    _matrix = None
    _matrix_loaded = False
    _all_words_cached = None
    _word_to_index_cached = None
    def __init__(self, word_api):
        self.word_api = word_api
        if not EntropySolver._matrix_loaded:
            self.all_words = list(word_api.words_list)
            self.word_to_index = {w: i for i, w in enumerate(self.all_words)}
            
            base_dir = os.path.dirname(os.path.abspath(__file__))
            matrix_path = os.path.join(base_dir, "pattern_matrix.npy")
            if not os.path.exists(matrix_path):
                raise FileNotFoundError("Please run generate_matrix.py first!")
            print("Loading Pattern Matrix into RAM... (one-time load)")
            EntropySolver._matrix = np.load(matrix_path)
            EntropySolver._all_words_cached = self.all_words
            EntropySolver._word_to_index_cached = self.word_to_index
            EntropySolver._matrix_loaded = True
            print("Matrix Loaded and Cached.")
        else:
            self.all_words = EntropySolver._all_words_cached
            self.word_to_index = EntropySolver._word_to_index_cached
        self.start_time = 0
        self.total_operations = 0
        self.expanded_nodes = 0
        self.solution_path = []
        self.memory_usage = 0
    @property
    def matrix(self):
        return EntropySolver._matrix
    def _calculate_entropy_vectorized(self, guess_idx, candidate_indices):
        patterns = self.matrix[guess_idx, candidate_indices]
        self.total_operations += len(candidate_indices)
        _, counts = np.unique(patterns, return_counts=True)
        probs = counts / len(candidate_indices)
        entropy = -np.sum(probs * np.log2(probs))
        return entropy
    def solve(self, board_state=None, hard_mode=True):
        self.start_time = time.time()
        self.solution_path = []
        self.expanded_nodes = 0
        current_candidate_indices = np.arange(len(self.all_words))
        if board_state:
            for guess_word, fb_chars in board_state:
                if guess_word not in self.word_to_index: continue
                
                guess_idx = self.word_to_index[guess_word]
                pattern_int = 0
                for c in fb_chars:
                    val = 2 if c == 'G' else (1 if c == 'Y' else 0)
                    pattern_int = pattern_int * 3 + val
                patterns = self.matrix[guess_idx, current_candidate_indices]
                matches = (patterns == pattern_int)
                current_candidate_indices = current_candidate_indices[matches]
                self.solution_path.append(guess_word)
        start_attempt = len(self.solution_path)

        for attempt in range(start_attempt, 100):
            if attempt == 0 and not board_state:
                best_guess = "SOARE"
            elif len(current_candidate_indices) <= 2:
                idx = current_candidate_indices[0]
                best_guess = self.all_words[idx]
            else:
                if hard_mode:
                    search_indices = current_candidate_indices
                else:
                    search_indices = np.arange(len(self.all_words))
                best_guess_idx = -1
                max_entropy = -1.0
                if len(search_indices) > 500:
                    indices_to_check = np.random.choice(search_indices, 200, replace=False)
                else:
                    indices_to_check = search_indices
                for idx in indices_to_check:
                    ent = self._calculate_entropy_vectorized(idx, current_candidate_indices)
                    if ent > max_entropy:
                        max_entropy = ent
                        best_guess_idx = idx
                self.expanded_nodes += 1
                best_guess = self.all_words[best_guess_idx]

            self.solution_path.append(best_guess)
            if self.word_api.is_valid_guess(best_guess):
                break
            real_fb_list = self.word_api.get_feedback(best_guess)
            pattern_int = 0
            for c in real_fb_list:
                val = 2 if c == 'G' else (1 if c == 'Y' else 0)
                pattern_int = pattern_int * 3 + val
            guess_idx = self.word_to_index[best_guess]
            patterns = self.matrix[guess_idx, current_candidate_indices]
            matches = (patterns == pattern_int)
            current_candidate_indices = current_candidate_indices[matches] 
            if len(current_candidate_indices) == 0:
                print("Error: Empty candidates")
                break

        self.end_time = time.time()
        
        # Calculate memory from data structures
        mem_candidates = current_candidate_indices.nbytes  # NumPy array
        mem_path = sys.getsizeof(self.solution_path) + sum(sys.getsizeof(w) for w in self.solution_path)
        self.memory_usage = mem_candidates + mem_path
        
        return self.solution_path

    def get_stats(self):
        """Return statistics follow normal format"""
        # Format memory intelligently
        if self.memory_usage < 1024:
            mem_str = f"{self.memory_usage} bytes"
        elif self.memory_usage < 1024 * 1024:
            mem_str = f"{self.memory_usage / 1024:.2f} KB"
        else:
            mem_str = f"{self.memory_usage / (1024 * 1024):.2f} MB"
        
        return {
            "Time": f"{self.end_time - self.start_time:.4f}s",
            "Expanded Nodes": self.expanded_nodes,
            "Total Guesses": len(self.solution_path),
            "Memory Usage": mem_str,
            "Status": "Win" if (self.solution_path and self.word_api.is_valid_guess(self.solution_path[-1])) else "Failed"
        }