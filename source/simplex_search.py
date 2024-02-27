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
      # print('Length of tower:', len(self.tower.tiers))
      # print('Bottom tier has collapsed to trivial graph.')
      # print('Removing bottom tier.')
      self.tower.tiers.pop(self.bottommost_index)
      self.tower.maps.pop((self.bottommost_index-1, self.bottommost_index))
      # print('Map keys:', [key for key in self.tower.maps])
      self.tower.length = len(self.tower.tiers)
      # print('Length of tower:', self.tower.length)
      # print('Bottom-most index:', self.bottommost_index)
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


  def raw(self):
    #print(self.tower.tiers[self.bottommost_index].sSet.simplices)
    '''Method for `Bot` that runs a "raw," i,e., "no HNSW" search for next incomplete dimension in current search tier. Intended as base, in bottom of tower, for HNSW search'''
    # print('New raw search run started.')
    # print('   `Bot.search_index` (tier to search):', self.search_index)
    # print('   `Bot.search_dimension` (dimension to search):', self.search_dimension)
    # print('   `self.tower.tiers[self.search_index].sSet.simplices`:', self.tower.tiers[self.search_index].sSet.simplices)
    max_complete_dimension = self.completion_log[self.search_index]
    self.search_dimension = max_complete_dimension + 1
    # print('   `max_complete_dimension`:', max_complete_dimension)
    # print('   `Bot.search_dimension`:', self.search_dimension)
    '''If `self.tower.tiers[self.search_index].sSet.simplices` doesn't have `self.search_dimension` as a key yet, we update `self.tower.tiers[self.search_index].sSet.simplices` with this missing key'''
    if self.search_dimension not in self.tower.tiers[self.search_index].sSet.simplices:
      # print('      Key missing from `self.tower.tiers[self.search_index].sSet.simplices`:', self.search_dimension)
      self.tower.tiers[self.search_index].sSet.simplices.update({self.search_dimension: []})
      # if self.search_dimension in self.tower.tiers[self.search_index].sSet.simplices:
        # print('      Missing key {} added to dictionary'.format(self.search_dimension))
        # print('      Currently found simplices:', self.tower.tiers[self.search_index].sSet.simplices)
    current_simplices = self.tower.tiers[self.search_index].sSet.simplices[max_complete_dimension]
    if self.search_dimension > self.top_dimension:
      return
    '''The following triple loop is the major source of the latency of the "raw" algorithm.'''
    for potential_top_vertex in self.tower.tiers[self.search_index].vertices:
      # print('         Current `potential_top_vertices`:', potential_top_vertex)
      # print('         Current `self.edge_aids`:', self.edge_aids)
      source_vertices = self.edge_aids[self.search_index][potential_top_vertex]
      # print('         Current `source_vertices`:', source_vertices)
      for simplex in current_simplices:
        # print('            Current `simplex`:', simplex)
        simplex_contained_in_source_vertices = True
        for potential_source_vertex in simplex:
          new_proposition = (potential_source_vertex in source_vertices)
          # print('               Value of `potential_source_vertex in source_vertices`:', new_proposition)
          simplex_contained_in_source_vertices *= (potential_source_vertex in source_vertices)
        if simplex_contained_in_source_vertices:
          new_simplex = simplex + [potential_top_vertex]
          '''It's critical to use  `include_all_subsimplices=False` in `nondegen_simplex` below to prevent a needless slowdown.'''
          self.tower.tiers[self.search_index].sSet.nondegen_simplex(new_simplex, include_all_subsimplices=False)
    self.completion_log.update({self.search_index: self.search_dimension})
    if self.search_dimension > self.top_dimension:
      if self.search_index > self.uppermost_index:
        self.search_index = self.search_index - 1
    # print('   Post raw search run `self.tower.tiers[self.search_index].sSet.simplices`:', self.tower.tiers[self.search_index].sSet.simplices)


  def update_parameters(self):
    for difference in range(1, self.bottommost_index - self.uppermost_index+1):
      current_tier_index = self.bottommost_index - difference # We work with this index because we're moving up the tower, i.e., down in tier index
      above_tier_index = current_tier_index - 1
      highest_completed_at_this_tier = self.completion_log[current_tier_index]
      highest_completed_at_tier_above = self.completion_log[above_tier_index]
      if highest_completed_at_tier_above < highest_completed_at_this_tier:
        self.search_index = above_tier_index
        self.search_dimension = highest_completed_at_tier_above + 1


  def run(self):
    self.update_parameters()
    if self.search_dimension > self.top_dimension: # If our current search dimension is higher than our top dimension, then stop search
      return
    if self.search_index == self.bottommost_index: # In this case, our search space is the enite bottom tier, using the (k-1)-skeleton of the bottom tier
      search_space = {}
    else: # In this case, we have to use our knowledge of the (k-1)-simplices in the tier below to narrow our search space
      search_space = {}