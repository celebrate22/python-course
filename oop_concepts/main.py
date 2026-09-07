"""
oop_concepts.py
-----------------
A tour of Python's object-oriented programming concepts, with runnable
examples for each, plus a Banking System project at the end that ties
several of them together (encapsulation for balances, inheritance for
account types, polymorphism for interest calculation).

Run this file directly to see every demo print its output:
    python oop_concepts.py
"""

from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# 1 & 2. CLASSES, OBJECTS & CONSTRUCTORS
# ---------------------------------------------------------------------------
class Dog:
    # __init__ is the constructor - runs automatically when you create a Dog()
    def __init__(self, name, breed):
        self.name = name    # instance attribute
        self.breed = breed

    def bark(self):
        return f"{self.name} says Woof!"


def demo_classes_and_constructors():
    print("\n=== CLASSES, OBJECTS & CONSTRUCTORS ===")
    d1 = Dog("Rex", "Labrador")     # d1 is an object (an instance of Dog)
    d2 = Dog("Milo", "Beagle")
    print(d1.bark())
    print(d2.bark())
    print(f"{d1.name} is a {d1.breed}")


# ---------------------------------------------------------------------------
# 3. 'self' AS DEFAULT ARGUMENT
# ---------------------------------------------------------------------------
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        # 'self' is how the method knows WHICH object's count to change.
        # counter.increment() is really Counter.increment(counter) under the hood.
        self.count += 1
        return self.count


def demo_self():
    print("\n=== 'self' AS DEFAULT ARGUMENT ===")
    c1 = Counter()
    c2 = Counter()
    c1.increment()
    c1.increment()
    c2.increment()
    # Each object keeps its OWN state because 'self' points to a specific instance
    print(f"c1.count = {c1.count}, c2.count = {c2.count}")


# ---------------------------------------------------------------------------
# 4. POLYMORPHISM
# ---------------------------------------------------------------------------
class Cat:
    def speak(self):
        return "Meow"


class Duck:
    def speak(self):
        return "Quack"


def demo_polymorphism():
    print("\n=== POLYMORPHISM ===")
    animals = [Cat(), Duck(), Dog("Rex", "Lab")]
    # We don't care what TYPE each animal is - we just call .speak()
    # and each object responds in its own way. Note: Dog uses .bark() above,
    # so here's a quick example with a shared method name instead:
    for animal in animals:
        if hasattr(animal, "speak"):
            print(animal.speak())
        else:
            print(animal.bark())


# ---------------------------------------------------------------------------
# 5. INHERITANCE
# ---------------------------------------------------------------------------
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "Some generic animal sound"

    def describe(self):
        return f"{self.name} says: {self.speak()}"


class Cow(Animal):          # Cow inherits from Animal
    def speak(self):        # override the parent's method
        return "Moo"


class Sheep(Animal):
    def speak(self):
        return "Baa"


def demo_inheritance():
    print("\n=== INHERITANCE ===")
    farm = [Cow("Bessie"), Sheep("Dolly")]
    for creature in farm:
        print(creature.describe())  # describe() is inherited, speak() is overridden


# ---------------------------------------------------------------------------
# 6. ABSTRACTION
# ---------------------------------------------------------------------------
class Shape(ABC):
    @abstractmethod
    def area(self):
        """Every subclass MUST implement this - Shape itself can't say how."""
        pass


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


def demo_abstraction():
    print("\n=== ABSTRACTION ===")
    shapes = [Circle(3), Rectangle(4, 5)]
    for shape in shapes:
        print(f"{type(shape).__name__} area: {shape.area():.2f}")

    try:
        Shape()  # can't instantiate an abstract class directly
    except TypeError as e:
        print("Can't instantiate Shape directly:", e)


# ---------------------------------------------------------------------------
# 7. ENCAPSULATION
# ---------------------------------------------------------------------------
class BankAccountBasic:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance  # double underscore -> "private" (name-mangled)

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

    def get_balance(self):
        # Controlled access - outside code can't touch __balance directly
        return self.__balance


def demo_encapsulation():
    print("\n=== ENCAPSULATION ===")
    acc = BankAccountBasic("Ada", 100)
    acc.deposit(50)
    print("Balance via method:", acc.get_balance())
    try:
        print(acc.__balance)  # this will fail - name is mangled/hidden
    except AttributeError as e:
        print("Can't access __balance directly:", e)


# ---------------------------------------------------------------------------
# 8. ITERATORS
# ---------------------------------------------------------------------------
class CountUpTo:
    """A custom iterator that counts from 1 up to a limit."""

    def __init__(self, limit):
        self.limit = limit
        self.current = 0

    def __iter__(self):
        return self  # an iterator returns itself here

    def __next__(self):
        if self.current < self.limit:
            self.current += 1
            return self.current
        raise StopIteration  # signals the for-loop to stop


def demo_iterators():
    print("\n=== ITERATORS ===")
    for number in CountUpTo(5):
        print(number, end=" ")
    print()


# ---------------------------------------------------------------------------
# PROJECT: Banking System
# Uses: encapsulation (private balance), inheritance (account types),
#       polymorphism (interest calculation differs per account type),
#       constructors, and iterators (looping over transaction history).
# ---------------------------------------------------------------------------
class InsufficientFundsError(Exception):
    pass


class BankAccount:
    def __init__(self, owner, balance=0.0):
        self.owner = owner
        self._balance = balance          # "protected" by convention
        self._transactions = []          # transaction history

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount
        self._transactions.append(f"Deposited {amount:.2f}")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise InsufficientFundsError(
                f"Cannot withdraw {amount:.2f}; balance is {self._balance:.2f}"
            )
        self._balance -= amount
        self._transactions.append(f"Withdrew {amount:.2f}")

    def apply_interest(self):
        """Base accounts earn no interest - subclasses override this."""
        pass

    def __str__(self):
        return f"{type(self).__name__}({self.owner}): {self._balance:.2f}"

    def __iter__(self):
        # Lets you do: for entry in account: ...
        return iter(self._transactions)


class SavingsAccount(BankAccount):
    INTEREST_RATE = 0.02  # 2%

    def apply_interest(self):
        interest = self._balance * self.INTEREST_RATE
        self._balance += interest
        self._transactions.append(f"Applied interest: {interest:.2f}")


class CheckingAccount(BankAccount):
    OVERDRAFT_LIMIT = 100.0

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance + self.OVERDRAFT_LIMIT:
            raise InsufficientFundsError(
                f"Cannot withdraw {amount:.2f}; exceeds overdraft limit."
            )
        self._balance -= amount
        self._transactions.append(f"Withdrew {amount:.2f}")


def demo_banking_system():
    print("\n=== PROJECT: BANKING SYSTEM ===")
    savings = SavingsAccount("Ada", 1000)
    checking = CheckingAccount("Grace", 200)

    savings.deposit(500)
    savings.apply_interest()          # polymorphism: SavingsAccount's own version
    print(savings)

    checking.withdraw(250)            # goes into overdraft, but within limit
    print(checking)

    try:
        checking.withdraw(1000)       # exceeds overdraft limit -> raises error
    except InsufficientFundsError as e:
        print("Error:", e)

    print(f"\nTransaction history for {savings.owner}:")
    for entry in savings:             # uses BankAccount.__iter__
        print(" -", entry)

    accounts = [savings, checking]
    print("\nAll account summaries:")
    for acc in accounts:
        print(" ", acc)               # polymorphism via __str__


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    demo_classes_and_constructors()
    demo_self()
    demo_polymorphism()
    demo_inheritance()
    demo_abstraction()
    demo_encapsulation()
    demo_iterators()
    demo_banking_system()