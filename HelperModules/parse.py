def parse_line_raw(line):
    return line


def parse_file(filename, parse_line=parse_line_raw):
    with open(filename, 'r') as file:
        lines = file.readlines()
        lines = list(map(lambda line: line.split('\n')[0], lines))
        if lines[-1] == '':
            lines.pop()

    parsed_file = list(map(parse_line, lines))
    return parsed_file
