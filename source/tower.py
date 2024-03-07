import dgl
import copy
import numbers
import math

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
    #-----------------------------------------
    self.seed_graph = seed_graph
    self.tiers = {starting_index: tier.Tier(seed_graph)}
    self.maps = {}
    self.sample_ratio = sample_ratio
    sample_count = math.ceil(len(self.seed_graph.nodes()) * self.sample_ratio)

    self.starting_index = starting_index
    running_index = copy.deepcopy(starting_index)
    bottom_tier = self.tiers[running_index]
    bottom_edge_count = len(bottom_tier.graph.edges()[0])
    while bottom_edge_count != 0:
      double_index = (running_index, running_index+1)
      running_index += 1
      bottom_tier, bottom_map = bottom_tier.random_contractions(sample_count)
      self.tiers.update({running_index : bottom_tier})
      self.maps.update({double_index : bottom_map})
      bottom_edge_count = len(bottom_tier.graph.edges()[0])
    self.ending_index = running_index
    self.length = len(self.tiers)

  
  def build_preimage_lookups(self, to_tower_attribute=False):
    '''Method that returns a dictionary of "inverted maps", i.e., pre-image lookup dictionaries'''
    preimage_lookups = {}
    for index in self.maps:
      map_dictionary = self.maps[index].partial_map
      preimage_lookup = {}
      for input_value in map_dictionary:
        output_value =  map_dictionary[input_value]
        if output_value in preimage_lookup: preimage_lookup[output_value].append(input_value)
        else: preimage_lookup.update({output_value : [input_value]})
      preimage_lookups.update({(index[1], index[0]) : preimage_lookup})
    if to_tower_attribute == True: self.preimage_lookups = preimage_lookups
    return preimage_lookups
  

  def include_loops(self):
    tier_indices = [index for index in self.tiers]
    for tier_index in tier_indices: self.tiers[tier_index].include_loops()