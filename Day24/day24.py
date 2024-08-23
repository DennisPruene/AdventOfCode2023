import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from HelperModules.parse import parse_file, extract_integers
import numpy as np
import sympy as sym

def parse_input(filename, ignore_z=False):
    input = parse_file(filename, extract_integers)
    if ignore_z:
        positions = np.asarray([row[:2] for row in input])
        velocities = np.asarray([row[3:5] for row in input])
    else:
        positions = np.asarray([row[:3] for row in input])
        velocities = np.asarray([row[3:] for row in input])
    return (positions, velocities)

def linalg_solve(A, b):
    try:
        x = np.linalg.solve(A, b)
        return x
    except Exception:
        return None
    
def does_path_intersect_box(p, v, l, r, u, d):
    if p[0] >= l and p[0] <= r and p[1] >= d and p[1] <= u:
        return True
    if p[0] < l and v[0] > 0:
        t = (l - p[0]) / v[0]
        y = p[1] + t*v[1]
        if y >= d and y <= u:
            return True
    return False 
    
def is_intersection_in_bounds(p, v, q, w, lower_bound=200000000000000, upper_bound=400000000000000):
    A = np.zeros((2, 2), dtype=int)
    A[:, 0] = v
    A[:, 1] = -w
    b = q - p
    x = linalg_solve(A, b)
    if x is None:
        return does_path_intersect_box(p, v, lower_bound, upper_bound, lower_bound, upper_bound)
    if x[0] < 0 or x[1] < 0:
        return False
    intersection = p + x[0]*v
    return intersection[0] >= lower_bound and intersection[0] <= upper_bound and intersection[1] >= lower_bound and intersection[1] <= upper_bound

    

def solve_part1(filename):
    (positions, velocities) = parse_input(filename, ignore_z=True)
    result = 0
    for (i, (p, v)) in enumerate(zip(positions, velocities)):
        for q, w in zip(positions[i+1:], velocities[i+1:]):
            if is_intersection_in_bounds(p, v, q, w):
                result += 1
    print(result)

def solve_for_colliding_bullet(p1, v1, p2, v2, p3, v3):
    t1 = sym.Symbol("t1")
    t2 = sym.Symbol("t2")
    t3 = sym.Symbol("t3")
    A = sym.Matrix([[(p3 - p2)[0], (p1 - p3)[0], (p2 - p1)[0]], 
                    [(p3 - p2)[1], (p1 - p3)[1], (p2 - p1)[1]], 
                    [(p3 - p2)[2], (p1 - p3)[2], (p2 - p1)[2]]])
    B = sym.Matrix([[(v2 - v3)[0], (v3 - v1)[0], (v1 - v2)[0]],
                    [(v2 - v3)[1], (v3 - v1)[1], (v1 - v2)[1]],
                    [(v2 - v3)[2], (v3 - v1)[2], (v1 - v2)[2]]])
    term = A * sym.Matrix([[t1], [t2], [t3]]) + B * sym.Matrix([[t2 * t3], [t1 * t3], [t1 * t2]])
    return sym.solve(term, (t1, t2, t3))

def filter_possible_collision_timings(possible_solutions):
    solutions = []
    for possible_solution in possible_solutions:
        is_correct = True
        for i, val in enumerate(possible_solution):
            for val2 in possible_solution[i+1:]:
                if val == val2:
                    is_correct = False
                    break
            if not is_correct:
                break
            if val < 0:
                is_correct = False
                break
            if not val.is_integer:
                is_correct = False
                break
        if is_correct:
            solutions.append(possible_solution)
    return solutions

def compute_collision_path_from_collision_timings(p1, v1, p2, v2, p3, v3, collision_timings):
    v = (p2 - p1 + collision_timings[1]*v2 - collision_timings[0]*v1) // (collision_timings[1] - collision_timings[0])
    p = p1 + collision_timings[0]*(v1 - v)
    print(p)
    print(sum(p))
    assert (p + collision_timings[0] * v == p1 + collision_timings[0] * v1).all()
    assert (p + collision_timings[1] * v == p2 + collision_timings[1] * v2).all()
    assert (p + collision_timings[2] * v == p3 + collision_timings[2] * v3).all()
    return (p, v)


def solve_part2(filename):
    (positions, velocities) = parse_input(filename)
    p1 = positions[0]
    p2 = positions[1]
    p3 = positions[2]
    v1 = velocities[0]
    v2 = velocities[1]
    v3 = velocities[2]
    possible_solutions = solve_for_colliding_bullet(p1, v1, p2, v2, p3, v3)
    solutions = filter_possible_collision_timings(possible_solutions)
    compute_collision_path_from_collision_timings(p1, v1, p2, v2, p3, v3, solutions[0])


if __name__ == '__main__':
    solve_part2('input.txt')
