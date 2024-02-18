import dgl
import torch
import copy
import numbers

'''Local project modules'''
import tier


'''
Classes
'''
class Tower():
  def __init__(self,
               seed_graph,
               sample_ratio=0.5,
               starting_index=0,
               ):
    assert isinstance(seed_graph, dgl.DGLHeteroGraph), 'Keyword argument `seed_graph` of graph_towers\'s init method must be a dgl.DGLHeteroGraph.'
    assert isinstance(sample_ratio, numbers.Number), 'Keyword argument `sample_ratio` of graph_towers\'s init method must be a float.'
    assert sample_ratio<=1. and sample_ratio>=0., 'Keyword argument `ratio` of graph_towers\'s init method must be between 0 and 1.'
    assert isinstance(starting_index, int), 'Keyword argument `bottom_level` of graph_towers\'s init method must be an integer.'

    self.seed_graph = seed_graph
    self.tiers = {starting_index: tier.Tier(seed_graph)}