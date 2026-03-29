#!/usr/bin/env python3
"""max_flow - Ford-Fulkerson max flow with BFS (Edmonds-Karp)."""
import sys
from collections import defaultdict, deque

class FlowNetwork:
    def __init__(self):
        self.graph = defaultdict(lambda: defaultdict(int))
        self.nodes = set()
    def add_edge(self, u, v, cap):
        self.graph[u][v] += cap
        self.nodes.update([u, v])
    def _bfs(self, s, t, parent):
        visited = {s}
        q = deque([s])
        while q:
            u = q.popleft()
            for v in self.graph[u]:
                if v not in visited and self.graph[u][v] > 0:
                    visited.add(v)
                    parent[v] = u
                    if v == t: return True
                    q.append(v)
        return False
    def max_flow(self, s, t):
        rg = defaultdict(lambda: defaultdict(int))
        for u in self.graph:
            for v in self.graph[u]:
                rg[u][v] = self.graph[u][v]
        total = 0
        while True:
            parent = {}
            visited = {s}
            q = deque([s])
            found = False
            while q:
                u = q.popleft()
                for v in rg[u]:
                    if v not in visited and rg[u][v] > 0:
                        visited.add(v)
                        parent[v] = u
                        if v == t: found = True; break
                        q.append(v)
                if found: break
            if not found: break
            flow = float("inf")
            v = t
            while v != s:
                u = parent[v]
                flow = min(flow, rg[u][v])
                v = u
            v = t
            while v != s:
                u = parent[v]
                rg[u][v] -= flow
                rg[v][u] += flow
                v = u
            total += flow
        return total

def test():
    fn = FlowNetwork()
    fn.add_edge("s", "a", 10)
    fn.add_edge("s", "b", 5)
    fn.add_edge("a", "b", 15)
    fn.add_edge("a", "t", 10)
    fn.add_edge("b", "t", 10)
    assert fn.max_flow("s", "t") == 15
    fn2 = FlowNetwork()
    fn2.add_edge(0, 1, 3)
    fn2.add_edge(0, 2, 2)
    fn2.add_edge(1, 3, 2)
    fn2.add_edge(2, 3, 3)
    fn2.add_edge(1, 2, 1)
    assert fn2.max_flow(0, 3) == 5
    print("max_flow: all tests passed")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("Usage: max_flow.py --test")
