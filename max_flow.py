#!/usr/bin/env python3
"""max_flow - Maximum flow algorithms (Ford-Fulkerson with BFS/Edmonds-Karp)."""
import sys
from collections import deque

class FlowNetwork:
    def __init__(self, n):
        self.n = n
        self.capacity = [[0]*n for _ in range(n)]
        self.flow = [[0]*n for _ in range(n)]

    def add_edge(self, u, v, cap):
        self.capacity[u][v] += cap

    def _bfs(self, source, sink, parent):
        visited = [False]*self.n
        visited[source] = True
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v in range(self.n):
                if not visited[v] and self.capacity[u][v] - self.flow[u][v] > 0:
                    visited[v] = True
                    parent[v] = u
                    if v == sink:
                        return True
                    queue.append(v)
        return False

    def max_flow(self, source, sink):
        total = 0
        parent = [-1]*self.n
        while self._bfs(source, sink, parent):
            path_flow = float('inf')
            v = sink
            while v != source:
                u = parent[v]
                path_flow = min(path_flow, self.capacity[u][v] - self.flow[u][v])
                v = u
            v = sink
            while v != source:
                u = parent[v]
                self.flow[u][v] += path_flow
                self.flow[v][u] -= path_flow
                v = u
            total += path_flow
            parent = [-1]*self.n
        return total

    def min_cut(self, source):
        visited = [False]*self.n
        queue = deque([source])
        visited[source] = True
        while queue:
            u = queue.popleft()
            for v in range(self.n):
                if not visited[v] and self.capacity[u][v] - self.flow[u][v] > 0:
                    visited[v] = True
                    queue.append(v)
        cut_edges = []
        for u in range(self.n):
            for v in range(self.n):
                if visited[u] and not visited[v] and self.capacity[u][v] > 0:
                    cut_edges.append((u, v))
        return cut_edges

def test():
    g = FlowNetwork(6)
    g.add_edge(0,1,16); g.add_edge(0,2,13)
    g.add_edge(1,2,10); g.add_edge(1,3,12)
    g.add_edge(2,1,4);  g.add_edge(2,4,14)
    g.add_edge(3,2,9);  g.add_edge(3,5,20)
    g.add_edge(4,3,7);  g.add_edge(4,5,4)
    assert g.max_flow(0, 5) == 23
    cut = g.min_cut(0)
    assert len(cut) > 0
    g2 = FlowNetwork(4)
    g2.add_edge(0,1,10); g2.add_edge(0,2,10)
    g2.add_edge(1,3,10); g2.add_edge(2,3,10)
    assert g2.max_flow(0, 3) == 20
    g3 = FlowNetwork(2)
    g3.add_edge(0,1,5)
    assert g3.max_flow(0, 1) == 5
    print("All tests passed!")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("max_flow: Maximum flow. Use --test")
