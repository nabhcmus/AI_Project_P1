import pickle
import os
import numpy as np
import math
import sys
import time
from multiprocessing import Pool, cpu_count
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATA_FILE = "static_entropy.pkl"
TREE_FILE = "full_turn2_tree.pkl"
shared_table = None
shared_full_dict = None
shared_w2i = None

def init_worker(data_pack):
    global shared_table, shared_full_dict, shared_w2i
    shared_table = data_pack["pattern_table"]
    shared_full_dict = data_pack["full_dictionary"]
    shared_w2i = data_pack["word_to_idx"]
def calculate_best_next_move(args):
    start_word_idx, all_candidate_indices = args
    patterns = shared_table[start_word_idx, all_candidate_indices]
    unique_patterns, inverse_indices = np.unique(patterns, return_inverse=True)
    result_map = {}
    for i, pid in enumerate(unique_patterns):
        subset_indices = all_candidate_indices[inverse_indices == i]
        if len(subset_indices) == 0: continue
        if len(subset_indices) == 1:
            best_idx = subset_indices[0]
            result_map[pid] = best_idx
            continue
        best_score = -1.0
        best_idx = -1
        for guess_idx in subset_indices:
            sub_patterns = shared_table[guess_idx, subset_indices]
            _, counts = np.unique(sub_patterns, return_counts=True)
            total = len(subset_indices)
            probs = counts / total
            entropy = -np.sum(probs * np.log2(probs))
            if entropy > best_score:
                best_score = entropy
                best_idx = guess_idx
        result_map[pid] = best_idx
    return (start_word_idx, result_map)

def generate_full_tree():
    print("Loading pattern table...")
    paths = [DATA_FILE, os.path.join("Search_Algorithm", DATA_FILE), os.path.join("..", DATA_FILE)]
    found = next((p for p in paths if os.path.exists(p)), None)
    if not found: raise FileNotFoundError("Missing static_entropy.pkl")
    
    with open(found, 'rb') as f:
        data = pickle.load(f)
    
    full_dict = data["full_dictionary"]
    all_candidates = np.arange(len(full_dict))
    
    print(f"🚀 Starting parallel computation on {cpu_count()} CPU cores.")
    print(f"Workload: {len(full_dict)} starting words. Go grab a coffee...")
    
    t0 = time.time()
    tasks = [(i, all_candidates) for i in range(len(full_dict))]
    full_tree = {}
    with Pool(processes=cpu_count(), initializer=init_worker, initargs=(data,)) as pool:
        results = pool.imap_unordered(calculate_best_next_move, tasks, chunksize=10)
        count = 0
        total = len(full_dict)
        for res in results:
            start_idx, map_data = res
            full_tree[start_idx] = map_data
            count += 1
            if count % 100 == 0:
                elapsed = time.time() - t0
                rate = count / elapsed
                remain = (total - count) / rate
                print(f"Progress: {count}/{total} ({count/total*100:.1f}%) - ETA: {remain/60:.1f} min", end='\r')

    print(f"\n✅ Completed computation in {(time.time()-t0)/60:.2f} minutes.")
    
    # Save file
    print("Saving the giant decision tree file...")
    with open(TREE_FILE, "wb") as f:
        pickle.dump(full_tree, f)
    print(f"Done! File saved at {TREE_FILE}")

if __name__ == "__main__":
    generate_full_tree()