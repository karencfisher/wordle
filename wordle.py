import tkinter as tk
from tkinter import messagebox
import random
from collections import defaultdict

class WordleGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Wordle Game")
        self.guess = ''
        self.secret_word = ''
        self.secret_letters = defaultdict(int)
        self.words = None
        
        # Create the text boxes
        self.text_boxes = []
        for i in range(6):
            row = []
            for j in range(5):
                text_box = tk.Entry(self.master, width=5)
                Font_tuple = ("Comic Sans MS", 20, "bold")
                text_box.configure(font=Font_tuple, justify='center')
                text_box.grid(row=i, column=j, padx=3, pady=3)
                row.append(text_box)
            self.text_boxes.append(row)
            
        # Bind a function to the keypress event for each text box
        for i in range(6):
            for j in range(5):
                def handle_keypress(event, i=i, j=j):
                    self.check_word(i, j, event.char)
                    if j < 4:
                        # Move to the next box in the row
                        self.text_boxes[i][j+1].focus()
                    elif j == 4:
                        if i < 5:
                            self.text_boxes[i+1][0].focus()
                        else:
                            self.done()
                self.text_boxes[i][j].bind("<KeyRelease>", handle_keypress)
        self.giveup_button = tk.Button(self.master, text="I give up", command=self.give_up)
        self.giveup_button.grid(row=7, column=4, sticky="sew", padx=(10, 4), pady=10)
        self.text_boxes[0][0].focus()
        
    def set_secret_word(self, word):
        self.secret_word = word
        self.secret_letters = defaultdict(int)
        for letter in word:
            self.secret_letters[letter] += 1

    def give_up(self):
        ans = messagebox.askyesno('Wordle Quitter',
                                  f'Word was "{self.secret_word}"\nDo you want to try again?')
        if ans:
            self.reset()
        else:
            self.master.quit()
    
    # Function to be called when a letter is typed in the last box of a row
    def check_word(self, row, col, letter):
        self.guess += letter
        if col == 4:
            correct = 0
            used = []
            for i, letter in enumerate(self.guess):
                if letter == self.secret_word[i]:
                    correct += 1
                    self.text_boxes[row][i].configure(bg='green')
                    self.secret_letters[letter] -= 1
                    used.append(i)

            for i, letter in enumerate(self.guess):
                if i in used:
                    continue
                if letter in self.secret_word:
                    if self.secret_letters[letter] > 0:
                        self.text_boxes[row][i].configure(bg='yellow')
                        self.secret_letters[letter] -= 1
                    else:
                        self.text_boxes[row][i].configure(bg='gray')
                    # yellow
                else:
                    self.text_boxes[row][i].configure(bg='gray')
                    #gray

            if correct == 5:
                ans = messagebox.askyesno(title='Wordle Winner', 
                                          message='You nailed it! Want to try another?')
                if ans:
                    self.reset()
                else:
                    self.master.quit()
            self.guess = ''
        self.set_secret_word(self.secret_word)

    def reset(self):
        self.set_secret_word(random.choice(self.words))
        # print(self.secret_word)
        for i in range(6):
            for j in range(5):
                self.text_boxes[i][j].delete(0, tk.END)
                self.text_boxes[i][j].configure(bg='white')
        self.text_boxes[0][0].focus()

    def done(self):
        ans = messagebox.askyesno(title='Wordle Loser', 
                                  message=f'Out of tries. The secret word was "{self.secret_word}". Try agian?')
        if ans:
            self.reset()
        else:
            self.master.quit()
    
    def run(self):
        self.master.mainloop()

def main():
    # Create the window and start the GUI
    root = tk.Tk()
    game = WordleGUI(root)

    with open('words', 'r') as F:
        vocab = F.readlines()
    vocab = list(map(lambda x: x.strip(), vocab))
    game.words = vocab
    game.set_secret_word(random.choice(vocab))
    # print(game.secret_word)
    game.run()


if __name__ == '__main__':
    main()


