# Optimizing Culinary Processes: A Data-Driven Approach with Functional Object-Oriented Network and Search Algorithms
we optimize culinary processes through the use of Functional Object-Oriented Network (FOON) and leveraging Iterative Deepening Search (IDS) and Greedy Best-First Search (GBFS) guided by heuristic functions, we extract task trees for various dishes, seeking to improve the efficiency and accuracy of culinary operations

Modernizing culinary practices involves the integration of technology and innovative approaches to streamline and enhance the process of preparing dishes. In this paper, we present a data-driven approach to optimize culinary processes through the use of Functional Object-Oriented Network (FOON) and efficient search algorithms. FOON, a structured framework capturing the essence of dish preparation, incorporates functional units, nodes, edges, and task trees. Leveraging Iterative Deepending Search (IDS) and Greedy Best-First Search (GBFS) guided by heuristic functions, we extract task trees for various dishes, seeking to improve the efficiency and accuracy of culinary operations. The performance comparison of these algorithms, considering functional units, computational complexity, and memory usage, sheds light on their efficacy in culinary task optimization.

## Visualization of functional units for two tasks - (a) orange juice and (b) whipped cream

Utilizing [visualization tools](http://foonets.com/), we create illustrative figure above of functional units of two different tasks. The green nodes denote objects, while the red nodes denote motions. These visualizations provide insights into the structure and organization of the FOON, aiding in the understanding and debugging of the program.

![functional_units.png](https://github.com/FarhatBuet14/RoboKitchen-Task-Tree-Retrieval/blob/main/images/functional_units.png)


## Search Algorithms

* __Iterative Deepening Search__: Iterative Deepening Search (IDS) is a depth-first search strategy that systematically explores the search space, incrementing the depth limit iteratively until a solution is found. In our context, the search begins with a depth of 0 and gradually increases until the desired goal state—a task tree where the leaf nodes are available in the kitchen—is reached. While multiple paths to prepare an object may exist, IDS selects the first path encountered.

* __Greedy Best-First Search__: Greedy Best-First Search (GBFS) is a heuristic-based search algorithm that makes decisions based on the evaluation of heuristic functions. It prioritizes exploration based on these heuristics, aiming to reach the goal efficiently. In this project, we utilize two heuristic functions to guide the search:

	* __h1(n)__: Success rate of the motion.
	* __h2(n)__: Number of input objects in the function unit.

The selection of the path during exploration is determined by the evaluation of these heuristic functions.

## Performance Comparison Results

From the performance comparison (see the Table above), it is evident that the number of functional units in the task tree varies for each algorithm based on the goal node. The computational and memory complexities also vary, influenced by the heuristic functions utilized. GBFS with heuristic function h1 generally resulted in a reduced number of functional units compared to IDS and GBFS with heuristic function h2. However, it's important to note that this reduction in functional units might not always align with the actual optimal solution. In terms of computational and memory complexities, both IDS and GBFS demonstrate reasonable performance, with GBFS often requiring slightly less computational time but slightly more memory. The choice of heuristic function also affects the performance in terms of the number of functional units generated. 

![performance%2Bcomparison.png](https://github.com/FarhatBuet14/RoboKitchen-Task-Tree-Retrieval/blob/main/images/performance%2Bcomparison.png)
