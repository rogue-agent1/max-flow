#!/usr/bin/env python3
"""Max flow — Ford-Fulkerson with BFS (Edmonds-Karp)."""
import sys
from collections import defaultdict, deque

class MaxFlow:
    def __init__(self, n):
        self.n = n
        self.cap = defaultdict(lambda: defaultdict(int))
        self.adj = defaultdict(set)
    def add_edge(self, u, v, c):
        self.cap[u][v] += c
        self.adj[u].add(v)
        self.adj[v].add(u)
    def _bfs(self, s, t, parent):
        visited = {s}
        q = deque([s])
        while q:
            u = q.popleft()
            for v in self.adj[u]:
                if v not in visited and self.cap[u][v] > 0:
                    visited.add(v)
                    parent[v] = u
                    if v == t: return True
                    q.append(v)
        return False
    def max_flow(self, s, t):
        flow = 0
        while True:
            parent = {}
            if not self._bfs(s, t, parent): break
            path_flow = float('inf')
            v = t
            while v != s:
                u = parent[v]
                path_flow = min(path_flow, self.cap[u][v])
                v = u
            v = t
            while v != s:
                u = parent[v]
                self.cap[u][v] -= path_flow
                self.cap[v][u] += path_flow
                v = u
            flow += path_flow
        return flow

def test():
    mf = MaxFlow(6)
    mf.add_edge(0,1,16); mf.add_edge(0,2,13)
    mf.add_edge(1,2,10); mf.add_edge(1,3,12)
    mf.add_edge(2,1,4); mf.add_edge(2,4,14)
    mf.add_edge(3,2,9); mf.add_edge(3,5,20)
    mf.add_edge(4,3,7); mf.add_edge(4,5,4)
    assert mf.max_flow(0, 5) == 23
    mf2 = MaxFlow(2)
    mf2.add_edge(0,1,5)
    assert mf2.max_flow(0, 1) == 5
    print("  max_flow: ALL TESTS PASSED")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Max flow (Edmonds-Karp)")
