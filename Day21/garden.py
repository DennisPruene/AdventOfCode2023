import numpy as np

DIRS = [np.array((1, 0)), np.array((0, 1)),
        np.array((-1, 0)), np.array((0, -1))]
DIAG_DIRS = [np.array((-1, -1)), np.array((1, -1)),
             np.array((1, 1)), np.array((-1, 1))]
BUCKETS = [np.array((0, 0))] + DIRS + DIAG_DIRS


class Garden:
    def __init__(self, tile):
        self.length = tile.shape[0]
        if tile.shape[0] != tile.shape[1]:
            print("Error: only square shaped tiles allowed!")
        (y,), (x,) = np.where(tile == 'S')
        self.start_pos = (y, x)
        self.start_dist = y
        if y != x or self.length - y - 1 != x:
            print("Error: Starting position has to be in the precise middle of the tile!")
        tile[self.start_pos] = '.'
        self.tile = np.where(tile == '#', False, True)
        self.padded_tile = np.pad(self.tile, 1, constant_values=False)
        self.reachability_masks_by_bucket = {tuple(bucket): self.compute_reachable_masks(
            self.start_pos - bucket * self.start_dist) for bucket in BUCKETS}
        self.filled_plot_count = {bucket: [np.count_nonzero(mask) for mask in masks] for (
            bucket, masks) in self.reachability_masks_by_bucket.items()}
        self.steps_to_fill = {bucket: max(np.max(masks[0]), np.max(
            masks[1])) - 1 for (bucket, masks) in self.reachability_masks_by_bucket.items()}
        self.unfilled_plot_counts = {bucket: [np.count_nonzero(
            np.where(masks[i % 2] > i + 1, 0, masks[i % 2]))
            for i in range(self.steps_to_fill[bucket])] for
            (bucket, masks) in self.reachability_masks_by_bucket.items()}

    def from_file(filename):
        with open(filename, 'r') as file:
            lines = file.readlines()

        tile = np.array(list(map(lambda line: list(
            line[:-1]), filter(lambda line: line != '\n', lines))))
        return Garden(tile)

    def tile_to_string(self):
        return '\n'.join((''.join(row) for row in np.where(self.tile, '.', '#')))

    def compute_reachable_masks(self, start_position) -> np.ndarray:
        start_position = np.array(start_position)
        print(start_position)
        masks = [np.zeros_like(self.tile, dtype=int),
                 np.zeros_like(self.tile, dtype=int)]
        masks[0][tuple(start_position)] = 1
        current_point_queue = [start_position]
        current_step = 2
        current_mode = 1
        while current_point_queue:
            next_point_queue = []
            for current_point in current_point_queue:
                for direction in DIRS:
                    next_point = current_point + direction
                    if self.padded_tile[tuple(next_point + 1)] and masks[current_mode][tuple(next_point)] == 0:
                        masks[current_mode][tuple(next_point)] = current_step
                        next_point_queue.append(next_point)
            current_point_queue = next_point_queue
            current_step += 1
            current_mode = 1 - current_mode
        return masks

    def compute_reachable_plot_count(self, steps):
        reachable_plot_count = self.compute_reachable_plot_count_for_tile(
            steps, (0, 0))
        current_distance = 1
        while self.compute_reachable_plot_count_for_tile(steps, (current_distance - 1, 1)) > 0:
            for direction in DIRS:
                reachable_plot_count += self.compute_reachable_plot_count_for_tile(
                    steps, direction * current_distance)
            for direction in DIAG_DIRS:
                tile_point = np.array((current_distance - 1, 1))
                tile_point[0] *= direction[0]
                tile_point[1] *= direction[1]
                reachable_plot_count += (current_distance - 1) * \
                    self.compute_reachable_plot_count_for_tile(
                        steps, tile_point)
            current_distance += 1
        return reachable_plot_count

    def compute_reachable_plot_count_for_tile(self, steps_left, tile_point):
        steps_left -= self.compute_steps_necessary_to_reach_tile(tile_point)
        if steps_left < 0:
            return 0

        modality = steps_left % 2
        bucket = np.sign(tile_point)
        if steps_left < self.steps_to_fill[tuple(bucket)]:
            return self.reachable_plot_count_unfilled_tile(bucket, steps_left)
        else:
            return self.filled_plot_count[tuple(bucket)][modality]

    def compute_steps_necessary_to_reach_tile(self, tile_point):
        return self.length * np.sum(np.abs(tile_point)) - self.start_dist * np.sum(np.abs(np.sign(tile_point)))

    def reachable_plot_count_unfilled_tile(self, bucket, steps_left):
        return self.unfilled_plot_counts[tuple(bucket)][steps_left]

    def compute_inner_area_radius(self, steps):
        return (steps - self.length) // self.length

    def compute_inner_area(self, steps):
        fill_radius = self.compute_inner_area_radius(steps)
        green_tile_count = 1 + 4 * \
            (fill_radius // 2) * ((fill_radius // 2) + 1)
        red_tile_count = 4 * ((fill_radius // 2) + (fill_radius % 2))**2
        modality = steps % 2
        return green_tile_count * self.filled_plot_count[(0, 0)][modality] \
            + red_tile_count * self.filled_plot_count[(0, 0)][1 - modality]

    def compute_plot_count_optimized(self, steps):
        inner_area = self.compute_inner_area(steps)
        perimeter = 0
        reachable_radius = (steps + self.length - 1) // self.length
        fill_radius = self.compute_inner_area_radius(steps)
        for current_distance in range(fill_radius + 1, reachable_radius + 1):
            for direction in DIRS:
                perimeter += self.compute_reachable_plot_count_for_tile(
                    steps, direction * current_distance)
            for direction in DIAG_DIRS:
                tile_point = np.array((current_distance - 1, 1))
                tile_point[0] *= direction[0]
                tile_point[1] *= direction[1]
                perimeter += (current_distance - 1) * \
                    self.compute_reachable_plot_count_for_tile(
                        steps, tile_point)
        return inner_area + perimeter


def generate_integer_points(limit=float('inf')):
    current_point = np.array((0, 0))
    yield current_point
    while np.sum(np.abs(current_point)) < limit:
        # yield current_point
        current_point += np.array((0, 1))
        for direction in DIAG_DIRS:
            yield current_point
            current_point += direction
            while current_point[0] != 0 and current_point[1] != 0:
                yield current_point
                current_point += direction


if __name__ == '__main__':
    garden: Garden = Garden.from_file('input')
    print("Initialization done!")
    # print(garden.tile_to_string())

    # for point in generate_integer_points(5):
    #     print(f'{point}: {garden.compute_reachable_plot_count_for_tile(10001, point)}')

    print(garden.compute_plot_count_optimized(26501365))
    print(garden.compute_plot_count_optimized(26501365000000000))
