# Weighted Bipartite b-Matching algorithm

Weighted bipartite matching is one of the widely studied and fundamental problems in combinatorial optimization for modeling data management applications and resource allocation systems.

Given the bipartite undirected graph G = ((*U, V ), E, W *) in which the two disjoint sets of vertices *U* and *V* are fully connected with edges which are weighted based on a score, a bipartite matching algorithm finds a subgraph *M*  ⊆ G such that the total weight *W* is optimal (maximal or minimal, depending on the objective function). 

There are various methods for matching weighted bipartite graphs. One strategy is to exhaustively select all edges over a specific threshold. This strategy is not optimal and can not take constraints into account. 

On the other hand, weighted-bipartite matching suggests an optimal solution as a matching where the sum of weights has an optimal value. This method is known as the assignment problem [3]. The Hungarian algorithm is one of the solutions that solve the assignment problem in polynomial time [3].

Although the maximum weight matching is more efficient than the exhaustive method, it only yields one-to-one links between the vertices. Therefore, the matching subgraph does not consider any more-than-one incident between two edges. To remedy this, the weighted bipartite b-matching (WBbM) algorithm has been proposed which finds the subgraph H = (*(U, V ), E′, W* ) which maximizes ∑W (e) having every vertex u ∈ (U ∪ V) adjacent to at most *b*(u) edges. *b* is the capacity vector of the graph G. 

The following figure (from [2]) shows a bipartite graph with a total weight of 2.2. The maximum matching solution is shown in blue, with the highest score of 1.6. The red degree constraints refer to the capacity of each vertex. 

![bipartite_b_matching_chen_et_al](https://github.com/sinaahmadi/Bipartite_b_matching/blob/master/figures/Chen_et_al_fig1.png)

## Implementation

This repository is a fork of Ahmed et al's work titled "Diverse Weighted Bipartite *b*-Matching" [1]. The original paper studies a complementary goal of balancing diversity and efficiency, therefore it goes beyond the WBbM algorithm. The current repository is a fork and addresses only the WBbM problem. A representative example that has been mentioned in the original work and can be helpful for modeling similar problems is matching academic papers (left of the graph) to possible reviewers (right of the graph). Each reviewer has a minimum number of articles and a maximum number, called capacity. 

### Usage

In order to initialize an object of the `WBbM` class, you need to pass the following arguments to the constructor:
- `num_left`: number of the vertices in the left side of the graph.
- `num_right`: number of the vertices in the right side of the graph. 
- `W`: the weight matrix. Not that in an undirected weighted bipartite graph, edges in the two sides have identical weights. 
- `lda`: minimum papers every reviewer has to review.
- `uda`: maximum papers one reviewer will review with the minimum value of 2. It can also be a list of capacities with different values.
- `ldp`: minimum paper cardinality. 
- `udp`: maximum paper cardinality with the minimum value of 2. It can also be a list of capacities with different values.
- (optional) `LogToConsole=0` enables you to have the computation details of Gorubi in your console.

### Example
In the `main.py`contains an example. A bipartite weighted graph is created with random weights [0-10], using NetworkX, and an optimal solution for the WBbM algorithm is found using the `WBbM` class. The following figures show the output of the algorithm for matching edges over a specific threshold. The figures in left show the graph with a weight over the threshold and those in right show the matched output. 
- Model parameters: lda=0, uda=2, udp=2, ldp=0.
![WBbM_1](https://github.com/sinaahmadi/Bipartite_b_matching/blob/master/figures/figure_0220.png)

- Model parameters: lda=1, uda=2, udp=2, ldp=1.
![WBbM_1](https://github.com/sinaahmadi/Bipartite_b_matching/blob/master/figures/figure_1221.png)

##Requirements
- Python 2.7
- [Gorubi](http://www.gurobi.com/)
- [Numpy](http://www.numpy.org/)
- [NetworkX](http://networkx.github.io/)

### References
[1] Ahmed, Faez, John P. Dickerson, and Mark Fuge. "Diverse weighted bipartite b-matching." arXiv preprint arXiv:1702.07134 (2017).

[2] Chen, Cheng, et al. "Group-aware weighted bipartite b-matching." Proceedings of the 25th ACM International on Conference on Information and Knowledge Management. ACM, 2016.

[3] Munkres, James. "Algorithms for the assignment and transportation problems." Journal of the society for industrial and applied mathematics 5.1 (1957): 32-38.

To discover more about matching algorithms, see [this](https://www.geeksforgeeks.org/maximum-bipartite-matching/), [this](http://www-sop.inria.fr/members/Frederic.Havet/Cours/matching.pdf) and [this](https://www.cse.ust.hk/~golin/COMP572/Notes/Matching.pdf).
