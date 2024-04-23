# AI-PR2
Berkeley Project #2 - Artificial Inteligence


## Problem #1

```bash
python pacman.py -p ReflexAgent -l testClassic

python pacman.py --frameTime 0 -p ReflexAgent -k 1

python pacman.py --frameTime 0 -p ReflexAgent -k 2

python autograder.py -q q1 --no-graphics

```

## Problem #2

```bash
python pacman.py -p MinimaxAgent -l trappedClassic -a depth=3

python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4

python autograder.py -q q2 --no-graphics
```

## Problem #3

```bash
python pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic

python autograder.py -q q3 --no-graphics
```

## Problem #4

```bash
python pacman.py -p ExpectimaxAgent -l minimaxClassic -a depth=3

python pacman.py -p AlphaBetaAgent -l trappedClassic -a depth=3 -q -n 10

python pacman.py -p ExpectimaxAgent -l trappedClassic -a depth=3 -q -n 10

python autograder.py -q q4
```