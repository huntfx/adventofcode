import math

class Forest(object):
    def __init__(self, width, height):
        self.trees = set()
        self.width = width
        self.height = height

    @classmethod
    def grow(cls):
        lines = []
        with open('input.txt', 'r') as f:
            for y, line in enumerate(f):
                lines.append(line.strip())

        new = cls(len(lines[0]), len(lines))
        for y, line in enumerate(lines):
            for x, tree in enumerate(line.strip()):
                if tree == '#':
                    new.trees.add((x, y))
        return new

    def has_tree(self, x, y):
        return (x % self.width, y) in self.trees

    def travel(self, direction):
        count = 0
        cur_x = cur_y = 0
        while cur_y < self.height:
            cur_x += direction[0]
            cur_y += direction[1]
            if self.has_tree(cur_x, cur_y):
                count += 1
        return count

pt1 = [(3, 1)]
pt2 = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
forest = Forest.grow()
fn = lambda directions: math.prod(map(forest.travel, directions))

print(f'Part 1: {fn(pt1)}')
print(f'Part 2: {fn(pt2)}')
