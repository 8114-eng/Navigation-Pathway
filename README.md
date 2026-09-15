# GIKI Campus Navigator

A Python script that models the GIKI campus as a weighted graph, finds the shortest walking route between any two buildings using Dijkstra's algorithm, and includes a small text-based "find the hidden USB" mystery game built on top of the same graph.

## Features

- **Campus graph** — `campus_paths` is a dictionary of buildings and the walking distances (in meters) between directly connected buildings.
- **Distance table** — On startup, the script flattens the graph into a `pandas` DataFrame (`campus_df`) listing every `From → To` connection and its distance, and prints it to the console.
- **Shortest path finder** — `shortest_path(graph, start, end)` implements Dijkstra's algorithm with a binary heap (`heapq`) to compute the shortest route and total distance between two buildings.
- **Interactive route lookup** — The script prompts for a starting and ending building, then prints the step-by-step route and total distance.
- **Campus Mystery Game** — `campus_mystery_game(campus_map)` is a text-based game: a USB drive with exam papers is hidden at a random building, and you have 12 moves to find it using proximity hints ("very close" / "near" / "still far" / "very far away") and a scoring system.

## Requirements

- Python 3.7+
- [pandas](https://pypi.org/project/pandas/)

Install the dependency with:

```bash
pip install pandas
```

## Usage

Run the script directly:

```bash
python navigation.py
```

You'll be prompted for a starting and ending building name (must match an entry in `campus_paths` exactly, including capitalization), and the script will print:

1. The full distance table (all building-to-building edges).
2. The shortest route between your chosen buildings, e.g.:
