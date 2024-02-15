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
               sSet,
               ):
    
    self.sSet = sSet
    self.vertices = self.sSet.extract_vertices()
    self.edges = self.extract_edges()
    self.graph = dgl.heterograph({('node', 'to', 'node'): (self.edges)})
