import itertools
import math

with open('input.txt', 'r') as f:
    numbers = [int(line) for line in f]

def fn(numbers, n):
    for combination in itertools.product(*[numbers] * n):
        if sum(combination) == 2020:
            return math.prod(combination)

print(f'Part 1: {fn(numbers, 2)}')
print(f'Part 2: {fn(numbers, 3)}')
