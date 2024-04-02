class PriorityQueue:
    def __init__(self):
        self.queue = [None]
        self.priorities = {}
        self.indices = {}

    def __len__(self):
        return len(self.queue) - 1

    def __bool__(self):
        return len(self) > 0

    def bubble_up(self, value):
        current_index = self.indices[value]
        while current_index > 1 and self.priorities[self.queue[current_index // 2]] > self.priorities[value]:
            self.indices[self.queue[current_index // 2]] = current_index
            self.queue[current_index] = self.queue[current_index // 2]
            self.queue[current_index // 2] = value
            current_index //= 2
        self.indices[value] = current_index

    def add_with_priority(self, value, priority):
        self.priorities[value] = priority
        self.queue.append(value)
        self.indices[value] = len(self.queue) - 1
        self.bubble_up(value)

    def decrease_priority(self, value, priority):
        self.priorities[value] = priority
        self.bubble_up(value)

    def extract_min(self):
        if len(self.queue) == 2:
            return self.queue.pop()
        elif len(self.queue) == 1:
            raise IndexError
        result = self.queue[1]
        removed_value = self.queue.pop()
        self.queue[1] = removed_value
        current_index = 1
        while 2 * current_index < len(self.queue):
            min_priority = self.priorities[self.queue[current_index]]
            min_index = current_index
            if self.priorities[self.queue[2 * current_index]] < min_priority:
                min_priority = self.priorities[self.queue[2 * current_index]]
                min_index = 2 * current_index
            if 2 * current_index + 1 < len(self.queue) and self.priorities[self.queue[2 * current_index + 1]] < min_priority:
                min_priority = self.priorities[self.queue[2 *
                                                          current_index + 1]]
                min_index = 2 * current_index + 1
            if min_index == current_index:
                break
            self.queue[current_index] = self.queue[min_index]
            current_index = min_index
            self.indices[self.queue[current_index]] = current_index
        self.queue[current_index] = removed_value
        self.indices[removed_value] = current_index
        return result


if __name__ == '__main__':
    queue = PriorityQueue()
    removed_order = []
    queue.add_with_priority(1, 100)
    queue.add_with_priority(2, 25)
    queue.add_with_priority(3, 500)
    removed_order.append(queue.extract_min())
    queue.add_with_priority(4, 20)
    queue.add_with_priority(5, 5)
    queue.decrease_priority(3, 75)
    removed_order.append(queue.extract_min())
    queue.add_with_priority(6, 40)
    queue.decrease_priority(1, 15)
    removed_order.append(queue.extract_min())
    removed_order.append(queue.extract_min())
    removed_order.append(queue.extract_min())
    removed_order.append(queue.extract_min())
    print(removed_order)
