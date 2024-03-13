import traceback
import dgl

'''Local project modules'''
import helpers
import simplicial_set
import tier
import tower
import simplex_search


'''
Basic wrapper for testing calls
'''
def test_call(test_description, function, test_counter, *args, **kwargs):
  assert isinstance(test_counter, int), '`test_counter` must be an integer.'
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

def run_search_with_nondegen_test(edge_pair, ratio_value):
  test_tower = tower.Tower(dgl.heterograph({('node', 'to', 'node'): edge_pair}), sample_ratio=ratio_value)
  test_bot = simplex_search.Bot(test_tower)
  test_bot.top_dimension = 3
  test_bot.run()
  test_bot.expunge_degenerates()

  
'''
Dictionary of calls for testing
'''
call_dict = {
  'Test of `simplices_search.Bot.run` with expunge_degenerates`' : (run_search_with_nondegen_test, [([0,0,1,2,2,3,4,0,0], [1,2,2,3,4,4,0,3,4]), .2], {}),
}


'''
Testing block
'''
if __name__ == '__main__':
  print('\n\nBeginning testing block...\n')
  test_counter = 0
  for key in call_dict:
    function, argument_list, keyword_argument_dictionary  = call_dict[key]
    test_description = key
    test_counter = test_call(test_description, function, test_counter, *argument_list, **keyword_argument_dictionary)