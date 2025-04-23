# dot -Tpng callgraph.dot -o organigramme.png

calls = {
    "run": ["load_edges", "build_matrix",
            "oriented_leaders", "followers_of",
            "best_followers", "undirected_leaders",
            "bfs_shortest_path", "draw"],
    "bfs_shortest_path": ["bfs_tree"],
}

with open("callgraph.dot", "w") as out:
    out.write("digraph G {\n")
    for caller, callees in calls.items():
        for callee in callees:
            out.write(f'  "{caller}()" -> "{callee}()";\n')
    out.write("}\n")
