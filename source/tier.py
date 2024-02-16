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

  
  def name_simplex(self, vertex_list, check_present=True):
    simplex_dimension = len(vertex_list) - 1

    print('`self.edges`:', self.edges)
    if check_present:
      for i in range(0, len(vertex_list)-1):
        for j in range(i,len(vertex_list)):
          assert [vertex_list[i], vertex_list[j]] in self.edges, \
            'Proposed simplex contains boundary 1-simplices not in underlying graph.'
          
    self.sSet.nondegen_simplex(vertex_list)




'''
Functions using above class(es)
'''

def from_graph(seed_graph):
  seed_sSet = simplicial_set.from_graph(seed_graph)
  output = Tier(seed_sSet)
  
  return output
  
