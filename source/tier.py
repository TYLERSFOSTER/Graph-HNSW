import dgl
import torch
import copy


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
    self.known_simplices = {-1: {}}
