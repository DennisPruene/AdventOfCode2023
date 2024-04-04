import numpy as np

CHAR_TO_DIRECTION = {'D': np.array((1, 0)),
                     'R': np.array((0, 1)),
                     'U': np.array((-1, 0)),
                     'L': np.array((0, -1))}


class Trench:
    def __init__(self):
        self.trench = np.array([[0]])
        self.offset = np.array((0, 0))

    def print_trench(self):
        print("\n".join(''.join(row)
              for row in np.where(self.trench, '#', '.')))

    def get_position(self, position):
        if position[0] < -self.offset[0] or position[1] < -self.offset[1] \
                or position[0] >= self.trench.shape[0] - self.offset[0] \
                or position[1] >= self.trench.shape[1] - self.offset[1]:
            return -1
        return self.trench[tuple(np.array(position) + self.offset)]

    def set_position(self, position, value):
        self.trench[tuple(np.array(position) + self.offset)] = value

    def follow_instructions(self, instructions):
        position = np.array((0, 0))
        for (direction, steps) in instructions:
            direction = CHAR_TO_DIRECTION[direction]
            for _ in range(steps):
                position += direction
                if position[0] < -self.offset[0]:
                    self.trench = np.pad(self.trench, ((1, 0), (0, 0)))
                    self.offset[0] += 1
                if position[1] < -self.offset[1]:
                    self.trench = np.pad(self.trench, ((0, 0), (1, 0)))
                    self.offset[1] += 1
                if position[0] >= self.trench.shape[0] - self.offset[0]:
                    self.trench = np.pad(self.trench, ((0, 1), (0, 0)))
                if position[1] >= self.trench.shape[1] - self.offset[1]:
                    self.trench = np.pad(self.trench, ((0, 0), (0, 1)))
                self.set_position(position, 1)
        self.trench = np.pad(self.trench, 1)
        self.offset += np.array((1, 1))

    def fill_trench(self, start_position=None):
        if start_position is None:
            start_position = -self.offset
        queue = [np.array(start_position)]
        while queue:
            current_position = queue.pop(0)
            if self.get_position(current_position) == 0:
                self.set_position(current_position, -1)
                for direction in CHAR_TO_DIRECTION.values():
                    queue.append(current_position + direction)
        self.trench = np.where(self.trench >= 0, 1, 0)
