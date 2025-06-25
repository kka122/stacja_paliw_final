#!/usr/bin/env python3
"""
Generuje diagram klas UML dla pakietu gas_station.
Używa kolejno: Graphviz (jeśli dot działa) lub NetworkX+Matplotlib.
"""
import os, inspect, pkgutil, importlib
OUTPUT_PNG = "docs/class_diagram.png"
PACKAGE = "gas_station"

# próba Graphviz
try:
    from graphviz import Digraph
    HAS_GV = True
except ImportError:
    HAS_GV = False

import networkx as nx
import matplotlib.pyplot as plt

def collect_classes():
    pkg = importlib.import_module(PACKAGE)
    classes = {}
    for _, modname, _ in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + "."):
        mod = importlib.import_module(modname)
        for nm, obj in inspect.getmembers(mod, inspect.isclass):
            if obj.__module__.startswith(PACKAGE):
                classes[f"{obj.__module__}.{nm}"] = obj
    return classes

def generate_class_diagram():
    cls = collect_classes()
    edges = []
    for name, C in cls.items():
        for b in C.__bases__:
            key = f"{b.__module__}.{b.__name__}"
            if key in cls:
                edges.append((key, name))

    os.makedirs(os.path.dirname(OUTPUT_PNG), exist_ok=True)

    if HAS_GV:
        try:
            dot = Digraph(format="png")
            dot.attr(node_shape="record")
            for name, C in cls.items():
                fields = []
                for a,t in getattr(C, "__annotations__", {}).items():
                    fields.append(f"{a}: {getattr(t,'__name__',t)}")
                lbl = "{{%s|%s}}"%(C.__name__, "\\l".join(fields)+"\\l" if fields else "")
                dot.node(name, lbl)
            for src,dst in edges:
                dot.edge(src, dst, arrowhead="onormal")
            path = dot.render(OUTPUT_PNG.replace(".png",""), cleanup=True)
            try: dot.view(OUTPUT_PNG.replace(".png",""))
            except: pass
            print("🔄 Diagram UML (Graphviz):", path)
            return
        except Exception as e:
            print("⚠️ Graphviz failed:", e)

    # fallback NetworkX + Matplotlib
    G = nx.DiGraph()
    for name,C in cls.items():
        G.add_node(name, label=C.__name__)
    G.add_edges_from(edges)
    plt.figure(figsize=(10,8))
    pos = nx.spring_layout(G)
    labels = {n:d["label"] for n,d in G.nodes(data=True)}
    nx.draw(G, pos, labels=labels, with_labels=True, arrows=True, node_size=3000, font_size=10)
    plt.tight_layout()
    plt.savefig(OUTPUT_PNG)
    print("🔄 Diagram UML (NetworkX):", OUTPUT_PNG)
    plt.show()
