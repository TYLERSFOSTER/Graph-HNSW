import dgl
import torch
import copy

'''Local project modules'''
import simplicial_set


'''
Classes
'''
class Tier():
  def __init__(self,
               seed_graph=dgl.heterograph({('node', 'to', 'node'): (list(), list())}),
               level_index=0,
               ):
 
    assert isinstance(seed_graph, dgl.DGLHeteroGraph), \
        'Keyword argument `seed_graph` of graph_towers\'s init method must be a dgl.DGLHeteroGraph.'
    assert isinstance(level_index, int), \
        'Keyword argument `bottom_level` of graph_towers\'s init method must be an integer.'
    
    self.seed_graph = seed_graph
    self.level_index = level_index

    self.vertices = self.seed_graph.nodes()
    self.known_simplices = simplicial_set.NonDegenSSet().add_vertices(self.vertices)
    self.edges = self.seed_graph.edges()
