'''Local project modules'''
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
    self.completion_log = {tier_index: 1 for tier_index in self.tower.tiers} # Because the simplicial set attached to each tier includes edges, the bot can start search at dimension 2
    self.search_index = self.bottommost_index # The bot holds attribute `Bot.search_index` that keeps track of the index wehre it last stopped its search
    self.search_dimension = 2 # The bot holds attribute `Bot.self.search_dimension` that keeps track of where its search halted

  
  def update_parameters(self):
    '''Method that checks attributes of the search bot `self`, making sure that `self.search_index` and `self.search_dimension`'''
    '''The main `for` loop runs UP the tower, from bottom-most tier to tier just below upper-most tier:'''
    for difference in range(0, self.bottommost_index - self.uppermost_index):
      current_tier_index = self.bottommost_index - difference # We work with this index because we're moving up the tower, i.e., down in tier index
      above_tier_index = current_tier_index - 1
      highest_completed_at_this_tier = self.completion_log[current_tier_index]
      highest_completed_at_tier_above = self.completion_log[above_tier_index]
      '''The `if` block checks if current tier is more complete than above tier. If so, we switch to above tier, ready to search at its lowest incomplete dimension:'''
      if highest_completed_at_tier_above < highest_completed_at_this_tier:
        self.search_dimension = highest_completed_at_tier_above + 1
        self.search_index = above_tier_index
      elif highest_completed_at_tier_above >= highest_completed_at_this_tier:
        self.search_dimension = highest_completed_at_this_tier + 1
    print('Updated tier index to search:', self.search_index)
    print('Updated dimension to search:', self.search_dimension)


  def raw(self):
    '''Method for `Bot` that runs a "raw," i,e., "no HNSW" search for next incomplete dimension in current search tier. Intended as base, in bottom of tower, for HNSW search'''
    max_complete_dimension = self.completion_log[self.search_index]
    self.search_dimension = max_complete_dimension + 1
    '''If `self.tower.tiers[self.search_index].sSet.simplices` doesn't have `self.search_dimension` as a key yet, we update `self.tower.tiers[self.search_index].sSet.simplices` with this missing key'''
    if self.search_dimension not in self.tower.tiers[self.search_index].sSet.simplices:
      self.tower.tiers[self.search_index].sSet.simplices.update({self.search_dimension: []})
    current_simplices = self.tower.tiers[self.search_index].sSet.simplices[max_complete_dimension]
    if self.search_dimension > self.top_dimension:
      return
    '''The following triple loop is the major source of the time complexity of the `raw` algorithm.'''
    for potential_top_vertex in self.tower.tiers[self.search_index].vertices:
      source_vertices = self.edge_aids[self.search_index][potential_top_vertex]
      for simplex in current_simplices:
        simplex_contained_in_source_vertices = True
        for potential_source_vertex in simplex:
          new_proposition = (potential_source_vertex in source_vertices)
          simplex_contained_in_source_vertices *= (potential_source_vertex in source_vertices)
        if simplex_contained_in_source_vertices:
          new_simplex = simplex + [potential_top_vertex]
          self.tower.tiers[self.search_index].sSet.nondegen_simplex(new_simplex, include_all_subsimplices=False) # IMPORTANT: `include_all_subsimplices=False`
    self.completion_log.update({self.search_index: self.search_dimension})
    # if self.search_dimension > self.top_dimension and self.search_index > self.uppermost_index):
    #   self.search_index = self.search_index - 1


  def run(self):
    counter = 0
    while min([self.completion_log[k] for k in self.completion_log]) < self.top_dimension:
      print('Completion log:', self.completion_log)
      self.update_parameters()
      if self.search_index == self.bottommost_index:
        self.raw()
      else:
        max_downstairs_dimension = self.completion_log[self.search_index + 1]
        for d in range(0, max_downstairs_dimension + 1):
          current_downstairs_simplices = self.tower.tiers[self.search_index + 1].sSet.simplices[d]

      counter += 1
      if counter > 10:
        print('There seems to be an infinite loop present.')
        break
        
