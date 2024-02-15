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
  
  print('Test {} \u2014 '.format(test_counter) + test_description )
  try:
    function(*args, **kwargs)
    print('Test {} completed succesfully'.format(test_counter))
  except Exception as inst:
    print('Test {}: Failed'.format(test_counter))
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

def build_simplex_test(vertices, vertex_subset, check_dict):
  test_sSet = simplicial_set.NonDegenSSet()
  test_sSet.add_vertices(vertices)
  test_sSet.nondegen_simplex(vertex_subset)
  for key in check_dict:
    test_sSet.simplices[key] == check_dict[key]

  
'''
Dictionary of calls for testing
'''
call_dict = {
  'Test of `simplicial_set.all_sublists` on `[\'x\',\'y\',\'z\']`' : (helpers.all_sublists, [['x','y','z']]),
  'Test of free instantiation of `simplicial_set.NonDegenSSet`' : (simplicial_set.NonDegenSSet, []),
  'Test of `simplicial_set.NonDegenSSet().add_vertices([\'a\',\'00\',\'three\'])`': (add_vertices_test, [['a','00','three']]),
  'Test of `simplicial_set.NonDegenSSet().add_vertices([\'x\',\'y\',\'z\']).nondegen_simplex([\'x\',\'y\'])`' : (build_simplex_test, [['x','y','z'], ['x', 'y'], {1 : [['x', 'y']]}]),
  'Test of `simplicial_set.NonDegenSSet().add_vertices([\'w\',\'x\',\'y\',\'z\']).nondegen_simplex([\'w\',\'x\',\'y\'])`' : (build_simplex_test, [['w', 'x','y','z'], ['w', 'x', 'y'], {1: [['w', 'x'], ['w', 'y'], ['x', 'y']]}]),
  'Test of free instantiation of `tier.Tier`' : (tier.Tier, []),
  'Test of free instantiation of `tier.Tier`' : (tier.Tier, [[],{'seed_graph': dgl.heterograph({('node', 'to', 'node'): ([1,2], [2,3])})}]),
  'Test of free instantiation of `quotient_tower.Tower`' : (quotient_tower.Tower, []),
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

