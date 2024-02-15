import traceback
import dgl
import torch
import copy

import tier
import quotient_tower
import simplicial_set



def test_call(function, test_counter, *args):
  assert isinstance(test_counter, int), \
    '`test_counter` must be an integer.'
  
  print('Test {}: Testing call {}'.format(test_counter, str(function)))
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

  call_list = [
    (tier.Tier, []), # Test free instantiation of `tier.Tier`
    (quotient_tower.Tower, []), # Test free instantiation of `tier.Tier`
    (simplicial_set.NonDegenSSet, []), # Test free instantiation of `simplicial_set.NonDegenSSet`
    (add_vertices_test, [['a','00','three']]), # Test `add_vertices` foor `simplicial_set.NonDegenSSet`
    (simplicial_set.all_sublists, [['x','y','z']]),
    (build_simplex_test, [['x','y','z'], ['x', 'y']]),
       ]
  
  test_counter = 0
  for function, argument_list in call_list:
    test_counter = test_call(function, test_counter, *argument_list)

