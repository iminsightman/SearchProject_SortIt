from Solution import Solution
from Problem import Problem
from datetime import datetime
import heapq
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritizedItem:
    priority: float
    item: Any=field(compare=False)

class Search:
    @staticmethod
    def bfs(prb: Problem) -> Solution:  # this method get a first state of Problem and do bfs for find solution if no
        # solution is find return None else return the solution
        start_time = datetime.now()
        queue = []
        state = prb.initState
        queue.append(state)
        while len(queue) > 0:
            state = queue.pop(0)
            neighbors = prb.successor(state)
            for c in neighbors:
                if prb.is_goal(c):
                    return Solution(c, prb, start_time)
                queue.append(c)
        return None
    
    @staticmethod
    def dfs(prb: Problem) -> Solution:
        start_time = datetime.now()
        stack = []
        state = prb.initState
        stack.append(state)
        while len(stack) > 0:
            state = stack.pop()
            neighbors = prb.successor(state)
            for c in neighbors:
                if prb.is_goal(c):
                    return Solution(c, prb, start_time)
                stack.append(c)
        return None

    @staticmethod
    def dfs1(prb: Problem) -> Solution:
        start_time = datetime.now()
        stack = []
        state = prb.initState
        visited = set()
        stack.append(state)
        visited.add(state.__hash__())
        while len(stack) > 0:
            state = stack.pop()
            neighbors = prb.successor(state)
            for c in neighbors:
                if c.__hash__ not in visited:
                    visited.add(c.__hash__)
                    if prb.is_goal(c):
                        return Solution(c, prb, start_time)
                    stack.append(c)
        return None

    @staticmethod
    def ucs(prb: Problem) -> Solution:
        start_time = datetime.now()
        queue = []
        state = prb.initState
        visited = set()
        heapq.heappush(queue, PrioritizedItem(state.g_n, state))
        visited.add(state.__hash__())
        while len(queue) > 0:
            state = heapq.heappop(queue).item
            neighbors = prb.successor(state)
            for c in neighbors:
                if c.__hash__() not in visited:
                    visited.add(c.__hash__())
                    if prb.is_goal(c):
                        return Solution(c, prb, start_time)
                    heapq.heappush(queue, PrioritizedItem(c.g_n, c))
        return None
    
    @staticmethod
    def a_star(prb: Problem) -> Solution:
        start_time = datetime.now()
        queue = []
        state = prb.initState
        visited = set()
        heapq.heappush(queue, PrioritizedItem(state.g_n+prb.heuristc(state), state))
        visited.add(state.__hash__())
        while len(queue) > 0:
            state = heapq.heappop(queue).item
            neighbors = prb.successor(state)
            for c in neighbors:
                if c.__hash__() not in visited:
                    visited.add(c.__hash__())
                    if prb.is_goal(c):
                        return Solution(c, prb, start_time)
                    heapq.heappush(queue, PrioritizedItem(c.g_n+prb.heuristc(c), c))
        return None


    def dfs_limited(prb: Problem, depth: int , start_time) -> Solution:
        stack = []
        state = prb.initState
        stack.append(state)
        visited = set()
        visited.add(state.__hash__())
        while len(stack) > 0:
            state = stack.pop()
            if state.g_n < depth:
                neighbors = prb.successor(state)
                for c in neighbors:
                    if c.__hash__() not in visited:
                        visited.add(c.__hash__())
                        if prb.is_goal(c):
                            return Solution(c, prb, start_time)
                        stack.append(c)
        return None


    def ids(prb: Problem) -> Solution:
        start_time = datetime.now()
        depth = 0
        while True:
            result = dfs_limited(prb, depth , start_time )
            if result is not None:
                return result
            depth += 1

     def rbfs(prb: Problem) -> Solution:
            start_time = datetime.now()
            state = prb.initState
            visited = set()
            visited.add(state.__hash__())
            solution, _ = rbfs1(prb ,state, float('inf'), visited,  start_time)
            return solution


    def rbfs1(state, f_limit, visited, prb, start_time):

        if prb.is_goal(state):
            return Solution(state, prb, start_time), 0
        successors = prb.successor(state)
        if not successors:
            return None, float('inf')
        for c in successors:
            if c.__hash__() in visited:
                continue
            visited.add(c.__hash__())
            c.f_n = prb.heuristic(c)
        heap = [(c.f_n, c) for c in successors]
        heapq.heapify(heap)
        while True:
            best_f_n, best = heapq.heappop(heap)
            if best_f_n > f_limit:
                return None, best_f_n
            if len(heap) > 0:
                alternative_f_n, alternative = heapq.heappop(heap)
                heapq.heappush(heap, (alternative_f_n, alternative))
                result, best.f_n = rbfs1(best, min(f_limit, alternative_f_n), visited, prb, start_time)
            else:
                result, best.f_n = rbfs1(best, f_limit, visited, prb, start_time)
            if result:
                return result, 0
            heapq.heappush(heap, (best.f_n, best))
