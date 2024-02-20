import dgl
import torch
import copy

'''Local project modules'''
import helpers


'''
Classes
'''
class NonDegenSSet(): 
  '''Class representing a simplicial set-like object in which every simplex is determined by an ordered list of vertices.'''
  def __init__(self,
               dimension=0,
               ):
    assert isinstance(dimension, int), 'Keyword argument `dim` must be a nonnegative integer.'
    assert dimension >= 0, 'Keyword argument `dim` must be a nonnegative integer.'
    #-----------------------------------------
    self.simplices = {-1 : [], # This is like fantasy "base simplicial set of dimension -1"
                      0 : [],
                      }


  def add_vertices(self, vertex_labels):
    assert isinstance(vertex_labels, list), 'Keyword argument `vertex_labels` must be a list.'
    #-----------------------------------------
    for label in vertex_labels:
      assert isinstance(label, int), 'Each entry in list `vertex_labels` must be an integer.'
      assert label not in self.simplices[0], 'Each entry in list must be a string that does NOT yet appear in `NonDegenSSet.simplices[0]`.'
    bracketed_labels = [[label] for label in vertex_labels]
    self.simplices[0] += bracketed_labels


  def extract_vertices(self):
    bracketed_vertices = self.simplices[0]
    output = [bracketed_vertex[0] for bracketed_vertex in bracketed_vertices]
    return output


  def extract_edges(self):
    src_list = []
    tgt_list = []
    if 1 in self.simplices:
      for src, tgt in self.simplices[1]:
        src_list.append(src)
        tgt_list.append(tgt)
    return src_list, tgt_list


  def nondegen_simplex(self, vertices):
    # print('Simplex to add:', vertices)
    assert isinstance(vertices, list), 'Argument `vertices` must be a list of distinct elements of `NonDegenSSet.simplices[0]`.'
    assert len(set(vertices)) == len(vertices), 'Argument `vertices` must be a list of distinct elements of `NonDegenSSet.simplices[0]`.'
    extracted_vertices = self.extract_vertices()
    for vertex in vertices:
      assert vertex in extracted_vertices, 'Argument `vertices` must be a list of distinct elements of `NonDegenSSet.simplices[0]`.'
    #-----------------------------------------
    subsimplices = helpers.all_sublists(vertices)
    subsimplices.remove([])
    for subsimplex in subsimplices:
      local_dim_n = len(subsimplex) - 1
      if local_dim_n not in self.simplices:
        self.simplices.update({local_dim_n : []})
      if subsimplex not in self.simplices[local_dim_n]:
        (self.simplices[local_dim_n]).append(subsimplex)


'''
Functions using above class(es)
'''
def from_graph(seed_graph):
  assert isinstance(seed_graph, dgl.DGLGraph)
  #-----------------------------------------
  output = NonDegenSSet()
  verts = seed_graph.nodes().tolist()
  output.add_vertices(verts)
  inout = seed_graph.edges()[0].tolist(), seed_graph.edges()[1].tolist()
  for k in range(len(inout[0])):
    output.nondegen_simplex([inout[0][k], inout[1][k]])
  return output