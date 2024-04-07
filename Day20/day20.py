import re
from parse import parse_file
from typing import List, Tuple

Pulse = Tuple[str, bool, str]


class Module:
    def __init__(self, name: str, destination_modules: List[str]):
        self.name = name
        self.destination_modules = destination_modules
        self.source_modules = None

    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name

    def __repr__(self) -> str:
        return f'{type(self).module_prefix()}{self.name} -> {self.destination_modules}'

    def set_source_modules(self, source_modules):
        self.source_modules = source_modules

    def receive_pulse(self, source_module: str, signal: bool) -> List[Pulse]:
        return []

    def module_prefix() -> str:
        return ''


class BroadcasterModule(Module):
    def __init__(self, name: str, destination_modules: List[str]):
        super().__init__(name, destination_modules)

    def receive_pulse(self, source_module: str, signal: bool) -> List[Pulse]:
        return [(self.name, signal, destination_module) for destination_module in self.destination_modules]

    def module_prefix() -> str:
        return 'broadcaster'


class FlipFlopModule(Module):
    def __init__(self, name: str, destination_modules: List[str]):
        super().__init__(name, destination_modules)
        self.is_on = False

    def __eq__(self, __value: object) -> bool:
        if not super().__eq__(__value):
            return False
        return self.is_on == __value.is_on

    def __repr__(self) -> str:
        return super().__repr__() + f', is_on = {self.is_on}'

    def receive_pulse(self, source_module: str, signal: bool) -> List[Pulse]:
        if signal:
            return []
        else:
            self.is_on = not self.is_on
            return [(self.name, self.is_on, destination_module) for destination_module in self.destination_modules]

    def module_prefix() -> str:
        return '%'


class ConjunctionModule(Module):
    def __init__(self, name: str, destination_modules: List[str]):
        super().__init__(name, destination_modules)
        self.memory = {}

    def __eq__(self, __value: object) -> bool:
        if not super().__eq__(__value):
            return False
        for (source_module, last_signal) in self.memory.items():
            if source_module in __value.memory:
                if last_signal != __value.memory[source_module]:
                    return False
            else:
                if last_signal:
                    return False
        for (source_module, last_signal) in __value.memory.items():
            if source_module in self.memory:
                if last_signal != self.memory[source_module]:
                    return False
            else:
                if last_signal:
                    return False
        return True

    def __repr__(self) -> str:
        return super().__repr__() + f', memory = {self.memory}'

    def set_source_modules(self, source_modules):
        super().set_source_modules(source_modules)
        self.memory = {
            source_module: False for source_module in source_modules}

    def receive_pulse(self, source_module: str, signal: bool) -> List[Pulse]:
        self.memory[source_module] = signal
        signal = not all(self.memory.values())
        return [(self.name, signal, destination_module) for destination_module in self.destination_modules]

    def module_prefix() -> str:
        return '&'


MODULE_TYPES = [BroadcasterModule, FlipFlopModule, ConjunctionModule]


def parse_line(line):
    match = re.match("(broadcaster|%|&)([a-z]*) -> ([a-z, ]+)", line)
    (module_prefix, module_name, destination_modules) = match.groups()
    destination_modules = destination_modules.split(', ')
    for ModuleType in MODULE_TYPES:
        if module_prefix == ModuleType.module_prefix():
            return ModuleType(module_name, destination_modules)


def connect_source_modules(modules):
    source_module_map = {module: [] for module in modules.keys()}
    for module in modules.values():
        for destination_module in module.destination_modules:
            if destination_module in source_module_map:
                source_module_map[destination_module].append(module.name)
    for (module_name, source_modules) in source_module_map.items():
        modules[module_name].set_source_modules(source_modules)


def press_button(modules, watch_for_module='rx'):
    pulse_queue = [('button', False, '')]
    low_pulse_count = 0
    high_pulse_count = 0
    has_watched_module_received_low_pulse = False
    while pulse_queue:
        (source_module, signal, destination_module) = pulse_queue.pop(0)
        if destination_module == watch_for_module and not signal:
            has_watched_module_received_low_pulse = True
        # if signal:
        #     print(f'{source_module} high-> {destination_module}')
        # else:
        #     print(f'{source_module} low-> {destination_module}')
        if signal:
            high_pulse_count += 1
        else:
            low_pulse_count += 1
        if destination_module in modules:
            pulse_queue.extend(
                modules[destination_module].receive_pulse(source_module, signal))
    return (low_pulse_count, high_pulse_count, has_watched_module_received_low_pulse)


def solve_part1(filename):
    modules = parse_file(filename, parse_line)
    modules = {module.name: module for module in modules}
    connect_source_modules(modules)
    # print(modules)
    low_pulse_count, high_pulse_count = 0, 0
    for _ in range(1000):
        dl, dh, _ = press_button(modules)
        low_pulse_count, high_pulse_count = low_pulse_count + dl, high_pulse_count + dh
    print(f'{low_pulse_count} * {high_pulse_count} = {low_pulse_count * high_pulse_count}')


def solve_part2(filename):
    modules = parse_file(filename, parse_line)
    modules = {module.name: module for module in modules}
    connect_source_modules(modules)
    has_rx_received_low_pulse = False
    button_presses = 0
    while not has_rx_received_low_pulse:
        _, _, has_rx_received_low_pulse = press_button(modules)
        button_presses += 1
        if button_presses % 1e6 == 0:
            print(button_presses)
    print(button_presses)


if __name__ == '__main__':
    solve_part1('input')
    solve_part2('input')
