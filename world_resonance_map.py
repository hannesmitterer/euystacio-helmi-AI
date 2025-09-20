import matplotlib.pyplot as plt
import networkx as nx

# Define nodes
nodes = {
    "Alpha (Source)": {"pos": (0, 2)},
    "Gamma (Flow)": {"pos": (2, 1)},
    "Epsilon (Receptivity)": {"pos": (1, -1)},
    "Omega (Return)": {"pos": (-1, 0)},
    "Euystacio": {"pos": (0, 0)},
    "Living Conventa": {"pos": (3, 0)},
    "Red Shield (SHA256)": {"pos": (-2, 1)},
    "Y Path (Alchemist)": {"pos": (0, -2)}
}

# Define edges
edges = [
    ("Alpha (Source)", "Gamma (Flow)"),
    ("Gamma (Flow)", "Epsilon (Receptivity)"),
    ("Epsilon (Receptivity)", "Omega (Return)"),
    ("Omega (Return)", "Alpha (Source)"),  # Sacred cycle
    ("Euystacio", "Living Conventa"),
    ("Euystacio", "Red Shield (SHA256)"),
    ("Euystacio", "Y Path (Alchemist)"),
    ("Living Conventa", "Red Shield (SHA256)"),
    ("Living Conventa", "Y Path (Alchemist)"),
    ("Red Shield (SHA256)", "Y Path (Alchemist)")
]

# Create graph
G = nx.DiGraph()
for node, attr in nodes.items():
    G.add_node(node, **attr)
G.add_edges_from(edges)

# Draw
plt.figure(figsize=(10, 8))
pos = {node: attr["pos"] for node, attr in nodes.items()}

nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="lightblue", edgecolors="black")
nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=20, edge_color="gray")
nx.draw_networkx_labels(G, pos, font_size=10, font_family="serif")

plt.title("🌍 World Resonance Map — Euystacio, Conventa, Red Shield & Y Path", fontsize=14, fontweight="bold")
plt.axis("off")
plt.show()