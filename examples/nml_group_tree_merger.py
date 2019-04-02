import argparse
import logging
import os
import numpy as np
import xml.etree.ElementTree as ET
from math import inf
from wknml import Edge, Tree, NML, parse_nml, dump_nml
from typing import List, Tuple


logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s  %(name)-8s %(message)s",
  datefmt="%Y-%m-%d %H:%M:%S")

logger = logging.getLogger(__file__)


def find_tress_by_id(trees: List[Tree], group_id: int):
  trees_with_group_id = []
  for current_tree in trees:
    if current_tree.groupId == group_id:
      trees_with_group_id.append(current_tree)
  return trees_with_group_id

def dist(a: np.ndarray, b: np.ndarray):
  return np.sqrt(np.sum(((a - b)) ** 2, axis=1))


def get_np_array_of_nodes_with_scale(tree: Tree, scale: Tuple[float]):
  nodes = list(map(lambda x: [x.position[0] * scale[0], x.position[1] * scale[1], x.position[2] * scale[2]], tree.nodes))
  return np.array(nodes)


def merge_trees_to_one_tree(trees: List[Tree], scale):
  # merge trees until only one 1 is left
  while len(trees) > 1:
    # sort the trees by the number of nodes
    trees = sorted(trees, key=lambda tree: len(tree.nodes))
    merging_tree = trees[0]
    min_distance_tree = 0
    min_merging_tree_node_index = 0
    min_distance_tree_node_index = 0
    min_dist = inf
    
    # find the nearest neighbour nodes of one node of the smallest tree and the other trees
    for current_tree in trees[1:]:
      node_coordinates_from_current_tree = get_np_array_of_nodes_with_scale(current_tree, scale)
      for current_node_index in np.arange(len(merging_tree.nodes)):
        current_node_coordinates = np.array(merging_tree.nodes[current_node_index].position) * scale
        distances = dist(node_coordinates_from_current_tree, current_node_coordinates)
        min_dist_index = np.argmin(distances)
        if distances[min_dist_index] < min_dist:
          min_distance_tree = current_tree
          min_merging_tree_node_index = current_node_index
          min_distance_tree_node_index = min_dist_index
          min_dist = distances[min_dist_index]
    # append the nodes to the other tree
    min_distance_tree.nodes.extend(merging_tree.nodes)
    min_distance_tree.edges.extend(merging_tree.edges)
    # connect the merged trees with the identified node
    min_distance_tree.edges.append(Edge(merging_tree.nodes[min_merging_tree_node_index].id,
                                        min_distance_tree.nodes[min_distance_tree_node_index].id))
    # delete merged tree
    del trees[0]

  return trees


def create_merged_nml(nml: NML, scale):
  merged_nml = NML(nml.parameters, [], nml.branchpoints, nml.comments, nml.groups)

  for current_group in nml.groups:
    group_id = current_group.id
    logger.info("Starting to merge group with id: {} and name: {}".format(group_id, current_group.name))

    trees_to_be_merged = find_tress_by_id(nml.trees, group_id)
    merged_tree = merge_trees_to_one_tree(trees_to_be_merged, scale)[0]
    merged_nml.trees.append(merged_tree)

  return merged_nml


def load_and_save_merged_nml_trees(source: str, destination: str, scale):

  assert os.path.isfile(source), "No file was provided as source."
  assert os.path.exists(os.path.dirname(destination)), "The destination directory does not exists."

  logger.info("Reading data")
  nml_root = ET.parse(source).getroot()
  nml = parse_nml(nml_root)

  logger.info("Starting to merge tree groups")
  merged_nml = create_merged_nml(nml, scale)

  logger.info("Writing data")
  merged_nml_xml = dump_nml(merged_nml)

  merged_nml_tree = ET.ElementTree()
  merged_nml_tree._setroot(merged_nml_xml)

  merged_nml_tree.write(destination)

  logger.info("Done")


def make_argparser():

  parser = argparse.ArgumentParser("Script to merge NML-trees with the same group-id into one tree.")
  parser.add_argument("--source",
                      required=True,
                      help="Path to the NML-file",
                      type=str)
  parser.add_argument("--destination",
                      required=True,
                      help="Path and name of the output file.",
                      type=str)
  parser.add_argument("--scale",
                      help="Scale of the dataset (e.g. 11.2,11.2,25)",
                      default="1,1,1")

  return parser

if __name__ == "__main__":

  parser = make_argparser()
  args = parser.parse_args()
  scale = np.array(tuple(float(x) for x in args.scale.split(",")))
  load_and_save_merged_nml_trees(args.source, args.destination, scale)


