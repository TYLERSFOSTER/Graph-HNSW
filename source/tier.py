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
               seed_sSet,
               ):
    
    self.sSet = seed_sSet
    self.vertices = self.sSet.extract_vertices()
    self.edges = self.sSet.extract_edges()
    self.graph = dgl.heterograph({('node', 'to', 'node'): (self.edges)})



'''
Functions using above class(es)
'''

def from_graph(seed_graph):
  seed_sSet = simplicial_set.from_graph(seed_graph)
  output = Tier(seed_sSet)
  
  print(output.edges)
  
  return output
  
