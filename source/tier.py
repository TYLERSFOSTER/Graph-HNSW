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

  
  def name_simplex(self, vertex_list, check_present=True):
    simplex_dimension = len(vertex_list) - 1

    if check_present:
      for i in range(len(vertex_list)):
        for j in range(i+1,len(vertex_list)+1):
          assert [i, j] in self.edges, \
            'Proposed simplex contains boundary 1-simplices not in underlying graph.'
          
    self.sSet.nondegen_simplex(vertex_list)




'''
Functions using above class(es)
'''

def from_graph(seed_graph):
  seed_sSet = simplicial_set.from_graph(seed_graph)
  output = Tier(seed_sSet)
  
  return output
  
