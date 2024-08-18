import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from HelperModules.parse import parse_file, extract_integers
import numpy as np

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




if __name__ == '__main__':
    solve_part1('input.txt')
