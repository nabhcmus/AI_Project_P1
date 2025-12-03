# Testing Framework - Hướng Dẫn Sử Dụng

## Tổng Quan

Framework này cung cấp các công cụ để test và đánh giá hiệu suất của 4 thuật toán Wordle:
- **BFS** (Breadth-First Search)
- **DFS** (Depth-First Search)  
- **A*** (A-Star Search)
- **Entropy** (Entropy-based Search)

## File Structure

```
Testing/
├── test_full_algorithm.py      # Test toàn diện 1000 lần/thuật toán
├── visualize_results.py         # Tạo biểu đồ phân tích
├── test_bfs.py                  # Test riêng BFS
├── test_dfs.py                  # Test riêng DFS
├── test_astar.py                # Test riêng A*
└── TESTING_README.md            # File này
```

## 1. Test Toàn Diện (test_full_algorithm.py)

### Mô tả
- Test cả 4 thuật toán với **1000 lần chạy** mỗi thuật toán
- Thu thập metrics chi tiết: time, nodes, guesses
- Lưu kết quả ra CSV và JSON để dễ phân tích

### Cách chạy

```bash
cd Testing
python test_full_algorithm.py
```

### Output

Sau khi chạy, tất cả kết quả sẽ được lưu trong thư mục `test_results/`:

```
test_results/
├── bfs_20251203_193045.csv              # CSV data cho BFS
├── bfs_20251203_193045_detailed.json    # JSON chi tiết BFS
├── dfs_20251203_193045.csv              # CSV data cho DFS
├── dfs_20251203_193045_detailed.json    # JSON chi tiết DFS
├── astar_20251203_193045.csv            # CSV data cho A*
├── astar_20251203_193045_detailed.json  # JSON chi tiết A*
├── entropy_20251203_193045.csv          # CSV data cho Entropy
├── entropy_20251203_193045_detailed.json # JSON chi tiết Entropy
└── summary_20251203_193045.json         # Tổng hợp so sánh
```

### Metrics Thu Thập

Mỗi lần chạy thu thập:
- `target`: Từ cần đoán
- `total_guesses`: Tổng số lần đoán
- `expanded_nodes`: Số nodes đã explore
- `execution_time`: Thời gian chạy (giây)
- `solution_path`: Đường đi tìm được
- `status`: Win/Failed

### Statistics Tính Toán

Cho mỗi thuật toán:
- **Guesses**: Mean, Median, Std, Min, Max, Q25, Q75
- **Time**: Mean, Median, Std, Min, Max, Total
- **Nodes**: Mean, Median, Std, Min, Max
- **Distribution**: Phân bố số lần đoán
- **Success Rate**: Tỷ lệ thành công

### Output Console

```
==================================================
📊 BFS STATISTICS
==================================================

📈 SUCCESS RATE:
   Total tests: 1000
   Successful: 998
   Failed: 2
   Success rate: 99.80%

🎯 GUESSES STATISTICS:
   Mean:   3.24
   Median: 3.00
   Std:    0.85
   Min:    2
   Max:    7
   Q25:    3.00
   Q75:    4.00

⏱️  TIME STATISTICS (seconds):
   Mean:   0.0234s
   Median: 0.0221s
   ...
```

## 2. Visualization (visualize_results.py)

### Mô tả
- Đọc CSV files từ `test_results/`
- Tạo 6 loại biểu đồ để phân tích và so sánh

### Cài đặt thư viện cần thiết

```bash
pip install matplotlib seaborn pandas numpy
```

### Cách chạy

```bash
cd Testing
python visualize_results.py
```

### Biểu Đồ Được Tạo

1. **Guesses Comparison** (Box Plot)
   - So sánh phân bố số lần đoán giữa 4 thuật toán
   - Hiển thị mean, median, quartiles
   
2. **Time Comparison** (Box Plot)
   - So sánh thời gian chạy
   - Xác định thuật toán nhanh nhất
   
3. **Nodes Comparison** (Box Plot)
   - So sánh số nodes expanded
   - Log scale nếu chênh lệch quá lớn
   
4. **Guess Distribution** (Histogram)
   - 4 histograms riêng cho mỗi thuật toán
   - Hiển thị phân bố chi tiết số lần đoán
   
5. **Summary Table**
   - Bảng tổng hợp tất cả metrics
   - Dễ so sánh nhanh giữa các thuật toán
   
6. **Performance Scatter**
   - Scatter plot: Time vs Guesses
   - Xem mối quan hệ giữa tốc độ và chất lượng

### Output

Tất cả biểu đồ được lưu trong thư mục `visualizations/`:

```
visualizations/
├── guesses_comparison_20251203_193045.png
├── time_comparison_20251203_193045.png
├── nodes_comparison_20251203_193045.png
├── guess_distribution_20251203_193045.png
├── summary_table_20251203_193045.png
└── performance_scatter_20251203_193045.png
```

## 3. Test Riêng Từng Thuật Toán

### test_bfs.py

