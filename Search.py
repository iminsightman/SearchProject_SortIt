from Solution import Solution
from Problem import Problem
from datetime import datetime
import heapq
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritizedItem:
    priority: int
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


  def dfs_limited(prb: Problem, depth: int) -> State:
        stack = []
        state = prb.initState
        stack.append(state)
        visited = set()
        visited.add(state.__hash__())
        while len(stack) > 0:
            state = stack.pop()
            if prb.is_goal(state):
                return state
            if state.g_n < depth:
                neighbors = prb.successor(state)
                for c in neighbors:
                    if c.__hash__() not in visited:
                        visited.add(c.__hash__())
                        stack.append(c)
        return None

     def ids(prb: Problem) -> Solution:
            start_time = datetime.now()
            depth = 0
            while True:
                result = dfs_limited(prb, depth)
                if result is not None:
                    return Solution(result, prb, start_time)
                depth += 1