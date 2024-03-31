from parse import parse_file
import numpy as np


def parse_input(filename):
    data = parse_file(filename)
    pictures = []
    cur_picture = []
    for row in data:
        if row == '':
            pictures.append(np.array(cur_picture))
            cur_picture = []
        else:
            cur_picture.append(list(row))
    pictures.append(np.array(cur_picture))
    return pictures


def solve_part1(filename):
    pictures = parse_input(filename)

    solution = 0
    for picture in pictures:
        reflection_characteristic = None
        vertical_reflection_result = check_for_vertical_reflection(picture)
        if vertical_reflection_result is not None:
            reflection_characteristic = vertical_reflection_result + 1
            print(
                f'{picture}\nVertical reflection axis: {vertical_reflection_result}')
        else:
            horizontal_reflection_axis = check_for_horizontal_reflection(
                picture)
            reflection_characteristic = 100 * (horizontal_reflection_axis + 1)
            print(
                f'{picture}\nHorizontal reflection axis: {horizontal_reflection_axis}')
        solution += reflection_characteristic
    print(solution)


def solve_part2(filename):
    pictures = parse_input(filename)

    solution = 0
    for picture in pictures:
        solution += get_smudged_reflection_characteristic(picture)
    print(solution)


def check_for_vertical_reflection(picture):
    for i in range(picture.shape[1] - 1):
        index = i
        index_reflection = index + 1
        reflects_correctly = True
        while index >= 0 and index_reflection < picture.shape[1]:
            if not np.array_equal(picture[:, index], picture[:, index_reflection]):
                reflects_correctly = False
                break
            index -= 1
            index_reflection += 1
        if reflects_correctly:
            return i
    return None


def check_for_horizontal_reflection(picture):
    for i in range(picture.shape[0] - 1):
        index = i
        index_reflection = index + 1
        reflects_correctly = True
        while index >= 0 and index_reflection < picture.shape[0]:
            if not np.array_equal(picture[index], picture[index_reflection]):
                reflects_correctly = False
                break
            index -= 1
            index_reflection += 1
        if reflects_correctly:
            return i
    return None


def get_smudged_reflection_characteristic(picture):
    vert_result = check_for_smudged_vertical_reflection(picture)
    if vert_result is not None:
        print(f'{picture}\nVertical reflection axis: {vert_result}')
        return vert_result + 1

    horz_result = check_for_smudged_horizontal_reflection(picture)
    print(f'{picture}\nHorizontal reflection axis: {horz_result}')
    return (horz_result + 1) * 100


def check_for_smudged_vertical_reflection(picture):
    for i in range(picture.shape[1] - 1):
        index = i
        index_reflection = index + 1
        reflects_correctly = True
        is_smudge_fix_available = True
        while index >= 0 and index_reflection < picture.shape[1]:
            mismatch_count = np.count_nonzero(
                np.where(picture[:, index] != picture[:, index_reflection], 1, 0))
            if mismatch_count >= 2 or (mismatch_count == 1 and not is_smudge_fix_available):
                reflects_correctly = False
                break
            if mismatch_count == 1:
                is_smudge_fix_available = False
            index -= 1
            index_reflection += 1
        if reflects_correctly and not is_smudge_fix_available:
            return i
    return None


def check_for_smudged_horizontal_reflection(picture):
    for i in range(picture.shape[0] - 1):
        index = i
        index_reflection = index + 1
        reflects_correctly = True
        is_smudge_fix_available = True
        while index >= 0 and index_reflection < picture.shape[0]:
            mismatch_count = np.count_nonzero(
                np.where(picture[index] != picture[index_reflection], 1, 0))
            if mismatch_count >= 2 or (mismatch_count == 1 and not is_smudge_fix_available):
                reflects_correctly = False
                break
            if mismatch_count == 1:
                is_smudge_fix_available = False
            index -= 1
            index_reflection += 1
        if reflects_correctly and not is_smudge_fix_available:
            return i
    return None


if __name__ == '__main__':
    solve_part2('input')
