# Social-Network Analyzer (APP3)

This Python application analyses a directed social-network dataset and highlights:

- **Leaders** (nodes with maximum incoming edges)
- **Followers** of each leader (nodes pointing to a leader)
- **Best followers** (nodes with maximum outgoing edges)
- **Leaders in the undirected graph** (nodes with most neighbours)
- **Shortest path** (via BFS) between the first two leaders
- **Visualization** of the graph with colored nodes

## Requirements

- Python 3.8+
- NetworkX
- Matplotlib

## Installation
   ```bash
   pip install -r requirements.txt
   ```
   or
   ```bash
   pip install networkx matplotlib
   ```

## Usage
   ```bash
   python main.py exemple.txt
   ```
 - Prints metrics to the console.
 - Writes `matrix.txt` with the adjacency matrix.
 - Opens a window showing the colored graph.


## Project Structure

```
social_analyzer/
├── main.py              # core application
├── exemple.txt          # sample input data
├── matrix.txt           # generated adjacency matrix
├── organigramme.png     # function-call diagram
└── README.md            # this document
```

## Features

1. **Adjacency Matrix**: Generates & saves a binary matrix.
2. **Directed Leaders**: Finds nodes with highest in-degree.
3. **Followers Listing**: Outputs each leader’s followers.
4. **Best Followers**: Finds nodes with highest out-degree.
5. **Undirected Leaders**: Finds nodes with most neighbours ignoring direction.
6. **BFS Pathfinding**: Computes shortest path (in hops) between two leaders.
7. **Visualization**: Colors leaders in red, best followers in orange, leaders' followers in light coral, others in light blue.

## Authors

- Shramkov Rostyslav
- Mathis Lin
- Fernandez Hugo