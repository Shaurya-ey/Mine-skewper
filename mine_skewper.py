import random
letters = "abcdefghij"


def play():
    print("-----------------------------------------------------------------Welcome to Mine Skewper!----------------------------------------------------------------")
    print("Wanna experience the thrill like that of classic windows minesweepwer? well this is an inspired version of that game.")
    print()
    print("---------------Pick a position for e.g: a1,b6 and etc, to reveal the position and try your luck+skills to avoid the bombs and win the game.---------------")

def difficulty_set():
    print("Select difficulty level:")
    print("1. Easy [6x6, 5 bombs]")
    print("2. Medium [8x8, 10 bombs]")
    print("3. Hard [10x10, 15 bombs]")    

    while True:
        select = input("Enter your choice: ")
        if select == "1":
            return 6, 5, 1  #size, bombs, score multiplier
        elif select == "2":
            return 8, 10, 2    
        elif select == "3":
            return 10, 15, 3
        else:
            print("Invalid Selection...")

class Mineskewper:
    def __init__(self, size, bombs, score_multiplier):
        self.size = size
        self.bombs = bombs
        self.score_multiplier = score_multiplier
        self.score = 0
        self.opened = 0     #safe cells opened
        self.safe_cells = size * size - bombs # when all safe cells are opened, player wins
        self.game_over = False      
        self.revealed = self.m_revealed()
        self.table = self.m_table()

    def m_table(self):
        table = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(0)
            table.append(row)

        #placing bomb randomly
        placed_b = 0   #tracks how many bombs are placed
        while placed_b < self.bombs:
            rows = random.randint(0, self.size - 1)
            columns = random.randint(0, self.size - 1)
            if table[rows][columns] != -1:
                table[rows][columns] = -1
                placed_b += 1

        #counting bombs touching each cell
        for rows in range(self.size):
            for columns in range(self.size):
                if table[rows][columns] == -1:
                    continue
                count = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        row_n = rows + i
                        columns_n = columns + j
                        if (0 <= row_n < self.size) and (0 <= columns_n < self.size) and (table[row_n][columns_n] == -1):
                            count += 1
                table[rows][columns] = count
        return table    

    def m_revealed(self):
        revealed = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(False)
            revealed.append(row)
        return revealed

    #showing the board...
    def show_table(self, show_all = False):
        line = "----+" + "-----+" * self.size
        header = "    |" #for column letters
        for letter in letters[:self.size].upper():
            header += "  " + letter + "  |"
        print(line)
        print(header)
        print(line)

        for rows in range(self.size):
            text = str(rows + 1).rjust(3) + " |"
            for columns in range(self.size):
                if self.revealed[rows][columns] or show_all:
                    if self.table[rows][columns]== -1:
                        row_str = "*"
                    elif self.table[rows][columns] == 0:
                        row_str = " "
                    else:
                        row_str = str(self.table[rows][columns])
                else:
                    row_str = "#"
                text += "  " + row_str + "  |"
            print(text)
            print(line)


    def show_score(self):
        print("Score:", self.score)
    def show_status(self, show_all = False):
        print("---------------------------------------------------------------------------------------------------------------------------------------------------------")
        self.show_table(show_all)
        self.show_score()

    #game logic
    #converts "e4" to rows & columns
    def get_pos(self):
        while True:
            position = input("Enter position (example:a1): ")
            gg = position.strip().lower()

            if len(gg) < 2 or len(gg) > 3:
                print("Invalid input, example: a1")
                continue

            letter = gg[0]
            number = gg[1:]

            if letter not in letters[:self.size] or not number.isdigit():
                print("Invalid input, example: a1")
                continue

            rows = int(number) - 1
            columns = letters.index(letter)

            if rows < 0 or rows >= self.size:
                print("that row is out of bounds, please enter a valid position.") 
                continue

            return rows, columns
        
    def reveal(self, rows, columns):
        if rows < 0 or rows >= self.size or columns < 0 or columns >= self.size:
            return 0
        if self.revealed[rows][columns]:
            return 0

        self.revealed[rows][columns] = True
        count = 1

        if self.table[rows][columns] == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    count += self.reveal(rows + i, columns + j)
        return count

    def is_won(self):
        return self.opened == self.safe_cells
    
    def loose(self):
        self.show_status(show_all = True)
        print("You hit a bomb! Game Over.")
        self.game_over = True

    def win(self):
        print("Congratulations! You have won the game.")
        print("Your final score is:", self.score)
        self.game_over = True

# game loop
    def p_loop(self):
        self.show_status()

        while not self.game_over:
            rows, columns = self.get_pos()

            if self.revealed[rows][columns]:
                print("Position already choosen. Please choose another position.")
                continue

            if self.table[rows][columns] == -1:
                self.loose()
                break

            new_cells = self.reveal(rows, columns)
            self.opened += new_cells
            self.score += new_cells * 10 * self.score_multiplier

            self.show_status()

            if self.is_won():
                self.win()  
    
while True:
    play()
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------")
    size, bombs, score_multiplier = difficulty_set()
    strt = Mineskewper(size, bombs, score_multiplier)
    strt.p_loop()

    play_again = input("Do you want to play again? (y/n): ")
    if play_again.lower() != 'y':
        print("Thanks for playing!")
        break
