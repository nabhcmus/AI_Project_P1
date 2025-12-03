# Hệ Thống Statistics Logging Thống Nhất

## Tổng Quan

Tất cả 4 thuật toán (BFS, DFS, A*, Entropy) giờ đây sử dụng một hệ thống logging thống nhất thông qua module `StatsLogger`.

## Các Thay Đổi

### 1. Format Statistics Chuẩn Hóa

Tất cả các solver giờ trả về `get_stats()` với format nhất quán:

```python
{
    "Time": "0.0234s",           # Thời gian chạy
    "Expanded Nodes": 124,       # Số nodes đã explore
    "Total Guesses": 5,          # Tổng số lần đoán
    "Max Queue/Memory": ...,     # Thông tin memory (tuỳ thuật toán)
    "Status": "Win"              # Win/Failed
}
```

### 2. Module `stats_logger.py`

Module mới cung cấp 2 chức năng chính:

#### `StatsLogger.print_stats(algorithm_name, stats_dict)`
In statistics ra console theo format đẹp và chuẩn:

```python
from Search_Algorithm.stats_logger import StatsLogger

solver = BFSSolver(word_api)
solution = solver.solve([])
stats = solver.get_stats()

StatsLogger.print_stats("BFS", stats)
```

#### `StatsLogger.save_run(algorithm_name, stats_dict, solution_path, target_word, word_length)`
Lưu kết quả vào file Excel với lịch sử đầy đủ:

```python
StatsLogger.save_run(
    algorithm_name="BFS",
    stats_dict=stats,
    solution_path=solver.winning_path,
    target_word="GOLFS",
    word_length=5
)
```

### 3. File Excel Output

**File:** `Experiments_History.xlsx`

**Cấu trúc:**
- Header với màu xanh
- Mỗi thuật toán có màu riêng (BFS=xanh lá, DFS=cam, A*=xanh dương, Entropy=vàng)
- Lưu giữ toàn bộ lịch sử (không ghi đè)
- Thêm timestamp cho mỗi lần chạy

**Cột:**
1. Timestamp - Thời điểm chạy
2. Algorithm - Tên thuật toán
3. Target Word - Từ cần đoán
4. Word Length - Độ dài từ
5. Time (s) - Thời gian chạy
6. Expanded Nodes - Số nodes explore
7. Total Guesses - Tổng số lần đoán
8. Solution Path - Đường đi (hiển thị 15 bước đầu)
9. Max Memory - Memory usage
10. Status - Win/Failed

### 4. Cập Nhật Trong `main.py`

Tất cả 4 hàm `solve_*()` giờ sử dụng StatsLogger:

```python
def solve_bfs(self):
    board_state = self._get_board_state()
    solver = BFSSolver(self.word_api)
    solution = solver.solve(board_state)
    
    stats = solver.get_stats()
    StatsLogger.print_stats("BFS", stats)
    StatsLogger.save_run(
        algorithm_name="BFS",
        stats_dict=stats,
        solution_path=solver.winning_path,
        target_word=self.word_api.word.upper(),
        word_length=self.word_size
    )
    self._animate_solution(solution, solver)
```

## Cách Sử Dụng

### Trong GUI (main.py)
Không cần thay đổi gì - tự động log khi nhấn nút "Solve"

### Trong Testing Script
```python
from Search_Algorithm.stats_logger import StatsLogger
import words_api

# Khởi tạo
word_api = words_api.Words(5)
solver = BFSSolver(word_api)

# Chạy
solution = solver.solve([])
stats = solver.get_stats()

# In + Lưu
StatsLogger.print_stats("BFS", stats)
StatsLogger.save_run(
    algorithm_name="BFS",
    stats_dict=stats,
    solution_path=solver.winning_path,
    target_word=word_api.word.upper(),
    word_length=5
)
```

### Test Script Mẫu
Chạy `test_logging.py` để test tất cả 4 thuật toán:

```bash
python test_logging.py
```

## Lợi Ích

✅ **Nhất quán:** Tất cả thuật toán dùng chung format
✅ **Lịch sử:** Lưu giữ toàn bộ lịch sử chạy
✅ **Trực quan:** Excel với màu sắc phân biệt
✅ **Dễ phân tích:** Format chuẩn, dễ compare
✅ **Tự động:** Không cần code logging cho mỗi thuật toán

## File Quan Trọng

- `Search_Algorithm/stats_logger.py` - Module logging chính
- `Experiments_History.xlsx` - File lưu lịch sử
- `test_logging.py` - Script test mẫu
- `check_excel.py` - Script kiểm tra Excel

## Ví Dụ Output Console

```
==================================================
BFS SOLVER STATISTICS
==================================================
Time             : 0.0358s
Expanded Nodes   : 24
Total Guesses    : 3
Max Queue Size   : 22
Status           : Win
==================================================

✅ Statistics saved to Experiments_History.xlsx
```

## Ghi Chú

- File Excel tự động tạo nếu chưa tồn tại
- Lịch sử **không bao giờ** bị ghi đè
- Mỗi lần chạy thêm 1 dòng mới
- Solution path hiển thị tối đa 15 bước (để tránh quá dài)
