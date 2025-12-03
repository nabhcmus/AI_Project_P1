import random
import os

class Words:
    def __init__(self, size):
        self.size = size
        self.words_list = []
        self.used_words = []
        self.word = ""

        self.load_words()
        self.select_word()

    def load_words(self):
        if self.size == 3:
            file_name = 'three_letters'
        elif self.size == 4:
            file_name = 'four_letters'
        elif self.size == 5:
            file_name = 'five_letters'
        else:
            file_name = 'six_letters'

        # Tìm đường dẫn tuyệt đối đến thư mục gốc của project
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "word_files", f"{file_name}.txt")
        
        with open(file_path, 'r') as file:
            self.words_list = file.readlines()

        self.words_list = [word.strip().upper() for word in self.words_list]


    def is_at_right_position(self, i, char):
        if self.word[i] == char:
            return True
        return False

    def is_in_word(self, char):
        if char in self.word:
            return True
        return False

    def is_valid_guess(self, guess):
        if guess == self.word:
            return True
        return False

    def select_word(self):
        self.word = random.choice(self.words_list).upper()
        while self.word in self.used_words:
            self.word = random.choice(self.words_list).upper()

        self.used_words.append(self.word)

    def is_in_dictionary(self, word):
        return word in self.words_list

    def display_right_word(self):
        print("Right word was : ", self.word)
    def get_feedback(self, guess):
        secret = list(self.word)
        guess_list = list(guess)
        feedback = ['X'] * len(self.word)

        # 1. Check Green
        for i in range(len(self.word)):
            if guess_list[i] == secret[i]:
                feedback[i] = 'G'
                secret[i] = None
                guess_list[i] = None # Đánh dấu để không xét Yellow vị trí này nữa

        # 2. Check Yellow
        for i in range(len(self.word)):
            if guess_list[i] is not None: # Bỏ qua những ô đã là Green
                char = guess_list[i]
                if char in secret:
                    feedback[i] = 'Y'
                    # Xóa ký tự đã dùng trong secret (1-đổi-1 mechanism)
                    secret[secret.index(char)] = None
        
        return feedback