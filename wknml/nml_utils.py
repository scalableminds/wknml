from typing import Union, Dict, List
from math import sqrt, ceil
import networkx as nx
import numpy as np

from . import NML
from .nml_generation import generate_graph, generate_nml


def ensure_max_edge_length(nml_or_graph: Union[NML, nx.Graph], max_length: int) -> Union[NML, nx.Graph]:
    # it is easier to operate on a graph
    if isinstance(nml_or_graph, nx.Graph):
        nml_graph = nml_or_graph
    else:
        nml_graph, parameter_dict = generate_graph(nml_or_graph)
    max_id = detect_max_node_id_from_all_graphs(nml_graph)
    next_valid_id = max_id + 1
    for group in nml_graph.values():
        for graph in group:
            next_valid_id = ensure_max_edge_length_in_tree(graph, max_length, next_valid_id)

    # return the same format as the input
    if isinstance(nml_or_graph, nx.Graph):
        return nml_graph
    else:
        return generate_nml(nml_graph, parameter_dict)



def calculate_distance_between_nodes(node1: Dict, node2: Dict) -> float:
    return sqrt((node1['x'] - node2['x']) ** 2 +
                (node1['y'] - node2['y']) ** 2 +
                (node1['z'] - node2['z']) ** 2)


def get_vector_between_nodes(node1: Dict, node2: Dict) -> List[int]:
    return [node2['x'] - node1['x'],
            node2['y'] - node1['y'],
            node2['z'] - node1['z']]


def get_padding_node_position(node1: Dict, node2: Dict, relative_distance_along_vector: float) -> List[int]:
    vector_between_nodes = get_vector_between_nodes(node1, node2)
    return [node1['x'] + vector_between_nodes[0] * relative_distance_along_vector,
            node1['y'] + vector_between_nodes[1] * relative_distance_along_vector,
            node1['z'] + vector_between_nodes[2] * relative_distance_along_vector]


def detect_max_node_id_from_all_graphs(graph_dict: Dict[str, nx.Graph]) -> int:
    max_id = None
    for group in graph_dict.values():
        for tree in group:
            max_id_f_current_tree = np.array(list(tree.nodes)).max()
            max_id = max_id_f_current_tree if max_id_f_current_tree > max_id or not max_id else max_id

    return max_id


def ensure_max_edge_length_in_tree(graph: nx.Graph, max_length: int, current_id: int) -> int:
    for edge in graph.edges:
        node1 = graph.nodes[edge[0]]
        node2 = graph.nodes[edge[1]]
        edge_distance = calculate_distance_between_nodes(node1, node2)
        # add padding nodes if the distance is too high
        if edge_distance > max_length:
            number_of_padding_nodes = ceil(edge_distance / max_length)
            # remove old edge
            graph.remove_edge(*edge)
            # add all padding nodes and the edges
            previous_edge_id = edge[0]
            for padding_node_number in range(1, number_of_padding_nodes):
                relative_distance_between_nodes = edge_distance * padding_node_number / number_of_padding_nodes
                padding_node_position = get_padding_node_position(node1, node2, relative_distance_between_nodes)

                # attributes of the new node
                node_attributes = node1
                node_attributes['x'] = padding_node_position[0]
                node_attributes['y'] = padding_node_position[1]
                node_attributes['z'] = padding_node_position[2]

                # add node and edge to predecessor
                graph.add_node(current_id, **node_attributes)
                graph.add_edge(previous_edge_id, current_id)

                # update variables
                previous_edge_id = current_id
                current_id += 1
            # add the edge between the last padding node and the second original node
            graph.add_edge(previous_edge_id, edge[1])

    return current_id
