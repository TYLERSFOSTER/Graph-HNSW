import traceback
import dgl
import torch
import copy

import tier
import quotient_tower
import simplicial_set


call_dict = {
  'Test of free instantiation of `tier.Tier`' : (tier.Tier, []),
  'Test of free instantiation of `tier.Tier`' : (quotient_tower.Tower, []),
  'Test of free instantiation of `simplicial_set.NonDegenSSet`' : (simplicial_set.NonDegenSSet, []),
  'Test of `simplicial_set.NonDegenSSet().add_vertices([\'a\',\'00\',\'three\'])`': (add_vertices_test, [['a','00','three']]),
  'Test of `simplicial_set.all_sublists` on `[\'x\',\'y\',\'z\']`' : (simplicial_set.all_sublists, [['x','y','z']]),
  'Test of `simplicial_set.NonDegenSSet().add_vertices([\'x\',\'y\',\'z\']).nondegen_simplex([\'x\',\'y\'])`' : (build_simplex_test, [['x','y','z'], ['x', 'y']]),
}


def test_call(test_description, function, test_counter, *args):
  assert isinstance(test_counter, int), \
    '`test_counter` must be an integer.'
  
  print('Test {} \U2014 '.format(test_counter) + test_description)
  try:
    function(*args)
    print('Test {}: Completed succesfully'.format(test_counter))
  except Exception as inst:
    print('Test {}: Failed'.format(test_counter))
    print('Details of test failure:')
    print('\n', inst.__class__, '\n')
    for exception_argument in inst.args:
        print(exception_argument)
    print('\n', traceback.format_exc())
  
  return test_counter + 1


'''
More complex calls to test
'''
def add_vertices_test(vertex_labels):
  test_sSet = simplicial_set.NonDegenSSet()
  test_sSet.add_vertices(vertex_labels)
  assert test_sSet.simplices[0] == vertex_labels

def build_simplex_test(vertices, vertex_subset):
  test_sSet = simplicial_set.NonDegenSSet()
  test_sSet.add_vertices(vertices)
  test_sSet.nondegen_simplex(vertex_subset)


'''
Testing block
'''
if __name__ == '__main__':
  test_counter = 0
  for key in call_list:
    function, argument_list = call_list[key]
    test_description = key
    test_counter = test_call(test_description, function, test_counter, *argument_list)

