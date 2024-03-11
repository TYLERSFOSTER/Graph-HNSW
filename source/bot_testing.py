import simplex_search

def run_for_testing(self):
  self.bottom_out_parameters()
  self.update_parameters()
  print('\n\n\n\n\n____________________________________________________________________')
  print('____________________________________________________________________')
  print('\nRetrieving Bot parameters at start of `run` search...')
  print('Completion log at start of `run` search:', self.completion_log)
  self.print_parameters()
  counter = 0
  while min([self.completion_log[k] for k in self.completion_log]) < self.top_dimension:
    print('\n\n   __________________________________')
    print('   New cycle of `Bot.run`\'s `while` loop.')
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
      d = self.search_dimension
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
        truncated_downstairs = downstairs_simplex[:-1]
        if str(truncated_downstairs) not in self.fast_search_sSets[self.search_index][d-1]:
          continue
        initial_subsimplices = self.fast_search_sSets[self.search_index][d-1][str(truncated_downstairs)]
        terminal_fiber = relevant_preimage_lookup[downstairs_simplex[-1]]
        print('            `terminal_fiber`:', terminal_fiber)
        print('            Truncated downstairs simplex:', truncated_downstairs)
        print('            `Bot.fast_search_sSets`:', initial_subsimplices)
        for terminal_vertex in terminal_fiber:
          for initial_simplex in initial_subsimplices:
            forms_full_simplex = True
            for initial_vertex in initial_simplex:
              if [initial_vertex, terminal_vertex] not in self.tower.tiers[self.search_index].edges:
                forms_full_simplex = False
                break
            if forms_full_simplex == True:
              new_simplex = initial_simplex + [terminal_vertex]
              if self.search_dimension not in self.tower.tiers[self.search_index].sSet.simplices:
                self.tower.tiers[self.search_index].sSet.simplices.update({self.search_dimension : []})
              self.tower.tiers[self.search_index].sSet.simplices[self.search_dimension].append(new_simplex)
              if self.search_dimension not in self.fast_search_sSets[self.search_index]:
                self.fast_search_sSets[self.search_index].update({self.search_dimension : {}})
              if str(downstairs_simplex) not in self.fast_search_sSets[self.search_index][self.search_dimension]:
                self.fast_search_sSets[self.search_index].update({self.search_dimension : {str(downstairs_simplex):[]}})
              self.fast_search_sSets[self.search_index][self.search_dimension][str(downstairs_simplex)].append(new_simplex)
      print('               `self.fast_search_sSets[self.search_index][self.search_dimension]`:', self.fast_search_sSets[self.search_index][self.search_dimension])
    self.completion_log[self.search_index] = self.search_dimension
    self.update_parameters()
    ('\n         Cycle of `for` loop in `while` subblock now complete.')
    print('\n   Cycle of `Bot.run`\'s `while` loop now complete.')
    print('   __________________________________')
    
    counter += 1
    if self.cycle_limit:
      if counter > self.cycle_limit:
        print('The cycle count in `Bot.run`\'s `while` loop has exceeded the value of `Bot.cycle_limit`.')
        break
simplex_search.Bot.run_for_testing = run_for_testing