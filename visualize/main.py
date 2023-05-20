import random
from pathlib import Path

import pandas as pd
from pyvis.network import Network

CurrentPath = Path(__file__).resolve().parent
BasePath = CurrentPath.parent


def generate_random_hex():
    r = lambda: random.randint(0, 255)
    return '#%02X%02X%02X' % (r(), r(), r())


def main():
    df = pd.read_csv(BasePath / "submission.csv")
    df = df[:10]
    size = df.size
    net = Network()

    nodes = set()
    colors = {}
    for index, row in df.iterrows():
        print(f"{index}/ {size}")
        ego_id = int(row["ego_id"])
        if ego_id not in colors:
            colors.update({ego_id: generate_random_hex()})
        u = f'{ego_id}_{int(row["u"])}'
        v = f'{ego_id}_{int(row["v"])}'

        if u not in nodes:
            nodes.add(u)
            net.add_node(u, label=f"Node {u}", color=colors[ego_id])
        if v not in nodes:
            nodes.add(v)
            net.add_node(v, label=f"Node {v}", color=colors[ego_id])
        net.add_edge(u, v)

    net.toggle_physics(True)
    try:
        net.show((CurrentPath / "out" / 'mygraph.html').as_posix())
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    main()
