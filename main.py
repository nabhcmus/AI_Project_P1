import tkinter as tk
from PIL import Image, ImageTk
import ctypes
import words_api
import settings as std
import os
import sqlite3
import time
from tkinter import messagebox
from Search_Algorithm.astar import AStarSolver
from Search_Algorithm.dfs import DFSSolver
from Search_Algorithm.bfs import BFSSolver
from Search_Algorithm.entropy_best_first import EntropySolver
from Search_Algorithm.stats_logger import StatsLogger
ctypes.windll.shcore.SetProcessDpiAwareness(1)
from openpyxl import Workbook, load_workbook
import os

class Wordle:
    FIRST_RIGHT = 10
    BG = "#171717"
    MAX_SCORE = 12

    def __init__(self):
        self.root = tk.Tk()

        self.width = 600
        self.height = 1000
        self.x_co = int(self.root.winfo_screenwidth() / 2) - int(self.width / 2)
        self.y_co = 50

        self.root.geometry(f"{self.width}x{self.height}+{self.x_co}+{self.y_co}")

        self.root.configure(background=self.BG)
        self.root.title("Wordle")
        self.root.wm_iconbitmap('images/icon.ico')

        self.guess = ""
        self.won = False
        self.guess_count = 0
        self.score = 0
        self.word_size = 5
        self.high_score = 0
        self.word_api = None
        self.get_from_db()
        self.solver_has_run = False
        self.setting = Image.open('images/setting.png')
        self.setting = self.setting.resize((40, 40), Image.Resampling.LANCZOS)
        self.setting = ImageTk.PhotoImage(self.setting)

        self.setting_dark = Image.open('images/setting_dark.png')
        self.setting_dark = self.setting_dark.resize((40, 40), Image.Resampling.LANCZOS)
        self.setting_dark = ImageTk.PhotoImage(self.setting_dark)

        label = Image.open('images/head.png')
        # label = label.resize((402, 100), Image.Resampling.LANCZOS)
        label = ImageTk.PhotoImage(label)

        top_frame = tk.Frame(self.root, bg=self.BG)
        top_frame.pack(fill="x")

        sett = tk.Button(top_frame, image=self.setting,command=self.open_setting, bd=0, bg=self.BG, cursor="hand2", activebackground=self.BG)
        sett.pack(side="right")
        sett.bind("<Enter>", self.on_hover)
        sett.bind("<Leave>", self.off_hover)

        head = tk.Label(self.root, image=label, bd=0, bg=self.BG)
        head.pack()

        # word buttons

        main_btn_frame = tk.Frame(self.root, bg=self.BG)
        main_btn_frame.pack(pady=15)

        f1 = tk.Frame(main_btn_frame, bg=self.BG)
        f2 = tk.Frame(main_btn_frame, bg=self.BG)
        f3 = tk.Frame(main_btn_frame, bg=self.BG)
        f4 = tk.Frame(main_btn_frame, bg=self.BG)
        f5 = tk.Frame(main_btn_frame, bg=self.BG)
        f6 = tk.Frame(main_btn_frame, bg=self.BG)
        self.button_frames = [f1, f2, f3, f4, f5, f6]

        self.b_row1 = self.b_row2 = self.b_row3 = self.b_row4 = self.b_row5 = self.b_row6 = []
        self.buttons = []

        self.current_B_row = 0
        self.current_b = 0

        self.show_buttons()

        # keypad buttons

        keyboard_frame = tk.Frame(self.root, bg=self.BG)
        keyboard_frame.pack(pady=5)

        c = 65

        f1 = tk.Frame(keyboard_frame, bg=self.BG)
        f1.pack(side="top", pady=2)
        f2 = tk.Frame(keyboard_frame, bg=self.BG)
        f2.pack(side="top", pady=2)
        f3 = tk.Frame(keyboard_frame, bg=self.BG)
        f3.pack(side="top", pady=2)

        f = [f1, f2, f3]
        step = 6
        self.keypad_buttons = [[], [], []]

        self.keypad_btn_pos = {0: [chr(i) for i in range(65, 71)],
                               1: [chr(i) for i in range(71, 81)],
                               2: [chr(i) for i in range(81, 91)]}

        key_pad_color = "#ff7700"
        index = 0
        for i in range(3):
            for _ in range(step):
                b = tk.Button(f[index], text=chr(c), font="cambria 13 bold", bg=self.BG,
                              fg=key_pad_color, cursor="hand2", padx=3)
                b.pack(side="left", padx=2)
                self.keypad_buttons[i].append(b)
                b.bind("<Button-1>", lambda e: self.key_press(keyboard=e))
                b.bind("<Enter>", lambda e: on_hover(e, "#575656"))
                b.bind("<Leave>", lambda e: off_hover(e, self.BG))
                c += 1
            if i == 0:
                b = tk.Button(f[index], text="Enter", font="cambria 13 bold", bg=self.BG,
                              fg=key_pad_color, cursor="hand2")
                b.pack(side="left", padx=2)
                b.bind("<Button-1>", lambda e: self.key_press(keyboard=e))
                b.bind("<Enter>", lambda e: on_hover(e, "#575656"))
                b.bind("<Leave>", lambda e: off_hover(e, self.BG))
            if i == 0:
                b = tk.Button(f[index], text="←", font="cambria 13 bold", bg=self.BG,
                              fg=key_pad_color, cursor="hand2")
                b.pack(side="left", padx=2)
                b.bind("<Button-1>", lambda e: self.key_press(keyboard=e))
                b.bind("<Enter>", lambda e: on_hover(e, "#575656"))
                b.bind("<Leave>", lambda e: off_hover(e, self.BG))
            index += 1
            step = 10
        solve_frame = tk.Frame(self.root, bg=self.BG)
        solve_frame.pack(pady=15)

        self.solve_button = tk.Button(
            solve_frame,
            text="Solve",
            font="cambria 18 bold",
            fg="#00eaff",
            bg="#202020",
            padx=20,
            pady=5,
            cursor="hand2",
            command=self.solve  # gọi phương thức solve() trong Wordle
        )
        self.solve_button.pack(side="left", padx=10)
        self.new_game_button = tk.Button(
            solve_frame,
            text="New Game",
            font="cambria 18 bold",
            fg="#14f41f",
            bg="#202020",
            padx=20,
            pady=5,
            cursor="hand2",
            command=self.start_new_game
        )
        self.new_game_button.pack(side="right", padx=10)
        self.status_bar = tk.Label(self.root, text=f"Score : {self.score}",font="cambria 10 bold",
                                   anchor="w",padx=10,background="#242424",fg="white")
        self.status_bar.pack(fill='x', side="bottom")

        self.root.bind("<KeyRelease>", self.key_press)

        self.root.mainloop()

    def show_buttons(self):
        if self.buttons:
            for b in self.buttons:
                if b:
                    for i in b:
                        i.destroy()

        self.b_row1 = self.b_row2 = self.b_row3 = self.b_row4 = self.b_row5 = self.b_row6 = []
        self.buttons = []

        self.current_B_row = 0
        self.current_b = 0

        for i in range(6):
            row_btn = []
            self.button_frames[i].pack(pady=4)
            for j in range(self.word_size):
                b = tk.Button(self.button_frames[i], text="", fg="white", bd=2,
                              font="lucida 18", bg=self.BG, width=3, height=1)
                b.pack(side="left", padx=2)

                row_btn.append(b)
            self.buttons.append(row_btn)

    def key_press(self, e=None, keyboard=None):
        if e:
            if e.keysym == "BackSpace":
                self.erase_character()

            elif e.keysym == "Return":
                self.check_for_match()

            elif 65 <= e.keycode <= 90:
                key = e.char
                if self.current_b == self.word_size:
                    self.current_b = self.word_size - 1

                    characters = list(self.guess)
                    characters[self.current_b] = ""
                    self.guess = "".join(characters)

                self.buttons[self.current_B_row][self.current_b]["text"] = key.upper()
                self.buttons[self.current_B_row][self.current_b]['bg'] = "#3d3d3d"
                self.guess += key.upper()
                self.current_b += 1
            else:
                print(e.keysym)
        else:
            key_press = keyboard.widget
            if key_press['text'] == 'Enter':
                self.check_for_match()
            elif key_press['text'] == '←':
                self.erase_character()
            else:
                if self.current_b == self.word_size:
                    self.current_b = self.word_size - 1

                    characters = list(self.guess)
                    characters[self.current_b] = ""
                    self.guess = "".join(characters)

                self.buttons[self.current_B_row][self.current_b]["text"] = key_press['text']
                self.guess += key_press['text']
                self.current_b += 1
    
    def clear_current_row(self):
        for button in self.buttons[self.current_B_row]:
            button["text"] = ""
            button["bg"] = self.BG
        
        self.guess = ""
        self.current_b = 0
    
    def erase_character(self):
        if self.current_b > 0:
            self.current_b -= 1
            self.guess = self.guess[0: self.current_b]

            self.buttons[self.current_B_row][self.current_b]["bg"] = self.BG
            self.buttons[self.current_B_row][self.current_b]["text"] = ""

    def check_for_match(self):
        print("guess = ", self.guess)
        if len(self.guess) == self.word_size:
            if not self.word_api.is_in_dictionary(self.guess):
                messagebox.showwarning("Invalid Word", f"'{self.guess}' is not in our word list. Please try another word.")
                self.clear_current_row()
                return 
            self.guess_count += 1
            self.solver_has_run = False

            if self.word_api.is_valid_guess(self.guess):
                for button in self.buttons[self.current_B_row]:
                    button["bg"] = "green"

                # changing the keypad color
                self.change_keypad_color("#00ff2a", self.guess)

                self.won = True
                self.score += self.MAX_SCORE - 2 * (self.guess_count - 1)

                self.status_bar["text"] = f"Score : {self.score}"

                if self.score > self.high_score:
                    self.update_high_score()

                print("You won !!!")
                self.word_api.select_word()
                self.show_popup()
            else:
                if self.guess_count == 6:
                    print("You Lost !!!")
                    self.show_popup()
                    self.word_api.select_word()
                    return
                for i in range(self.word_size):
                    if self.word_api.is_at_right_position(i, self.guess[i]):
                        self.buttons[self.current_B_row][i]['bg'] = "green"

                        # changing the keypad color
                        self.change_keypad_color("#0fd630", self.guess[i], "#239436", "#0fd630")

                        """
                         if a character is present more than once in a word then we will only
                         change the color of, that comes first, That's why we are replacing the 
                         duplicates with '/' so that the duplic+-ates are not highlighted.
                        """
                        characters = list(self.guess)
                        for index, char in enumerate(characters):
                            if self.word_api.is_at_right_position(i, char):
                                characters[index] = '/'

                        self.guess = "".join(characters)

                    elif self.word_api.is_in_word(self.guess[i]):
                        self.buttons[self.current_B_row][i]['bg'] = "#d0d925"

                        # changing the keypad color
                        self.change_keypad_color("#d0d925", self.guess[i], "#9ba128", "#d0d925")

                        """
                         if a character is present more than once in a word then we will only
                         change the color of, that comes first, That's why we are replacing the 
                         duplicates with '/' so that the duplicates are not highlighted.
                        """
                        characters = list(self.guess)
                        print(characters)
                        for index, char in enumerate(characters):
                            if char == self.guess[i] and index != i:
                                characters[index] = '/'
                            # if self.word_api.is_at_right_position(i, char):
                            #     characters[index] = '/'

                        self.guess = "".join(characters)
                    else:
                        self.change_keypad_color("#4d4a4a", self.guess[i], "#3d3b3b", "#4d4a4a")

            self.current_b = 0
            self.current_B_row += 1
            self.guess = ""

    def start_new_game(self):
        print("Starting a new game...")
        self.word_api.select_word()
        # print(f"New secret word is: {self.word_api.word}")
        self.reset(keypad=True)
        for row_buttons in self.buttons:
            for button in row_buttons:
                button.config(text="", bg=self.BG)

    def reset(self, popup=None, keypad=None):
        self.solver_has_run = False
        if not keypad:
            for buttons_list in self.buttons:
                for button in buttons_list:
                    button["text"] = ""
                    button["bg"] = self.BG

        for buttons_list in self.keypad_buttons:
            for button in buttons_list:
                button["bg"] = self.BG
                button.bind("<Enter>", lambda e: on_hover(e, "#575656"))
                button.bind("<Leave>", lambda e: off_hover(e, self.BG))

        self.current_b = self.current_B_row = 0
        if not self.won:
            self.score = 0

        self.status_bar["text"] = f"Score : {self.score}"

        self.won = False
        self.guess_count = 0
        self.guess = ""

        self.root.attributes('-disabled', False)
        self.root.focus_get()
        if popup:
            popup.destroy()

    def show_popup(self):
        popup = tk.Toplevel()
        popup.title("Game Over")

        x_co = int(self.width / 2 - (450 / 2)) + self.x_co
        y_co = self.y_co + int(self.height / 2 - (250 / 2))

        popup.geometry(f"450x250+{x_co}+{y_co}")
        popup.configure(background="black")
        popup.wm_iconbitmap('images/icon.ico')
        popup.focus_force()

        status = "You Lost :("

        if self.won:
            status = "You Won !!!"

        status_label = tk.Label(popup, text=status, font="cambria 20 bold", fg="#14f41f", bg="black")
        status_label.pack(pady=10)

        if not self.won:
            right_word = tk.Label(popup, text=f"The word was {self.word_api.word}", font="cambria 15 bold",
                                  fg="#14f41f", bg="black")
            right_word.pack(pady=3)

        score_label = tk.Label(popup, text=f"Score : {self.score}", font="lucida 15 bold", fg="white", bg="black")
        score_label.pack(pady=4)

        high_score_label = tk.Label(popup, text=f"High Score : {self.high_score}", font="lucida 15 bold", fg="white", bg="black")
        high_score_label.pack(pady=4)

        button = tk.Button(popup, text="Okay", font="lucida 12 bold", fg="#00d0ff", cursor="hand2",
                           bg="#252525", padx=10, command=lambda: self.reset(popup))
        button.pack(pady=4)

        # disable the main window, will get enabled only when popup is closed
        self.root.attributes('-disabled', True)

        def close():
            self.reset(popup)

        popup.protocol("WM_DELETE_WINDOW", close)

    def change_keypad_color(self, color, guess, on_hover_color=None, off_hover_color=None):
        for char in guess:
            if 65 <= ord(char) <= 70:
                btn_frame_index = 0
                btn_index = ord(char) - 65
            elif 71 <= ord(char) <= 80:
                btn_frame_index = 1
                btn_index = ord(char) - 71
            else:
                btn_frame_index = 2
                btn_index = ord(char) - 81

            if char == "/":
                return

            self.keypad_buttons[btn_frame_index][btn_index]['bg'] = color

            if on_hover_color:
                self.keypad_buttons[btn_frame_index][btn_index].bind("<Enter>", lambda e: on_hover(e, on_hover_color))
                self.keypad_buttons[btn_frame_index][btn_index].bind("<Leave>", lambda e: off_hover(e, off_hover_color))

    def get_from_db(self):
        if not os.path.exists("settings.db"):
            connection = sqlite3.connect("settings.db")
            cursor = connection.cursor()

            # Tạo DB mới với solve_method và hard_mode
            cursor.execute(
                "CREATE TABLE info(id integer, word_length integer, high_score integer, solve_method text, hard_mode integer)"
            )
            cursor.execute(
                "INSERT INTO info VALUES(?,?,?,?,?)",
                (0, 5, 0, "BFS", 1)    # default solve = BFS, hard_mode = True
            )

            self.word_size = 5
            self.high_score = 0
            self.solve_method = "BFS"
            self.hard_mode = True
            self.word_api = words_api.Words(self.word_size)

            connection.commit()
            connection.close()

        else:
            connection = sqlite3.connect("settings.db")
            cursor = connection.cursor()

            # Kiểm tra xem các cột cần thiết có tồn tại không
            cursor.execute("PRAGMA table_info(info)")
            columns = [col[1] for col in cursor.fetchall()]

            if "solve_method" not in columns:
                cursor.execute("ALTER TABLE info ADD COLUMN solve_method TEXT DEFAULT 'BFS'")
                connection.commit()

            if "hard_mode" not in columns:
                cursor.execute("ALTER TABLE info ADD COLUMN hard_mode INTEGER DEFAULT 1")
                connection.commit()

            # Đọc lại dữ liệu
            cursor.execute("SELECT * FROM info")
            data = cursor.fetchall()

            self.word_size = data[0][1]
            self.high_score = data[0][2]
            self.solve_method = data[0][3]
            try:
                self.hard_mode = bool(data[0][4])
            except Exception:
                self.hard_mode = True

            self.word_api = words_api.Words(self.word_size)

            connection.close()

    def solve(self):
        if self.solver_has_run:
            for r in range(self.current_B_row, 6):
                for c in range(self.word_size):
                    self.buttons[r][c].config(text="", bg=self.BG)
            self.root.update()
        print("Running solver method:", self.solve_method)
        if self.solve_method == "BFS":
            self.solve_bfs()
        elif self.solve_method == "DFS":
            self.solve_dfs()
        elif self.solve_method == "Entropy":
            self.solve_entropy()
        elif self.solve_method == "A*":
            self.solve_astar()
        else:
            print("Unknown solve method:", self.solve_method)
            return
        self.solver_has_run = True


    def update_high_score(self):
        connection = sqlite3.connect("settings.db")
        cursor = connection.cursor()

        self.high_score = self.score
        print("update score = ",self.high_score)
        cursor.execute(f"UPDATE info SET high_score={self.score} WHERE id=0")
        connection.commit()

        connection.close()

    def open_setting(self):
        setting = std.Settings(self)

    def on_hover(self, e):
        widget = e.widget
        widget["image"] = self.setting_dark

    def off_hover(self, e):
        widget = e.widget
        widget["image"] = self.setting

    def solve_astar(self):
        # 1. Thu thập trạng thái bàn cờ hiện tại (Giống hệt solve_dfs)
        board_state = []
        for r in range(self.current_B_row):
            guess = "".join([self.buttons[r][c]["text"] for c in range(self.word_size)])
            
            feedback = []
            for c in range(self.word_size):
                color = self.buttons[r][c]["bg"]
                if color == "green": 
                    feedback.append('G')
                elif color == "#d0d925": 
                    feedback.append('Y')
                else: 
                    feedback.append('X') # Gray

            if guess:
                # Đảm bảo guess luôn là chữ hoa để khớp với từ điển
                board_state.append((guess.upper(), feedback))
        
        # 2. Khởi tạo Solver và gọi hàm giải
        # Lưu ý: Phải truyền board_state vào hàm solve()
        solver = AStarSolver(self.word_api)
        solution = solver.solve(board_state)
        
        # 3. Hiển thị kết quả lên giao diện
        print(f"A* Solution found: {solution}")
        
        start_row = self.current_B_row
        secret_word = self.word_api.word.upper()
        
        for i, word in enumerate(solution):
            current_row = start_row + i
            if current_row > 5: # Không vượt quá 6 hàng
                break
            
            # Tính toán màu sắc dựa trên đáp án thật (secret_word) để vẽ lên GUI
            # Dùng hàm _calculate_feedback có sẵn trong solver (trả về G, Y, X)
            feedback = solver._calculate_feedback(word, secret_word)
            
            for c in range(self.word_size):
                # Điền chữ
                self.buttons[current_row][c]["text"] = word[c]
                
                # Tô màu
                if feedback[c] == 'G': 
                    self.buttons[current_row][c].config(bg="green")
                elif feedback[c] == 'Y': 
                    self.buttons[current_row][c].config(bg="#d0d925")
                else: 
                    self.buttons[current_row][c].config(bg="#4d4a4a")
            
            # Cập nhật giao diện từng bước
            self.root.update()
            time.sleep(0.5) # Tạo hiệu ứng gõ phím từ từ
            
        # 4. Xuất thống kê (Excel / Console)
        stats = solver.get_stats()
        StatsLogger.print_stats("A*", stats)
        StatsLogger.save_run(
            algorithm_name="A*",
            stats_dict=stats,
            solution_path=solver.guesses_history,
            target_word=self.word_api.word.upper(),
            word_length=self.word_size
        )
    
    
    def solve_dfs(self):
        board_state = []
        for r in range(self.current_B_row):
            guess = "".join([self.buttons[r][c]["text"] for c in range(self.word_size)])
            
            feedback = []
            for c in range(self.word_size):
                color = self.buttons[r][c]["bg"]
                if color == "green": feedback.append('G')
                elif color == "#d0d925": feedback.append('Y')
                else: feedback.append('X')

            if guess:
                # CẢI TIẾN: Đảm bảo guess luôn là chữ hoa
                board_state.append((guess.upper(), feedback))
                
        solver = DFSSolver(self.word_api)
        solution_for_gui = solver.solve(board_state)
        
        start_row = self.current_B_row
        secret_word = self.word_api.word
        
        for i, word in enumerate(solution_for_gui):
            current_row = start_row + i
            if current_row > 5: break
            
            feedback = solver._calculate_feedback(word, secret_word)
            
            for c in range(self.word_size):
                self.buttons[current_row][c]["text"] = word[c]
                if feedback[c] == 'G': self.buttons[current_row][c].config(bg="green")
                elif feedback[c] == 'Y': self.buttons[current_row][c].config(bg="#d0d925")
                else: self.buttons[current_row][c].config(bg="#4d4a4a")
            self.root.update()
            # time.sleep(0.5) 
        
        stats = solver.get_stats()
        StatsLogger.print_stats("DFS", stats)
        StatsLogger.save_run(
            algorithm_name="DFS",
            stats_dict=stats,
            solution_path=solver.full_solution_path,
            target_word=self.word_api.word.upper(),
            word_length=self.word_size
        )
    
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

    def solve_entropy(self):
        # --- 1. Tạo trạng thái bàn cờ từ giao diện (Parsing Board State) ---
        board_state = []
        # Duyệt qua các hàng đã đoán (current_B_row) để lấy dữ liệu quá khứ
        for r in range(self.current_B_row):
            # Lấy text từ button
            guess = "".join([self.buttons[r][c]["text"] for c in range(self.word_size)])
            
            # Nếu hàng đó chưa có chữ (hoặc lỗi), bỏ qua
            if len(guess) != self.word_size:
                continue

            feedback = []
            for c in range(self.word_size):
                bg_color = self.buttons[r][c]["bg"]
                # Map màu từ GUI sang ký tự G/Y/X
                if bg_color == "green":
                    feedback.append('G')
                elif bg_color == "#d0d925": # Màu vàng
                    feedback.append('Y')
                else: # Màu xám (#4d4a4a hoặc màu mặc định)
                    feedback.append('X')
            
            board_state.append((guess, feedback))

        # --- 2. Khởi tạo và gọi solver ---
        print("Solver is thinking...")
        self.root.update() # Cập nhật UI để tránh bị đơ khi tính toán
        
        solver = EntropySolver(self.word_api)
        
        # Gọi hàm solve chuẩn.
        # Lưu ý: Sử dụng lựa chọn hard mode từ Settings (self.hard_mode)
        solution = solver.solve(board_state, hard_mode=self.hard_mode)

        stats = solver.get_stats()
        StatsLogger.print_stats("Entropy", stats)
        StatsLogger.save_run(
            algorithm_name="Entropy",
            stats_dict=stats,
            solution_path=solution,
            target_word=self.word_api.word.upper(),
            word_length=self.word_size
        )

        # --- 3. Hiển thị kết quả (Chỉ hiển thị các nước đi MỚI) ---
        
        # full_solution chứa cả các từ cũ. Ta cần cắt bỏ phần đã có trên bảng.
        # Ví dụ: board có 2 từ, solution có 5 từ -> chỉ lấy 3 từ cuối
        current_guesses_count = len(board_state)
        new_moves = solution[current_guesses_count:] 

        start_row = self.current_B_row
        
        # UI only shows max 6 rows, but solution continues beyond
        for i, word in enumerate(new_moves):
            current_row = start_row + i
            
            # Only display on UI if within 6 rows
            if current_row < 6:
                # Điền chữ cái
                for c in range(self.word_size):
                    self.buttons[current_row][c]["text"] = word[c]
                
                # Tính màu để hiển thị
                fb = self.word_api.get_feedback(word)
                
                for c, f in enumerate(fb):
                    if f == "G":
                        self.buttons[current_row][c].config(bg="green")
                    elif f == "Y":
                        self.buttons[current_row][c].config(bg="#d0d925")
                    else:
                        self.buttons[current_row][c].config(bg="#4d4a4a")
                
                # Cập nhật biến theo dõi dòng hiện tại của Game
                self.current_B_row += 1 
                
                self.root.update()
                time.sleep(0.5)
            
            # Check if solved (even if beyond row 6)
            if word == self.word_api.word:
                break

        # Kiểm tra thắng thua sau khi chạy xong
        total_guesses = len(solution)
        if solution and self.word_api.is_valid_guess(solution[-1]):
            if total_guesses <= 6:
                print(f">>> SOLVER WON in {total_guesses} guesses!")
            else:
                print(f">>> SOLVER SOLVED in {total_guesses} guesses (beyond 6-guess UI limit)")
        else:
            print(">>> SOLVER STOPPED (Lost or Error)")

    def _get_board_state(self):
            """Helper để lấy trạng thái bàn cờ hiện tại"""
            board_state = []
            for r in range(self.current_B_row):
                guess = "".join([self.buttons[r][c]["text"] for c in range(self.word_size)])
                if not guess: continue
                
                feedback = []
                for c in range(self.word_size):
                    color = self.buttons[r][c]["bg"]
                    if color == "green": feedback.append('G')
                    elif color == "#d0d925": feedback.append('Y')
                    else: feedback.append('X')
                board_state.append((guess, feedback))
            return board_state
    def _animate_solution(self, solution, solver_instance):
        """Helper để hiển thị lời giải lên màn hình"""
        start_row = self.current_B_row
        secret_word = self.word_api.word
        
        for i, word in enumerate(solution):
            current_row = start_row + i
            if current_row > 5: break
            
            feedback = solver_instance._calculate_feedback(word, secret_word)
            
            for c in range(self.word_size):
                self.buttons[current_row][c]["text"] = word[c]
                if feedback[c] == 'G':
                    self.buttons[current_row][c].config(bg="green")
                elif feedback[c] == 'Y':
                    self.buttons[current_row][c].config(bg="#d0d925")
                else:
                    self.buttons[current_row][c].config(bg="#4d4a4a")
            
            self.root.update()
            time.sleep(0.5)

def on_hover(e, color):
    button = e.widget
    button["bg"] = color


def off_hover(e, color):
    button = e.widget
    button["bg"] = color


if __name__ == '__main__':
    Wordle()
