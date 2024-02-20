import traceback
import dgl

'''Local project modules'''
import helpers
import simplicial_set
import tier
import tower
import simplices_search


'''
Basic wrapper for testing calls
'''
def test_call(test_description, function, test_counter, *args, **kwargs):
  assert isinstance(test_counter, int), \
    '`test_counter` must be an integer.'
  #-----------------------------------------
  print('Test {} \u2014 '.format(test_counter) + test_description)
  try:
    function(*args, **kwargs)
    print('Test {} completed succesfully'.format(test_counter))
  except Exception as inst:
    print('Test {} failed \u2014 '.format(test_counter) + test_description)
    print('Details of test failure:')
    print('\n', inst.__class__, '\n')
    for exception_argument in inst.args:
        print(exception_argument)
    print('\n', traceback.format_exc())
  return test_counter + 1


'''
Define more complex calls for some of the more complex testing
'''
def reverse_dictionary_test():
  test_dictionary = {1:2, 2:3, 3:2}
  test_output = helpers.reverse_dictionary(test_dictionary)
  assert test_output == {2:[1,3], 3:[2]}

def downshift_test(m, n):
  assert m > n, 'Arguments m and n must be integers satisfying m > n.'
  assert helpers.downshift_above(m,n) == m-1
  assert helpers.downshift_above(n,m) == n

def add_vertices_test(vertex_labels):
  test_sSet = simplicial_set.NonDegenSSet()
  test_sSet.add_vertices(vertex_labels)
  assert test_sSet.extract_vertices() == vertex_labels
  
def build_simplex_test(vertices, vertex_subset, check_dict):
  test_sSet = simplicial_set.NonDegenSSet()
  test_sSet.add_vertices(vertices)
  test_sSet.nondegen_simplex(vertex_subset)
  for key in check_dict:
    test_sSet.simplices[key] == check_dict[key]

def name_simplex_in_tier(edge_pair, vertex_subset):
  seed_graph = dgl.heterograph({('node', 'to', 'node'): edge_pair})
  test_tier = tier.Tier(seed_graph)
  test_tier.name_simplex(vertex_subset)

def contract_single_edge(edge_pair, edge):
  seed_graph = dgl.heterograph({('node', 'to', 'node'): edge_pair})
  test_tier = tier.Tier(seed_graph)
  test_tier.contract_edge(edge)

def contract_random_edge_test(edge_pair, edge):
  seed_graph = dgl.heterograph({('node', 'to', 'node'): edge_pair})
  test_tier = tier.Tier(seed_graph)
  test_tier.contract_random_edge()

def successive_quotients(edge_pair, edge_1, edge_2):
  seed_graph = dgl.heterograph({('node', 'to', 'node'): edge_pair})
  tier_0 = tier.Tier(seed_graph)
  tier_1 = tier_0.contract_edge(edge_1)[0]
  tier_2 = tier_1.contract_edge(edge_2)[0]

def compose_maps_test(edge_pair, edge_1, edge_2):
  seed_graph = dgl.heterograph({('node', 'to', 'node'): edge_pair})
  tier_0 = tier.Tier(seed_graph)
  tier_1, tier_map_0 = tier_0.contract_edge(edge_1)
  tier_2, tier_map_1 = tier_1.contract_edge(edge_2)
  composite_map = tier.compose_maps(tier_map_0, tier_map_1)

def random_contractions_test(edge_pair, n):
  seed_graph = dgl.heterograph({('node', 'to', 'node'): edge_pair})
  tier_0 = tier.Tier(seed_graph)
  tier_2, tier_map_0 = tier_0.random_contractions(n)

def tower_length_test(edge_pair, ratio_value):
  current_tower = tower.Tower(dgl.heterograph({('node', 'to', 'node'): edge_pair}), sample_ratio=ratio_value)

  
