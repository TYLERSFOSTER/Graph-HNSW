class Tower():
  def __init__(self,
               sample_ratio=0.0,
               seed_graph=dgl.heterograph({('node', 'to', 'node'): (src, dst)}),
               bottom_level=0,
               ):
            
    assert isinstance(seed_graph, dgl.DGLHeteroGraph), \
        'Keyword argument `seed_graph` of graph_towers\'s init method must be a dgl.DGLHeteroGraph.'
    assert isinstance(sample_ratio, float), \
        'Keyword argument `sample_ratio` of graph_towers\'s init method must be a float.'
    assert sample_ratio<=1. and sample_ratio>=0., \
        'Keyword argument `ratio` of graph_towers\'s init method must be between 0 and 1.'
    assert isinstance(bottom_level, int), \
        'Keyword argument `bottom_level` of graph_towers\'s init method must be an integer.'

    self.seed_graph = seed_graph
    self.srcs_and_dsts = self.seed_graph.edges()        
    self.sample_ratio = sample_ratio
    self.updated_graph = dgl.heterograph({('node', 'to', 'node'): ([], [])})
    self.bottom_level = bottom_level
    self.number_of_nodes = len(self.seed_graph.nodes())
    self.number_of_edges = len(self.seed_graph.edges()[0])
    self.selected_edges = None
    self.quotient_number = 0
    self.simplex_id = 0