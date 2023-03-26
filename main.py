from Pipe import Pipe
from Problem import Problem
from State import State
from Search import Search
import numpy as np


def build_random_problem(n_pipes, limit, colors):
    p = []
    balls = []
    for color in colors:
        balls.extend([color]*limit)
    balls = np.array(balls)
    np.random.shuffle(balls)
    balls = list(balls)
    for _ in range(n_pipes):
        p.append(Pipe(balls[:limit], limit))
        balls = balls[limit:]
    init_state = State(p, None, 0, (0, 0))
    prb = Problem(init_state)
    return prb


if __name__ == '__main__':
    """test_path = 'tests/test5.txt'
    file = open(test_path, 'r')
    p = []
    for i in file.readlines():
        a = i.replace('\n', '')
        a = a.replace(' ', '')
        a = a.split(',')
        p.append(Pipe(a[:-1], int(a[-1])))"""
    
    prb = build_random_problem(5, 4, ['red', 'green', 'blue', 'white'])
    s = Search.a_star(prb)
    s.print_path()
    s.execute_gui()
