# Graph-HNSW Application
Refactor of Graph HNSW scripts

Run ```python3 testing.py``` at Linux command line, from the directory '/source', to execute a sequence of tests that run through all the basic functionality of the application.

### Next TODOs:
- Build `search.py` module
- Solve issue: When edge contraction sampling ratio is too high, error occurs because graph collapses too fast.

## Some key ideas
### Basic idea behind the application.
The reason *binary search*-type algorithms are able to speed up search-type tasks on lists is because these algorithms include succesive sub-steps where we greatly reduce the search space, which is to say the list we're searching through. There's a bit of a limit/colimit choice going on here.
<p align="center">
  <img src="https://github.com/TYLERSFOSTER/Graph-HNSW/blob/main/documentation/material/quotient_binary_search_01.jpg" alt="drawing" width="375"/>
</p>
<p align="center">
  The setting for binary search as a tower of quotients.
</p>

[...]

<p align="center">
<img src="https://github.com/TYLERSFOSTER/Graph-HNSW/blob/main/documentation/material/quotient_binary_search_02.jpg" alt="drawing" width="280"/>
</p>
<p align="center">
  Binary search as movement up through a tower of quotients.
</p>
[...]

### Vertex re-indexing issue for graph quotients.
<p align="center">
<img src="https://github.com/TYLERSFOSTER/Graph-HNSW/blob/main/documentation/material/inactive_vertices.jpg" alt="drawing" width="350"/>
</p>
