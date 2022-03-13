from solver import Solver
from constants import Constants


if __name__ == "__main__":
    print("wordle solver!")
    c = Constants()
    print(c.today)
    s = Solver(c)
    s.play()
