import traceback
import dgl
import torch
import copy

'''Local project modules'''
import helpers
import simplicial_set
import tier
import quotient_tower


'''
Basic wrapper for testing calls
'''
def test_call(test_description, function, test_counter, *args, **kwargs):
  assert isinstance(test_counter, int), \
    '`test_counter` must be an integer.'
  
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
Define complex calls for testing
'''
def add_vertices_test(vertex_labels):
  test_sSet = simplicial_set.NonDegenSSet()
  test_sSet.add_vertices(vertex_labels)
  assert test_sSet.extract_vertices() == vertex_labels
  del(test_sSet)

def build_simplex_test(vertices, vertex_subset, check_dict):
  test_sSet = simplicial_set.NonDegenSSet()
  test_sSet.add_vertices(vertices)
  test_sSet.nondegen_simplex(vertex_subset)
  for key in check_dict:
    test_sSet.simplices[key] == check_dict[key]
  del(test_sSet)

def name_simplex_in_tier(edge_pair, vertex_subset):
  seed_graph = dgl.heterograph({('node', 'to', 'node'): edge_pair})
  test_tier = tier.Tier(seed_graph)
  test_tier.name_simplex(vertex_subset)
  del(seed_graph)
  del(test_tier)

def contract_single_edge(edge_pair, edge):
  seed_graph = dgl.heterograph({('node', 'to', 'node'): edge_pair})
  test_tier = tier.Tier(seed_graph)
  test_tier.contract_edge(edge)
  del(seed_graph)
  del(test_tier)


  
'''
Dictionary of calls for testing
'''
call_dict = {
  'Test of `simplicial_set.all_sublists` on `[\'x\',\'y\',\'z\']`' : \
    (helpers.all_sublists, [['x','y','z']]),
  'Test of free instantiation of `simplicial_set.NonDegenSSet`' : \
    (simplicial_set.NonDegenSSet, []),
  'Test of `simplicial_set.NonDegenSSet().add_vertices([1,4,7])`': \
    (add_vertices_test, [[1,4,7]]),
  'Test of `simplicial_set.NonDegenSSet().add_vertices([0,1,2]).nondegen_simplex([0,1])`' : \
    (build_simplex_test, [[0,1,2], [0,1], {1 : [[0,1]]}]),
  'Test of `simplicial_set.NonDegenSSet().add_vertices([0,1,2,3]).nondegen_simplex([0,1,2])`' : \
    (build_simplex_test, [[0,1,2,3], [0,1,2], {1: [[0,1], [0,2], [1, 2]]}]),
  'Test of `simplicial_set.from_graph`' : \
    (simplicial_set.from_graph, [dgl.heterograph({('node', 'to', 'node'): ([1,2], [2,3])})]),
  'Test of `tier.Tier` on `simplicial_set.from_graph(dgl.heterograph({(\'node\', \'to\', \'node\'): ([1,2], [2,3])}))`' : \
    (tier.Tier, [dgl.heterograph({('node', 'to', 'node'): ([1,2], [2,3])})]),
  'Test of `simplicial_set.from_graph` on `([1,1,2], [2,3,3])`, and then naming of 3-simplex present within' : \
    (name_simplex_in_tier, [([1,1,2], [2,3,3]), [1,2,3]]),
  'Test of `contract_edge` applied to edge `[1,3]` in 1-dimensional boundary' + u'\u2202' +'\u0394[2] (on vertices indexed 1, 2, 3)' : \
    (contract_single_edge, [([1,1,2], [2,3,3]), [1,3]]),
  'Test of free instantiation of `quotient_tower.Tower`' : \
    (quotient_tower.Tower, []),
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

