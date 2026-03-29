#!/usr/bin/env python3
"""max_flow: Ford-Fulkerson max flow (BFS/Edmonds-Karp)."""
from collections import deque
import sys

def max_flow(capacity, source, sink):
    n = len(capacity)
    residual = [row[:] for row in capacity]
    total = 0
    while True:
        parent = [-1] * n
        parent[source] = source
        queue = deque([source])
        while queue and parent[sink] == -1:
            u = queue.popleft()
            for v in range(n):
                if parent[v] == -1 and residual[u][v] > 0:
                    parent[v] = u
                    queue.append(v)
        if parent[sink] == -1: break
        # Find bottleneck
        path_flow = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, residual[u][v])
            v = u
        # Update residual
        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= path_flow
            residual[v][u] += path_flow
            v = u
        total += path_flow
    return total

def min_cut(capacity, source, sink):
    n = len(capacity)
    residual = [row[:] for row in capacity]
    # Run max flow first
    while True:
        parent = [-1] * n
        parent[source] = source
        queue = deque([source])
        while queue and parent[sink] == -1:
            u = queue.popleft()
            for v in range(n):
                if parent[v] == -1 and residual[u][v] > 0:
                    parent[v] = u
                    queue.append(v)
        if parent[sink] == -1: break
        path_flow = float('inf')
        v = sink
        while v != source:
            u = parent[v]; path_flow = min(path_flow, residual[u][v]); v = u
        v = sink
        while v != source:
            u = parent[v]; residual[u][v] -= path_flow; residual[v][u] += path_flow; v = u
    # BFS on residual to find reachable
    visited = [False] * n
    queue = deque([source]); visited[source] = True
    while queue:
        u = queue.popleft()
        for v in range(n):
            if not visited[v] and residual[u][v] > 0:
                visited[v] = True; queue.append(v)
    cuts = []
    for u in range(n):
        for v in range(n):
            if visited[u] and not visited[v] and capacity[u][v] > 0:
                cuts.append((u, v))
    return cuts

def test():
    # Simple network
    cap = [[0,16,13,0,0,0],
           [0,0,10,12,0,0],
           [0,4,0,0,14,0],
           [0,0,9,0,0,20],
           [0,0,0,7,0,4],
           [0,0,0,0,0,0]]
    assert max_flow(cap, 0, 5) == 23
    # Simple 2-node
    cap2 = [[0,5],[0,0]]
    assert max_flow(cap2, 0, 1) == 5
    # Parallel paths
    cap3 = [[0,3,3,0],[0,0,0,3],[0,0,0,3],[0,0,0,0]]
    assert max_flow(cap3, 0, 3) == 6
    # Min cut
    cuts = min_cut(cap, 0, 5)
    assert len(cuts) > 0
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: max_flow.py test")
