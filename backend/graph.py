import os
import numpy as np
from tqdm import tqdm
from typing import Dict


class GraphNode:
    def __init__(self, node_id: str):
        self.__node_id = node_id
        self.__connections = {}

    def add_connection(self, conn_id: str, weight: int) -> None:
        if conn_id not in self.__connections:
            self.__connections[conn_id] = weight
        else:
            self.__connections[conn_id] += weight

    def delete_connection(self, conn_id: str) -> None:
        if conn_id in self.__connections:
            del self.__connections[conn_id]

    def get_connections(self) -> dict:
        self.__connections = dict(sorted(self.__connections.items(), key=lambda x: x[1], reverse=True))
        return self.__connections

    def get_connections_keys(self) -> list:
        return list(self.__connections.keys())

    def __len__(self):
        return len(self.__connections)


class Graph:
    def __init__(self):
        self.__nodes = {}

    def graph_traversal(self, start_id: str, abs_level: int, min_similarity: int, max_similarity: int):
        abstract_ids: Dict[int, list] = {0: [start_id]}
        locked_ids = [start_id]
        for level in range(1, abs_level):  # Уровень абстракции
            if level - 1 in abstract_ids:
                for id in abstract_ids[level - 1]:  # Раскрываем предыдущий уровень
                    connections = dict(sorted(self.__nodes[id].get_connections().items(),
                                              key=lambda x: x[1],
                                              reverse=True))
                    values = list(connections.values())
                    min_val = np.percentile(values, min_similarity)
                    max_val = np.percentile(values, max_similarity)
                    # aver = sum(connections.values())/len(connections.values())
                    for value in list(connections.keys()):
                        if max_val >= connections[value] >= min_val:
                            if value not in locked_ids:
                                locked_ids.append(value)
                                if level not in abstract_ids:
                                    abstract_ids[level] = [value]
                                else:
                                    abstract_ids[level] += [value]
        return abstract_ids

    def get_node(self, node_id: str) -> GraphNode:
        if node_id not in self.__nodes:
            raise Exception("There is no such vertex in the graph!")
        else:
            return self.__nodes[node_id]

    def get_nodes_ids(self):
        return list(self.__nodes.keys())

    def add_edge(self, start_node_id: str, end_node_id: str, weight: int):
        if start_node_id not in self.__nodes:
            self.__nodes[start_node_id]: GraphNode = GraphNode(node_id=start_node_id)
        self.__nodes[start_node_id].add_connection(conn_id=end_node_id, weight=weight)
        if end_node_id not in self.__nodes:
            self.__nodes[end_node_id]: GraphNode = GraphNode(node_id=end_node_id)
        self.__nodes[end_node_id].add_connection(conn_id=start_node_id, weight=weight)

    def delete_edge(self, start_node_id: str, end_node_id: str):
        if start_node_id in self.__nodes:
            if len(self.__nodes[start_node_id]) > 1:
                self.__nodes[start_node_id].delete_connection(conn_id=end_node_id)
            else:
                del self.__nodes[start_node_id]

    def __len__(self):
        return len(self.__nodes)


def launch_graph(dataset, graph):
    for i in tqdm(range(len(dataset)), desc="Initialization graph weights..."):
        graph.add_edge(start_node_id=str(dataset['KPGZ'][i]),
                   end_node_id=str(dataset['with_KPGZ'][i]),
                   weight=int(dataset['count'][i]))
