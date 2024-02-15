import dgl
import torch
import copy


''' Helper functions'''

def all_sublists(input_list): # Generates all (ordered) sublists of a given list
  output = [[]]
  for element in input_list:
    existing_sublists = list(copy.deepcopy(output))
    for sublist in existing_sublists:
      sublist.append(element)
      output.append(sublist)
  return output



'''Classes'''

class SSet():
  def __init__(self,
               dimension=0,
               ):
    
    assert isinstance(dimension, dgl.DGLHeteroGraph), \
      'Keyword argument `dim` of sSet\'s init method must be a nonnegative integer.'
    
    self.simplices = {0 : {}}

  # A lot to figure out here. Leaving for later.



class NonDegenSSet():
  def __init__(self,
               dimension=0,
               ):
    
    assert isinstance(dimension, int), \
      'Keyword argument `dim` must be a nonnegative integer.'
    assert dimension >= 0, \
      'Keyword argument `dim` must be a nonnegative integer.'
    
    self.simplices = {-1 : [],
                      0 : [],
                      }



  def add_vertices(self, vertex_labels):
    assert isinstance(vertex_labels, list), \
      'Keyword argument `vertex_labels` must be a list.'
  
    for label in vertex_labels:
      assert isinstance(label, str), \
        'Each entry in list `vertex_labels` must be a string.'
      assert label not in self.simplices[0], \
        'Each entry in list must be a string that does NOT yet appear in `NonDegenSSet.simplices[0]`.'

    self.simplices[0] += vertex_labels



  def nondegen_simplex(self, vertices):
    assert isinstance(vertices, list), \
      'Argument `vertices` must be a list of distinct elements of `NonDegenSSet.simplices[0]`.'
    assert len(set(vertices)) == len(vertices), \
      'Argument `vertices` must be a list of distinct elements of `NonDegenSSet.simplices[0]`.'
    for vertex in vertices:
      assert vertex in self.simplices[0], \
        'Argument `vertices` must be a list of distinct elements of `NonDegenSSet.simplices[0]`.'
    
    subsimplices = all_sublists(vertices)
    for subsimplex in subsimplices:
      local_dim = len(subsimplex) - 1
      print('THIS:', self.simplices[local_dim])
      new_simplex_list = list(set(self.simplices[local_dim] + [subsimplex]))