'''
Dictionary of calls for testing
'''
call_dict = {
  'Test of `reverse_dictionary` on {1:2, 2:3, 3:2}' : (reverse_dictionary_test, []),
  'Test of `downshift_above(m, n)` for m > n' : (downshift_test, [6, 5]),
  'Test of `simplicial_set.all_sublists` on `[\'x\',\'y\',\'z\']`' : (helpers.all_sublists, [['x','y','z']]),
  'Test of `helpers.max_index` on {1:2, 2:3, 3:2}' : (helpers.max_key, [{1:2, 2:3, 3:2}]),
  'Test of free instantiation of `simplicial_set.NonDegenSSet`' : (simplicial_set.NonDegenSSet, []),
  'Test of `simplicial_set.NonDegenSSet().add_vertices([1,4,7])`': (add_vertices_test, [[1,4,7]]),
  'Test of `simplicial_set.NonDegenSSet().add_vertices([0,1,2]).nondegen_simplex([0,1])`' : (build_simplex_test, [[0,1,2], [0,1], {1 : [[0,1]]}]),
  'Test of `simplicial_set.NonDegenSSet().add_vertices([0,1,2,3]).nondegen_simplex([0,1,2])`' : (build_simplex_test, [[0,1,2,3], [0,1,2], {1: [[0,1], [0,2], [1, 2]]}]),
  'Test of `simplicial_set.from_graph`' : (simplicial_set.from_graph, [dgl.heterograph({('node', 'to', 'node'): ([1,2], [2,3])})]),
  'Test of `tier.Tier` on `simplicial_set.from_graph(dgl.heterograph({(\'node\', \'to\', \'node\'): ([1,2], [2,3])}))`' : (tier.Tier, [dgl.heterograph({('node', 'to', 'node'): ([1,2], [2,3])})]),
  'Test of `simplicial_set.from_graph` on `([1,1,2], [2,3,3])`, and then naming of 3-simplex present within' : (name_simplex_in_tier, [([1,1,2], [2,3,3]), [1,2,3]]),
  'Test of `contract_edge` applied to edge `[1,3]` in 1-dimensional boundary ' + u'\u2202' +'\u0394[2] (on vertices indexed 1, 2, 3)' : (contract_single_edge, [([1,1,2], [2,3,3]), [1,3]]),
  'Test of `contract_random_edge`' : (contract_random_edge_test, [([1,1,2], [2,3,3]), [1,3]]),
  'Test of succesive applications of `contract_edge` applied to edge `[1,3]` in 1-dimensional boundary ' + u'\u2202' +'\u0394[2] (on vertices indexed 1,2,3)' : (successive_quotients, [([1,1,2], [2,3,3]), [1,3], [1,2]]),
  'Test of `compose_maps` on graph ([0,1,2,3], [1,2,3,0]), contracting edge [0,1], and then again contracting edge [0,1]' : (compose_maps_test, [([0,1,2, 3], [1,2,3,0]), [0,1], [0,1]]),
  'Test of `random_contractions_test` on graph ([0,1,2,3,4,5], [1,2,3,4,5,0]), with 4 successive contractions' : (random_contractions_test, [([0,1,2,3,4,5], [1,2,3,4,5,0]), 4]),
  'Test of `random_contractions_test` on graph ([0,1,2,3], [1,2,3,0]), with 3 successive contractions' : (random_contractions_test, [([0,1,2,3], [1,2,3,0]), 3]), # Debugging needs to start with key error here...
  'Test of free instantiation of `quotient_tower.Tower`' : (tower.Tower, [dgl.heterograph({('node', 'to', 'node'): ([1,2], [2,3])})]),
  'Test of `tower.Tower` on length-4 cycle graph ([0,1,2, 3], [1,2,3,0]) at edge contraction rate 0.5' : (tower.Tower, [dgl.heterograph({('node', 'to', 'node'): ([0,1,2, 3], [1,2,3,0])})]),
  'Test of `tower.Tower.length` on length-7 cycle graph at edge contraction rate 0.2' : (tower_length_test, [([0,1,2,3,4,5,6], [1,2,3,4,5,6,0]), .2]),
  'Test of `simplices_search.Bot` instantiated from `tower.Tower` on length-7 cycle graph at edge contraction rate 0.2' : (simplices_search.Bot, [tower.Tower(dgl.heterograph({('node', 'to', 'node'): ([0,1,2, 3], [1,2,3,0])}), sample_ratio=.2)]),
}


'''
Testing block
'''
if __name__ == '__main__':
  test_counter = 0
  for key in call_dict:
    function, argument_list = call_dict[key]
    test_description = key
    test_counter = test_call(test_description, function, test_counter, *argument_list)