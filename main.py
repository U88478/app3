import csv
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx


class GraphAnalyzer:
    """Analyse a directed social‑network graph described by a CSV file."""

    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.edges = []  # (src, dst)
        self.node_ids = []  # index → real ID
        self.id_to_idx = {}  # real ID → index
        self.adj = []  # adjacency matrix

    # ---------- reading & preprocessing ---------- #
    def load_edges(self):
        ids = set()
        with self.file_path.open(newline="") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            for row in reader:
                if len(row) < 2:
                    continue
                u = int(row[0].strip())
                v = int(row[1].strip())
                self.edges.append((u, v))
                ids.add(u)
                ids.add(v)
        self.node_ids = sorted(ids)
        self.id_to_idx = {n: i for i, n in enumerate(self.node_ids)}

    def build_matrix(self):
        n = len(self.node_ids)
        self.adj = [[0] * n for _ in range(n)]
        for u, v in self.edges:
            i = self.id_to_idx[u]
            j = self.id_to_idx[v]
            self.adj[i][j] = 1

    def save_matrix(self):
        with open("matrix.txt", "w+") as file:
            file.write("\n".join([str(i) for i in self.adj]))

    # ---------- queries ---------- #
    def _degrees(self):
        in_deg = {n: 0 for n in self.node_ids}
        out_deg = {n: 0 for n in self.node_ids}
        for u, v in self.edges:
            out_deg[u] += 1
            in_deg[v] += 1
        return in_deg, out_deg

    def oriented_leaders(self):
        in_deg, _ = self._degrees()
        max_in = max(in_deg.values()) if in_deg else 0
        return [n for n, d in in_deg.items() if d == max_in]

    def undirected_leaders(self):
        n = len(self.node_ids)
        counts = [0] * n
        for i in range(n):
            for j in range(n):
                if self.adj[i][j] or self.adj[j][i]:
                    counts[i] += 1
        max_nb = max(counts) if counts else 0
        return [self.node_ids[i] for i, c in enumerate(counts) if c == max_nb]

    def followers_of(self, leaders):
        res = {ld: [] for ld in leaders}
        for u, v in self.edges:
            if v in res:
                res[v].append(u)
        return res

    def best_followers(self):
        _, out_deg = self._degrees()
        max_out = max(out_deg.values()) if out_deg else 0
        return [n for n, d in out_deg.items() if d == max_out]

    def bfs_tree(self, source):
        if source not in self.id_to_idx:
            return {}
        parent = {source: None}
        queue = [source]
        idx = 0
        while idx < len(queue):
            u = queue[idx]
            idx += 1
            i = self.id_to_idx[u]
            for j, has_edge in enumerate(self.adj[i]):
                if has_edge:  # or self.adj[j][i]
                    v = self.node_ids[j]
                    if v not in parent:
                        parent[v] = u
                        queue.append(v)
        return parent

    def bfs_shortest_path(self, src, dst):
        parents = self.bfs_tree(src)
        if dst not in parents:
            return []
        path = [dst]
        while path[-1] != src:
            path.append(parents[path[-1]])
        return list(reversed(path))

    # ---------- drawing ---------- #
    def draw(self, leaders, best_fols, leader_fols):
        g = nx.DiGraph(self.edges)
        colours = []
        fol_set = {u for lst in leader_fols.values() for u in lst}
        for n in g.nodes():
            if n in leaders:
                colours.append("red")
            elif n in best_fols:
                colours.append("orange")
            elif n in fol_set:
                colours.append("lightcoral")
            else:
                colours.append("lightblue")
        nx.draw_networkx(
            g,
            labels={n: n for n in g.nodes()},
            node_color=colours,
            arrows=True,
        )
        plt.axis("off")
        plt.show()

    def run(self):
        self.load_edges()
        self.build_matrix()
        self.save_matrix()

        leaders = self.oriented_leaders()
        leader_fols = self.followers_of(leaders)
        best_fols = self.best_followers()
        undirected_ld = self.undirected_leaders()
        bfs_map = self.bfs_tree(leaders[0]) if leaders else {}
        lead_path = self.bfs_shortest_path(leaders[0], leaders[1]) if len(leaders) > 1 else [leaders[0]]

        print("Leaders (directed):", leaders)
        print("Followers of leaders:", leader_fols)
        print("Best followers:", best_fols)
        print("Leaders (undirected):", undirected_ld)
        print("BFS tree from first leader:", bfs_map)
        print("Path between leaders:", lead_path)

        self.draw(leaders, best_fols, leader_fols)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "students.csv"
    GraphAnalyzer(path).run()
