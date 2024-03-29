<p>
  <img src="https://github.com/TYLERSFOSTER/Graph-HNSW/blob/main/documentation/material/HNSW_tower_00X.jpg" alt="drawing" width="775">
</p>

# Graph-HNSW Application
**Tyler Foster**  *and*  **Abdul Malik**

#### Overview.
This repo collects a refactoring of a critical sub-component of a larger graph machine learning project.

The larger project develops a graph machine learning model that uses message passing across higher-dimensional simplices (directed triangles, directed tetrahedra, etc.) to improve performance at node classification tasks in directed graphs.
Because message passing across higher-dimensional simplices hidden within a given graph only works if we've already identified higher-dimensional simplices implicit in the graph, the forward pass of our graph ML model requires an effective algorithm that searches for higher-dimensional simplices in directed graphs.
The combinatorial explosion endemic to search algorithms in graphs renders naive versions of such an algorithm useless.
In the present repository, we develop an application that takes, as input, a directed graph $$G:\ \ \ \ \ \ G_1\xrightarrow{\ \ \ d_0,d_1\ }G_0,$$
and proceeds to build a descending tower
<p align="center">
  <img src="https://github.com/TYLERSFOSTER/Graph-HNSW/blob/main/documentation/material/towerTOWER.jpg" alt="drawing" width="725">
</p>
where each tier is a graph obtained from the tier above by a sequence of random edge contractions.

The application then searches this tower using a *hierarchical, navigable, small worlds* (*HNSW*) algorithm to leverage knowledge of simplices at one tier in the tower to speed up its search for simplices of the same dimension one tier above.
 
The sub-component of this larger model that we collect in the present repo does not, itself, use any machine learning. It provides a tool for use in a graph machine learning model developed in a repository elsewhere.


Run ```python3 testing.py``` at Linux command line, from the directory '/source', to execute a sequence of tests that run through all the basic functionality of the application.

### Next TODOs:
- Get rid of `simplex_search.Bot.raw` method, and replace all its previous functionality with method `simplicial_set.SSet.dynamic_search`.
- Re-write the memory-intensive `for` loop in `tier.Tier.random_contractions`
- Extensive testing of the `simplex_search.Bot.run` method (in progress).

## Some key ideas
### Basic idea behind the application: A platform for generalizations of binary search to finite directed graphs.
The reason *binary search*-type algorithms are able to speed up search-type tasks on lists is because these algorithms include succesive sub-steps where we greatly reduce the search space. We might call this the "limit" perspective on binary search. There is a dual, "colimit" perspective where we do not descend into smaller and smaller subspaces of our search space, but instead *ascend* through larger and larger contractions of our search space.
<p align="center">
  <img src="https://github.com/TYLERSFOSTER/Graph-HNSW/blob/main/documentation/material/quotient_binary_search_01.jpg" alt="drawing" width="375"/>
  <img src="https://github.com/TYLERSFOSTER/Graph-HNSW/blob/main/documentation/material/quotient_binary_search_02.jpg" alt="drawing" width="280"/>
</p>
<p align="center">
  The setting for binary search as a tower of quotients. | Binary search as movement up through a tower of quotients.
</p>

[...]

### Using topology to manage the combinatorial explosion implicit in graph searches.
[...]

<p align="center">
  <img src="https://github.com/TYLERSFOSTER/Graph-HNSW/blob/main/documentation/material/HNSW_tower_001.jpg" alt="drawing" width="375"/>
</p>
<p align="center">

[...]

<p align="center">
  <img src="https://github.com/TYLERSFOSTER/Graph-HNSW/blob/main/documentation/material/HNSW_tower_002.jpg" alt="drawing" width="380"/>
</p>
<p align="center">

### Number of steps in tower is O(log #G_1)

### Vertex re-indexing issue for graph quotients.
<p align="center">
<img src="https://github.com/TYLERSFOSTER/Graph-HNSW/blob/main/documentation/material/inactive_vertices.jpg" alt="drawing" width="350"/>
</p>

### Degenerate simplices and loops.
If we are unwilling to keep track of degenerate simplices, then it becomess difficult to carry out a graph-HNSW search that finds all simplices implicit in a given graph.
This is because maps in the graph-HNSW tower can map simplices in a given tier of the tower down to degenerate simplices in the tier immediately  below.
This implies that iIf we hope to detect, downstairs, regions of the graph over which simplices might lie upstairs, then we have to be willing to keep track of degenerate simplices as we fill out the simplicial set associated to the downstairs tier.

### The graph-HNSW-based simplex search algorithm
<p align="center">
<img src="https://github.com/TYLERSFOSTER/Graph-HNSW/blob/main/documentation/material/search_order.jpg" alt="drawing" width="500"/>
</p>

[...]

