import dgl
import torch
import copy


'''
Helper functions
'''
def all_sublists(input_list):
  '''Generates all (ordered) sublists of a given list'''
  output = [[]]
  for element in input_list:
    existing_sublists = list(copy.deepcopy(output))
    for sublist in existing_sublists:
      sublist.append(element)
      output.append(sublist)
  return output


def downshift_above(index, n):
  '''For re-indexing vertices: shifts index down by 1 if index is larger than some fixed integer.'''
  assert isinstance(n, int)
  assert isinstance(index, int)

  if index > n:
    output = index-1
  else:
    output = index

  return output