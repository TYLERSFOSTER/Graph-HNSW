import copy
import random


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
  if index > n: output = index-1
  else: output = index
  return output


def reverse_dictionary(input_dictionary):
  '''For the roles of keys and values in a dictionary.'''
  output_dictionary = {}
  for key in input_dictionary:
    value = input_dictionary[key]
    if value in output_dictionary: output_dictionary[value].append(key)
    else: output_dictionary.update({value: [key]})
  return output_dictionary


def one_more_cut(given_partition):
  '''Generates all partitions obtained from a given partition by adding one cut to rightmost cell in the given partition.'''
  rightmost_sublist = given_partition[-1]
  existing_cuts = given_partition[:-1]
  output_list_of_partitions = []
  for cut_index in range(1, len(rightmost_sublist)):
    new_partition = copy.deepcopy(existing_cuts)
    left_half = rightmost_sublist[:cut_index]
    right_half = rightmost_sublist[cut_index:]
    new_partition.append(left_half)
    new_partition.append(right_half)
    output_list_of_partitions.append(new_partition)
  return output_list_of_partitions


def all_partitions(input_list):
  '''Generates all partitions of a given list, organized in a dictionary where `dict[key]` is a list of all partitions with key+1 many cells.'''
  output_partition_dictionary = {0 : [[input_list]]}
  key = 0
  while len(input_list) not in output_partition_dictionary:
    output_partition_dictionary.update({key+1 : []})
    for sequence_of_cuts in output_partition_dictionary[key]:
      output_partition_dictionary[key+1] = output_partition_dictionary[key+1] + one_more_cut(sequence_of_cuts)
    key += 1
  output_partition_dictionary.pop(key)
  return output_partition_dictionary