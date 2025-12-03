import pickle
import os
import numpy as np
import math
import sys
from tqdm import tqdm
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

OPENING_WORD = "SALET"
DATA_FILE = "static_entropy.pkl"
TREE_FILE = "turn2_lookup.pkl"

def load_data():
    paths = [DATA_FILE, os.path.join("Search_Algorithm", DATA_FILE), os.path.join("..", DATA_FILE)]
    found = next((p for p in paths if os.path.exists(p)), None)
    if not found: raise FileNotFoundError(f"Missing {DATA_FILE}. Run precompute.py first!")
    
    with open(found, 'rb') as f:
        return pickle.load(f)

def calculate_entropy(table, guess_idx, candidates_indices):
    patterns = table[guess_idx, candidates_indices]
    _, counts = np.unique(patterns, return_counts=True)
    probs = counts / len(candidates_indices)
    return -np.sum(probs * np.log2(probs))

def generate_tree():
    print(f"🚀 Building Decision Tree for turn 2 (Base: {OPENING_WORD})...")
    
    data = load_data()
    table = data["pattern_table"]
    w2i = data["word_to_idx"]
    full_dict = data["full_dictionary"]
    
    
    if OPENING_WORD not in w2i:
        print(f"Error: {OPENING_WORD} not found in dictionary.")
        return
    
    start_idx = w2i[OPENING_WORD]
    all_candidates = np.arange(len(full_dict))
    
    
    turn2_map = {}
    
    
    
    print("⏳ Calculating optimal moves for each feedback pattern...")
    
    for pid in tqdm(range(243)):
        
        
        row = table[start_idx, all_candidates]
        subset_indices = all_candidates[row == pid]
        
        
        if len(subset_indices) == 0:
            continue
            
        
        if len(subset_indices) == 1:
            best_word = full_dict[subset_indices[0]]
            turn2_map[pid] = best_word
            continue
            
        
        
        best_score = -1.0
        best_idx = -1
        
        for idx in subset_indices:
            ent = calculate_entropy(table, idx, subset_indices)
            if ent > best_score:
                best_score = ent
                best_idx = idx
        
        turn2_map[pid] = full_dict[best_idx]
        
    
    with open(TREE_FILE, "wb") as f:
        pickle.dump(turn2_map, f)
        
    print(f"✅ Done! Saved {len(turn2_map)} cases to '{TREE_FILE}'.")

if __name__ == "__main__":
    generate_tree()