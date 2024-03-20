import re

digits_spelled_out = ['zero', 'one', 'two', 'three',
                      'four', 'five', 'six', 'seven', 'eight', 'nine']
digit_finder_forwards_re = '[0-9]|' + \
    '|'.join(map(lambda s: s, digits_spelled_out))
digit_finder_backwards_re = '[0-9]|' + \
    '|'.join(map(lambda s: s[::-1], digits_spelled_out))
digit_finder_forwards = re.compile(digit_finder_forwards_re)
digit_finder_backards = re.compile(digit_finder_backwards_re)


def solve(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        lines = list(map(lambda line: line.split('\n')[0], lines))
        if lines[-1] == '':
            lines.pop()
    calibration_value_sum = 0
    for line in lines:
        calibration_value_sum += get_calibration_value(line)
    print(calibration_value_sum)


def get_first_calibration_digit(string):
    digit_string = digit_finder_forwards.search(string).group()
    return convert_digit_string_to_int(digit_string)


def get_last_calibration_digit(string):
    digit_string = digit_finder_backards.search(string[::-1]).group()[::-1]
    return convert_digit_string_to_int(digit_string)


def get_calibration_value(string):
    first_digit = get_first_calibration_digit(string)
    last_digit = get_last_calibration_digit(string)
    return int(str(first_digit) + str(last_digit))


def convert_digit_string_to_int(digit_string):
    for (digit, digit_as_word) in enumerate(digits_spelled_out):
        if digit_string == digit_as_word:
            return digit
    return int(digit_string)


if __name__ == "__main__":
    solve('input')
