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
  assert isinstance(n, int)
  assert isinstance(index, int)
  if index > n:
    output = index-1
  else:
    output = index
  return output


def reverse_dictionary(input_dictionary):
  output_dictionary = {}
  for key in input_dictionary:
    value = input_dictionary[key]
    if value in output_dictionary:
      output_dictionary[value].append(key)
    else:
      output_dictionary.update({value: [key]})
  return output_dictionary


def max_key(input_dictionary):
  output = max(input_dictionary.keys())
  return output


def one_more_cut(sequence_of_cuts):
  rightmost_sublist = sequence_of_cuts[-1]
  existing_cuts = sequence_of_cuts[:-1]
  output_sequences = []
  for cut_index in range(1, len(rightmost_sublist)):
    new_sequence_of_cuts = copy.deepcopy(existing_cuts)
    left_half = rightmost_sublist[:cut_index]
    right_half = rightmost_sublist[cut_index:]
    new_sequence_of_cuts.append(left_half)
    new_sequence_of_cuts.append(right_half)
    output_sequences.append(new_sequence_of_cuts)
  return output_sequences


def all_partitions(input_list):
  output_partitions = {0 : [[input_list]]}
  N = len(input_list)
  while N not in output_partitions:
    indexing_keys = [key for key in output_partitions]
    for key in indexing_keys:
      if key+1 not in output_partitions:
        output_partitions.update({key+1 : []})
      indexing_sequences_of_cuts = copy.deepcopy(output_partitions[key])
      for sequence_of_cuts in indexing_sequences_of_cuts:
        new_sequences_of_cuts = one_more_cut(sequence_of_cuts)
        for sequence_of_cuts in new_sequences_of_cuts:
          if sequence_of_cuts not in output_partitions[key+1]:
            output_partitions[key+1].append(sequence_of_cuts)
  return output_partitions