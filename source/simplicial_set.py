import dgl

'''Local project modules'''
import helpers


'''
Classes
'''
class SSet(): 
  '''Class representing a simplicial set-like object in which every simplex is determined by an ordered list of vertices.'''
  def __init__(self,
               dimension=0,
               ):
    assert isinstance(dimension, int), 'Keyword argument `dim` must be a nonnegative integer.'
    assert dimension >= 0, 'Keyword argument `dim` must be a nonnegative integer.'
    self.simplices = {-1 : [], # This is like fantasy "base simplicial set of dimension -1"
                      0 : [],
                      }


  def add_vertices(self, vertex_labels):
    assert isinstance(vertex_labels, list), 'Keyword argument `vertex_labels` must be a list.'
    for label in vertex_labels:
      assert isinstance(label, int), 'Each entry in list `vertex_labels` must be an integer.'
      assert label not in self.simplices[0], 'Each entry in list must be a string that does NOT yet appear in `SSet.simplices[0]`.'
    bracketed_labels = [[label] for label in vertex_labels]
    self.simplices[0] += bracketed_labels


  def extract_vertices(self):
    bracketed_vertices = self.simplices[0]
    output = [bracketed_vertex[0] for bracketed_vertex in bracketed_vertices]
    return output


  def extract_edges(self):
    src_list = []; tgt_list = []
    if 1 in self.simplices:
      for src, tgt in self.simplices[1]: src_list.append(src); tgt_list.append(tgt)
    return src_list, tgt_list


  def catalog_simplex(self, vertices, include_all_subsimplices=True, outlaw_degenerate_simplices=True):
    assert isinstance(vertices, list), 'Argument `vertices` must be a list of elements of `SSet.simplices[0]`.'
    if outlaw_degenerate_simplices: assert len(set(vertices)) == len(vertices), 'When `outlaw_degenerate_simplices=True`, argument `vertices` must be a list of distinct elements of `SSet.simplices[0]`.'
    extracted_vertices = self.extract_vertices()
    for vertex in vertices: assert vertex in extracted_vertices, 'Argument `vertices` must be a list of elements of `SSet.simplices[0]`.'
    if include_all_subsimplices == True: subsimplices = helpers.all_sublists(vertices); subsimplices.remove([])
    else: subsimplices = [vertices]
    for subsimplex in subsimplices:
      local_dim_n = len(subsimplex) - 1
      if local_dim_n not in self.simplices: self.simplices.update({local_dim_n : []})
      if subsimplex not in self.simplices[local_dim_n]: (self.simplices[local_dim_n]).append(subsimplex)


  def dynamic_search(self, search_dimension):
    '''Method that looks for implicit n-simplices based on knowledge of (n-1)-simplices'''
    assert isinstance(search_dimension, int)
    assert search_dimension >= 2
    if 1 not in self.simplices:
      self.simplices.update({1 : []})
    if search_dimension not in self.simplices:
      self.simplices.update({search_dimension: []})
    vertices = [singleton[0] for singleton in self.simplices[0]]
    edge_aids = {vertex : [] for vertex in vertices}
    for edge in self.simplices[1]:
      source = edge[0]
      target = edge[1]
      edge_aids[target].append(source)
    current_simplices = self.simplices[search_dimension-1]
    for potential_top_vertex in vertices:
      source_vertices = edge_aids[potential_top_vertex]
      for simplex in current_simplices:
        simplex_contained_in_source_vertices = True
        for potential_source_vertex in simplex:
          simplex_contained_in_source_vertices *= (potential_source_vertex in source_vertices)
        if simplex_contained_in_source_vertices:
          new_simplex = simplex + [potential_top_vertex]
          self.simplices[search_dimension].append(new_simplex)

  
  def expunge_degenerates(self):
    indexing_dimensions = [dimension for dimension in self.simplices]
    for dimension in indexing_dimensions:
      nondegenerate_simplices = [simplex for simplex in self.simplices[dimension] if len(list(set(simplex))) == len(simplex)]
      self.simplices[dimension] = nondegenerate_simplices

      



'''
Functions using above class(es)
'''
def from_graph(seed_graph):
  assert isinstance(seed_graph, dgl.DGLGraph)
  output = SSet()
  vertices = seed_graph.nodes().tolist()
  output.add_vertices(vertices)
  inout = seed_graph.edges()[0].tolist(), seed_graph.edges()[1].tolist()
  for k in range(len(inout[0])): output.catalog_simplex([inout[0][k], inout[1][k]])
  return output