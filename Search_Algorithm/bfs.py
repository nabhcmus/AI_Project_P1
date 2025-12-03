import time
import random
import os
import sys
from collections import deque

class BFSSolver:
    MASTER_START_WORDS = ['SLATE', 'CRANE', 'SOARE', 'RAISE', 'TRACE']
    
    def __init__(self, word_api):
        self.word_api = word_api
        self.all_words = list(set([w.upper() for w in self.word_api.words_list]))
        self.secret_word = self.word_api.word.upper()
        self.start_time = 0
        self.end_time = 0
        
        self.expanded_nodes = 0
        self.max_queue_size = 0
        
        self.parent_map = {} 
        self.winning_path = []
        self.all_expanded_nodes_log = []
        self.traversed_count = 0

    def _calculate_feedback(self, guess, secret):
        feedback = [''] * len(secret)
        secret_list = list(secret)
        guess_list = list(guess)
        for i in range(len(secret)):
            if guess_list[i] == secret_list[i]:
                feedback[i] = 'G'
                secret_list[i] = '#'
                guess_list[i] = '$'
        for i in range(len(secret)):
            if guess_list[i] != '$' and guess_list[i] in secret_list:
                feedback[i] = 'Y'
                secret_list[secret_list.index(guess_list[i])] = '#'
        for i in range(len(secret)):
            if feedback[i] == '':
                feedback[i] = 'X'
        
        return tuple(feedback)

    def _filter_candidates(self, candidates, guess, feedback):
        new_candidates = []
        for word in candidates:
            if self._calculate_feedback(guess, word) == feedback:
                new_candidates.append(word)
        return new_candidates
    
    def _reconstruct_path(self, current_node):
        path = []
        while current_node is not None:
            path.append(current_node)
            current_node = self.parent_map.get(current_node)
        return path[::-1]

    def solve(self, board_state):
        self.start_time = time.time()
        self.expanded_nodes = 0
        self.max_queue_size = 0
        self.parent_map = {} 
        self.all_expanded_nodes_log = []
        self.memory_usage = 0  # Initialize
        
        print(f"========== BFS START ==========")
        print(f"TARGET WORD: {self.secret_word}")
        candidates = self.all_words.copy()
        last_parent = None
        
        for guess, feedback in board_state:
            guess = guess.upper()
            self.parent_map[guess] = last_parent 
            last_parent = guess
            feedback_tuple = tuple(feedback) if isinstance(feedback, list) else feedback
            candidates = self._filter_candidates(candidates, guess, feedback_tuple)
        queue = deque()
        visited_words = set([w.upper() for w, _ in board_state])

        if not board_state:
            start_word = random.choice(self.MASTER_START_WORDS)
            self.parent_map[start_word] = None
            queue.append(start_word)
            visited_words.add(start_word)
        else:
            for word in candidates[:100]:
                if word not in visited_words:
                    self.parent_map[word] = last_parent 
                    visited_words.add(word)
                    queue.append(word)
        while queue:
            self.max_queue_size = max(self.max_queue_size, len(queue))
            guess = queue.popleft()
            self.expanded_nodes += 1
            self.all_expanded_nodes_log.append(guess)
            print(f"[Expand #{self.expanded_nodes:04d}] Current Node: {guess} | Queue Size: {len(queue)}")
            feedback = self._calculate_feedback(guess, self.secret_word)
            
            if feedback == tuple(['G'] * 5):
                print("=============================")
                print(f">>> BFS SUCCESS FOUND TARGET: {guess}")
                print(f"Total Expanded Nodes: {self.expanded_nodes}")
                self.end_time = time.time()
                
                # Calculate memory from data structures
                queue_mem = sys.getsizeof(queue) + sum(sys.getsizeof(item) for item in queue)
                visited_mem = sys.getsizeof(visited_words) + sum(sys.getsizeof(item) for item in visited_words)
                parent_mem = sys.getsizeof(self.parent_map) + sum(sys.getsizeof(k) + sys.getsizeof(v) for k, v in self.parent_map.items())
                self.memory_usage = queue_mem + visited_mem + parent_mem
                
                self.winning_path = self._reconstruct_path(guess)
                print(f"Correct Solution Path: {' -> '.join(self.winning_path)}")
                
                board_len = len(board_state)
                display_path = self.winning_path[board_len:][:6]
                return display_path
            candidates = self._filter_candidates(candidates, guess, feedback)
            limit_add = 20
            count = 0
            for word in candidates:
                if word not in visited_words:
                    visited_words.add(word)
                    self.parent_map[word] = guess
                    queue.append(word)
                    count += 1
                    if count >= limit_add:
                        break
            if self.expanded_nodes > 10000:
                print("Limit reached!")
                break
        
        self.end_time = time.time()
        
        # Calculate memory from data structures
        queue_mem = sys.getsizeof(queue) + sum(sys.getsizeof(item) for item in queue)
        visited_mem = sys.getsizeof(visited_words) + sum(sys.getsizeof(item) for item in visited_words)
        parent_mem = sys.getsizeof(self.parent_map) + sum(sys.getsizeof(k) + sys.getsizeof(v) for k, v in self.parent_map.items())
        self.memory_usage = queue_mem + visited_mem + parent_mem
        
        print("BFS Failed: Queue Empty.")
        return []

    def get_stats(self):
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
            "Total Guesses": len(self.winning_path),
            "Max Queue": self.max_queue_size,
            "Memory Usage": mem_str,
            "Status": "Win" if self.winning_path and self.winning_path[-1] == self.secret_word else "Failed"
        }
    
    def get_display_path(self, limit=6):
        return self.winning_path[:limit]