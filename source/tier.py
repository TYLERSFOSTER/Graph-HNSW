import dgl
import copy
import random

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
               include_loops=False,
               ):
    self.sSet = simplicial_set.from_graph(seed_graph)
    self.vertices = self.sSet.extract_vertices()
    self.sparse_edges = self.sSet.extract_edges()
    self.edges = [[self.sparse_edges[0][k], self.sparse_edges[1][k]] for k in range(len(self.sparse_edges[0]))]
    self.graph = seed_graph
    if include_loops:
      self.include_loops()
    

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
    if is_present: self.sSet.catalog_simplex(vertex_list)

      
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
    self.downstairs_vertices = self.downstairs.vertices
    self.partial_map = {}

  def partial_preimage(self):
    output = helpers.reverse_dictionary(self.partial_map)
    return output
  

class Tier_Fibration():
  '''Class representing the fibration of simplicial sets implicit in a `Tier_Map`'''
  def __init__(self,
               tier_map
               ):
    assert isinstance(tier_map, Tier_Map)
    self.tier_map = tier_map
    self.simplicial_fibers = {vertex : simplicial_set.SSet() for vertex in self.tier_map.downstairs_vertices} 
    for image_vertex in self.simplicial_fibers:
      preimage = [preimage_vertex for preimage_vertex in self.tier_map.upstairs_vertices if self.tier_map.partial_map[preimage_vertex] == image_vertex]
      self.simplicial_fibers[image_vertex].simplices[0] = [[v] for v in preimage]
      self.simplicial_fibers[image_vertex].simplices.update({1 : []}) # Debugging: changed  index `2` to `1`
      for u in preimage:
        for v in preimage:
          candidate_edge = [u, v]
          if candidate_edge in self.tier_map.upstairs.edges:
            self.simplicial_fibers[image_vertex].simplices[1].append(candidate_edge) # Debugging: changed  index `2` to `1`



'''
Further functions and methods for above class(es)
'''
def contract_edge(self, contracting_edge):
  '''Method for `Tier` contracting a single edge and producting a new tier alpong with a contracting map.'''
  assert contracting_edge in self.edges, 'Edge to contract must be in `Tier.edges`'
  #-----------------------------------------
  old_edge_list = self.edges
  new_vertex_list = []
  new_STpair_list = []
  new_ST_pair = ([],[])
  for edge in old_edge_list:
    new_edge = copy.deepcopy(edge)
    for i in [0,1]:
      if edge[i] == contracting_edge[0]: new_edge[i] = contracting_edge[1]
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
    if index != contracting_edge[0]: output_map.partial_map.update({index : helpers.downshift_above(index, contracting_edge[0])})
    else: output_map.partial_map.update({contracting_edge[0] : helpers.downshift_above(contracting_edge[1], contracting_edge[0])})
  return output_tier, output_map
Tier.contract_edge = contract_edge


def contract_random_edge(self):
  all_edges = self.edges
  contracting_edge = random.sample(all_edges, 1)[0]
  output_tier, output_map = self.contract_edge(contracting_edge)
  return output_tier, output_map
Tier.contract_random_edge = contract_random_edge


def compose_maps(*args):
  assert len(args) > 0
  for k, tier_map in enumerate(args):
    assert isinstance(tier_map, Tier_Map)
    if k < len(args)-1: assert tier_map.downstairs == args[k+1].upstairs
  initial_values = args[0].upstairs.vertices
  composite_map = {key : key for key in initial_values}
  composite_input = list(composite_map.keys())
  tier_counter = 0
  for tier_map in args:
    F = tier_map.partial_map
    new_composite_map = {}
    for input_value in composite_input:
      old_composite_value = int(composite_map[input_value])
      output_value = int(F[old_composite_value])
      new_composite_map.update({input_value : output_value})
    composite_map = new_composite_map
    tier_counter += 1
  output = Tier_Map(args[0].upstairs, args[-1].downstairs)
  output.partial_map = composite_map
  return output


def random_contractions(self, n):
  assert len(self.edges) >= n, 'Graph must have at least n edges if we plan to contract n edges.'
  assert isinstance(n, int)
  assert n > 0
  map_counter = n
  output_maps = []
  output_tier = copy.deepcopy(self)
  # This loop needs to be rewritten, because it is too memory intensive. It should do each composition pairwise, redfining variables each time.
  while len(output_tier.edges) > 0 and map_counter > 0:
    output_tier, output_map = output_tier.contract_random_edge()
    output_maps.append(output_map)
    map_counter -= 1
  composite_quotient_map = compose_maps(*output_maps)
  return output_tier, composite_quotient_map
Tier.random_contractions = random_contractions


def include_loops(self):
    for vertex in self.vertices:
      self.sparse_edges[0].append(vertex); self.sparse_edges[1].append(vertex)
      new_edge = [vertex, vertex]
      self.edges.append(new_edge)
      self.graph = dgl.heterograph({('node', 'to', 'node'): self.edges})
      self.sSet.simplices[1].append(new_edge)
Tier.include_loops = include_loops