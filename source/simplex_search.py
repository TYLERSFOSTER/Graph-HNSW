import copy

'''Local project modules'''
import helpers
import tower


'''
Classes
'''
class Bot():
  '''Class representing bot that crawls up HNSW tower, searching for simplices below a fixed dimension'''
  def __init__(self,
               tower_to_search,
               top_search_dimension=1,
               ):
    assert isinstance(tower_to_search, tower.Tower), 'Argument `tower_to_search` must be an instance of the class `tower.Tower`.'
    assert isinstance(top_search_dimension, int), 'Argument `top_search_dimension` must be a positive integer.'
    assert top_search_dimension > 0, 'Argument `top_search_dimension` must be a positive integer.'
    #-----------------------------------------
    '''Attributes that do NOT change as Bot searches'''
    self.tower = tower_to_search
    self.tier_indices = [tier_index for tier_index in self.tower.tiers]
    for tier_index in self.tier_indices:
      self.tower.tiers[tier_index].nondegen_sSet = copy.deepcopy(self.tower.tiers[tier_index].sSet).expunge_degenerates()
    tower_to_search.include_loops()
    self.top_dimension = top_search_dimension
    self.uppermost_index = self.tower.starting_index
    self.bottommost_index = self.tower.ending_index    
    '''Remove bottom tier if trivial'''
    bottom_sparse_pair = self.tower.tiers[self.bottommost_index].edges
    if bottom_sparse_pair == []:
      self.tower.tiers.pop(self.bottommost_index)
      self.tower.maps.pop((self.bottommost_index-1, self.bottommost_index))
      self.tower.length = len(self.tower.tiers)
      self.bottommost_index -= 1
      self.tower.ending_index = self.bottommost_index

    self.preimage_lookups = self.tower.build_preimage_lookups()
    self.edge_aids = {tier_index : {} for tier_index in self.tower.tiers}
    for tier_index in self.edge_aids:
      current_tier = self.tower.tiers[tier_index]
      current_vertices = current_tier.vertices
      current_edges = current_tier.edges
      self.edge_aids[tier_index] = {vertex : [] for vertex in current_vertices}
      for edge in current_edges:
        source_vertex = edge[0]
        target_vertex = edge[1]
        self.edge_aids[tier_index][target_vertex].append(source_vertex)
    '''Attributes that change as Bot searches'''
    self.fast_search_sSets = {}
    for tier_index in self.tower.tiers:
      if tier_index == self.bottommost_index:
        continue
      self.fast_search_sSets.update({tier_index : {}})
      current_sSet = self.tower.tiers[tier_index].sSet.simplices
      current_map = self.tower.maps[(tier_index, tier_index + 1)].partial_map
      for dimension in current_sSet:
        self.fast_search_sSets[tier_index].update({dimension : {}})
        current_simplices = current_sSet[dimension]
        for simplex in current_simplices:
          image_simplex = str([current_map[vertex] for vertex in simplex])
          if image_simplex not in self.fast_search_sSets[tier_index][dimension]:
            self.fast_search_sSets[tier_index][dimension].update({image_simplex : []})
          self.fast_search_sSets[tier_index][dimension][image_simplex].append(simplex)

      
    self.completion_log = {tier_index: 1 for tier_index in self.tower.tiers} # Because the simplicial set attached to each tier includes edges, the bot can start search at dimension 2
    self.search_index = self.bottommost_index # The bot holds attribute `Bot.search_index` that keeps track of the index wehre it last stopped its search
    self.search_dimension = 2 # The bot holds attribute `Bot.self.search_dimension` that keeps track of where its search halted
    


  def print_parameters(self):
    print('         Current search index:', self.search_index)
    print('         Current search dimension:', self.search_dimension)
    print('         Current simplicial set at this tier:', self.tower.tiers[self.search_index].sSet.simplices)

  
  def bottom_out_parameters(self):
    self.search_index = copy.deepcopy(self.bottommost_index)
    self.search_dimension = 0


  def update_parameters(self):
    '''Method that checks attributes of the search bot `self`, making sure that `self.search_index` and `self.search_dimension`'''
    '''The main `for` loop runs UP the tower, from bottom-most tier to tier just below upper-most tier:'''
    self.bottom_out_parameters()
    for difference in range(0, self.bottommost_index - self.uppermost_index):
      current_tier_index = self.bottommost_index - difference # We work with this index because we're moving up the tower, i.e., down in tier index
      above_tier_index = current_tier_index - 1
      '''The `if` block checks if current tier is more complete than above tier. If so, we switch to above tier, ready to search at its lowest incomplete dimension:'''
      if self.completion_log[above_tier_index] < self.completion_log[current_tier_index]:
        self.search_dimension = self.completion_log[above_tier_index] + 1
        self.search_index = above_tier_index
        break
      elif self.completion_log[above_tier_index] == self.completion_log[current_tier_index]:
        self.search_index = above_tier_index
        if self.search_index == self.uppermost_index:
          self.search_dimension = self.completion_log[current_tier_index] + 1
          self.search_index = self.bottommost_index
          break
      elif self.completion_log[above_tier_index] > self.completion_log[current_tier_index]:
        self.search_dimension = self.completion_log[current_tier_index] + 1
        self.search_index = current_tier_index
        break


  def raw(self):
    '''Method for `Bot` that runs a "raw," i,e., "no HNSW" search for next incomplete dimension in current search tier. Intended as base, in bottom of tower, for HNSW search'''
    max_complete_dimension = self.completion_log[self.search_index]
    self.search_dimension = self.completion_log[self.search_index] + 1
    '''If `self.tower.tiers[self.search_index].sSet.simplices` doesn't have `self.search_dimension` as a key yet, we update `self.tower.tiers[self.search_index].sSet.simplices` with this missing key'''
    if self.search_dimension not in self.tower.tiers[self.search_index].sSet.simplices:
      self.tower.tiers[self.search_index].sSet.simplices.update({self.search_dimension: []})
    current_simplices = self.tower.tiers[self.search_index].sSet.simplices[max_complete_dimension]
    if self.search_dimension > self.top_dimension: return
    '''The following triple loop is the major source of the time complexity of the `raw` algorithm.'''
    for potential_top_vertex in self.tower.tiers[self.search_index].vertices:
      source_vertices = self.edge_aids[self.search_index][potential_top_vertex]
      for simplex in current_simplices:
        simplex_contained_in_source_vertices = True
        for potential_source_vertex in simplex:
          simplex_contained_in_source_vertices *= (potential_source_vertex in source_vertices)
        if simplex_contained_in_source_vertices:
          new_simplex = simplex + [potential_top_vertex]
          self.tower.tiers[self.search_index].sSet.catalog_simplex(new_simplex, include_all_subsimplices=False, outlaw_degenerate_simplices=False) # IMPORTANT: `include_all_subsimplices=False`
    self.completion_log.update({self.search_index: self.search_dimension})


  def run(self):
    self.bottom_out_parameters()
    self.update_parameters()
    print('\n\n\n\n\n____________________________________________________________________')
    print('____________________________________________________________________')
    print('\nRetrieving Bot parameters at start of `run` search...')
    print('Completion log at start of `run` search:', self.completion_log)
    self.print_parameters()
    counter = 0
    while min([self.completion_log[k] for k in self.completion_log]) < self.top_dimension:
      print('\n\n\n   __________________________________')
      print('   New cycle of `run`\'s `while` loop.')
      if counter != 0:
        print('\n      Retrieving Bot parameters at start of this cycle...')
        print('      Completion log at start of this cycle:', self.completion_log)
        self.print_parameters()
      print('\n   Updating Bot parameters at start of this cycle...')
      self.update_parameters()
      self.print_parameters()
      if self.search_index == self.bottommost_index:
        print('\n      Running `raw` search...')
        self.raw()
        print('      `raw` search complete.')
        print('\n      Retrieving Bot parameters after `raw` search...')
        print('      Completion log at start of this cycle:', self.completion_log)
        self.print_parameters()
      else:
        print('\n      Executing subblock to run informed search for simplices in tier {}, based on tier {}...'.format(self.search_index, self.search_index+1))
        relevant_preimage_lookup = self.preimage_lookups[(self.search_index+1, self.search_index)]
        print('      Relevant pre-image look-up:', relevant_preimage_lookup)
        print('      Completion log at start of this cycle:', self.completion_log)
        present_tier_dimension = self.completion_log[self.search_index]
        max_downstairs_dimension = self.completion_log[self.search_index + 1]
        print('      Max dimension completed in present tier:', present_tier_dimension)
        print('      Max dimension completed in lower tier:', max_downstairs_dimension)
        for d in range(present_tier_dimension + 1, max_downstairs_dimension + 1):
          if self.search_dimension not in self.tower.tiers[self.search_index].sSet.simplices:
            self.tower.tiers[self.search_index].sSet.simplices.update({self.search_dimension : []})
          print('\n         Executing cycle of `for` loop within subblock, searching for dimension {} in tier {}...'.format(d, self.search_index, self.search_index, self.bottommost_index))
          print('         Retrieving Bot parameters after `raw` search...')
          print('         Completion log at start of this cycle:', self.completion_log)
          self.print_parameters()
          downstairs_simplices = self.tower.tiers[self.search_index + 1].sSet.simplices
          relevant_downstairs_simplices = downstairs_simplices[d]
          print('         Length of `relevant_downstairs_simplices`:', len(relevant_downstairs_simplices))
          print('         `relevant_downstairs_simplices`:', relevant_downstairs_simplices)
          for downstairs_simplex in relevant_downstairs_simplices:
            print('            Initiating search for non-degenerate {}-simplices in tier {} that happen to lie over the {}-simplex {} in tier {}.'.format(d+1, self.search_index, d+1, downstairs_simplex, self.search_index+1))
            relevant_fiber_sequence = [relevant_preimage_lookup[downstairs_vertex] for downstairs_vertex in downstairs_simplex]
            print('            `relevant_fibers`', relevant_fiber_sequence)

          print('\n         Cycle of `for` loop in `while` subblock now complete.')
      print('\n   Cycle of `while` loop now complete.')
      print('   __________________________________')

      counter += 1
      if counter > 2:
        print('There seems to be an infinite loop present.')
        break
        
