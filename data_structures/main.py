"""
data_structures.py
-------------------
A tour of Python's core data structures, with runnable examples for each,
plus a small Tic Tac Toe project at the end that uses several of them
together (list for the board, tuples for coordinates, sets for tracking
moves, dict for scoring).

Run this file directly to see every demo print its output:
    python data_structures.py
"""


# ---------------------------------------------------------------------------
# 1. STRINGS - immutable sequences of characters
# ---------------------------------------------------------------------------
def demo_strings():
    print("=== STRINGS ===")
    name = "Python"

    # Indexing and slicing
    print("First char:", name[0])
    print("Last 3 chars:", name[-3:])

    # Strings are immutable - this creates a NEW string, doesn't mutate name
    shout = name.upper()
    print("Uppercase:", shout)

    # Splitting and joining
    sentence = "data structures are fun"
    words = sentence.split(" ")
    print("Split into words:", words)
    print("Joined with dashes:", "-".join(words))

    # f-strings for formatting (preferred way to build strings with values)
    count = len(words)
    print(f"That sentence has {count} words.")

    # Common cleanup
    messy = "   trailing spaces   "
    print(f"Stripped: '{messy.strip()}'")


# ---------------------------------------------------------------------------
# 2. LISTS - mutable, ordered collections
# ---------------------------------------------------------------------------
def demo_lists():
    print("\n=== LISTS ===")
    fruits = ["apple", "banana", "cherry"]

    fruits.append("date")            # add to the end
    fruits.insert(1, "blueberry")    # insert at a specific index
    print("After adding:", fruits)

    fruits.remove("banana")          # remove by value
    popped = fruits.pop()            # remove & return the last item
    print("After removing:", fruits, "| popped:", popped)

    fruits.sort()
    print("Sorted:", fruits)

    # Slicing works like strings
    print("First two:", fruits[:2])

    # Lists can be nested
    matrix = [[1, 2, 3], [4, 5, 6]]
    print("Nested list element [1][2]:", matrix[1][2])


# ---------------------------------------------------------------------------
# 3. TUPLES - immutable, ordered collections
# ---------------------------------------------------------------------------
def demo_tuples():
    print("\n=== TUPLES ===")
    point = (3, 4)
    print("Point:", point, "| x =", point[0], "| y =", point[1])

    # Tuples are great for multiple return values
    def min_max(numbers):
        return min(numbers), max(numbers)  # returns a tuple

    low, high = min_max([5, 1, 9, 3])  # unpacking
    print(f"Min: {low}, Max: {high}")

    # Attempting point[0] = 10 would raise TypeError - tuples can't be mutated
    try:
        point[0] = 10
    except TypeError as e:
        print("Can't modify a tuple:", e)


# ---------------------------------------------------------------------------
# 4. DICTIONARIES - key/value pairs
# ---------------------------------------------------------------------------
def demo_dictionaries():
    print("\n=== DICTIONARIES ===")
    student = {"name": "Ada", "age": 28, "major": "CS"}

    print("Name:", student["name"])
    student["age"] = 29           # update a value
    student["gpa"] = 3.9          # add a new key
    print("Updated dict:", student)

    # .get() avoids KeyError if the key might not exist
    print("Minor (if any):", student.get("minor", "None declared"))

    # Iterating
    for key, value in student.items():
        print(f"  {key}: {value}")

    # Dict comprehension
    squares = {n: n * n for n in range(5)}
    print("Squares dict:", squares)


# ---------------------------------------------------------------------------
# 5. SETS - unordered collections of unique elements
# ---------------------------------------------------------------------------
def demo_sets():
    print("\n=== SETS ===")
    a = {1, 2, 3, 4}
    b = {3, 4, 5, 6}

    print("Union:", a | b)
    print("Intersection:", a & b)
    print("Difference (a - b):", a - b)

    # Great for deduplication
    numbers = [1, 2, 2, 3, 3, 3, 4]
    print("Deduplicated:", set(numbers))

    # Fast membership testing
    print("Is 3 in a?", 3 in a)


# ---------------------------------------------------------------------------
# 6. ARRAYS - fixed-type sequences (via the built-in 'array' module)
# ---------------------------------------------------------------------------
def demo_arrays():
    print("\n=== ARRAYS ===")
    from array import array

    # 'i' = signed int type code; every element must be the same type
    nums = array("i", [1, 2, 3, 4])
    nums.append(5)
    print("Array:", nums)
    print("As a list:", nums.tolist())

    try:
        nums.append("not a number")  # will raise TypeError
    except TypeError as e:
        print("Arrays enforce a single type:", e)


# ---------------------------------------------------------------------------
# 7. LIST COMPREHENSIONS - concise way to build lists
# ---------------------------------------------------------------------------
def demo_list_comprehensions():
    print("\n=== LIST COMPREHENSIONS ===")

    squares = [n * n for n in range(10)]
    print("Squares:", squares)

    evens = [n for n in range(20) if n % 2 == 0]
    print("Evens:", evens)

    # Comprehension with a transformation + condition
    words = ["hello", "WORLD", "Python"]
    shouted_short = [w.upper() for w in words if len(w) <= 6]
    print("Upper, len<=6:", shouted_short)

    # Nested comprehension - flatten a matrix
    matrix = [[1, 2], [3, 4], [5, 6]]
    flat = [num for row in matrix for num in row]
    print("Flattened matrix:", flat)


# ---------------------------------------------------------------------------
# PROJECT: Tic Tac Toe
# Uses: list (the board), tuples (coordinates), set (available moves),
#       dict (score tracking)
# ---------------------------------------------------------------------------
class TicTacToe:
    def __init__(self):
        # Board is a list of 9 elements, indexed 0-8, left-to-right top-to-bottom
        self.board = [" "] * 9
        # Track which positions are still open using a set for fast lookup/removal
        self.available = set(range(9))
        self.current_player = "X"
        self.scores = {"X": 0, "O": 0, "Ties": 0}

    def print_board(self):
        b = self.board
        rows = [b[0:3], b[3:6], b[6:9]]
        print()
        for i, row in enumerate(rows):
            print(" | ".join(row))
            if i < 2:
                print("-" * 9)
        print()

    def make_move(self, position):
        if position not in self.available:
            print("That spot is taken or invalid. Try again.")
            return False
        self.board[position] = self.current_player
        self.available.remove(position)
        return True

    def check_winner(self):
        # All possible winning triples, expressed as tuples of board indices
        winning_lines = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6),             # diagonals
        ]
        for a, b, c in winning_lines:
            if self.board[a] == self.board[b] == self.board[c] != " ":
                return self.board[a]
        if not self.available:
            return "Tie"
        return None

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def play(self):
        print("Welcome to Tic Tac Toe! Positions are numbered 0-8, left-to-right.")
        while True:
            self.print_board()
            try:
                move = int(input(f"Player {self.current_player}, choose a position (0-8): "))
            except ValueError:
                print("Please enter a number between 0 and 8.")
                continue

            if not self.make_move(move):
                continue

            result = self.check_winner()
            if result:
                self.print_board()
                if result == "Tie":
                    print("It's a tie!")
                    self.scores["Ties"] += 1
                else:
                    print(f"Player {result} wins!")
                    self.scores[result] += 1
                print("Scores:", self.scores)
                break

            self.switch_player()


def play_tic_tac_toe():
    game = TicTacToe()
    game.play()


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    demo_strings()
    demo_lists()
    demo_tuples()
    demo_dictionaries()
    demo_sets()
    demo_arrays()
    demo_list_comprehensions()

    # Uncomment to play interactively:
    # play_tic_tac_toe()