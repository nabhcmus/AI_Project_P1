import pickle
import math
import time
import numpy as np
import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from words_api import Words

def generate_static_data():
    print("Initializing static data (Static Entropy)...")
    t0 = time.time()

    
    
    
    api = Words(5) 
    full_dictionary = [w.upper() for w in api.words_list] 
    candidates = full_dictionary 
    
    n_guess = len(full_dictionary)
    n_cand = len(candidates)
    
    print(f"Dataset: {n_guess} guesses x {n_cand} answers.")
    
    
    
    word_to_idx = {w: i for i, w in enumerate(full_dictionary)}
    
    print("  > Creating Pattern Table (Numpy)...")
    
    guess_arr = np.array([list(w) for w in full_dictionary], dtype='U1').view(np.int32)
    cand_arr = np.array([list(w) for w in candidates], dtype='U1').view(np.int32)
    
    
    
    table = np.zeros((n_guess, n_cand), dtype=np.uint8)
    
    
    for i, guess in enumerate(full_dictionary):
        
        
        
        g_chars = list(guess)
        for j, secret in enumerate(candidates):
            s_chars = list(secret)
            temp_g = g_chars[:]
            p_vals = [0]*5
            
            
            for k in range(5):
                if temp_g[k] == s_chars[k]:
                    p_vals[k] = 2; s_chars[k] = '
            
            for k in range(5):
                if temp_g[k] == '$': continue
                if temp_g[k] in s_chars:
                    p_vals[k] = 1; s_chars[s_chars.index(temp_g[k])] = '
            
            
            pid = sum(v * (3**k) for k, v in enumerate(p_vals))
            table[i, j] = pid
            
        if i % 1000 == 0: print(f"    Processed {i}/{n_guess} words...")

    print("  > Calculating Static Entropy...")
    entropy_map = {}
    
    
    for i, word in enumerate(full_dictionary):
        row = table[i, :]
        
        _, counts = np.unique(row, return_counts=True)
        
        
        probs = counts / n_cand
        ent = -np.sum(probs * np.log2(probs))
        
        entropy_map[word] = ent

    
    data_pack = {
        "pattern_table": table, 
        "entropy_map": entropy_map,
        "full_dictionary": full_dictionary,
        "word_to_idx": word_to_idx
    }
    
    with open("static_entropy.pkl", "wb") as f:
        pickle.dump(data_pack, f)
        
    print(f"DONE! Saved to 'static_entropy.pkl'. Time: {time.time()-t0:.2f}s")

if __name__ == "__main__":
    generate_static_data()