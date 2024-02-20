import traceback
import dgl
import torch
import copy

'''Local project modules'''
import helpers
import simplicial_set
import tier
import tower


'''
Classes
'''
class SimplexBot():
  '''Class representing bot that crawls up HNSW tower, searching for simplices below a fixed dimension'''
  def __init__(self,
               tower_to_search,
               top_search_dimension=1,
               ):
    assert isinstance(tower_to_search, tower.Tower), 'Argument `tower_to_search` must be an instance of the class `tower.Tower`.'
    assert isinstance(top_search_dimension, int), 'Argument `top_search_dimension` must be a positive integer.'
    assert top_search_dimension > 0, 'Argument `top_search_dimension` must be a positive integer.'
    #-----------------------------------------
    self.tower = tower_to_search
    self.top_dimension = top_search_dimension
    self.start_index = self.tower.starting_index
    self.end_index = self.tower.ending_index
    self.top_sSet = self.tower.tiers[self.start_index].sSet