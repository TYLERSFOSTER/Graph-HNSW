# Graph-HNSW Application
Refactor of Graph HNSW scripts

Run ```python3 testing.py``` at Linux command line, from the directory '/source', to execute a sequence of tests that run through all the basic functionality of the application.

### Next TODOs:
- Debug the method `raw` for `simplices_search.Bot`. This is suppose to be the base, no-HNSW search. I believe this is due to a failure of `tower.Tower` to built the 1-skeletons of its `tower.Tower.tiers[index].sSet` attributes.
- Solve issue: When edge contraction sampling ratio is too high, error occurs because graph collapses too fast.

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

### Vertex re-indexing issue for graph quotients.
<p align="center">
<img src="https://github.com/TYLERSFOSTER/Graph-HNSW/blob/main/documentation/material/inactive_vertices.jpg" alt="drawing" width="350"/>
</p>
