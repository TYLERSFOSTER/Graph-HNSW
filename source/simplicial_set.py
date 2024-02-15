import dgl
import torch
import copy

'''Local project modules'''
import helpers


'''
Classes
'''
class NonDegenSSet():
  '''
  Class representing a simplicial set-like object in which every simplex is determined by an ordered list of vertices.
  '''
  def __init__(self,
               dimension=0,
               ):
    
    assert isinstance(dimension, int), 'Keyword argument `dim` must be a nonnegative integer.'
    assert dimension >= 0, 'Keyword argument `dim` must be a nonnegative integer.'
    
    self.simplices = {-1 : [],
                      0 : [],
                      }


  def add_vertices(self, vertex_labels):
    assert isinstance(vertex_labels, list), 'Keyword argument `vertex_labels` must be a list.'
  
    for label in vertex_labels:
      assert isinstance(label, str), 'Each entry in list `vertex_labels` must be a string.'
      assert label not in self.simplices[0], 'Each entry in list must be a string that does NOT yet appear in `NonDegenSSet.simplices[0]`.'

    bracketed_labels = [[label] for label in vertex_labels]
    self.simplices[0] += bracketed_labels


  def extract_vertices(self):
    bracketed_vertices = self.simplices[0]
    output = [bracketed_vertex[0] for bracketed_vertex in bracketed_vertices]
    return output


  def nondegen_simplex(self, vertices):
    assert isinstance(vertices, list), 'Argument `vertices` must be a list of distinct elements of `NonDegenSSet.simplices[0]`.'
    assert len(set(vertices)) == len(vertices), 'Argument `vertices` must be a list of distinct elements of `NonDegenSSet.simplices[0]`.'
    extracted_vertices = self.extract_vertices()
    for vertex in vertices:
      assert vertex in extracted_vertices, 'Argument `vertices` must be a list of distinct elements of `NonDegenSSet.simplices[0]`.'
    
    subsimplices = helpers.all_sublists(vertices)
    subsimplices.remove([])
    for subsimplex in subsimplices:
      local_dim_n = len(subsimplex) - 1
      if local_dim_n not in self.simplices:
        self.simplices.update({local_dim_n : []})
      if subsimplex not in self.simplices[local_dim_n]:
        (self.simplices[local_dim_n]).append(subsimplex)