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
    self.tower = tower_to_search
    self.top_dimension = top_search_dimension
    self.uppermost_index = self.tower.starting_index
    self.bottommost_index = self.tower.ending_index
    self.top_sSet = self.tower.tiers[self.uppermost_index].sSet
    self.preimage_lookups = self.tower.build_preimage_lookups()
    self.completion_log = {tier_index: 1 for tier_index in self.tower.tiers} # Because the simplicial set attached to each tier includes edges, the bot can start search at dimension 2
    self.search_index = self.bottommost_index # The bot holds attribute `Bot.search_index` that keeps track of the index wehre it last stopped its search
    self.search_tier = self.tower.tiers[self.search_index] # The bot holds attribute `Bot.search_tier` that keeps track of the tier where it last stopped its search
    self.found_sSet = self.search_tier.sSet # The bot holds attribute `Bot.found_sSet` that keeps track of the tier where it last stopped its search
    self.search_dimension = 2 # The bot holds attribute `Bot.self.search_dimension` that keeps track of where its search halted


  def update_parameters(self):
    for difference in range(1, self.bottommost_index - self.uppermost_index+1):
      current_tier_index = self.bottommost_index - difference # We work with this index because we're moving up the tower, i.e., down in tier index
      above_tier_index = current_tier_index - 1
      highest_completed_at_this_tier = self.completion_log[current_tier_index]
      highest_completed_at_tier_above = self.completion_log[cabove_tier_index]
      if highest_completed_at_tier_above < highest_completed_at_this_tier:
        self.search_index = above_tier_index
        self.search_tier = self.tower.tiers[self.search_index]
        self.found_sSet = self.search_tier.sSet
        self.search_dimension = highest_completed_at_tier_above + 1


'''
Further functions and methods for above class(es)
'''
def raw(self):
  '''Method for `Bot` that runs a "raw," i,e., "no HNSW" search for next incomplete dimension in a single tier, for searching bottommost tier of the tower'''
  current_index = self.search_index
  current_tier = self.search_tier
  current_sSet = self.found_sSet
  max_complete_dimension = self.completion_log[current_index]
  if max_complete_dimension >= self.top_dimension:
    return
  else:
    min_incomplete_dimension = max_complete_dimension - 1
  '''Will write this next. This funciton is really just the search algorithm as it existed before HNSW...'''
'''Give method `raw` to class `Bot`'''
Bot.raw = raw
  

def run(self):
  self.update_parameters()
  if self.search_dimension > self.top_dimension: # If our current search dimension is higher than our top dimension, then stop search
    return
  if self.search_index == self.bottommost_index: # In this case, our search space is the enite bottom tier, using the (k-1)-skeleton of `self.found_sSet`
    search_space = {}
  else: # In this case, we have to use our knowledge of the (k-1)-simplices in the tier below to narrow our search space
    search_space = {}
  '''The bulk of this function will be that previous algorithm that goes vertex-by-vertex checking if top verte of simplex...'''


