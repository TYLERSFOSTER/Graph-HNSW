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
    self.sparse_edges = self.sSet.extract_edges()
    self.edges = [[self.sparse_edges[0][k], self.sparse_edges[1][k]] for k in range(len(self.sparse_edges[0]))]
    self.graph = dgl.heterograph({('node', 'to', 'node'): (self.edges)})


  def simplex_present(self, vertex_list):
    dim_plus_one = len(vertex_list)
    output = True
    for i in range(0, dim_plus_one-1):
      for j in range(i+1, dim_plus_one):
        candidate_edge = [vertex_list[i], vertex_list[j]]
        output *= (candidate_edge in self.edges)
    return output
  

  def name_simplex(self, vertex_list):
    is_present = self.simplex_present(vertex_list)
    if is_present:
      self.sSet.nondegen_simplex(vertex_list)



'''
Functions using above class(es)
'''

def from_graph(seed_graph):
  seed_sSet = simplicial_set.from_graph(seed_graph)
  output = Tier(seed_sSet)
  
  return output
  
