import numpy as np
import re
from parse import parse_file


def parse_line(line):
    match_obj = re.match(
        '([0-9]+),([0-9]+),([0-9]+)~([0-9]+),([0-9]+),([0-9]+)', line)
    x1, y1, z1, x2, y2, z2 = list(map(int, match_obj.groups()))
    return ((z1, y1, x1), (z2, y2, x2))


class SandPile:
    def __init__(self, bricks, pile):
        self.bricks = bricks
        self.pile = pile

    def from_file(filename):
        bricks = np.array(parse_file(filename, parse_line))
        pile = np.zeros(tuple(np.max(bricks, axis=(0, 1)) +
                              np.array((1, 1, 1))), dtype=int)
        pile[0, :, :] = -1
        for (brick_index, (from_point, to_point)) in enumerate(bricks):
            pile[from_point[0]:to_point[0] + 1, from_point[1]:to_point[1] +
                 1, from_point[2]:to_point[2] + 1] = brick_index + 1
        SandPile.drop_bricks(bricks, pile)
        return SandPile(bricks, pile)

    def __copy__(self):
        return SandPile(self.bricks.copy(), self.pile.copy())

    def drop_bricks(bricks, pile):
        changed_block_count = 0
        surface_height_map = np.ones(shape=pile.shape[1:], dtype=int)
        handled_bricks = set()
        for layer in range(1, pile.shape[0]):
            bricks_on_this_layer = set(pile[layer][pile[layer] != 0])
            for brick in filter(lambda b: b not in handled_bricks, bricks_on_this_layer):
                handled_bricks.add(brick)
                brick -= 1
                (from_z, from_y, from_x), (to_z, to_y,
                                           to_x) = bricks[brick, :, :]
                new_height = np.max(
                    surface_height_map[from_y:to_y + 1, from_x:to_x + 1])
                pile[from_z:to_z + 1,
                     from_y:to_y + 1, from_x:to_x + 1] = 0
                pile[new_height:new_height + to_z - from_z +
                     1, from_y:to_y + 1, from_x:to_x + 1] = brick + 1
                surface_height_map[from_y:to_y + 1,
                                   from_x:to_x + 1] = new_height + to_z - from_z + 1
                bricks[brick, :, 0] = (
                    new_height, new_height + to_z - from_z)
                if new_height != from_z:
                    changed_block_count += 1
        return changed_block_count

    def support_bricks(self, brick):
        (from_z, from_y, from_x), (_, to_y, to_x) = self.bricks[brick]
        return set(self.pile[from_z - 1, from_y:to_y + 1, from_x:to_x + 1]
                   [self.pile[from_z - 1, from_y:to_y + 1, from_x:to_x + 1] != 0])

    def can_brick_be_disintigrated(self, brick):
        (_, from_y, from_x), (to_z, to_y, to_x) = self.bricks[brick]
        bricks_above = set(self.pile[to_z + 1, from_y:to_y + 1, from_x:to_x + 1]
                           [self.pile[to_z + 1, from_y:to_y + 1, from_x:to_x + 1] != 0])
        return all((len(self.support_bricks(brick_above - 1)) > 1 for brick_above in bricks_above))

    def compute_disintigratable_count(self):
        count = 0
        for brick in range(len(self.bricks)):
            if self.can_brick_be_disintigrated(brick):
                count += 1
        return count

    def disintigrate_brick(self, brick):
        (from_z, from_y, from_x), (to_z, to_y, to_x) = self.bricks[brick]
        self.pile[from_z:to_z + 1, from_y:to_y + 1, from_x:to_x + 1] = 0
        result = SandPile.drop_bricks(self.bricks, self.pile)
        return result

    def solve_part2(self):
        result = 0
        copy_self = self.__copy__()
        for brick in range(len(self.bricks)):
            result += self.disintigrate_brick(brick)
            self = copy_self.__copy__()
        return result


if __name__ == '__main__':
    pile = SandPile.from_file('input')
    print(pile.compute_disintigratable_count())
    print(pile.solve_part2())
