import dgl
import torch
import copy

'''Local project modules'''
import simplicial_set
import helpers


'''
Classes
'''

class Tier():
  '''Class representing a single "tier" or "level" in a graph HNSW tower.'''
  def __init__(self,
               seed_graph,
               ):
    
    self.sSet = simplicial_set.from_graph(seed_graph)
    self.vertices = self.sSet.extract_vertices()
    self.sparse_edges = self.sSet.extract_edges()
    self.edges = [[self.sparse_edges[0][k], self.sparse_edges[1][k]] for k in range(len(self.sparse_edges[0]))]
    self.graph = seed_graph
    #self.live_vertices = seed_graph.nodes().tolist()


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

      

class Tier_Map():
  '''Class representing a partially-defined map between tiers in a graph HNSW tower.'''
  def __init__(self,
               tier_upstairs,
               tier_downstairs,
               ):
    assert isinstance(tier_upstairs, Tier)
    assert isinstance(tier_downstairs, Tier)

    self.upstairs = tier_upstairs
    self.upstairs_vertices = self.upstairs.vertices
    self.downstairs = tier_downstairs

    self.partial_map = {}



'''
Further methods for above class(es)
'''

def contract_edge(self, contracting_edge):
  '''Method for `Tier` contracting a single edge and producting a new tier alpong with a contracting map.'''
  assert contracting_edge in self.edges, \
    'Edge to contract must be in `Tier.edges`'

  old_edge_list = self.edges
  new_vertex_list = []
  new_STpair_list = []
  new_ST_pair = ([],[])
  for edge in old_edge_list:
    new_edge = copy.deepcopy(edge)
    for i in [0,1]:
      if edge[i] == contracting_edge[0]:
        new_edge[i] = contracting_edge[1]
    new_vertex_list += new_edge
    if (new_edge[0] != new_edge[1]) and ([new_edge[0], new_edge[1]] not in new_STpair_list):
      new_STpair_list.append([new_edge[0], new_edge[1]])
      new_ST_pair[0].append(new_edge[0])
      new_ST_pair[1].append(new_edge[1])
  shifted_sources = [helpers.downshift_above(index, contracting_edge[0]) for index in new_ST_pair[0]]
  shifted_targets = [helpers.downshift_above(index, contracting_edge[0]) for index in new_ST_pair[1]]
  new_vertex_list = list(set(new_vertex_list))
  new_seed_graph = dgl.heterograph({('node', 'to', 'node'): (shifted_sources, shifted_targets)})
  output_tier = Tier(new_seed_graph)

  output_map = Tier_Map(self, output_tier)
  for index in self.vertices:
    output_map.partial_map.update({index : helpers.downshift_above(index, contracting_edge[0])})

  return output_tier, output_map

# Give method to class `Tier`
Tier.contract_edge = contract_edge


  