Test riêng BFS với nhiều chế độ:

```bash
python test_bfs.py
```

**Chế độ:**
1. Test 100 lần với random words (thống kê đầy đủ)
2. Test với 1 từ cụ thể
3. Test nhanh 10 lần

**Chia nhóm:**
- Nhóm 1: ≤6 lượt đoán (trong giới hạn Wordle)
- Nhóm 2: >6 lượt đoán

### test_dfs.py

Test riêng DFS:

```bash
python test_dfs.py
```

**Tính năng:**
- Test với goal word cố định
- Test với start word cố định
- Test với board_state có sẵn
- So sánh nhiều goal words

### test_astar.py

Test riêng A*:

```bash
python test_astar.py
```

## 4. Workflow Khuyến Nghị

### Bước 1: Chạy Test Toàn Diện

```bash
cd Testing
python test_full_algorithm.py
```

⏱️ **Thời gian dự kiến:** 20-30 phút (tùy thuộc vào máy)

### Bước 2: Tạo Visualizations

```bash
python visualize_results.py
```

⏱️ **Thời gian:** < 1 phút

### Bước 3: Phân Tích Kết Quả

1. Xem `summary_[timestamp].json` để có overview nhanh
2. Xem các biểu đồ trong `visualizations/` để phân tích chi tiết
3. Mở CSV files trong Excel/Google Sheets để filter/sort

## 5. Ví Dụ Kết Quả

### So Sánh Giữa Các Thuật Toán

```
⚔️  ALGORITHM COMPARISON
====================================================================
Metric                    BFS          DFS          A*           Entropy     
------------------------------------------------------------------------
Success Rate (%)          99.80        98.50        99.90        100.00      
Mean Guesses              3.24         4.87         5.12         5.45        
Mean Time (s)             0.0234       0.0198       0.5234       0.0156      
Mean Expanded Nodes       28.45        5.23         1876.34      342.56      
====================================================================
```

### Nhận Xét Dự Kiến

- **BFS**: Ít guesses nhất, tốc độ trung bình
- **DFS**: Nhanh nhất, nhưng nhiều guesses hơn
- **A***: Chậm nhất (vì tính heuristic), guesses trung bình
- **Entropy**: Tốc độ tốt, guesses ổn định

## 6. Troubleshooting

### Lỗi: "pattern_matrix.npy not found"

Entropy cần file pattern matrix. Nếu chưa có:

```bash
# Tạo matrix (chỉ cần chạy 1 lần)
cd Search_Algorithm
python generate_matrix.py
```

### Lỗi: "No module named matplotlib"

Cài đặt thư viện visualization:

```bash
pip install matplotlib seaborn pandas numpy
```

### Test bị dừng giữa chừng

- Nhấn `Ctrl+C` để dừng
- Kết quả đã test sẽ vẫn được lưu trong `test_results/`
- Có thể resume bằng cách giảm `num_tests` trong code

## 7. Tùy Chỉnh

### Thay đổi số lần test

Sửa trong `test_full_algorithm.py`:

```python
# Dòng 518
results = run_algorithm_tests(algo_name, test_func, num_tests=1000)
# Đổi thành:
results = run_algorithm_tests(algo_name, test_func, num_tests=100)  # Test 100 lần
```

### Test với word_size khác

```python
# Thêm parameter word_size
results = run_algorithm_tests(algo_name, test_func, num_tests=1000, word_size=6)
```

### Test Entropy với Normal Mode

```python
# Trong test_full_algorithm.py, dòng 517
('Entropy', lambda: test_entropy_single(hard_mode=False))  # Normal mode
```

## 8. Tips & Best Practices

### 💡 Tối Ưu Thời Gian Test

- Test 100 lần trước để có overview nhanh (~2-3 phút)
- Test 1000 lần để có kết quả chính xác (~20-30 phút)

### 💡 Phân Tích Hiệu Quả

1. **Xem Summary Table** trước để có big picture
2. **Xem Box Plots** để hiểu phân bố
3. **Xem Histograms** để phân tích chi tiết từng thuật toán
4. **Đọc CSV** để tìm edge cases (từ khó, từ dễ)

### 💡 So Sánh Công Bằng

- Đảm bảo cùng `word_size`
- Đảm bảo cùng word list
- Test cùng số lần cho mỗi thuật toán
- Chạy trên cùng một máy

## 9. Kết Luận

Framework này cung cấp:
- ✅ Test toàn diện với 1000 runs/algorithm
- ✅ Statistics chi tiết và chính xác
- ✅ Visualizations đẹp và dễ hiểu
- ✅ CSV/JSON export để phân tích thêm
- ✅ So sánh công bằng giữa các thuật toán

Kết quả test giúp:
- Đánh giá hiệu suất thực tế của thuật toán
- Tìm điểm mạnh/yếu của mỗi thuật toán
- Chọn thuật toán phù hợp cho use case cụ thể
- Visualize để trình bày/báo cáo

---

**Happy Testing! 🧪**
