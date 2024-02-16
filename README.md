# Graph-HNSW Application
Refactor of Graph HNSW scripts

Run ```python3 test.py``` at Linux command line, from the directory '/source', to execute a sequence of tests that run through all the basic functionality of the application.

## Some key ideas
### Basic idea behind the application.
The reason *binary search*-type algorithms are able to speed up search-type tasks on lists is because these algorithms include succesive sub-steps where we greatly reduce the search space, which is to say the list we're searching through. There's a bit of a limit/colimit choice going on here.
<p align="center">
  <img src="https://github.com/TYLERSFOSTER/Graph-HNSW/blob/main/documentation/material/quotient_binary_search_01.jpg" alt="drawing" width="375"/>
</p>
<p align="center">
  **Figure: Binary search as a tower of quotients.**
</p>
<p align="center">
<img src="https://github.com/TYLERSFOSTER/Graph-HNSW/blob/main/documentation/material/quotient_binary_search_02.jpg" alt="drawing" width="280"/>
</p>
[...]

### Vertex re-indexing issue for graph quotients.
<p align="center">
<img src="https://github.com/TYLERSFOSTER/Graph-HNSW/blob/main/documentation/material/inactive_vertices.jpg" alt="drawing" width="350"/>
</p>
