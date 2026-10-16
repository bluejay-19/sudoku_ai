""" Draws two evaluation charts from the generated benchmark CSVs

    Reads results/results.csv and results/brute-force.csv and writes results/nodes_chart.png
    and results/time_chart.png (log scale on the y-axis)
"""
import csv
import matplotlib.pyplot as plt

# read both results files into one list of rows
# each row is a dict keyed by the csv header
rows = []
for path in ["results/results.csv", "results/brute-force.csv"]:
    with open(path, newline="") as file:
        for row in csv.DictReader(file):
            rows.append(row)

# values: {mode: {puzzle name: number}} CSV values are strings so they need to be converted
nodes = {"plain": {}, "fc": {}}
times = {"plain": {}, "fc": {}}
for row in rows:
    name = row["Puzzle"].replace(".txt", "")
    mode = row["Mode"]
    nodes[mode][name] = int(row["Nodes"])
    times[mode][name] = float(row["Time"])

# order the bars from smallest plain node count to the largest (chart reads easy to hard)
puzzle_names = sorted(nodes["plain"], key=lambda name: nodes["plain"][name])


def draw_chart(values, title, y_label, filename):
    """ Draw grouped bars (plain vs MRV + FC) per puzzle on a log scale and save the chart"""
    positions = list(range(len(puzzle_names)))
    width =0.4
    plain_heights = [values["plain"][name] for name in puzzle_names]
    fc_heights = [values["fc"][name] for name in puzzle_names]

    plt.figure(figsize=(11,5))
    # shift one set of bars to the left and the other to the right so they sit by side
    plt.bar([p - width / 2 for p in positions], plain_heights, width, label="Plain backtracking", color="#1e3a5f", edgecolor="black", linewidth=0.5)
    plt.bar([p + width / 2 for p in positions], fc_heights, width, label="MRV + FC", color="#4fc3f7", edgecolor="black", linewidth=0.5)
    plt.xticks(positions, puzzle_names, rotation=45, ha="right")
    plt.yscale("log")   # values span sever orders of magnitude
    plt.ylabel(y_label, fontsize=12)
    plt.title(title, fontsize=12)
    plt.legend()
    plt.tight_layout()
    plt.grid(axis="both", linestyle="--", alpha=0.8)
    plt.gca().set_axisbelow(True)
    plt.savefig(filename, dpi=200)
    plt.close()  # so the second chart gets to start from a blank figure

draw_chart(nodes, "Search nodes per puzzle (log scale)", "Nodes", "results/nodes_chart.png")
draw_chart(nodes, "Solve time per puzzle (log scale)", "TIme(seconds)", "results/time_chart.png")